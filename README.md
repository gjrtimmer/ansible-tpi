# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

- [Usage](#usage)
  - [Ansible Vault Password](#ansible-vault-password)
- [Playbooks](#playbooks)
- [Roles](#roles)
- [Provision New Server](#provision-new-server)
  - [Provision/Bootstrap Server](#provisionbootstrap-server)
    - [SSH Key Generation](#ssh-key-generation)
    - [Use Existing SSH Keys](#use-existing-ssh-keys)

## Usage

In order to use this repository the following requirements must be configured first.

### Ansible Vault Password

Use the following command to configure or update the `Ansible Vault Password`.
Replace `PASSWORD` with your actual password.

```shell
echo 'PASSWORD' > ~/.ansible_vault_pass
```

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

In order to provision any server, `cloud-init` is used to bootstrap the server,
and configure users with SSH keys for this repository to work properly.
This process will generate new SSH keys if they are not found.
If you want to use your own SSH keys, please see the nexy section [Use Existing SSH Keys](#use-existing-ssh-keys).

The default user is assumed to be `ubuntu`. This is configured in `group_vars/all.yml`.
If no SSH key is found for the `ubuntu` user a new one will be created.

The following additional users are created.

- `ansible`: User which runs the `ansible` playbooks, configured in `group_vars/all.yml`.

> SSH Filenames
>
> The ssh keys are prefixed with the name configured in the hosts file under `tpi.name`.
> This is the name given to the BMC by the user and used as a prefix.

### Provision/Bootstrap Server

Run the following command to bootstrap a server, replace `{LIMIT}` with either a groupname
or specific server from the inventory.

```shell
ansible-playbook -l {LIMIT} playbooks/bootstrap.yml
```

#### SSH Key Generation

If for some reason only the SSH key generation is required, run the provision playbook
but limit it to only run with the tag `ssh`.

```shell
ansible-playbook -l {LIMIT} -t ssh playbooks/bootstrap.yml
```

#### Use Existing SSH Keys

Copy your existing Public/Private SSH keys you want to use to the following locations.
Where `{PREFIX}` is replaced with the name configured in `hosts.yml` as the `tpi.name`
key of the BMC.

Example; if the `tpi.name` key is `tpi`, then the private key for the `ansible` user
will be expected at `~/.ssh/tpi/tpi.ansible.key`.
