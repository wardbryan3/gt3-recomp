---
title: Transmission — selection is not engagement
---

This orientation summarizes bounded research, not a whole-transmission replacement.
Read the [producer/consumer map](../research/transmission/producer-consumer-map.md)
for original-code evidence and [power transfer](../research/transmission/power-transfer.md)
for mechanisms and remaining calibration/policy gaps.

```text
original command construction and processing
  → coupling candidate / processed requests
  → admission and saved-rate preparation (001E6D48)
  → drive and differential calculations
  → engine-rate integration / synchronization (001E7500)
  → policy routing / selection (001E77E0 → 001E5690)
  → accepted ratio commit (001E4E78)
```

A state written after drive cannot explain the contribution already computed in
that update. The MT selector `001E5458` decides an index or no change; it does not
commit the ratio, select a clutch state or calculate effort.

| State/representation | Bounded meaning |
|---|---|
| Signed command `+2` / car `+0x1305` | Relative request, not absolute H position |
| `+0x13BA` | Selected ratio index; **0 is Reverse** |
| Selector return −1 | No accepted selection; not Neutral |
| `+0x13BB` | Engine/driveline transition state, not a second gear number |
| `+0x13BE` | Inhibition/rearm counter, not necessarily shift duration |
| `+0x139C` | Coupling candidate, not a calibrated physical clutch axis |

State 0 can retain a forward ratio while engine-directed effort is zero. State 2
can transmit effort with candidate zero. Ordinary forward changes can use state 3
with candidate one. Thus neither the candidate nor selected index alone describes
physical engagement. Wheel forces and vehicle acceleration are broader quantities.

Readable selector, helper and whole-admission recovery have separate proofs. Engine
and commit decision models are partial projections, not whole-function ABI
replacements. None is installed into current products. Follow the
[worked selector](../developer-guide/worked-example-mt-selector/index.md) for one
complete bounded example; use [state research](../research/transmission/state-transitions-v1.md)
for precise transition conditions and limits.
