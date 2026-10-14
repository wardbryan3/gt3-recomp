#!/usr/bin/env bash
# Optional local bootstrap when just is not installed. No system/global installation.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if command -v just >/dev/null 2>&1; then exec just --justfile "$root/justfile" "$@"; fi
bin="$root/build/tooling/bin/just"
if [[ ! -x "$bin" ]]; then
 mkdir -p "$(dirname "$bin")"
 archive="$root/build/tooling/just-1.40.0.tar.gz"
 curl -fL --max-time 120 https://github.com/casey/just/releases/download/1.40.0/just-1.40.0-x86_64-unknown-linux-musl.tar.gz -o "$archive"
 printf '%s  %s\n' 181b91d0ceebe8a57723fb648ed2ce1a44d849438ce2e658339df4f8db5f1263 "$archive" | sha256sum -c -
 tar -xzf "$archive" -C "$(dirname "$bin")" just
fi
exec "$bin" --justfile "$root/justfile" "$@"
