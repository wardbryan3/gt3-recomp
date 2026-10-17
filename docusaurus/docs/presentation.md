:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Presentation, performance and audio boundaries
---

The renderer, desktop/display modes, streaming settings and default launcher were preserved tonight. Existing GPU anisotropic and hardware/runtime regression assertions pass unchanged.

Earlier presentation report at `$GT3_LEGACY_ROOT/presentation/REPORT.md` demonstrates native virtual Wayland/WebGPU **5760×1080** presentation with **5760×1344 / 9×3** internal sampling. Clocked-audio game-frame requests were approximately60/sec, but occasional **33.33ms** presentation gaps remain. Strict smooth60FPS, three physical monitors, scanout and audible output are **not proved** by that evidence.

This initialization's clean validation uses **1280×240 native offscreen WebGPU readback**. It establishes generated/clean visual/state equality, not a new desktop/headless simulator feature, real-time benchmark or audio claim. Existing synthetic experiment's earlier native-window runs remain separately documented.

Before Checkpoint1 acceptance, a separate measurement cycle must define workload, warmup, duration, frame request versus submit versus actual presentation/scanout, pacing distribution/tail latency, audio underruns and audible output, drawable versus requested resolution, and actual triple-screen topology. Compare against preserved working settings before proposing changes. Do not modify renderer or system/desktop settings under a controls recovery request.
