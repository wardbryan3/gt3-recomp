#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
build="${1:-$root/build/native-gt3-usa-v110}"
"${CXX:-clang++}" -std=c++20 -I"$root/runtime/include" -I"$root/runtime/src" \
  "$root/tests/gt3_hardware.cpp" "$build/libps2runtime.a" \
  "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm \
  -o "$build/gt3_hardware_test"
"$build/gt3_hardware_test"
