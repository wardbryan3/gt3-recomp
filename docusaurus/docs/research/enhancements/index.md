---
title: Enhancement research — isolated policy, separate proof
---

The [architecture proposal](architecture-proposal.md) separates recoverable original
mechanisms from optional native policy. The [stopped boundary audit](stopped-boundary-audit.md)
records why a proposed path could not proceed: missing request-boundary,
commit/engagement and reachable-admission proof were real gaps, not an invitation
to enlarge the change silently.

The later [virtual-transmission v1 experiment](virtual-transmission-v1.md) has its
own source closure, tests and bounded evidence. It preserves failed attempts,
OFF equivalence and ON policy assertions separately. Historical AT/input limitations,
anti-stall and mode semantics are part of that contract, not global promises.

Changing which original stores occur changes behavior. Do not describe virtual
held-clutch/free policy as an original physical clutch model. Do not add its ON
runs to an original-default product count or infer integration from “Frozen.”
Current products do not install it. See [enhancement architecture](../../architecture/enhancements.md)
and [authorization](../../reference/authorization.md).
