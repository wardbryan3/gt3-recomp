---
title: The clean implementation and its ABI obligations
---

# 3. Implementation: preserving the outgoing EE ABI

## What "recovery" means for one function

`src/gt3/gameplay/transmission/gt3_clean_transmission.cpp` re-implements the
decisions in C++, but a correct-looking gear number is **not** the contract.
Later generated code can observe everything the EE left behind, so the bridge
preserves the complete outgoing CPU, not just the selection:

- Scratch registers `v0/v1/a0–a3` and their path-dependent values, plus
  preserved upper lanes within the 128-bit general registers — no host
  calling-convention shortcut.
- The original 16-byte stack frame: incoming RA low 64 stored at `SP-16`, RA
  and SP restored, return PC taken from original RA low 32.
- The accelerator comparison's **FPU condition** effect (the `FCR` condition
  bit), and, on the helper path, the helper's full FP/scratch and cost
  semantics.
- All other CPU fields, FCR bits, HI/LO/SA/base and RAM stay exact; body RAM
  writes are only the saved-RA slot and, on applicable paths, `car+0x13BE`.
- Delay-slot and branch-likely effects and the **exact dynamic instruction
  budget**; observed isolated costs are **13–4,103**, including the longest
  tested 254-iteration original search.

The source epilogue does the ABI bookkeeping: reload the saved RA low 64, cost
three instructions, restore `SP+16`, and take the return PC from RA low 32.

The internal `Execution` object keeps the low-level obligations local: `word()`
uses `ps2::set32`, `signed_byte()` sign-extends the original byte, `cost()` adjusts
guest accounting and `finish()` restores the original caller. `select()` expresses
the traced branch order. This public-source accepted-upshift tail illustrates why
“return selected + 1” alone would lose state:

```cpp
e.word(2,selected+1);       // outgoing v0, including EE extension semantics
ps2::st8(car+0x13be,1);    // rearm/inhibit future relative requests
e.cost(3);                 // this path's guest instruction accounting
e.finish();               // stack, RA, return PC and epilogue cost
return;
```

Floating-point work uses EE bit-pattern operations (`ps2::fp::key`), never host
`double` arithmetic, so signed zero, denormals, infinities and NaNs compare
independently against original execution. The only recovered decision body is
the MT function; the retained helper is **not** claimed recovered merely
because it is called.

## Guards and the no-mutation fallback

`replace_manual_selector` must decide **before any CPU/RAM mutation** whether
it is allowed to run. Admission checks require original body and helper
fingerprints (`profile_matches()`); full 64-bit pointer representations in
`a0`/`a1`/`SP` (low32 equal full64); bounded ordinary RAM ranges with aligned
car (4) and stack (16); the original GP value `0x3579F0`; non-overlapping
stack/car/request regions, with the
low protected region (`0x100000–0x400000`) covering the original loaded image
and GP constants and aliases into it rejected; either the native `car+0x1304`
request pair or a disjoint pair; and no near signed-budget overflow.

The helper path adds a depth limit and a conservative remaining budget of
`16*maximum_index+64`, sufficient for the entire bounded original loop —
derived from the original byte maximum, not a magic 10,000. Any failure
increments `counts.fallback` and returns `false` **before** mutation, so the
original generated code executes unchanged. These are bounded structural
guards, not all-car/all-thread coverage; validation uses the existing
single-thread deterministic native setup.

The **historical validation host** used `--gt3-clean-transmission`; its build-OFF
binary rejected the request and both gates defaulted OFF. Trace-only and build-OFF
paths executed original bodies. This is not a supported current product switch:
no current gameplay hook is installed. Use [validation](../validation.md) for
current source-only and original-fixture commands, not an old overlay launch recipe.

Next: [proving it with independent oracles](differential-validation.md).
