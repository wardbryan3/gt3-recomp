---
title: Controls producer / consumer chain
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

> **Reading this map:** addresses identify original-code dataflow, with bounded
> historical recovered implementations described separately. Current bounded source
> proof is not product installation: both products still execute original generated
> gameplay, with no recovered or enhanced gameplay integrated. See
> [execution status](development/restructuring.md) and [validation layers](testing.md).

```mermaid
flowchart TD
  PAD[Pad report +6 / cached stick +1A] --> STATE[0022FC30 - combined input channels]
  STATE --> DISPATCH[00211430 - pad dispatcher]
  DP[D-pad pressures] --> DISPATCH
  DISPATCH --> STICK[00210E68 / 00211398 - steering and mapped actions]
  BIND[Binding records + signed primary / secondary channel] --> STICK
  WDEV[Wheel object report state] --> WSTATE[00230D10 -> 0022FFE8]
  WSTATE --> WBUILD[002115F8 - wheel types 1..3 / bank 0 or 16]
  STICK --> CMD[Common 16-byte command]
  WBUILD --> CMD
  CMD --> MAN[001E4D38 -> 001E4CB0 -> 001E4478]
  MAN --> STEER[Steering +13A0 - bounded clean region]
  STEER --> ANGLE[001E8978 / 001E8910 -> individual wheel angles]
  ANGLE --> PHYS[001E7328 - unchanged wheel motion]
  MAN --> PEDAL[Original pedal / control tail +13AC / +13B0]
  PEDAL --> ENGINE[+1428 -> 001E7500 -> original torque path]
  PEDAL --> BRAKE[001EAC60 -> +1074 + wheel*A4 -> 001E6EC8]
```

Two wheel joins: shared command, then steering float. Wheel mode 4 does **not** use the stick response/filter; policies 0–3 still slew limits, policy 4 uses the mechanical limit directly. A wheel builder can overwrite centered pad steering; released wheel pedals leave preceding pad commands in place.

Standalone mapping helpers now live at `src/gt3/gameplay/controls/gt3_controls.hpp`
(formerly `host/gt3_controls.hpp`, per `project/gt3/migration-map.json`). They recover
binding lookup and primary/secondary mapped actions. Primary producer `00211050`,
secondary `002111C0`; `00211398` is a distinct inspected control producer, **not**
`fill_mapped_actions`. Normalization's older throwing-zero contract is intentionally
separate from the EE-compatible clean bridge. Relocated sources are not automatically
the exact versions evaluated by historical proof.

The detailed [controls](baseline/gt3-controls.md),
[pad trace](baseline/gt3-steering-trace.md) and
[wheel trace](baseline/gt3-wheel-steering-trace.md) remain educational references:
report bytes → command representation → processed state → original consumers.
The [clean steering contract](baseline/gt3-clean-steering.md) and
[synthetic experiment](baseline/gt3-synthetic-wheel-experiment.md) describe separate
historical validation mechanisms. [Pedal v1](pedal-v1.md) explains pedal producers,
Q12 versus digital commands, the 22 original-only discovery fixtures and the exact
join contract; [closure](pedal-closure.md) owns later stack admission and finite
profile coverage. [Handbrake](handbrake-v1.md), [virtual pedals](virtual-pedals.md)
and [virtual handbrake](virtual-handbrake.md) have separate contracts. No full
controls class, physical report parser or device-output contract is claimed.
