#!/usr/bin/env bash
set -euo pipefail
lanroot="$(cd "$(dirname "$0")" && pwd)"
source "$lanroot/../presentation/session-env.sh"
exec "$lanroot/../lan-play-venv/bin/python" "$lanroot/server.py"
