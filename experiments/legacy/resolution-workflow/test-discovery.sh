#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)";cd "$root"
export PATH="/home/b/experiments/gt3-native-20261013/toolchain/bin:$PATH"
mkdir -p build/foundation/discovery
clang++ -std=c++20 -O2 -I runtime/include tests/gt3_pedal_discovery.cpp \
 build/synthetic-wheel/libps2game.a build/synthetic-wheel/libps2runtime.a \
 third_party/wgpu-native/lib/libwgpu_native.a -ldl -lpthread -lm -o build/foundation/discovery/pedal-discovery
build/foundation/discovery/pedal-discovery games/gt3-usa-v110/core.elf
