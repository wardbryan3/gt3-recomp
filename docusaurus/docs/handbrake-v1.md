---
title: Handbrake Recovery v1
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


# Bounded clean handbrake recovery

**Frozen for the exact evaluated validation-only seam and source.** All named
public/native regression and strict evidence gates pass; the bounded live and
fixture limitations below remain part of that status.

**Current-source, validation-only recovery of USA PBPX-95503 v1.10.**
The replacement is the interior region **001E4BB8–001E4C5F**, joining original
processing at **001E4C60**, inside canonical function **001E4478**. It is not a
new whole function, a controller adapter, a wheel-brake rewrite or canonical
runtime installation. Lifecycle and exact evaluated source are authoritative in
[`handbrake.json`](registry/handbrake.md). No proprietary inputs are needed for
public checks; `just --justfile handbrake.just verify-handbrake EXPLICIT_REPOSITORY_ROOT` strictly checks
private proof and inherited Frozen evidence.

Implementation: `host/gt3_clean_handbrake.{hpp,cpp}`. Build and runtime gates both
default **OFF**. `gt3_recovered` only compile-checks this source; **ps2run does not
link it**. A disposable translated-unit overlay is the only installation.
Frozen pedals, steering, wheel compatibility, virtual pedals, runtime/recompiler,
transmission, coupling, clutch and FFB sources/authorities are unchanged.

## Verified producer → state → consumer path

The initial reconnaissance was checked against the fingerprinted original ELF,
Ghidra r5900 instruction evidence, and independently generated original execution.
The static ledger has 18 new retained records. Exact IDs, selectors, artifact
hashes and source/build context are in `decomp/gt3/handbrake.json`; raw records
remain private in `local/handbrake-v1/static-final.json`.

1. **Command lifetime and clearing.** 001E4D38 owns a 16-byte command at its frame
   SP. 00210740 first calls 001F4330, clearing flags and all command fields,
   including the halfword at +14. This is activation-local stack storage, not a
   newly inferred global input object. The existing observed positions 0049AF50
   and alternate 0049AF40 are not interchangeable pointers in one activation.
2. **Digital producer.** 00210EF8 tests digital mask **0x1000**, writes **1** to
   command+14 and clears only flag **0x10**. No matching mask leaves those bytes
   unchanged. Other action and shift writes remain original. This helper is also
   called from the existing wheel builder; no new wheel/handbrake adapter exists.
3. **Analog producer.** Primary 00211050 and secondary 002111C0 select mapped
   **action 4**, resolve a signed channel, skip negative/unbound mappings, set
   flag0x10, call original normalization00210F90, shift the result left four and
   truncate to the command halfword at +14. Zero still sets analog presence.
   Primary sensitivity is100; secondary handbrake sensitivity is20. Channel
   response, binding lookup and wrapping behavior remain in the existing reviewed
   mapping helpers/generated originals, not a new calibration interpretation.
4. **Ordering matters.** 00211430 applies digital actions before the applicable
   mapped-action fill. Input-kind selectors4/5/7/8 choose differing builder paths;
   this is not a universal device identification. 002115F8 can subsequently apply
   another digital-action pass before its wheel axis/pedals. It adds no analog
   handbrake axis. Existing clean wheel/mapping code was not edited.
5. **Recording/playback boundary.** 00210740 can instead use original001F4660,
   whose command cache at object+18 is copied as16 bytes. Its change-mask0x20
   updates cached handbrake at+26 through the existing halfword codec. Original
   001F4998 records changes to command+14 under the same mask and maintains the
   cache. The codec is not replaced or promoted to a newly recovered subsystem.
6. **Owner policy/notification.** After building the command,001E4D38 retains the
   original indirect notification and control-kind selection. Its manual branch
   reaches001E4CB0 →001E4478. Other branches remain original001E35D8. Immediately
   before the handbrake seam,001E4BA8 copies command+2 to control+1, or clears it
   under the existing car+14BA suppression. That is adjacent **shift command
   handling**, not handbrake history. Suppression does not itself skip the
   subsequent handbrake seam.
7. **Processing.** 001E4BB8 tests flag0x10 and sign-extends command+14. The only
   guest memory mutation in the bounded seam is the four-byte processed value at
   **car+13B4**. The prior value is digital history; no separate handbrake history
   byte was found in this seam. Steering/pedal history fields are not reused.
8. **Original continuation.** 001E4C60 calls original
   `update_control_coupling_candidate`001E4180. Wrapper propagation, original shift
   interface001E3A68, brake preparation001E6EC8 and engine processing001E7500 remain
   generated. Direct generated calls are covered by the disposable interior-label
   gate; this is not an assumption that dispatch interception catches them.

### State outside the manual seam

