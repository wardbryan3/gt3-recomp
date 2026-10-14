#!/usr/bin/env bash
set -euo pipefail
experiment="$(cd "$(dirname "$0")" && pwd)"
cd "$experiment/repo"
export PATH="$experiment/../toolchain/bin:$PATH"
export TMPDIR="$experiment/tmp"
mkdir -p "$TMPDIR"
if [[ "${SSE41:-OFF}" == ON ]] && ! grep -q -w sse4_1 /proc/cpuinfo; then
    echo 'SSE4.1 is required for this opt-in experiment' >&2; exit 1
fi
echo '174f966d4f069b6ae69fe4eab9ab98e90fd99d1435c8d6e8958e4dd418fe8ae5  build/resolution-triple/libps2game.a' | sha256sum -c -
cmake -S . -B build/performance -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ -DPS2_EXPERIMENT_SSE41_GPU="${SSE41:-OFF}"
ninja -C build/performance -j 8 ps2runtime
# Reuse the copied, fingerprint-recorded game archive; no translated game changes.
clang++ -std=c++20 -O3 -DNDEBUG -DPS2_GPU -DPS2_WINDOW -DPS2_PROFILE \
  -Iruntime/include -Ithird_party/wgpu-native/include $(pkg-config --cflags sdl2) \
  host/main.cpp host/window.cpp host/profile.cpp \
  build/resolution-triple/libps2game.a build/performance/libps2runtime.a \
  third_party/wgpu-native/lib/libwgpu_native.a $(pkg-config --libs sdl2) -ldl -lpthread -lm \
  -o build/performance/ps2run
