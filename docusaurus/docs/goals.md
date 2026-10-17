---
title: Goals and project contract
---

## Six months, three milestones

The six-month project objective is unchanged. Restructuring provides ownership and
repeatable evidence; it is not completion of any milestone.

1. **Reliable GT3 on an actual racing simulator.** Physical wheel/pedals/clutch/
   H-pattern shifter, recovered original-intent FFB, triple-screen presentation,
   pacing/performance and synchronized audio. Validate both original-equivalent
   defaults and a separately named enhanced simulator configuration. Software
   input injection, virtual disconnects and streamed windows are not hardware proof.
2. **Correct headless AI training.** Shared authoritative gameplay, build settings
   and numerical contracts with playable execution; no easier/faster training
   physics fork. Explicit reset/step, observations, reproducibility and versioned
   replay qualification must be implemented and validated separately.
3. **Complete playable native GT3 without PS2 execution/translation machinery.**
   Full playable behavior must ultimately no longer require EE/VU execution,
   generated translations or PS2 compatibility runtime. Legally supplied ISO assets
   are still required. A native host around generated code is not this milestone.

Correctness comes before acceleration; transitional original PS2 execution is
permitted. Selective recovery follows concrete milestone dependencies, not a plan
to decompile every routine before useful play.

## Acceptance boundaries and unresolved contracts

Simulator acceptance requires actual device calibration and reports: wheel/pedal
ranges, enumeration/device matching, clutch and shifter intent and original output
transport. Software injection is useful bounded
contract evidence, not physical calibration. Original output bytes may mix wheel
effects with pad vibration; biased byte encoding alone does not establish torque
units or certify FFB. Test real three-monitor scanout, pacing/latency and audible,
underrun-free synchronized audio rather than inferring them from virtual windows
or captures. Long-session and car/mode coverage need explicit qualification too.

AI acceptance requires trustworthy telemetry units, coordinate frames, ownership,
lifetime and atomic sampling, plus proven lap/finish/failure transitions. Candidate
field names and UI labels are investigation seeds, not APIs; the broad vehicle
post-update candidate `001EB218` is not a proven lap-count routine. Snapshot
continuation does not establish a complete deterministic reset of host/runtime,
input/audio/render state. Frame counting does not establish physics-tick boundaries,
a resumable atomic step or faster-than-real-time correctness. Replay/reset/step
must prove those contracts before training can rely on them.

These are acceptance requirements and limits, not a duplicate recovery-status
inventory. Consult [current products](registry/current-products.md) for integration,
[testing](testing.md) for evidence classes, and the existing
[telemetry](telemetry.md) and [reset/step](reset-step.md) reports for bounded findings.
New probes, device adapters and headless interfaces require scoped authorization;
no framework or API is implied by these milestones.

## Four classifications, not four copies

| Class | Contract |
|---|---|
| Original | Original executable-derived execution; permanent reference |
| Recovered | Readable original-equivalent behavior within an explicit proven scope |
| Modernized | Separately approved native timing/ordering/outcome and numerical contract |
| Enhanced / Extended | Deliberate extra or changed behavior, explicitly activated and inactive-neutral |

Classification does not require another backend, directory or duplicate maintained
implementation. Recover first, modify second. A modernization may remove guest
accounting only under its approved contract; small numerical differences require
stateful race evidence, not just one-call tolerance. Preserve the existing `2e-6`
contract unless a separate approved component contract says otherwise.

## Products and promotion

`ps2run` is the permanent enhancement-free generated reference. It can receive
reviewed runtime/recompiler/platform updates with qualified identities and evidence.
`gt3-native` evolves toward the playable native product and eventual default.
Initially both use original generated execution; no readable recovery is installed.

Enhancements may eventually be compiled into the native product, but require
explicit activation and must be neutral when inactive. The current validation-only
virtual-transmission build/runtime gates remain OFF; restructuring does not install
that extension or authorize composition with clean transmission.

Implementation proof is distinct from product approval. A promoted scope cannot
silently call its superseded original. Temporary fallback must be explicit,
observable, tested and have an exit criterion; eventually retire its execution and
link inputs without sacrificing normal coverage. Current non-integrated libraries
are not an excuse for a second actively maintained gameplay implementation.

Replay is version/configuration/numerical-contract qualified; incompatible versions
may reject. Its format is undecided. No headless, device, reset/step, FFB, recovery
promotion or enhancement integration is authorized by repository restructuring.
