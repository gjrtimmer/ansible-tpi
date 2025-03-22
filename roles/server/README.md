# Server Role

This roles contains the basic configuration for a server.

## Variables

| Variable    | Description                                                |
| ----------- | ---------------------------------------------------------- |
| reboot      | Decide to reboot server on required handlers, default true |
| network_mtu | Default network MTU                                        |

## Tasks

The following tasks are defined and get be individually run with a tag. The tag is the same as the task defined here.

| Task    | Tag     | Description      |
| ------- | ------- | ---------------- |
| sysctl  | sysctl  | Configure sysctl |
| selinux | selinux | Disable SELinux  |
