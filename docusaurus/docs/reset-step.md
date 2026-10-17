:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Reset and controlled-step reconnaissance
---

Existing `runtime/src/system.cpp` exposes **save_state**, **load_state** and **frame_count** (`g_frames`). Existing CLI runs bounded frame continuations and scheduled absolute-frame button/wheel events. These were already used for steering validation; initialization did not add a reset/step interface.

The race-start snapshot SHA-256 is **154077352bb0b738fa65fe52ce878d1bf378e43805a285ee84c4b77e3a62af07** and resumes guest frame4801. Repeated original/clean runs give exact bounded state/capture equality in tested cases. This is strong local regression evidence, **not deterministic reset certification**.

Unknowns that block Checkpoint2 acceptance:

- Completeness/versioning of serialized EE/IOP/SPU/devices, VU/DMA/timing, host-side input schedules, audio clocks/buffers, GPU state/caches and external resources.
- Boundary between guest frames, physics updates, interlace/vertical blank, frame requests, renderer submit and host presentation.
- Safe quiescence/resume and whether pending device work or callbacks can change the first post-load observation.
- Whether a future controlled step can advance exactly N simulation updates without accidentally consuming actions or dropping observations.
- Determinism under repeated restore/action sequences and independent process runs, including pads, time, random state and device effects.

Future proof should define the initial/reset state, replay the same action/time sequence independently, compare complete relevant state and observations at each tick, test disabled/trace-only neutrality, and explicitly state any excluded rendering/audio nondeterminism. Do not merely wrap the existing save/load function as an AI episode API. No headless, faster-than-real-time, deterministic step or reset implementation is authorized now.
