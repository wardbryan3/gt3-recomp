:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# Original engine-to-drivetrain power transfer

## Verdict and scope

**Read-only reconnaissance; not transmission recovery or recovery authorization.**
This report consolidates [Map v1](producer-consumer-map.md),
the historical moving-forward Reverse investigation, and the subsequent engagement
investigation for **GT3 USA v1.10**. The Reverse reproduction and search boundary
are retained below. It explains the bounded
original mechanisms rather than imposing a clutch pedal, a Neutral ratio, or a
modern gearbox model.

The central result is that **ratio selection, engine-rate synchronization,
permission to engage, and engine-directed effort are different mechanisms**.
There is no single established “clutch flag.” In particular:

- **ESTABLISHED:** state 0 bypasses the inspected engine-drive calculation while
  retaining a selected forward or Reverse ratio. Its engine rate can evolve freely.
- **ESTABLISHED:** state 3 uses a different, calibration-derived transfer term.
  With that term zero, a forward-to-forward shift can interrupt engine-directed
  effort without passing through state 0.
- **ESTABLISHED:** state 2 can transmit effort with coupling candidate zero;
  state 0 can suppress it with coupling candidate one.
- **UNRESOLVED:** independently reached policies 2–6, a player clutch control,
  a separately selectable Neutral, and the effect of an independently installed
  upgraded clutch in otherwise matched original execution.

“ESTABLISHED” below means established by the specified static body or finite
execution coverage—not universally executed on all cars, modes, or devices.
“INFERRED” marks an interpretation; “UNRESOLVED” identifies a remaining proof gap.

No clean transmission code, input adapter, direct state write, parts installation,
calibration/save/credits edit, or runtime/Frozen change was made. This continuation
launched **no new game runs** and introduced no new instrumentation. Its new
execution findings are reductions of previously accepted, immutable original traces.
Later [state recovery](state-transitions-v1.md) adds whole-admission ABI proof,
partial engine/commit decision models and independently reached post-drive aborts;
it does not turn this broader mechanism report into comprehensive recovery.

## Evidence and reconciliation

Original ELF SHA-256:
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
The documentation starting point is commit `0ec5cfa`. The engagement observer and
original runs remain at source/build context
`bdf1cf605a826626bfc65dcf0146e0729b098c5a`; they were not rebuilt at the documentation
revision. Original generated inputs were identity-checked reused baseline outputs,
not a fresh translation.

The engagement parent contains ten accepted observer/original/observer-repeat
trios: **30 runs, 4,508 observed / 13,524 total updates**. Their final snapshots,
complete 36 MiB EE/IOP/SPU dumps, capture sets, and observer-repeat traces match
exactly. Full-width car ownership, command lifetime, and stage order are qualified.
The separate Map and Reverse proofs remain separate populations, not extra
independent repetitions of these 4,508 updates.

The additional exact trace reduction yields:

| State at engine-stage entry, after that update's drive stage | Updates | Zero pre-ratio engine contribution | Nonzero observed rear engine-directed term |
|---|---:|---:|---:|
| 0 | 2,011 | 2,011 | 0 |
| 1 | 1,510 | 0 | 1,510 |
| 2 | 849 | 0 | 849 |
| 3 | 138 | 138 | 0 |

All 138 state-3 observations have the transfer coefficient at `car+0x2A4` zero.
The original ordinary net engine effort computed alongside it is **nonzero and
negative in all 138**; zero transfer is not merely a zero engine-effort sample.
This also prevents misdescribing these observations as 138 measured cuts of
positive acceleration or positive combustion torque.
**77 state-2 observations have zero coupling candidate and nonzero contribution.**
Across all 4,508 drive stages, the reducer also checks the original stored absolute
magnitude and the exact EE product from pre-ratio contribution to the rear term
for this drivetrain. These are retained-original consistency checks, **not a clean
implementation differential**, an all-drivetrain assertion, or a physical test.

Two corrections prevent misleading extensions of the earlier ledger:

1. The `001DDAD0` dispatch on saved incoming register 11 values 1–7 supplies
   placement/initial-condition data. It is **not** a demonstrated producer of
   transmission policies 1–7. Policy comes from a different saved argument.
2. The configuration consumed by initialization is a separately assembled object.
   Its byte offsets must **not** be read by treating `car+16` as that configuration.
   A rejected inventory made precisely this aliasing mistake; its output is excluded.

