---
title: Pedal Recovery v1 — stopped prerequisite audit
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


## Subsequent authorized continuation

After the separate prerequisite baseline was committed/pushed as `46a32c7`, an
explicit user request resumed only the bounded pedal tail. See [Pedal v1](pedal-v1.md)
and [join audit](pedal-join-contract.md) for its new source, exact ABI/cost,
wrapper/consumer and native-v3 live proof. The stopped cycle below remains a
historical report; it does not describe the present implementation status.

## Subsequent prerequisite restoration

The separate [current-main native baseline](current-baseline.md) task has now
restored dependencies, fresh builds/regressions and a normal-boot identity-pinned
v3 race fixture, and repeated bounded steering/synthetic live validation. Its new
evidence is separate from this earlier stopped pedal audit. **That baseline task did not resume or promote pedal recovery.** The blocker descriptions below remain historical facts
about the earlier attempt, not current tool/fixture availability.

## Outcome

**Not recovered, not integrated, not Frozen.** This cycle stopped before clean
implementation. No steering semantics, generated bodies, runtime gates, original
assets, snapshots or cards were changed. Accelerator/brake execution remains
entirely generated. This is an audit of the candidate boundary, not completion of
Pedal Recovery v1.

Source context: clean checkout at `82987de` when the audit began. The maintained
inventories, rather than historical workspace paths, supplied the interpretation
of retained private evidence. `just verify-private` against the repository-local
preserved oracle verified the original ELF, eleven artifact hashes and 66 evidence
IDs without modifying them.

## Stop gate: current-main prerequisites

1. The available retained validation states are **v2**. All 22 top-level `.state`
   files in the repository-local validation donor have that header. Current main
   deliberately requires **v3**, including additional i.Link PHY state
   (`runtime/src/system.cpp`, `machine_state`). A probe linked to the available
   current-main software runtime archive called `ps2::load_state` on the retained
   race-start state. It returned false with **“state file from another version”**.
   No header was patched and no compatibility loader was installed. No validated
   current-main race fixture or compatibility path was available in the inspected
   current build/retained validation locations. This is the prerequisite already
   called out in `HANDOFF.md`, not evidence of broken pedal math.
2. A fresh regression build is unavailable in this execution environment:
   **`just test` fails in its build prerequisite because `cmake` is not found**
   (exit 127). `ninja` is also absent from PATH. The GPU baseline configuration
   attempt fails for the same missing `cmake`. Prior migration logs report passing
   builds; those historical results do not establish tool availability now. No
   system tools were installed or configuration rewritten to conceal the failure.

These prevent a fresh-build baseline and the required current-main live steering /
synthetic equivalence prerequisite. Available archive-linked fixtures are useful
but do not discharge either gate. Stop here instead of promoting historical
installation/live statuses or adding a snapshot compatibility/reset redesign.
A fresh supported v3 race capture or independently validated compatibility path,
plus a working documented build toolchain, is required before resuming. This does
not establish that fresh capture is impossible; it records what is missing at
this checkpoint.

## Candidate boundary: static audit

The retained original generated `unit_0039.cpp` supports
**`001E48FC–001E4BA7`, inclusive; rejoin `001E4BA8`**, within `001E4478`.
There is no demonstrated need to widen it. This is not yet a dynamically proved
replacement contract.

- Original prefix establishes `s7 = car`, `s0 = car+0F84`, `s2 = command`,
  `s3 = control-state address`, and the enclosing 176-byte stack frame.
- Immediately before entry, `v1` holds signed car+136D. Both the generated
  steering path and the preserved clean steering bridge supply it. The bridge
  itself is unchanged and is not installed into current-main gameplay.
- `001E48FC–001E4913`: compute numeric policy in `s1`. It is zero when control
  kind is 1 or car+14B8 is nonzero; otherwise it is unsigned car+13E5.
- `001E4914–001E4997`: obtain accelerator/auxiliary halfwords, flags and policy
  arbitration. Policy jump targets were checked in the fingerprint-verified ELF:
  0/1/2 select the larger unsigned request (ties select auxiliary and its source
  flag); 5 discards auxiliary; 3/4/6 retain both. Policies outside 0–6 retain both.
  Nonzero car+14BA clears the auxiliary request **before** arbitration.
