# Ansible TPI

This repository holds the Ansible configuration to manage your Turing PI.

- [Usage](#usage)
- [Update Inventory](#update-inventory)
- [Ansible Vault Password](#ansible-vault-password)
- [host\_vars](#host_vars)
- [Playbooks](#playbooks)
- [Roles](#roles)
- [SSH Key Generation](#ssh-key-generation)
- [Provision](#provision)
  - [Provision/Bootstrap Server](#provisionbootstrap-server)

## Usage

In order to use this repository the following requirements must be configured first.

<!-- no toc -->
- [Update Inventory](#update-inventory)
- [Set Ansible Vault Password](#ansible-vault-password)
- [Generate SSH keys](#ssh-key-generation)
- [host_vars]

## Update Inventory

Update your Ansible inventory `hosts.yml` accordingly to your configuration.
After you configure your Ansible Vault Password, you can encrypt your BMC root password.

You can find examples for inventories in the [.config](./.config) directory.

## Ansible Vault Password

Use the following command to configure or update the `Ansible Vault Password`.
Replace `PASSWORD` with your actual password.

```shell
echo 'PASSWORD' > ~/.ansible_vault_pass
```

## host_vars

Copy `.config/node.yml` to `host_vars/{NODE_HOSTNAME}.yml` and update the IP number for each host.

## Playbooks

| Playbook                                   | Description                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| [bootstrap](./playbooks/bootstrap.yml)     | Bootstrap Node                                                             |
| [flash-nodes](./playbooks/flash-nodes.yml) | Flash node(s), this playbook will also install the `tpi` cli on localhost. |
| [ssh](./playbooks/ssh.yml)                 | Configure SSH                                                              |
| [tpi](./playbooks/tpi.yml)                 | Install `tpi` client                                                       |

## Roles

> IMPORTANT
>
> The Flashing of a CM4 module has not been tested.

Read the documentation of the Role to get more information regarding configuration or variables.

- [bootstrap](./roles/bootstrap/README.md)
- [flash](./roles/flash/README.md)
- [ssh](./roles/ssh/README.md)
- [tpi](./roles/tpi/README.md)

## SSH Key Generation

To generate the required ssh keys run the following command.
This command will also intall the generate SSH key for the linked BMC into the BMC.

```shell
ansible-playbook playbooks/ssh.yml
```

If new keys are required, you can re-run the same playbook with the following option to regenerate
all the keys and install the new ones.

```shell
ansible-playbook playbooks/ssh.yml -e ssh_overwrite=true
```

## Provision

In order to provision any server, `cloud-init` is used to bootstrap the server,
and configure users with SSH keys for this repository to work properly.
This process will generate new SSH keys if they are not found.

The default user is assumed to be `ubuntu`. This is configured in `group_vars/all.yml`.
If no SSH key is found for the `ubuntu` user a new one will be created.

The following additional users are created.

- `ansible`: User which runs the `ansible` playbooks, configured in `group_vars/all.yml`.

> SSH Filenames
>
> The ssh keys are prefixed with the name configured in the hosts file under `tpi.name`.
> This is the name given to the BMC by the user and used as a prefix.
>
> The BMC will also be given its own SSH key.

### Provision/Bootstrap Server

Run the following command to bootstrap a server, replace `{LIMIT}` with either a groupname
or specific server from the inventory.

```shell
ansible-playbook -l {LIMIT} playbooks/bootstrap.yml
```
