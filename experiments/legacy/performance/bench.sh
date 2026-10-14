#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
exe="${1:-$root/ps2run-baseline}"; path="${2:-single}"; label="${3:-probe}"
mkdir -p "$root/results" "$root/tmp" "$root/cache"
export TMPDIR="$root/tmp" XDG_CACHE_HOME="$root/cache"
unset PS2_TIME PS2_PROFILE PS2_GS_PROFILE PS2_ONE_THREAD PS2_NO_VU_THREAD
cd "$root/repo"
exec timeout 180 "$exe" games/gt3-usa-v110/core-triple.elf \
 --disc games/gt3-usa-v110/disc.iso --load-state "$root/../validation/race-start.state" \
 --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080 \
 --press 4801:cross:2000 --frames 5701 --benchmark-path "$path" \
 --benchmark-capture "$root/results/$label.ppm"
