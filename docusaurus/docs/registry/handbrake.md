---
title: Handbrake v1 authority
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


<!-- Generated from decomp/gt3/handbrake.json. -->

Lifecycle: **frozen**, bounded validation-only. Build/runtime default OFF. Canonical gameplay is generated-only.

| Gate | Result |
|---|---|
| static | passing |
| exact_join | passing |
| stateful_transitions | passing |
| original_downstream | passing |
| native_v3 | passing |
| default_off | passing |
| public_regressions | passing |
| native_regressions | passing |
| strict_evidence | passing |

Only 001E4BB8–001E4C5F is substituted, resume001E4C60. See [semantics, proof and limits](../handbrake-v1.md).

Strict private proof: `just --justfile handbrake.just verify-handbrake EXPLICIT_REPOSITORY_ROOT`.