## A. Architecture: effort is not engine rate or vehicle acceleration

### Qualified chain

The relevant original update, rooted at `001E8598`, is ordered as follows:

```text
original command construction and owner-specific control processing
  -> processed pedals / request bytes / coupling candidate
  -> traction/effective-accelerator processing
  -> 001E6EC8 -> 001E6D48: admission and saved rate samples
  -> wheel/contact/slip preparation and existing force processing
  -> 001E5B98: engine contribution, ratio conversion, axle/driveline processing
  -> 001E6488: differential/wheel-rate processing
  -> 001E7500: engine-rate integration or tracking; synchronization completion
  -> 001E77E0 -> 001E5690: selection decision and immediate commit
  -> 001E7D90 / 001E8008: further chassis-force/velocity processing
```

The graph is a bounded causal slice, not a whole-game CFG. Some wheel forces and
speed updates occur **before** the current drive calculation. Thus even “this
frame's acceleration” cannot be equated to the current engine contribution.

### Quantities that must remain separate

| Quantity | Established role |
|---|---|
| `car+0x13CC` | Evolving engine-rate quantity; not torque and not selected ratio |
| `car+0x1414` | RPM-domain **halfword**, interpreted signed by relevant consumers |
| `car+0x13BA` | Selected ratio index; 0 is Reverse |
| `car+0x1310/+0x1314` | Saved engine/selected-ratio rates used in crossing tests |
| `car+0x139C` | Coupling candidate; consumers test zero/nonzero or exact one |
| `car+0x1478` | Absolute pre-ratio engine contribution stored by `001E5B98` |
| `car+0x1308/+0x130C` | Axle-directed engine terms; the covered rear-drive case uses the latter |
| Wheel/chassis force accumulators | Include contact, braking, resistance, and driveline effects—not engine torque alone |
| Longitudinal speed / vehicle acceleration | Results of broader integration, constraints, and prior/current forces |

`001E17F0`, `001E1768`, and their calibration/curve helpers produce signed engine
**effort**. Accelerator-dependent positive production, resisting effort, optional
curve/power shaping, and the RPM limiter are upstream of ratio conversion. The
limiter at `001E1768` has a calibrated upper threshold and a 500-RPM hysteresis
release; suppressing positive production does not mean all signed resisting
engine effort disappears. Nor does zero accelerator guarantee zero engine effort.

**INFERRED:** torque/inertia terminology is a useful physical interpretation of
these rate and effort operations. Exact physical units and a complete engine
model are not established by this investigation.

### Transfer and downstream effects

`001E5B98` chooses the state-dependent pre-ratio contribution, stores its absolute
magnitude, multiplies by the selected original ratio, then follows drivetrain-
configuration branches for axle terms and coupled rate/force processing.
`001E6C28/001E6CA8` derive the relevant axle/selected-ratio rates; this is not a
second gear selector.

`001E5768`, `001E57F8`, and `001E6488` combine wheel reaction/braking terms,
differential configuration, relative rates, limiting, and locked/free rate paths.
A zero engine term does **not** erase tire reaction, differential redistribution,
wheel rotation, vehicle momentum, or braking.

There are additional downstream zero/attenuation paths:

- `001E7C08` clears the relevant per-wheel force outputs when its wheel force/load
  input is zero; otherwise it shapes and limits the force vector before scaling.
- `001E8598` tests the exact sum of four wheel contact/load candidates. A zero sum
  bypasses the ordinary aggregate force/velocity work through arguments to
  `001E7D90/001E8008`. **INFERRED:** this participates in unsupported/no-contact
  handling; it is not demonstrated as a driver-operated disengagement command.
- `001E8008` has a separate suppression-halfword branch and low-speed/constraint
  branches that clear velocity/acceleration quantities. These are chassis gates,
  not evidence of a Neutral ratio or clutch input.
- Traction/effective-accelerator processing can reduce engine production; service
  brake and handbrake can oppose motion and separately veto engagement. They must
  not be collapsed into a single transmission disconnect mechanism.

These downstream bodies are statically traced, not newly branch-covered live.
No claim is made to have isolated every contributor to whole-car acceleration.

## B. Bounded state machine and per-update causality

### State meanings at the drive stage

