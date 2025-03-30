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
        - Uses standard YAML inventory and applies ansible_host dynamically per host based on tailnet or fallback IP.
        - Implements a two-pass approach to avoid repeated overwrites in multi-group scenarios.
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
        # We'll store merged vars for each host here, in a single pass.
        self.collected_hosts = {}  # e.g. { 'node1': { 'merged': {...}, 'groups': [...]} }

    def verify_file(self, path):
        return path.endswith(('.yml', '.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)
        self.inventory = inventory
        self.loader = loader
        self.path = path

        project_root = os.getcwd()
        hosts_file = os.path.join(project_root, "hosts.yml")
        hostvars_dir = os.path.join(project_root, "host_vars")
        groupvars_dir = os.path.join(project_root, "group_vars")

        with open(path, 'r') as f:
            plugin_config = yaml.safe_load(f) or {}
            plugin_options = plugin_config.get("inventory_plugin", {})
            ignore_hosts = set(plugin_options.get("ignore_hosts", []))
            self.merge_lists = set(plugin_options.get("merge_lists", []))
            self.override = plugin_options.get("override", False) or plugin_options.get("override_ansible_host", False)

        if not os.path.isfile(hosts_file):
            raise AnsibleParserError(f"Missing hosts.yml file at {hosts_file}")

        with open(hosts_file, 'r') as f:
            try:
                inventory_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise AnsibleParserError(f"Invalid YAML in hosts.yml: {e}")

        # We'll define some helper methods:

        def load_vars(file_path):
            try:
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except FileNotFoundError:
                return {}

        def get_host_vars(h):
            return load_vars(os.path.join(hostvars_dir, f"{h}.yml"))

        def get_group_vars(g):
            return load_vars(os.path.join(groupvars_dir, f"{g}.yml"))

        def deep_merge(dict1, dict2, path=""):
            result = {}
            keys = set(dict1) | set(dict2)
            for key in keys:
                full_path = f"{path}.{key}" if path else key
                val1 = dict1.get(key)
                val2 = dict2.get(key)

                if isinstance(val1, dict) and isinstance(val2, dict):
                    result[key] = deep_merge(val1, val2, path=full_path)
                elif isinstance(val1, list) and isinstance(val2, list):
                    if full_path in self.merge_lists:
                        result[key] = val1 + val2
                    else:
                        result[key] = val2
                else:
                    result[key] = val2 if key in dict2 else val1
            return result

        def expand_bracket_expression(h):
            pattern = r"^(.*)\[(\d+):(\d+)\](.*)$"
            m = re.match(pattern, h)
            if m:
                prefix, start, end, suffix = m.groups()
                pad_width = max(len(start), len(end))
                return [f"{prefix}{str(i).zfill(pad_width)}{suffix}" for i in range(int(start), int(end) + 1)]
            else:
                return [h]

        # We'll gather group data in a single pass:

        def process_group(group_name, group_data):
            self.inventory.add_group(group_name)

            # Merge group-level vars from group_vars/<group>.yml + group_data['vars']
            group_merged_vars = get_group_vars(group_name)
            if 'vars' in group_data:
                group_merged_vars = deep_merge(group_merged_vars, group_data['vars'])

            # Add hosts
            hosts = group_data.get("hosts", {})
            for raw_host in hosts:
                for h in expand_bracket_expression(raw_host):
                    if h in ignore_hosts:
                        continue
                    # Make sure host is in the inventory
                    self.inventory.add_host(h, group_name)

                    # Merge group-level and host-level vars
                    host_merged_vars = get_host_vars(h)
                    combined = deep_merge(group_merged_vars, host_merged_vars)

                    # Store or re-merge if host appears in multiple groups
                    if h not in self.collected_hosts:
                        self.collected_hosts[h] = combined
                    else:
                        # re-merge old + new
                        old = self.collected_hosts[h]
                        new = deep_merge(old, combined)
                        self.collected_hosts[h] = new

            # children
            children = group_data.get("children", {})
            for subgroup, subgroup_data in children.items():
                process_group(subgroup, subgroup_data)
                self.inventory.add_child(group_name, subgroup)

        # top-level group iteration
        for gname, gdata in inventory_data.items():
            process_group(gname, gdata)

        # SECOND PASS: set ansible_host exactly once per host

        def resolve_ansible_host(h, combined_vars):
            tailscale = combined_vars.get("tailscale", {})
            tailnet = tailscale.get("tailnet")
            enabled = tailscale.get("enabled")
            ip_address = combined_vars.get("ip_address")

            if enabled and tailnet:
                fqdn = f"{h}.{tailnet}"
                # print(f"[DEBUG] Setting ansible_host for {h} using tailnet: {fqdn}")
                return fqdn
            elif ip_address:
                # print(f"[DEBUG] Setting ansible_host for {h} using ip_address: {ip_address}")
                return ip_address
            else:
                # print(f"[WARNING] No ip_address or tailnet for {h}; fallback to hostname")
                return h

        for h, merged_vars in self.collected_hosts.items():
            # set all normal merged vars
            for k, v in merged_vars.items():
                self.inventory.set_variable(h, k, v)

            # only now do we set ansible_host, once
            maybe_ansible = resolve_ansible_host(h, merged_vars)
            if maybe_ansible:
                # if override is false and ansible_host already set, skip
                existing = self.inventory.get_host(h).get_vars().get("ansible_host")
                if existing and not self.override:
                    print(f"[DEBUG] Not overriding existing ansible_host for {h}: {existing}")
                else:
                    self.inventory.set_variable(h, "ansible_host", maybe_ansible)
