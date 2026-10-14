#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
for role in audio-policy audio compositor; do
 file="$root/$role.pid"; [[ -f "$file" ]] || continue
 pid="$(< "$file")"; [[ "$pid" =~ ^[0-9]+$ ]] || exit 1
 if kill -0 "$pid" 2>/dev/null; then
  cmd="$(tr '\0' ' ' < /proc/$pid/cmdline)"
  pgid="$(ps -o pgid= -p "$pid" | tr -d ' ')"
  [[ "$pgid" == "$pid" ]] || { echo "Refusing non-owned group $pid" >&2; exit 1; }
  case "$role" in
   compositor) [[ "$cmd" == *"--config-file $root/config/dbus.conf"* ]] || exit 1 ;;
   audio) [[ "$cmd" == *"-c $root/config/audio.conf"* ]] || exit 1 ;;
   audio-policy) [[ "$cmd" == 'wireplumber --profile policy '* ]] || exit 1 ;;
  esac
  kill -TERM -- "-$pid"
 fi
 rm "$file"
done