Original001E35D8 clears processed handbrake on entry. Original001E4CF0 can force it
to1 when car+14B8 equals8, after its existing helper. Owner selection remains
unchanged, so these mutations are neither lost nor incorrectly replaced by the
manual algorithm. This is a bounded manual-input recovery, not authority to
replace alternate/AI controls or initialize a whole car structure.

## Exact processing semantics and quirks

All arithmetic below denotes **EE bit-pattern operations** with original operation
ordering, not host double arithmetic, `std::clamp`, or a new normalized API.

Let `q` be the **signed** input halfword, `h` the previous processed value,
`rise`/`fall` the dynamic words at002D4940/002D4944, and `floor` the shared word at
00352990 (GP−5060 for the pinned GP). Stock rise/fall are each1; stock floor is the
binary32 representation of0.1. These are observed calibration values, not embedded
replacement tables or physical-device units.

| Mode | Exact behavior |
|---|---|
| Digital, q ≠ 0 | `x = add(h,rise)`; output1 only if `1 < x`, otherwise x |
| Digital, q = 0 | `x = sub(h,fall)`; output0 only if `x < 0`, otherwise x |
| Analog, q = 0 | Signed conversion and Q12 multiplication produce zero; store it directly |
| Analog, q ≠ 0 | `x = mul(cvt_s_w(q),2^-12)`; output `add(x,mul(floor,sub(1,x)))` |

Digital negative values count as pressed; magnitude is irrelevant. Press has no
lower clamp, release has no upper clamp. Analog is not generically saturated:
negative and above4096 values retain their original extrapolation. Analog ignores
old output, including its invalid/NaN-like history. A switch back to digital uses
that analog result as history. Unlike the mode4 accelerator/brake path, this
handbrake region calls **no response evaluator**. No time-step multiplier appears
in its ramp. Stock digital action is therefore effectively immediate under normal
history, but altered calibration/history is deliberately not simplified away.

### Interior CPU / cost / mutation contract

The clean semantic `Result` separates behavior from the EE join bridge. It carries
f0/f1/f2 scratch patterns, v0, conditional at assignment, final comparison condition
and dynamic cost. The bridge preserves every other CPU bit, including GPR upper
lanes, HI/LO/SA/FACC, other FCR31 bits, VU/COP0 and stack. The digital store of an
unclamped temporary followed by an endpoint store has the same final word and
mutation surface; no original call/probe/scheduling boundary lies between them.

| Path | Exact instruction budget charged |
|---|---|
| Analog zero / nonzero |14 /21|
| Digital pressed, unclamped / clamped |15 /17|
| Digital released, unclamped / clamped |16 /18|

Resume PC is001E4C60. Full-width base identities, alignment, 32MiB RAM bounds,
non-overlap, pinned GP and a fingerprint of every instruction byte in the seam
protect admission. The bridge writes **only car+13B4**, never opaque padding.
Commands need no assumed absolute stack address or ownership exception because
this seam only reads their bounded16-byte layout and retains no pointer/callee.

**Scheduling exception:** original digital release has a backward-branch
preemption check at001E4C14, after14 charged instructions. If that check might run,
the replacement declines without CPU/RAM mutation and lets the original execute.
Other paths contain no preemption check, so signed-negative budgets there are not
incorrectly rejected. Budget-underflow contexts also fall back. The call-free seam
has no recursion-depth dependency; generated exact-entry tests include at/beyond
`kMaxDepth`. No runtime scheduler or recompiler semantics changed.

## Downstream effects, with evidence limits

- **Rear brake contribution:**001E6EC8 first executes original001E6D48. It scales
  four wheel values at car+1074, strideA4, into requests at+1274, stride24, using
  gains+E38/+E3C by pair. It then adds
  `mul(processed_handbrake, car[E40])` to **only entries2 and3**, at+12BC/+12E0.
  It does not subtract front requests or saturate the handbrake addition. Its
  existing wheel flags subsequently reflect the resulting request and another
  zero-valued wheel field. This establishes rear-brake effects, not force units,
  physical hardware proof, or recovered wheel/tire physics.
- **Coupling candidate:**001E4180 checks the processed value against original
  GP−75E8 (stock0.8) only in a branch selected by car+20B==1, after higher-priority
  gates/policies. A value strictly above that threshold writes zero to the
  candidate at+139C. Other policy/brake/history branches still determine it. The
  wrapper fixtures cross the nearby Q12 codes3185/3186 and state gates; the
  original threshold effect is asserted. This does **not** prove the candidate is
  a clutch and it is not renamed.
- **Shift interface:**001E3A68, after original001E3360, passes an enable operand to
  original001E3068:1 iff processed handbrake is **strictly below** GP−75F8
  (stock0.1), otherwise0. Equality disables it. Live entry/decision/return probes
  show exact generated/clean CPU parity through this original processing. This
  records the observed interaction; it does not implement transmission, establish
  all downstream shift policy, or infer new field names.
