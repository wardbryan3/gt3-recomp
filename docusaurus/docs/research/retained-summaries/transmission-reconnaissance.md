:::note Superseded early reconnaissance

The [later transmission map](../transmission/producer-consumer-map.md) rejects early
gear-selector candidate leads. Use the [transmission index](../transmission/index.md)
for subsequent bounded recoveries; the early observations below are not renamed.

:::

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Transmission, clutch and handbrake reconnaissance
---

**Historical reconnaissance:** the bounded [transmission map v1](../transmission/producer-consumer-map.md)
now traces the actual selector/commit path with fresh original-only AT/MT observations.
It corrects the transmission-candidate lead below, distinguishes ratio index from
transition state, and retains neutral naming for `+0x139C`. The older leads and
priority list on this page are preserved as history, not current authorization.
The later [moving-forward Reverse investigation](../transmission/reverse-investigation.md)
reproduces original neutral-like free-engine behavior without identifying a new
neutral ratio or renaming the coupling candidate.
The consolidated [engine-to-drivetrain power-transfer report](../transmission/power-transfer.md)
adds the state-3 calibration-dependent interruption, bounded transition model,
policy/owner and clutch-parts dataflow, rejected leads, and explicit missing
fixtures. It remains read-only and **not recovery-ready**; the historical leads
below are not the current model.

## New bounded recovery checkpoint

[MT selector recovery v1](../transmission/mt-selector-v1.md) now recovers only whole
`001E5458–001E553B`, with independent exact differential, opt-in integration and
bounded native proof. Its original `001E4E80` dependency, dispatcher/commit,
AT/alternate policies and all engine/driveline/wheel processing remain generated.
The separate source-pinned authority is `decomp/gt3/transmission.json`; canonical
installation remains false and build/runtime gates default OFF. This does not
close the comprehensive power-transfer report's unresolved gates.

The **following historical dependency map** is not new recovery authorization.
Retained static batch evidence is in `evidence/rea/project-init.json`; use
`just evidence ADDRESS`. Except for the explicitly bounded validation-only MT
entry above, these original routines stay generated.

## Shift / gearing

- Common command **signed byte +2** is shift intent. Digital helper assigns it even when mask is zero; `0x8000` prioritizes -1, otherwise bit14 gives +1/0. Synthetic overlay restores the original pad-built shift byte.
- Original `001E4478` at `001E4BA8` writes command shift into control state **car+1305** unless car+14BA suppresses it. The proposed pedal recovery stops before this dispatch.
- `001E3B18/001E3708` are control orchestration candidates. `001E3A68 → 001E3360/001E3068` are transmission/shift-transition candidates using state near car+E8C, processed handbrake and counters.
- `001E7500` indexes ratios by **car+13BA** and branches on **car+13BB**; these are different fields. Do not label +13BB as the selected gear. Engine rate +13CC and display conversion +1414 interact with idle/rev limits.

Automatic/manual policy, timing, neutral/reverse semantics, selector mapping and exact field roles still need a bounded producer-to-consumer trace. Search string `gear_auto_on/off` is evidence of UI labels, not a validated configuration policy.

## Clutch / coupling

`001E4180` writes **car+139C** based on mode, brake, shift/auxiliary, handbrake, driveline state, idle thresholds and suppression flags. In policy value 3 it derives `1-brake` and clears brake. Mode 6 reacts to command shift and auxiliary pressure. `001E7500` reads this field in coupled transitions.

Call it **coupling candidate**, not a proven physical clutch input. There is no added clutch command field, axis, pedal adapter or general manual gearbox API. The `parts_drv_clutch` string describes a tuning part and alone proves no input axis.

## Handbrake

Command signed halfword **+14**, analog flag **0x10**, enters original tail `001E4BB8–001E4C5F`: digital rise/fall constants **002D4940/44**, analog Q12 plus nonzero floor at **00352990**, processed state **car+13B4**. `001E6EC8` adds it times car+E40 to the two rear request entries at +12BC/+12E0, and coupling/shift routines also inspect it.

Those static relationships support handbrake intent, not a full wheel-torque or physical-device contract. The proposed pedal boundary excludes handbrake and the `001E4180` coupling call. Do not extend recovery across these interactions without separate fixtures and approval.

## Priority

1. Freeze accelerator/brake handoff and mode arbitration.
2. Trace existing pad/digital shift through control-state and transmission candidates, including automatic paths.
3. Isolate original handbrake and coupling semantics; decide if necessary for Checkpoint 1.
4. Only then consider separately authorized physical shifter/clutch integration. No recovery or host integration was done tonight.
