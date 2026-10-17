---
title: Virtual pedal v1 experiment
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


<!-- Generated from decomp/gt3/virtual-pedals.json. -->

Status: **validated-bounded**. Isolated validation only; build/runtime gates default OFF; no canonical installation.

| Gate | Result |
|---|---|
| parser | passing |
| oracle | passing |
| live | passing |
| regressions | passing |
| strict | passing |
| public | passing |

Host [0,1] maps to Q12 0–4096, positive half ties up, at original command-builder return. No processed car writes or physical calibration. See [experiment report](../virtual-pedals.md).

Strict private verification: `just verify-virtual-pedals EXPLICIT_REPOSITORY_ROOT`.
