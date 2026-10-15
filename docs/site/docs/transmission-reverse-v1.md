---
title: Moving-forward Reverse and neutral-like behavior v1
---

# Moving-forward Reverse and neutral-like behavior v1

**Read-only continuation of [Transmission Map v1](transmission-map-v1.md), not
transmission recovery or a controller implementation.** Source context: `6c82588`.
GT3 USA v1.10, original ELF SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
All transmission, coupling, engine, brake and neighboring routines remain
original translations. Canonical ps2run and Frozen systems are unchanged.

**Established** identifies a bounded original-code relationship; native evidence
is identified separately. **Inferred** describes a mechanism, not a recovered
original name. **Unresolved** means the proposed interpretation is not established.
Native here means original-game execution through the native recompiler/runtime,
not a physical PS2 or physical controller test.

## Result

The reported **neutral-like behavior is reproducible through original pad input**.
It is not adequately described as either “Reverse was rejected” or “coupling went
to zero, therefore the clutch opened.” The observed sequence combines:

1. **Immediate selection of Reverse, index 0**, despite forward motion.
2. A prolonged **state-2 rate transition that still transmits drive effort**.
3. In suitable entry conditions, transition completion followed by entry to
   **state 0: free-engine integration and a zero engine-to-driveline contribution**.
4. A temporary free-engine interval if Reverse remains held, or a longer coast if
   Reverse is released during that interval. An original shift-up request can
   subsequently select a **forward index while state 0 persists**.

No new neutral ratio is selected. Index 0 retains its negative original ratio and
HUD `R`. The forward-index coast is also not a second selected-neutral index.
A **dedicated Neutral command/index/state-selection API was not found within the
bounded search below**; that is not proof of absence throughout the game.

`car+0x139C` remains **coupling candidate**. It participates causally in particular
state changes, but it is neither a universal drive-torque multiplier nor a
standalone indication that the driveline is engaged. A clutch-pedal axis or
physical clutch-engagement percentage is **not established**. “Free-engine” and
“neutral-like” are **inferred descriptive names** for the established branch and
observations, not recovered original enum labels or a physical clutch model.

## Repeatable original-input reproduction

The accepted MT fixture is the existing native-v3 ALTEZZA Single Race state at
frame 4501. No state, transmission value, calibration or input command is patched.
The runner supplies the existing native pad `--press` schedule; original command
construction and all processing execute. In this fixture Cross is accelerator,
R2 is shift-up, Square is brake, and Triangle exercises auxiliary/Reverse.
Bindings are not asserted universal.

The high-forward-gear schedule is:

| Original pad schedule | Purpose / native observation |
|---|---|
| Cross at 4502 for 400 updates | Accelerate from the pinned start |
| R2 at 4700, 4760 and 4820, each for 4 updates | Accepted selections at 4701/4761/4821 reach indices 2/3/4 and settle |
| Triangle at 4902, replacing Cross | Original auxiliary request first arrives at processing frame 4903; selected index 4, RPM-domain sample 3154, positive longitudinal quantity about 20.11 |
| Keep Triangle held | Reverse is selected immediately; the later free-engine interval occurs at 5106–5121 |
| Alternatively, release Triangle after its processing at 5108 | No accelerator/brake/auxiliary input from 5109; free-engine coast persists through 5402 |
| Cross at 5402 | In the released case, a forward selection is accepted at 5403 and settled state 1 is reached at 5411 |

These are fixture-anchored native frame numbers, not a universal timing recipe.
The qualitative procedure is **accelerate in a settled higher forward gear,
request Reverse through the original auxiliary path, then release it during the
free-engine interval**. The lower-gear comparison did not enter that interval.
This is not an instant neutral button or a guaranteed response at arbitrary speed.

The original command contains auxiliary halfword `+12 = 4096` while Triangle is
held; the processed request `car+0x1304` becomes 1. Original arbitration also
supplies accelerator from that request. A held Reverse request therefore does not
mean zero engine input, even though Cross has been released. Shift intent remains
separate at command `+2` / car `+0x1305`. No virtual-input adapter is involved.

## Before, during and after: qualified native stages

The important order is **engagement/history `001E6D48` → drive processing
`001E5B98` → engine transition `001E7500` → selection `001E77E0`**. An engine-exit
state or selector result must not be retroactively attributed to earlier work in
that update. All results below are qualified to the tracked car and probe stage.

