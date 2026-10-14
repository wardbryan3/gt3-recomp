#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)";cd "$root"
mode="${1:?generated or clean}";shift
[[ "$mode" == generated || "$mode" == clean ]] || exit 2
for arg in "$@"; do
 [[ "$arg" != --memcard && "$arg" != --memcard=* ]] || { echo 'Disposable cards only.' >&2; exit 2; }
done
[[ -x "build/foundation/$mode/ps2run" ]] || { echo "Build $mode first." >&2;exit 1; }
sandbox="$(mktemp -d "$root/build/foundation/$mode/run-XXXXXX")"
export PS2_ONE_THREAD=1
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-wayland}"
echo "Disposable run: $sandbox" >&2
exec "build/foundation/$mode/ps2run" games/gt3-usa-v110/core-triple.elf \
 --disc games/gt3-usa-v110/disc.iso --ntsc --window --gt3-triple \
 --output-size 1920x360 --render-scale 3 --render-scale-y 1 --memcard "$sandbox/card.ps2" "$@"
