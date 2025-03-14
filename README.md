# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

> IMPORTANT: SSH
>
> To ensure everythings works your hosts `.ssh` folder is mounted Read/Write!

- [Usage](#usage)
  - [Ansible Vault Password](#ansible-vault-password)
  - [SSH Key Configuration](#ssh-key-configuration)
    - [New Key](#new-key)
    - [Use Existing Key](#use-existing-key)
- [Playbooks](#playbooks)
- [Roles](#roles)
- [Provision New Server](#provision-new-server)

## Usage

In order to use this repository the following requirements must be configured first.

- [Usage](#usage)
  - [Ansible Vault Password](#ansible-vault-password)
  - [SSH Key Configuration](#ssh-key-configuration)
    - [New Key](#new-key)
    - [Use Existing Key](#use-existing-key)
- [Playbooks](#playbooks)
- [Roles](#roles)
- [Provision New Server](#provision-new-server)

### Ansible Vault Password

Use the following command to configure or update the `Ansible Vault Password`.
Replace `PASSWORD` with your actual password.

```shell
echo 'PASSWORD' > ~/.ansible_vault_pass
```

### SSH Key Configuration

In order to provision any server with this project a SSH key needs to be present.

#### New Key

#### Use Existing Key



## Playbooks

| Playbook                                   | Description                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| [flash-nodes](./playbooks/flash-nodes.yml) | Flash node(s), this playbook will also install the `tpi` cli on localhost. |
| [tpi-cli](./playbooks/tpi-cli.yml)         | Install `tpi` client                                                       |

## Roles

> IMPORTANT
>
> The Flashing of a CM4 module has not been tested.

Read the documentation of the Role to get more information regarding configuration or variables.

- [flash-nodes](./roles/flash/README.md)
- [tpi-cli](./roles/tpi-cli/)

## Provision New Server