| Frame / stage, higher-gear MT run | Selected index / state | Established observation |
|---|---|---|
| 4903, selector return `001E77F8` | Stored 4 / state 1; accepted result 0 | Request is accepted, not held pending or returned as no-change |
| 4903, commit return `001E7838` | 0 / state 2 | Reverse index commits immediately while motion remains forward |
| 4904, history then drive | 0 / state 2 | Saved rate `+0x1310 ≈ 330.339`; target `+0x1314 = 0`; evolving engine rate changes independently; nonzero reverse-directed drive term |
| 5038, after command and at drive stage | 0 / state 2; coupling 0 | RPM-domain sample 799 is below the original idle threshold 800; drive contribution is still nonzero |
| 5105, engine return | 0 / state 1; coupling 0 | Saved/target crossing completes; this update still had nonzero drive contribution |
| 5106, engagement then drive | 0 / state 0; coupling 0 | State-1 zero-coupling branch enters state 0; drive magnitude is zero and the rear drive term is negative zero |
| 5107, command versus engagement result | 0 / state 0 | Command processing writes coupling 1; engagement processing clears it back to 0 |
| 5122, held-Reverse variant, drive stage | 0 / state 2; coupling 1 | Original RPM-domain re-entry threshold is passed; drive transition resumes |
| 5253, held-Reverse variant, engine return | 0 / state 1 | Settled reverse-rate tracking; subsequent execution moves backward |

The positive longitudinal quantity at frame 5106 is **7.92244**, with HUD about
17 mph: the car is still moving forward during the genuine free-engine interval.
The held case reaches a negative longitudinal quantity below -17 later, with HUD
`R` and wrong-way presentation. Private crops were reviewed for forward 4, `R`
during transition/free coast, forward 1 after selection, and settled Reverse.

The saved and target samples are **refreshed**, not values latched for the entire
shift. Native bit-level checks now include both `+0x1310` and `+0x1314`. At the
history-to-drive stage in states 2/3, the saved sample equals the incoming engine
rate, and the target matches the original selected-ratio product with its
nonpositive-to-zero rule. Engine completion can recompute the derived rate after
drive integration: the final engine rate need not equal the earlier target sample.

`+0x1414` remains a **halfword RPM-domain sample**, not an EE float or an exact
unclamped view of `+0x13CC`. Its original minimum/rounding behavior matters: 799
can coexist with a lower raw engine rate. State 0 then applies its own idle floor.

## Why it becomes free-running

### Reverse is selected before synchronization

The ordinary MT selector `001E5458` accepts the auxiliary request as index 0;
`001E77E0` / `001E4E78` commits it. The AT comparison follows its original policy-0
selector and also commits 0 before synchronization. There is no delayed selected-
ratio commit hidden in `+0x13BB`.

`001E6CA8` derives the rate using the selected ratio and a driveline-rate quantity
from `001E6C28`, not the chassis longitudinal value alone. A negative Reverse ratio
with a forward driveline rate initially yields a nonpositive product, replaced by
zero. Subsequent wheel/driveline evolution can change this target while the body
is still moving forward. “Reverse cannot immediately engage” is therefore a
reasonable description of **unsettled rate behavior**, not of rejected selection.

### State 2 is not the zero-drive branch

`001E5B98` treats the engine/driveline states differently. State 2 uses original
rate-gap-dependent drive processing; it is not equivalent to the state-0 bypass.
The new observation includes the magnitude stored at **car `+0x1478`** and the
ratio-scaled axle-directed term at **car `+0x130C`** in this original drivetrain
configuration. Their physical units and a general all-drivetrain model are not
claimed. Here the Reverse transition has a negative rear drive term, including
when coupling is zero.

For the higher-gear held case, **68 drive-stage updates have state 2, coupling 0
and nonzero drive contribution**. The first coupling zero is not the onset of
free running. There is no direct `+0x139C` load in this bounded drive routine.

### The zero-coupling test becomes consequential in state 1

In the ordinary policy-0/1 path, `001E4180` compares the signed RPM-domain sample
against the original idle threshold while the engine state is nonzero. At 5038
it writes coupling 0 because 799 is below 800. Other suppression/policy/handbrake
branches remain original; this sequence does not exercise them all.

`001E6D48` does **not** use its state-1 coupling-zero exit for state 2. The latter
continues to refresh samples and drive the original rate transition. At 5105,
`001E7500` completes the crossing into state 1. On the **next** pass, state 1 plus
coupling zero causes `001E6D48` to store state 0. This is a traced writer/consumer
relationship, not merely coincident field changes.

`001E5B98` starts its drive contribution at zero and bypasses its engine-drive
calculation when state is 0. `001E7500` separately uses free-engine integration
with its idle floor. This establishes an unloaded engine-drive branch, **not that
all wheel forces, braking, drag or vehicle motion are zero**.

### Why held Reverse exits, but released Reverse can coast

