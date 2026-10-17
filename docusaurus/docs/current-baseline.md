---
title: Historical native-v3 baseline
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

This record describes the earlier native-v3 baseline evaluated from source base
`82987dec7a71d76414adfff8663da5494a280938` plus its validation overlay.
“Current,” “fresh,” and stop instructions below refer to that checkpoint, not the
present repository. Its clean/synthetic gates ran only in an isolated validation
host. The recipes are retained historical instructions, not maintained build commands.
See [current authorities](reference/current-authorities.md) and
[validation layers](testing.md) for present proof and approval boundaries.

:::


## Scope and authority

This cycle restores build/validation prerequisites only. It does not recover
pedals or change gameplay, control algorithms, rendering, or the save-state
format. Evaluated source base was `82987dec7a71d76414adfff8663da5494a280938`, plus
the reviewed validation scripts, test-only host wrapper and registry/docs updates.
Canonical `host/`, `runtime/`, `recomp/` and root CMake gameplay/build targets are
unchanged. The previous pedal audit remains a historical stopped-cycle report.

Results for this historical checkpoint were recorded separately in
`decomp/gt3/current-validation.json`, now located at
`project/gt3/current-validation.json`; the [public authority](pathname:///knowledge/current-validation.json)
retains the checkpoint's gate results and limitations.
`project/gt3/migration-map.json` also locates the host, clock shim and layout probe
at `validation/gt3/live/gt3_baseline_{host,clock,layout}.cpp`. These are current
locators, not replacements for the exact evaluated historical source versions.
The older per-function lifecycle/differential/live fields still describe the
preserved private experiment. New baseline evidence does not automatically promote
pedals or establish all-game compatibility.

## Recorded historical result {#recorded-current-result}

**PASS, bounded native baseline.** Four fresh canonical executables built in
independent directories have identical SHA-256
`b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a`.
The trusted v3 race fixture is
`local/baseline-v3/accepted-live/capture/race-start-v3.state`, SHA-256
`da2661b490f977bd2d1b4d076d957bd8580aebf301f3c02e83b25964312c895a`.
It was saved by canonical normal boot, not an old-state conversion.

The 28 recorded live runs include independent boots, canonical repeat/replay,
uninterrupted continuation, disabled/trace-only, clean pad and ten generated/clean
wheel pairs. Wheel coverage is **3,400 clean mode-4 updates / 13,600 original
consumer calls**, maximum reconstruction error **5.96046448e-8**, unchanged
**2e-6** tolerance. Pad coverage is 800 clean normalizations and 200 wheel-builder,
filter and envelope calls. All compared semantic traces, captures and complete
EE/IOP/SPU dumps match exactly. The two accelerated opposite-sign captures were
reviewed; both show racing at 81 mph with opposite turns. No performance or physical
input claim follows from that observation.

Fresh regressions pass: 25,600 normalization / 57,344 mapped actions; 15,360 pad
frames; 19,468 wheel commands / 7,560 driving frames; clean exact matrices of
28,160 / 16,384 / 16,000 / 20,000 cases; synthetic 8,193 quantizations / 42
integrations; 22 **original-only** pedal fixtures; hardware/SIF, source consistency,
9x3 anisotropic GPU/state conversion, patch, metadata/publication and docs checks.
Metadata consistency/negative coverage now has 19 tests. The new read-only
padding comparator additionally has seven synthetic tests,
including rejection of every nonpadding byte mutation. Existing assertions remain
unchanged.

New authority pins 15 private artifacts and a hashed manifest of all **302 live
evidence files**. `just verify-current "$PWD"` fails on missing/changed members,
including traces, complete dumps and captures, and independently checks the native
v3 header. Historical `verify-private` still verifies its original eleven hashes
and 66 evidence IDs. No evidence hash was rewritten to hide a failed attempt.

## Toolchain restoration and fresh builds

The missing packages were installed using the machine's package manager:
CMake 4.4.4 and Ninja 1.13.2, with their required `cppdap`/`rhash` dependencies.
Existing Clang 23.1.1, SDL2 compatibility development files and Vulkan support were
used. `scripts/fetch_wgpu.sh` fetched the documented **wgpu-native v29.0.1.1** into
ignored third-party storage. No compiler/runtime downgrade, system upgrade,
service, firewall or desktop change was performed. Package-manager snapshot hooks
ran normally.

There are separate fresh software-only and GPU/native build directories. EE and
VU translations are regenerated using **current-main eerecomp/vurecomp**, original
fingerprint-verified USA v1.10 ELF, retained discovery entry seeds and retained VU
recordings. No old generated source or compiled game/runtime library is linked.
This is not a claim of fresh-from-ISO discovery coverage for every scene.

The following recipe is historical; its bespoke baseline builders are retired.
Do not change old paths to suggest it runs on today's tree. Maintained public
checks are `just check`, `just test`, `just docs-build`; root
`just verify-historical baseline "$PWD"` (also `just verify-current "$PWD"`) verifies
this **historical** checkpoint, not current product qualification.

```bash
just test
scripts/fetch_wgpu.sh
scripts/build_gt3_baseline.sh /absolute/private/gt3-usa-v110 /absolute/new/build-root
tests/run_gt3_baseline.sh /absolute/new/build-root /absolute/private/core.elf \
  /absolute/new/regression-results
python3 scripts/validate_gt3_baseline.py \
  --build /absolute/new/build-root --elf /absolute/private/core.elf \
  --iso /absolute/private/GT3.iso --out /absolute/new/live-results
just check
just docs-build
just verify-private /absolute/preserved/resolution-repo
just verify-current "$PWD"
```

The input directory must supply `core.elf`, `entries.txt`, and `vu1/*.bin`.
Output directories must not already exist. The normal native binary is
`BUILD_ROOT/original/ps2run`; the isolated validation binary is
`BUILD_ROOT/observed/gt3_baseline_host`. Exact source/input/generated/executable
hashes and compiler identity are retained in private `build-identity.json`.
Public source/schema/docs tests still require no game or GPU.

## Validation-only installation, not a canonical runtime feature

The normal generated translation has **no added clean/synthetic gates**. A second
fresh translation uses the existing wheel observation probes and four unchanged
frozen steering gates, retaining generated bodies as fallback:

- `00210F90`: normalization;
- `002115F8`: wheel builder, existing shipped-vtable guards;
- `001E4368`: stick filter;
- `001E45A8–001E48FB`: steering interior; resumes original `001E48FC`.

Only `tests/gt3_baseline_host.cpp` enables these in its isolated process, and only
when `--gt3-clean-steering` is passed. Its synthetic input additionally requires
`--gt3-wheel` / `--gt3-wheel-at`; trace-only does not inject input. The wrapper
calls the **existing normal host main**, boot/load/run logic and existing clean /
synthetic source. It does not add options or hooks to canonical ps2run. No new
pedal/control implementation or direct final-steering-state injection was added.
Profile checks, fallback and original EE cost accounting remain unchanged.

## Native v3 fixture construction

No old state is accepted by the capture script. It starts canonical ps2run from
normal boot, uses a fresh disposable card path, and supplies scheduled pad input:
Start at 300, then Cross at 600 through 4500 in 300-frame increments. These select
an Arcade race through normal menus. The reviewed exploratory capture showed the
Super Speedway race, lap 1/2, car stationary; captures remain private.

The final recipe requests `--save-state 4801:NEW_PATH --frames 4802`, so the normal
runtime saves **native version 3 at frame 4801**. No header rewrite, import loader,
RAM patch, old save-state execution or save-state-format change occurs. The
fixture, executable, ELF, ISO, build identity, validator and clock environment are
fingerprinted. The same fixture must replay deterministically before live
comparisons are accepted. Continuation pad input begins at **4802**, not 4801:
`vblank()` samples frame-4801 inputs before requesting that frame's state save.
Supplying new frame-4801 input only on an uninterrupted boot is not an equivalent
scenario to loading the already-sampled snapshot. A diagnostic pair using future
frame-4802 input matched complete dumps and captures exactly; the final validator
retains that strict uninterrupted-versus-resumed comparison.

### Clock input and retained failed attempts

The first capture attempt assumed the historical frame-4800 request would save
frame 4801; current main saves the requested frame 4800. The recipe now explicitly
requests frame 4801. No runtime timing code was changed.

Two subsequent independent normal boots produced identical reviewed race captures
but different complete state bytes. Current `runtime/src/iop/cdvd.cpp` and
`cdvdfsv.cpp` read `std::time` for the external CD/DVD UTC clock; time-derived guest
state differed between boots. The failure is retained, not rehashed or silently
normalized away.

For reproducibility, `tests/gt3_baseline_clock.cpp` builds a **process-local test
clock-input shim**. Only validation subprocesses use `LD_PRELOAD` with
`GT3_BASELINE_UTC_EPOCH=1791964800` (2026-10-14 08:00:00 UTC). It supplies that fixed
value to the original `time()` calls. It does **not** intercept monotonic clocks,
change the machine clock, modify game memory, alter simulation timing or install
itself into ps2run. The shim is hash-pinned with the other build inputs. Canonical runtime outside this test environment continues to read the normal host
clock.

With the UTC input pinned, independent boots produced **exact complete guest
memory dumps**, but raw snapshots still differed in 23 bytes. A compiler-layout
audit located every difference in native EE `Thread` padding (member gaps
60–63 and 72–79, size 768). The existing state writer serializes that whole host
object. The read-only `tests/gt3_baseline_layout.cpp` includes the authoritative
source type and compiles exact offset/size assertions. It does not implement a
new loader or writer.

:::caution Unresolved historical padding count

The prose above reports **23 differing bytes**, whereas the unchanged authority
`project/gt3/current-validation.json` reports **22**. This discrepancy is
**UNRESOLVED**: the available public account does not establish whether these
refer to different attempts or a reporting error. Both original assertions are
preserved; no count is selected or recomputed here, and no authority, hash,
fixture or expected result is changed. Resolving it requires the pinned historical
comparison reports, not an editorial inference from padding layout.

:::

The new validator's initial raw-file-equality assumption was therefore too broad.
It now asserts that **every defined serialized byte is equal**, any raw difference
lies exclusively in those compiled padding slots, and all complete EE/IOP/SPU dumps
and captures match. Any difference outside those slots is fatal. Neither snapshot
is normalized or rewritten: both original hashes and the differing offsets are
retained. Existing steering, GPU, ABI/budget and live equality checks are unchanged.
The pinned fixture is a specific immutable raw file; recreating normal boot may
produce another raw hash because of unspecified host padding.

## Acceptance and limitations

The validator requires independent normal-boot defined-state equality (with only
the proven native padding distinction described above), exact guest dumps, matching
canonical snapshot replays, equality against uninterrupted normal-boot
continuation, disabled/trace-only equivalence, clean pad equivalence and ten wheel
scenarios (seven fixed values, signed transition through center and both
accelerated opposite-sign cases). It checks exact semantic traces, every captured
frame, final complete EE/IOP/SPU memory dumps, independent clean-call counters and
original downstream consumer probes. Reconstruction tolerance remains **2e-6**.
Clean semantic seams are bridge observations, not claims that skipped EE
instructions executed.

This historical checkpoint's acceptance status and artifact fingerprints are in
the machine-readable current-validation registry. Its name does not make it the
present product baseline. Do not infer a pass from the recipe alone.

All applicable native tests are run unchanged: hardware/SIF, controls/mapping,
pad/wheel steering, clean differential, synthetic adapter, original-only pedal
propagation, anisotropic GPU sampling/state conversion, patch, metadata,
publication, documentation and repository checks. No assertion in the pre-existing
suites was weakened. This does not claim browser, physical-wheel/pedal, physical
scanout, full-game compatibility or long-session coverage. Existing overlay/replay
and detached-VU teardown limitations remain.

**Stop after this baseline.** Pedal recovery still requires its own join-level
ABI/cost/descriptor differential and authorization to resume that cycle. No
transmission, clutch, handbrake, FFB, renderer, reset or physical-adapter work is
part of this validation task.
