# Terraform Setup for Kubernetes Homelab (Proxmox)

# Configure Variables

1. Create file `terraform.tfvars`

```
proxmox_host_ip        = "192.168.1.5"
proxmox_password    = "password"
proxmox_node        = "yourNode"
cloud_init_password = "initPassword"
vm_name = ["k3s-master", "k3s-worker-1", "k3s-worker-2"]
vm_template = "ubuntu-template"
cpu_cores = 1
ram_size = 2048
disk_size = "25G"
ip_addresses = ["192.x.x.x", "192.x.x.x", "192.x.x.x"]
gateway = "192.x.x.x"
```

# Initialize, Plan and Apply



1. `terraform init`:
- Initializes terraform. As this is utilizing the provider `telmate/proxmox` it will begin downloading

2. `terraform plan`:
- This shows what actions terraform will apply before actually actioning.

3. `terraform apply`:
- This will require user interaction to run. If you want to auto confirm you can with the argument `-auto-approve`.


## Additional Terraform Commands
1. `terraform fmt`:
- Formats code for readability and consistency

2. `terraform verify`:
- Checks the syntax and consistency of configuration

3. `terraform destroy`:
- This will delete the infrastructure on proxmox.

4. `terraform output`:
- This will display the data outlines in the `outputs.tf` after VM creation.


