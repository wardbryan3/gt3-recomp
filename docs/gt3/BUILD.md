# Building GT3 locally

## Standard native path

```bash
scripts/build_gt3.sh /path/to/GT3.iso
build/native-gt3/ps2run games/gt3/core.elf --disc games/gt3/disc.iso --ntsc --window
```

The helper calls upstream's discovery pipeline with the GT3 CORE extraction fix.
The ISO is linked/read, not patched. Native window/audio need SDL2. Use a suitable
compiler, Git/CMake/Ninja/Python, and the SDK fetched by setup. Archived discs can
be handled directly by `scripts/port.sh gt3 /path/to/archive --native-only`.
The wrapper currently accepts an ISO and prints the tested USA/NTSC launch mode;
other disc revisions or regions need their own validation/rate selection.

## Optional triple profile

```bash
scripts/build_gt3.sh /path/to/GT3.iso --triple
build/native-gt3-triple/ps2run games/gt3-triple/core-triple.elf \
  --disc games/gt3-triple/disc.iso --ntsc --gt3-triple \
  --render-scale 9 --render-scale-y 3 --output-size 5760x1080 --window
```

Only the fingerprint-pinned USA PBPX-95503 v1.10 core is accepted by the patch
recipe. It writes a separate output ELF and local manifest; expected instruction
words are checked. Patched EE units are regenerated with the scene probe, then
locally recorded VU units are regenerated. Standard and triple builds are separate.
This does not configure a desktop output: the drawable can be constrained by your
compositor. Check actual window size instead of assuming requested size was granted.

Full 9×3 sampling has a large memory budget and is not the default. Allocation
limits are checked and oversized GPU configurations are rejected. The inherited
host may fall back to software rendering; inspect its backend output rather than
assuming the requested GPU sampling is active.
The game still uses translated EE code and an emulated console runtime.

## Native comparison options

- Upstream parallel execution is the default; `PS2_ONE_THREAD=1` selects its
  single-thread path.
- `PS2_PRESENT_MODE=fifo` is an explicit surface-mode experiment; unset preserves
  upstream selection. FIFO can improve cadence but increase buffering latency.
- `-DPS2_NATIVE_SSE41=ON` enables SSE4.1 compilation only for native x86 graphics
  preparation. It has **no runtime CPU dispatch**; use only a supporting CPU.
  Default OFF retains portable code and is required for ARM/browser builds.

```bash
cmake -S . -B build/native-gt3-triple -DPS2_NATIVE_SSE41=ON
cmake --build build/native-gt3-triple --target ps2run
```

## Tests and snapshots

Synthetic CTest regressions need no game, generated code or GPU SDK (README command).
GPU sampling/state conversion and the actual translated-input differential test
are local-only Linux tests after building the appropriate game library:

```bash
tests/run_resolution_tests.sh "$PWD/build/native-gt3-triple"
```

The differential routine addresses are pinned to the supported USA core; do not
use that test to claim coverage for another revision. GPU tests require an adapter
capable of the requested buffers. Frame-limit/screenshot checks are not proof of
proper joinable worker teardown.

This rebased fork's snapshot format is **version 3**; private experiment/upstream
version-2 snapshots are not imported. Memory cards are separate from snapshots.
Use new local paths; never overwrite an existing user's save to run a test.

## Browser status

Upstream browser infrastructure remains, but native fork validation must not be
represented as completed GT3 browser validation. Generic browser builds can be
attempted with `scripts/port.sh gt3 /path/to/GT3.iso` after installing Emscripten;
triple-profile/browser UI integration and browser regressions remain follow-up work.
Do not publish generated WebAssembly/data or serve your ISO to untrusted clients.
