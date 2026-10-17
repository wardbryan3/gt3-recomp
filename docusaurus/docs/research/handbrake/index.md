---
title: Handbrake evidence
---

[Handbrake v1](recovery-v1.md) recovers a bounded interior slice of `001DF5B0`
from `001DF670` through the pre-`001DF6B0` join, not the containing function.
It preserves copied command value, zero/no-copy behavior, full required state and
path-dependent cost. Independent commit fixtures distinguish exact-zero apply
transitions from merely inspecting a nonzero source halfword.

[Virtual handbrake v1](virtual-input-v1.md) covers the qualified controller mapping,
digital/analog paths and original packet versus adapter/actual-join comparisons.
Keep adapter tests, clean substitution proof and original commit observations
separate; downstream brake physics remains original.

The retained authority tables are historical snapshots, not regenerated views or
current product acceptance. See [retained summaries](../retained-summaries/index.md),
[current controls architecture](../../architecture/controls.md) and
[validation](../../developer-guide/validation.md). Neither report is physical
handbrake calibration or permission to install a hook.
