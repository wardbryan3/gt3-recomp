---
title: Virtual Handbrake v1
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


# Virtual analog handbrake controller

**Validated bounded virtual input; all named gates pass.** Acceptance is the
separate [`virtual-handbrake.json`](registry/virtual-handbrake.md) authority, not
an inference from the earlier Frozen checkpoint. This is a new **virtual input
adapter**, not new handbrake behavior or a recovered adjacent function.

Source: `host/gt3_virtual_handbrake.{hpp,cpp}`. Both build and runtime gates default
**OFF**. Canonical `ps2run`, runtime/recompiler, all Frozen source/authorities and
prior proof-pinned CMake/justfiles remain byte-identical. No physical device,
calibration, generalized DriverInput, transmission, coupling, clutch or FFB API
is introduced. No generated game code, snapshots or captures are public.

## Protocol: input fraction, not a new force model

| Host value | Original analog command |
|---|---|
| 0 | flag0x10 present; signed halfword+14 =0 |
| 0.5 | flag0x10 present; halfword+14 =2048 |
| 1 | flag0x10 present; halfword+14 =4096 |

The API accepts **finite binary64 values in [0,1]**. Quantization is nearest
`value ×4096`, with positive exact half ties rounding up. Inputs just outside the
range, infinities and NaNs reject **before** quantization/guest access, even when
rounding would otherwise yield an endpoint. They are never clamped. API negative
zero is mathematical zero; the stricter unsigned-decimal CLI grammar rejects a
minus sign, including textual `-0`.

This exposes the complete4,097-code nonnegative Q12 representation. It is a
**virtual protocol**, not a claim that a native pressure channel has4,097 physical
positions. Very small valid inputs can quantize to zero. Original mapped action4
sets this same analog flag and writes the same halfword after its device-specific
normalization; that producer ordinarily has coarser channel resolution.

**Half input is not a new calibrated half-force guarantee.** GT3 retains its exact
EE zero bypass and nonzero floor arithmetic. Thus0.5 supplies Q2048 and GT3 applies
its existing floor, yielding approximately0.55 processed state under the observed
calibration. No inverse-floor compensation, host smoothing, rate limit, extra
brake effect or transmission policy is added. Endpoints still mean zero/full
handbrake. Original digital behavior/history remains available when this adapter
is disabled; the virtual source deliberately requests the **analog** path.

## Upstream integration and lifetime

Injection is at **001E4D5C**, immediately after original00210740 has finished
building the activation-local16-byte action command in001E4D38's64-byte frame.
This is before the owner's original indirect notification,001E4290, manual-input
wrapper001E4CB0 and original/Frozen handbrake processing001E4BB8. Original coupling,
shift-interface comparison, rear-brake preparation and engine processing remain
untouched/generated.

This is the earliest sensible **device-neutral, completed action-command** point
in that owner. Earlier physical channel storage is binding- and input-kind-
dependent, can be shared with other mapped actions, and is still subject to
multiple builder passes. Altering it would require a device/binding layer and
could modify unrelated controls. Injecting the processed car field or the
handbrake processor's interior would instead bypass upstream processing or its
normal notification. Neither is done.

The original command recording inside00210740 has already occurred. Consequently
this experiment does **not** add virtual-input replay recording/playback support
or change the codec/cache. That limitation is explicit, not a claim of complete
input-system recovery.

The adapter changes only **three possible command bytes**: OR0x10 into flags and
write the little-endian halfword+14. Every other flag and command byte—including
steering, accelerator, wheel brake, shift, mode and auxiliary bytes—is preserved.
Enabled virtual input takes explicit precedence over native handbrake for that
activation; it is not OR/max/add composition. A native Circle press during the
half-input live case confirms that distinction.

At **001E4E68**, before owner unwind/reuse, precisely those three bytes are
restored. The complete16-byte packet must match the saved original. Integrity is
also checked before processing and before restoration; unexpected mutation or
nested ownership fails the experiment rather than overwriting unknown changes.
No guest CPU/budget mutation belongs to injection/restoration, and **no processed
car state, calibration, pad channel or opaque padding is written by the adapter**.

Admission checks the original wrapper/builder/handbrake instruction fingerprints,
GP, full-width register identities, bounded high-RAM car, aligned structural
64-byte owner frame, and original owner policy selecting manual controls. The
term *manual controls* here means the player-input processing branch, **not MT
gearbox selection**: both AT and MT reach it. Neither model nor scene nor a single
absolute car/command address is an allowlist. Actual alternate-stack Time Trial,
Free Run and B-1 commands at0049AF40 are covered alongside0049AF50.

