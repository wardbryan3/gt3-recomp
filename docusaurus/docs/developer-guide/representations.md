---
title: Representations, partial layouts and the machine boundary
---

## Start with storage, not a convenient API

A byte can mean a signed direction, unsigned index or counter. The selector reads
signed request bytes but unsigned selected/maximum indices. Converting everything
to a host enum before tracing the original would discard invalid-byte behavior.
Likewise, original command halfwords may be digital truthy values or **Q12** fixed
point: 4096 represents 1.0 only on the analog path selected by the relevant flag.

Guest addresses are 32-bit values, not host pointers. A register also has upper
lanes and full-width address representations. Checking only its low word can
admit a representation the original bridge does not support.

A partial C++ layout names evidenced fields, leaves unknown bytes as padding, and
asserts size and offsets. `CarPartial::maximum_index` in the selector header is at
`0x20A`. The differential caught an earlier assumption of `0x210`. Do not bulk-copy
an entire partially known car back into guest memory; write only owned fields.

## EE floating-point is not interchangeable with host float

The recovered bridges transport floating values as `uint32_t` bit patterns and
use runtime EE operations such as `ps2::fp::key`, not reassociated host arithmetic.
Signed zero, denormals, exponent-255 patterns, rounding and FPU status can change
which path executes or what later original code observes. Existing tolerance
`2e-6` applies where specified; it does not permit weakening exact CPU/RAM/cost tests.

## ABI means more than the returned answer

The **application binary interface** includes arguments, scratch/preserved registers,
stack contents, return address and return PC. A whole-function replacement must
preserve its claimed outgoing state, not just the gear index. An interior recovery
must instead meet the exact state at its original join, retaining its containing
function's frame and continuation. Partial semantic projections are not whole ABI proof.

Instruction budgets represent guest execution cost. Branch paths and delay slots
have different costs; matching a scalar formula does not establish matching
scheduling. If safe admission cannot preserve an original preemption boundary,
reject before mutation and let original execution handle it. A host performance
speedup is a separate question from preserving guest accounting.

Read the [MT selector contract](worked-example-mt-selector/trace-and-contract.md)
and [implementation](worked-example-mt-selector/implementation.md) for a concrete
application, then the [validation guide](validation.md) for what must be compared.
