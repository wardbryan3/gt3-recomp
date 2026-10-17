---
title: "Historical: gt3-clean-steering"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


> Preserved experiment narrative, not validation of current main. Commands refer to the historical runtime. Raw exports and game artifacts are private.

# GT3 readable steering-boundary experiment

Completed in `resolution/repo`, uncommitted and opt-in. This continues the completed
[synthetic experiment](gt3-synthetic-wheel-experiment.md), without modifying that
adapter, its launcher, its generated oracle, or its retained evidence.

## Exact replacement boundary

| Original address/range | Readable implementation | Runtime coverage |
|---|---|---|
| `00210F90–0021104F` | `normalize_mapped_channel` | Entire mapped-input normalization routine; shared callers retain the same behavior |
| `002115F8–0021174F` | `build_wheel_command` | Entire builder, **only** for shipped input vtable `0033F7E0`, zero adjustments, getters `0022DFA8` / `0022E000` |
| `001E4368–001E4467` | `filter_stick` | Entire stick spring/damping/rate/overshoot filter |
| `001E45A8–001E48FB`, within `001E4478` | `process_steering` | Envelope extension/clamping, modes, wheel limit slew, history, stick filtering, final steering and envelope-ratio update |

**This does not replace all of `001E4478`.** Its generated prologue and prefix
`001E4478–001E45A7` remain: classification (`001F2F68`), table lookup, nonnegative
curve input, curve selection and original interpolation (`001D8FB8`). The bridge
receives the resulting curve limit, classification and averaged wheel quantity.
Execution resumes at generated `001E48FC`: all pedal, shift and remaining vehicle
control processing, its original callees, and the epilogue remain generated.

The wheel builder necessarily preserves its existing pedal/digital command writes;
this is not a new pedal feature. `00210EF8`, `002115D8`, `001E4470` and `001E4320`
semantics are expressed inside the clean routines where needed, but their other
original entry points are **not** installed as replacements. The normalizer is
shared by mapped actions; those callers are not redesigned.

Original `00210DA8`, `00210E68`, mapping lookup, pad dispatcher, command hooks,
wheel enumeration/report ingestion, `001E8978`, `001E8910`, `001E7328`, and all
simulation/rendering remain generated. No host value is written directly to
`car +13A0`; clean code calculates it from the original command/state boundary.

## Source, layout and arithmetic

Current locators from `project/gt3/migration-map.json` are
`src/gt3/gameplay/controls/gt3_clean_steering.{hpp,cpp}` and
`validation/gt3/differential/gt3_clean_steering_test.cpp`. The historical `host/`
and `tests/` spellings below identify the evaluated versions, not active recipes.
Relocation does not establish source-version equivalence or product installation.

`host/gt3_clean_steering.{hpp,cpp}` separates readable, typed state transformations
from a small CPU/guest-memory bridge. `Command`, `InputPartial` and `CarPartial`
have explicit opaque padding and `offsetof`/size assertions. Guest objects are
copied with `memcpy`; only evidenced vehicle fields are stored back. Padding is
not invented into a full car definition. Guest addresses and floating bit patterns
remain 32-bit values, not host pointers or host floating arithmetic.

The implementation uses existing `ps2::fp` EE arithmetic and comparison ordering,
not reassociated host expressions. The differential checks require **exact bits**
and exact instruction-budget consumption, stronger than the unchanged trace
suite's `2e-6` tolerance. `Cost` counts the original dynamic instruction paths,
including skipped helper calls; it prevents an apparently equivalent rewrite from
silently changing guest timing. It does not execute a shadow generated routine in
the enabled game. The original implementation is executed independently by tests
and separate live oracle runs.

Preserved peculiarities include:

- channel/raw-byte masking, half-axis curves, pressure saturation, signed DIV1;
  zero sensitivity emits the original runtime BREAK diagnostic then returns `-1`
  for the nonnegative numerator (the existing runtime logs BREAK rather than
  stopping). The older standalone helper's throwing contract is unchanged;
- wheel types **1–3 only**, bank 0 versus 16, 32-bit wrapping before signed clamping,
  steering overwriting a preceding pad command even at center;
- digital writes clearing analog flags, nonpositive pedals leaving preceding
  commands intact, and the shift byte being assigned even for a zero mask;
- signed wheel policy, policy-dependent envelope floors and widening, mechanical
  clamping, history updates, invalid-policy steering zero, and mode-4 leaving
  stick rate unchanged;
- centered pad input preserving steering-kind state, invalid modes retaining the
  previous steering, asymmetric return filtering, crossing reset, EE special
  bit-pattern handling and ratio-division invalid flags.

`+13A4` is named `unknown13a4`: its assignment to `1.0` is evidenced, its larger
purpose is not. The average of `+105C/+1100`, classification meanings, policy
names, unused layout bytes, and all curve calibration semantics remain partly
unresolved. No branded-wheel or physical-PS2 equivalence claim is made.

## Static evidence provenance

No new decompiler output is claimed. The boundary was checked against the retained
REA evidence and the original generated EE paths in `unit_0039.cpp`,
`unit_0044.cpp`, and `unit_004B.cpp`:

