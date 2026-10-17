:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# Virtual clutch / H-pattern v1 — stopped intervention-boundary audit

## Status

**Controller NOT implemented.** This is a bounded feasibility result, not feature
acceptance, a replacement, or a claim that safe controlled integration is impossible.
The requested unconditional clutch behavior needs a deliberate transition-policy
extension. Whether routing execution to original state stores is permitted by the
request's **no direct state forcing** restriction needs clarification before doing
that work. The audit does not silently treat an original instruction as a safe new
API in arbitrary contexts.

Source context: `bea85fcc9bf76f55b1c28b3997d3b438b72388cb`. Existing tracked files,
Frozen authorities/implementations, canonical host/runtime/build, game files and
calibration remain unchanged. No controller skeleton, runtime switch, physical
adapter, Neutral ratio, HUD change, canonical installation, commit or push.

## 1. The established original entry points are insufficient by themselves

The existing [state recovery](../transmission/state-transitions-v1.md) establishes this order:

```text
candidate/control -> admission/preparation -> drive -> engine/synchronization
                 -> selection decision -> ratio-only commit
```

| Established mechanism | Actual behavior | Why it does not meet unconditional v1 by itself |
| --- | --- | --- |
| Candidate zero at001E6D48 | State1 becomes0; state2/3 retain state and prepare rates | Cannot disconnect an already synchronizing vehicle before drive |
| Candidate nonzero from0 | Directional-speed/accelerator or sampled-RPM admission tests | Does not guarantee synchronization on release |
| Original engine aborts | Conditional state2 brake/low-engine-or-speed abort or state3 low-target abort, after completion tests | Conditions are not universally true; run **after drive**; completion has priority |
|001E4E78 ratio leaf | Writes selected ratio only | Does not disengage or initiate synchronization |
|001E77F8 selection phase | Accepted nonzero state goes to2/3; accepted free state remains0 | Does not provide nonzero→0 disengagement |
| Original reset / moving initialization | Broad reset to0 / initial setup to1 with other control/rate changes | Not a clutch API; unrelated resets or wheel-rate writes would violate the feature boundary |

This is scoped to the inspected/recovered entry points, **not** a whole-program
proof that no other original interface can exist.

Even granting an adapter control over candidate zero is insufficient. The audit
therefore does not implement a processed `+139C` override and call it a clutch.
Using handbrake/brake effects to solicit an abort would also add unwanted braking,
would not guarantee a pre-drive disconnect, and is not a solution. State3's zero
transfer in retained zero-calibration fixtures is not universal free-engine behavior.
Changing its calibration or forcing a policy/configuration is not an alternative.

## 2. New independent original-only probes

A standalone synthetic test links **unaltered generated-original code** and the
identity-verified original archives. It does not link a recovered decision model as
its expected result and does not install an overlay. Fixture writes occur only in
a synthetic test process, not in native gameplay or original saves/configurations.

**54 original-only probes**, each with a whole32MiB mutation-surface check:

-18 whole admission calls, including states0–3, zero/nonzero candidate, Reverse
 and forward-selected contexts, low RPM, exact RPM/accelerator boundaries and
 ordinary admission positive controls.
-4 engine **interior semantic projections**: state2/3 with candidate zero remain
 synchronizing under non-crossing/no-abort conditions; positive controls exercise
 the two conditional aborts. These are **not whole-engine ABI comparisons**.
-16 original ratio-leaf calls: ratios0/1/3/6 in states0–3, only ratio byte changes.
-16 original selection-phase projections: rejected/Reverse/forward results across
 states0–3. No claim to replace the whole dispatcher or selector.

Key observed counterexamples:

- State2 + candidate0 →2; state3 + candidate0 →3 in admission.
- State0, forward1, candidate1, speed0, sampled RPM800, threshold2500 →0 with
 candidate cleared, at accelerator0,0.25 **and1**.
- State0, forward1, speed8m/s, RPM6000, candidate1, accelerator0 or0.25 →0.
 Accelerator strictly above0.25 admits2 on that route; RPM2501 admits2 on the
 low-speed route. Positive controls prevent mistaking an inert fixture for proof.

The executable was rebuilt in a fresh directory and reproduced **byte-for-byte**;
all54 probe outputs reproduced exactly. No test failure, comparison relaxation,
original body edit or expected-hash rewrite occurred.

## 3. Original native evidence, correctly qualified

Strict unchanged state proof verification authenticates the earlier evidence.
A new read-only reduction of its inherited engagement traces rederives:

-4,508 original drive stages;
-**77 state2 stages with candidate zero and a nonzero engine-directed term**.

Nonzero includes engine braking, not necessarily positive acceleration. Neither
wheel force nor vehicle acceleration is being substituted for this engine term.
This contradicts a universal candidate-zero-disconnect assumption in actual
original gameplay, not just a synthetic fixture.

**Zero new native gameplay runs** were launched for this audit. These are retained
original observations, not virtual-clutch input, feature-ON execution, physical
reachability or new substitutions. The previous state-recovery49-run matrix and
Frozen native proofs remain unchanged; strict verification does not relaunch them.

