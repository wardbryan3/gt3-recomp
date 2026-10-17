:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

> **Current admission:** [Observed-context closure](pedal-closure.md) is re-frozen: unchanged body,4,199 actual-context differentials and4,199 guarded substitutions, zero fallback, all14 observed representative runs /five classes. No universal/physical/canonical-integration claim; stop.

> **Evidence context:** original discovery below is historical. Fresh steering/synthetic proof is in [current baseline](current-baseline.md); separately authorized bounded pedal recovery is in [Pedal v1](pedal-v1.md). Canonical ps2run remains generated-only.

---
title: Throttle and brake — detailed original-code discovery
---

**Historical discovery narrative.** Canonical pedal/control processing remains generated. A new bounded validation-only replacement is documented separately; no physical or synthetic pedal adapter was added.

## Current requested cycle

[Pedal Recovery v1 prerequisite audit](pedal-recovery-v1.md) stopped before
implementation. A separate [current-main baseline](current-baseline.md) task has
since restored tools, fresh regressions, a native v3 race fixture and bounded
steering/synthetic live proof. It did not itself resume pedals. A subsequent
explicit request produced [Pedal v1](pedal-v1.md), with exact join/wrapper/consumer
and bounded v3 live proof in an isolated default-OFF host. The discovery below
retains its historical context; it is not the new validation report.

The subsequent [descriptor/profile reachability survey](pedal-profiles.md)
**stopped at an unsupported command-buffer context**, without changing Frozen.
Four paired cases passed; remaining clean pairs/full native regressions were not
continued. Original-only configuration observations are not broader equivalence.

## Original producers

- Digital mask helper `00210EF8`: mask `0x400/0x800` sets command accelerator `+8` / brake `+10` to 1 and clears analog flags 2/4. A truthy digital command is not the same representation as Q12 analog pressure.
- Mapped pad primary/secondary actions (`00211050/002111C0`) normalize channels via `00210F90`; signed negative mappings remain unmapped. `00211398` is an inspected action producer, distinct from mapped-action filling. Complete action-policy interpretation is not re-established tonight; prior controls fixtures remain authoritative.
- Wheel input `00230D10 → 0022FFE8 → 002115F8`: shipped getters select bank 0 or 16, types 1–3. Channels bank+1/+2 use `002115D8(raw, threshold)` with thresholds **75/80**. Positive pressure only writes command `+8/+10 = pressure*16` and flags 2/4. Released pressure preserves preceding commands. EE wrapping occurs before signed cap; tested raw 0–255 is fixture domain, not physical calibration.

For ordinary fixture values, `pressure = min((255-raw-threshold)*2,256)`; nonpositive pressure is not assigned. Full accelerator at raw≤52, brake at raw≤47; adjacent raw53/raw48 produce Q12 **4064**. Accelerator releases at raw180, brake at raw175. These arithmetic cutoffs are not a hardware-report-range claim.

## Manual command and control processing

`001E4D38` builds a command, preserves the original optional virtual command hook, and calls `001E4CB0`. That wrapper calls **`001E4478(car,command,car+1304)`**, then copies processed accelerator **car+13AC → car+1428**, and calls `001EAC60` with processed brake **car+13B0**.

The accelerator/brake boundary is **`001E48FC–001E4BA7`**, resuming original **`001E4BA8`**. It is now recovered only in the separately documented validation host, not installed into canonical ps2run. Original steering, handbrake, shift dispatch, coupling helper and epilogue remain outside it.

Accelerator processing is not a simple `command+8 /4096`: policy-dependent arbitration includes auxiliary command `+12`, analog flags 2/8, prior state, and control-state bytes. It mutates car+13AC and control-state bytes at car+1304/+1306. Digital rise/fall constants are at **002D4930/34**. Analog nonzero pressure applies `x + k*(1-x)` with **k at 00352990**; exactly zero remains special. Mode 4 applies signed response descriptor **0049D060** through `001D92E0`. Descriptor mode 0/default is identity; 1 is shifted quadratic, 2 is shifted square-root; optional derivative behavior and EE edge cases must be audited before any clean recovery. Real live descriptor contents/calibration are not inferred from zero-initialized fixture data.

