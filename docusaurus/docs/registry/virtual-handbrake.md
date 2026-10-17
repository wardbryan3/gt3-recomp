---
title: Virtual handbrake authority
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


# Virtual handbrake v1 authority

Status: **validated-bounded**. Separate virtual-input experiment, not a Frozen processor change or canonical installation.

Protocol: finite normalized binary64 [0,1], nearest Q12 / positive half ties up; invalid input rejects, never clamps. Original floor/processing/downstream remain in GT3.

| Gate | Result |
|---|---|
| static_boundary | passing |
| protocol_oracle | passing |
| command_mutation_lifetime | passing |
| native_v3 | passing |
| default_off | passing |
| fresh_handbrake | passing |
| native_regressions | passing |
| public_source | passing |
| docs | passing |
| strict_evidence | passing |

49,170 original oracle cases /98,340 complete final CPU+32MiB comparisons;52 native-v3 runs /8,596 clean substitutions /zero fallback; all4,097 Q12 codes reached live.

12 representative contexts, seven v3 fixture identities, five UI-identified cars plus an unidentified Time Trial preset; Arcade Single Race/Time Trial/Free Run and Simulation B-1, AT and MT. This is bounded evidence, not all-game/browser/physical proof.

[Full report](../virtual-handbrake.md). Strict proof: `just --justfile virtual-handbrake.just verify-virtual-handbrake EXPLICIT_ROOT`. No raw evidence is published.
