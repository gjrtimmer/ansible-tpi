#!/usr/bin/env bash
# shellcheck shell=bash disable=SC2034

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"
PROJECT_DIR="$(git rev-parse --show-toplevel)"

printf "\n%s" "Configuring DevContainer..."

# shellcheck disable=SC2154
git -C "${PROJECT_DIR}" config --global --add safe.directory /work
git -C "${PROJECT_DIR}" config core.autocrlf false
git -C "${PROJECT_DIR}" config core.eol lf

# Configure Ansible Vault Pass
sudo chmod -x ${HOME}/.ansible_vault_pass

# Configure ownership mounts
sudo chmod 0600 ${HOME}/.ssh/config
sudo chmod 0600 ${HOME}/.ssh/known_hosts
sudo chmod 0755 ${HOME}/.ssh/tpi
sudo chmod 0600 ${HOME}/.ssh/tpi/*.key
sudo chmod 0755 ${HOME}/.ssh/tpi/*.key.pub
sudo chown -R vscode:vscode ${HOME}/.ssh/tpi

if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"
fi

# Migrate Data to ~/.tpi data directory
if [[ -d /work/group_vars ]] && [[ ! -L /work/group_vars ]]; then
    mv /work/group_vars "${HOME}/.tpi"
    ln -s "${HOME}/.tpi/group_vars" "${PROJECT_DIR}/group_vars"
else
    if [[ ! -d "${HOME}/.tpi/group_vars" ]]; then
        cp -r "${PROJECT_DIR}/.config/group_vars" "${HOME}/.tpi"
        ln -s "${HOME}/.tpi/group_vars" "${PROJECT_DIR}/group_vars"
    fi
fi

if [[ -d /work/host_vars ]] && [[ ! -L /work/host_vars ]]; then
    mv /work/host_vars "${HOME}/.tpi"
    ln -s "${HOME}/.tpi/host_vars" "${PROJECT_DIR}/host_vars"
else
    if [[ ! -d "${HOME}/.tpi/host_vars" ]]; then
        cp -r "${PROJECT_DIR}/.config/host_vars" "${HOME}/.tpi"
        ln -s "${HOME}/.tpi/host_vars" "${PROJECT_DIR}/host_vars"
    fi
fi

if [[ -f /work/hosts.yml ]] && [[ ! -L /work/hosts.yml ]]; then
    mv /work/hosts.yml "${HOME}/.tpi"
    ln -s "${HOME}/.tpi/hosts.yml" "${PROJECT_DIR}/hosts.yml"
else
    if [[ ! -f "${HOME}/.tpi/hosts.yml" ]]; then
        cp "${PROJECT_DIR}/.config/inventory/hosts.tmpl.yml" "${HOME}/.tpi/hosts.yml"
        ln -s "${HOME}/.tpi/hosts.yml" "${PROJECT_DIR}/hosts.yml"
    fi
fi

if [ ! -f "${PROJECT_DIR}/group_vars/nodes.yml" ]; then
    cp "${PROJECT_DIR}/.config/group_vars/nodes.yml" "${PROJECT_DIR}/group_vars/nodes.yml"
fi

# Migrate .bashrc
if [[ -f "/work/.devcontainer/.bashrc" ]]; then
    sed -i "s|/work/.config/hosts.playground.yml|/work/.config/inventory/hosts.playground.yml|g" /work/.devcontainer/.bashrc
fi

# Create Temp Directory
if [[ ! -d /tmp/tpi ]]; then
    mkdir -p /tmp/tpi
fi

# Finalizing DevContainer
printf "%s\n" "[DONE]"

# Install collections
printf "\n%s\n" "Running Ansible Galaxy"
ANSIBLE_COLLECTIONS_PATH=/work/.ansible/collections ansible-galaxy collection install -U -p .ansible/collections -r requirements.yml
ANSIBLE_ROLES_PATH=/work/.ansible/roles ansible-galaxy role install -p .ansible/roles -r requirements.yml

# Install TPI Client
CWD=$(pwd)
cd /work
printf "\n%s" "Install TPI Client..."
ansible-playbook -l localhost playbooks/tpi.yml > /tmp/tpi/client-install.log
printf "%s\n" "[DONE]"
cd "${CWD}" || exit 1

printf "\n%s\n\n" "Container Start Completed"
