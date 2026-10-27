# Configure Grafana Alloy and Prometheus with Ansible

This playbook installs and configures Grafana Alloy on existing Debian or Ubuntu Proxmox LXCs. It collects host metrics, systemd logs, and optional application or Docker logs, then forwards them to the configured Prometheus, Loki, and Tempo endpoints. It also manages the Prometheus scrape configuration on the `prometheus` LXC.

It does not create containers or change Proxmox, networking, or firewall settings.

## Requirements

Run the playbook from a machine that has:

- Python 3
- SSH access to each running LXC
- Host aliases in `~/.ssh/config` that match `inventory/hosts.yml`

Each target needs Python 3, systemd, and access to its Debian or Ubuntu package repositories. New Alloy installations also need access to `apt.grafana.com`.

## Configure

1. Add or remove hosts in `inventory/hosts.yml`.
2. Set the Prometheus, Loki, Tempo, and environment values in `inventory/group_vars/alloy_lxc.yml`.
3. Add host-specific settings under `inventory/host_vars/` when needed.
4. Confirm that SSH works for every target before running Ansible.

The inventory uses the `root` user by default. To use a sudo account, set `ansible_user` and run the playbook with `--ask-become-pass`.

## Run

From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Check the inventory and connectivity:

```sh
ansible-inventory --graph
ansible proxmox_lxcs -m ping
ansible-playbook site.yml --syntax-check
```

Preview and apply the configuration to one host first:

```sh
ansible-playbook site.yml --limit n8n --check --diff
ansible-playbook site.yml --limit n8n --diff
```

After verifying that host, apply the configuration to all reachable LXCs:

```sh
ansible-playbook site.yml --diff
```

The playbook updates one host at a time. Use `--limit` to exclude stopped or unavailable containers.

## What the playbook changes

- Installs Alloy from Grafana's APT repository when it is missing.
- Renders and validates `/etc/alloy/config.alloy` before replacing it.
- Saves a timestamped backup of the previous configuration.
- Restarts Alloy only when the configuration changes.
- Grants the configured supplementary groups to the Alloy service user.
- Renders and validates `/etc/prometheus/prometheus.yml` on the `prometheus_lxc` host.
- Saves a backup and restarts Prometheus only when its configuration changes.

Existing Alloy packages are not automatically upgraded. Check mode can preview changes on configured hosts, but a new installation requires a real run before its configuration can be validated.

Each Alloy instance scrapes its own metrics endpoint on `127.0.0.1:12345` and sends those metrics to Prometheus through remote write. Prometheus therefore does not need direct network access to port `12345` on the LXCs.

The Prometheus, Traefik, Proxmox, and PVE exporter endpoints are configured with DNS/inventory names in `inventory/group_vars/prometheus_lxc.yml`. Those names must resolve from the Prometheus LXC.

If an endpoint has no resolvable name, put its private address in an ignored `secrets.yml` file and pass it at runtime instead of committing it:

```yaml
prometheus_proxmox_target: <private-address>:8006
```

```sh
ansible-playbook site.yml --extra-vars @secrets.yml
```

The Prometheus role finds `promtool` through the remote host's `PATH`. If it is installed elsewhere, set `prometheus_promtool_binary` to its absolute path in `inventory/group_vars/prometheus_lxc.yml`.

Preview and apply only the Prometheus configuration with:

```sh
ansible-playbook site.yml --limit prometheus_lxc --tags prometheus --check --diff
ansible-playbook site.yml --limit prometheus_lxc --tags prometheus --diff
```

## Add host-specific collection

Create `inventory/host_vars/<host>.yml` and enable only the sources that exist on that LXC. For example:

```yaml
alloy_docker_logs: true
alloy_journal_services:
  mealie.service: mealie
alloy_app_scrapes:
  - name: mealie
    address: 127.0.0.1:REPLACE_WITH_METRICS_PORT
    instance: mealie:REPLACE_WITH_METRICS_PORT
    service_name: mealie
    metrics_path: /metrics
```

File logs use `alloy_file_logs` entries with `name`, `path`, and `service_name`. Avoid collecting the same logs from more than one source.

## Verify

On a target LXC:

```sh
systemctl status alloy --no-pager
journalctl -u alloy -n 50 --no-pager -l
```

Confirm delivery from the monitoring stack as well:

```promql
up{deployment_environment="prod"}
```

```logql
{host="n8n", service_name="n8n"}
```

## Restore a backup

If a deployed configuration fails, use the backup path printed by Ansible on the affected LXC:

```sh
cp /etc/alloy/config.alloy.TIMESTAMP_BACKUP /etc/alloy/config.alloy
alloy validate /etc/alloy/config.alloy && systemctl restart alloy
```

Update the inventory or template before the next playbook run, or Ansible will reapply the managed configuration.
