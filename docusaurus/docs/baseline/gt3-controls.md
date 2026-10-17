---
title: "Historical: gt3-controls"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


> Preserved experiment narrative, not validation of current main. Commands refer to the historical runtime. Raw exports and game artifacts are private.

# GT3 controls: selective decompilation

## Target and status

Target: `games/gt3-usa-v110/core.elf`, extracted PBPX-95503 USA v1.10 core,
SHA-256 `b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
Static analysis uses Ghidra 12.1.4 with `r5900:LE:32:default`.

Readable code: `host/gt3_controls.hpp`. Differential harness:
`tests/gt3_controls_test.cpp`. These are standalone reconstructions, **not yet
installed as guest routine replacements or host controller mappings**.

Focused, source-bound pseudocode/assembly and Evidence IDs are retained in
`docs/gt3-controls-evidence.json`; it is an excerpt collection, not a complete
REA evidence bundle. Names below are ours, not recovered original symbols.

## Reconstructed paths

| EE entry | Readable helper | Status |
|---|---|---|
| `0x00210F90` | `normalize_mapped_input` | Existing helper, corroborated; positive sensitivities tested |
| `0x00217998` | `binding_index` | Reconstructed; covered through caller tests |
| `0x002178C8` | `mapped_channel(..., primary)` | Reconstructed; signed halfword at record +2 |
| `0x00217938` | `mapped_channel(..., secondary)` | Reconstructed; signed halfword at record +4 |
| `0x00211050` | `fill_mapped_actions(..., primary)` | Reconstructed and differential-tested |
| `0x002111C0` | `fill_mapped_actions(..., secondary)` | Reconstructed and differential-tested |
| `0x00211330` | No helper yet | Inspected threshold query |
| `0x00211430` | No helper yet | Inspected dispatcher; indirect calls unresolved |

### Mapping lookup

`0x00217998` reads a 32-bit binding index at:

```
mapping_base + bank * 0x50 + variant * 0x28 + action * 4
```

The wrappers then read a **signed** halfword from a six-byte record at
`0x002E2CF8 + binding_index * 6`, either +2 (primary) or +4 (secondary).
Any negative channel is treated as unmapped by the action routines. The first
halfword's role and table dimensions remain unknown. The C++ helpers assume
valid caller-owned arrays and indices; they do not emulate invalid guest pointers.

Evidence: `ev_3acb92c65732f7f382ce1053dc870b0fbcbbc72044c867d7076b3e811ace55dd`,
`ev_0a3f3fdcfae0293ea0d8e4932f8b3c20fec890bb9f98651da62a680c3a46cd73`,
`ev_21aec165142c345e5ed50e32ed71684a4df7927b07aba218fff37ced3d59d496`.
The wrapper pseudocode omits forwarded arguments; assembly shows that a0–a3
reach `0x00217998` unchanged. `lh`, rather than the decompiler's `undefined2`,
establishes signedness.

### Four mapped action values

Both routines visit action IDs **1, 2, 4, 3**, in that order. For each valid
channel they read a word at `input_object + 0x38 + (channel & 0xff) * 4`,
normalize its low byte, OR a bit into output byte 0, and store the result
shifted left four bits into a little-endian halfword:

| Action ID | Presence bit | Output offset | Primary sensitivity | Secondary sensitivity |
|---|---|---|---|---|
| 1 | `0x02` | `+0x08` | 100 | 35 |
| 2 | `0x04` | `+0x0A` | 100 | 65 |
| 3 | `0x08` | `+0x0C` | 100 | 35 |
| 4 | `0x10` | `+0x0E` | 100 | 20 |

A valid mapping with a zero input **still sets the presence bit**. An unmapped
action leaves its previous value and flag intact. Neither routine clears the
output block. Values normally span 0–4096, but unsplit stick channels retain
0–255 before shifting (maximum 4080). The reconstruction exposes the first
16 output bytes without claiming that this is the full object size.

Evidence: `ev_7134af55597a9dbcff3d70484fd13d09e7cbd99a0b3445b480a8cf57a1401994`
and `ev_d3721c632319b7933906eb15dd9817d1aacd3bf8e96511d2c7a3af523ba1941a`.

### Normalization and inspected callers

For channel low bytes 0–3, `0x00210F90` indexes the byte response curve at
`0x003416F8`. Bits `0x100` and `0x200` select the negative/positive half-axis,
respectively, centered on 128 and doubled with a zero floor. Other combinations
return the curved byte. Other channels double pressure, cap at 256, multiply
by 100, divide by sensitivity, and cap again at 256.

The original uses signed division/comparison and traps on zero sensitivity.
The existing C++ helper models positive sensitivities and throws for zero;
this is not a claim of trap equivalence or equivalence for negative/out-of-domain
sensitivity values.

`0x00211330` performs primary lookup, returns false for a negative mapping,
and otherwise tests `(normalized_value << 4) >= 0x800` at sensitivity 100.
For ordinary output values this means normalized value >=128.

`0x00211430` selects paths using `input_object[+0x14] & 0x1f`: 5/7 use the
primary routine, 8 uses secondary, and 4 takes a separate simpler path. It
obtains mapping and other state through unresolved virtual calls. A subsequent [steering trace](gt3-steering-trace.md) resolves the pad-ID table:
0x41 maps to type 4, 0x73 to type 7, and 0x79 to type 8.

Evidence: normalization
`ev_ddfbe374f8896acd31e66f958a765e27afde3edc8568e55ec7e1111f5d59269f`;
threshold `ev_53089c1d62ca912edc058a9dfd480ac45f1c9cace7c17f83535bcf20fedf4474`;
dispatcher `ev_1b6c14638b4821f607d91c46386620cfa9549707afda12753967f234d328e11d`.

## Validation

Run `tests/run_resolution_tests.sh` (defaults to `build/resolution-triple`).
On this pass:

- Normalization: **25,600 cases passed**, adding secondary sensitivity 20.
- Mapped actions: **57,344 cases passed** against generated EE routines,
  including the real lookup call chain, two curves, all 256 raw-byte values,
  two banks, two variants, both record fields, mixed valid/negative mappings,
  split-axis and pressure channels, nonzero raw high bytes, prefilled flags and
  halfwords, return PC, stack restoration, and trailing output guards.
- Existing anisotropic GPU and GT3 hardware regression tests also passed.

This is execution of the generated EE code under the project's runtime with
synthetic fixtures, not a physical-PS2 comparison or observed in-game input
trace. It tests valid table accesses and separate input/output allocations.

## Next investigation

1. Trace output-field consumers to identify actions (throttle/brake/etc. are
   plausible but **not established here**).
2. Resolve dispatcher virtual calls, mapping initialization, and table bounds.
3. Inspect `0x00211398`. Adjacent steering/digital routines have now been
   traced through the [wheel-angle consumer](gt3-steering-trace.md).
4. Recover response-curve construction. The shipped curve and pad-ID labels
   are now recorded in the steering trace.
5. Only then consider installing selective guest replacements, with tests for
   the surrounding output initialization and input-object lifecycle.
