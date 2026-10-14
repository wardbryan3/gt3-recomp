#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
build="${1:-$root/build/native-gt3-triple}"
common=(-std=c++20 -O2 -I"$root/host" -I"$root/runtime/include" -I"$root/runtime/src")
link=("$build/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm)
"${CXX:-clang++}" "${common[@]}" "$root/tests/gt3_controls_test.cpp" "$build/libps2game.a" "${link[@]}" -o "$build/gt3_controls_test"
"$build/gt3_controls_test"
"${CXX:-clang++}" "${common[@]}" "$root/tests/anisotropic_test.cpp" "${link[@]}" -o "$build/anisotropic_test"
"$build/anisotropic_test"
"$root/tests/run_gt3_hardware.sh" "$build"
