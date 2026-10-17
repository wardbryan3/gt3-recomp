---
title: Transmission producer-to-consumer map v1
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


# Transmission producer-to-consumer map v1

**Read-only investigation, not recovery or an input-controller implementation.**
GT3 USA v1.10, original ELF SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
Source context: `ff31b22`. At this investigation checkpoint, all transmission,
engine, coupling and neighboring routines were generated-original. No canonical
runtime installation changed.

**Established** below means a bounded original-code relationship, with native
corroboration explicitly identified where available. **Inferred** names summarize
a mechanism but are not recovered original names. **Unresolved** means the
investigation does not establish the proposed interpretation. Static tracing,
original-only native observations and physical hardware proof are different claims.

## Reading the transmission reports

Start here for **command → policy → accepted selection → immediate commit**.
The reports below describe different boundaries, not successive claims that the
whole gearbox has been replaced:

| Report | Boundary and purpose |
|---|---|
| [Power transfer](transmission-power-transfer-v1.md) | Original mechanism, Reverse reproduction and controls, coupling, effort and calibration limits |
| [MT selector](transmission-recovery-v1.md) | Whole `001E5458–001E553B`; its original proof retains generated speed helper `001E4E80` |
| [Speed search](transmission-speed-v1.md) | Separate whole-helper recovery and later selector/helper composition proof |
| [State transitions](transmission-state-v1.md) | Whole admission `001E6D48–001E6EC7` ABI recovery, but **partial engine/commit decision models**, not whole-engine/commit replacements |
| [Virtual clutch/H-pattern](virtual-transmission-v1.md) | Deliberate extension of original transition policy, not recovered original inputs |

