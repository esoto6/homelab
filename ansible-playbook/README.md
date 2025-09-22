
# Create file vars/secrets.yaml

```sh
cloudflare_api_token: "<token>"
bitwarden_access_token: "<token>"
email: "<email>"
domain: "<example.com>"
metallb_addresses: "192.168.1.xxx-192.168.1.xxx"
```

Run playbook
```sh
ansible-playbook cluster-setup.yaml
```

Reset Cluster
```sh
ansible-playbook cluster-reset.yaml