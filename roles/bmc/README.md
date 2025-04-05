# TPI CLI

This role provides common tasks used by other roles or playbooks.

> **IMPORTANT!**
>
> There is NO main.yml, this is deliberate, this is because the tasks in this role are meant to be imported.

- [Tasks](#tasks)

## Tasks

The following tasks are available for use:

- [Tasks](#tasks)
  - [Power On](#power-on)
  - [Power Off](#power-off)
  - [Mount NVMe Drive](#mount-nvme-drive)
  - [Umount NVMe Drive](#umount-nvme-drive)

### Power On

```yaml
- name: Power On Node
  ansible.builtin.import_role:
    name: bmc
    tasks_from: power-on.yml
```

### Power Off

```yaml
- name: Power Off Node
  ansible.builtin.import_role:
    name: bmc
    tasks_from: power-off.yml
```

### Mount NVMe Drive

```yaml
- name: Mount NVMe
  ansible.builtin.import_role:
    name: bmc
    tasks_from: msd-mount.yml
```

### Umount NVMe Drive

```yaml
- name: Unmount NVMe
  ansible.builtin.import_role:
    name: bmc
    tasks_from: msd-umount.yml
```
