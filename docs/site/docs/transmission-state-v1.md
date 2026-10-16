# Transmission state transitions: original decision model

## Result and limits

**Bounded original recovery, not a canonical transmission replacement.** This
companion work targets USA v1.10 `car+0x13BB`. It adds readable, bit-pattern C++
models of admission, preparation, synchronization/completion/aborts, free engine
integration, common engine clamping and selection commit decisions. One whole
routine, **001E6D48–001E6EC7**, additionally has an independently tested EE-ABI
implementation and an isolated, default-OFF native substitution.

The engine and commit **decision models are not ABI replacements** for whole
001E7500 or001E77E0. Their surrounding helpers, call/unwind/scheduler effects,
scratch registers and complete whole-function cost are deliberately not claimed
recovered. Engine production, target derivation, drivetrain force mathematics,
AT selection and initialization remain original. No candidate-to-clutch rename,
Neutral ratio, H-pattern API, calibration or canonical gameplay change is added.
Existing Frozen sources, authorities, tests, build recipes and documentation
remain byte-identical. No commit/push is part of this task.

- Models: `host/gt3_transmission_state.{hpp,cpp}`.
- Whole admission: `host/gt3_clean_transmission_admission.{hpp,cpp}`.
- Authority: `decomp/gt3/transmission-state.json`; workflow: `transmission-state.just`.
- Evaluated source base: `511f8575325e8d585ead26e92f56d109780d5635` plus separately
  hashed additive sources. Original generated baseline remains
  `82987dec7a71d76414adfff8663da5494a280938`; no fresh whole-game translation.
- ELF SHA-256: `b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.

## 1. Three decisions, not one clutch state

In the inspected ordinary update rooted at001E8598:

```text
original command/control/candidate generation
 ->001E6EC8 clears saved-rate slots ->001E6D48 admission/preparation
 ->wheel/contact processing ->001E5B98 drive ->001E6488 differential/rates
 ->001E7500 engine integration/tracking, completion, abort, clamp, RPM sample
 ->001E77E0 policy selection and transition ->001E4E78 ratio-only commit
 ->further original chassis/force/velocity work
