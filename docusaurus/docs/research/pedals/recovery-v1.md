---
title: Pedal Recovery v1 — bounded historical contract
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::


## Historical disposition and current locators {#current-disposition}

The semantic body below remained unchanged through the separately pinned
[observed-context closure](closure.md): **4,199** actual-entry shadow comparisons
and **4,199** guarded substitutions, zero fallback, all **14** representative
contexts / **five** processing classes. That later historical admission superseded
the original absolute-address exception; neither checkpoint installs recovered
processing into either current product. See [current authorities](../../reference/authorities.md)
and [validation layers](../../developer-guide/validation.md) for present proof and approval boundaries.

The mechanical `project/gt3/migration-map.json` locates the implementation at
`src/gt3/gameplay/controls/gt3_clean_pedals.{hpp,cpp}`, the join audit at
`validation/gt3/differential/gt3_pedal_abi_audit.cpp`, and this checkpoint's authority
at `project/gt3/pedal-validation.json`. These are current source locators, not
claims that current bytes are the exact historical evaluated versions.

## Original result and scope

The user-authorized continuation has recovered **only 001E48FC–001E4BA7**,
rejoining generated execution at **001E4BA8** inside native routine 001E4478.
**Frozen — bounded validation-only implementation.** Final checkpoint evaluation is recorded in
`decomp/gt3/pedal-validation.json`
and its [public authority copy](pathname:///knowledge/pedal-validation.json).

Source base was committed/pushed baseline **46a32c7**, plus the identity-recorded
recovery overlay. The [historical native-v3 baseline](../checkpoints/native-v3-baseline.md), its authority and its
trusted normal-boot v3 fixture remain unchanged. The prior
[stopped audit](stopped-prerequisite-audit.md) is historical, not the present outcome.

**Canonical ps2run remains generated-only.** `gt3_recovered` is a compile-checked
source library, not linked into canonical ps2run. `CMakeLists.txt` adds the pedal
source to that existing test library only. The new gate exists in a disposable
validation translation and requires separate build AND runtime opt-in, both
OFF by default. Interior recovery is not whole-function recovery or an input API.

## Original producer → representation → consumer chain

The original producers build the common 16-byte command before manual processing:

- Digital helper `00210EF8` tests masks **0x400/0x800**, sets accelerator **+8** /
  brake **+10** to **1**, and clears analog flags **2/4**. A truthy digital value
  is not Q12 analog pressure.
- Mapped pad actions `00211050/002111C0` normalize through `00210F90`; signed
  negative channel mappings remain unmapped. `00211398` is a distinct inspected
  action producer, **not** mapped-action filling. The detailed lookup, sensitivities
  and visitation order are in [the controls reference](../controls/mapped-actions.md).
- Wheel path `00230D10 → 0022FFE8 → 002115F8` uses shipped getters, banks **0/16**,
  types **1–3**. Pedal channels bank+1/+2 call `002115D8` with thresholds **75/80**.
  Positive pressure writes `pressure*16` to +8/+10 and sets flags 2/4; release
  leaves earlier pad/digital commands intact. Wrapping precedes signed capping.

For ordinary fixture values, pressure is `min((255-raw-threshold)*2,256)`;
nonpositive pressure is not assigned. Full accelerator is reached at raw≤52,
brake at raw≤47; raw53/raw48 respectively produce **4064**. Accelerator releases
at raw180, brake at raw175. The tested raw **0–255** domain and these cutoffs
are arithmetic fixtures, **not physical report calibration**.

`001E4D38` builds the activation-local command, retains the optional original
virtual command hook, and calls `001E4CB0 → 001E4478(car,command,car+1304)`.
The wrapper copies processed accelerator **+13AC → +1428** and sends processed
brake **+13B0** to `001EAC60`. Later original `001E4180` can move brake information
into `1-brake` at coupling candidate **+139C** and clear brake under policy 3;
a pre-coupling brake value is therefore **not always final braking**.

The first simulation consumers remain original:

- **Throttle:** +1428 enters `001E7500`; its free-engine branch uses `001E17F0`,
  `001E1768` and `001E0C38` for torque conditioning/power limiting, integrating
  `car+13CC += torque * car+2BC * dt`. `001E6D00` derives display-speed candidate
  +1414. Command pressure, processed request and final engine torque are distinct.
- **Brake:** `001EAC60` broadcasts to **+1074+i*A4** for four wheels. `001E6EC8`
  scales by axle parameters **+E38/+E3C** into **+1274+i*24**, adding handbrake
  **+13B4 * +E40** to the rear pair. `001E7450`, `001E7328` and original wheel/
  drivetrain integration consume these requests. Physical force units and
  recovered tire/force integration are not established by this chain.

### Original-only discovery fixtures

The initial discovery ran **22 fixtures: two banks × 11 raw values**, through
original `002115F8 → 001E4CB0 → 001E6EC8 → 001E7500`, using original ELF data,
vtable and constants. Current locator:
`validation/gt3/differential/gt3_pedal_discovery.cpp`; historical output was
`build/project-init/pedal-fixture.jsonl` and `.log`. Assertions cover command
propagation, exact processed/effective throttle copy, all four broadcast/scaled
brake values, engine-rate step and return PC/SP. **No clean differential or game
boot occurred in that initial population.** These observations are separate from
the initial **32,768 original-only join-audit cases**, the final **131,072-case**
join matrices, and later wrapper/live proof; their counts must not be combined.

| Raw | Command accelerator / brake | Original processed accelerator / brake |
|---:|---:|---:|
| 0 | 4096 / 4096 | 1 / 1 |
| 48 | 4096 / 4064 | 1 / 0.992968738 |
| 53 | 4064 / 3904 | 0.992968738 / 0.957812488 |
| 100 | 2560 / 2400 | 0.662499964 / 0.627343714 |
| 174 | 192 / 32 | 0.142187491 / 0.107031249 |
| 175 | 160 / 0 | 0.135156244 / 0 |
| 180, 255 | 0 / 0 | 0 / 0 |

These fixtures use constant steering curves, identity pedal descriptors, dt=1/60,
axle factors=1, no handbrake, free-engine state and selected synthetic coefficients.
Engine rate 100 reaches 100.016663 at full pressure. An initial zero rev-limit
field cut torque; setting the fixture rev limit to 8000 corrected setup without
relaxing checks. This proves bounded original propagation, **not stock calibration,
actual racing acceleration/deceleration or physical-pedal usability**. The later
full-wrapper differential below is a separate proof population.

## Entry, output and join contract {#contract-established-before-integration}

The pre-implementation join audit executed **32,768 original-only cases**, with
initial measured cost **48–139** EE instructions including the original response
helper. That was not a clean differential or live proof. The final independent
original and clean runs each cover **131,072 cases**, including the observed
**0049AF50** command position and a disjoint synthetic buffer. The original report
called the low address BSS; [closure](closure.md#what-actually-owns-the-command)
corrected that historical assumption to activation-local **stack** ownership.

At entry **001E48FC**, `s7` is car, `s0=car+F84`, `s2` is command, `s3` is the
control-state pointer, `v1=int8(car+136D)` and pinned `gp=3579F0`. The prefix owns
the **176-byte frame** and saved register slots; the manual wrapper supplies
`s3=car+1304`. Other incoming scratch/FPU values persist wherever the original
does not overwrite them. Unsupported aliases/contexts remain generated.

The original may clobber low 64-bit GPR lanes **r1–r8, s1, ra**, FPRs **f0–f3,
f12**, and the FCR31 condition bit. Upper GPR lanes and other CPU state remain
stable. Both descriptor calls pass a null derivative; their original return PCs
are **001E4AD4/001E4B9C**. FCR31's other bits, including existing invalid flags,
remain untouched; no divide occurs on those derivative-null response paths.

- Exact writes: **car+13AC, car+13B0, control-state+0/+2**. No bulk object writes.
- Outgoing **v0 = uint16(car+14BA)**, computed numeric policy **s1**, all GPR/FPR
  scratch effects, upper GPR lanes, FCR31, preserved HI/LO/SA/FACC/VU/COP0 and
  enclosing frame state are compared. This is not a dead-scratch-register mask.
- Both response sites retain **original generated 001D92E0**, derivative null,
  original return PCs, original arithmetic/register effects and original cost.
  Descriptor, command and stack windows remain unchanged.
- Exact path-dependent instruction consumption is compared at the join, with
  positive and negative budgets and supported depth levels 0–191. Observed cost
  range is **48–152**, not a universal timing/performance claim. The bounded
  path/leaf helper has no scheduler edge. Unsupported depth, near-overflow budget,
  profile, pointer, kind or alias contexts fall back **before any mutation**.
- A fixture checkpoint gives PC its semantic join value. Live traces serialize
  every defined CPU field with explicit probe PC; stale direct-branch `Cpu.pc`
  transport values are retained separately. They are not silently erased from raw
  evidence or represented as a hardware PC trace. No guest cost is charged for
  observation; no preemption or instruction-accounting assertion was removed.

`host/gt3_clean_pedals.hpp` provides explicitly padded partial command/control/car
views with compiled size/offset assertions. `host/gt3_clean_pedals.cpp` is newly
written semantic processing, with a scratch-lane ABI sidecar and path-cost
accounting. It is not pasted assembly/decompiler output. Technical provenance
is not a legal-rights or clean-room certification.

## Preserved semantics

Original accelerator digital rise/fall constants are at **002D4930/34**; brake
rise/fall at **002D4938/3C**. The nonzero analog floor word is **00352990**.
Mode4 uses accelerator/brake descriptors **0049D060/0049D070** through original
`001D92E0`: descriptor mode0/default is identity, mode1 shifted quadratic, mode2
shifted square-root. Descriptor identity/execution and finite live calibration
reachability are distinguished in [closure](closure.md#descriptor-presence-is-not-response-execution);
zero-initialized fixture descriptors do not establish stock live calibration.
Accelerator history/control writes are at **car+1304/+1306** in the manual wrapper.

Digital accelerator/auxiliary requests shift then **truncate to 16 bits**. Policy
arbitration uses unsigned magnitudes and selects auxiliary on a tie. Suppression
clears auxiliary before arbitration. Policy remains numeric, not a clutch mode.

Digital rise/release, zero analog with history and fresh zero analog are distinct
paths. Release uses `<0`, whereas zero-analog history decay uses `<=0`; history 2
can force the auxiliary indicator. Unknown history values are not normalized.
Digital history can bypass mode-4 response evaluation. Analog nonzero uses ordered
EE `x + k*(1-x)` without generic saturation. Accelerator halfwords are unsigned;
brake halfwords are signed. Brake exact zero bypasses the floor, not necessarily
the response descriptor. Preserve signed zero, denormals, NaN/infinity bit behavior,
wrapping and existing FCR31 bits. All numeric operations use existing EE bit-pattern
helpers; no host float modernization or fused expression was introduced.

The matrix exercises all numeric policies, signed/unsigned halfword edges,
representation flags, mode 0/4 plus unknown byte modes, histories including
unknown values, suppression/classification variations, existing random CPU state,
response modes 0/1/2/default and synthetic coefficient/prior-state special values.
These are constructed EE fixtures, **not original calibration or physical inputs**.

## Independent full-wrapper and consumer proof

**2,160** constructed cases vary flags, modes, policies 0–6/7/255, history,
suppression and zero/full/edge pressure. Each runs independent original versus
clean wrapper, original brake distribution and original engine consumer:
**6,480 complete CPU + 32 MiB guest-RAM comparisons**. The generated suffix,
shift/handbrake handling, 001E4180 coupling and wrapper propagation execute
unchanged. Policy-3/6 downstream interactions are therefore not inferred from a
pre-coupling brake value alone.

The preserved **22 original-only discovery fixtures** also pass unchanged in
normal compilation. Their explicit differential build adds complete CPU/RAM
comparisons without removing the original assertions; they are not the sole
nonzero-pedal or policy proof.

## Bounded native-v3 live proof

The exact trusted frame-4801 native v3 fixture is reused read-only, with future
input starting at **4802**, and only the original baseline's external UTC input
pin. No v2 import, header rewrite, snapshot format or reset redesign.

**19 runs / seven paired scenarios**: neutral, accelerator-to-brake, simultaneous
accelerator/brake, pad turn/release, wheel left, wheel right and wheel transitions.
The latter cases include the unchanged frozen clean-steering path. Independent
pairs differ only in the new pedal runtime flag.

- **2,100 clean pedal updates**, **zero accepted live fallbacks**.
- **1,800 original response calls** from the clean path, also observed in the
  generated counterpart. Both descriptor sites execute in mode-4 scenarios.
- **4,200 player-car original brake/engine consumer observations**, plus generated
  coupling continuation and **8,400 original steering-consumer observations**.
- Every compared defined CPU/pedal trace, unchanged steering trace, capture and
  **complete EE/IOP/SPU dump** matches exactly. No float tolerance is needed for
  these equality checks. Steering reconstruction retains **2e-6**, measured maximum
  error **5.96046448e-8** (900 mode-4 updates in these pedal scenarios).
- Canonical, build-OFF disabled/trace-only, runtime-disabled and trace-only dumps
  and captures match. A build-OFF host rejects the enable flag with exit 2.
- Reviewed accelerator/brake captures show the native race UI at 16 mph before
  braking and zero afterward. This is a bounded visual observation, not physical
  speed/pedal calibration.
- **14** independent disabled/profile/context/depth/budget/alias fallback cases
  leave complete CPU and all 32 MiB RAM unchanged.

The first live attempt was **not accepted**: its conservative low-region alias
check correctly fell back on the actual 0049AF50 command position. The assertion
requiring genuine replacement failed. That run/build is retained. A narrowly
explicit exception, then described as a BSS context, was independently audited
and freshly rebuilt; the assertion was not weakened and no fallback was forced
into success. That ownership description was later corrected to stack storage
by closure; the original attempt and its result are not relabeled.

Private accepted build/live/regression trees contain **623 / 129 / 7 files**,
pinned individually through separate manifests. Earlier attempts remain under
ignored `local/pedal-v1-resume/`. The authoritative fixture and old evidence hashes
are unchanged. No raw trace, screenshot, generated source, binary, descriptor or
machine configuration is published.

## Historical regression and reproduction {#regression-and-reproduction}

The following results and recipe belong to the original evaluated checkpoint.
The bespoke builders are retired; do not mechanically substitute current paths
into this recipe. Maintained public checks are `just check`, `just test` and
`just docs-build`; retained proof uses root `just verify-pedals "$PWD"` (historical
only). See [workflow](../../developer-guide/workflow.md) and [testing](../../developer-guide/validation.md) for current guidance.

Full checkpoint-native baseline regressions passed unchanged: controls **25,600 /
57,344**, pad **15,360**, wheel **19,468 / 7,560**, clean steering differentials
**28,160 / 16,384 / 16,000 / 20,000**, synthetic **8,193 / 42**, original pedal
fixtures **22**, GPU anisotropic/state conversion, hardware/SIF/source consistency,
patch, metadata/publication and docs. Final `just check`, `just test`, `just docs-build`, strict historical/current/pedal
verifiers and unchanged protected ISO/ELF/card checks pass. Metadata negative tests
include scope/default-OFF, boundary, ABI/cost, fixture, source/evidence integrity
and Frozen prerequisite rejection.

The fresh canonical executable remains byte-identical to the authoritative
baseline: SHA-256 `b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a`.
No change to `host/main.cpp`, steering/synthetic algorithms, runtime, recompiler,
renderer, save-state format, ISO/ELF, original cards or baseline snapshots.

```bash
# Both output roots MUST be new. Inputs remain private and fingerprint-pinned.
scripts/build_gt3_pedals.sh /absolute/private/gt3-usa-v110 /absolute/new/build \
  --enable-validation-pedal-substitution
python3 scripts/validate_gt3_pedals.py --build /absolute/new/build \
  --elf /absolute/private/core.elf --iso /absolute/private/GT3.iso \
  --out /absolute/new/live
tests/run_gt3_baseline.sh /absolute/new/build/base \
  /absolute/private/core.elf /absolute/new/regressions
just check
just test
just docs-build
just verify-current "$PWD"
just verify-pedals "$PWD"
just verify-private "$PWD/local/legacy/resolution-repo"
```

Without the explicit build argument, only the OFF validation host is produced;
canonical ps2run is generated-only in either case. A passing isolated validation
is not authorization to install gates into normal gameplay or distribute a game
build. Further recovery requires a separate request.

## Original stopping point {#stop-and-next-dependency}

The checkpoint's instruction was: **this exact boundary is Frozen; stop here.**
The separately authorized finite survey and [closure](closure.md) followed
later; they are not permission for further work. The original next dependency was:
separately authorized original descriptor/profile reachability characterization
for additional modes/cars, before any broader pedal API or claim. Original
**001E4180 remains `update_control_coupling_candidate`**. No transmission, clutch,
handbrake, physical adapter, FFB, physics, AI/reset/step or neighboring recovery
has been implemented or authorized by this checkpoint.
