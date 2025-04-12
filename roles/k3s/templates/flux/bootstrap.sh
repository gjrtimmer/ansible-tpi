#!/usr/bin/env bash
# shellcheck shell=bash

set -x

TYPE="{{ k3s.profiles[profile].flux.bootstrap.type }}"
OWNER="{{ k3s.profiles[profile].flux.bootstrap.owner }}"
REPO="{{ k3s.profiles[profile].flux.bootstrap.repository }}"
BRANCH="{{ k3s.profiles[profile].flux.bootstrap.branch | default('main') }}"
PROFILE="{{ profile }}"
PERSONAL="{{ k3s.profiles[profile].flux.bootstrap.personal | lower | default('true') }}"

case "${TYPE,,}" in
    gitlab)
        echo "Bootstrapping Flux on GitLab"
        echo "${TOKEN}" | flux bootstrap gitlab \
            --deploy-token-auth \
            --owner="${OWNER}" \
            --repository="${REPO}" \
            --branch="${BRANCH}" \
            --path="clusters/${PROFILE}" \
            --personal="${PERSONAL}"
        ;;
    github)
        echo "Bootstrapping Flux on GitHub"
        export GITHUB_TOKEN="${TOKEN}"
        echo "${TOKEN}" | flux bootstrap github \
            --token-auth \
            --owner="${OWNER}" \
            --repository="${REPO}" \
            --branch="${BRANCH}" \
            --path="clusters/${PROFILE}" \
            --personal="${PERSONAL}"
        ;;
    *)
        echo "Unsupported bootstrap type: ${TYPE}"
        exit 1
        ;;
esac
