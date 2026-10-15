# GT3 Recomp

An experimental **Gran Turismo 3 recompilation and reverse-engineering project**,
based on [snuri00/ps2-web-recomp](https://github.com/snuri00/ps2-web-recomp).
The scope of this fork is GT3: compatibility, readable reconstructions, native
rendering, controls, and repeatable validation—not a new general-purpose PS2
emulator or a claim to have recovered the original game source.

**Bring your own legally obtained GT3 disc image. No game executable, assets,
generated game translations, or game-containing builds are distributed.**

## Selective-decompilation checkpoint

The project now has one source-of-truth workflow: root `justfile`, `AGENTS.md`,
[HANDOFF.md](HANDOFF.md), `decomp/gt3` inventories and the curated Docusaurus site.

```bash
just check                 # source/schema/types/publication; no game needed
just test                  # source-only regressions; NOT a live-game oracle
just setup && just docs-build
just status
just lookup 0x001e4478
```

Readable mapping, clean steering and independent synthetic-wheel source are
preserved with original-dependent fixture source. **The recovered library is
compile checked, not linked into ps2run or installed into generated bodies.**
Historical exact/live results are explicitly contextualized. Fresh current-main
baseline evidence is tracked [separately](docs/site/docs/current-baseline.md), using
an isolated validation host rather than installing hooks into canonical ps2run.
[Pedal Recovery v1](docs/site/docs/pedal-v1.md) now has a separately pinned bounded
validation-only replacement; canonical ps2run remains generated-only. No physical
pedal/FFB/AI API is implemented here. The later bounded
[descriptor/profile characterization](docs/site/docs/pedal-profiles.md) and
read-only [admission audit](docs/site/docs/pedal-admission-49af40.md) retain their
historical stopped results. A separately authorized
[observed-context closure](docs/site/docs/pedal-closure.md) now proves the unchanged
body at all 4,199 retained representative entries, including Time Trial’s alternate
stack position. Structural caller-frame admission passes 4,199 actual guarded
substitutions with zero fallback. This bounded validation-only checkpoint is
re-frozen; no universal reachability, physical-device or canonical integration
claim, and no adjacent work follows automatically.

A separate [Synthetic / Virtual Pedal Controller v1](docs/site/docs/virtual-pedals.md)
provides opt-in, frame-scheduled normalized throttle/brake at the original command
boundary. It preserves Frozen semantics and original downstream simulation, has no
canonical installation, and does not claim physical pedals or calibration. See its
separate bounded proof and `just verify-virtual-pedals EXPLICIT_REPOSITORY_ROOT`.

[Legacy source ledger](experiments/legacy/README.md) preserves unique old source
variants as restoration patches, not copied active runtime repositories. Raw
exports and game artifacts remain private; public docs build without them.

## What comes from upstream

The EE static recompiler, VU translation infrastructure, emulated PS2 runtime,
WebGPU GS renderer, browser frontend, and existing parallel execution architecture
originate upstream. Its Git history, MIT license, copyright and third-party
notices are retained. This fork does not claim that architecture or the large
parallel-versus-single speed difference as a new invention.

## GT3 work in this fork

- `CORE.GT3` extraction/porting support alongside the inherited CORE format tooling.
- SIF descriptor reads through EE address decoding, including scratchpad.
- Correct transition to idle when the final running guest thread is deleted.
- Limited i.Link register initialization/PHY behavior, **not network play**.
- Independent horizontal/vertical GS sampling and adapter allocation-limit checks.
- Native output dimensions, aspect control, scripted analog input, and a
  fingerprint-checked **USA PBPX-95503 v1.10** triple-width projection profile.
- A readable input-normalization reference and local differential-test harness.
- Optional native FIFO comparison and opt-in x86 SSE4.1 graphics preparation.
- Synthetic hardware regressions plus local GPU and game-dependent tests.

Upstream now has an interrupt latch fix equivalent to a local experiment;
this fork keeps the upstream implementation rather than duplicating it.

## Build locally

Linux/native is the currently validated experiment path. You need Git, CMake,
Ninja, Python 3, Clang with C++20 support, and SDL2 development files for a window.
The inherited VU implementation uses Clang vector builtins; GCC is not supported.
Setup downloads wgpu-native into ignored local storage. No system package or
firewall changes are made by these build scripts.

```bash
# Native GT3 extraction, discovery, and compilation (ISO stays local):
scripts/build_gt3.sh /absolute/path/to/your/GT3.iso

# Optional fingerprint-pinned triple-width profile:
scripts/build_gt3.sh /absolute/path/to/your/GT3.iso --triple
```

These use the inherited exploring/entry-discovery pipeline. Discovery depends
on the scenes exercised; it is not proof that every game mode has been covered.
The original ELF/ISO are not modified. Triple output is a separate local ELF.
See [build instructions](docs/gt3/BUILD.md) before enabling the triple profile.

## Status and limits

The private experiment reached menus and races, exercised bumper/chase and
look-behind, and validated save/reload and full 9×3 sampling. An isolated native
5760×1080 window and a center-cropped 1080p browser stream were exercised.
These are **observations on one setup**, not a promise of smooth 60 FPS on every
machine. Physical scanout, complete game compatibility, and joinable native VU
shutdown are not established. Some overlays/replays remain incorrect.

This source tree is rebased onto upstream commit
`a02cdd56a8ab5077724da2b5ff8ca683024d7cf4`. The experiment's full validation
results must not be confused with validation of this newly rebased tree.
[Status](docs/gt3/STATUS.md) distinguishes those cases. Browser GT3 parity and
fresh-clone end-to-end discovery need additional validation.

## Tests

```bash
# No ISO or generated game code required; software runtime:
cmake -S . -B build/tests -G Ninja -DCMAKE_CXX_COMPILER=clang++ -DBUILD_TESTING=ON \
  -DPS2_WGPU_DIR="$PWD/build/no-gpu-sdk"
cmake --build build/tests --target gt3_hardware_test sif_scratchpad_test
ctest --test-dir build/tests --output-on-failure
python3 tests/gt3_patch_test.py
python3 scripts/audit_public.py
```

With a locally generated GT3 library and GPU SDK, the additional sampling and
translated-routine differential tests are described in the build guide.

## Recompilation and decompilation

Recompilation translates the original executable **locally**; that generated
code is not public project source. Readable reference implementations and
future reconstructed modules belong in the project after provenance review.
The [decompilation roadmap](decomp/README.md) tracks that work without claiming
complete source recovery. Assembly/decompiler dumps stay private by default.

## Controls (native)

Z accelerates/confirms; A brakes; arrow keys steer/navigate; W is R1 (bumper/chase);
hold Q for L1 (look behind); Enter pauses. X is Circle, S is Triangle, 1/2 are
L2/R2, and Backspace is Select. Exact in-game actions depend on mode/bindings.

## Contributing, provenance and legal

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [publication policy](docs/gt3/PUBLICATION.md).
Generic fixes should be proposed upstream as focused PRs; GT3-specific work
remains this project's focus. Patch address leads retain their attribution in
`scripts/gt3_triple.py`; candidate roles are not recovered original symbols.

Original project code is under [MIT](LICENSE); preserve all existing notices,
including the BSD notice in `runtime/src/ipu/NOTICE`. The license does **not**
license GT3's executable, data, or generated translations. Gran Turismo and
PlayStation are their owners' trademarks. This project is not affiliated with
Sony, Polyphony Digital, or the upstream maintainer. Do not upload game files,
private dumps, or game-containing release binaries.
