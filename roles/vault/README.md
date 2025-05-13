# Vault

This will install vault on targeted nodes. This role requires an inventory group named `vault` with the hosts where Vault must be installed.
Furthermore, a variable `vault_init_node` is required which will tell which node must be used to initialize vault.

Example for `hosts.yml`

```yaml
vault:
  hosts:
    node1:
    node2:
    node3:
    node4:
  vars:
    vault_init_node: node1
```

## Configuration

Vault can be configured using the `vault` configuration key.
These are the defaults:

```yaml
vault:
  data_dir: /opt/vault
  tls:
    enabled: false
    ca: /etc/vault.d/chain.crt
    crt: /etc/vault.d/server.crt
    key: /etc/vault.d/server.key
```
