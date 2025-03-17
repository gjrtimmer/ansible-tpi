# TPI CLI

This role provides common tasks used by other roles or playbooks.

> **IMPORTANT!**
>
> There is NO main.yml, this is deliberate, this is because the tasks in this role are meant to be imported.

- [Tasks](#tasks)

## Tasks

The following tasks are available for use:

- [Tasks](#tasks)
  - [Install Client](#install-client)
  - [Power On](#power-on)
  - [Power Off](#power-off)

### Install Client

Check and install the TPI Client to the targeted hosts.

```yaml
- name: TPI Client
  ansible.builtin.import_role:
    name: tpi
    tasks_from: client-install.yml
```

### Power On

```yaml
- name: Power Off Node
  ansible.builtin.import_role:
    name: tpi
    tasks_from: power-on.yml
```

### Power Off

```yaml
- name: Power Off Node
  ansible.builtin.import_role:
    name: tpi
    tasks_from: power-off.yml
```
