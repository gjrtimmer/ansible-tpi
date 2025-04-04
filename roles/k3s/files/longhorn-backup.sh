#!/usr/bin/env bash
# shellcheck shell=bash
set -e

volumes=$(kubectl -n longhorn-system get volumes -o name)

for vol in $volumes; do
  kubectl -n longhorn-system patch "$vol" --type merge -p '{"spec":{"fromBackup":"","numberOfReplicas":3}}'
done