# LXC observability

Installs/configures Grafana Alloy and updates Prometheus scrape jobs on existing
LXCs over SSH. Alloy validates configuration before deployment and restarts
when it changes. Prometheus must already be installed.

## Setup

Requires Python 3.11+ and SSH access with privilege escalation on target hosts.
Run commands from this directory:

```sh
cd proxmox/ansible
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Edit `inventory/hosts.yml`, `inventory/group_vars/`, and `inventory/host_vars/`.
Keep private overrides in ignored `secrets.yml`.
Operating details: **Hermes vault → Development → Homelab**.

## Run

```sh
.venv/bin/ansible-playbook site.yml --limit hermes -e @secrets.yml --check --diff
.venv/bin/ansible-playbook site.yml --limit hermes -e @secrets.yml --diff
```

Replace `hermes` with the target host or group. Omit `-e @secrets.yml` if no
private overrides are needed. Applying replaces configs and may restart services.
On a host without Alloy, check mode skips installation and configuration validation;
run a real deployment to install it.

## Tests

```sh
.venv/bin/ansible-playbook site.yml --syntax-check
.venv/bin/python -m unittest discover -s tests -v
```

The regression tests render real inventory locally and check Hermes telemetry
routing, opt-in behavior, and existing Docker OTLP behavior. They require no SSH
or running services; they do not run the Alloy binary validator.
