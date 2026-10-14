#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
for pair in 1 2 3; do
 for variant in baseline sse41; do
  for path in single vu; do
   label="repeat-$variant-$path-$pair"
   "$root/bench.sh" "$root/ps2run-$variant" "$path" "$label" > "$root/$label.log" 2>&1
   grep '\[benchmark\]' "$root/$label.log"
  done
 done
 for variant in baseline sse41; do
  for path in single vu; do
   cmp "$root/results/repeat-baseline-single-$pair.ppm" "$root/results/repeat-$variant-$path-$pair.ppm"
  done
 done
done
