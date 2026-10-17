:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# MT selector recovery v1

## Verdict and authority

**One whole function, bounded validation-only recovery:** `001E5458–001E553B`,
entry `001E5458`. The evaluated implementation was
`host/gt3_clean_transmission.cpp`,
with partial layout assertions in `host/gt3_clean_transmission.hpp`.
`decomp/gt3/transmission.json` is its historical source-pinned authority.
The maintained sources now live in `src/gt3/gameplay/transmission/`; see
[current architecture](../../architecture/index.md) for ownership and product exclusion.

The cycle is **Identify → Trace → Recover → Differential Validate → Opt-In
Integrate → Live Validate → Freeze**, for this boundary only. Frozen means the
exact evaluated **disposable validation overlay**, not canonical installation,
complete transmission recovery, or a physical-controller claim. Canonical
`ps2run`, earlier Frozen authorities, CMake and root build recipes are unchanged.
Both new build and runtime gates default **OFF**. Unsupported contexts execute
original generated code. There is no transmission input adapter.

At the evaluated checkpoint, starting HEAD was
`edc65a105ba682449391a2d62c513af8b9005e53`; the iteration was an
**uncommitted additive source overlay**, identified by individual hashes, not a
claim that that HEAD already contained the recovery. No commit or push was made.

The [power-transfer investigation](power-transfer.md) remains the
broader model and its comprehensive recovery gates remain open. This deliberately
smaller selection decision neither depends on inventing those missing mechanisms
nor closes them. Start with the [conceptual map](producer-consumer-map.md) for the
producer/consumer chain. The later [speed-helper recovery](speed-search-v1.md)
has its **own** selector/helper composition proof: it does not rewrite this
checkpoint's generated-helper dependency or its counts. The later
[state report](state-transitions-v1.md) separately distinguishes whole-admission
recovery from partial engine/commit models.

## 1. Identify and trace before coding

The private pre-implementation plan records the alternatives, boundary, dependency
closure, outgoing ABI, guards and tests. Fresh static dossiers rechecked the MT
entry, its one speed-selection callee and policy dispatcher against the immutable
USA v1.10 original. Original ELF SHA-256:
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.

Why this function:

- It makes a meaningful, bounded selection/rearm decision with legitimate original
  policy-1 player fixtures already available.
- `001E4E78` alone is only a small selection store, not a useful first decision.
- AT `001E4FF8` and dispatcher `001E5690` would widen policy dependencies.
- Selectors `001E5540/001E5600` depend on configurations not independently reached.
- Admission, synchronization and power-transfer functions would prematurely pull
  in the unresolved owner/calibration/state branches.
- The EE floating-point speed search `001E4E80` can remain an explicit original
  dependency rather than being casually modernized along with selection.

### Recovery/dependency map

```text
ORIGINAL command construction / manual processing / request delivery
  -> ORIGINAL 001E77E0: selection orchestration
     -> ORIGINAL 001E5690: owner/mode/suppression/effective-policy dispatch
        -> CLEAN 001E5458..001E553B: MT selection and inhibition/rearm
           -> ORIGINAL 001E4E80: speed-based forward-index search, if required
     -> ORIGINAL state write at 001E77E0, if a selection was accepted
     -> ORIGINAL 001E4E78: commit selected index
  -> ORIGINAL admission, engine, driveline, differential, wheels and chassis
     on their established update schedule
```

The final line means those systems remain original, **not** that they all execute
following selection in the same update. In the normal update, drive and engine
synchronization precede `001E77E0`; see the power-transfer report's ordering.
Direct calls within the generated unit are covered by a whole-function **entry
label** overlay, not merely a dispatch-table hook. This is not an interior-tail
recovery and has no invented resume address.

## 2. Bottom-up: exact small contract

| Input/read | Role |
|---|---|
| `a0` | Original car pointer |
| `a1+0/+1` | Signed auxiliary request / signed relative request; not absolute gear commands |
| `car+0x13BA`, unsigned byte | Current selected ratio index |
| `car+0x13BE`, unsigned byte | Inhibition/rearm countdown |
| `car+0x20A`, unsigned byte | Configured maximum selection/search index |
| `car+0x13AC`, EE bit pattern | Processed accelerator for the Reverse-to-forward route |
| `car+0x140C`, EE bit pattern | Speed supplied to the original search helper |
| Helper's original GP constant, RPM calibration and ratio array | Read only by retained `001E4E80`; never replaced with a host table |

