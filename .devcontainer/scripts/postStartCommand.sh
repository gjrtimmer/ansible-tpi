#!/usr/bin/env bash
# shellcheck shell=bash disable=SC2034

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"
PROJECT_DIR="$(git rev-parse --show-toplevel)"

echo "Configuring Git"
# shellcheck disable=SC2154
git -C "${PROJECT_DIR}" config --global --add safe.directory /work
git -C "${PROJECT_DIR}" config core.autocrlf false
git -C "${PROJECT_DIR}" config core.eol lf

# Configure Ansible Vault Pass
sudo chmod -x ${HOME}/.ansible_vault_pass

# Configure ownership of SSH mount
sudo chmod 0600 "${HOME}/.ssh/config" "${HOME}/.ssh/known_hosts"

if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    echo "Linking .bashrc"
    ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"
fi

if [ ! -f "${PROJECT_DIR}/hosts.yml" ]; then
    echo "Installing Ansible Inventory Template"
    cp "${PROJECT_DIR}/.config/hosts.tmpl.yml" "${PROJECT_DIR}/hosts.yml"
fi

# Create Temp Directory
if [[ ! -d /tmp/tpi ]]; then
    mkdir -p /tmp/tpi
fi


# Install collections
ANSIBLE_COLLECTIONS_PATH=/work/.ansible/collections ansible-galaxy collection install -U -p .ansible/collections -r requirements.yml
ANSIBLE_ROLES_PATH=/work/.ansible/roles ansible-galaxy role install -p .ansible/roles -r requirements.yml

echo "Container Start Completed"
