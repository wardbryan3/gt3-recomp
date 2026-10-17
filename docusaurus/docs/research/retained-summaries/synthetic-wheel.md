:::note Superseded synthetic-wheel orientation

See the [detailed synthetic-wheel evidence](../controls/synthetic-wheel.md) and
[current control architecture](../../architecture/controls.md). This old summary is retained, not maintained instructions.

:::

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence context:** experiment narrative below is historical. Fresh [current-main native validation](../checkpoints/native-v3-baseline.md) repeats the unchanged synthetic adapter/live checks in a test-only host; canonical ps2run has no synthetic runtime installation.

---
title: Preserved synthetic-wheel experiment
---

The earlier adapter remains independent in `host/gt3_synthetic_wheel.*`, default-OFF build flag, its own CLI and probes, build/run/validate scripts and `build/synthetic-wheel` evidence. Initialization did not redesign it around the clean API.

Temporary overlay at `002107AC`, restore at `002107B8`; manual context `001E4D38/001E4D5C`, shipped vtable guards, released pedals and shift restoration remain unchanged. The host supplies an axis word, not a final steering angle; original builder and downstream consumers run. No pedal/shifter/clutch/FFB feature is added.

`--gt3-wheel VALUE` accepts finite [-1,+1]. Absolute-frame `--gt3-wheel-at FRAME:VALUE` events must be strictly increasing. `--gt3-wheel-trace NEWFILE` alone is read-only; output files are exclusive-created. Earlier seven quantized axes are a **synthetic design domain**, not verified physical report calibration.

Standalone regressions remain **8,193** quantizations / **42** generated integrations, plus parser/profile/scope/restoration/scheduling guards. Earlier independent live evidence remains `build/synthetic-wheel/live-final/summary.json`; original executable is the independent oracle for fresh clean validation.

See [the unchanged experiment narrative](../controls/synthetic-wheel.md). Synthetic steering's success does not authorize physical-wheel support, and a clean-enabled build does not automatically enable synthetic injection.
