---
title: "Historical: gt3-synthetic-wheel-experiment"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


> Preserved experiment narrative, not validation of current main. Commands refer to the historical runtime. Raw exports and game artifacts are private.

# Opt-in synthetic host wheel integration — GT3 USA v1.10

**Result: demonstrated in the running native game.** A host value of `+0.5`
reaches the original wheel-command builder, selects mode 4, changes the live
steering float, reaches the original individual-wheel-angle routines, and
visibly turns the car in a race. Negative input turns the opposite way;
centering produces zero steering. This is an integration experiment, not
physical-wheel support.

## Historical isolation and launch {#isolation-and-launch}

The independent adapter was not redesigned around the clean steering API during
initialization. Its current locator is
`src/gt3/gameplay/controls/gt3_synthetic_wheel.{hpp,cpp}`, mapped from historical
`host/gt3_synthetic_wheel.*` by `project/gt3/migration-map.json`; the focused fixture
is now `validation/gt3/differential/gt3_synthetic_wheel_test.cpp`. These locators do
not replace the exact historical versions or imply current product installation.

The bespoke build/run/validate scripts below are retired historical recipes.
For maintained commands use [workflow](../workflow.md) and
[testing](../testing.md): `just check`, `just test`, `just docs-build`, or explicit
`just verify-historical baseline "$PWD"` for retained historical baseline proof.
Neither a clean-enabled validation build nor the current source build implicitly
enables synthetic injection.

The preserved `build/resolution-triple/ps2run`, original/triple ELFs, original
ISO, existing saves, and default `resolution/play-gt3-triple.sh` are not
modified. No renderer, desktop/display mode, streaming configuration or system
package changes were made. Build outputs and generated probes are confined to
`build/synthetic-wheel/`. CMake option **`PS2_GT3_SYNTHETIC_WHEEL` defaults OFF**;
the host adapter is compiled only in this experimental build.

```bash
# From resolution/repo:
scripts/build_gt3_synthetic_wheel.sh

# Explicit opt-in interactive launcher, always with a disposable memory card:
scripts/play_gt3_synthetic_wheel.sh --gt3-wheel +0.5

# Known race continuation; steering stays centered until guest frame 5600:
scripts/play_gt3_synthetic_wheel.sh \
  --load-state $GT3_LEGACY_ROOT/validation/race-start.state \
  --press 4801:cross:2000 --gt3-wheel 0 --gt3-wheel-at 5600:+0.5 --frames 5701

# Regression suite plus focused adapter tests:
tests/run_gt3_synthetic_wheel.sh

# Full-game, rendered validation with new output directory (never overwrite):
scripts/validate_gt3_synthetic_wheel.py \
  --snapshot $GT3_LEGACY_ROOT/validation/race-start.state \
  --out "$PWD/build/synthetic-wheel/my-live-run" --window
```

The interactive launcher opens an ordinary window; it does not change desktop
modes. `--gt3-wheel-at FRAME:VALUE` events use **absolute guest frames**, must
be strictly increasing, and hold their value until the next event. With no
initial value, scheduled-wheel mode starts centered. `--gt3-wheel-trace NEWFILE`
adds JSONL observations; used alone, it is **read-only**. Trace files are
**exclusive-created**: an existing output is not overwritten. Neither injection nor
tracing is installed when both are absent. These switches are unavailable in
a normal build. The dedicated build recipe is required: it generates the
matching probe profile and checks the original/triple ELF SHA-256s.

## Chosen seam and conversion

Inspection of the generated runtime ruled out a dispatch hook: generated
routines often call each other directly, bypassing `ps2::dispatch`. Existing
recompiler instruction probes support the required seam without modifying
guest instructions or replacing any routine.

**Injection is at `0x002107AC`**, after `0x00211430` has built the pad command
and immediately before its ordinary call to **`0x002115F8`**. Registers s0/s1
hold input/command pointers there. The host adapter:

1. Scopes the call to the manual live-driving context observed at `0x001E4D38`,
   checks `car +0x0C` matches the input object and checks the expected vtable.
   Context is cleared at `0x001E4D5C`; menus/AI/stale contexts are not injected.
