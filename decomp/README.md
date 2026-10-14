# GT3 readable reconstruction roadmap

The goal is to understand and progressively reconstruct GT3 behavior, alongside
its working local static-recompilation path. This is not a completed source
recovery and not an invitation to commit bulk decompiler output.

## Current reference

`host/gt3_controls.hpp`: readable input normalization, tested locally against the
actual translated EE routine for 20,480 cases with positive sensitivities.
The runtime still executes the translated game routine. Negative/high-bit or zero
sensitivity semantics are not interchangeable: the original uses signed division
and a trap at zero; the reference's domain is narrower. No original response-curve
data is distributed; test curves are synthetic.

## Next useful graphics work

- Map one deterministic frame's EE submissions, DMA/VIF/GIF traffic and GS state.
- Associate visible road/car/scenery/mirror/HUD passes with their producers.
- Trace projection and HUD layout before trying further patches.
- Identify VU programs through disassembly/traces; standalone VU decompilation
  support has not been established.
- Build reviewed replacements only after understanding their interfaces and
  equivalence domain; preserve a reference/differential test path.

Maintain a factual symbol ledger with confidence/provenance and test names.
Keep raw assembly, pseudocode exports, memory and original program images in
ignored local storage. Review new recovered code under
`docs/gt3/PUBLICATION.md` before making it public.
