# TPI Flash

Role to flash an OS to a TuringPI node, this role supports flashing a RK1 module or a Raspberry Compute Module 4.
After flashing this Ansible role will turn off the nodes in case the user wants to bootstrap the nodes first with
cloud-init before booting the nodes for the first time.

> **IMPORTANT**
>
> Please note that the tpi user/password is written to the hosts file, this is required because on some platforms like MacOS
> Ansible is unable to get a `input reader` and therefor the user/password must be provided to run the `tpi` commands.
>
> Please ensure the password is encrypted with `Ansible Vault` in your inventory file.

## Requirements

- `tpi` command to be installed locally
- BMC SDCard: This role expects that a SDCard is present in the BMC, if there is no SDCard, you can flash remote by setting `flash_sdcard=false`
- hosts.yml: configuration options must be present

This role does requires certain specifics from the inventory configuration.

Each hosts MUST have the following configuration present.

| Variable | Type   | R/O      | Description                                                                                                                                    |
| -------- | ------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| bmc      | string | Requried | Inventory hostname reference of the BMC where this node is located, this allows for multiple Turing PIs to be controlled by a single inventory |
| slot     | number | Required | Number of the TPI slot 1-4                                                                                                                     |
| type     | string | Required | Type of Node: Either RK1 or CM4; type NVIDIA is allowed to, however, this is not yet supported by this role                                    |
| root     | string | Optional | Root device where to move the root filesystem; example: `/dev/nvme0n1`                                                                         |

### Example Inventories

Example inventories can be found in the [.config](./.config) directory.

## Role Variables

All variables that can be controlled by the user start with the prefix `flash`, variables for this role are nested.

Example; flash a node use; `-e flash_node=true`

Example; force flash a node that is online and can be contacted use; `-e flash_node=true -e flash_force=true`

| Variable               | Description                                                                                                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| flash_sdcard           | Flash through SDCard, default: `true`, set to false if there is no BMC SDCard                                                                                                                |
| flash_node             | Flash node(s), in inventory or only the nodes, provided with the `-l` flag, this will flash all nodes that are off,offline,unreachable, if this flag is not provided NO node will be flashed |
| flash_force            | Force flash a node, will flash a node even if it is reachable                                                                                                                                |
| flash_version_rockchip | Override version of Rockchip for the RK1 image, currently: `2.4.0`                                                                                                                           |
| flash_version_rk1      | Provide different Ubuntu version for the RK1, dependent on `flash_version_rockchip`, current: `24.04`                                                                                        |
| flash_version_cm4      | Provide different Ubuntu version for the CM4, current: `24.04.1`                                                                                                                             |

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
---
- name: Flash nodes
  hosts: "{{ ansible_limit|default('nodes,!tpi') }}"
  gather_facts: false
  remote_user: root
  roles:
    - flash
```
