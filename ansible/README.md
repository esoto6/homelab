
# Create file vars/secrets.yaml

```sh
cloudflare_api_token: "<token>"
bitwarden_access_token: "<token>"
bitwarden_organization_id: "<id>"
bitwarden_project_id: "<id>"
cert_manager_domain_email: "<email>"
cert_manager_domain_name: "<example.com>"
ip_addresses: "192.168.1.xxx-192.168.1.xxx"
```

Run playbook
```sh
ansible-playbook cluster-setup.yaml
```

Reset Cluster
```sh
ansible-playbook cluster-reset.yaml