---
title: Handbrake v1 authority
---

<!-- Generated from decomp/gt3/handbrake.json. -->

Lifecycle: **frozen**, bounded validation-only. Build/runtime default OFF. Canonical gameplay is generated-only.

| Gate | Result |
|---|---|
| static | passing |
| exact_join | passing |
| stateful_transitions | passing |
| original_downstream | passing |
| native_v3 | passing |
| default_off | passing |
| public_regressions | passing |
| native_regressions | passing |
| strict_evidence | passing |

Only 001E4BB8–001E4C5F is substituted, resume001E4C60. See [semantics, proof and limits](../handbrake-v1.md).

Strict private proof: `just --justfile handbrake.just verify-handbrake EXPLICIT_REPOSITORY_ROOT`.