- controls evidence (private artifact `gt3-controls-evidence.json`):
  `ev_ddfbe374f8896acd31e66f958a765e27afde3edc8568e55ec7e1111f5d59269f`
  (`00210F90`, including assembly).
- steering evidence (private artifact `gt3-steering-evidence.json`):
  `ev_67389fdd72969c49440306f79a8c71a31fd08d161d23fc51c862ac51beea078f`
  (`001E4368`) and
  `ev_4827844f7d8db4d5eae4302c47de04a2f2d0a72fee6ddfa4856e821bf4004958`
  (`001E4478`).
- wheel evidence (private artifact `gt3-wheel-evidence.json`):
  `ev_0c1f4be70fd4e5794a059276b8aa8d6fd1ff32f9ff8cd823afc9ba8e2c306c4c`,
  `ev_ab529eae84b77c8495bdcd745a9d14a640718910b26e4fb2b412c53fcb9a4de3`,
  `ev_6d791be32090b211f598a7fffe668ef1f0ecc94bf2dcef2f48ac3bf69e712a44`,
  `ev_bd75205028a72307c6662fe769c9a5cb673340ce549400fac86ff1b2139eb2dc`
  (builder, digital helper, pedals, signed policy, slew, full vehicle routine).

See also [pad trace](gt3-steering-trace.md) and [wheel trace](gt3-wheel-steering-trace.md).
Static evidence, generated fixtures and running-game observations are distinct.

## Historical isolated installation and reproduction {#isolated-installation-and-reproduction}

The bespoke builders/launchers in this recipe are retired. Keep the recipe in
its original context; changing paths would not make it current. Maintained
commands are in [workflow](../workflow.md) and [testing](../testing.md): public
`just check`, `just test`, `just docs-build`; historical baseline verification is
`just verify-historical baseline "$PWD"`, not current product qualification.

CMake `PS2_GT3_CLEAN_STEERING` defaults **OFF**. The isolated build also enables the
independent synthetic infrastructure for its guards/probes; synthetic **injection**
still requires its own CLI flags. Runtime clean substitution additionally requires
`--gt3-clean-steering`; without it the generated oracle executes unchanged.

```bash
scripts/build_gt3_clean_steering.sh
tests/run_gt3_clean_steering.sh
scripts/play_gt3_clean_steering.sh                 # normal pad input, clean processing
scripts/play_gt3_clean_steering.sh --gt3-wheel +0.5
scripts/validate_gt3_clean_steering.py \
  --snapshot $GT3_LEGACY_ROOT/validation/race-start.state \
  --out "$PWD/build/clean-steering/my-new-live-run"
```

The build copies the **existing completed synthetic generated oracle** into
`build/clean-steering/generated/`, then inserts four gates before original labels.
Original bodies remain present. Direct generated calls are intercepted at their
labels, not through a dispatch-table replacement that those calls would bypass.
The partial vehicle gate jumps to `001E48FC`; complete-function gates return to
the caller. No original generated file is edited. Unsupported vtables, guest
addresses or classification/table indices fall back to generated execution.
ELF hashes and preserved artifacts are checked by the build, with additional
instruction/vtable guards before boot and after snapshot load. Do not point an
unrelated generated profile at this experiment.

The launcher uses a fresh disposable card. The live validator requires a new
output directory, uses fresh cards per run, reuses the unchanged synthetic
validator, and adds clean pad and preserved-executable oracle comparisons.

## Generated-EE differential and regression results

Final log: `build/clean-steering/evidence/regressions-final.log`.

| New exact differential test | Cases |
|---|---:|
| Mapped normalization, signed/zero sensitivity and raw high bits | 28,160 |
| Wheel builder, all types/banks, random digital/command/32-bit channel state | 16,384 |
| Stick filter, rates/dt/targets including signed zero, subnormals, huge values, infinity/NaN patterns | 16,000 |
| Steering envelope through full original vehicle tail, all 256 modes, signed policies and three classifications | 20,000 |

The vehicle comparisons cover **all `0x1800` fixture car bytes**, including status,
history, rate, limits, ratio, opaque padding and original pedal-tail mutations.
Wheel comparisons cover all 16 command bytes. Every comparison checks return PC,
SP, callee-saved GPRs and exact budget. They do not claim arbitrary caller-saved
register/FPU scratch equivalence. Wheel policies and modes vary independently.
Clean-enabled existing wheel fixtures additionally pass **19,468 commands** and
**7,560 driving frames**, retaining the original `2e-6` tolerance.

Unchanged controls/mapping, pad/wheel traces, anisotropic GPU, GT3 hardware/runtime
and synthetic adapter tests also pass: **25,600**, **57,344**, **15,360**, **19,468**,
**7,560**, and synthetic **8,193 quantizations / 42 integrations**, respectively.
The pre-change regression log is retained separately.

## Actual running-game result

