:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# Original speed-to-index search: bounded recovery

**Frozen, validation-only; not installed in canonical `ps2run`.** This is the
separate recovery of USA v1.10 **001E4E80–001E4F0F**, followed by comparison of it
and the already-Frozen MT selector **001E5458** together against original generated
code. At that evaluated checkpoint, the existing selector source, authority, tests,
tooling, documentation pins, root recipes and runtime files were **unchanged**.
The historical companion authority is
`decomp/gt3/transmission-speed.json`; it does not enlarge the historical inventory.
The maintained `gt3_clean_transmission_speed.{hpp,cpp}` sources are now in
`src/gt3/gameplay/transmission/`, with no current product installation implied.
See [architecture](../../architecture/index.md) for present ownership, the
[conceptual map](producer-consumer-map.md) for the wider chain, and
[MT selector recovery](mt-selector-v1.md) for the earlier independent
contract. Later [state recovery](state-transitions-v1.md) is a separate admission
and decision-model boundary, not comprehensive gearbox recovery.

## In plain language

The selector sometimes asks: **“Given this original speed and this object's
original ratio data, which forward index should I request?”** This helper answers
that question. It does not put the car into that index, engage anything, change
clutch behavior or apply force. The existing selector still interprets an answer
of zero as one on its particular Reverse/accelerator route. Original orchestration
and commit code still decide what happens afterward.

Think of the new implementation as replacing one calculator, not replacing the
transmission. We first compared that calculator independently with the original.
Then we ran the unchanged selector tests with the new calculator switched off and
on. Finally we compared both together in original orchestration and native runs.

## Boundary and dependencies

```text
Original caller / policy routing
  ├─ original MT dispatcher001E5690
  │    └─ unchanged Frozen MT selector001E5458 [independent runtime gate]
  │          └─ original dispatch of001E4E80
  │                └─ new clean search [independent runtime gate]
  └─ other original callers of001E4E80

original001E77E0 orchestration/state decision → original001E4E78 ratio-only commit
engine / driveline / wheel / contact work remains original
```

The authenticated retained native dossier identifies a contiguous **144-byte whole
function**, no native callees, and callers001DD8A8,001E4FF8,001E5458,001F6588.
Those are static relationships, not four live caller fixtures. The positive native
search below is reached through the MT selector. AT control reaches neither helper
nor MT selector in the accepted interval: it is noninterference, **not AT search
coverage**.

The existing selector authority continues to describe its own older proof with a
**generated helper dependency**. That statement has not been rewritten. The new
composition has a separate, explicitly qualified proof. The selector's old field
`original_speed_calls` remains literally unchanged; in this new composition it is
reported as **speed dispatches**, not proof that the target body was original.
Independent helper counters establish the actual target.

## Bottom-up contract

Inputs are original `a0` object address, `f12` EE speed bits and original GP.
The helper reads:

| Relative location | Role in this boundary |
| --- | --- |
| object+0x20A, unsigned byte | maximum/result index |
| object+0x236, unsigned halfword | upper-rate-bound candidate |
| object+0x264+4*i | original denominator bits for candidate i |
| GP−0x75E4 | original scale bits |

It returns zero for an **EE-negative** speed. Otherwise, maximum zero or one is
returned without searching. For larger maxima it visits candidates **1 through
maximum−1**, returning the first whose threshold is **strictly greater** than the
input. With no match it returns maximum, **without evaluating that last index**.
Each threshold uses original signed `(upper_bound−500)` conversion, EE multiply
by the original scale, then EE division by that candidate's original denominator.

This is not a host `float` approximation. It uses the runtime's `fp::key`,
`fp::cvt_s_w`, `fp::mul` and `fpu_div`, including EE zero/denormal/extreme-value
handling and the division's sticky flags. No table is reproduced, replaced or
retuned. Synthetic tests vary denominator/scale bits in their own fixture RAM;
native runs never edit these values. Invalid maximum bytes and zero/negative
calibration inputs retain original quirks rather than being clamped.

`ObjectReadSpan` has explicit padding and offset/size assertions. Its conservative
255-word possible-read span is **not a claim that the original physical ratio
array has 255 elements**. It bounds what an arbitrary unsigned maximum could make
this original function read, including later object words in invalid cases.

### Observable EE effects

The new body preserves the complete outgoing CPU: scratchGPR2–7, all untouched and
upper GPR lanes, FP0–2, condition/sticky FCR bits, RA/SP, returnPC and exact budget.
Even maximum0/1 advances the outgoing `a0` pointer in the original delay-slot
position. Negative input leaves different scratch effects from the positive path.
There is no frame, callee, selection/state commit or RAM write in this boundary.
The explicit ABI bookkeeping is intentional: subsequent generated code can observe
more than the scalar answer.

## Scheduling and admission

The generated original can poll the scheduler at **two backward transfers**:
when returning a successful candidate through001E4E9C, and when continuing at
001E4EC8. Both are conditional on negative budget. Recovering only mathematical
results and ignoring those sites would be incorrect.

