---
title: "Pedal v1 validation"
---

<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->

Source base: `46a32c70d414d87d192c2d00039365bbb59afb27` plus documented source overlay. Lifecycle: **frozen**. **Validation-only**, not canonical integration.

| Gate | Result |
|---|---|
| build | passing |
| differential | passing |
| regressions | passing |
| live | passing |

- Original USA v1.10 native runtime only; one trusted Super Speedway race fixture.
- Original generated oracle, not physical-PS2/physical-pedal proof; no browser or arbitrary-car/mode guarantee.
- Descriptors remain original generated calls with null derivative; no evaluator recovery.
- Semantic probe PC compared; stale direct-branch dispatch Cpu.pc retained separately in raw traces.
- Current-main validation-only gate; canonical ps2run remains generated-only.
- First live attempt correctly exercised fallback on the previously unsupported 0049AF50 BSS command buffer; retained unchanged. The explicit BSS context was audited with a new build, not forced past the guard.
- No steering/synthetic algorithm, renderer, recompiler, save-state format, coupling, transmission, clutch, handbrake, physical-device or FFB changes.

Use `just verify-pedals EXPLICIT_REPOSITORY_ROOT` for strict private verification. See [pedal recovery](../pedal-v1.md) and [join contract](../pedal-join-contract.md).
