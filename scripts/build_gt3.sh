#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -lt 1 || $# -gt 2 || ( $# -eq 2 && "$2" != --triple ) ]]; then
 echo 'Usage: scripts/build_gt3.sh /path/to/GT3.iso [--triple]' >&2; exit 2
fi
iso="$(realpath "$1")"; [[ -f "$iso" ]] || { echo 'Disc image not found' >&2; exit 1; }
name=gt3
[[ $# -eq 1 ]] || name=gt3-triple
# Separate local folders avoid overwriting a standard build with patched units.
"$root/scripts/port.sh" "$name" "$iso" --native-only
elf="$root/games/$name/core.elf"
[[ -f "$elf" ]] || { echo 'CORE.GT3 was not found; check your disc revision' >&2; exit 1; }
if [[ $# -eq 2 ]]; then
 elf="$root/games/$name/core-triple.elf"
 python3 -I "$root/scripts/gt3_triple.py" "$root/games/$name/core.elf" "$elf" \
  --manifest "$root/games/$name/triple-manifest.json"
 "$root/build/tools/eerecomp" "$elf" --entries "$root/games/$name/entries.txt" \
  --probes "$root/scripts/gt3_scene.probes" --out "$root/generated/$name"
 # Recreate compiled VU units after EE regeneration when local recordings exist.
 if compgen -G "$root/games/$name/vu1/*.bin" > /dev/null; then
  "$root/build/tools/vurecomp" "$root/games/$name/vu1" "$root/generated/$name"
 fi
 cmake --build "$root/build/native-$name" --target ps2run
fi
printf '\nRun locally:\n%q %q --disc %q --ntsc --window' \
 "$root/build/native-$name/ps2run" "$elf" "$root/games/$name/disc.iso"
if [[ $# -eq 2 ]]; then
 printf ' --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080'
fi
printf '\n'
