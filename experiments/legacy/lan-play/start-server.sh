#!/usr/bin/env bash
set -euo pipefail
lanroot="$(cd "$(dirname "$0")" && pwd)"
[[ ! -f "$lanroot/run/server.pid" ]] || { echo 'Existing PID file: inspect or run stop-server.sh first' >&2; exit 1; }
"$lanroot/firewall.sh" open
if [[ ! -S "$lanroot/../presentation/runtime/gt3-virtual" ]]; then "$lanroot/../presentation/start-session.sh"; fi
setsid "$lanroot/run-server.sh" > "$lanroot/logs/server.log" 2>&1 < /dev/null & echo $! > "$lanroot/run/server.pid"
for ((i=0;i<150;i++)); do
 if curl -fsS http://127.0.0.1:8765/ > /dev/null 2>&1; then
  printf 'http://10.6.65.10:8765/#%s\n' "$(< "$lanroot/run/access-token")"; exit 0
 fi
 kill -0 "$(< "$lanroot/run/server.pid")" 2>/dev/null || { echo 'Server exited; inspect logs/server.log' >&2; exit 1; }
 sleep .1
done
echo 'Startup timed out; inspect logs/server.log' >&2; exit 1
