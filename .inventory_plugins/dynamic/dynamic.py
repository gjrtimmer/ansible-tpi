# Copyright (c) 2023
# Licensed under the terms of the MIT license.

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

        # 1) Load plugin config via the Ansible DataLoader
        plugin_config = self._load_file_as_data(path)
        plugin_options = plugin_config.get('inventory_plugin', {})
        self.ignore_hosts = set(plugin_options.get('ignore_hosts', []))
        self.merge_lists = set(plugin_options.get('merge_lists', []))
        self.override = plugin_options.get('override', False) or plugin_options.get('override_ansible_host', False)

        if not os.path.isfile(hosts_file):
            raise AnsibleParserError(f"Missing hosts.yml file at {hosts_file}")

        # 2) Load the main inventory data (hosts.yml) with vault support
        inventory_data = self._load_file_as_data(hosts_file)

        # Helper function to load YAML with vault support
        def load_vars(file_path):
            try:
                return self._load_file_as_data(file_path)
            except FileNotFoundError:
                return {}

        def deep_merge(d1, d2):
            result = {}
            all_keys = set(d1) | set(d2)
            for k in all_keys:
                v1 = d1.get(k)
                v2 = d2.get(k)
                if isinstance(v1, dict) and isinstance(v2, dict):
                    result[k] = deep_merge(v1, v2)
                elif isinstance(v1, list) and isinstance(v2, list):
                    if k in self.merge_lists:
                        # lists are appended if in merge_lists
                        result[k] = v1 + v2
                    else:
                        # otherwise overwritten by second
                        result[k] = v2
                else:
                    # plain scalars or mismatched types are overwritten by second
                    result[k] = v2 if k in d2 else v1
            return result

        def get_host_vars(h):
            """Load host variables from host_vars/<h>.yml or host_vars/<h>/*.yml."""
            merged_data = {}
            file_yml = os.path.join(hostvars_dir, f'{h}.yml')
            file_yaml = os.path.join(hostvars_dir, f'{h}.yaml')

            # Check single-file host vars
            if os.path.isfile(file_yml):
                merged_data = deep_merge(merged_data, load_vars(file_yml))
            elif os.path.isfile(file_yaml):
                merged_data = deep_merge(merged_data, load_vars(file_yaml))

            # Also check if host_vars/<h>/ exists. If so, merge all .yml/.yaml files.
            host_subdir = os.path.join(hostvars_dir, h)
            if os.path.isdir(host_subdir):
                for filename in sorted(os.listdir(host_subdir)):
                    if filename.endswith(('.yml', '.yaml')):
                        subfile = os.path.join(host_subdir, filename)
                        merged_data = deep_merge(merged_data, load_vars(subfile))

            return merged_data

        def get_group_vars(g):
            """Load group variables from group_vars/<g>.yml or group_vars/<g>/*.yml."""
            merged_data = {}

            # primary file: group_vars/<g>.yml or <g>.yaml
            file_yml = os.path.join(groupvars_dir, f'{g}.yml')
            file_yaml = os.path.join(groupvars_dir, f'{g}.yaml')
            if os.path.isfile(file_yml):
                merged_data = deep_merge(merged_data, load_vars(file_yml))
            elif os.path.isfile(file_yaml):
                merged_data = deep_merge(merged_data, load_vars(file_yaml))

            # also check if group_vars/<g>/ exists. if so, merge all .yml/.yaml files.
            group_subdir = os.path.join(groupvars_dir, g)
            if os.path.isdir(group_subdir):
                for filename in sorted(os.listdir(group_subdir)):
                    if filename.endswith(('.yml', '.yaml')):
                        subfile = os.path.join(group_subdir, filename)
                        merged_data = deep_merge(merged_data, load_vars(subfile))

            return merged_data

        def expand_bracket_expression(h):
            pat = r"^(.*)\[(\d+):(\d+)\](.*)$"
            match = re.match(pat, h)
            if match:
                prefix, start, end, suffix = match.groups()
                pad_width = max(len(start), len(end))
                return [f"{prefix}{str(i).zfill(pad_width)}{suffix}" for i in range(int(start), int(end) + 1)]
            else:
                return [h]

        def process_group(gname, gdata):
            # add the group to inventory
            self.inventory.add_group(gname)

            # group-level merges
            group_level = get_group_vars(gname)
            if 'vars' in gdata:
                merged = deep_merge(group_level, gdata['vars'])
            else:
                merged = group_level

            # handle hosts
            hosts_block = gdata.get('hosts', {})
            if isinstance(hosts_block, list):
                # if user used list syntax, convert to dict
                tmp = {}
                for item in hosts_block:
                    tmp[item] = {}
                hosts_block = tmp

            for raw_host in hosts_block:
                for actual_host in expand_bracket_expression(raw_host):
                    if actual_host in self.ignore_hosts:
                        continue

                    self.inventory.add_host(actual_host, gname)

                    host_def = hosts_block[raw_host]
                    if not isinstance(host_def, dict):
                        host_def = {}

                    hv = get_host_vars(actual_host)
                    combined_gh = deep_merge(merged, host_def)
                    final_merged = deep_merge(combined_gh, hv)

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

        # if 'all' group present, process it first
        all_data = inventory_data.pop('all', None)
        if all_data:
            process_group('all', all_data)

        # process other top-level groups
        for gname, gdata in inventory_data.items():
            process_group(gname, gdata)

        # pass 2: finalize
        for host, merged_vars in self.collected_hosts.items():
            # set all normal variables first
            for k, v in merged_vars.items():
                self.inventory.set_variable(host, k, v)

            existing = self.inventory.get_host(host).get_vars().get('ansible_host')
            if existing and not self.override:
                continue

            # compute ansible_host
            maybe_ansible = self._resolve_ansible_host(host, merged_vars)
            if maybe_ansible:
                self.inventory.set_variable(host, 'ansible_host', maybe_ansible)

    def _load_file_as_data(self, file_path):
        """Use Ansible DataLoader (and manual file reading) to parse vault-encrypted YAML."""
        if not os.path.isfile(file_path):
            return {}
        try:
            with open(file_path, 'rb') as f:
                raw_content = f.read()
            data = self.loader.load(raw_content, file_name=file_path)
            return data or {}
        except Exception as e:
            raise AnsibleParserError(f"Invalid YAML in {file_path}: {e}")

    def _resolve_ansible_host(self, hostname, final_vars):
        """Compute ansible_host based on tailscale or ip_address."""
        tailscale = final_vars.get('tailscale', {})
        tailnet = tailscale.get('tailnet')
        enabled = tailscale.get('enabled')
        ip_address = final_vars.get('ip_address')

        if enabled and tailnet:
            return f"{hostname}.{tailnet}"
        elif ip_address:
            return ip_address
        else:
            return hostname
