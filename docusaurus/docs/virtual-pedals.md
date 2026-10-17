---
title: Synthetic / Virtual Pedal Controller v1
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


## Bounded result

Deterministic virtual throttle and brake are **validated end-to-end in an isolated
native USA v1.10 harness**. This is a separate experiment, not a pedal replacement,
physical pedal driver or general DriverInput architecture. Both build and runtime
gates default **OFF**. Canonical `ps2run` is unmodified and retains its baseline
executable hash. Frozen pedal/closure, steering and synthetic-wheel source and
existing assertions remain unchanged; no Frozen authority is promoted or rewritten.

Authority: [`virtual-pedals.json`](pathname:///knowledge/virtual-pedals.json),
[generated status](registry/virtual-pedals.md). Original evidence, linked executables,
states, captures and raw traces remain private under `local/virtual-pedals-v1/`.

## Exact virtual protocol, not calibration

Each input is a finite normalized **binary64 value in `[0,1]`**. The adapter maps
it to `Q = round(value × 4096)`, nearest integer with positive half ties **up**:

| Host request | GT3 command halfword |
|---|---|
| 0 | 0 |
| 0.25 | 1024 |
| 0.5 | 2048 |
| 1 | 4096 |

The request sets only command analog flags **2 and 4**, writes throttle at **+8**
(unsigned halfword) and brake at **+10** (positive signed-halfword domain), preserving
all other flags, mode, steering, action and auxiliary fields. Original processing
interprets these analog values with a `1/4096` scale. The mapping deliberately
avoids assumptions about pad pressure, wheel ADCs, polarity, physical travel,
deadzones or any physical calibration.

**Processed values need not equal host values.** Original floor, zero/history
release, unsigned auxiliary arbitration and mode-4 response evaluation remain in
force. Native half requests in these fixtures produce the original floor-adjusted
result, not a substituted linear car state. Mode-4 compatibility follows its
original response path. Zero requests are not a promise to erase existing history
or force instantaneous processed throttle zero. The experiment never writes
processed accelerator/brake, effective accelerator, control history or car physics.

Input grammar is locale-independent unsigned decimal `DIGITS[.DIGITS]`, no signs,
whitespace, hex, exponent, NaN, infinity, suffixes or out-of-range values. Parsing
fails rather than clamping. Events use an unsigned decimal **uint64 guest frame**;
overflow, malformed pairs, duplicate frames and out-of-order events fail. Both
channels change atomically at a threshold; the last event with `frame <= current`
wins, otherwise the initial pair is held. Repeated queries in a frame are identical.
No wall-clock timing, interpolation, sorting ambiguity or history reconstruction.

## Why this seam

The original command producer `00210740` initializes and builds a 16-byte command
owned by `001E4D38`'s stack activation. **001E4D5C** is its return, before the optional
original hook, original command notification (`001E4290`), manual processing,
pedal region and original downstream consumers. Injecting here lets those original
stages see the requested commands; injecting only at the pedal region would miss
that upstream notification. No original input object or ADC channel is overwritten.

The experiment checks the original code fingerprints, aligned bounded owner-frame
relationship, saved owner registers, manual kind0 branch, command mode2/3/4 and
zero auxiliary command. It does not invent auxiliary/clutch/handbrake semantics.
Unexpected/nested scopes, changed command bytes, unsupported profiles/modes or
auxiliary requests fail the validation run, never force admission.

At **001E4E68**, before the owner frame unwinds, it verifies command lifetime and
restores precisely the original flag byte and two original pedal halfwords, then
checks all16 original command bytes. Original outputs to the car remain original
simulation results; restoration is of temporary input, not rollback of physics.
Trace-only and default-OFF do not write guest memory. This is an EE-thread-only,
known-profile experiment, not a security boundary for arbitrary forged states or
an exhaustive scene/thread/virtual-hook guarantee.

## CLI and isolation

```bash
# Existing verified generated pedal build; every output directory must be new.
bash scripts/build_gt3_virtual_pedals.sh VERIFIED_PEDAL_BUILD NEW_BUILD --enable-virtual-pedals

NEW_BUILD/virtual-on ORIGINAL_ELF --disc ORIGINAL_ISO --load-state NATIVE_V3_STATE \
  --gt3-virtual-pedals 0:0 \
  --gt3-virtual-pedals-at 4802:0.5:0 \
  --gt3-virtual-pedals-at 4900:1:0 \
  --gt3-virtual-pedals-at 5000:0:0.5 \
  --gt3-virtual-pedals-trace NEW_EXCLUSIVE_TRACE
```

Without `--enable-virtual-pedals`, the script builds only the gate-OFF executable.
An enable request in that binary exits2. Events require explicit runtime enable.
Trace files are exclusive-create; an existing trace is refused unchanged. Omitting
virtual enable/trace is inert. `--gt3-clean-pedals` separately requests the unchanged
Frozen pedal gate in an opt-in build; without it, processing remains generated.

The build reuses the existing **validation host source** through a disposable
wrapper, not a copied runtime checkout or edited canonical host. Wheel options
remain separate. A coexistence test explicitly enables the existing synthetic
wheel; the virtual pedals run after its scoped builder operation, preserving its
steering command/mode. No wheel algorithm, schedule grammar or calibration changes.

A snapshot is not a reset/step API. Thresholds refer to the runtime's actual guest
frame labels; old events simply select the current request at the next observed
command. Previously executed/sampled frames are not replayed or rewritten.

## Evidence layers

- **Static original evidence:** retained Ghidra r5900 records establish the command
  producer/owner, original notification and Q12 pedal interpretation. No raw
  pseudocode, instructions or original tables are published.
- **Game-free tests:** strict syntax/range/overflow/event ordering and **8,193**
  exact quantization/half-tie checks. Reducer negatives reject missing stages,
  changed steering, wrong schedules/commands/restoration and consumer mismatch.
- **Independent generated oracle:** **12,291 fixtures /24,582 full CPU+32MiB
  comparisons**, covering every Q12 code in throttle-only, brake-only and paired
  sweeps. An independent integer-command reference runs the original notification,
  manual wrapper and original brake/engine routines. Adapter-generated and
  adapter-Frozen paths match it, including all CPU/budget/stack/memory effects.
  Pre-injection full-RAM checks allow only the five command bytes, and restoration
  exercises nonzero original halfwords. Both observed stack positions and modes
  2/3/4 are included. Eight unsupported frame/profile/mode/auxiliary/nesting cases
  reject without CPU/RAM mutation; nonmanual contexts remain isolated.
- **Native-v3 live proof:** **40 runs**:12 cases with generated, Frozen-clean and
  repeated-generated execution, plus canonical/default/trace-only/build-OFF
  comparisons. Each active path has **3,599** injections/restorations, **10,797**
  total. Frozen-clean performs3,599 actual replacements with zero fallback.
  Exact CPU, complete guest dump, captures, steering traces and repeated execution
  match. Trace proves requested Q12 at the original pedal entry, exact preservation
  of non-pedal command fields, original command restoration and identical processed
  pedal values at the original brake and engine consumer entries.

Live cases include zero, half/full throttle, half/full brake, separate quarter/
half/full/release schedules, throttle-to-brake, simultaneous input, native left
stick, explicit existing-wheel compatibility and Time Trial's alternate stack
position. They are finite representative executions, not all cars/calibrations.
The steering isolation claim is unchanged command fields and exact generated/clean
parity for identical input—not identical vehicle trajectories with different pedals.

Fresh **unchanged** suites also pass:19-run original Pedal v1 live suite;28-run
normal-boot native-v3 baseline; all14 profile runs /4,199 substitutions; full native
regressions and public check/test/docs; strict historical/current/pedal/profile/
admission/closure and new experiment evidence verification. Canonical remains
byte-identical. Protected-source hashes include the Frozen authorities/modules,
canonical host and runtime/recompiler source.

The first live harness attempt failed on missing capture directories; no game
mismatch was hidden. Its STOP/log/source remain private. A combined shell timed
out after completed oracle/virtual/pedal suites while the baseline suite was still
running; that incomplete baseline is retained and excluded. The baseline was
rerun independently in a fresh accepted directory. No assertion was weakened.

```bash
just check
just test
just docs-build
just verify-virtual-pedals "$PWD"
```

The strict verifier fails on missing/changed evidence, recomputes trace/dump/
capture/CPU parity and scheduling/restoration relationships, checks original v3
input/binary identities and invokes the unchanged inherited evidence verifiers.
Public checks require no game artifacts and are not an independent game oracle.

## Stop

**Deterministic virtual throttle/brake is proven through the existing GT3 command,
pedal and original downstream vehicle path for this bounded experiment. Stop.**
No physical pedals, calibration, USB/HID, clutch, handbrake, transmission, coupling
recovery, FFB/hardware, general DriverInput, AI/reset/step or canonical integration
is implemented or authorized by this result. Existing unknowns remain unknown.
