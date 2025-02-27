#!/usr/bin/env bash
# shellcheck shell=bash

SCRIPT_DIR="$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)"
DEVCON_DIR="$(dirname "${SCRIPT_DIR}")"
CONFIG_DIR="${DEVCON_DIR}/config"

# Configure inputrc
ln -sf "${CONFIG_DIR}/inpurc" "${HOME}/.inputrc"

# .bashrc
if [[ ! -f "${DEVCON_DIR}/.bashrc" ]]; then
    cp "${HOME}/.bashrc" "${DEVCON_DIR}/.bashrc"
    
    BASH_HISTORY="export PROMPT_COMMAND='history -a' && export HISTFILE=${DEVCON_DIR}/.bash_history"
    echo "${SNIPPET}" >> "${DEVCON_DIR}/.bashrc"

    ln -sf "${DEVCON_DIR}/.bashrc" "${HOME}/.bashrc"
fi
