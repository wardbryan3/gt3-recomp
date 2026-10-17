---
title: Products, gameplay ownership and PS2 bindings
---

`ps2run` is the permanent enhancement-free original generated reference.
`gt3-native` is the evolving playable product, original-equivalent by default.
They compile the same maintained `host/main.cpp` with explicit product definitions;
platform objects and runtime implementation are shared. The native host alone
retains inherited opt-in presentation support; this is not new simulator qualification.

`src/gt3/gameplay/controls/` and `src/gt3/gameplay/transmission/` own readable
implementations once. Domain-local tests check contracts; central
`validation/gt3/` owns independent differentials and cross-domain/live support.
Mixed gameplay/EE bridges were relocated, not silently converted to pure-native APIs.

Virtual transmission policy in `gameplay/transmission/virtual/` consumes typed host
intent. The concrete EE bridge in `bindings/ps2/virtual-transmission/` owns guest
profile, pointer, caller and execution constraints. Keeping policy separate does
not make an unvalidated continuation safe or imply a generic plugin interface.

The [generated product view](../reference/generated/current-products.md) lists
ownership and integration state. Compile checks and original fixtures do not mean
these gameplay libraries are linked into a product. See [enhancement isolation](enhancements.md)
and [authority rules](../reference/authorities.md).
