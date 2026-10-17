---
title: Platform and presentation experiments
---

These are historical experiments, not current machine provisioning or hardware
qualification. Exact bases, source deltas, failed approaches and measurement
limitations stay in the reports.

- [Resolution](resolution.md): **5760×1080 output** versus **5760×1344 internal**
  sampling (9×3); camera projection geometry, not stretching. Retains `0017E888`,
  `002F424C`, **20,480** normalization cases, upstream base `b6482fb4…`,
  Silentwarior112 attribution and anisotropic snapshot markers.
- [Presentation](presentation.md): **17 runs/72,000 guest frames**. FIFO improved
  pacing in a qualified setup but had buffering/latency costs (including a
  **62.5 ms median request-feedback** repeat), residual **33.33 ms** gaps and no
  physical-scanout/audible-output proof. The sampling and extra-final-present
  fence mistakes remain important negative results.
- [LAN streaming/input](lan-streaming.md): RGBA/BGRA metadata correction, seqlock
  readback, center-crop composition and LAN-only ICE qualification. Historical
  endpoints, firewall rules and service commands are not current instructions.

Native product inheritance does not freshly qualify these measurements, upstream
status, browser execution, triple physical scanout or synchronized sound. Current
run controls and renderer limitations are in [build/run](../../developer-guide/build-and-run.md)
and [validation](../../developer-guide/validation.md). No services or network rules
are changed by reading or building this documentation.