The source and exact evaluated overlay are pinned separately from the unchanged
[Frozen processor](handbrake-v1.md). Its guard/semantics/history/CPU/cost code was
not expanded or re-frozen by this work.

## Using the isolated native controller

The only installation is a newly compiled disposable unit/host overlay over the
verified Frozen build, not a copied runtime checkout or canonical-host hook:

```bash
bash scripts/build_gt3_virtual_handbrake.sh VERIFIED_HANDBRAKE_BUILD NEW_OUTPUT \
  --enable-virtual-handbrake

# Add to that validation host's normal original-ELF/disc/v3-state arguments:
NEW_OUTPUT/virtual-on ... --gt3-virtual-handbrake 0.5

# Piecewise-constant values at command-probe guest frames:
NEW_OUTPUT/virtual-on ... --gt3-virtual-handbrake 0 \
  --gt3-virtual-handbrake-at FRAME:0.25 \
  --gt3-virtual-handbrake-at LATER_FRAME:1 \
  --gt3-virtual-handbrake-at STILL_LATER_FRAME:0
```

Actual commands require the usual explicit game arguments; the ellipsis is not a
launcher. Add `--gt3-clean-handbrake` only to select the unchanged Frozen processor;
without it the same virtual input traverses the generated original. Optional
`--gt3-virtual-handbrake-trace PATH` and `--gt3-handbrake-trace PATH` record input
lifetime and original consumer/CPU observations. Trace files are exclusive, never
overwritten. Trace alone enables no virtual input.

CLI values are unsigned decimal digits with an optional nonempty fractional part;
no exponent, whitespace, sign or trailing junk. Frame schedules are strictly
increasing uint64 values; duplicates, disorder, overflow, invalid future values,
duplicate enable options and schedules without explicit enable reject before
running the game. No sorting or partial application of an invalid schedule.
Frame labels refer to the existing owner-command probe clock, not wall-clock
sampling or a claim about physical pad latency. Values hold until the next event.
There is no network/HID/asynchronous multi-thread controller API in this task.

## Independent original differential proof

Every tested valid binary64 input is exercised through a direct independently
encoded original packet, the virtual source + generated processor, and the same
virtual source + actual Frozen substitution. No expected value is calculated by
calling clean handbrake code.

For **each of two observed calibration bit patterns**,24,585 values cover:

- all4,097 Q12 centers, including both endpoints;
- all4,096 half-step boundaries and both adjacent binary64 neighbors;
-8,192 deterministic rational random inputs;
- eight extra decimal/precision/zero-edge values, including0.1,0.9,1/3, the smallest
  positive binary64, the predecessor of1 and API negative zero.

Total: **49,170 original oracle cases /98,340 complete final CPU+32MiB comparisons**,
393,360 original semantic-stage comparisons,590,040 original rear-only formula
assertions and49,170 actual Frozen substitutions. Source injection/restoration is
checked against full32MiB memory and complete CPU invariants. Four original stages
compare command, processed state, coupling candidate, wheel requests, CPU and exact
budget; only intermediate dispatch transport PC is replaced by the explicit
semantic probe PC. Final outgoing CPU comparison is entirely unnormalized.

The original notification/manual/coupling/brake/engine code executes in all three
paths. Steering/pedal commands, supported original policy combinations and eight
old-output patterns vary, including invalid/NaN-like history, which analog mode
must ignore. Each calibration also tests ten mutation-free unsupported-context
rejections, three ineligible owner kinds and seven invalid host values rejected
before any guest access. No existing2e-6 tolerance was relaxed; new comparisons
are **exact**.

## Native game evidence, not a single-fixture claim

**52 new runs:** four canonical/default/trace/build-OFF controls plus16
virtual-generated / virtual-Frozen / virtual-repeat triplets. **8,596 actual clean
substitutions**, zero fallback;25,788 injections and matching restorations across
the three active paths.

| Native contexts | What is established |
|---|---|
| Arcade Single Race, ALTEZZA AT and MT | Both transmission configurations; native acceleration/brake and MT shift-button context |
| Single Race, Alfa156 AT and MR-S AT | Other UI-identified car configurations |
| Arcade Time Trial / Mid-Field, MT | Different mode, unidentified preset model, alternate owner stack |
| Arcade Free Run, SLK230 Kompressor MT | Different car/mode and alternate owner stack |
| Simulation License B-1, New Beetle2.0 | Simulation/license path; preset transmission, no selected AT/MT claim |
| Native left-stick AT/MT, D-pad AT, existing wheel compatibility AT/MT | Unchanged surrounding input paths; Frozen steering compatibility, not physical wheel proof |
| Zero/half/full holds and exhaustive native sweep | Endpoints, partial application, native-handbrake precedence and all4,097 Q12 codes |

