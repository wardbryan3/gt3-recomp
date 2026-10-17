---
title: Historical telemetry and race-state reconnaissance
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence boundary:** the candidate map below records original-code reconnaissance and bounded historical observations, not a telemetry API. Later bounded transmission recovery clarifies some state fields; it does not establish telemetry ownership, units or sampling semantics. See [current authorities](../../reference/authorities.md) for source/proof/approval status.

## Recorded candidate map

| Guest field / routine | Candidate meaning | Confidence / evidence boundary |
|---|---|---|
| car+13A0; +FF0+i*A4 | Steering and per-wheel angles | High; static, differential and bounded running-game observations |
| car+13AC/+13B0/+1428 | Processed accelerator/brake and effective accelerator | High static / 22 constructed original-code fixtures, not a live pedal telemetry contract |
| car+13CC | Engine angular-rate candidate | Static integration and fixture; physical units/sign/range need verification |
| car+1414; `001E6D00` | Display engine speed candidate | Static rate×60/constant and idle-floor conversion; stored signed16, may wrap |
| car+140C | Steering-envelope speed input candidate | Live envelope changes at speed; units/frame not certified |
| car+F84 and following vector | Position-like candidate | Static motion/post-update consumers; axes, world frame and units not recovered |
| car+13BA/+13BB | Originally ratio index / driveline state candidates | Later bounded recovery identifies selected ratio / transition state; neither is simply displayed gear (see below) |
| `001ED000(race,index)` | Reads car-slot word at race+E388+index*4 | Static getter; count/ownership and player association need proof |
| `001F2B18` | Countdown-like race field +B7AE and callback | Static only, no lap/finish interpretation |

## Later state knowledge and remaining API uncertainty

The [transmission-state decision model](../transmission/state-transitions-v1.md) distinguishes
`+13BA` selected ratio, `+13BB` transition state and `+139C` coupling candidate.
Ratio 0 is Reverse; rejected selection −1 is not Neutral. State values 0–3
describe distinct drive routing and later engine transitions, not one clutch
engagement flag. It also identifies `+13CC` engine rate and `+1414` sampled
signed RPM halfword. These are bounded behavioral descriptions, not original
symbol names or certification of a public telemetry contract. The earlier
candidate table's ownership, physical-unit/range and sampling gaps are not
resolved merely by naming fields.

Live pointers in the historical snapshot (car01FBB7BC, input01FAC260) are observations, **not stable API addresses**. Find objects through proven ownership paths and guards in any future telemetry design.

## Race and lap inference limits

`001E7D90/001E8008` are vehicle motion candidates; `001EB218` orchestrates many post-update routines, including geometry/state/output work. It is **not a proven lap-count routine**, and none of these is a complete recovered telemetry boundary. `RaceLapTime` at003279B0, `RaceLapDisplay` at0032F190 and `LapCountLabel` at00330F18 are retained typed-string seeds; UI names do not establish the lap counter or timer. Trace writers and event lifecycle before exposing lap/finish state.

The earlier AI-episode reconnaissance required trusted observations and exact
race semantics in addition to actions, reset and controlled advancement. Finding
UI strings or a post-update caller did not establish lap/finish/failure event
writers, transitions or player association. No lap API was implemented by that
reconnaissance; [reset/step limits](reset-step.md) are a separate proof gap.

## Requirements for any separately authorized telemetry work

A future read-only telemetry contract must specify units, coordinate frame, sampling phase and atomicity, object lifetime/player selection, episode/tick identity, valid flags, race-state transitions, signed/wrapping fields and replay validation. Correlate observations with visible gameplay and independent original memory, not convenient names. No exporter, new probe, action API or live lap/finish experiment was implemented in this reconnaissance. These requirements are not authorization to add one.
