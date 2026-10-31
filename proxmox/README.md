# Proxmox LXCs

[Ansible](ansible/README.md) installs/configures Alloy and configures Prometheus
on existing Debian/Ubuntu containers. Follow that guide for setup, deployment,
and tests.

## Prepare SSH access

Edit `PUBLIC_KEY` in [enable-lxc-ssh-key.sh](scripts/enable-lxc-ssh-key.sh),
then copy the script to a Proxmox node and run it as root:

```sh
bash enable-lxc-ssh-key.sh
```

It adds the key to running containers and enables SSH, installing
`openssh-server` when needed. Confirm root key login and name resolution for
the hosts in `ansible/inventory/hosts.yml` before deploying.
