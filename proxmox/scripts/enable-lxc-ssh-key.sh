#!/usr/bin/env bash

PUBLIC_KEY='<your-public-key-here>'

if ! command -v pct >/dev/null 2>&1; then
  echo "Run this script on a Proxmox node where pct is available." >&2
  exit 1
fi

if ! printf '%s\n' "$PUBLIC_KEY" | ssh-keygen -lf - >/dev/null 2>&1; then
  echo "Invalid public key. Check the PUBLIC_KEY value." >&2
  exit 1
fi

while read -r CTID; do
  if ! pct status "$CTID" | grep -q 'status: running'; then
    echo "LXC $CTID: skipped (stopped)"
    continue
  fi

  if printf '%s\n' "$PUBLIC_KEY" | pct exec "$CTID" -- sh -c '
    set -eu
    key=$(cat)

    if ! command -v sshd >/dev/null 2>&1; then
      if ! command -v apt-get >/dev/null 2>&1; then
        echo "OpenSSH is missing and apt-get is unavailable." >&2
        exit 1
      fi
      export DEBIAN_FRONTEND=noninteractive
      apt-get update
      apt-get install -y openssh-server
    fi

    mkdir -p /root/.ssh
    touch /root/.ssh/authorized_keys
    chown root:root /root/.ssh /root/.ssh/authorized_keys
    chmod 700 /root/.ssh
    chmod 600 /root/.ssh/authorized_keys

    if grep -qxF "$key" /root/.ssh/authorized_keys; then
      echo "Key already present"
    else
      printf "\n%s\n" "$key" >> /root/.ssh/authorized_keys
      echo "Key added"
    fi

    if command -v systemctl >/dev/null 2>&1; then
      systemctl enable --now ssh 2>/dev/null ||
        systemctl enable --now sshd 2>/dev/null || {
          echo "Could not enable or start the SSH service." >&2
          exit 1
        }
    elif command -v service >/dev/null 2>&1; then
      service ssh start || service sshd start
    else
      echo "No supported service manager found for SSH." >&2
      exit 1
    fi
  '; then
    echo "LXC $CTID: OK"
  else
    echo "LXC $CTID: FAILED"
  fi
done < <(pct list | awk 'NR > 1 {print $1}')