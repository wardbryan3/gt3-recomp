---
title: Differential validation, oracles and test layers
---

# 4. Differential validation

## The independent oracle

The oracle is identity-checked `generated-original/unit_0039.cpp` from the
retained baseline (oracle source context
`82987dec7a71d76414adfff8663da5494a280938`) — **not** a new whole-game
translation at documentation HEAD. Only its exported unit symbol, self-call
binding and entry-array symbol are renamed to coexist with the overlay;
reversing those renames reproduces the exact original file. No original
instruction, helper body, comparison or budget is replaced. The independent
original supplies the expected side; the clean implementation never generates
its own expected values.

`cmake/gt3-validation.cmake` gates the layer: it requires `PS2_GENERATED` and
an existing `GT3_ORIGINAL_ELF`, hard-failing unless the ELF's SHA-256 matches
the pinned original profile. The isolated differential is registered as
`gt3_original_transmission` from
`validation/gt3/differential/gt3_transmission_oracle.cpp`.

## Case comparison vs memory comparison

Each case compares at three scopes:

- **Complete CPU every case** — all 32 general registers, FP registers and FCR,
  PC and remaining budget, clean vs original, exact bit equality. The existing
  `2e-6` floating tolerance is untouched; this recovery compares bits exactly.
- **Entire car + padding and entire 16-byte stack frame every case.**
- **Whole 32 MiB every 1,024th case**, plus a cumulative out-of-contract
  mutation check at the end (fixture-owned bytes restored; any other mutation
  fails).

Exact dynamic cost is checked each case, with min/max retained. The isolated
sweep exhausts the stated byte axes for selected index, inhibition and signed
requests (not their entire Cartesian product together with every other input), FP edge bit patterns (signed zero, denormals, ±infinity,
NaN), RPM values and budgets, including a forced 254-iteration original speed
traversal and a budget/depth edge matrix. Historical result: **663,959**
cases, complete CPU each, complete car/padding and stack every case,
**649** whole-32-MiB comparisons.

The same test's tail runs the **rejection contract**: **20** fallback cases
(disabled, profile, pointer, alias, stack-alignment, depth, budget), each
proving the CPU and all 32 MiB are unchanged.

## Wrapper vs the isolated oracle

The wrapper test, `validation/gt3/differential/gt3_transmission_wrapper.cpp`,
is a different layer: it starts at original `0x001E77E0` and runs the whole
chain `001E77E0 → 001E5690 → clean 001E5458 → original 001E4E78`, comparing
complete CPU + 32 MiB against the fully original chain across states 0–3,
indices 0–6, rearm values and request combinations — historically **1,008**
cases, **1,008** real gated replacements, zero fallback. It proves the clean
body composes inside the original dispatch, state-write and commit consumers.

## Reproduce only the layer you can supply

`just test` builds/runs `gt3_transmission_source_test` without game bytes. Inspect
`src/gt3/gameplay/transmission/tests/gt3_transmission_source_test.cpp`: `enabled`
starts false; enabling it in synthetic zero-filled RAM still fails the original
fingerprint; rejected calls must leave the CPU and all RAM unchanged. Its dispatch
stub aborts if called. This proves public guard/default consistency, **not** the
accepted selector behavior or historical differential counts.

With separately supplied original inputs and an explicitly qualified product
receipt, `just original-fixtures RECEIPT NEW_NAME` runs the current source/original
layer; the [validation guide](../validation.md#optional-current-original-fixtures)
describes the explicit ELF/generated-source CMake contract. Historical reproduction
uses `just verify-transmission ROOT` against exact registered predecessors. Missing
private inputs must fail. None of these commands installs the recovery.

CMake distinction: the current test list registers the **oracle** differential
(`gt3_original_transmission`) plus the separate speed and state oracles. The
**wrapper** file is retained under `validation/gt3/differential/` but is built
by the historical bespoke builders, which are retired — it is not a current
CMake target. Do not infer that a passing current CMake re-ran the wrapper.

These layers are not live game launches, not a virtual shifter; no test edits
calibration or supplies new driver commands. Next: [where actual native
processes matter](live-validation-and-lessons.md).