2. Temporarily sets wheel type 1 in input `+0x14`, preserving its pad bits.
3. Temporarily supplies wheel axis and released-pedal words in channels
   16/17/18 when pad bits are present, or 0/1/2 otherwise.
4. Temporarily zeroes the combined digital mask: pad actions were already
   built, and repeating the digital helper would overwrite their analog flags.
5. Allows the **original `0x002115F8`** to produce steering, analog flag 1,
   and mode 4 through the shipped virtual getter.
6. At `0x002107B8`, restores all five modified input words and the command's
   shift byte (the wheel digital helper always writes that byte). No host
   command steering or car-angle write is performed. Nonsteering command
   fields and flags retain the already-built pad values.

The normalized host input is a finite `double` in **[-1,+1]**, rejected rather
than clamped outside that domain. Positive means a **positive GT3 steering
command** (observed toward the left side in this particular race). Ordinary
values map to `axis = 512 - round(value * 4096 / 9)`; endpoints map to 0/1023
so GT3's own clamp reaches exact full steering. The original conversion is
still `clamp((512-axis)*9, -4096, +4096)`:

| Host value | Synthetic axis | Original command | Effective normalized command |
|---:|---:|---:|---:|
| -1 | 1023 | -4096 | -1 |
| -0.5 | 740 | -2052 | -0.5009765625 |
| -0.25 | 626 | -1026 | -0.25048828125 |
| 0 | 512 | 0 | 0 |
| +0.25 | 398 | +1026 | +0.25048828125 |
| +0.5 | 284 | +2052 | +0.5009765625 |
| +1 | 0 | +4096 | +1 |

Quantization error is at most 4.5/4096. This synthetic channel domain is a design
choice, **not** a newly established physical USB report range.

### Original processing retained

The experiment bypasses USB device polling, `0x00230D10`, and wheel-state
composition `0x0022FFE8`: its temporary overlay stands in for their output.
It deliberately does **not** bypass:

```text
0x002115F8 and its native virtual channel getter
 -> command storage/normal manual caller chain, including any original hook
 -> 0x001E4478 (original mode-4 curve, envelope, policy and limit slewing)
 -> car +0x13A0
 -> 0x001E8978 / 0x001E8910
 -> per-wheel angles
 -> 0x001E7328 and existing vehicle simulation
```

No car policy at `+0x136F`, limit, time step or steering angle is patched.
This preserves the recovered wheel behavior rather than approximating it with
a host-written final angle. Enabled mode 4 also retains GT3's original mode-4
pedal processing of the existing pad command; no synthetic pedals are added.

## Live evidence (not fixtures)

Final run: **`build/synthetic-wheel/live-final/summary.json`**, per-case
`trace.jsonl`, `run.log`, rendered PPM captures and RAM dumps. The validator
actually launches the full native game, loads an existing race snapshot
read-only, resumes the Super Speedway race, and uses scheduled pad throttle.
Snapshot SHA-256: `154077352bb0b738fa65fe52ce878d1bf378e43805a285ee84c4b77e3a62af07`.

- All seven requested deterministic values: **200 live race updates each**.
- `+0.5 -> 0 -> -0.5` transition: another **200** updates.
- Two accelerated race continuations: **900** updates each, centered until
  frame 5599, then opposite-sign steering at frame 5600.
- Total: **3,400** observed mode-4 updates and **13,600** calls consuming the
  steering float in `0x001E8910`.

At live car address **`0x01FBB7BC`** (numeric address **33273788**), the first
`+0.5` update at frame 4801 produced:

```text
host +0.5 -> channel axis 284 -> original command +2052, mode 4, flags 31
policy at car +0x136F = 0 (observed, not overridden)
limits = +0.698131680 / -0.698131680 radians
car +0x13A0 = +0.349747598 radians
front wheel angles = +0.418321341 / +0.297245741 radians
```

