---
title: "Current-main native baseline"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->

Historical function lifecycle remains separate. This page describes **current-main source with an isolated validation-only harness**, not canonical runtime installation.

Source base: `82987dec7a71d76414adfff8663da5494a280938`.

| Gate | Current result |
|---|---|
| build | passing |
| regressions | passing |
| live | passing |
| native v3 fixture | passing |

- Historical function lifecycle/runtime/live fields remain historical; this separate record establishes fresh bounded native validation, not canonical runtime installation.
- Native unpatched USA v1.10, one Super Speedway Arcade race with external UTC input pinned; no browser, physical-device, physical-scanout, arbitrary-car/mode or long-session proof.
- The raw v3 fixture is identity-pinned; independent normal boots can differ in unspecified serialized native padding. Every defined state byte, complete guest dumps and replay comparisons pass without rewriting either state.
- Canonical ps2run has no clean/synthetic runtime installation. Four unchanged frozen gates execute only in the isolated validation harness. No pedal recovery or lifecycle promotion.
- Initial capture/frame/clock/padding/input-phase assumptions and a comparison-helper tag typo were retained as failed attempts under local/baseline-v3; no original regression assertion, evidence hash or snapshot header was weakened/rewritten.

Private evidence is fingerprinted in `decomp/gt3/current-validation.json`; use `just verify-current EXPLICIT_REPOSITORY_ROOT`. Raw snapshots, binaries, traces and captures are not published. See [current baseline](../current-baseline.md).