In state 0, normal command processing can write coupling 1 again when brake is
below its original threshold. That is not a guarantee of engagement. For the
observed combination of positive motion and selected Reverse, `001E6D48` uses its
RPM-domain admission threshold at **car `+0x234` (unsigned halfword, 2500 here)**.
If not passed, it clears coupling back to zero and leaves state 0.

Held Triangle continues to supply accelerator. The free engine rises above that
threshold and the next engagement pass admits state 2. The observed 16-update
interval is therefore **not a universal neutral duration or the shared 12-count
inhibition timer**.

Releasing Triangle during the free interval removes that accelerator. In the
accepted released case, state 0/selected Reverse persists for **298 drive-stage
updates, 5106–5403**. From 5109 through 5402 auxiliary, accelerator and brake are
zero. Motion remains forward near 7.9; the engine settles at its free idle floor.
Post-command coupling 1 is repeatedly vetoed by the engagement helper. Original
Cross input subsequently selects a forward index, and the positive-motion /
accelerator admission path permits the return to state 2 and then state 1.

## Forward selection while free-running

A separate repeatable schedule releases Reverse as above, then requests original
shift-up at 5202 without accelerator. The MT selector accepts **index 1 at 5203**.
`001E77E0` preserves state 0 when committing a selection from state 0.

At **5204–5402**, the drive-stage observations are:

- Selected **forward index 1**, state **0**.
- Coupling candidate **1**, but zero engine-drive magnitude and zero rear drive term.
- No accelerator or brake; forward coasting continues.

Thus **free-engine behavior retaining a selected forward ratio is reachable**, but
in this tested sequence it follows Reverse-induced free running and a subsequent
forward selection. It is not what happened at the initial Reverse commit.
Pressing Cross then admits state 2 at 5403 and settled state 1 at 5410.

This also supplies the converse counterexample: **coupling 1 is insufficient to
establish engaged drive**. The field must be interpreted with engine state,
processing stage, original policy and admission conditions. It must not be renamed
“clutch” or exported as a calibrated engagement percentage on this evidence.

## Comparisons and bounded Neutral search

| Original-only schedule | Relevant distinction |
|---|---|
| Higher-forward-gear MT, Reverse held | State-2 drive transition, then 16 free-engine updates, then resumed Reverse transition |
| Same entry, Reverse released during free interval | Longer coast with index 0; later original accelerator returns forward |
| Same release, shift-up without accelerator | Forward index 1 can coexist with state 0 and coupling 1 |
| Lower-forward-gear MT, Reverse held | Immediate index 0 and prolonged state 2, but **no later state-0 interval** in the observed continuation |
| Higher-gear MT coast control, no Reverse or brake | Retains index 4 / state 1 during the comparison coast; no later state 0 |
| Higher-gear MT brake control, no Reverse | State 0 also occurs while retaining index 4; free-engine state is not Reverse-specific |
| Higher-gear MT Reverse plus brake | Separate original brake/speed exit from state 2; state 0 is written before the next drive-stage bypass |
| Low-speed MT Reverse/forward control | Normal reverse engagement, negative motion and return to forward; startup/braking state 0 remains distinct |
| AT policy 0, moving-forward Reverse | Immediate index 0; another 16-update free interval at 5743–5758, still moving forward near 9.52 |

Ordinary forward MT shifts in these prefixes use state 3, selected index commits
before settlement, and coupling remains 1. The lower-gear Reverse comparison and
AT comparison demonstrate that entry conditions change timing and whether the
free interval is encountered. No universal speed/RPM threshold surface is claimed.

The **static and reachable-path search boundary** was:

- The original auxiliary/relative-shift command path and digital action helper
  `00210EF8`: separate accelerator/brake/handbrake/auxiliary actions and signed
  relative shift, not a newly discovered Neutral action.
- Dispatch policies 0–6 and their selector helpers. New inspection of
  `001E5540` / `001E5600` supplements Map v1: one helper permits downshift from
  1 to 0, but that is still the existing Reverse index, not an added neutral slot.
  No dedicated neutral-index return was found in these bounded selector paths;
  `-1` still means no change and is not committed as a gear.
- Configuration setter `001DD0D8` and constructor `001DDAD0`: policy is supplied
  through original initialization, with owner/control-kind restrictions at the
  setter. A policy number is not itself a neutral ratio. This does not establish
  every menu/device route to every policy.
- Original policy-3/6 coupling-related branches from Map v1. They remain candidate
  alternate interactions; user-facing meaning/reachability is unresolved, not
  grounds for inventing a clutch/Neutral input.
- Defined ELF string search for neutral/clutch/shift/reverse and the adjacent
  action-name references. No Neutral string/action was established; clutch-named
  tuning/parts strings do not identify a controller axis. Ghidra-defined strings
  are incomplete coverage of possible text, and strings alone are not behavior.
