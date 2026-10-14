#!/usr/bin/env bash
set -euo pipefail
lanroot="$(cd "$(dirname "$0")" && pwd)"
file="$lanroot/run/server.pid"
if [[ -f "$file" ]]; then
 pid="$(< "$file")"; [[ "$pid" =~ ^[0-9]+$ ]] || exit 1
 if kill -0 "$pid" 2>/dev/null; then
  cmd="$(tr '\0' ' ' < /proc/$pid/cmdline)"
  pgid="$(ps -o pgid= -p "$pid" | tr -d ' ')"
  [[ "$cmd" == *"$lanroot/server.py"* && "$pgid" == "$pid" ]] || { echo 'Refusing unrecognized process' >&2; exit 1; }
  kill -TERM "$pid"
  for ((i=0;i<100;i++)); do kill -0 "$pid" 2>/dev/null || break; sleep .1; done
  if kill -0 "$pid" 2>/dev/null; then echo 'Server still stopping; inspect before retrying' >&2; exit 1; fi
 fi
 rm "$file"
fi
"$lanroot/../presentation/stop-session.sh"
"$lanroot/firewall.sh" close