The result is original **`v0=-1` for no accepted selection**, or an accepted
unsigned-byte-domain ratio index. **0 is Reverse, not Neutral.** This function
does not commit the selected index, change transition state, or compute drive.

Decisions in priority order:

1. A nonzero auxiliary request returns Reverse if the current index is nonzero;
   if already Reverse it returns no change. This priority bypasses the countdown.
2. While Reverse is selected and the original accelerator comparison is nonzero,
   call original `001E4E80` using the original speed. Convert its returned zero to
   forward index 1. This path also precedes ordinary rearm handling.
3. A nonzero inhibition count decrements modulo the byte store. If it reaches
   zero while a relative request is still held, rearm it to 1. Return no change.
4. With count zero, a positive signed request increments only below the configured
   maximum. A negative signed request decrements only from index 2 or higher.
   Either accepted relative selection writes inhibition 1. Otherwise no change.

Invalid byte indices and zero maximum values are **not repaired or clamped**.
The original helper-zero-to-one quirk is preserved even for a synthetic zero
maximum. Requests use signedness, not an assumed enum restricted to −1/0/+1.

### CPU, RAM, arithmetic and scheduling obligations

The bridge preserves the **complete outgoing CPU**, not just the selection:

- Original scratch `v0/v1/a0/a1/a2/a3`, their path-dependent values, and unchanged
  upper 128-bit-register lanes; no convenient host calling-convention shortcut.
- The original 16-byte stack frame, incoming RA low64 store at `SP-16`, RA/SP
  restoration, and return PC from original RA low32.
- The original EE accelerator comparison's FPU condition effect. The generated
  speed helper retains its FP registers, scratch registers, rate conversion,
  division, signed-word conversion and comparison semantics.
- All other CPU fields, FCR bits, HI/LO/SA/base and RAM remain exact. Normal body
  RAM writes are only the saved-RA slot and, on applicable paths, `car+0x13BE`.
- Original delay-slot and branch-likely effects and **exact dynamic instruction
  budget**. Observed isolated costs are **13–4,103**, including the longest tested
  254-iteration original search. Existing `2e-6` tolerance is unchanged; this
  recovery's comparisons use exact bit equality.

EE bit-pattern operations are used instead of host floating-point arithmetic.
Signed zero, denormal, infinity and NaN patterns are independently compared to
original execution. The only recovered decision/body is the MT function; the
retained helper is not claimed clean-recovered merely because it is called.

### Guard and fallback contract

Before any CPU/RAM mutation: require original body/helper fingerprints, matching
GP, full64 pointer representations, bounded ordinary RAM, aligned car/stack,
nonoverlapping stack/car/requests, and either the native `car+0x1304` request pair
or a disjoint pair. The low protected region includes the original loaded image
and GP constants; aliases into it are rejected. Partial types do not authorize
bulk reads/writes of unknown padding.

The generated helper route additionally requires depth below the native limit
and a conservative remaining budget of `16*maximum+64`, sufficient for the entire
bounded original loop. An unsupported scheduling context falls back **before
mutation**. Non-helper negative-budget paths have no backward poll and are tested
including depth-limit contexts. Near signed-budget overflow is rejected. No
canonical dispatcher, scheduler or fallback behavior is changed.

These are bounded structural guards, not a promise of all-car/all-thread live
coverage. Validation uses the existing single-thread deterministic native setup.

## 3. Top-down: what changed in gameplay architecture

Only the MT decision body can be replaced in a separately compiled disposable
unit. Its caller still chooses the effective policy, and its consumer still
writes transition state and commits the index. AT and policies 2–6 remain original.
The runtime switch is `--gt3-clean-transmission`; a build without the explicit
build option rejects that switch before running. Trace-only and build-OFF paths
execute original bodies. The canonical launcher has no new switch or hook.

Nothing supplies a new driver command. Tests use original native `--press`
schedules from unchanged original snapshots, not a virtual shifter, forced policy
or edited calibration. No parts, credits, settings, saves or original inputs were
modified. Synthetic isolated tests mutate **their own fixture RAM**, not live play.

