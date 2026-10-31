# Homelab

Automation for Proxmox LXC observability and Talos Kubernetes services.

| Environment | What it does | Setup, run, and tests |
| --- | --- | --- |
| Proxmox | Installs/configures Alloy and configures Prometheus on existing LXCs | [Ansible guide](proxmox/ansible/README.md) |
| Talos | Bootstraps cluster services, then deploys applications through Argo CD | [Cluster guide](talos/ansible/README.md) · [Application guide](talos/README.md) |

Start with the guide for your environment. Proxmox tests run locally without
connecting to guests; Talos validation renders manifests and checks playbook syntax.

Operating notes: **Hermes vault → Development → Homelab**.
Planned work: [TODO.md](TODO.md).
