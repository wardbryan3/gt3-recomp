> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Prioritized queue and precise next-cycle proposal
---

**Stop now.** This queue is a proposal, not authorization to execute it automatically.

```mermaid
flowchart TD
  A[0 - Frozen clean baseline and immutable evidence] --> B[1a - Audit pedal handoff and response helper]
  B --> C[1b - Recover bounded accelerator / brake tail]
  C --> D[1c - Exact differential / guarded runtime / live]
  D --> E[2 - Transmission / clutch / handbrake contracts]
  A --> F[3 - Original output / FFB producer-to-device trace]
  E --> G[4 - Physical report calibration and host adapter - future]
  F --> H[5 - Original-intent FFB integration - future]
  G --> I[Checkpoint 1 acceptance]
  H --> I
  A --> J[6 - Presentation / audio pacing measurements]
  J --> I
  I --> K[7 - Telemetry / race / reset / step contract proof]
  K --> L[Checkpoint 2 implementation - separately authorized]
```

## Pedal Recovery v1 audit outcome

The explicitly requested [v1 audit](pedal-recovery-v1.md) stopped before
implementation. A subsequent [native-baseline task](current-baseline.md) restored
tools, fresh regressions, a normal-boot v3 race fixture and isolated current-main
steering/synthetic live proof. No pedal boundary expansion or lifecycle promotion
followed. **Stop at that baseline**; a separate request is needed to resume the
pedal contract/differential work below, not an adjacent subsystem.

## Proposed next cycle: pedal semantics only

**Need:** recover the original accelerator/brake contract before any physical-pedal adapter. Steering is already sufficient and frozen. No new device features required.

**Exact candidate target:** interior **`001E48FC–001E4BA7`** of `001E4478`, resume **`001E4BA8`**. Audit all branch/delay-slot paths and outgoing register state before installation; if a complete contract cannot be shown, stop instead of widening the target. No replacement tonight.

**In scope:** accelerator/auxiliary arbitration required by this region, digital slewing, analog nonzero floor, mode4 response evaluation, prior control-state bytes, writes to car+13AC/+13B0 and control-state +0/+2, exact dynamic EE cost, relevant FPU state, `v0 = uint16(car+14BA)` at resume, and the computed policy in `s1` for the later `001E4180` call. Represent unknown policy values neutrally. The original prefix supplies control kind/context; do not infer human-facing mode labels from numeric values.

**Dependencies to audit first:**

1. Original assembly/generated instructions, retained REA record `ev_1ae7e5b58f8018c49aa9ed4a976e3984f3dda1001e36148fc94cff18145abd71`.
2. Descriptor helper **`001D92E0`** and live descriptor data **0049D060/70**; determine EE behavior for identity, quadratic, square-root, negative inputs, NaN-like/denormal/invalid states and optional derivative writes. Either keep its calls original in the bridge, or obtain explicit approval for a separately bounded standalone reconstruction. Do not silently replace a general math routine.
3. Tables/constants **002D4930/34/38/3C**, **00352990**, policy bytes +136D/+13E5 and suppression +14B8/+14BA, command flags 2/4/8, unsigned accelerator/auxiliary representation versus signed brake.
4. Typed **partial** pedal state with padding and every used offset asserted; observations currently lie inside steering padding and authorize no writes.
5. Resume ABI/budget: generated tail expects suppression value in `v0` and policy in `s1`; preserve shift/handbrake/coupling/epilogue and every other genuinely consumed outgoing value. Exact cost must account for original helper calls, branch/delay-slot choices and any bridge observation seams.

**Differential matrix before any integration:** zero/released/low/full pressure; boundary raw47/48,52/53,174/175,179/180; bank0/16, wheel types0–7; combined pad/wheel released-command persistence; flags2/4/8; command halfword extremes and wrapping; all observed policy values including0/1/2/3/5/6 and unsupported persistence; prior accelerator/brake and state bytes; digital rise/fall/clamps across frames; identity/quadratic/sqrt descriptors and signed/zero/invalid EE numeric inputs; suppression counters and analog-zero special behavior. Compare relevant memory, neighboring padding, control-state bytes, PC/SP, callee-saved state, FPU flags and exact budget. Use the original generated whole routine/tail as independent oracle, not a shared helper expectation.

**Integration only after pass:** separate copied generated build, build+runtime default-OFF opt-ins, profile/address/layout guards, fallback to generated outside evidence. Preserve original steering gates and synthetic adapter independently. Add explicit substitution counters for the new region, not just output observations.

**Live acceptance:** new evidence directory/disposable cards, identity-pinned snapshot, original versus clean runs with existing pad throttle/brake sequences (press, release, alternating and combined), enough state observation to distinguish pre-helper versus post-helper brake, car+1428 and unchanged engine/wheel consumers. Compare semantic traces, every capture, final car and complete dumps; disabled and trace-only must remain baseline-identical. Do not add synthetic pedals or physical polling to make validation easier. Preserve existing **2e-6** tolerance; do not weaken assertions or existing digital/analog tests.

**Excluded:** shift dispatch `001E4BA8`, handbrake `001E4BB8–001E4C5F`, coupling helper `001E4180`, wrapper/engine/torque/axle consumers, physical wheel/pedal/shifter/clutch/FFB, AI/reset/step/performance/renderer changes. Missing live calibration is a discovery task, not permission to tune curves.

**Stop gate:** bounded evidence+tests+guarded live validation documented, manifests updated, handoff written; or stop earlier with explicit unknowns if contract/ABI proof is incomplete. No automatic next subsystem.

## Following discovery cycles

- Transmission first: command shift → control-state → ratio/state/coupling, automatic/manual/neutral/reverse intent, then handbrake interactions.
- Output-side original FFB trace runs independently of input math; verify virtual targets and packet transport before host mapping.
- Physical hardware calibration/integration and pacing/audio acceptance remain later separately authorized Checkpoint1 work.
- Checkpoint2 telemetry/race/reset/step proof stays low priority until Checkpoint1 contracts and operation are stable.
