#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
export TMPDIR="$root/tmp" XDG_CACHE_HOME="$root/cache"
unset PS2_TIME PS2_PROFILE PS2_WINDOW_BENCH
mkdir -p "$root/correctness"
cd "$root/repo"
base=(games/gt3-usa-v110/core-triple.elf --disc games/gt3-usa-v110/disc.iso --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --press 4801:cross:2000 --frames 5701)
for scene in bumper chase behind; do
  inputs=()
  if [[ "$scene" == chase ]]; then inputs=(--press 5600:r1:6); fi
  if [[ "$scene" == behind ]]; then inputs=(--press 5660:l1:100); fi
  for variant in baseline sse41; do
    for path in single vu; do
      tag="$scene-$variant-$path"
      PS2_DUMP="$root/correctness/$tag.ram" timeout 120 "$root/ps2run-$variant" "${base[@]}" \
        --load-state "$root/../validation/race-start.state" "${inputs[@]}" \
        --benchmark-path "$path" --benchmark-capture "$root/correctness/$tag.ppm" \
        > "$root/correctness/$tag.log" 2>&1
    done
  done
  for tag in "$scene-baseline-vu" "$scene-sse41-single" "$scene-sse41-vu"; do
    cmp "$root/correctness/$scene-baseline-single.ppm" "$root/correctness/$tag.ppm"
    cmp "$root/correctness/$scene-baseline-single.ram" "$root/correctness/$tag.ram"
  done
  echo "$scene pixels and EE/IOP/SPU memory match across paths and optimization"
done
# State work is separate from controlled performance samples.
timeout 120 "$root/ps2run-sse41" "${base[@]}" --load-state "$root/../validation/race-start.state" \
 --benchmark-path vu --save-state "5650:$root/correctness/parallel.state" \
 --benchmark-capture "$root/correctness/save-direct.ppm" > "$root/correctness/save.log" 2>&1
for path in single vu; do
 timeout 120 "$root/ps2run-sse41" "${base[@]}" --load-state "$root/correctness/parallel.state" \
 --benchmark-path "$path" --benchmark-capture "$root/correctness/reload-$path.ppm" > "$root/correctness/reload-$path.log" 2>&1
 cmp "$root/correctness/save-direct.ppm" "$root/correctness/reload-$path.ppm"
done
echo 'Parallel 9x3 save/reload matches uninterrupted run in both paths'
for variant in baseline sse41; do
 mkdir -p "$root/correctness/output-$variant"
 timeout 120 "$root/ps2run-$variant" "${base[@]}" --load-state "$root/../validation/race-start.state" \
  --frames-dir "$root/correctness/output-$variant" --frame-every 5701 > "$root/correctness/output-$variant.log" 2>&1
done
cmp "$root/correctness/output-baseline/frame_05701.ppm" "$root/correctness/output-sse41/frame_05701.ppm"
echo '5760x1080 presentation captures match; raw benchmark captures are 5760x1344'