The new body does **not** recover scheduling or interior resumes. It admits a
looping entry only with budget **at least16*maximum+16**. The original worst-case
complete traversal costs16*maximum, so every backward poll in that admitted domain
has nonnegative budget. Negative-speed and maximum0/1 paths contain no backward
poll; safe negative budgets are supported there. Budgets too near signed underflow
are rejected. Original costs exercised are **7–4080**, exactly compared.

Other admission checks are original144-byte FNV fingerprint, original GP/full64
pointer representation, aligned bounded normal-RAM object/read span and safe
signed budget. Failure returns **before CPU/RAM mutation**, leaving generated code
responsible for execution and any yield/resume. Interior001E4E9C/001E4EC8 label
bodies remain generated; the overlay hooks only the whole-function entry.

Four controlled-scheduler cases use the **unchanged generated body** with a
linker-wrapped external `preempt` response: both poll destinations, yield and
no-yield, mutation-free fallback and original resume. These are scheduler-API
contract tests, **not real scheduler timing or hardware proof**. Native executables
are not linked with that wrapper. Their admitted clean calls perform no poll,
exactly like their original counterparts in those contexts.

## Independent original validation, before integration

The identity-checked baseline's generated original unit is compiled under separate
export/self-call and entry-array names. Reversing those names must reproduce the
original source exactly. The oracle self-calls its own original helper, not the
clean helper or hooked unit. The new source never supplies expected outputs.
Original ELF, generated sources, archives and source/build profile are checked;
this is not a fresh whole-game translation.

Executed independent corpus:

- **710,850 complete-CPU/exact-budget cases**, complete read span each case.
- **2,219 whole32MiB cases**, plus cumulative out-of-contract mutation checking.
- Every unsigned16-bit upper-bound value across three speed inputs; every unsigned
  maximum byte across targeted FP speed/denominator/rate combinations.
- Signed zeros, denormals, positive/negative extreme values, infinities/NaN bit
  patterns, zero/negative denominators, stickyFCR states and arbitrary upper lanes.
- Nonuniform ratios, exact threshold/equality/neighbors, 10,000 randomized cases,
  maximum254 searched iterations, RAM upper edge and admission-budget boundaries.
- **264 complete-CPU+32MiB mutation-free rejection cases**.
- **4 controlled scheduler/fallback/resume cases**, separately classified above.

No scheduler call occurs in any admitted corpus case. This is targeted exhaustive
byte/halfword coverage and FP class/edge coverage, **not exhaustive all32-bit FP
combinations or every possible global runtime context**.

## Both clean functions together

Only after the independent helper passed was a disposable generated **entry-label**
overlay built. Hooking the label matters: direct generated calls can bypass a
registration-table-only replacement. The selector calls original dispatch as
before; enabling the new helper changes the target reached by that dispatch.
No existing selector line or assertion was edited.

1. The **exact unchanged 663,959-case selector suite** passes in separate processes
   with helperOFF and helperON. Pair mode performs **6,571 actual helper
   substitutions**; every selector speed dispatch reaches it, with zero fallback.
2. The **exact unchanged 1,008-case original-consumer suite** passes OFF and ON,
   through original001E77E0→5690→selector→original4E78, with **36 helper
   substitutions** in pair mode.
3. A separate four-way matrix exercises neither clean body, selector-only,
   helper-only and both. **1,008 inputs /4,032 complete-CPU+32MiB comparisons**
   pass, including exact budget, original commit and preservation of state0.
   Actual selector substitutions are `[0,1008,0,1008]`; helper substitutions are
   `[0,0,36,36]`. Thus both direct generated-helper calls and the Frozen selector's
   dispatch are actually tested, not inferred from successful linking.

## Native validation

The accepted matrix has **28 runs**: original, buildOFF, runtimeOFF trace-only,
helper-only, selector-only, both and both-repeat for each of:

| Scenario | Updates per run | Qualified helper path |
| --- | ---: | --- |
| MTcycle | 600 | none; selector/control coverage |
| MTReverse | 600 | EE-negative input, result0, cost7 |
| ATcontrol | 300 | no MT/helper entries; noninterference only |
| moving-forward Reverse release | 201 | positive input, candidate1, cost28 |

The first matrix proved only the negative-speed helper path. That gap was recorded
before adding the last scenario. Its preparation used the unchanged original MT
snapshot, normal native acceleration/shifts/auxiliary-button schedule already
used by the earlier original investigation, and an ordinary save point. Untouched
original / runtimeOFF observer / observer-repeat preparations match exactly.
Continuations load **the original preparation's output** and deliver only native
`--press` acceleration. No memory/axis/guest-state injection, settings, parts or
save edits are used. **3 original-only preparation runs**,611 updates each, are
separate from the28-run substitution matrix. Total new gameplay: **31 accepted
runs /13,740 updates**. Two additional buildOFF CLI invocations reject clean flags
with exit2 before gameplay. There were no failed gameplay/build attempts in this
iteration; the initial positive-coverage gap was an actual limitation, not a failed
comparison quietly replaced by a later result. One later reducer diagnostic failed:
it expected200 positive-continuation entries, but the original preparation's saved
frame5111 produces **201** entries through5311 on reload. The failed reducer/log
are retained. The count and totals were corrected to the actual original trace;
no run, comparison, expected output, inherited pin or snapshot was changed.
The first seal candidate also failed strict canonical path ordering (`Path` ordering
versus serialized string ordering). It and its registration script/log are retained;
a fresh candidate sorts serialized paths, without weakening the verifier.
The first full private verification then completed the new proofs but failed on
an adapter typo (`old.private` instead of the unchanged selector API `old.verify`).
Its sealed candidate manifest, authority, checker, report and failed log are
preserved; the final seal is a **new manifest**, not a rewrite of that candidate.
The corrected delegation has an additional public regression test and the full
strict verification is rerun. No underlying oracle/native comparison was relaxed.

