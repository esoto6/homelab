# Ansible for K3S

## Create `inventory.yml` file

Create this file inside the `ansible` folder

```sh
all:
  hosts:
    k3s_master:
      ansible_host: 192.xxx.x.x1
    k3s_worker_1:
      ansible_host: 192.xxx.x.x2
    k3s_worker_2:
      ansible_host: 192.xxx.x.x3
  children:
    k3s_cluster:
      hosts:
        k3s_master:
        k3s_worker_1:
        k3s_worker_2:
    k3s_workers:
      hosts:
        k3s_worker_1:
        k3s_worker_2:
```

## Ansible Variables

### vars.yml
Update ip range for metallb to an address range within your network

```sh
metallb_ip_range: "192.168.1.93-192.168.1.99"
```

### secrets.yml

> [!NOTE]
> You will need to create this file.
>

```sh
cert_email: "your-email-for-cloudflare"
cloudflare_token: "your token from cloudflare"
```

Check to ensure that Ansible is able to connect to all the hosts
```sh
ansible -i inventory.ini all -m ping
```




Run Ansible Script
```sh
ansible-playbook install_k3s.yml
ansible-playbook install_metallb.yml --ask-become-pass
ansible-playbook install_certmanager.yml
```

If script is successfull you can now using your machine run the below commands to check everything is working as expected.

```sh
kubectl get nodes
kubectl get pods -A
```
![Results get nodes and pods](/docs/get-nodes.png)

If you see you master node and two worker nodes it has been set up successfully. 