These are **seven distinct identity-pinned native-v3 states**, not relabeled copies
of one race. Car/mode/transmission labels follow retained, reviewed original UI
selection lineage; the exact Time Trial model remains unidentified. No v2 import
or header rewriting occurred. Each of the12 representative contexts crosses
0 →1/4096 →1/16 →1/4 →1/2 →3/4 →1 →1/2 →0. The longer sweep reaches every wire code
in successive native updates and repeats independently. No processed-state
injection or synthetic downstream result substitutes for actual game execution.

Generated/clean/repeat match complete guest EE/IOP/SPU dumps, captures, steering,
command lifetime and processed/coupling/rear-brake observations, plus every defined
serialized CPU field and budget at all nine original stages. Dispatch transport
`Cpu.pc` is retained separately; equality uses the explicit semantic probe PC,
exactly as in the established Frozen live methodology. All injected commands and
processed values are independently checked against generated-original results at
the **actual observed calibration**, and original shift-interface decisions remain
read-only observations, not recovered transmission logic. A12-capture private
montage was reviewed; no game imagery is published. In the half-input precedence
case,50 original native full-handbrake commands became Q2048 for processing, while
all300 original packets were restored exactly afterward.

## Failed and revised attempts retained

1. The initial native trio matched exactly, but its extra table check correctly
   stopped: ELF initial floor bits are **3DCCCCCD**, while initialized native
   states use **3DCCCCCC**. Retained original dumps and new native traces establish
   this difference. The initialization writer is not newly recovered. No live
   calibration or Frozen code was changed; new original oracle runs cover **both**
   values and reference tables are keyed by exact calibration and Q12 code. The
   stopped attempt is not accepted as the full live matrix.
2. One combined build/two-oracle tool group exceeded600 seconds after the first
   oracle passed. The second process left a partial table and no PASS log; those
   outputs remain retained and are not accepted. The entire unchanged second
   oracle was repeated with exclusive new outputs and a separate900-second budget,
   without reducing cases/assertions. No orphan process was retained.
3. Post-capture audit replaced a floating `floor(x+0.5)` reference with exact
   binary64 integer-ratio rounding: floating addition can lose the predecessor of
   a half-step. The compiled controller already used correct `lround`, and original
   boundary fixtures already had independent explicit expected integers. The
   executed reducer version is preserved; all actual native values were Q12
   centers, so no native expectation changes. Final strict verification rechecks
   every retained row with the stronger reference, and public tests cover every
   half-step neighbor. This is revised analysis, not a changed runtime or replayed
   claim about hardware.

## Regression and stop rules

Use the additive workflow because earlier CMake/justfiles/checkers are themselves
proof-pinned; they are not exempted, modified or blindly rehashed:

```bash
just --justfile virtual-handbrake.just check
just --justfile virtual-handbrake.just test
just --justfile virtual-handbrake.just docs-build
just --justfile virtual-handbrake.just verify-virtual-handbrake EXPLICIT_ROOT
```

Public tests compile the new adapter/protocol and validate synthetic reducer,
range/boundary/schedule and authority negatives without game artifacts. They are
not an original-game oracle. Strict verification fails on every missing/changed
required artifact, checks new build/input identities and complete retained trees,
recomputes all new pairs/repeats/schedules/commands/results, then invokes unchanged
Frozen/inherited proof. The complete native baseline regression runner and fresh23-run
unchanged handbrake matrix passed and are separately retained. Root `just check`,
`just test`, `just docs-build`, the12 new public tests and explicit strict
missing/changed-evidence rejection tests also passed; this is not only source
consistency proof.

**Stop at the virtual handbrake checkpoint.** No physical-device/force calibration,
all-car/all-mode/browser/concurrent-owner or universal long-session proof is
claimed. No new clean adjacent code, transmission/coupling/clutch/wheel physics,
FFB, replay codec, generalized controller, canonical integration or next recovery
is authorized. The evaluated source is the new overlay over publication commite5a99ac;
original identity-verified generated archives are reused, not claimed as a fresh
whole-game retranslation or a new publication commit.
