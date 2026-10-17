---
title: Execution — from ISO to native process
---

A legally supplied supported ISO enters `scripts/project/products.py` through
`just build-game ISO NEW_NAME`. Extraction and bounded scene discovery find EE
entries and VU programs. The inherited recompilers generate native source representing
PS2 execution; this is not yet readable, PS2-independent recovered gameplay.

Assembly independently regenerates the source set and checks its identity, then
passes an explicit source list to CMake. Both products consume shared `ps2game`
and inherited runtime code. Receipts record inputs, tools, compiler settings,
link closure and outputs privately. A bounded discovery run cannot prove every
scene's entry/program coverage.

At runtime, generated code can call other generated functions directly. Dispatch
interception alone therefore cannot establish replacement coverage. Historical
validation overlays used original entry-label or interior-label gates in disposable
outputs, not edits to canonical original inputs. Current products install neither
those clean gameplay gates nor the enhanced virtual-transmission binding.

See the [build guide](../developer-guide/build-and-run.md), [architecture overview](index.md)
and [validation layers](../developer-guide/validation.md). Game source, translation
outputs and linked game binaries remain local and are not documentation downloads.
