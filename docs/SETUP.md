# Setup

Complete the following steps to initialize this repository.

<!-- no toc -->
1. [Update Inventory](#update-inventory)
2. [Set Ansible Vault Password](#ansible-vault-password)
3. [host_vars](#host_vars)
4. [Generate SSH keys](./docs/SSH.md)

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

Copy `.config/node.yml` to `host_vars/{NODE_HOSTNAME}.yml` and set the IP number for each host.
The name of the file must match the hostname configure in the inventory.

## DHCP Reservation

If you want to use router assigned DHCP, I advise to use the following workflow.
The reason the flashing of a node and the bootstrap was separated is to allow a user
to control the workflow on how to configure a node. DHCP is such an use-case.

1. Flash Node
2. Boot Node
3. Configure DHCP reservation in your router
4. Power Off node

From this point on, you can continue with the [bootstrap](./PROVISION.md#bootstrap-server) of your node.
