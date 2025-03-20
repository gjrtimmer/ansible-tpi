# Commands

This contain all the configured commands and their use.

| Action                            | Command                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| Flash Node (Full)                 | ansible-playbook playbooks/flash.yml -e flash_node=true          |
| Flash Node                        | ansible-playbook playbooks/flash.yml -e flash_node=true -t flash |
| Bootstrap Node (Full)             | ansible-playbook playbooks/bootstrap.yml                         |
| Bootstrap Node                    | ansible-playbook playbooks/bootstrap.yml -t bootstrap            |
| Bootstrap Node (RK1 NVMe Install) | ansible-playbook playbooks/bootstrap.yml -t bootstrap,rk1        |
| Bootstrap Node (DHCP Reservation) | ansible-playbook playbooks/bootstrap.yml -e dhcp_reservation     |
| Generate SSH Keys                 | ansible-playbook playbooks/ssh.yml                               |
| Regenerate SSH Keys               | ansible-playbook playbooks/ssh.yml -e ssh_overwrite=true         |
| Update known_hosts                | ansible-playbook playbooks/ssh.yml -t known_hosts                |
| Update known_hosts (TPI)          | ansible-playbook playbooks/ssh.yml -t known_hosts -l tpi         |
| Update known_hosts (Nodes)        | ansible-playbook playbooks/ssh.yml -t known_hosts -l nodes       |
| Update SSH Config                 | ansible-playbook playbooks/ssh.yml -t config                     |
| Update SSH Config (TPI)           | ansible-playbook playbooks/ssh.yml -t config -l tpi              |
| Update SSH Config (Nodes)         | ansible-playbook playbooks/ssh.yml -t config -l nodes            |
| Shutdown Nodes                    | ansible-playbook playbooks/shutdown.yml                          |
| Install TPI Client                | ansible-playbook playbooks/tpi.yml                               |
