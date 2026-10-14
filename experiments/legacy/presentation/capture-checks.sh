#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
source "$root/session-env.sh"
export PS2_PRESENT_MODE=fifo PS2_PRESENT_HOLD_MS=5000
mkdir -p "$root/captures"
cd "$root/repo"
for scene in bumper chase behind reload; do
 inputs=(); state="$root/../validation/race-start.state"
 if [[ "$scene" == chase ]]; then inputs=(--press 5600:r1:6); fi
 if [[ "$scene" == behind ]]; then inputs=(--press 5660:l1:100); fi
 if [[ "$scene" == reload ]]; then state="$root/captures/window.state"; fi
 for path in single parallel; do
  if [[ "$path" == single ]]; then export PS2_ONE_THREAD=1; else unset PS2_ONE_THREAD; fi
  label="$scene-$path"; export PS2_PRESENT_CSV="$root/captures/$label.csv"
  timeout 60 "$root/repo/build/presentation/ps2run" games/gt3-usa-v110/core-triple.elf \
   --disc games/gt3-usa-v110/disc.iso --load-state "$state" --ntsc --gt3-triple \
   --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --fullscreen \
   --press 4801:cross:2000 --frames 5701 "${inputs[@]}" > "$root/captures/$label.log" 2>&1 & app=$!
  for ((i=0;i<550;i++)); do grep -q '\[capture-hold\]' "$root/captures/$label.log" && break; sleep .1; done
  grep -q '\[capture-hold\]' "$root/captures/$label.log"
  timeout 10 spectacle -b -n -f -o "$root/captures/$label.png" > "$root/captures/$label.screenshot.log" 2>&1
  wait "$app"
  magick "$root/captures/$label.png" rgb:- | sha256sum > "$root/captures/$label.pixel.sha256"
 done
 cmp "$root/captures/$scene-single.pixel.sha256" "$root/captures/$scene-parallel.pixel.sha256"
 echo "$scene actual compositor screenshots match across single and parallel"
done
cmp "$root/captures/bumper-parallel.pixel.sha256" "$root/captures/reload-parallel.pixel.sha256"
echo 'Window save/reload matches uninterrupted compositor pixels'
