#!/usr/bin/env bash
# Explicitly approved LAN-only exceptions. Never flush/reload existing rules.
set -euo pipefail
case "${1:-}" in
 open)
  sudo -n ufw allow from 10.6.65.0/24 to any port 8765 proto tcp comment 'GT3 LAN temporary HTTP'
  sudo -n ufw allow from 10.6.65.0/24 to any port 8766 proto udp comment 'GT3 LAN temporary WebRTC'
  ;;
 close)
  sudo -n ufw --force delete allow from 10.6.65.0/24 to any port 8765 proto tcp
  sudo -n ufw --force delete allow from 10.6.65.0/24 to any port 8766 proto udp
  ;;
 *) echo 'Usage: firewall.sh open|close' >&2; exit 1 ;;
esac
