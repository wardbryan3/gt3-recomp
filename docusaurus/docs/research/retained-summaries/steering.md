:::note Superseded steering orientation

Use [controls architecture](../../architecture/controls.md) for the current model and
[controls evidence](../controls/index.md) for the detailed reports. The old summary remains below.

:::

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence context:** installation/results below describe the historical experiment. The unchanged four boundaries now also pass fresh [current-main native validation](../checkpoints/native-v3-baseline.md) in an isolated test-only host. Canonical ps2run remains generated-only.

---
title: Verified and frozen clean steering
---

Only four existing sites are installed:

| Original entry | Recovered implementation | Inclusive boundary / resume |
|---|---|---|
| `00210F90` | `normalize_mapped_channel` | `00210F90–0021104F`, return normally |
| `002115F8` | `build_wheel_command` | `002115F8–0021174F`, shipped input vtable/zero adjustments only |
| `001E4368` | `filter_stick` | `001E4368–001E4467`, return normally |
| `001E4478` | `process_steering` | **Interior `001E45A8–001E48FB` only**, resume `001E48FC` |

`001E4478–001E45A7` remains original: classification, curve selection and interpolation. The original pedal/control tail and epilogue remain generated. Helpers `00210EF8`, `002115D8`, `001E4470`, `001E4320` are expressed as needed internally but are **not separately installed replacements**. All downstream physics remains original.

## Integration guards

`PS2_GT3_CLEAN_STEERING` defaults OFF; runtime `--gt3-clean-steering` is additionally required. Synthetic infrastructure is built for independent profile guards/probes, but injection requires its own flag. Unsupported vtables/adjustments, invalid RAM ranges and classifications fallback to generated. Label gates operate on copied bodies, not protected original outputs.

`Command`, `InputPartial`, `CarPartial` are partial evidenced storage views. Use explicit padding, `memcpy`, offset assertions, EE bit-pattern arithmetic, wrapping integer behavior and exact dynamic cost. Do not reinterpret float fields with host arithmetic, rename `unknown13a4` as a physical quantity or bulk-write vehicle padding.

## Fresh initialization verification

Unchanged regression suite: **28,160** clean normalizations; **16,384** clean wheel builders; **16,000** filters; **20,000** envelope/full-original-tail cases. Relevant bytes, return PC/SP, callee-saved state and dynamic budget match exactly. Earlier controls/mapping/pad/wheel/synthetic/GPU/hardware assertions also pass. See [testing](../../developer-guide/validation.md).

Fresh full-game validation in `build/project-init/live/summary.json`: **3,400** clean mode-4 updates, **13,600** original consumers, maximum reconstruction error **5.96046448e-8**, existing tolerance **2e-6**. Seven values, `+.5 → 0 → -.5`, two accelerated *race continuations* (ordinary native execution; no faster-than-real-time API) and clean pad path repeated independently with preserved original executable. Per-frame semantic traces, captures, final car and complete EE/IOP/SPU dumps match. Gates-off and trace-only remain byte-identical to baseline.

Fresh isolated foundation clean build SHA-256 **`f42be9562a0201e5d7c1618e05ca0c500bed3a80cd654ef8c2329763be3234c3`** matches the frozen validated clean executable exactly. The original and synthetic executables were not rebuilt in place.

This repetition used native offscreen WebGPU readback, not a new desktop/presentation/audio test or physical device. One race snapshot and bounded continuations; no every-car/mode or physical-PS2 numeric guarantee. See [retained full contract](../controls/steering-recovery.md) for the detailed original evidence and historic failure fixes. **Freeze; do not extend without a new request.**