- `001E4998–001E4ADB`: accelerator response/history and optional original response
  evaluator. Stores processed accelerator and control-state bytes +0/+2.
- `001E4ADC–001E4BA3`: brake digital/analog response and optional evaluator.
- All exits reach `001E4BA8` with **`v0 = uint16(car+14BA)`**. The digital
  non-clamping route performs that load in a branch delay slot; other routes use
  `001E4BA4`. Counting only the linear address span would be incorrect.

No tail stack stores were found in this generated region. Its two helper call
sites call **original `001D92E0`**, with input bits in `f12`, descriptor in `a0`,
`a1 = 0` (no derivative output), result in `f0`, and return PCs `001E4AD4` /
`001E4B9C`. The helper is a leaf in the inspected generated implementation.
Keeping those calls original is the appropriate bounded dependency; no general
math helper recovery is proposed here.

### Inputs and mutation surface

| Input | Evidenced role |
|---|---|
| command+0 bits 2/4/8 | Accelerator/brake/auxiliary analog representation flags |
| command+1 | Numeric mode; 4 enables the applicable response descriptor calls |
| command+8 / +12 | Unsigned accelerator / auxiliary halfwords |
| command+10 | Signed brake halfword |
| car+136D, +13E5, +14B8, +14BA | Control kind, numeric policy, suppression state |
| car+13AC / +13B0 | Prior processed accelerator / brake bit patterns |
| control-state+2 | Accelerator history/source state; unknown values must persist where original does |
| 002D4930/34/38/3C | Accelerator rise/fall and brake rise/fall constants |
| gp-20576 (00352990 for pinned gp) | Nonzero analog floor coefficient |
| 0049D060 / 0049D070 | Runtime response descriptors; not file-backed ELF calibration |

The bounded direct write surface is **car+13AC, car+13B0,
control-state+0 and control-state+2**. The command is read-only here. Control-state
need not be assumed to alias car+1304 for an arbitrary entry; that alias is supplied
by the evidenced manual wrapper. Existing steering partial-type padding is **not**
a pedal type or permission to bulk-write it. No new partial C++ layout was added.

### Arithmetic and history requirements

- Digital accelerator/auxiliary conversion is a left shift by 12 followed by
  **16-bit truncation**, not generic truthy-to-full-pressure conversion.
- Digital accelerator slews prior state with path-specific comparisons/clamps and
  writes history 1 or 2 according to the arbitrated auxiliary request.
- Analog nonzero accelerator uses unsigned Q12 conversion and the ordered EE
  transformation `x + k*(1-x)`, clears history, and can then call the descriptor.
  Analog zero with history is a separate decay path; it is not immediate release.
  History value 2 can force control-state+0 during decay.
- Brake analog uses **signed** Q12 conversion. Exact zero bypasses the floor;
  other values use the ordered transformation. There is no general analog clamp.
  Digital brake uses nonzero versus zero input to select rise versus fall and
  only performs the corresponding clamp. Negative digital halfwords are nonzero.
- Accelerator descriptor evaluation can be bypassed by active history; brake
  descriptor evaluation is on its analog mode-4 path. Zero input may still reach
  a descriptor; do not impose a post-descriptor zero or clamp.
- Original `001D92E0` operates on magnitude then restores sign, supports identity,
  shifted quadratic and shifted square-root descriptors, and uses EE operations
  and comparison keys. The derivative branch exists but both tail callers pass
  null. Descriptor calibration and reachable live edge domains remain unproved.

This describes requirements for future readable code, not a clean implementation
or a floating-special-case differential result.

### Outgoing ABI obligations still to prove

A future replacement must preserve the enclosing stack/frame and surviving
`s0/s2/s3/s7/gp/sp`, carry the computed **`s1` policy**, supply the outgoing
**`v0` suppression halfword**, and rejoin at `001E4BA8`. Exact branch/helper costs,
FPU condition/invalid state and path-specific scratch-register effects require an
independent join-level differential. No such harness or complete dynamic ABI/cost
proof was produced in this stopped cycle. Existing whole-routine steering tests
do not compare every scratch register at this interior join.