```

A state written after drive cannot explain the contribution already calculated in
that update. In particular, **both newly observed aborts happen after drive**.
State3 can supply a zero engine term before an abort; state2 can supply a nonzero
term before aborting. Subsequent wheel forces, speed and acceleration are not the
same quantity as that term.

| State | Drive routing | Later engine behavior |
| --- | --- | --- |
| 0 | Bypass engine-directed contribution | Original effort integrates free engine rate; idle lower bound |
| 1 | Ordinary net engine effort | Track nonnegative selected-ratio target |
| 2 | Synchronization calculation, including rate-gap/production-dependent gain | Crossing or special-policy completion; possible brake abort |
| 3 | Signed calibration-derived transfer coefficient, not ordinary effort | Crossing or special-policy completion; possible low-target abort |

These are behavioral descriptions, not original symbol names. `+13BA` is selected
ratio, `+13BB` transition state, `+139C` coupling candidate, `+13CC` engine rate,
`+1310/+1314` saved engine/target samples, `+1414` sampled signed RPM halfword.
**0 is Reverse; −1 is a rejected selection, not Neutral.** Candidate one does not
guarantee engagement; candidate zero does not universally suppress state2 drive.

## 2. Complete decision table within the named normal-update boundaries

All floating comparisons below use the runtime's **EE `fp::key` ordering** on
original bit patterns, not host IEEE comparisons. Signed zero/denormals and
exponent-255 operands must not be reinterpreted as ordinary host math.

### Admission and preparation —001E6D48

| Incoming condition | State/candidate result | What does not happen |
| --- | --- | --- |
| State1, candidate EE-equal zero | Write state0 | Does not clear ratio or replace engine integration |
| State1, nonzero candidate | Retain1 | No engagement threshold check |
| State0, candidate EE-equal zero | Retain0 and candidate bits | Does not test RPM/speed/accelerator |
| State0, nonzero candidate; forward selected and speed strictly above positive threshold, or Reverse and speed strictly below negative threshold | Admit2 iff effective accelerator strictly above0.25 | Failed accelerator test retains candidate; no RPM alternative on this route |
| State0, other direction/speed; signed sampled RPM strictly above unsigned calibration halfword+234 | Write2 | Accelerator is irrelevant on this route |
| Same, RPM at/below threshold | Retain0, clear candidate to positive zero | Negative signed RPM does not become a large unsigned RPM |
| State2/3 | Retain state, prepare samples | Candidate does not veto this preparation |
| Other byte values | Retain byte; do not prepare | Not silently normalized into0/1/2/3 |

Native thresholds are original bits `0x4031C71D` / `0xC031C71D`, approximately
±2.77777791m/s. Equality takes the RPM route. Accelerator equality0.25 rejects
on the directional route. The typed models receive the original threshold bits,
not new constants written into gameplay.

For a resulting state2/3, save current engine rate at+1310, call the **original
001E6CA8** target helper, and save its result at+1314. This happens **every
preparation update**, not just upon entering a state. For ordinary state3,
effective accelerator becomes0 when target is strictly below saved engine,
otherwise1. Effective policies3/6 retain the prior accelerator instead.

Effective policy is0 when signed owner byte+136D equals1 **or** control-mode
byte+14B8 is nonzero; otherwise it is stored unsigned byte+13E5. This is not a
general rule that every non-player owner forces policy0. State initialization
may separately restrict stored policy for owners1/2.

The containing001E6EC8 clears both sample slots before calling admission. Whole
001E6D48 alone does **not** clear them when it does not sample. Its independent
oracle tests that distinction, including untouched padding and stack bytes.

### Synchronization — nonzero-state phase at001E7590

Let `E0/T0` be saved engine/target, `E/T` current engine/independently derived
target. For states2/3, evaluate in this order:

1. **Policies3/6 and candidate EE-equal exactly1:** write state1 and rewrite two
   axle rates and four wheel rates from engine/selected ratio and original axle
   coefficients. Division and multiplication retain EE behavior. Engine rate is
   not first snapped to `T`; inhibition is **not written12**. This skips ordinary
   crossing and both abort decisions. Original two-iteration rate-write loop and
   its scheduler polling remain original; the model is not its ABI replacement.
2. Otherwise, complete if `(E0 <= T0 && T <= E) || (T0 <= E0 && E <= T)`.
   Equality can complete. Write state1, engine=`T`, inhibition12. Non-exact-one
   policy3/6 values still use this **ordinary** crossing path.
3. If still3 and saved target `T0 <= converted idle`, abort to0. This tests the
   **saved target**, not the later target, and is not an elapsed-time timeout.
4. If still2 and processed brake **strictly above0.75**, abort to0 when either
   engine is strictly below converted idle+500 or speed is **strictly between**
   the original low-speed limits. Brake is required for **both** alternatives.
5. Otherwise retain the state, rate and inhibition.

Completion has priority over aborts. Abort does not clear selected ratio,
candidate or inhibition, and does not invoke state0's idle-floor integration in
this same call. State1 simply tracks `T`. Other nonzero state bytes retain their
state and existing engine rate before the common clamp.

After this phase, negative engine rate branches directly to positive zero;
otherwise a rate at/above the converted upper calibration+10 is limited to it.
This branch order is retained, not replaced by `std::clamp`. Original001E6D00
then updates sampled RPM, including its original integer/halfword quirks.

State0 instead calls original001E17F0 for effort and computes, in this exact EE
order, `engine + ((effort * coefficient(+2BC)) * timestep(+EC0))`, with an idle
lower bound. It bypasses the nonzero-state upper-clamp block in this function.
The free-integration model begins **after** the effort helper. It does not claim
to recover engine production, limiter, all scratch/FCR effects or that helper.

### Selection decision and commit —001E77F8 onward

| Dispatcher result / prior state | Immediate result |
| --- | --- |
| Full low64-bit register equals sign-extended−1 | No state or selected-ratio commit |
| Any accepted result while state0 | Commit low byte to ratio, retain0 |
| Accepted result while nonzero; full result0 or old ratio0 | Write2, commit ratio |
| Accepted result while nonzero; otherwise | Write3, commit ratio |

An accepted same-index forward request still chooses3. The caller compares the
full result before the leaf narrows it to a byte; e.g. a nonzero large result
whose low byte is0 is not automatically the Reverse-involving branch. Invalid
values are tested as original quirks, not newly advertised driver inputs.

**001E4E78 writes only+13BA.** It is not a state setter. Policy dispatch and
selection may reject before this phase. Existing Frozen MT selector/helper are
unchanged; original AT and other policy selectors are not newly recovered.

## 3. Timers, initialization and other readers

- `+13BE` is selector inhibition/rearm, not the age of state2/3. Ordinary crossing
  writes12 before selection in the same update. The later applicable selector
  can immediately decrement it; held-input rearm can retain1. Existing MT tests
  and exact native traces cover this composition. Completion is not a new
  twelve-update engagement delay.
- Original AT additionally decrements halfword+13E6, and certain request routes
  write240. Its ordinary automatic-decision route requires state1, but earlier
  request/override routes can bypass that state gate. This is not a universal
  prohibition on changing selection outside1. These AT timer/selector mechanics
  are mapped static dependencies, not a new clean AT implementation.
- Reset001DD5F0 writes state0 (001DD80C), candidate0 and engine0, selects1 through
  the ratio leaf, and performs many other resets. Its inhibition initialization
  depends on owner/control/policy. It is **not** emulated by just calling `admit`.
- Moving-start/setup001DD8A8 derives an initial ratio/rate, writes state1 at
  001DDA3C, candidate1 and original wheel/axle rates. These are entry-condition
  writers, not ordinary transitions. Both initialization bodies remain original.
- Original candidate writer001E4180 reads state and applies different idle/brake/
  handbrake predicates for0 versus nonzero states. Policy3 inverse-brake and
  policy6 raw-command vetoes remain distinct. Alternate001E35D8 processing reads
  state and has candidate-zero paths. No clean input/candidate writer is added.
-001E5998's differential response helper distinguishes state0, state2 and the
  packed state1/Reverse combination, together with calibration, brake and rate
  predicates.001E5B98 also rereads state in downstream rate/force paths. State0's
  zero engine term does not zero every differential/reaction/braking calculation.
-001DFB58 uses nonzero state with an additional enable byte in a derived response
  calculation.001DFC60 uses factor1 for state1,0.5 otherwise while updating
  filtered byte parameters.00192A58 exports a boolean for state exactly1 into an
  output record. These are static auxiliary consumers, not extra state writers;
  their device/UI meaning and full live branch coverage are not promoted.

The audit searches both car-relative+13BB and member-relative+437, and inspects
packed overlapping stores. A raw executable-word scan is an **untyped candidate
search**, not proof that every word is an instruction or every base is a car.
The packed+434 writers in001FB140/001FBF50/001FD720 are reached through the
inspected0x4F0-stride scene-object family, not demonstrated extra car transition
writers; this is qualification of those call paths, not a universal alias theorem.
Stack-relative+430 saves likewise are not car writes. Generic bulk copies,
other aliases/displacements, undiscovered indirect paths and all whole-program
initialization lifetimes are **not exhaustively ruled out**.

## 4. What is actually validated

### Independent generated-original tests

The baseline unit is renamed only for exported/self-call/entry-array isolation;
reversing the names must reproduce the exact original text. It is private and
never used as public recovered source. It supplies all expected CPU/RAM results.

- **156,464 whole-admission complete-CPU/exact-cost comparisons**, including all
  scratch/upper lanes, FCR, PC/RA/SP and untouched state. Complete car/padding and
 128-byte stack spans each case; **306 whole32MiB comparisons**. Costs22–103.
- All65,536 sampled RPM bit patterns, all256 state/policy bytes, all256 owner
  bytes with control modes0/1/255, maximum/invalid selected bytes, drivetrain
  branches, signed zeros/denormals/extremes/exponent255, strict threshold
  neighbors,10,000 randomized contexts, negative budgets and bounded depth.
- **12 fullCPU+32MiB mutation-free rejections** for default OFF, pointer/
  stack/GP/alignment/depth/budget constraints. The public synthetic test separately
  rejects a non-original profile without artifacts. Missing/changed required
  private evidence also fails strict verification; no expected hash is rewritten.
- **458,752 selection projections** against existing original interior entry154:
  every state/old-selection byte pair and seven full-width dispatcher values.
- **149,600 synchronization/clamp projections** against original entry150,
  including crossing direction/equality, priority, abort boundaries, policies3/6
  exact-one/non-one, invalid states and original axle/four-wheel special effects.
- **20,000 free-integration projections** against original entry149 after effort.
  Total semantic projections **628,352**. These deliberately do **not** assert
  complete CPU/ABI/cost equivalence of the engine or commit model.

The admission wrapper keeps original target001E6CA8 and its original drivetrain
helper001E6C28. Normal-RAM object and disjoint96-byte stack span, full pointers,
alignment, original GP, instruction/helper/table fingerprints, safe signed budget
and bounded call depth are checked **before mutation**. Its admitted original
call graph has no backward scheduler poll. Negative budgets are tested without
inventing scheduling; unsupported depth/addresses remain original fallback.
The partial field layout has explicit padding and offset/size assertions.

### Fresh original-native evidence

**49 accepted gameplay runs /19,278 updates**, seven scenarios × seven modes:
untouched original, instrumented buildOFF, runtimeOFF trace-only, admission-only,
unchanged Frozen selector/helper-only, both, and both-repeat. Exact final native-v3
snapshots, entire36MiB EE/IOP/SPU dumps and nonempty captures match seven ways.
Six-way complete CPU/cost traces match. Only the earlier Frozen selector/helper
**trace copy's entryPC** transport normalization is retained, with raw transport
PC recorded; actual outgoing/shadow CPU and all RAM comparisons have no masking.

| Scenario | Updates/run | Meaningful native paths |
| --- | ---: | --- |
| MT cycle |600|0→2,2/1→3,3→1; **3→0 low-target abort4522/4584** |
| Moving forward-selected coast + accelerator |351|State0 persistence; directional admission5403;2→1 at5410 |
| Independently braked coast + accelerator |351|RPM admission5418;2→1 at5570;1→0 at5571; re-admission5572 |
| Same original braked source + ordinary brake5424:8 |351|**2→0 brake abort5425**, re-admission5433,2→1 at5605 |
| Original MT Reverse schedule |600|Reverse-involving commits and negative speed-helper route |
| Original positive-helper continuation |201|Positive speed search and unchanged Frozen helper interaction |
| Original AT control |300|Common admission/engine model under policy0; original automatic selections; no MT/helper entries |

The Reverse and positive-helper cases use independently prepared **original** snapshots and
original button schedules. The brake-abort gesture is new normal native input,
not guest-state manufacture. No original state/card, policy, configuration,
calibration, parts or credits were edited. New output cards were not created.
The ALTEZZA owner0 context is qualified: effective policy1 for MT and0 for AT;
no all-car claim.

Activated modes perform **8,262 actual admission substitutions and8,262
real-entry fullCPU+32MiB/exact-cost admission shadows**, plus **7,362 selector
substitutions/shadows and6 helper substitutions/shadows**, all zero fallback.
All six instrumented modes also check the semantic models at actual admission,
engine and selection boundaries,2,754 checks per stage per mode. A shadow is not
counted as an actual substitution. Canonical original runs perform neither.
Native negative and positive helper entries are real; native multi-candidate
helper traversal remains the prior differential-only limitation.

These runs extend the earlier engagement fixture population: its statement that
no post-drive abort was observed was true for that finite set, **not a proof that
aborts cannot happen**. Both are now independently reached without forcing state.
Private side-by-side captures were reviewed; exact comparison is the primary gate.

## 5. Reproduction, evidence and honest stop

```sh
just check
just test
just docs-build
just --justfile transmission-state.just check
just --justfile transmission-state.just test
just --justfile transmission-state.just verify-state /explicit/repository/root
# Only explicitly requested disposable builds; fresh output directories required:
python3 scripts/validate_gt3_transmission_state.py build BASELINE NEW_ORACLE
python3 scripts/validate_gt3_transmission_state.py native BASELINE NEW_ORACLE NEW_OFF
python3 scripts/validate_gt3_transmission_state.py native BASELINE NEW_ORACLE NEW_ON --enable-clean
```

`--gt3-clean-admission` is independent and defaultOFF; buildOFF rejects it before
gameplay. Only the whole admission entry is hooked, including direct generated
calls. Original interior continuations stay original. No canonical source or
build file is modified. Models have **no mutation/install API**.

Fresh builds reproduce the executed oracle/admission/model/Frozen/native objects
and ON/OFF hosts byte-for-byte. The later partial-layout declaration changes no
executable bytes; exact evaluated earlier source/header versions are retained,
not substituted silently during identity checks. Strict verification pins every
new private artifact, checks these reproduction bindings and native reductions,
re-executes the independent new oracle and unchanged inherited Frozen proofs.
It does **not** launch another gameplay matrix. Original files, raw analysis,
generated code, executable overlays, captures and snapshots stay ignored under
`local/transmission-state-v1/` and immutable parents.

No oracle/gameplay mismatch occurred. Retained non-proof diagnostic notes include a
reader-index null-procedure handling error, an initial conservative overlap scan
with mistaken FP-store widths (corrected in a **new** final candidate inventory),
and unavailable Python image support (existing ImageMagick used instead). Earlier
oracle iterations are retained separately, not overwritten as final runs.

Representative static evidence: admission
`ev_04f7f4fa255cfd7b17b2382c2b8f6607b46001126f3763211ecbfebc96c025cf`,
engine `ev_ba862eb7a3b5186afe285c12642ec3333b3edf31134220656870980836379388`,
commit `ev_ad6ff9600494d25109501f34eb4acb29d1d1310a63ef420b3789449066d27014`,
reset `ev_298b7ddf5a8c401a87d925db782ec4251ac5bbbc89c59ce20a1dd5c886cb93a6`,
moving start `ev_0b08f844316e8ee6a68867bf1f4ff7a5ec807fd6661539a06ddd633a60288bac`.
The private index preserves authenticated inherited and new reader evidence,
including provider limitations; static instructions do not imply live execution.

**Stop at this bounded result.** Named normal-update decisions are mapped and
tested, admission is recovered with bounded ABI/live proof, and feasible ordinary
native transition paths now include both aborts. Specific remaining evidence gates:

- Independently reached policies2–6/alternate owners, including original fractional
  policy3 and exact-one policy3/6 rate rewriting. Synthetic proof is not native
  player/device reachability; no legitimate fixture was established here.
- Nonzero original configuration205→+2A4 and a matched installed-clutch fixture.
  The existing converter writes204, not205. Observed zero state3 transfer is not
  universal; neither missing producer nor hypothetical settings are invented.
- Whole engine/commit ABI, helper/unwind/scheduler and dynamic-cost recovery;
  decision projections are insufficient to substitute those whole routines.
- Full initialization/reset replacement and exhaustive bulk-copy/alias/indirect
  writer closure. Mapped setup bodies remain original.
- All-car/mode/thread/long-session/device/physical-console proof and complete
  downstream force/engine-production recovery remain outside the established slice.

These limitations prevent a comprehensive transmission replacement claim. They do
not invalidate the tested decision mapping, and they are not permission to force
new policy bytes or change parts/settings to manufacture evidence. No further
recovery, feature, canonical installation or commit/push follows automatically.