A changed ratio can still coexist with state 0. State 2 can still transfer effort
with coupling candidate zero. State 3 still uses the original calibration-derived
term. `car+0x139C` remains **coupling candidate**, not clutch position. No Neutral
sentinel, H-pattern mapping or timing/torque intervention has been introduced.

## 4. Validation actually executed

### Independent original and build identities

The oracle is identity-checked `generated-original/unit_0039.cpp` from the retained
baseline, source context `82987dec7a71d76414adfff8663da5494a280938`, **not a new
whole-game translation at documentation HEAD**. Only its exported unit symbol,
self-call binding and entry-array symbol are renamed to coexist with the overlay;
reversing those renames must reproduce the exact original file. No original
instruction, helper body, comparison or budget is replaced by clean code.

Original generated hashes, input/executable identities and linked runtime/source
hashes are checked. The game/runtime archive hashes reconcile to independent
immutable parent proof. Archive-preflight fresh builds reproduce the isolated
oracle, integrated wrapper, build-ON host and build-OFF host **byte for byte**.
Native records remain bound to their actually executed binary paths/hashes; they
are not relabeled as launches of the later reproducibility builds. The unused
baseline recovered-source archive is separately identified, never used as oracle.

| Layer | Fresh result | What it proves / does not prove |
|---|---|---|
| Isolated generated vs clean | **663,959** cases, complete CPU and exact cost each; complete car/padding and stack every case; **649** whole32MiB comparisons plus cumulative out-of-contract mutation check | Selection/body ABI across exhaustive byte axes and targeted FP/helper/scheduling edges; not full32MiB at every exhaustive case |
| Rejection contract | **20** fallback cases, complete CPU+32MiB unchanged | Disabled/profile/pointer/alias/depth/budget rejection; not live coverage of every rejection |
| Integrated original `77E0→5690→clean5458→original4E78` | **1,008** complete CPU+32MiB/cost comparisons; **1,008** real replacements, zero fallback | States0–3, indices0–6, rearm and requests; original state/commit consumer preserved |
| Accepted native-v3 matrix | **15** runs, **7,500** total updates | Two MT scenarios and an AT noninterference control, five modes each; not all cars/modes |
| Real-entry live shadow | **2,400** complete CPU+32MiB/exact-budget comparisons | Original entry CPU/RAM on actual clean/repeat paths, actual call depth; not fabricated fixture entries |
| Actual live substitution | **2,400**, zero fallback; **2** retained generated speed-helper calls | Clean body actually installed/executed in bounded MT coverage, not merely linked |
| Whole native parity | Exact final snapshots, complete36MiB EE/IOP/SPU dumps, capture sets and repeated entry/exit traces | End-to-end original/disabled/trace-only/clean/repeat agreement in these runs |

Each scenario has an **untouched original**, build-OFF trace, build-ON/runtime-OFF
trace, clean+shadow, and clean+shadow repeat. MT cycle uses 600 updates with native
up/down requests; MT Reverse uses 600 with original brake/auxiliary/accelerator
requests. AT uses 300 updates and enters the MT body zero times. The real MT entries
are owner0, effective/stored policy1, mode0, no suppression, car `01FBB7BC`, stack
`0049AF30`, return `001E5730`. Entry/exit pairing qualifies the lifetime. The
function does not commit index/state between those two sites. The cycle observes
10 accepted selections and all states0–3; Reverse observes two accepted selections,
160 auxiliary-held entries and one original speed call per clean/repeat run.
Those are finite original-context observations, not new all-state reachability
claims for other cars or policies.

Shadow original and clean executions use copies of the **actual entry CPU** and
entire actual RAM. Their full results are compared; all pre-entry RAM is restored
before actual substitution proceeds. Shadow counters are separated from actual
replacement counters. The original native control has neither probe nor clean
execution. Captures were privately reviewed; raw captures are not published.

### Retained failures and corrections

- First isolated link failed on a duplicated generated entry-array symbol. Its
  attempt/log is retained; the oracle now renames that symbol as well as the unit.
- The first differential caught my incorrect maximum offset `+0x210`. Actual
  original addressing resolves to **`+0x20A`**. Failed source, fixture and log are
  retained. Corrected source/fixture reran the full differential; no expectation
  or comparison was weakened.
