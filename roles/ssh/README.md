# SSH Keys

The role will generate SSH keys. The following keys will be generated.
The key for each BMC will be deployed to their BMC and entries will be created in the SSH known_hosts configuration.

## Users

- ubuntu
- ansible

## hosts

- All configured BMC's in the inventory.
