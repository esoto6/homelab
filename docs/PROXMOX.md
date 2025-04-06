# Proxmox General Settings

## Create cloud-init template

Instructions on creating a template can be found in the documentation located [here](https://registry.terraform.io/providers/Telmate/proxmox/latest/docs/guides/cloud-init%2520getting%2520started#creating-a-cloud-init-template).


# SSH key for Proxmox


On your local machine create the private / public key for SSH
```sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_proxmox -N ""
```



# Create a script snippet to be used for the cloud-init


>[!IMPORTANT]
>
> Creating a snippet is very important in this step as the template will not work with out having `qemu-guest-agent`
>

## Create ubuntu.yml

```sh
cd /var/lib/vz/snippets
touch ubuntu.yml
```

## ubuntu.yml contents
Update content with either vim or nano with the below content.

```sh
#cloud-config
runcmd:
  - apt update
  - apt install -y qemu-guest-agent
  - systemctl start qemu-guest-agent
  - systemctl enable ssh
  - reboot
```
