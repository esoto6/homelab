# TODOS

## TALOS

- [ ] Create Documentation
- [ ] Docs on Metrics including ETCD
- [ ] Securing ETCD with network rules

## Ansible Script

- [ ] Single script with flags
- [ ] Configure to use `dev` or `prod` dns01 challenge

## Kubernetes Applications/ App Sets

- [ ] Dynamic Apps-set for `dev` or `prod`
- [ ] Update READMEs for all applications


# Apps I want to Install and Manage
- [ ] Metallb (Currently only setup via ansible)
- [X] [cert-manager](kubernetes/applications/cert-manager/README.md) (wildcard certs)
- [X] [Traefik](kubernetes/applications/traefik/README.md)
- [X] [ArgoCD](kubernetes/applications/argocd/README.md) Using pre defined secret
- [X] [external-secrets](kubernetes/applications/external-secrets/README.md) utilizing Bitwarden Secrets Manager
    - [ ] Utilizing ClusterSecretStore to push secrets
- [X] [Nginx](/kubernetes/applications/nginx/README.md)
- [X] [Trivy Operator](kubernetes/applications/trivy-operator/README.md)
    - [X] Need to initialize CRDs prior to strapping
    - [ ] Monitoring the results
- [X] [Prometheus Grafana Stack](kubernetes/applications/monitoring/base/README.md) w/ Dashboards
    - [ ] Update Ansible Script or include docs to enable metrics for talos
- [ ] Homepage
- [ ] n8n
- [ ] ollama
- [ ] CloudNativePG
- [ ] MongoDB
- [ ] UptimeKuma

# Topics to continue exploring
- [ ] Storage (PVC)
    - [ ] Synology Cloud CSI or another
- [ ] Vulnerabilities
- [ ] Best Practices
- [ ] Self Host App (tip-of-the-day)