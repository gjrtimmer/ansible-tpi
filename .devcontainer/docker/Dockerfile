FROM mcr.microsoft.com/devcontainers/base:ubuntu24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates fonts-firacode sshpass inetutils-ping python3 pipx git git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates

RUN pipx install --include-deps ansible && \
    pipx install ansible-lint && \
    pipx install --include-deps ensurepath

WORKDIR /work
