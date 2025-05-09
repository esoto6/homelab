# Homelab-Kubernetes

## Introduction

I started this project to learn new tools and technologies while upgrading my homelab from a simple Raspberry Pi setup to a more scalable Kubernetes-based infrastructure. My goal is to explore GitOps, Terraform, Ansible, ArgoCD, monitoring, and security best practices, making the entire setup automated and repeatable.

This homelab will serve as a testing ground for K3s running on Proxmox, with infrastructure managed using Terraform and configuration handled by Ansible. Everything will be deployed using ArgoCD to enable GitOps workflows, while Prometheus and Grafana will provide monitoring and alerting.

### Infrastructure

The homelab runs on a dedicated machine with Proxmox as the hypervisor. The hardware has 4 cores, 16GM RAM, and SSD storage which is sufficient K3s. This setup is designed to get me introduced to new tools and technologies and expand to dedicated hardware in the future utilizing old hardware running Kubernetes.

### Pre-Requisites
- Helm
- Kustomize


## Bootstrap Cluster

### Steps

1. Add argocd via helm direct to cluster

```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install argocd argo/argo-cd --namespace argocd --create-namespace
```
2. Apply patch to enable-helm with kustomize
```
kubectl patch configmap argocd-cm -n argocd --type merge -p '{"data":{"kustomize.buildOptions":"--enable-helm"}}'
```

3. Port forward or implement LoadBalancer argocd

Rancher Desktop
```
k port-forward svc/argocd-server -n argocd 8080:443
```

K3s
```
k patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

4. Get argocd password
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

5. Create Secret for cert-manager

```
k create namespace cert-manager
k create secret generic cloudflare-api-token \
--from-literal=api-token=your-api-token-here \
-n cert-manager
```

6. Apply appset to cluster
```
k apply -f homelab/app-set.yaml
```

# [Issues](ISSUES.md)

