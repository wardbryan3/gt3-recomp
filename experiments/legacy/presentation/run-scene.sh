#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
source "$root/session-env.sh"
scene="${1:-super}"; path="${2:-parallel}"; frames="${3:-3600}"; label="${4:-$scene-$path}"; shift $(( $# < 4 ? $# : 4 ))
case "$scene" in
 super) state="$root/../validation/race-start.state"; start=4801 ;;
 trial) state="$root/../validation/trial.state"; start=5999 ;;
 midfield) state="$root/../validation/midfield.state"; start=6599 ;;
 *) exit 2 ;;
esac
if [[ "$path" == single ]]; then export PS2_ONE_THREAD=1; elif [[ "$path" != parallel ]]; then exit 2; fi
mkdir -p "$root/results"
export PS2_PRESENT_CSV="$root/results/$label.csv"
pw-top -b > "$root/results/$label.audio-top.txt" 2>&1 & monitor=$!
trap 'kill "$monitor" 2>/dev/null || true; wait "$monitor" 2>/dev/null || true' EXIT
cd "$root/repo"
python3 "$root/observe.py" "$root/results/$label.log" timeout 600 "$root/repo/build/presentation/ps2run" \
 games/gt3-usa-v110/core-triple.elf --disc games/gt3-usa-v110/disc.iso --load-state "$state" \
 --ntsc --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --fullscreen \
 --press "$start:cross:2000" --frames "$((start+frames))" "$@"
grep -E '\[window\]|\[audio-device\]|\[surface\]|\[probe|\[shutdown\]|halted:' "$root/results/$label.log"
