#!/usr/bin/env bash
# shellcheck shell=bash

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"

echo "Configuring Git"
# shellcheck disable=SC2154
git config --global --add safe.directory /work

# Configure filemode
git config core.filemode false

if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    echo "Linking .bashrc"
    ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"
fi

# Install collections
ansible-galaxy collection install --force -r requirements.yml
