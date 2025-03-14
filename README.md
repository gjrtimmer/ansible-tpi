# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

> IMPORTANT: SSH
>
> To ensure everythings works your hosts `.ssh` folder is mounted Read/Write!


## Playbooks

| Playbook                                   | Description                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| [flash-nodes](./playbooks/flash-nodes.yml) | Flash node(s), this playbook will also install the `tpi` cli on localhost. |
| [tpi-cli](./playbooks/tpi-cli.yml)         | Install `tpi` client                                                       |

## Roles

Read the documentation of the Role to get more information regarding configuration or variables.

- [flash-nodes](./roles/flash/README.md)
- [tpi-cli](./roles/tpi-cli/)
