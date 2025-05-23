# Server Role

This roles contains the basic configuration for a server.

## Variables

| Variable    | Description                                                |
| ----------- | ---------------------------------------------------------- |
| reboot      | Decide to reboot server on required handlers, default true |
| network_mtu | Default network MTU                                        |

## Tasks

The following tasks are defined and get be individually run with a tag. The tag is the same as the task defined here.

| Task     | Tag           | Description                                             |
| -------- | ------------- | ------------------------------------------------------- |
| sysctl   | sysctl        | Configure sysctl                                        |
| selinux  | selinux       | Disable SELinux                                         |
| htop     | htop          | Configure `htop` for default Ubuntu user                |
| time     | timezone      | Timezone configuration                                  |
| time     | ntp           | NTP Configuration                                       |
| time     | timezone, ntp | Run both timezone and NTP Configuration                 |
| network  | network       | Network MTU Configuration                               |
| env_vars | env_vars      | Environment Variable Configuration for /etc/environment |
