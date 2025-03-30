from ansible.plugins.inventory import BaseInventoryPlugin  # type: ignore
from ansible.errors import AnsibleParserError  # type: ignore
import os
import yaml

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
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'dynamic'

    def verify_file(self, path):
        return path.endswith(('.yml', '.yaml'))

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        # Look for hosts.yml at the project root
        project_root = os.getcwd()
        hosts_file = os.path.join(project_root, "hosts.yml")
        hostvars_dir = os.path.join(project_root, "host_vars")
        groupvars_dir = os.path.join(project_root, "group_vars")

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

        def resolve_ansible_host(hostname, combined_vars):
            if "ansible_host" in combined_vars:
                return None

            tailscale = combined_vars.get("tailscale", {})
            tailnet = tailscale.get("tailnet", "")
            enabled = tailscale.get("enabled", False)
            ip_address = combined_vars.get("ip_address")

            if tailnet and enabled:
                return f"{hostname}.{tailnet}"
            elif ip_address:
                return ip_address
            else:
                print(f"[WARNING] No ip_address defined for host '{hostname}', and Tailscale not enabled. ansible_host will fallback to hostname.")
                return hostname

        def process_group(group_name, group_data):
            self.inventory.add_group(group_name)
            group_vars = get_group_vars(group_name)
            if 'vars' in group_data:
                group_vars.update(group_data['vars'])

            hosts = group_data.get("hosts", {})
            for host in hosts:
                self.inventory.add_host(host, group_name)
                host_vars = get_host_vars(host)
                combined_vars = {**group_vars, **host_vars}

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
