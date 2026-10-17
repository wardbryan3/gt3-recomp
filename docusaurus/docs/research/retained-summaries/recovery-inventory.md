:::note Superseded inventory

Use [current ownership](../../reference/generated/current-products.md) and
[bounded research](../index.md). This old inventory is not current integration status.

:::

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# GT3 selective decompilation

Understand and reconstruct only what the current milestone needs, preserving
original behavior before modernization. This is not whole-game source recovery.

## Source checkpoint

- `host/gt3_controls.hpp`: normalization/binding/mapped-action references.
- `host/gt3_clean_steering.*`: bounded EE-compatible normalization, shipped wheel
  builder, stick filter and interior steering envelope, plus partial guest types.
- `host/gt3_synthetic_wheel.*`: independent scoped adapter source.
- `decomp/gt3/{manifest,symbols,types,provenance}.json`:132 selected records,
 129 canonical functions, private artifact/evidence references and explicit context.
- Original-dependent test source is preserved; current source-only compilation and
  synthetic consistency do not replace independent original differentials.

Four frozen statuses describe the old validated private experiment. Current main
compiles the source library but does NOT install runtime/generated label gates.
Revalidate that integration before enabling anything. No downstream physics rewrite.

Public docs are curated findings/metadata. Raw assembly, pseudocode exports,
original images/tables and generated game bodies stay private. See HANDOFF.md,
docs/gt3/PUBLICATION.md and the site's bounded queue for next work; the queue does
not authorize implementation. Pedals/FFB/AI/reset/step remain separate cycles.