Authoritative evidence: `build/clean-steering/live-final/summary.json` and per-case
JSONL, logs, EE/IOP/SPU dumps, PPM captures and generated-oracle subdirectories.
Executable SHA-256:
`f42be9562a0201e5d7c1618e05ca0c500bed3a80cd654ef8c2329763be3234c3`.
The race-start snapshot resumes at frame 4801; its preserved SHA-256 is
`154077352bb0b738fa65fe52ce878d1bf378e43805a285ee84c4b77e3a62af07`.

- All seven synthetic values, `+.5 → 0 → -.5`, and two accelerated opposite-sign
  cases pass through clean builder/envelope, `car +13A0`, original wheel-angle
  processing and original simulation: **3,400 clean mode-4 updates**, **13,600
  original individual-wheel consumer calls**. Maximum reconstruction error is
  **5.96046448e-8**, without weakening the existing tolerance.
- Each wheel case was repeated with the preserved generated executable and
  identical settings. Per-frame semantic JSONL, every rendered capture, final
  vehicle bytes, and **the entire final EE/IOP/SPU dump matched byte-for-byte**.
- Scheduled live pad throttle/left steering executes **200 clean filters/envelopes**,
  **800 normalizations**, and **200 wheel-builder calls** (inactive wheel type).
  Its semantic trace, captures, vehicle bytes and full dump exactly match gates-off.
- Gates-off and trace-only experimental runs match the preserved baseline in all
  captures and full RAM. Baseline/disabled/pad dump SHA-256 is
  `88cece47260e159b53edd9d4b0204f266f95a06720fd5c71a7620525171221b4`.
- Reviewed accelerated frame-5700 captures: positive turns toward the inside wall,
  negative toward the opposite side; displayed speeds are 45/61. These runs use
  actual native WebGPU rendering and headless readback at 1280×240, not new desktop
  presentation or physical scanout validation. No window/60-FPS/audio claim is added.

In clean runs, mode-4 and steering seam records are **bridge observations of clean
execution**, not proof that the skipped generated instructions executed. The
independent unchanged synthetic observer is fed the computed limits and state at
its existing semantic seams. Original downstream consumer probes actually execute.
Clean-call counters independently establish substitution occurred. The earlier
`live-first` directory predates the separate live generated-oracle repetitions;
use **`live-final`**.

## Separate initialization repetition

A later historical initialization check repeated the unchanged four boundaries
in an isolated host, independently of the experiment's `live-final` population
above. Its evidence was **`build/project-init/live/summary.json`**, not the later
[native-v3 baseline](../current-baseline.md) evidence tree. Do not sum these
repetitions into a new coverage claim.

The unchanged suite again recorded **28,160** normalizations, **16,384** wheel
builders, **16,000** filters and **20,000** envelope/full-original-tail cases.
Relevant bytes, return PC/SP, callee-saved state and dynamic budget matched.
The live repetition recorded **3,400 clean mode-4 updates / 13,600 original
consumers**, maximum reconstruction error **5.96046448e-8**, tolerance **2e-6**.
Seven values, `+.5 → 0 → -.5`, two accelerated race continuations and a clean pad
path were repeated independently against the preserved original executable.
Per-frame semantic traces, captures, final car and complete EE/IOP/SPU dumps
matched; gates-off and trace-only remained byte-identical to baseline.

The fresh isolated foundation clean executable's SHA-256 was
**`f42be9562a0201e5d7c1618e05ca0c500bed3a80cd654ef8c2329763be3234c3`**,
matching the frozen clean executable. Original and synthetic executables were not
rebuilt in place. This used native offscreen WebGPU readback, one race snapshot
and bounded continuations—not new desktop/audio, physical-device, all-car/mode
or physical-PS2 proof. “Accelerated” denotes ordinary native race continuation,
not a faster-than-real-time stepping API.

Initialization retained the same guards: build **and** runtime opt-in, independent
synthetic injection opt-in, unsupported vtable/adjustment/RAM/classification fallback
and gates on copied bodies rather than protected generated outputs. Partial views
retain explicit padding, `memcpy`, offset assertions, EE bit-pattern arithmetic,
wrapping and exact dynamic cost. Neither this repetition nor subsequent bounded
source proof authorizes current product integration.

## Preservation, limits and stopping point

Original/triple ELF, original ISO, existing saves, baseline runner/default launcher,
completed synthetic build/evidence, rendering/window configuration, desktop,
streaming settings and packages were not changed. Retained preservation manifest:
`build/clean-steering/preservation-before.sha256`. Existing unrelated dirty changes
were preserved; no commits were made.

This is one GT3 v1.10 profile and a deterministic short race continuation, not an
all-game-mode/full-track audit or a general guest ABI replacement framework.
Non-shipped vtables remain generated. Physical report calibration, SDL wheels,
pedals/shifter/clutch support and force feedback remain outside scope.

The next natural boundary, **if explicitly requested**, is the retained steering
prefix (`001E4478–001E45A7`), its curve descriptors and original interpolation
`001D8FB8`; alternatively the already traced pad command producer `00210E68`.
Neither requires touching downstream wheel physics. **Stop here.**
