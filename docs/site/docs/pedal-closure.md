---
title: Pedal v1 — observed-context admission closure
---

## Decision and boundary

**Re-frozen, validation-only; stop here.** The unchanged pedal body is equivalent
at every entry in the retained representative player-driving survey, including
Time Trial, Free Run and License B-1 with command `0049AF40`. The old
`0049AF50` exception was an overly specific address assumption, not a semantic
difference. It has been replaced by bounded manual-activation frame checks.

Authority: [`decomp/gt3/pedal-closure.json`](pathname:///knowledge/pedal-closure.json).
The original [Frozen checkpoint](pedal-v1.md), [stopped survey](pedal-profiles.md)
and [read-only admission audit](pedal-admission-49af40.md) remain separate,
immutable historical authorities. Their failures, source hashes and zero-replacement
runs were **not rewritten as successes**. Explicit historical source artifacts
preserve the original CPP and original audit analyzer; current hashes are pinned
separately. Missing/changed historical artifacts fail private verification.

Region remains **001E48FC–001E4BA7**, rejoin **001E4BA8**. No pedal arithmetic,
integer/EE FP behavior, response evaluation, downstream consumer, steering
algorithm, tolerance (`2e-6`), save-state format or original input was changed.
The complete semantic source prefix is byte-identical to the original Frozen body.
Canonical `ps2run` remains generated-only, byte-identical to the trusted baseline.
Both substitution gates remain default **OFF**, in disposable validation builds only.

## What actually owns the command

Original `001E4D38` reserves a 64-byte activation; its first 16 bytes are the
command, initialized by the existing producer. It is an activation-local object,
not an identified global BSS buffer. At pedal entry:

- `command = owner-entry SP − 64 = pedal-entry SP + 0xD0`;
- manual-wrapper and owner saved-register/return slots retain their original
  values, including returns `001E4CC8`, `001E4DFC`, `001F3B6C`;
- all **4,199** observed entries belong to exactly one running serialized native
  EE thread: thread 10, stack `[00493700,0049B700)`, size `0x8000`;
- the observer checks owner entry/unwind, hook call/return, no nested owner/hook,
  and ownership through the pedal join. Host Thread offsets/size/status are
  independently compiled against `runtime/src/kernel.cpp`, not guessed from RAM.

The upstream **16-byte displacement is explained**, not treated as another buffer.
Short, separately retained original diagnostic replays of Single Race, Time Trial,
Free Run and B-1 observe the same outer entry SP `0049B3B0`. Original mode callers
`00181E90` and `00187A50` reserve **96 versus 112 bytes**, respectively. Their calls
to common `001811B8` enter at `0049B350` versus `0049B340`, with returns
`00181EBC` versus `00187A9C`. The common descendant activation consequently places
the command at `0049AF50` versus `0049AF40`. Ghidra original-instruction evidence
corroborates those frame sizes. Raw stack scans alone were only candidate leads;
explicit entry probes establish these relationships.

Within one activation the two addresses are **not interchangeable**: one can be a
saved-register/return slot in the other context. Nothing was relocated, header-
spoofed or made to masquerade as the old allowed address.

Observed owner hooks were `001ED860` and, for Free Run, `001F14E8`. The former is
an original immediate-return leaf in the generated oracle and exact ELF word
check; Ghidra did not recognize/decode that leaf, an explicit retained limitation.
The latter conditionally obtains its existing object and forwards command **data**
through the original `002106B0` / `001F4998` path. The observed command activation
returns normally; no hook/owner reentry was encountered. This is not an exhaustive
inventory of arbitrary virtual targets or all possible allocations.

Importantly, equivalence does **not** depend on claiming universal pointer
non-escape: the replacement consumes the **actual**, unrelocated command, leaves
all command/stack/neighbor bytes unchanged, and establishes the identical complete
CPU, RAM and budget at the original join. Any retained alias therefore sees the
same bytes and pointer values. These compositional invariants, followed by exact
original continuation and guarded live replay, close the lifetime/alias issue for
the observed executions without inventing a whole-game no-retention theorem.

## Independent actual-context proof, before changing admission

An isolated shadow harness retained the **complete actual original entry CPU and
32 MiB RAM**. The generated body ran first. At its join, the harness independently
executed the unchanged Frozen semantic body on the saved entry, using the original
response evaluator, and checked:

1. complete `Cpu`, including high lanes, integer/FPU/status/scratch and exact budget;
2. the entire 32 MiB RAM against the generated result;
3. writes confined to the already recovered car/control bytes;
4. original command, all neighboring stack bytes and descriptors unchanged.

It restored original RAM, callback and diagnostic counts, so original execution
remained the continuation oracle. Semantic join PC normalization only removes the
known dispatcher transport-PC distinction, not any register or budget difference.
All **14 runs / 4,199 entries** pass, including **299 actual Time Trial entries**.
Native-pad costs are **63–72**, existing synthetic steering compatibility costs
**123–132**, within the audited **48–152** range. Original CPU/steering traces,
complete guest dumps and captures also match the retained original runs.

No absolute-pointer guard bypass was presented as an admitted live replacement.
The shadow entry is a clearly separated test-only call to the unchanged body.

## Narrow structural admission

Only the low-RAM command exception changed. Before mutation, the current guard
requires an aligned, bounded manual frame in the established low-RAM stack lane,
`command = SP + 0xD0`, exact saved car/register relationships and the three original
return-chain identities. The entire checked frame avoids the known descriptor
range; existing car/control/command/code/table alias, alignment, kind, depth,
budget, descriptor/helper/policy checks remain. A new fingerprint pins the original
manual/owner wrapper range `001E4CB0–001E4E77` as well.

This is **not** an address allowlist, a broad writable-BSS exemption, a runtime
thread-format dependency, or permission to reinterpret a neighboring saved slot.
Thread ownership was measured independently; the guard itself uses the proven
bounded caller-frame identities. Existing disjoint upper-RAM differential fixtures
remain supported; that is not an assertion of live coverage for every such pointer.
Malformed frames, changed return/register slots, wrong SP/command, out-of-range SP
and changed owner code are covered by mutation-free negative tests.

## Fresh guarded validation and regressions

- Exact original/clean region audit: **131,072 cases each**, all complete CPU/scratch,
  car/command/stack/descriptor and dynamic-budget checks; depths 0–191, budget/FP/
  integer/history/policy edges retained. Low-RAM fixtures now provide valid frames
  at **both** observed command positions; no assertion/tolerance was weakened.
- **24** fallback cases: zero CPU/32 MiB mutation, including structural negatives.
- Wrapper/policy/unchanged generated consumers: **2,160 cases / 6,480 complete
  CPU+32 MiB comparisons**; original-only **22** discovery fixtures retained.
- Full profile matrix: **68 new runs**, comprising 14 each build-OFF, runtime-
  disabled, trace-only and enabled, plus 12 native-pad canonical runs. **4,199
  actual guarded substitutions, zero accepted fallback**, exact CPU/steering
  traces, complete guest dumps and captures. Disabled is deliberately untraced;
  trace-only/default comparisons remain separate. Compatibility cases retain
  their existing synthetic steering label; exploratory axis0 cases do not become
  left-stick coverage.
- Fresh original Pedal v1 live suite: **19 runs / seven pairs / 2,100 substitutions**,
  zero accepted fallback, with unchanged canonical/build-OFF behavior.
- Fresh current-main baseline: normal-boot native-v3 fixture capture and all
  **28 baseline runs**, including pad and existing synthetic steering comparisons.
- Fresh complete native baseline regression driver and public source/type/schema/
  publication/docs gates; strict current, original Frozen, historical survey/audit,
  closure and historical-private verifiers all pass.

The original survey contains one exact descriptor family and five effective
processing classes `(2,0)`, `(2,1)`, `(3,0)`, `(4,0)`, `(4,1)`. Every one is covered.
Vehicles/modes include ALTEZZA AT/MT, Alfa 156 AT, MR-S AT, Time Trial preset MT
(exact model unverified), SLK230 Kompressor MT Free Run and New Beetle 2.0 B-1.
Native left stick/D-pad and compatibility steering remain distinct.

## Reproduction and stopping rule

```bash
# All output roots must be new; explicit private originals required.
bash scripts/build_gt3_pedal_closure.sh VERIFIED_ORIGINAL_PEDAL_BUILD NEW_SHADOW_BUILD
python3 scripts/validate_gt3_pedal_closure.py shadow --build NEW_SHADOW_BUILD --plan PRIVATE_PLAN --out NEW_SHADOW_RESULTS
bash scripts/build_gt3_pedals.sh ORIGINAL_INPUT_ROOT NEW_PEDAL_BUILD --enable-validation-pedal-substitution
python3 scripts/validate_gt3_pedal_closure.py live --build NEW_PEDAL_BUILD --plan PRIVATE_PLAN --out NEW_LIVE_RESULTS
just check
just test
just docs-build
just verify-pedal-closure "$PWD"
```

Private proof is under ignored `local/pedal-closure-v1/`; raw descriptors, traces,
assembly/decompiler output, binaries, states and captures are not public. Retained
failed diagnostic link and wrong-input-path attempts are explicitly separate from
accepted runs. The original survey/audit failures remain untouched.

**Discovery/admission is closed for the finite observed representative contexts,
not for all GT3 scenes, calibrations, virtual hooks, threads or long sessions.**
No unsupported observed class remains. Frame/profile-mismatching contexts still
fall back. The structural guard is not a scene allowlist: unobserved executions
that match it do not acquire live-proof coverage from this finite checkpoint. This is not physical PS2/device/browser proof, canonical
integration or legal/clean-room certification. No calibration/pedal API, coupling,
transmission, clutch/handbrake, steering rewrite, physical adapter, FFB, AI/reset/
step or other recovery follows automatically. **Stop at this bounded checkpoint.**
