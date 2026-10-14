> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Goals and checkpoints
---

## Checkpoint 1 — usable native racing simulator

A working native GT3 racing experience: original handling, eventual physical controls, recovered original-intent force feedback, triple-screen presentation, stable performance and audio. Present achievements do not establish all these promises.

```mermaid
flowchart LR
  N[Working native generated runtime] --> S[Verified steering boundary]
  S --> P[Recover throttle / brake]
  P --> T[Transmission / clutch / handbrake contracts]
  P --> I[Physical report calibration and adapter - future]
  T --> I
  N --> O[Trace original output / FFB]
  O --> F[Original-intent FFB recovery - future]
  I --> C[Checkpoint 1 acceptance]
  F --> C
  D[Existing triple presentation] --> R[Measure stable pacing / audio / displays]
  R --> C
```

Physical adapters must be a **separate modernization layer** over recovered original contracts. Do not substitute a generic simulator's pedal, steering or FFB model. Leave unrelated physics and game systems generated.

## Checkpoint 2 — future AI-controllable simulation

Only reconnaissance now: trustworthy telemetry, race-state transitions, reset semantics, controlled stepping, timing and observation. Game state loading and frame counts alone do not prove deterministic episodes. No AI/headless/accelerated simulation implementation is authorized.

```mermaid
flowchart TD
  C1[Checkpoint 1 original contracts] --> OBS[Read-only telemetry contract]
  OBS --> STATE[Race / lap / finish semantics]
  SNAP[Existing snapshots] --> RESET[Prove reset equivalence including host state]
  RESET --> STEP[Prove bounded step and timebase semantics]
  STATE --> C2[Future Checkpoint 2 acceptance]
  STEP --> C2
  OBS --> C2
```

## Excluded recovery

Full-game decompilation, general physics rewrite, menus/AI/assets unrelated to checkpoints, Windows, new wheel features tonight, physical-device polling tonight, modern FFB invention, faster-than-real-time or deterministic-control implementation. An interesting address is not authorization to recover it.
