# SSH

To generate the required ssh keys run the following command.
This command will also intall the generate SSH key for the linked BMC into the BMC.

```shell
ansible-playbook playbooks/ssh.yml
```

If new keys are required, you can re-run the same playbook with the following option to regenerate
all the keys and install the new ones.

```shell
ansible-playbook playbooks/ssh.yml -e ssh_overwrite=true
```
