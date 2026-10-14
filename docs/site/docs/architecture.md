> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Architecture and boundaries
---

The working tree is deliberately additive. Existing `host/`, `runtime/`, `generated/` and scripts retain their paths. `decomp/gt3/` is the knowledge inventory, **not a competing runtime implementation**.

```mermaid
flowchart TB
  ISO[Preserved ISO / original ELF] --> AOT[recomp - EE / VU generators]
  AOT --> GEN[Generated game routines - behavioral oracle]
  GEN --> RT[runtime - CPU / EE fp / memory / devices / VU]
  RT --> HOST[host - native application / SDL / WebGPU]
  HOST --> PRESENT[Existing triple-screen rendering / presentation]
  CLEAN[Recovered steering semantics in host/gt3_clean_steering] -. guarded label gates .-> GEN
  SYN[Synthetic wheel experiment - separate opt-in] -. temporary input overlay .-> GEN
  KB[decomp/gt3 JSON knowledge base] --> DOC[Generated Docusaurus knowledge site]
  EV[Static REA / generated fixtures / live artifacts] --> KB
  GEN --> TEST[Differential tests]
  CLEAN --> TEST
```

## Current versus target layering

- **Original generated layer**: game code, simulation, consumers; preserve intact and executable.
- **Recovered semantics**: readable steering math/layouts. Current math and CPU bridge coexist in `host/gt3_clean_steering.cpp`; this is acknowledged historical placement, not falsely claimed complete separation.
- **Compatibility bridge**: guest memory copies, EE numerical behavior, instruction budgets, return state, label gates and fallback guards. Guest objects must not be host reinterpret-cast or padded regions bulk-written.
- **Modernization / host adapters**: future physical input/output translation, explicitly separate from original semantics. The synthetic adapter retains its own seams and observers.
- **Platform / rendering / devices**: runtime and host. No renderer/platform dependencies should enter a future recovered semantic routine.

```mermaid
flowchart LR
  FP[EE bit arithmetic] --> SEM[Recovered semantic functions]
  LAYOUT[Partial asserted layouts] --> SEM
  SEM --> BRIDGE[Guarded compatibility bridge]
  BRIDGE --> GATE[Generated entry / interior-label gates]
  GATE --> TAIL[Unchanged generated consumers and tail]
  CLI[Build option AND runtime flag] --> BRIDGE
  ADAPTER[Independent synthetic adapter] --> GATE
  OBS[Independent read-only observation] --> TEST[Differential / live verification]
  TAIL --> TEST
```

Direct generated-to-generated calls bypass dispatcher replacement. The steering experiment inserts gates in **copied generated bodies**, not only a function dispatch table. `001E4478` is only partially replaced; classification, curve selection and remaining controls are original. See [steering](steering.md).

Future directory migrations need a separate request and regression proof. Keeping the current build working is more important than an attractive directory tree.