Across activated modes there are **4,203 actual selector substitutions and4,203
real-entry selector shadows**, plus **6 actual helper substitutions and6 real-entry
helper shadows**, all with **zero fallback**. Each shadow uses the real incoming
CPU/depth, independently runs original and clean, compares complete outgoing
CPU/exact budget and entire32MiB, then restores incoming RAM and both diagnostic
counter sets before actual execution. Shadow counts are not substitution counts.

The helper reaches original MT return001E54A8 at depth5, SP0049AF20, with owner0,
policy1, maximum6 and the qualified player object. The positive call occurs while
moving forward with Reverse still selected; it executes conversion/multiply/divide
and one candidate comparison, not merely a negative early return. **Native
exhaustion/multiple-candidate traversal is not covered**; those paths are covered
by independent and composition fixtures, not promoted to live proof.

Every seven-way group matches final snapshots, full36MiB EE/IOP/SPU dumps and
nonempty capture sets. The six instrumented modes match entry/return traces with
complete CPU/cost representations. The **trace copy's entryPC only** is normalized
to the function entry because direct generated and dispatched calls transport
incomingPC differently. Raw `transport_pc` is retained. No other trace field is
masked; actual outgoingCPU/shadow/RAM comparisons have **no normalization**.
Private side-by-side cycle/positive captures were visually reviewed.

## Build isolation, reproducibility and provenance

Canonical `host/main.cpp`, CMake, root recipes, original executables and archives
remain byte-identical. New code is not installed or added to the canonical runtime
library. The additive source test explicitly compiles it without original assets.
The disposable overlay's **build gate defaultsOFF**; both independent runtime
switches also defaultOFF:

- `--gt3-clean-speed`: new helper only.
- `--gt3-clean-transmission`: unchanged Frozen selector only.
- Both: opt-in composition.
- `--gt3-speed-shadow`: additional actual-entry comparison; not an implicit gate.

Fresh identity-preflight builds reproduce **11 object/executable outputs** byte
for byte, including independent oracle, unchanged Frozen object, pair composition,
legacy suites and native buildON/OFF hosts. Accepted launch paths remain identified
separately from their byte-identical reproduction paths.

Evaluated source base: `e9d8cb83caa383502d8935fc309aaeb27ecad63f`, with the new
source files individually hashed by the companion authority. Reused original
baseline source: `82987dec7a71d76414adfff8663da5494a280938`. Neither is represented
as a commit containing this uncommitted additive recovery. The old Frozen selector
strict verifier passes unchanged before and after. Its inherited, explicitly
version-qualified historical-document verification remains unchanged; this
iteration introduces no new document-resolution exception.

New private evidence is sealed under ignored `local/transmission-speed-v1`.
Strict verification requires all pinned members, accepted binary/source identities,
original inputs, native reductions and unchanged inherited proof. It re-executes
the independent original oracle, four-way composition and unchanged selector/
consumer suites OFF/ON. It does **not** relaunch gameplay or count retained native
evidence as a new live run. Missing/changed required bytes fail; read-fault tests
do not mutate actual artifacts. Raw generated bodies, overlays, linked binaries,
images, snapshots, dumps and REA evidence remain private.

## Current checks and historical reproduction {#reproduce-public-and-explicit-private-checks}

```sh
just check
just test
just docs-build
just verify-transmission-speed "$PWD" # explicit retained historical proof
```

Public checks need no proprietary artifact. The private command requires retained
inputs and checks the exact historical context; it is not current product acceptance
or a gameplay relaunch. The former `transmission-speed.just` and
`scripts/validate_gt3_transmission_speed.py` build/integrate workflow are retired.
Their exact evaluated versions remain in historical Git/private contexts, with the
original baseline, independent oracle and separate fresh OFF/ON outputs identified
by that proof. Historical documentation/source pins are not repointed here.
Use [workflow](../../developer-guide/workflow.md) and [testing](../../developer-guide/validation.md) for maintained guidance.

## Stop and remaining gates

This completes the requested helper-first, paired-second recovery, with bounded
validation-only freeze. It does **not** authorize another boundary, comprehensive
transmission replacement, installation, commit or push. No further recovery follows
automatically. Policies2–6, alternate-owner/caller live paths, all-car/thread/long
session/device/hardware proof, installed-clutch/config205 reachability and the
broader engagement/force questions remain open. Nothing here changes the meaning
of0=Reverse,−1=no accepted selection, or turns the coupling candidate into a
proportional clutch. Selection remains distinct from engagement and power transfer.