The [original-input reproduction](transmission-power-transfer-v1.md#original-input-reproduction-and-controls)
reaches free-engine behavior, including a forward-selected coast, without finding
a dedicated Neutral ratio/API. This map retains its separate original evidence
and coverage below. For current source ownership and product exclusion, use
[architecture](architecture.md); historical validation admission is not current
product approval.

## Main conclusions

- **Established:** command signed byte `+2` is relative shift intent, copied to
  `car+0x1305`; it is not an absolute requested gear.
- **Established:** `car+0x13BA` is the stored selected ratio index. The selector
  returns an accepted index in `v0`, or `-1` for **no change**. The accepted index
  is committed immediately, not held in `+0x13BB` pending completion.
- **Established:** `car+0x13BB` selects engine/driveline transition behavior.
  It is not a second gear number. A newly selected ratio can coexist with an
  unfinished engine-speed transition.
- **Established in the observed ALTEZZA contexts:** policy 0 uses autonomous AT
  selection; policy 1 uses the MT helper. Native MT cycling reached 1–6 and back;
  native AT shifted with zero shift-button intent.
- **Established in this path:** index 0 is reverse, not neutral. Selector return
  `-1` means no change, not reverse. A separately selectable neutral gear is
  **unresolved**.
- `car+0x139C` remains **coupling candidate**. Its role as a coupling/transition
  gate is established; a physical clutch-pedal axis, calibrated clutch engagement
  percentage or general clutch-input API is **not** established. Ordinary native
  MT shifts did **not** force this field to zero.

## Input through accepted selection

The existing digital command helper assigns signed shift byte `+2` even for a
zero mask: bit `0x8000` prioritizes `-1`; otherwise bit `0x4000` produces `+1`,
otherwise zero. This is the existing action boundary, not a newly invented pad
binding. In the observed native configuration, R2 produced `+1`, L2 produced
`-1`, and Triangle exercised the auxiliary/reverse path.

The bounded chain is:

1. Original command construction returns to `001E4D5C`; original notification and
   manual command processing still execute.
2. `001E4478`, at `001E4BA8–001E4BB4`, copies command `+2` to the second byte of
   the control pair at `car+0x1304`, i.e. `+0x1305`. Nonzero suppression halfword
   `car+0x14BA` clears that shift byte instead. The first byte, `+0x1304`, is the
   processed auxiliary/reverse request used by the selectors.
3. `001E77E0` passes that pair to `001E5690`. The latter resolves a policy using
   `car+0x13E5`, with overrides from owner/mode and suppression state; it is not
   simply an unconditional read of an AT/MT setting.
4. For effective policy 0, `001E5690` calls `001E4FF8` with variant 0. For policy
   1 it calls `001E5458`. Policy 2 also uses `001E4FF8`, with variant 1. Policies
   3/4/6 reach `001E5540`; policy 5 reaches `001E5600`. These other policies'
   user-facing meanings and reachability remain **unresolved** here.
5. `001E77E0` receives either no-change sentinel `-1` or an accepted index. For
   a change, it updates transition state when appropriate, then calls
   `001E4E78` with the car's `+0xF84` subobject and the accepted index. The helper
   stores the low byte at subobject `+0x436`, i.e. **car `+0x13BA`**.

There is no additional delayed gear commit in this observed chain. In particular,
**do not present `+0x13BB` as a pending, selected or actual gear number**.
This does not prove that no other gear-related field exists elsewhere.

## Fields, history and ratio effects

| Location | Width | Bounded role / status |
|---|---|---|
| Command `+2` | signed byte | **Established:** relative up/down/zero intent |
| Car `+0x1304 / +0x1305` | bytes | **Established:** selector control pair; auxiliary/reverse request and signed shift intent |
| Car `+0x13BA` | unsigned byte | **Established:** stored selected ratio index, used in ratio lookup |
| Car `+0x13BB` | unsigned byte | **Established:** engine/driveline state, not a gear index |
| Car `+0x13BE` | unsigned byte | **Established:** shared inhibition/countdown/release-rearm state; not a gear |
| Car `+0x1310` | EE float bits | **Established statically:** saved engine-rate sample in `001E6D48` |
| Car `+0x1314` | EE float bits | **Established statically:** selected-ratio-derived target sample in that helper |
| Car `+0x13CC` | EE float bits | **Established:** evolving engine rate, not a gear or an input axis |
| Car `+0x1414` | signed halfword at consumers | **Established statically:** RPM-domain conversion used by selector/idle thresholds; not a float |
| Car `+0x139C` | EE float bits | **Established:** coupling/transition gate; physical clutch-axis interpretation unresolved |

`001E6CA8` obtains a driveline-rate quantity from `001E6C28`, multiplies it by
`car[0x244 + 4*selected_index]`, and replaces a nonpositive result with zero
using the original EE operations and comparison. Thus changing
`+0x13BA` changes the rate target even while `+0x13BB` remains transitional.
In `001E6D48`, states 2/3 save the engine-rate sample to `+0x1310` and that
ratio-derived result to `+0x1314`. These are refreshed samples, not a second gear
or necessarily a value latched for the entire shift. `+0x1314` was statically
traced but was not one of the fields serialized by this native observer.

`001E7500` distinguishes these cases:

- State **0** uses a free-engine integration branch with an idle floor. This is
  an engine/driveline condition, **not proof of a neutral gear**.
- State **1** follows the selected-ratio-derived rate, subject to the routine's
  original rate limits. “Coupled tracking” is a useful **inferred name**.
- States **2/3** use the saved/target rate relationship and crossing comparisons
  to determine transition completion. The ordinary completion path selects state
  1, snaps the engine rate to the derived target and writes **12** to `+0x13BE`.
  There are also original idle/brake/speed exits to state 0 and special-policy
  branches. “Re-engaging” and “shift synchronization” are **inferred names**, not
  claims of a recovered physical clutch model.

`001E77E0` leaves state 0 unchanged when committing a selection. Otherwise it
chooses state 2 for reverse selection or a transition from old index 0, and state
3 for a forward selection from a nonzero old index. Both upshifts and downshifts
can use state 3. The state value therefore does not encode shift direction.

## MT, AT, reverse and timing

**MT helper `001E5458`:** positive intent increments the selected index only below
its configured maximum; negative intent decrements only when the old index is at
least 2. Ordinary downshift does not select index 0. Auxiliary/reverse request
can select 0. From reverse, accelerator/speed-dependent logic can choose a forward
index through `001E4E80`; it is not universally a hardcoded first-gear command.

**AT helper `001E4FF8`:** autonomous selection uses RPM-domain thresholds, current
index, accelerator/brake, speed, driveline state and driven-wheel conditions.
There are additional configuration-controlled shift-button branches, an override
countdown and a second selector variant. The native observations establish normal
AT policy 0, **not every AT override configuration or every calibration**.

**Shared history/inhibition:** a nonzero `+0x13BE` inhibits another selection while
it is decremented. If it reaches zero while shift intent is still held, the
helper rearms it to 1 and returns no change. The completion write of 12 is a
subsequent inhibition interval, **not proof that every shift lasts 12 updates**.
Accepted MT requests also arm the counter. Release/rearm behavior and the
upper/lower MT limits were reached in the native cycling run.

**Reverse versus neutral:** the native reverse sequence accepted index 0, showed
HUD `R`, used a negative original ratio entry and reached a negative longitudinal
value below -9 before returning to index 1. Index 0 is therefore not a zero-ratio
neutral in that fixture. No dedicated neutral command, selector index or stable
neutral API was established. A disengaged engine state with a stored forward
index must not be relabeled as a selected neutral gear.

## `+0x139C`: writers and consumers

Confirmed named writers in the inspected original path:

| Writer | Established relationship | Observation scope |
|---|---|---|
| `001DD5F0` | Initialization/reset path writes zero | Static; not a freshly exercised reset |
| `001DD8A8` | Initialization branch writes 1 and coupled state | Static; branch-specific, not every initialization |
| `001E35D8` | Alternate control path clears intent, then sets/clears coupling using mode and RPM thresholds | Static; no new alternate-controller experiment |
| `001E4180` | Manual command processing derives coupling from policy, suppression, brake, auxiliary/shift, handbrake and RPM/state | Static and observed normal native path |
| `001E6D48` | Can clear coupling again when state-0 engagement conditions are not met | Static and observed native startup transitions |

This is a confirmed-writer list, **not an exhaustive proof over all aliases,
object copies, initialization stores or snapshot restoration**.

Two directly traced transition consumers are:

- `001E6D48` tests coupling against zero when entering/leaving coupled state. It
  can reject an engagement and clear the field even after command processing
  wrote 1. A single sample before this helper is not the final coupling state.
- `001E7500` has special policy-3/6 transition behavior requiring coupling
  **exactly 1**, including wheel-rate adjustment using the selected ratio.

In `001E4180`, policy 3 derives `1 - processed_brake`, clears processed brake,
and can clear the control pair. Policy 6 can clear coupling for nonzero command
shift or auxiliary pressure. Ordinary branches also use suppression, processed
handbrake, brake and idle/state tests. Those are original policy interactions,
**not authorization to turn the brake or auxiliary command into a clutch axis**.
Fractional values are possible in the static policy-3 branch, but the normal
AT/MT observations here reached only 0/1.

Most importantly, in the MT cycling run, **all 600 post-command coupling samples
were 1**, including accepted upshifts/downshifts. Transition-state changes and
original effective-accelerator suppression still occurred. Equating “shifting”
with “`+0x139C` must be zero” is contradicted by original execution.

## Requested versus selected versus settled: native example

ALTEZZA MT, original-only execution:

| Native frame / stage | Accepted result / stored index | State / behavior |
|---|---|---|
| 4701, selector returns to `001E77F8` | Accepted 5; stored index still 4 | State 1 before the commit |
| 4701, `001E4E78` entry | Argument 5; old stored index 4 | State already changed to 3 |
| 4701, return at `001E7838` | Stored index now 5 | State 3; commit is immediate |
| 4702, `001E7500` entry | Stored index remains 5 | State 3; effective accelerator is zero |
| 4713, engine return `001E77BC` | Stored index remains 5 | State 1; inhibition counter is 12 |

This establishes both a short **accepted-result versus old stored-index** window
and a longer **new selected ratio versus unsettled engine/driveline** window.
It does **not** establish two persistent current/requested gear bytes. A future
telemetry consumer must not advertise a fully engaged physical gear solely from
`+0x13BA`, or use `+0x13BB` as the second gear number.

## Original-only runtime evidence and limits

A disposable observer adds read-only probes to three identity-verified original
translation units; stripping the probe calls reproduces the complete original
unit text. No input override, recovered substitution, budget adjustment or game
memory write is added. It reuses verified original archives rather than a new
whole-game translation. Linked host/runtime source identities were checked
against that baseline. This is fresh investigation at `ff31b22`, not installation
or revalidation of a clean transmission implementation.

Four native schedules each ran as **observer / untouched original / observer
repeat**: **12 accepted runs**, **2,700 observed updates**, **8,100 updates including
controls/repeats**. Each trio has exact native-v3 snapshot, final EE/IOP/SPU dump
and capture equality; the two observation traces also match exactly.

| Schedule | Observed updates | Owner-qualified accepted selections |
|---|---:|---|
| ALTEZZA MT cycling, R2/L2 with accelerator | 600 | 1→2→3→4→5→6→5→4→3→2→1; extra requests at the limits do not change index |
| ALTEZZA AT accelerator then brake, no shift buttons | 900 | 1→2→3→2→1, all with zero shift intent |
| ALTEZZA MT auxiliary reverse then forward | 600 | 1→0→1 |
| ALTEZZA MT accelerator, no shift buttons | 600 | Remains in index 1 |

The 16 accepted selections are counted only at owner-qualified selector returns;
no-change returns are separate. These are **two pinned native states of one car**,
not all-car/mode, indefinite-session or physical-PS2 proof. Private captures were
reviewed for HUD 6, R, 3 and 1 in the corresponding scenarios.

### Rejected leads and retained attempts

The old `001E3A68 → 001E3360 / 001E3068` lead did **not** identify the gear
selector: fresh static inspection shows traction/effective-accelerator and
wheel/brake-request processing there. `001E3708` likewise operates on wheel/
motion-dependent request state. Shared car fields or nearby call order did not
prove transmission ownership. Their complete subsystem semantics were not
recovered in this task, and their original behavior remains untouched.

An exploratory observer initially logged player fields at other cars' helper
calls, producing spurious apparent accepted requests. It also read an expired
stack command outside its lifetime. Those four exploratory runs are retained but
excluded from the accepted counts. The accepted observer records full-width
owner identities, qualifies results per probe site, and marks unavailable command
samples rather than interpreting reused stack bytes. Early manifest-shape/source-
scope checks and one argument-parser launch also failed before execution; logs
are retained. No original behavior, assertion or expected hash was changed to
accept those failed attempts.

### Evidence references

Private evidence is retained under ignored `local/transmission-map-v1/`:
`static.json` (17 REA records), `build-accepted/identity.json`, the twelve accepted
run directories, `summary.json`, `manifest.json`, `verify.py`, private captures/
review and rejected attempts. The explicit private verifier fails on required
missing/changed evidence. No raw assembly, generated bodies, captures or original
calibration tables are published here.

The 170-member private manifest SHA-256 is
`191e01595b138fc3eec718acff3132cf89e421b8c74ca19512806ff7f5c1a84c`;
the static bundle SHA-256 is
`e6c8c8662d31f544828aecb60cd6b5f7e33a42e5fc2338f9ac5957585ada480c`.
Missing/changed evidence rejection was also checked by read-fault injection without
altering the retained originals. Root and additive check/test/docs builds passed,
as did the unchanged inherited Frozen strict verifiers. These checks do not turn
this read-only map into a recovered implementation.

Representative REA records (original ELF, Ghidra 12.1.4, r5900):

| Claim boundary | Evidence ID |
|---|---|
| Policy dispatch `001E5690` | `ev_68a7346386b940c1b39d7b1e49cdb687964e61de042e149e6da1f259a1d2db9b` |
| MT helper `001E5458` | `ev_b97454512619de4d1a96d20dedf7fe7e04dcbdfb375531111adf7bd97a5dc75c` |
| AT helper `001E4FF8` | `ev_dd4b5c1dbe8d414d9fd0d1156d9a4f11006b957c2ed878511dbccf4bfef001e8` |
| Accept/commit orchestration `001E77E0` | `ev_ad6ff9600494d25109501f34eb4acb29d1d1310a63ef420b3789449066d27014` |
| Ratio-derived rate `001E6CA8` | `ev_86a78485335bf4706ca4be2298fc8c4241c88a4187126f8a79ea06066c0f190f` |
| Coupling writer `001E4180` | `ev_bb5fb5ef8531fc36f779c5f6497b94025d39db99e2ccffde7eb0a04e2f11bd33` |
| Engagement/history `001E6D48` | `ev_04f7f4fa255cfd7b17b2382c2b8f6607b46001126f3763211ecbfebc96c025cf` |
| Engine transition `001E7500` | `ev_ba862eb7a3b5186afe285c12642ec3333b3edf31134220656870980836379388` |

**Remaining unresolved:** independent neutral selection, physical clutch-input
semantics, all policy/configuration meanings, exhaustive alias writers/consumers,
HUD gear-producer internals, all-car/calibration transition behavior and every
mode/reset/alternate-owner path. No transmission source recovery, virtual
controller, neighboring-system cleanup or clutch rename is part of this checkpoint.
