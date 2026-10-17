---
title: Worked example — manual transmission selector
---

# Worked example: recovering one bounded function

This folder walks one complete, real recovery cycle: the **manual transmission
selector**, the whole original function at `0x001E5458–0x001E553B` — a small
decision function, **not** a gearbox, clutch, or whole transmission. It
answers one question per call: "which ratio index now, or no change?"

The cycle taught, end to end:

**Identify → Trace → Recover → Differential Validate → (Opt-In Integrate) →
Live Validate → Freeze.**

| Chapter | What you learn |
|---|---|
| [1. Identify and bound](identify-and-bound.md) | Choosing the function and its dependency closure |
| [2. Trace and contract](trace-and-contract.md) | Exact inputs, offsets, signedness, return |
| [3. Implementation](implementation.md) | CPU, stack, FP and cost obligations, guards |
| [4. Differential validation](differential-validation.md) | Independent oracle, isolated test, wrapper test |
| [5. Live validation and lessons](live-validation-and-lessons.md) | Live matrix, shadow/substitution, mistakes, limits |

**Boundaries to keep.** The historical experiment was validation-only: its build
and runtime gates defaulted OFF, unsupported contexts fell back to original code
before mutation, and “Frozen” identified the exact evaluated disposable overlay —
never canonical installation. Current products do not link this recovery or expose
its old validation-host switch. Counts are source-pinned in the
historical report [mt-selector-v1](../../research/transmission/mt-selector-v1.md).

Current sources: `src/gt3/gameplay/transmission/gt3_clean_transmission.hpp`
and `.cpp`; tests: `validation/gt3/differential/gt3_transmission_oracle.cpp`
and `gt3_transmission_wrapper.cpp`; registration: `cmake/gt3-validation.cmake`;
authority: `project/gt3/transmission.json`. General layers:
[validation guide](../validation.md).

## Terms used throughout

- **EE** — the PS2 *Emotion Engine* main processor, with 32-bit guest addresses
  and 128-bit general registers. This bridge recovery uses host C++ to reproduce
  the bounded CPU, memory, FP and guest-accounting effects; that is not a claim of
  identical host timing or physical-PS2 timing.
- **ABI** — the outgoing calling convention: scratch registers
  (`v0/v1/a0–a3`), stack frame layout, return register, exact dynamic
  instruction budget. A correct gear number is not enough.
- **Q12** — a fixed-point representation with 12 fractional bits (4096 = 1.0
  on the qualified analog control path). It appears in upstream control research,
  **not** in this selector's decision inputs. The retained helper consumes EE
  floating-point speed bits, not a Q12 pedal value.
- **Oracle** — independent original execution establishing expected behavior; a
  **differential test** compares original vs recovered under equivalent inputs.

Read in order; each chapter links the next.
