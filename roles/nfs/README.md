# Ansible Role: NFS Server

This role configures an NFS server using dynamic exports based on zone-aware host configuration. It supports resolution via LAN IP, Tailscale IP, and static network definitions. Fully compliant with `ansible-lint`, `exportfs`, and safe for production clusters.

---

## ✅ Features

- Profile-aware dynamic NFS exports (e.g., `lab`, `production`)
- DNS and Tailscale-based IP resolution
- Static IP fallback from `network.zones`
- Correct `/etc/exports` rendering (one line per export)
- Validated and reloadable with `exportfs -ra`
- Secure and customizable export options
- Ready for K3s / Kubernetes / backup usage

---

## 📁 Directory Layout

roles/nfs/
├── tasks/
│   ├── main.yml
│   ├── install.yml
│   ├── client.yml
│   ├── configure.yml
│   ├── resolve_clients.yml
│   ├── resolve_single_client.yml
├── templates/
│   └── exports.j2
├── vars/
│   └── schema.yml
├── defaults/
│   └── main.yml

---

## 📦 Dependencies

- NFS packages (`nfs-kernel-server`, `nfs-common`)
- DNS resolution (`dig` via `dnsutils`)
- Tailscale setup (optional, but supported)

---

## 🔧 Example `host_vars/node3.yml`

```yaml
nfs:
  server:
    enabled: true
    exports:
      - path: "/mnt/data/backups"
        clients:
          - node1
          - node2
          - "192.168.20.0/24"
      - path: "/mnt/data/shared"
        clients:
          - node1
          - node2
          - node3
          - node4
```

## Required Group/Global Vars

```yaml
profile: lab

tailscale:
  tailnet: tail504865.ts.net

network:
  zones:
    can:
      profile: lab
      nodes:
        node1: "192.168.10.21"
        node2: "192.168.10.22"
        node3: "192.168.10.23"
        node4: "192.168.10.24"
```

## Optional /etc/fstab client-side mount

/etc/fstab

```shell
node3:/mnt/data/backups /mnt/backups nfs4 defaults,_netdev,vers=4,timeo=30,nosuid,noatime 0 0
```

## Recommended Server Export Options

```yaml
nfs:
  server:
    default_options: "rw,sync,no_subtree_check,no_root_squash"
```

## Test Commands

```shell
sudo exportfs -ra
sudo exportfs -v
mount | grep nfs
```

## Enable noatime on the server filesystem

```shell
/dev/sda1 /mnt/data ext4 defaults,noatime 0 2
```
