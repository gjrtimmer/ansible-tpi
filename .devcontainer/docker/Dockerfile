FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates fonts-firacode sshpass && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates && \
    pipx install --include-deps ansible && \
    pipx install ansible-lint && \
    pipx install --include-deps ensurepath

WORKDIR /work
