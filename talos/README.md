# Talos Kubernetes Cluster

This directory contains configuration for the Talos cluster and workloads deployed into Kubernetes. It does not manage Proxmox LXC guests or services hosted directly in those guests.

## Contents

- [`ansible/`](ansible/README.md): bootstraps cluster-scoped components such as MetalLB, cert-manager, External Secrets, Traefik, and Argo CD.
- [`kubernetes/`](kubernetes/): Kubernetes application manifests, overlays, and the Argo CD ApplicationSet bootstrap.

The repository root README provides the cluster bootstrap sequence. ApplicationSet source paths are repository-relative and therefore include the `talos/` prefix.
