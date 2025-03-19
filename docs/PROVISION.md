# Provision

- [Flash Node](#flash-node)
- [Bootstrap Server](#bootstrap-server)
  - [Login](#login)

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

## Flash Node

To flash a node use the following command.

```shell
ansible-playground -l {LIMIT} playbooks/flash.yml -e flash_node=true
```

## Bootstrap Server

Run the following command to bootstrap a server, replace `{LIMIT}` with either a groupname
or specific server from the inventory.

```shell
ansible-playbook -l {LIMIT} playbooks/bootstrap.yml
```

### Login

The `cloud-init` process will configure the default `ubuntu` user with password `turing`.
Both the `ubuntu` user and `ansible` user are configured with the generated SSH keys for login.