- **Other reads:**001EB360 returns whether processed handbrake is strictly above
  0.25. Configuration-dependent reads in001E5B98 compare against additional
  thresholds. Their broader mechanics remain static-only/unclassified here;
  they must **not** be mislabeled as shift logic, clutch, or recovered physics.

Only command flags/+14 and processed car+13B4 were added to the new partial views.
Other offsets above are factual access observations, not newly typed structures
or permission to bulk-write car state.

## Differential and live proof

| Evidence class | Retained result |
|---|---|
| Independent exact generated entry |**2,228,224** cases: all65,536 halfwords × digital/analog ×16 history bit patterns, plus randomized calibration/history; full CPU/output/exact cost; batched full32MiB mutation-surface check |
| Stateful chains |**20,000** exact generated/clean transitions carrying prior output and scratch state across digital/analog/zero changes |
| Negative admission |**16** mutation-free rejections, including default-OFF, bounds/aliases/GP/profile and scheduling/budget guards |
| Original wrapper/consumers |**4,752** complete CPU+32MiB comparisons through original manual wrapper/coupling/brake/engine;38,016 rear-only formula checks across both paths |
| Native-v3 live |**23 runs**: five default/trace controls plus six generated/clean/repeat triplets;**1,800 actual clean substitutions**, zero fallback |

Join histories include signed zero, subnormals, boundary normals, infinities,
NaN-like patterns and extrema. Fuzzed calibration includes arbitrary bit patterns;
this is not exhaustive enumeration of every32-bit state combination. Existing
2e-6 tolerance is unchanged; these new join/wrapper/live parity comparisons are
**exact**, not merely within tolerance.

Native scenarios are neutral, held Circle, accelerator+handbrake then release,
wheel-brake+handbrake, native steering/shift buttons, and existing wheel/clean
steering compatibility. Each uses300 updates from the identity-pinned **native-v3
normal-boot Arcade Super Speedway fixture**. CPU/state/budget traces include seam
entry/join, original coupling return, original shift-interface entry/decision/
return, original brake entry/return and original engine entry. Generated/clean and
independent repeated runs match full guest dumps, all three captures and steering
traces. At live probes `Cpu.pc` is dispatch transport between direct translated
branches, not an ISA instruction counter: comparison uses the explicit semantic
probe PC and normalizes only the separately retained `transport_pc` field. Every
other defined serialized CPU field, including budget, is compared. The exact-entry
fixture compares the complete native CPU object, including the forced original
join PC. Captures were privately reviewed; no media are published.

**Live reached analog zero and4096 only.** Digital/intermediate analog are exact
fixture proof, not live reachability or physical-device proof. No synthetic
handbrake source, command injection, RAM relabeling, old-v2 loading or physical
handbrake was introduced. Native pressing uses the existing button path.

## Failed attempts retained

- Two initial overlay-generation attempts assumed001E6FC8 already had a generated
  label. The fix places a read-only probe at the verified instruction boundary;
  original instructions/budget remain unchanged.
- Two live attempts had exact output parity but **six protective fallbacks** in
  the accelerator/release case. They were not accepted as clean proof. An initial
  depth hypothesis was disproved (`depth_boundary=0`); signed-negative budgets
  were the actual cause. The guard was corrected by path-specific original
  scheduling evidence, then exact negative-budget/depth tests and the complete
  live matrix were repeated. Old builds, traces, source versions and the mistaken
  hypothesis remain in private evidence; hashes were not rewritten to hide them.
- The initial docs-generation attempt rejected changes to the root `justfile`
  and `provenance.json`: both are pinned by immutable virtual-pedal proof. Those
  two files were restored byte-for-byte, not rehashed or exempted. A subsequent
  metadata negative test exposed the temporary placement of a not-yet-Frozen
  record before the existing first Frozen interior record. The new record was
  moved after the existing one; the negative test was not edited or weakened.
  Additive tasks
  live in `handbrake.just`; the new manifest record links `handbrake.json` and its
  separate proof checker. Root `just test` also runs the new source/authority tests.
- A review-montage attempt found Pillow unavailable; ImageMagick produced the
  private montage instead. No environment package installation was needed.

## Bounds and stop

This checkpoint is bounded to the evaluated seam/source/profile and observed
fixture. It is not universal car/mode/thread/long-session/browser/physical proof,
complete replay/AI control recovery, or a right to distribute original materials.
Unsupported scheduling/admission contexts retain original fallback. Static
findings, generated fixtures and native live observations remain separate.

**Stop after handbrake.** No synthetic/physical handbrake input, transmission or
coupling replacement, clutch rename, brake/physics expansion, FFB, canonical
integration or next subsystem is authorized by this recovery.
