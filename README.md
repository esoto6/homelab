# Homelab-Kubernetes

## Introduction

I started this project to learn new tools and technologies while upgrading my homelab from a simple Raspberry Pi setup to a more scalable Kubernetes-based infrastructure. My goal is to explore GitOps, Terraform, Ansible, ArgoCD, monitoring, and security best practices, making the entire setup automated and repeatable.Everything will be deployed using ArgoCD to enable GitOps workflows, while Prometheus and Grafana will provide monitoring and alerting.


## Infrastructure

The homelab initially started with running a K3s cluster running in Proxmox on an intel nuc n100 processor utilizing Terraform, Ansible and Gitops with ArgoCD. Since the inception I have transitioned to utilizing Talos linux on independent machines with varying specs. This setup is designed to get me introduced to new tools and technologies .

### Pre-Requisites

- Ansible
- Helm
- Kustomize
- kubectl
- talosctl


## Setup Cluster

1. Setup Talos Cluster
2. [Ansible Pre Sync](/ansible/README.md)
3. Once ArgoCD is installed bootstrap cluster

```sh
kubectl apply -f kubernetes/bootstrap/apps-set-kustomize.yaml
```

>[!NOTE]
>Items to do/complete
>[Todo List](TODO.md)

