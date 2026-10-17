---
title: Trace and the exact contract
---

# 2. Trace and the exact contract

## Inputs, reads and the exact offsets

EE calling convention: `a0` is the original car pointer, `a1` the requests
pair. All reads were traced from the original and asserted in
`src/gt3/gameplay/transmission/gt3_clean_transmission.hpp`:

| Input/read | Role |
|---|---|
| `a0` | Original car pointer |
| `a1+0` / `a1+1` | **Signed** auxiliary / **signed** relative requests; not absolute gear commands |
| `car+0x13BA` (u8) | Current selected ratio index |
| `car+0x13BE` (u8) | Inhibition/rearm countdown |
| `car+0x20A` (u8) | Configured maximum selection/search index — **not** `+0x210` (chapter 5) |
| `car+0x13AC` (EE bits) | Processed accelerator, for the Reverse-to-forward route |
| `car+0x140C` (EE bits) | Speed supplied to the original search helper |
| Helper GP constant, RPM calibration, ratio array | Read **only** by retained `0x001E4E80`; never a host table |

The partial layout (`CarPartial`, total `0x1410`) makes the offsets
compile-time facts, not prose, and its opaque `unknown*` padding is read-only:
it describes reads and is **never bulk-written**. For example, these declarations
from the public header turn the request width and maximum-index offset into checked
facts:

```cpp
struct Requests { std::int8_t auxiliary, relative; };
static_assert(sizeof(Requests)==2);
static_assert(offsetof(CarPartial,maximum_index)==0x20a);
```

The `accelerator_bits` and `longitudinal_bits` fields are `std::uint32_t` storage
for original FP bit patterns, not host physics values to recompute.

## Result and domain conventions

- Return is original `v0`: **`-1` (all-ones 32-bit) for no accepted selection**,
  otherwise an accepted ratio index in the unsigned-byte domain.
- **0 is Reverse, not Neutral.** No Neutral sentinel exists in this contract.
- The function does **not** commit the selected index, change transition state,
  or compute drive; a changed ratio can coexist with state 0.
- Requests are **signed** bytes (`std::int8_t`); sign is bit 7 of the raw byte
  — not an assumed −1/0/+1 enum, not a host `char` type.
- Invalid byte indices and zero maxima are **not repaired or clamped**; the
  helper-zero-to-one quirk is preserved even for a synthetic zero maximum.

## Decision order (highest priority first)

1. Nonzero auxiliary request: return Reverse if the current index is nonzero;
   already Reverse means no change. Bypasses the countdown.
2. While Reverse (index 0) and the original accelerator comparison is nonzero:
   call original `0x001E4E80` with the original speed; its zero becomes forward
   index 1. Precedes ordinary rearm.
3. Nonzero inhibition count: decrement modulo the byte store; reaching zero
   with a held relative request rearms it to 1; return no change.
4. Count zero: positive signed request increments only below the configured
   maximum; negative decrements only from index ≥ 2; an accepted relative
   selection writes inhibition 1; otherwise no change.

## Original helper dependency

Decision 2 is the one outgoing call: the original EE speed search `0x001E4E80`,
still generated. It owns its FP/scratch registers, rate conversion, division
and comparisons; the clean body preserves that ABI
([chapter 3](implementation.md)) but interprets nothing beyond the original
return. Recovering the helper is a **separate** composition — the
[speed-search report](../../research/transmission/speed-search-v1.md).

Next: [how the implementation honors this contract](implementation.md).
