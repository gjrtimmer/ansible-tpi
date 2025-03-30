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
        - Uses standard YAML inventory and applies ansible_host dynamically per host based on tailnet or fallback IP
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

    def verify_file(self, path):
        return path.endswith(('.yml', '.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        project_root = os.getcwd()
        hosts_file = os.path.join(project_root, "hosts.yml")
        hostvars_dir = os.path.join(project_root, "host_vars")
        groupvars_dir = os.path.join(project_root, "group_vars")

        with open(path, 'r') as f:
            plugin_config = yaml.safe_load(f)
            plugin_options = plugin_config.get("inventory_plugin", {})
            ignore_hosts = set(plugin_options.get("ignore_hosts", []))
            merge_lists = set(plugin_options.get("merge_lists", []))
            override = plugin_options.get("override", False) or plugin_options.get("override_ansible_host", False)

        if not os.path.isfile(hosts_file):
            raise AnsibleParserError(f"Missing hosts.yml file at {hosts_file}")

        with open(hosts_file, 'r') as f:
            try:
                inventory_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise AnsibleParserError(f"Invalid YAML in hosts.yml: {e}")

        def load_vars(file_path):
            try:
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except FileNotFoundError:
                return {}

        def get_host_vars(host):
            return load_vars(os.path.join(hostvars_dir, f"{host}.yml"))

        def get_group_vars(group):
            return load_vars(os.path.join(groupvars_dir, f"{group}.yml"))

        def deep_merge(dict1, dict2, path=""):
            result = dict1.copy()
            for key, value in dict2.items():
                full_path = f"{path}.{key}" if path else key
                if key in result:
                    if isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = deep_merge(result[key], value, path=full_path)
                    elif isinstance(result[key], list) and isinstance(value, list):
                        if full_path in merge_lists:
                            result[key] = result[key] + value
                        else:
                            result[key] = value
                    else:
                        result[key] = value
                else:
                    result[key] = value
            return result

        def expand_bracket_expression(hostname):
            pattern = r"^(.*)\[(\d+):(\d+)\](.*)$"
            match = re.match(pattern, hostname)
            if match:
                prefix, start, end, suffix = match.groups()
                pad_width = max(len(start), len(end))
                return [f"{prefix}{str(i).zfill(pad_width)}{suffix}" for i in range(int(start), int(end)+1)]
            else:
                return [hostname]

        def resolve_ansible_host(hostname, combined_vars):
            # if not override_ansible_host and "ansible_host" in combined_vars:
            #     print(f"[DEBUG] Skipping ansible_host for {hostname} (already defined: {combined_vars['ansible_host']})")
            #     return None
            if not override and "ansible_host" in combined_vars:
                print(f"[DEBUG] Skipping ansible_host for {hostname} (already defined: {combined_vars['ansible_host']})")
                return None

            tailscale = combined_vars.get("tailscale", {})
            tailnet = tailscale.get("tailnet", "")
            enabled = tailscale.get("enabled", None)
            ip_address = combined_vars.get("ip_address")

            if enabled is True and tailnet:
                return f"{hostname}.{tailnet}"
            elif ip_address:
                return ip_address
            elif enabled is None:
                print(f"[WARNING] No ip_address defined for host '{hostname}', and Tailscale config not defined. ansible_host will fallback to hostname.")
            return hostname

        def process_group(group_name, group_data):
            self.inventory.add_group(group_name)
            group_vars = get_group_vars(group_name)
            if 'vars' in group_data:
                group_vars.update(group_data['vars'])

            hosts = group_data.get("hosts", {})
            for raw_host in hosts:
                for host in expand_bracket_expression(raw_host):
                    if host in ignore_hosts:
                        continue
                    self.inventory.add_host(host, group_name)
                    host_vars = get_host_vars(host)
                    combined_vars = deep_merge(group_vars, host_vars)

                    resolved_host = resolve_ansible_host(host, combined_vars)
                    if resolved_host is not None:
                        self.inventory.set_variable(host, "ansible_host", resolved_host)

                    if "ansible_connection" not in combined_vars:
                        self.inventory.set_variable(host, "ansible_connection", "ssh")

                    for key, val in combined_vars.items():
                        self.inventory.set_variable(host, key, val)

            children = group_data.get("children", {})
            for subgroup, subgroup_data in children.items():
                process_group(subgroup, subgroup_data)
                self.inventory.add_child(group_name, subgroup)

        for group_name, group_data in inventory_data.items():
            process_group(group_name, group_data)
