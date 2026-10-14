> **Evidence context:** original checkpoint narrative below is historical. Fresh current-main native build/fixture/live validation is recorded separately in [current baseline](current-baseline.md); canonical ps2run still has no recovered runtime installation.

---
title: GT3-native selective decompilation
slug: /intro
---

Recover only what the checkpoints require. Keep the generated implementation executable as the oracle. **Recover original behavior before modernizing it.** This is a private local GT3 USA v1.10 research workspace, not a source release of the game.

## Where to start

1. [Permissions and agent rules](permissions.md): changes need a bounded request.
2. [Getting started](getting-started.md): local tools, isolated builds, tests, docs.
3. [Frozen steering baseline](steering.md): four default-OFF substitution sites; originals remain available.
4. [Pedal discovery](pedals.md): the next dependency-ordered recovery candidate, **not implemented tonight**.
5. [Morning report / handoff](handoff.md) and [prioritized queue](queue.md).

The machine-readable authorities are `decomp/gt3/{manifest,symbols,types,provenance}.json`. Status/type/symbol pages are generated from them. Retained static evidence lives in the original `docs/*-evidence.json` and `evidence/rea/project-init.json`; fixtures and running-game observations are explicitly separate.

No physical-wheel support, pedal injection, shifter, clutch axis, modern force-feedback mapping, AI interface, deterministic reset/step API, Windows port or physics replacement was added during initialization. Existing synthetic steering and clean steering remain independent opt-ins. Existing files were not moved.

**Initialization complete; stop and await an explicit next-cycle request.**