The exclusive wheel branch is observed at **`0x001E471C`**, after the mode
comparison at `0x001E470C`. The original write is observed at `0x001E48A0`.
Each steering result is compared to the recovered policy/limit-slew calculation
using **live prior limits, native envelope targets and dt**. The limit update
and unchanged filter-rate value are checked too. Each `0x001E8910` input is
compared to `car +0x13A0`, and all four stored angles are checked at the
`0x001E7328` consumer. Maximum combined reconstruction error across the final
runs: **5.96046448e-8**, below the existing 2e-6 tolerance.

The transition returned steering to **exactly zero at frame 4881**, and to
negative steering at 4941. Centering changes the steering angle, not the car's
already accumulated heading or lateral velocity.

At speed, frame 5600 produced **±0.0748132691 radians** from ±0.5, rather than
±0.3497: GT3's live envelope had decreased to ±0.149334878. This confirms that
the original vehicle-dependent processing remains relevant. At frame 5700,
positive input had turned the view toward the left wall; negative input had
turned toward the right-side lane/car. Reviewed captures:

- `live-final/moving_positive/frame_05700.png` (speedometer reads 45)
- `live-final/moving_negative/frame_05700.png` (speedometer reads 61)

Four cases were also presented through actual native WebGPU/Wayland windows.
Requested capture size was 1280×240; window drawable was 1129×240. No claim of
full-size scanout, sustained 60 FPS or real-audio validation is made.

**Disabled preservation:** baseline, experimental-with-no-switches, and
read-only-trace runs used the same race snapshot and `cross+left` pad input.
All final EE/IOP/SPU RAM dumps and every rendered capture were **byte-identical**.
Trace-only observed pad mode 3 and nonzero steering, with **no exclusive mode-4
branch hits**. RAM SHA-256 for all three:
`88cece47260e159b53edd9d4b0204f266f95a06720fd5c71a7620525171221b4`.

An initial observer placed at the shared mode comparison incorrectly counted
pad calls as wheel-branch hits. The disabled-mode assertion caught this; the
observer was moved to the exclusive body at `0x001E471C`. No behavioral code
or assertions were weakened. All final runs above use the corrected observer.

## Automated tests and evidence boundaries

Final regression log: **`build/synthetic-wheel/regressions-verified.log`**.
Existing assertions unchanged:

- Control normalization **25,600**, mapped actions **57,344** cases.
- Stick trace **15,360** frames.
- Wheel commands **19,468** cases; wheel driving **7,560** frames.
- Anisotropic GPU and GT3 hardware/runtime regressions: PASS.
- New adapter: **8,193** quantization values, **42** generated-EE integration
  cases, full input restoration, nonsteering command preservation, disabled/
  AI/stale-context/vtable guards, invalid profile/parser checks and scheduling.

**Static evidence:** [stick trace](gt3-steering-trace.md),
[wheel trace](gt3-wheel-steering-trace.md) and their retained REA JSON establish
the original path and numerical behavior. Generated code inspection establishes
the probe/register seam; no new binary-semantic hypothesis is required.
**Fixture evidence:** the regression counts above execute generated EE routines
with original data and synthetic objects.
**Live evidence:** separate full-game processes, dynamic game-owned objects,
exclusive branch observations, numeric consumers, rendered races and baseline
comparisons establish actual integration.

Initialization separately retained **8,193 quantizations / 42 generated
integrations**, parser/profile/scope/restoration/scheduling guards and the adapter's
own CLI/probes. The earlier independent live evidence remained
`build/synthetic-wheel/live-final/summary.json`; the preserved original executable
was the independent oracle for the separate clean-steering repetitions. These
counts are repetitions of the adapter checks, not additional live coverage.

Limitations: GT3 v1.10/profile-specific, one manual-player race snapshot, short
continuations, no physical input device, no full-track test, no USB enumeration,
no physical-PS2 numeric equivalence. The optional original command hook remains
in the path; its preservation of injected steering was observed here, not
claimed for every game mode. Traces and scheduled input are experiment-local,
not serialized host configuration for general save/load support. There is no
pedal/shifter/clutch/force-feedback integration. **Stop condition met; no further
wheel features implemented.**
