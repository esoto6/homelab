
# Ansible

This ansible script is utilized to initial start my cluster or initiate core components that are needed for almost every app within my cluster.

Apps:
- Metallb (LoadBalancer)
- Cert-Manager (Manage Certificate w/ DNS01 Challenge)
- External-Secrets w/ Bitwarden Secrets Manager (Retrieve Secrets)
- Traefik (Ingress Controller)
- ArgoCD (GitOps)
- Pre Install Additional CRDs as needed
    - Trivy
    - Grafana

# Run Ansible Script

1. Create a file vars/app-secrets.yaml
2. Populate newly created file with the below structure

```sh
cloudflare_token: "<token>"
bitwarden_access_token: "<token>"
bitwarden_organization_id: "<id>"
bitwarden_project_id: "<id>"
cert_manager_domain_email: "<email>"
cert_manager_domain_name: "<example.com>"
ip_addresses: "192.168.1.xxx-192.168.1.xxx"
```


# Setup and Teardown of Ansible Managed Applications

## Setup Apps

1. Create Initial Apps
Run playbook
```sh
ansible-playbook ansible/cluster-setup.yaml
```

## Teardown Apps

1. Teardown Ansible created Apps
Reset Cluster
```sh
ansible-playbook ansible/cluster-reset.yaml