Static basis is the authenticated REA evidence cited by the state-recovery report:
admission `ev_04f7f4fa255cfd7b17b2382c2b8f6607b46001126f3763211ecbfebc96c025cf`,
engine `ev_ba862eb7a3b5186afe285c12642ec3333b3edf31134220656870980836379388`,
selection `ev_ad6ff9600494d25109501f34eb4acb29d1d1310a63ef420b3789449066d27014`.
Same original ELF SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
Existing exports were reused; no new static analysis or exhaustive alias closure
is claimed.

## 4. Smallest viable next design — requires clarification, not implemented

The candidate is an isolated **virtual transition-policy shim**, not a new clutch
physics model:

1. Before drive, clutch/Neutral chooses an original state0-write path even from
 states2/3. This deliberately adds unconditional cancellation of synchronization.
2. Released clutch plus valid selected gear chooses the original state2-write and
 rate-sampling/preparation path irrespective of normal admission thresholds.
 It must not set1 or bypass the subsequent original synchronization calculations,
 crossing/completion/abort behavior, engine integration or drivetrain processing.
3. While virtual authority is active, suppress competing original selector results;
 validate requested index against original maximum `car+20A`, then use original
 ratio-only commit while disengaged. Neutral stays host-owned, never index0 or−1.
4. Prove the new continuation-entry/frame/register/FCR/delay-slot/budget/helper/
 scheduling contracts before any substitution. Original interior labels are not
 automatically callable functions. Direct generated calls must also reach gates.

Although this could avoid host code directly storing a state byte, selecting the
original store using a new host predicate is still a **new transition policy**.
It is not recovered original input behavior, nor has this audit established its
ABI/live safety. It must not be used merely as a disguised state-write shortcut.

**Owner question:** Is that narrowly scoped policy override permitted—especially
pre-drive2/3→0 cancellation and unconditional valid-gear0→2 through guarded original
write/preparation paths—under the no-state-forcing restriction? If yes, next prove
those contracts, then implement/test the controller. If no, the original-input-only
alternative must relax unconditional disengagement and release admission; it does
**not** satisfy the requested v1. Waiting for a conditional post-drive abort is not
an equivalent fallback.

A future host contract should separate connection/enabled state, binary clutch and
`Reverse | Neutral | forward index`; do not infer all cars have six gears. Proposed
minimal policies are: reject unavailable gears without a commit; reject engaged,
unclutched ratio changes rather than invent damage; allow Neutral immediately;
apply valid disengaged ratio changes before starting synchronization; avoid
restarting existing synchronization on repeated released samples. Deactivation
and disconnection require an explicit handoff policy and tests, not hidden
restoration of an old ratio/state or an assumed safe automatic engagement.
These are proposals, **not implemented behavior or a supported input API**.

## 5. Reproduction and acceptance status

New ignored proof: `local/virtual-transmission-v1/`,16 sealed members; manifest SHA-256
`c3946578c8da6de049b759d02dbf6c5190ace865d382f7dcb09bd6c388925526`.
It retains the plan, original-only synthetic test, exact build commands/identities,
accepted builds/logs, static reuse receipt, native reduction, tracked-file snapshot
and strict verifier. No originals, generated bodies, executables or captures are
public documentation assets.

```sh
# A fresh output directory is mandatory. This builds ONLY an original-only probe.
python3 local/virtual-transmission-v1/reproduce.py NEW_OUTPUT_DIRECTORY
python3 local/virtual-transmission-v1/verify.py /explicit/repository/root \
  c3946578c8da6de049b759d02dbf6c5190ace865d382f7dcb09bd6c388925526
just --justfile transmission-state.just verify-state /explicit/repository/root
just check
just test
just docs-build
just audit
```

Strict boundary verification checks every sealed member, all prior tracked bytes,
both executable/source identities, reexecutes54 probes and rederives77 retained
native counterexamples; it delegates unchanged state/inherited strict verification.
Missing/changed evidence fails, not silently skips. Checkpoint logs and read-only
fault results stay separately under `local/virtual-transmission-checkpoint-v1/`.

| Acceptance item | Result |
| --- | --- |
| Existing source/Frozen/canonical preservation | Unchanged bytes; unchanged strict proof reverified |
| Original-only boundary experiment |54 probes; independently rebuilt executable identical |
| Original native counterexample audit |77 retained counterexamples; no new gameplay |
| Working controller and host input contract | **NOT IMPLEMENTED** |
| New default-OFF build/runtime gates | **NOT IMPLEMENTED; no integration exists** |
| New original-vs-controller-OFF native comparison | **NOT RUN**, not inferred from unchanged source |
| Feature-ON clutch/Neutral/H-pattern/edge/loss/long-run tests | **NOT RUN** |
| Whole-engine/commit ABI or physical-device proof | **NOT CLAIMED** |

Stop at the intervention/permission boundary. No further recovery, invented
physics, controller installation or publication is implied by this audit.
