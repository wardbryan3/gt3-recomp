---
title: Historical reset and controlled-step reconnaissance
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence boundary:** snapshot continuation and bounded replay tests are not a headless episode API. The earlier reconnaissance and later native-v3 fixture below are separate historical contexts. See [current authorities](reference/current-authorities.md) for present product and proof status.

## Existing primitives, not a controlled-step contract

The runtime declares **save_state**, **load_state** and **frame_count** in
`runtime/include/ps2/system.hpp` and
implements them in `runtime/src/system.cpp`
(`frame_count` returns `g_frames`). The CLI's bounded frame continuations and
scheduled absolute-frame button/wheel events were used for steering validation;
that use did not add a resumable, atomic simulation-step or episode-reset interface.

## Separate fixture contexts

The earlier race-start snapshot SHA-256 is **154077352bb0b738fa65fe52ce878d1bf378e43805a285ee84c4b77e3a62af07** and was reported to resume guest frame4801. Repeated original/clean runs gave exact bounded state/capture equality in tested cases. This is local regression evidence for that fixture, **not deterministic reset certification**.

The later [historical native-v3 baseline](current-baseline.md#native-v3-fixture-construction)
used a separately identified normal-boot v3 fixture, not conversion of that old
snapshot. It explicitly saved frame **4801**, with continuation input beginning at
**4802**: `vblank()` had already sampled frame-4801 input before requesting the
save. Supplying new input at 4801 only on uninterrupted boot was not equivalent to
loading the saved state. With external UTC input pinned, the recorded bounded
uninterrupted/resumed comparison matched guest dumps and captures. Independent
boots compared defined serialized bytes while accounting for proven native Thread
padding, not raw-file identity or all host/external state. These later checks
resolve specific replay assumptions; they do not certify arbitrary episode resets,
old-state compatibility or exactly N simulation updates per CLI frame limit.

## Controlled-step and reset proof gaps

The earlier Checkpoint 2 objective was repeatable AI-controllable episodes with
trusted actions, observations, race semantics, reset and bounded advancement.
Snapshot load plus a frame counter establishes neither that interface nor its
correctness. Remaining contract questions include:

- Completeness/versioning of serialized EE/IOP/SPU/devices, VU/DMA/timing, host-side input schedules, audio clocks/buffers, GPU state/caches and external resources.
- Boundary between guest frames, physics updates, interlace/vertical blank, frame requests, renderer submit and host presentation.
- Safe quiescence/resume and whether pending device work or callbacks can change the first post-load observation.
- Whether a future controlled step can advance exactly N simulation updates without accidentally consuming actions or dropping observations.
- Determinism under repeated restore/action sequences and independent process runs, including pads, time, random state and device effects.

## Requirements for separately authorized work

Future proof should define the initial/reset state, replay the same action/time sequence independently, compare complete relevant state and observations at each tick, test disabled/trace-only neutrality, and explicitly state any excluded rendering/audio nondeterminism. Do not merely wrap the existing save/load function as an AI episode API. This reconnaissance implemented no headless, faster-than-real-time, deterministic step or episode-reset API. Such work requires separate bounded authorization; the list above is not a work order.
