#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
cd "$root/repo"
export TMPDIR="$root/tmp" PATH="$root/../toolchain/bin:$PATH"
mkdir -p build/presentation "$TMPDIR"
echo '174f966d4f069b6ae69fe4eab9ab98e90fd99d1435c8d6e8958e4dd418fe8ae5  build/resolution-triple/libps2game.a' | sha256sum -c -
cmake -S . -B build/presentation -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ -DPS2_EXPERIMENT_SSE41_GPU=OFF
ninja -C build/presentation -j 8 ps2runtime
xml=/usr/share/qt6/wayland/protocols/presentation-time/presentation-time.xml
wayland-scanner client-header "$xml" build/presentation/presentation-time-client-protocol.h
wayland-scanner private-code "$xml" build/presentation/presentation-time-protocol.c
clang -c build/presentation/presentation-time-protocol.c -o build/presentation/presentation-time-protocol.o $(pkg-config --cflags wayland-client)
clang++ -std=c++20 -O3 -DNDEBUG -DPS2_GPU -DPS2_WINDOW -DPS2_PROFILE \
 -Iruntime/include -Ithird_party/wgpu-native/include -Ibuild/presentation $(pkg-config --cflags sdl2 wayland-client) \
 host/main.cpp host/window.cpp host/profile.cpp host/presentation_probe.cpp build/presentation/presentation-time-protocol.o \
 build/resolution-triple/libps2game.a build/presentation/libps2runtime.a \
 third_party/wgpu-native/lib/libwgpu_native.a $(pkg-config --libs sdl2 wayland-client) -ldl -lpthread -lm -o build/presentation/ps2run
cp build/resolution-triple/libps2game.a build/presentation/
