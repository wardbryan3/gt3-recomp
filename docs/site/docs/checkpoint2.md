> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Checkpoint 2 — limited reconnaissance only
---

Future objective: repeatable AI-controllable episodes with trusted actions, observations, race semantics, reset and bounded time advancement. Initialization **does not implement any of these interfaces**.

| Need | Evidence now | Unknown / next proof |
|---|---|---|
| Telemetry | Steering/angles live-proven; engine rate/display conversion and motion candidates static | Units, frames, ownership, lifetime, sampling atomicity |
| Race state / lap / finish | Race car-slot getter and UI/lap labels identified | Exact lap counter, event writers, finish/failure transitions not established |
| Reset | Existing snapshot continuation works for bounded steering validation | Full host/runtime state, deterministic replay, input/audio/render side effects |
| Controlled step | Existing frame count and frame-limit CLI | Frame versus physics tick versus presentation; resumable atomic step not proved |

See [telemetry candidates](telemetry.md) and [reset/step limits](reset-step.md). `001EB218` is a broad vehicle post-update orchestration candidate, **not a proven lap-count routine**. A `RaceLapTime` or `LapCountLabel` string is an investigation seed, not a recovered race-state API.

Do not add headless/accelerated execution, AI sockets, action APIs, resets, episode wrappers or nondeterministic telemetry collection under this discovery request. New read-only probes themselves require scope/behavior-neutrality validation. Checkpoint1 original control contracts and usable native operation come first.