Brake digital input slews previous **car+13B0**, rises/falls with **002D4938/3C**, clamps on the corresponding path. Analog input uses signed Q12 conversion, the same nonzero floor, and mode-4 response descriptor **0049D070**. Do not replace these with host-normalized linear floats or clamp unsupported inputs preemptively. The generated instructions at the boundary also load car+14BA into `v0` for the following shift guard; this outgoing state is part of the handoff contract.

Original `001E4180` later writes coupling candidate car+139C. In policy value 3 it moves brake information into `1-brake` coupling and clears brake; this can change the wrapper's final broadcast value. Therefore pre-helper brake is **not always final braking**. Mode/policy meanings are still partial; retain neutral field names.

## First meaningful simulation consumers

**Throttle**: car+1428 enters `001E7500`, whose free-engine state reads it into `001E17F0`, calls `001E1768` and `001E0C38` for torque conditioning/power limiting, and integrates **car+13CC += torque * car+2BC * dt**. Coupled branches interact with gearing, wheel speeds and clamping; they remain untouched. `001E6D00` converts engine rate into display-speed candidate car+1414. Accelerator request is not final engine torque or a vehicle force.

**Brake**: `001EAC60` broadcasts processed brake into **car+1074+i*A4** for all four wheel structures. `001E6EC8` scales by axle parameters **car+E38/+E3C**, writing **car+1274+i*24**. Rear entries additionally receive **car+13B4 * car+E40** (handbrake candidate). Later `001E7450`, `001E7328` and drivetrain/wheel integration consume requests; units are not certified as physical brake torque. No tire/force integration was replaced or reconstructed tonight.

## Executed original-only fixture evidence

`tests/gt3_pedal_discovery.cpp`, `historical discovery runner`; retained results **`build/project-init/pedal-fixture.jsonl`** and `.log`. **22** fixtures: two banks × 11 raw values. Original ELF data/vtable/constants and generated calls at `002115F8 → 001E4CB0 → 001E6EC8 → 001E7500`. Checks assert command propagation, exact processed/effective throttle copy, all four wheel broadcast/scaled values, engine-rate step and return PC/SP. No clean differential or game boot occurs.

| raw | command accelerator / brake | original processed accelerator / brake |
|---:|---:|---:|
| 0 | 4096 / 4096 | 1 / 1 |
| 48 | 4096 / 4064 | 1 / 0.992968738 |
| 53 | 4064 / 3904 | 0.992968738 / 0.957812488 |
| 100 | 2560 / 2400 | 0.662499964 / 0.627343714 |
| 174 | 192 / 32 | 0.142187491 / 0.107031249 |
| 175 | 160 / 0 | 0.135156244 / 0 |
| 180, 255 | 0 / 0 | 0 / 0 |

Fixture curves are constant steering curves and identity pedal descriptors; dt=1/60; axle factors=1; no handbrake; free-engine state and selected synthetic coefficients. Starting engine rate 100 rises to 100.016663 at full pressure. This proves bounded original propagation, **not stock engine/axle calibration, actual racing acceleration/deceleration, or physical-pedal usability**.

The first attempt aborted because a zero rev-limit field cut torque. The fixture now configures rev limit 8000; checks were not relaxed. See the [next-cycle plan](queue.md) for required digital/arbitration/curve/mode coverage before recovery.

## Static citations

Retained `evidence/rea/project-init.json`:

- Manual processing, wrapper, coupling, response evaluator: **`ev_1ae7e5b58f8018c49aa9ed4a976e3984f3dda1001e36148fc94cff18145abd71`**.
- Broadcast and action producers: **`ev_8c3e03fbea44f8fbe453131cb558f8b3f64ccef1d449d2d0c18bcac42922560e`**.
- Engine step / downstream request assembly: **`ev_74e74e6769a0fe2bb6fb5df2bdc51f7e881b7bea114215dbc676928cc2219142`**.
- Wheel brake preparation / power limiter: **`ev_8362907ce1bf0ec57b1c2b7100f631cb8232c654c181a2dd8431a8b3d0ae164b`**.
- Engine torque path: **`ev_e6e1f4108a626daaa3d88d47aebb049c8d8d78004d6c4b118e56795a7f1302ea`**, **`ev_ed109d25a990ea10dec38122a191195ab39aaa3fa7db1828308b1dec22338763`**.

Pseudocode float-argument/return types can be wrong; ABI and region boundaries also checked against retained generated `unit_0039.cpp` instructions. Static naming certainty does not certify every consumer's physical meaning.