- The first live-host compile used an unavailable frame symbol; the failed source
  and log remain, followed by a separate corrected build.
- The first clean native launch stopped on guard rejection, not CPU mismatch:
  the protected-region guard incorrectly included the real `0049AF30` stack.
  Original ELF loaded end is `003531E3`. The corrected guard protects the actual
  low-image/constant region, and native-stack plus budget-boundary differentials
  were added before new isolated/integrated builds and fresh native attempts.
- The initial helper budget guard was unnecessarily 10,000; it now derives the
  conservative complete-loop bound from the original byte maximum. Original
  preemption is not suppressed; unsupported contexts still fall back untouched.
- A completed 100-update AT control produced **no scheduled capture**. It is
  excluded, not accepted on dump equality alone. A new 300-update five-way AT
  control supplies the required capture with all comparisons intact.

There were **24 attempted native processes**:15 accepted,8 completed exclusions
(the initial three original/trace controls and five short AT runs), and one aborted
guard attempt. All remain separate. Missing optional-path lookups and diagnostic
errors are also recorded in the private ledger, not silently treated as absence.

Final raw parent verification also rejected three legitimately updated public
files: handoff, transmission navigation and sidebar. Their **exact `edc65a1`
versions**, independently matching the old manifest pins, are preserved privately.
The new verifier explicitly resolves only those three historical documentation
reads while separately checking the current files. The raw failure stays retained;
no old manifest, expectation, runtime source or game evidence was rewritten or
skipped. Calling the raw parent verifier on current documentation still rejects;
the successful result is specifically a **version-qualified parent verification**.

## 5. Junior-developer explanation

Think of this function as a tiny clerk, not the gearbox:

1. It reads the driver's already-processed requests and the currently selected
   index. It can answer “choose this index” or “no change.”
2. A small counter prevents held inputs from generating uncontrolled repeated
   changes. Reverse has its original special priority and forward-return search.
3. Another original function commits that answer. Other original functions decide
   when engine and wheels synchronize or transfer effort.
4. The C++ also has to leave the old CPU's scratch registers, stack and time budget
   exactly as the old machine code did. A correct-looking gear number alone would
   not be enough: later generated code can observe those other effects.
5. We ran the original and the new body on the same inputs, then compared those
   effects. Only after that did a separately gated build substitute the new body
   in original gameplay, with untouched-original and repeat controls.

Calling this a clutch or a whole manual transmission would be misleading. It is
one small decision inside a much larger original system.

## 6. Current checks and historical reproduction {#6-reproduce-preserve-stop}

Use the root workflow for public, artifact-free checks:

```bash
just check
just test
just docs-build
just verify-transmission "$PWD" # explicit retained historical proof, not current integration
```

The private command requires the retained evidence root and fails on missing/changed
required proof; it re-executes the independent isolated and wrapper oracles. It does
not launch the native matrix again. The former `transmission.just` and bespoke
builders are retired; exact evaluated versions remain in historical Git/private
contexts. See [workflow](../../developer-guide/workflow.md) and [testing](../../developer-guide/validation.md) for maintained
commands and the distinction between historical proof and current qualification.
The ignored `local/transmission-recovery-v1/` retains the pre-code plan, static
bundles, rejected attempts, complete builds, native runs, summary, manifests and
fail-closed read-fault tests. No assembly, decompiler output, original tables,
generated game code, binaries, snapshots or captures are public.

Fresh root/additive source tests, documentation/public audit, inherited immutable
proof verification and new strict proof are recorded separately. Earlier native
matrices are **not** claimed rerun merely because their verifiers passed.

**Historical next recommendation:** independently bound `001E4E80`, the generated
dependency in this proof. The later [speed-search report](speed-search-v1.md)
records that separate EE FP/table/loop/budget/preemption contract, original oracles
and bounded actual-context proof. It is not implicit in this selector result.
AT, owner policies2–6, clutch-parts/config205 and comprehensive engagement/wheel-force
recovery remain separate scopes, not work authorized by this page.

**Stop after this iteration.** No canonical installation, physical integration,
new shifter/clutch/Neutral API, adjacent Frozen modification or commit/push.
