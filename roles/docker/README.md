# Docker Runtime

This role will install the docker runtime. Nvidia devices are supported for Jetson.

> Nvidia Runtime
>
> Manual install for Nvidia devices regarding the manual installation of the Nvidia repository for the Nvidia Docker runtime is not yet implemented.

This role is conditionally included in the bootstrap playbook, and activated by providing the global variable `container_runtime=docker`.

## Docker Config

If a `config.json` file is present in the `config/docker` directory it will be installed into `/etc/docker/config.json`.
Furthermore, this role will try to configure docker config files for the users `root` and `ubuntu`.
It will search for the file `config.{{ username }}.json` in the `docker/files` directory to install them.

## qemu

This role will auto install and configure buildkit to have support for building cross-platform images with `qemu`.

## buildkitd.toml

If you require additional configuration for `buildkit`, for example you have a repository which has a self-signed certificate,
this certificate must be added to the buildkit to ensure it is accepted when `docker` tries to pull or push images from it.

This can be configure with the following configuration, the certificate will be tried to be found in `config/docker/{{ REGISTRY }}/{{ FILE }}`.
If found it will upload it to to node. If not found, it will check that the certificate is already present on the node in `/etc/docker/certs.d/{{ REGISTRY }}/{{ FILE }}`.
Please note that this is dynamic configuration. The `{{ REGISTRY }}` is the key `name` of the list under `registries`.

```yaml
docker:
  buildkitd:
    debug: false
    registries:
      - name: harbor.local
        ca: 'ca.crt'
```

This configuration will generate the following `/etc/buildkitd.toml`

```toml
# /etc/buildkitd.toml
debug = false
[registry."harbor.local"]
  ca=["/etc/docker/certs.d/harbor.local/ca.crt"]
```
