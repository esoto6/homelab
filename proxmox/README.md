# Proxmox LXCs

This directory contains automation for services that run inside Proxmox-managed Linux containers. It is independent of Talos cluster bootstrap and Kubernetes application deployment.

## Current scope

- [`ansible/`](ansible/README.md): installs and configures Grafana Alloy on existing Debian/Ubuntu LXCs over SSH.
- [`scripts/enable-lxc-ssh-key.sh`](scripts/enable-lxc-ssh-key.sh): manually prepares running LXCs for root SSH key access from a Proxmox node.

## Prepare LXC SSH access

Before using Ansible, edit `PUBLIC_KEY` in the script with your public key, then run it as root on a Proxmox node:

```bash
bash proxmox/scripts/enable-lxc-ssh-key.sh
```

The script validates the key, skips stopped containers, adds it to root's `authorized_keys` without duplicates, and enables/starts SSH. If `sshd` is missing, it installs `openssh-server` using `apt-get`, so that LXC must be Debian/Ubuntu-based with working package repositories. It does not change firewall rules or override SSH server policy that may prohibit root key login. Confirm access to each LXC before running Ansible.

For easier connections, add host aliases and your key to the SSH config on your client machine at `~/.ssh/config`. For example:

```sshconfig
Host *.lan
	User root
	IdentityFile ~/.ssh/YOUR_PRIVATE_KEY
	IdentitiesOnly yes
```

Then connect with `ssh gotify.lan`. SSH config selects the user and key; it does not create DNS records. Ensure each `.lan` name resolves to the correct LXC IP, or define a host-specific alias with `HostName` set to that IP.

This Ansible project does not create, destroy, or configure Proxmox VMs/LXCs, networks, storage, or host settings. Add Proxmox API or guest lifecycle automation here if that becomes part of the homelab workflow. Put service-specific LXC provisioning alongside the existing host automation, not in `talos/`.
