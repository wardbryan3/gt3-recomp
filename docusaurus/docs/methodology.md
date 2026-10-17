---
title: Methodology and evidence levels
---

## Recover, prove, then seek separate approval

1. Work within explicit authorized scope; choose a milestone necessity and the
   smallest observable contract. A queue entry is not authorization.
2. Preserve original identity and the independent executable oracle; inspect
   retained evidence before requesting new analysis.
3. Trace producers, mutations, units/representation and consumers, including
   fallback paths. Establish partial layouts with honest unknowns and offset
   assertions rather than inventing a complete class.
4. Reconstruct readable behavior **without cleaning up original quirks**: preserve
   EE floating-point bit patterns, integer wrap/signedness, zero/invalid behavior
   and the applicable numerical tolerance.
5. Differential-test original versus recovered behavior, including relevant bytes,
   calling convention (ABI), returns, mutations and dynamic instruction cost.
   Original-only fixtures and fallback execution are not replacement proof.
6. Where separately authorized for validation, test enabled, disabled and trace-only
   paths in an isolated game context, with build/runtime gates default OFF. Keep
   the original oracle enhancement-free; bounded validation is not installation.
7. Present the bounded proof and limitations for **separate explicit product
   approval**. Neither passing tests nor a historical Frozen label grants approval.
   Any approved temporary fallback must be observable, tested and have an exit
   criterion; it is not a permanent second gameplay implementation.

Use the [current workflow](workflow.md) for commands and
[current authorities](reference/current-authorities.md) for proof/approval records.

## Evidence is not interchangeable

| Category | What it establishes | What it cannot establish alone |
|---|---|---|
| Original assembly/data, aided by REA | Profile-specific instruction/data findings checked against the original | Live object state, hardware calibration, real timing |
| Generated EE fixture | Executed original code in a controlled constructed state | Actual stock-car configuration, physical device behavior, arbitrary races |
| Differential fixture | Equivalence within tested state/domain | All possible modes, physical-PS2 numerical identity |
| Running native game | Actual integration with dynamic objects and downstream consumers | Every car/track, long-session reliability, audible/physical-display output unless measured |
| Measured physical simulator | Tested device calibration, output and display/audio behavior | Untested devices, configurations or long-session reliability |
| Hypothesis / naming inference | A prioritized investigation target | A recovered contract or authorized replacement |

## Reading retained experiments

In the historical private experiment, the 22 pedal discovery fixtures were
**original-only propagation checks**, not clean/native differentials or live
pedals. Historical steering live checks compared genuinely independent original
and clean executions; clean semantic observers were bridge observations, not
proof that skipped EE instructions ran. These populations and evidence classes
must remain separate from later pedal closure and current product qualification.

REA/decompiler pseudocode is an analysis aid, not the behavioral authority. It
can have incomplete EE signatures, caller/return types and canonical containment.
Requests at interior addresses may resolve to a different containing function. Use
assembly/generated instructions before selecting boundaries; never turn requested
selectors into asserted entry points automatically.

Retain failures and remediation when needed for active verification. In the
historical pedal experiment, an initial fixture aborted because a zero rev-limit
configuration cut torque; the synthetic engine configuration was fixed, assertions
were not relaxed. Qualify a new observation separately rather than rewriting an
old conclusion to hide a contradiction. Regenerate disposable outputs where
practical; do not create a new evidence archive or preservation system.
