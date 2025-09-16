# Homelab-Kubernetes

## Introduction

I started this project to learn new tools and technologies while upgrading my homelab from a simple Raspberry Pi setup to a more scalable Kubernetes-based infrastructure. My goal is to explore GitOps, Terraform, Ansible, ArgoCD, monitoring, and security best practices, making the entire setup automated and repeatable.

This homelab will serve as a testing ground for K3s running on Proxmox, with infrastructure managed using Terraform and configuration handled by Ansible. Everything will be deployed using ArgoCD to enable GitOps workflows, while Prometheus and Grafana will provide monitoring and alerting.

### Infrastructure

The homelab runs on a dedicated machine with Proxmox as the hypervisor. The hardware has 4 cores, 16GM RAM, and SSD storage which is sufficient for K3s. This setup is designed to get me introduced to new tools and technologies and expand to dedicated hardware in the future utilizing old hardware running Kubernetes.

### Pre-Requisites
- Helm
- Kustomize


## Bootstrap Cluster

### Steps

#### Terraform - Proxmox
Utilizing this repo [terraform-proxmox](https://github.com/esoto6/terraform-proxmox) to configure vms on proxmox

#### Ansible 
Initially started using my own ansible steps to initiate k3s. Discovered this repo [k3s-ansible](https://github.com/timothystewart6/k3s-ansible) which I am utilizing to initiate k3s. 

#### Intermediate step

I need to figure out how to automate this step. Prep requirements in order for argocd install to go smoothly. 

1. Need external secrets to pull secrets
2. Once eso is configured need to install cert-manager to create certificates use dns01 challenge
3. Once certificates are valid use traefik to create ingress routes for apps

[Intermediate steps](INTERMEDIATE_STEPS.md)

Once argocd is installed bootstrap cluster

```sh
kubectl apply -f bootstrap/apps-set-kustomize.yaml
```

# [Issues](ISSUES.md)

