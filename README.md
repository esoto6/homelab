# Homelab

Automation and configuration for two parts of my homelab:

- **Proxmox LXCs:** installs and configures Grafana Alloy on existing Linux containers.
- **Talos Kubernetes:** bootstraps cluster services and deploys applications through Argo CD.

The Proxmox and Talos workflows are independent. Use only the section you need.

## Requirements

- Ansible
- Helm
- Kustomize
- `kubectl`
- `talosctl`

## Run the Proxmox LXC automation

The containers must already exist and be reachable over SSH.

```sh
cd proxmox/ansible
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ansible-playbook site.yml --check --diff
ansible-playbook site.yml --diff
```

Configure the inventory and SSH access before running the playbook. See [proxmox/ansible/README.md](proxmox/ansible/README.md) for details.

## Run the Talos Kubernetes bootstrap

First provision the Talos machines and make sure the cluster is reachable. Then configure the kubeconfig path and secrets described in [talos/ansible/README.md](talos/ansible/README.md).

From the repository root, run:

```sh
ansible-playbook talos/ansible/cluster-setup.yaml
kubectl apply -f talos/kubernetes/bootstrap/apps-set-kustomize.yaml
```

The Ansible playbook installs MetalLB, cert-manager, External Secrets, Traefik, Argo CD, and required CRDs. The `kubectl` command hands application deployment over to Argo CD.

More details are available in [talos/README.md](talos/README.md). Planned work is tracked in [TODO.md](TODO.md).
