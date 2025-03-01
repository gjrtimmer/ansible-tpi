#!/usr/bin/env bash
# shellcheck shell=bash disable=SC2034

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"
PROJECT_DIR="$(git rev-parse --show-toplevel)"

echo "Configuring Git"
# shellcheck disable=SC2154
git config --global --add safe.directory /work

# Configure filemode
#git config core.filemode false

if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    echo "Linking .bashrc"
    ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"
fi

if [ ! -f "${PROJECT_DIR}/hosts.yml" ]; then
    echo "Installing Ansible Inventory Template"
    cp "${PROJECT_DIR}/.config/hosts.tmpl.yml" "${PROJECT_DIR}/hosts.yml"
fi

# Install collections
ansible-galaxy collection install --force --collections-path .ansible/collections -r requirements.yml
ansible-galaxy role install --force --roles-path .ansible/roles -r requirements.yml

echo "Container Start Completed"
