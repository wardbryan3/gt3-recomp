---
title: Build, discover and run
---

## Public development, no game

Use Linux with Git, Python 3, CMake, Ninja, **Clang with C++20**, `just`, Node 22+
and npm. SDL2 development files enable a native window. The VU implementation uses
Clang vector builtins; a GCC fallback is not supported. Public checks do not need
wgpu, Vulkan, an ISO, generated game code or historical private workspaces.

```sh
git clone REPOSITORY_URL gt3-recomp
cd gt3-recomp
just check
just test
just setup
just docs-build
```

Use the actual repository URL for `REPOSITORY_URL`. Historical public consistency
checks need Git revision `aee79fba37937e4dc99dac4263589d005112c504` and its blobs.
Normal full clones retain it. A shallow checkout must fetch the required history,
for example `git fetch --unshallow`; unavailable history is an error, not permission
to read current source as its predecessor. CI fetches full history explicitly.

`just build` configures isolated software-runtime source tests under `build/gt3-public-source`;
`just test` runs them and preserved historical reducer/authority negatives. Neither
is live-game proof. `just status` distinguishes current integration from historical
findings. `just lookup ADDRESS` / `just evidence ADDRESS` expose public knowledge,
not raw assembly or dumps. `just evidence ADDRESS` emits historical manifest
records as JSON, not decompiler pseudocode.

### Optional private analysis tooling

REA is an optional private analysis tool, **not a public build/test dependency**.
The tracked `scripts/project/rea-local.sh` launcher expects a separately installed,
licensed REA/Ghidra/JDK stack under ignored `local/rea/`; a fresh public clone does
not supply it. Review the launcher's prerequisites before use. Agent configuration,
credentials, analysis databases and sessions stay private. None is needed for the
public commands above or fresh ISO generation below.

## Fresh original generation and both products

Bring a legally obtained **USA PBPX-95503 v1.10** ISO. Supported original ELF SHA256:
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
The retained comparison ISO is
`0946bb943a766d0afe057fbff5aa96132b16a797f3e3edc985a3b6d2f3afee0e`.
Install Vulkan/driver support and SDL2 development files for GPU/window execution.
The existing setup script fetches wgpu-native into ignored local dependency storage;
it does not install game files or change firewall/system services.

```sh
just build-game /absolute/path/to/GT3.iso my-gt3-build
build/native-my-gt3-build/ps2run games/my-gt3-build/core.elf \
  --disc /absolute/path/to/GT3.iso --ntsc --window
build/native-my-gt3-build/gt3-native games/my-gt3-build/core.elf \
  --disc /absolute/path/to/GT3.iso --ntsc --window
```

Always choose a **new** name. The pipeline extracts the executable, translates EE,
boots/explores with a 5,101-frame bound and up to eight discovery rounds, captures
VU programs and compiles original code. Assembly independently regenerates EE/VU
units into a separate ignored directory and requires exact file-set/hash identity,
then supplies an explicit authenticated source list to CMake. Both product link
closures/maps and build/input/tool identities are recorded privately.

No old generated library or private workspace is needed to perform this generation
and build. The ISO/ELF remain unchanged. Discovery is scene-dependent: a completed
bounded discovery run is **not** full-game coverage. Further discovery requires a
new qualified context, not silently adding an old generated overlay.

Native defaults are original-equivalent. Readable GT3 libraries are compile/fixture
checked but not installed. `ps2run` rejects GT3 enhancement options. The inherited
native-only presentation path is not a newly qualified triple-screen simulator
configuration; that milestone still requires separate approval and hardware proof.

## Native runtime and build options

Keep comparison settings explicit; these are existing host/build controls, not new
simulator qualification:

- Upstream parallel execution is the default; `PS2_ONE_THREAD=1` selects the
  single-thread path for comparison.
- `PS2_PRESENT_MODE=fifo` requests FIFO surface presentation. Leave it unset for
  upstream selection. Measure cadence and input latency: FIFO may improve pacing
  but add buffering, and is not a smooth-frame-rate guarantee.
- CMake `-DPS2_NATIVE_SSE41=ON` requires SSE4.1 on native x86-64 graphics preparation.
  There is **no runtime CPU dispatch**. Default OFF is the portable setting and
  must remain OFF for ARM/browser builds; do not enable it on unsupported CPUs.
- `--render-scale` / `--render-scale-y` increase internal sampling, not desktop
  resolution. High sampling has a large GPU memory cost; adapter buffer-limit
  checks reject oversized configurations. Inspect backend diagnostics: failed GPU
  initialization can fall back to software rendering.
- `--output-size WxH` requests a drawable size, but the window system/compositor
  can constrain it. Check the actual drawable and active backend rather than
  assuming the requested size or GPU sampling was granted.

Native Linux evidence does not qualify GT3 browser execution. The inherited
browser infrastructure remains, but browser regressions and presentation/UI
integration require their own validation; do not publish generated WebAssembly,
game data or an ISO through a web server. See [testing limits](validation.md).

## Inputs and evidence

Native keyboard mapping: Z accelerates/confirms, A brakes, arrows steer/navigate,
W is R1, Q is L1, Enter pauses, X is Circle, S is Triangle, 1/2 are L2/R2 and
Backspace is Select. Exact in-game actions depend on mode/bindings.

Fresh private acceptance additionally requires the exact retained fixtures and
oracles; those are intentionally not in a public clone. See [testing](validation.md).
Missing private inputs fail explicit verification rather than silently reducing the
matrix. Do not publish generated source, executable outputs, states/cards or captures.
