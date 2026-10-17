---
title: Partial type knowledge
---

<!-- Generated; edit project/gt3 authorities, not this view. -->

Partial guest layouts are compiled against **current relocated headers**. This is layout consistency, not gameplay proof.

This historical layout inventory is not exhaustive. Transmission layouts also have source-local assertions; see the [selector contract](../../developer-guide/worked-example-mt-selector/trace-and-contract.md). Opaque padding is unknown storage, not permission to bulk-write a car.

## HandbrakeCommandPartial

`src/gt3/gameplay/controls/gt3_clean_handbrake.hpp`; size `0x10`.

| Offset | Field | Meaning |
|---|---|---|
| `0x0` | `flags` | Bit 0x10 selects analog handbrake |
| `0xe` | `handbrake` | Signed halfword; digital nonzero or analog Q12, not generically clamped |

## HandbrakeCarPartial

`src/gt3/gameplay/controls/gt3_clean_handbrake.hpp`; size `0x13b8`.

| Offset | Field | Meaning |
|---|---|---|
| `0x13b4` | `processed_handbrake` | Processed handbrake; prior value is digital ramp history; analog replaces it |

## PedalCommandPartial

`src/gt3/gameplay/controls/gt3_clean_pedals.hpp`; size `0x10`.

| Offset | Field | Meaning |
|---|---|---|
| `0x0` | `flags` | representation flags, preserved numeric bits |
| `0x1` | `mode` | numeric mode, 4 selects applicable original descriptors |
| `0x8` | `accelerator` | unsigned pressure or wrapping digital halfword |
| `0xa` | `brake` | signed pressure or digital nonzero halfword |
| `0xc` | `auxiliary` | unsigned request arbitrated before accelerator processing; not physical clutch |

## PedalControlPartial

`src/gt3/gameplay/controls/gt3_clean_pedals.hpp`; size `0x4`.

| Offset | Field | Meaning |
|---|---|---|
| `0x0` | `auxiliary_active` | auxiliary arbitration/history indicator, not a physical-device interpretation |
| `0x2` | `accelerator_history` | numeric history/source state; unknown values retained where original does |

## PedalCarPartial

`src/gt3/gameplay/controls/gt3_clean_pedals.hpp`; size `0x14bc`.

| Offset | Field | Meaning |
|---|---|---|
| `0x1304` | `control` | manual wrapper control-state alias; only nested +0/+2 written |
| `0x136d` | `control_kind` | signed numeric classification, not a new device type |
| `0x13ac` | `processed_accelerator` | processed accelerator before original coupling/effective-accelerator propagation |
| `0x13b0` | `processed_brake` | processed brake before original policy coupling/distribution |
| `0x13e5` | `numeric_policy` | numeric arbitration/coupling policy, not physical clutch mode |
| `0x14b8` | `policy_suppression` | nonzero forces local numeric policy zero |
| `0x14ba` | `auxiliary_suppression` | clears auxiliary before arbitration; required outgoing v0 |

## BindingRecord

`src/gt3/gameplay/controls/gt3_controls.hpp`; size `0x6`.

| Offset | Field | Meaning |
|---|---|---|
| `0x0` | `unknown` | unknown |
| `0x2` | `primary_channel` | primary_channel |
| `0x4` | `secondary_channel` | secondary_channel |

## Command

`src/gt3/gameplay/controls/gt3_clean_steering.hpp`; size `0x10`.

| Offset | Field | Meaning |
|---|---|---|
| `0x0` | `analog_flags` | analog_flags |
| `0x1` | `steering_mode` | steering_mode |
| `0x2` | `shift` | shift |
| `0x3` | `unknown03` | unknown03 |
| `0x4` | `steering` | steering |
| `0x6` | `opposing_pressure` | opposing_pressure |
| `0x8` | `accelerator` | accelerator |
| `0xa` | `brake` | brake |
| `0xc` | `auxiliary` | auxiliary |
| `0xe` | `handbrake` | handbrake |

## InputPartial

`src/gt3/gameplay/controls/gt3_clean_steering.hpp`; size `0xc4`.

| Offset | Field | Meaning |
|---|---|---|
| `0x14` | `type_bits` | type_bits |
| `0x2c` | `digital_mask` | digital_mask |
| `0x38` | `channels` | channels |
| `0xc0` | `vtable` | vtable |

## CarPartial

`src/gt3/gameplay/controls/gt3_clean_steering.hpp`; size `0x16a8`.

| Offset | Field | Meaning |
|---|---|---|
| `0x68` | `mechanical_limit` | mechanical_limit |
| `0xec0` | `dt` | dt |
| `0x136d` | `control_kind136d` | control_kind136d |
| `0x136e` | `unknown136e` | Unknown hook gate |
| `0x136f` | `wheel_policy` | wheel_policy |
| `0x13a0` | `steering` | steering |
| `0x13a4` | `unknown13a4` | Unknown broader purpose; assignment to 1.0 evidenced |
| `0x13a8` | `steering_rate` | steering_rate |
| `0x1420` | `envelope_ratio` | envelope_ratio |
| `0x142c` | `negative_limit` | negative_limit |
| `0x1430` | `positive_limit` | positive_limit |
| `0x16a4` | `wheel_command` | wheel_command |
| `0x16a6` | `previous_wheel_command` | previous_wheel_command |
