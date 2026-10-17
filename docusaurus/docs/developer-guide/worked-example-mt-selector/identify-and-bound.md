---
title: Identify and bound the function
---

# 1. Identify and bound the function

## Why this function first

The private pre-implementation plan records the alternatives before the
boundary. Static dossiers rechecked the MT entry, its speed-selection callee,
and the policy dispatcher against the immutable USA v1.10 original (ELF
SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`).

`0x001E5458` was chosen because it is a meaningful, **bounded** selection and
rearm decision with existing policy-1 player fixtures. Nearby candidates were
rejected, each for a reason:

- `0x001E4E78` alone is only a small selection store, not a useful first
decision.
- AT entry `0x001E4FF8` and dispatcher `0x001E5690` would widen the policy
dependency closure (owner/mode/suppression/effective-policy selection).
- MT-adjacent selectors `0x001E5540` and `0x001E5600` depend on configurations
not independently reached.
- Admission, synchronization and power-transfer functions would prematurely
pull in unresolved owner/calibration/state branches.
- The EE floating-point speed search `0x001E4E80` can stay an **explicit
original dependency** instead of being modernized with the selection.

## Keep the evaluated source identities separate

The historical selector overlay began from
`edc65a105ba682449391a2d62c513af8b9005e53` and was an **uncommitted additive overlay**
identified by individual source hashes, not a claim that the base commit contained
the finished recovery. Its independent original oracle used source context
`82987dec7a71d76414adfff8663da5494a280938`. Today's relocated paths identify maintained
source; they do not repin either historical identity. The [research report](../../research/transmission/mt-selector-v1.md)
retains that provenance, failed attempts and original results.

## The boundary

One whole function: `0x001E5458..0x001E553B`, entry `0x001E5458`, no interior
tail, no invented resume address — `project/gt3/transmission.json` records
`boundary_kind: "whole-function"`, `resume: null`. Direct calls inside the
generated unit are covered by a whole-function **entry label** overlay, not a
dispatch-table hook.

## The dependency closure

```text
ORIGINAL command construction / manual processing / request delivery
  -> ORIGINAL 001E77E0: selection orchestration
     -> ORIGINAL 001E5690: owner/mode/suppression/effective-policy dispatch
        -> CLEAN 001E5458..001E553B: MT selection and inhibition/rearm
           -> ORIGINAL 001E4E80: speed-based forward-index search, if required
     -> ORIGINAL state write at 001E77E0, if a selection was accepted
     -> ORIGINAL 001E4E78: commit selected index
  -> ORIGINAL admission, engine, driveline, differential, wheels, chassis
     (on their established update schedule)
```

Only the middle `CLEAN` line is replaced. The caller still chooses the
effective policy; the consumer still writes transition state and commits the
index. The helper `0x001E4E80` is **retained generated** — its own recovery has a
separate composition, separate proof and separate approval; this checkpoint's
counts do not claim it.

## Bounding discipline

"Bound" means the pre-code plan also pins the outgoing ABI, the guards, and
the tests to run — before any code, the exact reads, write set, register/time
obligations, and rejection behavior were written down. Everything in
[chapter 2](trace-and-contract.md) is the result of that trace.
