#!/usr/bin/env bash
# shellcheck shell=bash

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"

# Configure inputrc
ln -sf "${CONFIG_DIR}/inputrc" "${HOME}/.inputrc"

# .bashrc
if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    cp "${HOME}/.bashrc" "${DEVCON_DIR}/.bashrc"
    
    echo "export PROMPT_COMMAND='history -a'" >> "${DEVCON_DIR}/.bashrc"
    echo "export HISTFILE=${DEVCON_DIR}/.bash_history" >> "${DEVCON_DIR}/.bashrc"
    
    echo "alias ansible-playground='ansible -i /work/.config/hosts.playground.yml'" >> "${DEVCON_DIR}/.bashrc"
    echo "alias ansible-playground-playbook='ansible-playbook -i /work/.config/hosts.playground.yml'" >> "${DEVCON_DIR}/.bashrc"
    echo "alias ansible-pg='ansible -i /work/.config/hosts.playground.yml'" >> "${DEVCON_DIR}/.bashrc"
    echo "alias ansible-pp='ansible-playbook -i /work/.config/hosts.playground.yml'" >> "${DEVCON_DIR}/.bashrc"
fi
ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"

echo "Container Create Completed"
