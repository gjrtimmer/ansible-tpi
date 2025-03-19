FROM mcr.microsoft.com/devcontainers/base:ubuntu24.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates fonts-firacode sshpass inetutils-ping python3 python3-pip pipx git git-lfs whois && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates

USER vscode

RUN pipx install --include-deps ansible && \
    pipx install ansible-lint && \
    pipx install --include-deps ensurepath && \
    pipx install jmespath && \
    pipx inject ansible jmespath && \
    pipx inject ansible-lint jmespath && \
    pipx install argcomplete && \
    pipx inject ansible argcomplete && \
    pipx inject ansible-lint argcomplete

USER root
ENV PATH=/home/vscode/.local/bin:/work/.bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /work
