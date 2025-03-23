# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

- [Usage](#usage)
- [Provision Nodes](#provision-nodes)
- [Commands](#commands)
- [Playbooks](#playbooks)
- [Roles](#roles)

## Usage

In order to use this repository read the [setup](./docs/SETUP.md) documentation first.

## Provision Nodes

[Start provisiong node with the following documentation](./docs/PROVISION.md).

## Commands

See [Commands](./docs/COMMANDS.md) for an entire list of commands.

## Playbooks

| Playbook                                   | Description                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| [bootstrap](./playbooks/bootstrap.yml)     | Bootstrap Node                                                             |
| [flash-nodes](./playbooks/flash-nodes.yml) | Flash node(s), this playbook will also install the `tpi` cli on localhost. |
| [shutdown](./playbooks/shutdown.yml)       | Shutdown Node(s)                                                           |
| [ssh](./playbooks/ssh.yml)                 | Configure SSH                                                              |
| [tpi](./playbooks/tpi.yml)                 | Install `tpi` client                                                       |

## Roles

> IMPORTANT
>
> The Flashing of a CM4 module has not been tested.

Read the documentation of the Role to get more information regarding configuration or variables.

- [bootstrap](./roles/bootstrap/README.md)
- [flash](./roles/flash/README.md)
- [server](./roles/server/README.md)
- [ssh](./roles/ssh/README.md)
- [tpi](./roles/tpi/README.md)