Effective accelerator **car+1428 is not written in this region**. Shift dispatch
`001E4BA8`, handbrake `001E4BB8–001E4C5F`, coupling `001E4180`, wrapper
`001E4CB0`, and downstream engine/brake consumers remain original/generated.
Likewise **car+139C is not a bounded pedal-tail write**.

`001E4180` remains `update_control_coupling_candidate`. Its policy-3 path clears
processed brake and derives coupling from `1-brake`, with control-state clearing
on its original condition. Policy 6 and other paths depend on shift/auxiliary,
handbrake, driveline and suppression inputs. A pedal-tail differential must include
those original downstream interactions; a pre-helper brake float is not the final
wrapper brake request. No physical clutch semantics or clutch axis is established.

## Evidence and discrepancies

Static evidence remains the immutable registry references, particularly:

- `ev_1ae7e5b58f8018c49aa9ed4a976e3984f3dda1001e36148fc94cff18145abd71`
  (control routine, wrapper, coupling and evaluator).
- `ev_4827844f7d8db4d5eae4302c47de04a2f2d0a72fee6ddfa4856e821bf4004958`
  and `ev_bd75205028a72307c6662fe769c9a5cb673340ce549400fac86ff1b2139eb2dc`
  (earlier control routine views).
- `ev_b6ab11b03e8cb2096578c1eb74a3c596422398b054c371f442f77ec9c77b78b8`
  (coupling view).

Retained generated `unit_0039.cpp` and evaluator `unit_0036.cpp` were used to
resolve pseudocode ABI ambiguity. Raw dumps and tables are not published.
No boundary contradiction was found. The important qualification to earlier
reconnaissance is that identity fixture descriptors are artificial: the live
writable descriptors are not stock calibration extracted from ELF bytes.
The request's frozen steering reference describes a **historical** installation;
current main is still compile-only. Migration success logs do not contradict the
observed missing tools, but must not be substituted for this session's results.

## Validation actually repeated

Unchanged fixture source was compiled with Clang against the **available
current-main `build/source` runtime/recovered archives** and the **retained
historically gated generated game archive**. This mixes source/compiled contexts:
the archives were not freshly rebuilt, and the generated archive is not claimed
to be freshly regenerated or installed into current-main ps2run. Oracle and clean
fixture executions remain independent. Profile guards passed.

| Check | Result / coverage |
|---|---|
| Controls differential | PASS: 25,600 normalization; 57,344 mapped actions |
| Steering trace | PASS: 15,360 pad frames |
| Wheel trace | PASS: 19,468 commands; 7,560 driving frames |
| Frozen clean differential | PASS: 28,160 normalization; 16,384 wheel; 16,000 filter; 20,000 envelope/full-tail cases |
| Synthetic adapter | PASS: 8,193 quantizations; 42 integrations; existing guards/parser/schedule |
| Original-only pedal discovery | PASS: 22 fixtures; **zero new clean pedal differential cases** |
| Available hardware / SIF executables | PASS, cached executables; not a fresh rebuild |
| Available recovered-source executable | PASS, cached; not an original oracle |
| Strict private verification | PASS: original ELF, 11 hashes, 66 IDs |
| `just check` | PASS |
| `just docs-build` | PASS |
| `just test` | **BLOCKED/FAIL**: missing `cmake` before tests execute |
| GPU regression rebuild | **BLOCKED** at configuration: missing `cmake` |
| Current-main race-state load | Rejected v2 as expected; **not a race run** |
| New live pedal / steering equivalence | **NOT RUN** |

Private commands, fixture logs and the load probe are retained under ignored
`local/pedal-v1/`. No immutable old evidence hash was updated. Registry lifecycle,
symbol meanings and type layouts remain unchanged; manifest notes record the
stopped cycle and generated knowledge assets are regenerated from that authority.
No enabled/disabled/trace-only live comparison or physical-pedal validation is
claimed. The unchanged `2e-6` tolerance and every existing assertion were retained.

## Exact next dependency — do not start it here

Restore the documented current-main build prerequisites and establish an
identity-pinned, safely usable **v3 race fixture plus original/clean steering and
synthetic baseline revalidation**, without changing frozen steering semantics or
spoofing v2 headers. Then resume the pedal join-level ABI/cost/descriptor audit and
independent differential harness. No transmission, clutch, handbrake, physics,
physical adapter or renderer recovery is suggested by this stop.
