---
title: Transmission evidence
---

| Read in this order | Claim boundary |
|---|---|
| [Producer/consumer map](producer-consumer-map.md) | Original update order and rejected early candidate leads; not a recovered gearbox. |
| [Moving-forward Reverse](reverse-investigation.md) | Reverse is index 0; no accepted change is not Neutral. |
| [Power transfer](power-transfer.md) | Distinguishes selected ratio, engine state, coupling, drive calculation and commit. Broader recovery gates remain open. |
| [MT selector v1](mt-selector-v1.md) | Whole `001E5458–001E553B` decision, exact CPU/RAM/cost; retains generated helper dependency. |
| [Speed/helper search v1](speed-search-v1.md) | Separately recovers helper and validates selector+helper composition. Its counts do not replace selector-only proof. |
| [Admission/state v1](state-transitions-v1.md) | Whole admission plus partial engine/commit decision models. Models are not whole-function ABI replacements. |

The early `001E3A68/001E3360/001E3068` gear-selector candidates retained in the
symbol table were rejected as that lead. Later recovered boundaries have separate
source-pinned authorities; an “unclassified” entry in an early inventory is not a
retraction of later evidence. Do not rename historical authorities to hide the progression.

Use the new [MT selector walkthrough](../../developer-guide/worked-example-mt-selector/index.md)
for a teaching sequence tied to current source/tests, and
[transmission architecture](../../architecture/transmission.md) for the concise model.
The research report remains the original bounded evaluation, not the tutorial or a
supported current hook-installation runbook. Virtual transmission is an
[enhancement experiment](../enhancements/index.md), not original drivetrain behavior.