| State | Original behavior in inspected bodies | Evidence boundary |
|---|---|---|
| 0 | Bypasses engine-drive contribution; later integrates free engine rate with an idle lower bound | Static plus 2,011 covered drive stages |
| 1 | Uses ordinary net engine contribution; later tracks selected-ratio-derived rate | Static plus 1,510 covered stages; “settled/coupled tracking” is a bounded description |
| 2 | Uses synchronization transfer machinery that can transmit effort even with candidate zero | Static plus 849 covered stages |
| 3 | Uses signed calibration-derived transfer term, rather than ordinary net engine effort | Static plus 138 zero-term stages in the covered zero-coefficient configuration |

For state 2, the inspected computation includes an engine-production-dependent
term, a rate-gap-dependent bounded gain, and sign handling. It is **not** a
multiplication of ordinary effort by coupling candidate. For state 3, the sign of
the calibration-derived term follows rate ordering. A nonzero calibration could
therefore change its result; the observed zero is not a universal property of 3.

### Transition table

| Stage / source | Condition | Result |
|---|---|---|
| `001E6D48`, state 1 | Candidate equals zero | State 0 before drive |
| `001E6D48`, state 0 | Candidate zero | Remains 0; both admission routes vetoed |
| Same, state 0 | Candidate nonzero, forward selection and speed strictly above +2.77777791 m/s, or Reverse and speed strictly below −2.77777791 m/s | Admit 2 only if **effective accelerator > 0.25** |
| Same, state 0 | Other speed/direction cases | Admit 2 only if signed sampled RPM strictly exceeds calibrated `car+0x234`; otherwise clear candidate |
| Same, states 2/3 | Preparation | Refresh saved engine/target rates; ordinary policy state 3 also chooses effective accelerator 0 or 1 from rate ordering |
| `001E7500`, states 2/3 | Saved ordering and current engine/target rates cross | State 1, clamp engine rate to target, write inhibition/rearm count 12 |
| Same, effective policy 3/6 | Candidate **exactly 1** | Special state-1 path writes axle/wheel rates from engine rate; this path does not perform the ordinary completion write of 12 |
| Same, still state 3 | Saved target at/below converted calibrated idle | Abort to 0 |
| Same, still state 2 | Processed brake >0.75 **and** (engine below converted idle+500 **or** speed strictly within the directional low-speed interval) | Abort to 0; the brake condition applies to either alternative |
| `001E77E0`, accepted selection while state 0 | Any accepted ratio | Commit ratio, retain state 0 |
| Same, accepted selection while nonzero state | Reverse involved (old or new index 0) | Commit ratio and state 2 |
| Same | Old and new selections both forward | Commit ratio and state 3 |
| Selector returns −1 | No accepted selection | No commit; −1 is **not a Neutral index** |

```text
                         zero candidate
              state 1 --------------------> state 0
                 ^                              |
                 | crossing / exact-one         | nonzero candidate AND
                 | special policy path          | applicable admission test
              state 2 <-------------------------+
                 ^
                 | accepted Reverse-involving selection from nonzero state
                 |
              state 3 <--- accepted forward-to-forward selection from nonzero state
                 |
                 +---- low-target abort ----> state 0

state 2 also has brake/low-speed aborts to 0.
A selection while already 0 changes the ratio without leaving 0.
```

This diagram is for the named normal-update bodies. Initialization/reset writers,
owner selection, and alternate control processing are separate entry conditions;
it is not an exhaustive whole-program alias proof for every possible state write.

**Timing matters:** completion in `001E7500` occurs after that update's drive.
Likewise a new selection/state written by `001E77E0` cannot describe the earlier
contribution. The next admission stage may immediately change a just-completed
state 1 back to 0 if the original coupling writer supplies zero.

### Entry, persistence, and exit of forward-selected state 0

**ESTABLISHED in independent original histories:** Reverse-derived coast and
brake-derived forward coast converge on state-1/zero-candidate admission to 0.
The preceding RPM is 799 against calibrated idle 800 in the covered entries.

A moving forward-selected coast can then persist in 0 even with candidate one:
nonzero candidate permits the directional-speed accelerator test; it does not
satisfy it. A stopped brake-derived coast can repeatedly have candidate written
one by input processing and cleared again by the insufficient-RPM admission test.

