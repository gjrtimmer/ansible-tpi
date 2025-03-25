# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

- [Usage](#usage)
- [Data Persistence](#data-persistence)
- [Provision Nodes](#provision-nodes)
- [Commands](#commands)
- [Playbooks](#playbooks)
- [Roles](#roles)

## Usage

In order to use this repository read the [setup](./docs/SETUP.md) documentation first.

## Data Persistence

The container will create the two following directories on the host to manage the persistent data.

- $HOME/.tpi
- $HOME/.ssh/tpi

If you are using a previous version of this repository, data should be automatically migrated to this new configuration.
This is to ensure that we keep the user data, like inventory, group_vars, host_vars in the case the user resets the repository
or removes the repository from the host all together.

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
