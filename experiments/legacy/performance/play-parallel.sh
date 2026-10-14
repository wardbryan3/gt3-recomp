#!/usr/bin/env bash
# Opt-in experiment only. Does not replace resolution/play-gt3-triple.sh.
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}" SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-wayland}"
export TMPDIR="$root/tmp" XDG_CACHE_HOME="$root/cache"
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME"
unset PS2_ONE_THREAD PS2_NO_VU_THREAD PS2_TIME PS2_WINDOW_BENCH
cd "$root/repo"
exec "$root/ps2run-sse41" games/gt3-usa-v110/core-triple.elf \
 --disc games/gt3-usa-v110/disc.iso --ntsc --window --gt3-triple \
 --output-size 5760x1080 --render-scale 9 --render-scale-y 3 "$@"
