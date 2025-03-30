from ansible.plugins.inventory import BaseInventoryPlugin  # type: ignore
from ansible.errors import AnsibleParserError  # type: ignore
import os
import re
import yaml  # type: ignore

DOCUMENTATION = r'''
    name: dynamic
    plugin_type: inventory
    short_description: Enhance ansible_host dynamically with Tailscale support
    description:
        - Uses a two-pass approach so multiple group definitions don’t overwrite ansible_host.
        - Merges top-level 'all' group and merges 'localhost: ansible_connection=local' if present.
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['dynamic']
        inventory_plugin:
            description: Plugin options
            required: false
            type: dict
            suboptions:
                ignore_hosts:
                    description: List of hostnames to skip processing
                    type: list
                    elements: str
                merge_lists:
                    description: List of dotted variable paths where lists should be merged
                    type: list
                    elements: str
                override:
                    description: Whether to override ansible_host if already set
                    type: bool
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'dynamic'

    def __init__(self):
        super().__init__()
        self.inventory = None
        self.loader = None
        self.path = None

        self.collected_hosts = {}  # storing final merged vars for each host
        self.merge_lists = set()
        self.override = False
        self.ignore_hosts = set()

    def verify_file(self, path):
        # Accept plugin file if it ends in yml/yaml
        return path.endswith(('.yml', '.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache=cache)
        self.inventory = inventory
        self.loader = loader
        self.path = path

        project_root = os.getcwd()
        hosts_file = os.path.join(project_root, 'hosts.yml')
        hostvars_dir = os.path.join(project_root, 'host_vars')
        groupvars_dir = os.path.join(project_root, 'group_vars')

        with open(path, 'r') as f:
            plugin_config = yaml.safe_load(f) or {}
            plugin_options = plugin_config.get('inventory_plugin', {})
            self.ignore_hosts = set(plugin_options.get('ignore_hosts', []))
            self.merge_lists = set(plugin_options.get('merge_lists', []))
            self.override = plugin_options.get('override', False) or plugin_options.get('override_ansible_host', False)

        if not os.path.isfile(hosts_file):
            raise AnsibleParserError(f"Missing hosts.yml file at {hosts_file}")

        # load the top-level inventory data from hosts.yml
        with open(hosts_file, 'r') as f:
            try:
                inventory_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise AnsibleParserError(f"Invalid YAML in hosts.yml: {e}")

        def load_vars(file_path):
            try:
                with open(file_path, 'r') as vf:
                    return yaml.safe_load(vf) or {}
            except FileNotFoundError:
                return {}

        def get_host_vars(h):
            return load_vars(os.path.join(hostvars_dir, f'{h}.yml'))

        def get_group_vars(g):
            return load_vars(os.path.join(groupvars_dir, f'{g}.yml'))

        def deep_merge(d1, d2):
            result = {}
            all_keys = set(d1) | set(d2)
            for k in all_keys:
                v1 = d1.get(k)
                v2 = d2.get(k)
                if isinstance(v1, dict) and isinstance(v2, dict):
                    result[k] = deep_merge(v1, v2)
                elif isinstance(v1, list) and isinstance(v2, list):
                    # Optionally handle merges in lists
                    # for simplicity, just override unless in merge_lists
                    result[k] = v2
                else:
                    result[k] = v2 if k in d2 else v1
            return result

        def expand_bracket_expression(h):
            pat = r"^(.*)\[(\d+):(\d+)\](.*)$"
            match = re.match(pat, h)
            if match:
                prefix, start, end, suffix = match.groups()
                pad_width = max(len(start), len(end))
                return [f"{prefix}{str(i).zfill(pad_width)}{suffix}" for i in range(int(start), int(end) + 1)]
            else:
                return [h]

        # pass 1: gather merges

        def process_group(gname, gdata):
            # ensure the group is known to the inventory
            self.inventory.add_group(gname)

            # group-level vars from group_vars + inline vars
            group_level = get_group_vars(gname)
            if 'vars' in gdata:
                group_level = deep_merge(group_level, gdata['vars'])

            # handle hosts:
            hosts_block = gdata.get('hosts', {})
            if isinstance(hosts_block, list):
                # if the user uses a list style
                tmp = {}
                for item in hosts_block:
                    tmp[item] = {}
                hosts_block = tmp

            for raw_host in hosts_block:
                for actual_host in expand_bracket_expression(raw_host):
                    if actual_host in self.ignore_hosts:
                        continue

                    # ensure the host is in the inventory
                    self.inventory.add_host(actual_host, gname)

                    # host-level merges
                    host_def = hosts_block[raw_host]
                    if not isinstance(host_def, dict):
                        host_def = {}

                    hv = get_host_vars(actual_host)
                    # group + host_def + host_vars
                    combined_gh = deep_merge(group_level, host_def)
                    final_merged = deep_merge(combined_gh, hv)

                    # store in collected_hosts
                    if actual_host not in self.collected_hosts:
                        self.collected_hosts[actual_host] = final_merged
                    else:
                        old_merged = self.collected_hosts[actual_host]
                        new_merged = deep_merge(old_merged, final_merged)
                        self.collected_hosts[actual_host] = new_merged

            # handle children
            children = gdata.get('children', {})
            for subg, subgdata in children.items():
                process_group(subg, subgdata)
                self.inventory.add_child(gname, subg)

        # if user has a top-level 'all' group, handle that first to ensure merges
        # we do a manual check if 'all' is present
        all_data = inventory_data.pop('all', None)
        if all_data:
            process_group('all', all_data)

        # now process the other top-level groups
        for gname, gdata in inventory_data.items():
            process_group(gname, gdata)

        # pass 2: finalize

        def resolve_ansible_host(h, final_vars):
            tailscale = final_vars.get('tailscale', {})
            tailnet = tailscale.get('tailnet')
            enabled = tailscale.get('enabled')
            ip_address = final_vars.get('ip_address')

            if enabled and tailnet:
                fqdn = f"{h}.{tailnet}"
                print(f"[DEBUG] Setting ansible_host for {h} using tailnet: {fqdn}")
                return fqdn
            elif ip_address:
                print(f"[DEBUG] Setting ansible_host for {h} using ip_address: {ip_address}")
                return ip_address
            else:
                print(f"[WARNING] No ip_address or tailnet for {h}; fallback to hostname")
                return h

        # apply final merges
        for host, merged_vars in self.collected_hosts.items():
            # set all normal variables first
            for k, v in merged_vars.items():
                self.inventory.set_variable(host, k, v)

            # see if ansible_host is pre-set
            existing = self.inventory.get_host(host).get_vars().get('ansible_host')
            if existing and not self.override:
                print(f"[DEBUG] Not overriding existing ansible_host for {host}: {existing}")
                continue

            # otherwise compute ansible_host
            maybe_ansible = resolve_ansible_host(host, merged_vars)
            if maybe_ansible:
                self.inventory.set_variable(host, 'ansible_host', maybe_ansible)