In the retained moving accelerator continuation, admission is at frame 5403,
about 7.869 m/s, effective accelerator 1, sampled RPM 799. In the independently
braked continuation it waits until frame 5418, RPM 2604 against threshold 2500.
The latter completes synchronization at 5570 **after drive**, falls back to 0 at
5571, re-admits 2 at 5572, and later completes again. A forward selection during
coast does not itself re-engage; that continuation admits only after accelerator.

Handbrake/brake-held continuations delay admission until release. These are
original control/threshold interactions—not an implemented Neutral command.
The **earlier 4,508-update engagement population** contains no late engine-stage
state-0 abort write. This is a finite-population result, not an unreachable-branch
claim. The later [state-recovery native matrix](state-transitions-v1.md#fresh-original-native-evidence)
independently reaches both the state-3 low-target and state-2 brake aborts **after
drive**; its 49 runs are a separate evidence population.

### Original-input reproduction and controls

The earlier Reverse checkpoint (`6c82588`) used the native-v3 ALTEZZA Single Race
MT fixture at frame 4501. The historical runner supplies its existing native pad
`--press` schedule; original command construction and processing execute, with no
virtual-input adapter or transmission/state/calibration patch. In this fixture Cross is
accelerator, R2 shift-up, Square brake, and Triangle auxiliary/Reverse. These
bindings and frame numbers are fixture-specific, not universal controls or timing.

| Original pad schedule | Purpose / observation |
|---|---|
| Cross at 4502 for 400 updates | Accelerate from the pinned start |
| R2 at 4700, 4760 and 4820, each for 4 updates | Accepted selections at 4701/4761/4821 reach indices 2/3/4 and settle |
| Triangle at 4902, replacing Cross | Auxiliary request arrives at processing frame 4903: index 4, sampled RPM 3154, positive longitudinal quantity about 20.11 |
| Keep Triangle held | Reverse commits immediately; free-engine interval later occurs at 5106–5121 |
| Alternatively, release Triangle after processing at 5108 | From 5109, no accelerator/brake/auxiliary input; free-engine coast persists through 5402 |
| Cross at 5402 in the released case | Forward selection accepted at 5403; settled state 1 at 5411 |

The qualitative recipe is **accelerate in a settled higher forward gear, request
Reverse through the original auxiliary path, then release it during the free-engine
interval**. The lower-gear control did not enter that interval. It is not an instant
Neutral button or guaranteed disengagement at arbitrary speed.

While Triangle is held, command auxiliary halfword `+12 = 4096` produces processed
request `car+0x1304 = 1`. Original arbitration also supplies accelerator from that
request: releasing Cross does not make held Reverse zero engine input. Relative
shift intent remains separate at command `+2` / car `+0x1305`.

The stage-qualified timeline explains why accepting Reverse is not the same as
settling it or interrupting drive:

| Frame / stage, higher-gear MT run | Selected index / state | Observation |
|---|---|---|
| 4903, selector return `001E77F8` | Stored 4 / state 1; accepted 0 | Reverse accepted, not returned as no-change |
| 4903, commit return `001E7838` | 0 / state 2 | Immediate Reverse commit while moving forward |
| 4904, history then drive | 0 / state 2 | Saved rate `+0x1310 ≈ 330.339`, target `+0x1314 = 0`; nonzero reverse-directed term |
| 5038, after command and at drive | 0 / state 2; candidate 0 | Sampled RPM 799 below idle 800, but contribution still nonzero |
| 5105, engine return | 0 / state 1; candidate 0 | Crossing completes **after** this update's nonzero drive |
| 5106, admission then drive | 0 / state 0; candidate 0 | State-1/zero-candidate exit; zero magnitude and negative-zero rear term |
| 5107, command then admission | 0 / state 0 | Command writes candidate 1; admission clears it to 0 |
| 5122, held-Reverse variant, drive | 0 / state 2; candidate 1 | RPM re-entry threshold passed; transition resumes |
| 5253, held-Reverse variant, engine return | 0 / state 1 | Settled Reverse tracking; subsequent backward motion |

At 5106 the positive longitudinal quantity is **7.92244**, HUD about 17 mph.
The held case later goes below −17 with HUD `R`. The free interval is genuine
while moving forward, not evidence that Reverse was rejected. In that held run,
**68 state-2 drive updates** have candidate zero and nonzero contribution. These
are this Reverse population's observations, not additional independent cases to
add to the engagement population's 77.

Held Triangle raises the free engine past the RPM admission threshold (2500 here),
so the 16-update free interval ends. It is not the shared 12-count inhibition timer.
In the released case, state 0/Reverse persists for **298 drive updates, 5106–5403**;
post-command candidate 1 is repeatedly vetoed, and the engine settles at free idle.
Saved engine/target samples are refreshed each preparation update, not latched for
the entire shift. Target may be recomputed after drive, and sampled halfword RPM
799 need not equal the raw engine rate.

A separate release-then-shift-up schedule requests R2 at 5202 without accelerator.
Index **1 is accepted at 5203** while state 0 is retained. At **5204–5402**, forward
index 1, state 0 and candidate 1 coexist with zero engine magnitude/rear term and
forward coasting. Cross then admits 2 at 5403 and reaches 1 at 5410. This contrasts
with the released-Reverse/accelerator schedule's settlement at 5411 above.

| Contrasting original-only schedule | Result in the observed continuation |
|---|---|
| Higher-gear MT, Reverse held | State-2 drive, 16 free-engine updates, resumed Reverse transition |
| Same entry, release during free interval | Longer coast with index 0; later accelerator returns forward |
| Same release, shift-up without accelerator | Forward index 1 with state 0 and candidate 1 |
| Lower-gear MT, Reverse held | Immediate index 0 and prolonged state 2; **no later state 0** observed |
| Higher-gear MT coast, no Reverse/brake | Retains index 4 / state 1; no later state 0 |
| Higher-gear MT brake, no Reverse | State 0 while retaining index 4: not Reverse-specific |
| Higher-gear MT Reverse plus brake | Separate conditional state-2 brake/speed exit; subsequent drive bypass |
| Low-speed MT Reverse/forward | Normal Reverse, negative motion and return forward; startup/braking state 0 remains distinct |
| AT policy 0, moving-forward Reverse | Immediate index 0; 16 free updates at 5743–5758, forward quantity near 9.52 |

Ordinary forward MT shifts in these prefixes use state 3 and candidate 1, with
commit before settlement. Entry conditions change whether and when free running
occurs; these controls do not establish a universal speed/RPM threshold surface.

**Separate Reverse evidence population:** nine observer/original/observer-repeat
trios, **27 accepted runs, 11,500 observed / 34,500 total updates**, **33
owner-qualified accepted selections**, and **14 new static records**. Exact trio
snapshots, full EE/IOP/SPU dumps, captures and repeated traces match. Coverage is
two pinned ALTEZZA states, MT and AT—not physical hardware or all cars. The SLK
attempt with undelivered Triangle input is excluded, not negative Reverse proof.
A reducer's initial host-rounding mismatch was retained and corrected to original
EE truncating multiplication without relaxing comparisons. These counts do not
augment Map v1's or the engagement investigation's populations.

### Bounded Neutral negative search

The Reverse search inspected these specific paths, without establishing a dedicated
Neutral action, ratio index or state-selection API:

- Original auxiliary/relative commands and digital helper `00210EF8`: separate
  accelerator/brake/handbrake/auxiliary actions and signed relative shift.
- Policies 0–6 and selector helpers, including `001E5540/001E5600`. A decrement
  from 1 to 0 still selects **Reverse**; −1 is no change and is not committed.
- Setter `001DD0D8` and constructor `001DDAD0`: owner/control-kind restrictions
  and original policy initialization, not every menu/device route to each policy.
- Policy-3/6 coupling interactions: static alternatives, not identified player
  clutch/Neutral inputs or demonstrated reachability.
- Defined ELF strings for neutral/clutch/shift/reverse and adjacent action-name
  references: no established Neutral string/action. Clutch-parts names identify
  no controller axis, and provider-defined strings do not cover every byte or
  encoded/localized resource.
- Native Reverse/release/shift-up/accelerator/brake gestures in MT and AT: reachable
  neutral-like state 0, including forward-selected coast, **not a Neutral API**.

The later configuration/owner/string tracing in sections C–E adds bounded context,
not whole-game absence proof. All device mappings, indirect paths, aliases,
cars/calibrations, reset/alternate owners and indefinite coasting remain outside
this negative-search claim. Neither “no neutral-like behavior exists” nor “a
native Neutral gear was recovered” follows.

## C. Coupling candidate, policies, and ownership

### What `+0x139C` does—and does not do

**ESTABLISHED:** ordinary input processing at `001E4180` writes candidate zero or
one from suppression conditions, current state, brake/handbrake processing, idle
calibration, and sampled RPM. State 0 and nonzero states have different writer
conditions. Initialization/reset paths also write it.

Policy 3 is distinct: it writes **1 minus processed brake**, clears processed
brake, and, when the result is nonzero, clears the two outgoing auxiliary/relative
request bytes. Fractional processed brake can therefore statically generate a
fractional candidate. This does not prove that a currently reached player profile
provides that original fractional channel under policy 3.

Policy 6 first adds vetoes for raw command **signed byte +2** or **signed halfword
+12** being nonzero, then follows the ordinary candidate logic. The halfword is
not another independent, identified clutch axis.

The inspected transfer path does **not** use this candidate as a proportional
engine-torque multiplier. Its established consumers use zero/nonzero permission
and an exact-one special synchronization path. A fractional value is not evidence
of fractional transmitted torque, and inverse-brake generation is not proof of a
physical clutch pedal or a dedicated player clutch mapping.

### Policy mechanics

These are **effective** policies. Owner/control-mode guards can select policy 0
instead of the stored policy byte; observing a stored value alone is insufficient.

| Policy | Inspected selector route | Other relevant distinction | Independently covered here? |
|---|---|---|---|
| 0 | `001E4FF8`, ordinary AT route | Ordinary candidate and synchronization | Inherited AT evidence; not new deep-pass runs |
| 1 | `001E5458`, MT route | Ordinary candidate and synchronization | Accepted engagement traces |
| 2 | `001E4FF8` with its alternate argument | Different AT branch; not an identified device mode | No |
| 3 | `001E5540` | Inverse-brake candidate; request suppression; exact-one rate path | Static only |
| 4 | `001E5540` | Shares this selector, not proof of identical complete control semantics | Static only |
| 5 | `001E5600` | Relative selector permits decrement toward index 0 | Static only |
| 6 | `001E5540` | Added raw-command vetoes; exact-one rate path | Static only |

`001E5540/001E5600` implement bounded original requests and rearm handling, not an
established H-pattern API. Sharing a destination does not identify a peripheral.
Values outside the dispatch range are not permission to invent fallback behavior.

### Producers and alternate owners

`0017AE88` writes its incoming argument to a driver record's `+8420` after index
resolution. Original initialization follows the scene callback through
`001F29A0/001F3188`: one branch copies driver control/policy words; other branches
clear them. `001F3844` carries the resulting arguments through `001DDAD0` to
`001DD0D8`. That setter accepts the policy argument for owner 0, forces policy 0
for owners 1/2, and leaves other owner values unchanged. `001DD0C8` separately
sets owner and clears the control-mode byte.

The retained caller search finds boolean/XOR-one and settings-word sources, but
**does not prove that all possible stored values are 0/1**, nor identify legitimate
player configurations producing 2–6. A read-only inventory of twelve independently
pinned historical original dumps finds owner 0, control-mode byte 0, stored policy
0/1, and zero `+0x2A4`. This is inventory evidence only: the profiles are not twelve
new engagement experiments, and compatibility profiles are not physical hardware.

`001E4D38` distinguishes ordinary owner-0 processing from alternate owner/mode
paths. `001E35D8` can call `001F8A00` with `car+3784`; that callee obtains the car
through the member at argument+4 and clears its candidate before either branch.
The retained fixture verifies that back-pointer. Thus **this is a qualified static
candidate-zero writer**, not merely an offset match. Its player execution and
policy applicability remain unproved in the accepted traces.

Conversely, the generic `001FC5C0` read of offset 1048 is **not** promoted to a
coupling consumer: its caller supplies a separate scene-owned, 0x4F0-stride object
array. Its surrounding operations concern paired-object geometry/response.
Equal numeric offsets do not establish the car/subsystem owner. Collision-like
response may affect motion without constituting transmission engagement.

## D. Original clutch-parts path and calibration

**ESTABLISHED statically:** the `parts_drv_clutch` registration reaches callback
`0015F2E8`; the lookup chain through `00235830/002352C0/00234C70` resolves
**category 15**, using the settings key at +184 and its parts header. The UI/change
registration and part lookup are concrete clutch-parts evidence, not a clutch input.

Calibration assembly at `002325B8` selects converter `00233C68` for that category.
Its relevant effects are:

| Source part field | Assembled configuration destination | Actual consumer / role |
|---|---|---|
| Bytes 17–20, percentage scalars | Halfwords 108, 106, 210, 212 respectively | Original integer scaling/division; not floating replacement math |
| Configuration 106 | `001E1C98` → engine-rate coefficients, including `car+0x214/+0x2BC` | Affects rate integration; **INFERRED** inertia interpretation |
| Configuration 108 | `001E10E8` → engine effort/curve coefficients | Effort/loss machinery; not a proved engagement switch |
| Configuration 210/212 | `001E1C98` → axle/driveline rate coefficients | Rate/response terms also consumed downstream |
| Byte 21 | **Byte 204** | Must not be silently substituted for byte 205 |
| **Byte 205**, separate source | `001E1C98` → `car+0x2A4` | Signed state-3 transfer magnitude after conversion |

The ordinary assembly path at `001DA308` first clears 994 configuration bytes.
The converter closure was inspected, including direct callees and helper stores;
no affirmative nonzero producer for byte 205 was established. In particular,
`00233C68` writes 204, **not 205**. The standard zero initialization is an identified
producer of zero; a nonzero producer or alternate supplied configuration remains
**UNRESOLVED**, not proved impossible throughout the program.

In the covered ALTEZZA part record, the four scale bytes are 100%, and byte 21
maps to configuration 204 value 150. Original lookup data remain private.
Neither that 150 nor a hypothetical installed upgrade establishes nonzero
`+0x2A4`. No off-by-one “repair,” configuration substitution, or speculative
clutch-capacity correction is justified.

**ESTABLISHED:** the zero runtime term explains the 138 covered state-3 zero
contributions. **UNRESOLVED:** a matched original installed-clutch comparison,
its effect on synchronization/effort/timing, and whether any legitimate original
configuration supplies nonzero byte 205. Static percentage scaling alone cannot
substitute for this comparison or prove upgraded-clutch gameplay behavior.

## E. Separate verdicts on disconnection and control semantics

| Question | Verdict |
|---|---|
| Can engine rate evolve without engine-directed drive while a forward ratio remains selected? | **ESTABLISHED**, state 0 in independently derived original histories |
| Can an ordinary forward shift interrupt effort without entering 0? | **ESTABLISHED in the zero-coefficient fixture**, state 3; not universal all-calibration behavior |
| Is candidate zero a universal disconnect? | **Contradicted** by 77 covered state-2 nonzero-drive observations |
| Does candidate one guarantee engagement? | **Contradicted** by forward-selected state-0 persistence |
| Is continuous candidate generation present in original code? | **ESTABLISHED statically**, inverse processed brake under policy 3 |
| Does candidate continuously scale transmitted torque? | **Not established; not what the inspected consumers do** |
| Is an original player clutch control identified? | **UNRESOLVED**; parts names and policy mechanics do not identify its configuration/device/input producer |
| Is separately selectable Neutral identified? | **Not found within the bounded command/selector/configuration search**; whole-game absence is not proved |
| Is index 0 or selector return −1 Neutral? | **No**: 0 is Reverse; −1 means no accepted selection |
| Does zero engine-directed effort imply zero wheel force or zero acceleration? | **No**; downstream/reaction/braking/constraint effects and integration are separate |

The fresh provider-defined string search found shift names and clutch-parts/UI
labels, but no matching Neutral label. Mirrored mapped strings are not independent
features. This searches **provider-defined string objects**, not every byte or
encoded/localized resource. The command builder at `00210740`, original command
consumers, selector dispatch, owner initialization, and inspected configuration
paths likewise do not establish a new dedicated Neutral/clutch command. This is
bounded negative evidence, not an exhaustive device/resource/indirect-call proof.

## F. Remaining gates and minimum useful experiments

| Gap | Exact missing observation or bounded next action |
|---|---|
| Policies 2–6 player reachability | Independently reached original native-v3 fixture; trace driver `+8420`, callback outputs, owner, stored/effective policy and control processing together. No forced policy byte. |
| Policy-3 fractional behavior | Such a fixture plus a legitimate original fractional channel; observe raw channel → processed brake → candidate → requests, drive stage and exact-one/non-one completion. The previous undelivered analog attempt is excluded. |
| Policy 6 | Original fixture showing its producer and actual command-halfword/relative-command vetoes; compare original release/rearm, not a guessed clutch profile. |
| Installed clutch | Same car/mode and documented independently installed original clutch difference, with unchanged other parts/settings; compare assembled inputs, derived coefficients, drive and synchronization. A user-supplied native-v3 fixture is sufficient. Buying/installing parts or save edits were not authorized here. |
| Nonzero configuration 205 | Original initialization that supplies it, including a lifetime-qualified source configuration and resulting `+0x2A4`; do not alias configuration to runtime car layout or copy byte 204. |
| Alternate writer/owners | Original execution reaching `001E35D8 → 001F8A00`, with full car back-pointer/owner qualification and subsequent admission/drive observations. Static applicability is not live reachability. |
| Downstream force gates | Original wheel-contact/load, limiting and suppression observations if whole-car force claims are needed; current static slice does not supply an all-branch dynamic force proof. |
| Universal absence claims | Additional device/configuration/resource and indirect producer closure. No finite empty string search can certify whole-game absence. |

Any newly instrumented experiment would need an untouched original control and
observer repeat with exact full-state/dump/capture parity, accepted input delivery,
owner/lifetime qualification, immutable source/build identities, and retained
failures. None of the missing fixtures is declared impossible to obtain.

## G. Recovery readiness and preservation

**Not ready for comprehensive engine/transmission recovery.** The normal
policy-0/1 control slice and forward-selected state-0 mechanism are substantially
better bounded. They are not substitutes for independent oracles covering the
unreached policy/calibration/owner branches, a bounded implementation contract,
full CPU/RAM/ABI and dynamic-cost differentials, and enabled/disabled/trace-only
live verification under isolated default-OFF build and runtime gates.

This report does not authorize even a seemingly simple candidate-to-clutch rename,
a Neutral sentinel, a clutch axis, an H-pattern selector, direct state writes,
a generic torque blend, or a calibration fix. Downstream original physics must
remain original unless separately authorized.

The earlier handbrake, virtual analog handbrake, Map v1, and moving-forward Reverse
checkpoints are preserved. Fresh private checks validate retained proofs; they do
not mean those historical native runs were executed again. No physical-controller,
physical-console, or modern clean replacement equivalence proof is added here.

### Reproducible private references

Current public and historical verification entry points are documented in
[workflow](../../developer-guide/workflow.md) and [testing](../../developer-guide/validation.md). The private verifier paths below
identify exact historical evidence contexts, not current builders or product gates.
The Reverse proof remains under ignored `local/reverse-shift-v1/`, with its separate
fail-closed `python3 local/reverse-shift-v1/verify.py`; its original manifest and
expected results are unchanged.

Raw evidence, original tables, instructions, traces and snapshots remain ignored
under `local/transmission-deep-v1/` and its immutable parent workspaces. The private
index connects claims to **131 distinct indexed static records (including inherited
records)** and explicit limitations. Verify the bounded continuation with
`python3 local/transmission-deep-v1/verify.py`.
Representative records:

| Finding | REA Evidence ID |
|---|---|
| Admission / saved rates, `001E6D48` | `ev_04f7f4fa255cfd7b17b2382c2b8f6607b46001126f3763211ecbfebc96c025cf` |
| Candidate writer, `001E4180` | `ev_bb5fb5ef8531fc36f779c5f6497b94025d39db99e2ccffde7eb0a04e2f11bd33` |
| Drive / state-3 term, `001E5B98` | `ev_a42bc92b6b1aee6c3da9437477398db145cdd39ed5b268b7e8cbc7f150b62237` |
| Engine / synchronization, `001E7500` | `ev_ba862eb7a3b5186afe285c12642ec3333b3edf31134220656870980836379388` |
| Actual containing update, `001E8598` | `ev_06f79f2c806da10e59afbf3a3eaee03ed08621b4cd5859258e7519e5f665a075` |
| Alternate writer, `001F8A00` | `ev_b5fe941019c84fc351b8c6f6bb09536907674b31d0a1f3516cb1b6db1320ec46` |
| Clutch converter, `00233C68` | `ev_e8d581284dab79c77fb8474d0b54e3584cd54376f97d9cc5332de2dc781c25c5` |
| Configuration initialization, `001DA308` | `ev_42e3c39c342c807e6d4c74e8ea02659c3d77476926062d1a21f027580584bd2e` |

Private verification is explicit and fail-closed; source/site checks require no
proprietary inputs. Passing artifact verification certifies the retained bounded
record, **not** universal model completeness or recovery readiness.
