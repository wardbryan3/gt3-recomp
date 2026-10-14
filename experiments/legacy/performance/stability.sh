#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$root/stability"
export TMPDIR="$root/tmp" XDG_CACHE_HOME="$root/cache"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}" WAYLAND_DISPLAY=wayland-0
export SDL_VIDEODRIVER=wayland SDL_AUDIODRIVER=dummy PS2_WINDOW_BENCH=1
unset PS2_ONE_THREAD PS2_NO_VU_THREAD PS2_TIME PS2_PROFILE
cd "$root/repo"
TIMEFORMAT='wall_seconds=%R'
{ time timeout 600 "$root/ps2run-sse41" \
 games/gt3-usa-v110/core-triple.elf --disc games/gt3-usa-v110/disc.iso \
 --load-state "$root/../validation/race-start.state" --gt3-triple \
 --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --frames 40801 --window \
 --press 4801:cross:2000 --press 6000:r1:6 --press 6600:r1:6 --press 7000:l1:120 \
 --save-state "40000:$root/stability/window.state"; } > "$root/stability/window.log" 2>&1
unset PS2_WINDOW_BENCH
for path in single vu; do
 timeout 120 "$root/ps2run-sse41" games/gt3-usa-v110/core-triple.elf \
 --disc games/gt3-usa-v110/disc.iso --load-state "$root/stability/window.state" \
 --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --frames 40801 \
 --benchmark-path "$path" --benchmark-capture "$root/stability/reload-$path.ppm" \
 > "$root/stability/reload-$path.log" 2>&1
done
cmp "$root/stability/reload-single.ppm" "$root/stability/reload-vu.ppm"
echo '36000-frame unpaced window continuation and cross-path final-state reload PASS'