- Native original gestures above: Reverse, release, relative shift-up, accelerator,
  brake, MT and AT. These establish reachable **neutral-like state-0 behavior**,
  including a forward-selected coast, but not a dedicated Neutral selection API.

**Unresolved:** a dedicated Neutral control or separately selectable neutral
ratio elsewhere; all original configuration/device mappings and policy meanings;
all cars/calibrations, reset/alternate-owner paths and indefinite coasting. The
conclusion is neither “GT3 has no neutral-like behavior” nor “a native neutral gear
has been recovered.”

## Evidence, validation and stop

Private evidence is under ignored **`local/reverse-shift-v1/`**: 14 new REA records,
probe-only original overlays, input plans, raw observations, native-v3 states,
complete dumps/captures, retained exploratory attempts, reducers and a fail-closed
verifier. Map v1's 17 static records and earlier evidence remain unchanged.

Nine schedules each ran **observer / untouched original / observer repeat**:
**27 accepted runs, 11,500 observed updates / 34,500 including controls and repeats**.
All trio snapshots, complete EE/IOP/SPU dumps and captures match exactly; repeated
observation traces match exactly. There are **33 owner-qualified accepted
selections**, each checked against its immediate original commit. Samples include
full-width owner identities, valid command lifetimes, both rate-history fields,
engine/drive stages and register/FP context. Removing probes reproduces the entire
original translation text of the three rebuilt units; linked original archives
and host/runtime/input identities are verified.

These accepted runs use **two pinned states of one ALTEZZA**, MT and AT. An
exploratory SLK context did not deliver the scheduled Triangle input as the
tracked auxiliary request; it is retained, excluded and not negative proof about
Reverse in that car. The first analysis reducer incorrectly used host IEEE
round-to-nearest for a target multiplication; its one-bit mismatch was retained.
The corrected reducer uses the existing EE truncating product semantics and keeps
exact comparisons. No game/runtime behavior, tolerance or expected evidence hash
was changed to make a run pass. Private image review uses external cropping only;
original captures remain unchanged.

Representative new REA records (Ghidra 12.1.4, r5900):

| Boundary | Evidence ID |
|---|---|
| State-dependent drive processing `001E5B98` | `ev_a42bc92b6b1aee6c3da9437477398db145cdd39ed5b268b7e8cbc7f150b62237` |
| Alternate selector `001E5540` | `ev_94d6d2871c2c4695d245f04c8591b91c575c458631442f3d43f0c095530c01ae` |
| Alternate selector `001E5600` | `ev_1c5de75be186030dc41e5404126a6339b80e3cbc8525216a4804335dac5d7d42` |
| Forward-index selection helper `001E4E80` | `ev_b9f1ba9d5fcebd77e752feb4cab6f2e602c39c01070d438e9412fdf2a28bf8f2` |
| Original digital action helper `00210EF8` | `ev_843178f095daa914ee77e9ee005a0a46fc477eab944ebd02f9c3ee427c015287` |
| Policy setter `001DD0D8` | `ev_6fd50713b6f952786645c67bba4822542d2474085d21d124b0e61ec318c54208` |
| Policy initialization `001DDAD0` | `ev_5d12bb4943722bcfa886126811fd845b0eb14b687485c0f7af3389f760e41842` |
| Bounded defined-string search | `ev_3ca19485413d758da201a63be5ffad76f3bce25203324dc3f23d8843d0fb6547` |

The coupling writer, history/engagement and engine-transition records cited in
[Map v1](transmission-map-v1.md#evidence-references) supply the other causal edges.
REA's native session is closed. No raw assembly, decompiler output, calibration
table, generated game code or game media is published.

The private manifest pins **2,026 members**, SHA-256
`530cdadc8cb2fc996e61a5236d04997378e8de6e53ffc67ab5b344aa703b2205`.
The new static bundle SHA-256 is
`b77aba4a9b6d2e9ba5457a6cb20bd44594f1c8a2d103c1a22aa1ed42990644cb`.
Explicit private verification: `python3 local/reverse-shift-v1/verify.py`.
Required-evidence read faults reject missing/changed input with `FileNotFoundError`
/ `AssertionError`, without modifying the retained originals.

Root and additive source checks/tests/docs builds, unchanged Map v1 verification
and inherited Frozen strict verification passed. These are separate from this
original-only investigation; no new clean/original differential or physical proof
is claimed. Missing/changed-evidence rejection does not authorize rehashing a
mismatch.

**Stop at this read-only mapping checkpoint.** No clean transmission C++, H-pattern
or virtual transmission controller, direct neutral/state/coupling write, physical
clutch mapping, Frozen change or canonical runtime integration is authorized.
