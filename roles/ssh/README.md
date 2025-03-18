# SSH Keys

The role will generate SSH keys. The following keys will be generated.
The key for each BMC will be deployed to their BMC and entries will be created in the SSH known_hosts configuration.

## Users

- ubuntu
- ansible

## hosts

- All configured BMC's in the inventory.

## Tasks

The following tasks are available for import and use by other roles, or playbooks.

- [Users](#users)
- [hosts](#hosts)
- [Tasks](#tasks)
  - [known\_hosts](#known_hosts)
- [config](#config)

### known_hosts

This task will add a host to the known_hosts. The variable `host` must be provided with the hostname which must be added.

```yaml
- name: Add known_host
  vars:
    host: "{{ bmc_host }}"
  ansible.builtin.include_role:
    name: ssh
    tasks_from: known_hosts.yml
```

## config

This task will add a host to the SSH config.

The following variables must be provided.

| Variable | Desription                  |
| -------- | --------------------------- |
| host     | Host entry ID               |
| hostname | Hostname of the server      |
| username | SSH Username                |
| key      | Path to the SSH private key |

```yaml
 - name: Add config
  vars:
    host: "{{ user }}"
    hostname: "{{ bmc_host }}"
    username: "{{ bmc_user }}"
    key: "{{ bmc_key }}"
  ansible.builtin.include_role:
    name: ssh
    tasks_from: config.yml
```
