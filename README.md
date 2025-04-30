# Homelab-Kubernetes

## Introduction

I started this project to learn new tools and technologies while upgrading my homelab from a simple Raspberry Pi setup to a more scalable Kubernetes-based infrastructure. My goal is to explore GitOps, Terraform, Ansible, ArgoCD, monitoring, and security best practices, making the entire setup automated and repeatable.

This homelab will serve as a testing ground for K3s running on Proxmox, with infrastructure managed using Terraform and configuration handled by Ansible. Everything will be deployed using ArgoCD to enable GitOps workflows, while Prometheus and Grafana will provide monitoring and alerting.

## Infrastructure

The homelab runs on a dedicated machine with Proxmox as the hypervisor. The hardware has 4 cores, 16GM RAM, and SSD storage which is sufficient K3s. This setup is designed to get me introduced to new tools and technologies and expand to dedicated hardware in the future utilizing old hardware running Kubernetes.

## Pre-Requisites
- [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-terraform)
- Install Ansible via pip
```sh
sudo apt install python3-pip
pip install --user ansible
export PATH=$PATH:~/.local/bin
```

# Sections
- 1. [Proxmox / Terraform](https://github.com/esoto6/terraform-proxmox)
- 2. [Ansible](https://github.com/techno-tim/k3s-ansible)
