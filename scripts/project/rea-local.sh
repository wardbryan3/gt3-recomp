#!/usr/bin/env bash
# REA is private, repository-local software; never install it globally or publish it.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
tools="$root/local/rea"
export PATH="$tools/jdk/bin:/usr/local/bin:$PATH"
export HOME="$tools/rea-home"
export XDG_CONFIG_HOME="$HOME/config" XDG_CACHE_HOME="$HOME/cache" XDG_DATA_HOME="$HOME/data"
export TMPDIR="$tools/tmp" TMP="$tools/tmp" TEMP="$tools/tmp"
export GHIDRA_INSTALL_DIR="$tools/ghidra/ghidra_12.1.4_PUBLIC" JAVA_HOME="$tools/jdk"
export REA_ANALYSIS_PROVIDER=ghidra REA_GHIDRA_LANGUAGE_ID=r5900:LE:32:default REA_GHIDRA_COMPILER_SPEC_ID=default
export REA_GHIDRA_STARTUP_TIMEOUT_MS=600000
mkdir -p "$HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME" "$TMPDIR"
chmod 700 "$HOME" "$TMPDIR"
exec /usr/local/bin/node "$tools/rea/node_modules/rea-agents/scripts/rea.mjs" "$@"
