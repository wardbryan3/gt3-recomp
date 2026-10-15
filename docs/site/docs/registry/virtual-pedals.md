---
title: Virtual pedal v1 experiment
---

<!-- Generated from decomp/gt3/virtual-pedals.json. -->

Status: **validated-bounded**. Isolated validation only; build/runtime gates default OFF; no canonical installation.

| Gate | Result |
|---|---|
| parser | passing |
| oracle | passing |
| live | passing |
| regressions | passing |
| strict | passing |
| public | passing |

Host [0,1] maps to Q12 0–4096, positive half ties up, at original command-builder return. No processed car writes or physical calibration. See [experiment report](../virtual-pedals.md).

Strict private verification: `just verify-virtual-pedals EXPLICIT_REPOSITORY_ROOT`.
