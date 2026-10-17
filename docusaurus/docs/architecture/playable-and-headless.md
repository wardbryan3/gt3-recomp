---
title: Playable and headless — intended shared gameplay
---

Playable and future headless hosts must consume one authoritative gameplay
implementation with shared settings and numerical contracts. There is no faster,
easier training-physics fork. Separate hosts do not require parallel gameplay bodies.

**Headless episode/reset/step interfaces are not implemented by restructuring or
this documentation.** Existing snapshot load/save and frame counters are runtime
primitives, not a proven atomic physics-step API. A process frame limit is not proof
of exactly N simulation updates, reproducible reset, complete host-state capture,
or faster-than-real-time correctness.

Before an AI consumer can rely on observations, it needs proven object ownership,
units, coordinate frames, sampling phase/atomicity and race/lap/finish transitions.
UI strings and candidate field names do not establish these contracts. Replay must
be qualified by version, configuration and numerical contract; its format is undecided.

The third milestone ultimately removes PS2 execution/translation machinery from
complete playable GT3, while still requiring legally supplied ISO assets. Current
native executables do not meet that milestone. See [goals](../start-here/goals.md),
[telemetry research](../research/reconnaissance/telemetry.md) and
[reset/step research](../research/reconnaissance/reset-step.md). Further interfaces
or probes require separate scoped authorization, not a speculative framework.
