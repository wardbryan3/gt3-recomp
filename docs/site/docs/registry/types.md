---
title: "Partial type knowledge"
---

<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->

Authoritative inventory: `decomp/gt3/types.json`. Offset assertions are generated into `build/foundation/type-assertions.cpp` and compiled with `just check`. All guest pointers are 32-bit little-endian; EE floats retain bit patterns. **Do not treat opaque padding as recovered fields or bulk-write it.**

## PedalCommandPartial

Size `0x10`. bounded read-only accelerator/brake/auxiliary command view; no neighboring recovery. Source: `host/gt3_clean_pedals.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x0` | `flags` | `u8` | representation flags, preserved numeric bits |
| `0x1` | `mode` | `u8` | numeric mode, 4 selects applicable original descriptors |
| `0x8` | `accelerator` | `u16` | unsigned pressure or wrapping digital halfword |
| `0xa` | `brake` | `i16` | signed pressure or digital nonzero halfword |
| `0xc` | `auxiliary` | `u16` | unsigned request arbitrated before accelerator processing; not physical clutch |

## PedalControlPartial

Size `0x4`. two bounded writable bytes; other bytes opaque and unchanged. Source: `host/gt3_clean_pedals.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x0` | `auxiliary_active` | `u8` | auxiliary arbitration/history indicator, not a physical-device interpretation |
| `0x2` | `accelerator_history` | `u8` | numeric history/source state; unknown values retained where original does |

## PedalCarPartial

Size `0x14bc`. manual-wrapper partial view only; no opaque padding writes or full-car claim. Source: `host/gt3_clean_pedals.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x1304` | `control` | `PedalControlPartial` | manual wrapper control-state alias; only nested +0/+2 written |
| `0x136d` | `control_kind` | `i8` | signed numeric classification, not a new device type |
| `0x13ac` | `processed_accelerator` | `EE float bits u32` | processed accelerator before original coupling/effective-accelerator propagation |
| `0x13b0` | `processed_brake` | `EE float bits u32` | processed brake before original policy coupling/distribution |
| `0x13e5` | `numeric_policy` | `u8` | numeric arbitration/coupling policy, not physical clutch mode |
| `0x14b8` | `policy_suppression` | `u8` | nonzero forces local numeric policy zero |
| `0x14ba` | `auxiliary_suppression` | `u16` | clears auxiliary before arbitration; required outgoing v0 |

## BindingRecord

Size `0x6`. six-byte record storage; first halfword meaning unknown. Source: `host/gt3_controls.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x0` | `unknown` | `i16` | unknown |
| `0x2` | `primary_channel` | `i16` | primary_channel |
| `0x4` | `secondary_channel` | `i16` | secondary_channel |

## Command

Size `0x10`. full storage; unknown03 semantic unknown. Source: `host/gt3_clean_steering.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x0` | `analog_flags` | `u8` | analog_flags |
| `0x1` | `steering_mode` | `u8` | steering_mode |
| `0x2` | `shift` | `i8` | shift |
| `0x3` | `unknown03` | `u8` | unknown03 |
| `0x4` | `steering` | `i16` | steering |
| `0x6` | `opposing_pressure` | `i16` | opposing_pressure |
| `0x8` | `accelerator` | `i16` | accelerator |
| `0xa` | `brake` | `i16` | brake |
| `0xc` | `auxiliary` | `i16` | auxiliary |
| `0xe` | `handbrake` | `i16` | handbrake |

## InputPartial

Size `0xc4`. partial only; unknown padding NOT zero-filled by a bridge. Source: `host/gt3_clean_steering.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x14` | `type_bits` | `u32` | type_bits |
| `0x2c` | `digital_mask` | `u32` | digital_mask |
| `0x38` | `channels` | `u32[32]` | channels |
| `0xc0` | `vtable` | `u32` | vtable |

## CarPartial

Size `0x16a8`. partial steering view; not the full car; opaque padding must not be bulk-written. Source: `host/gt3_clean_steering.hpp`.

| Offset | Field | Representation | Meaning |
|---|---|---|---|
| `0x68` | `mechanical_limit` | `EeFloat:u32` | mechanical_limit |
| `0xec0` | `dt` | `EeFloat:u32` | dt |
| `0x136d` | `control_kind136d` | `i8` | control_kind136d |
| `0x136e` | `unknown136e` | `i8` | Unknown hook gate |
| `0x136f` | `wheel_policy` | `i8` | wheel_policy |
| `0x13a0` | `steering` | `EeFloat:u32` | steering |
| `0x13a4` | `unknown13a4` | `EeFloat:u32` | Unknown broader purpose; assignment to 1.0 evidenced |
| `0x13a8` | `steering_rate` | `EeFloat:u32` | steering_rate |
| `0x1420` | `envelope_ratio` | `EeFloat:u32` | envelope_ratio |
| `0x142c` | `negative_limit` | `EeFloat:u32` | negative_limit |
| `0x1430` | `positive_limit` | `EeFloat:u32` | positive_limit |
| `0x16a4` | `wheel_command` | `i16` | wheel_command |
| `0x16a6` | `previous_wheel_command` | `i16` | previous_wheel_command |

## Untyped car observations

These offsets do **not** extend the C++ layout or authorize writes.

| Offset | Provisional name | Confidence | Meaning |
|---|---|---|---|
| `0x1304` | `control_state1304` | high | Observed four-byte control-state window passed to 001E4478; not a whole-class layout |
| `0x13e5` | `control_policy13e5` | medium | Numeric accelerator/auxiliary arbitration and coupling policy; UI meaning unknown |
| `0x14b8` | `suppression14b8` | medium | Suppresses several manual control/driver paths |
| `0x14ba` | `suppression14ba` | medium | Suppresses auxiliary/shift/coupling; zero versus nonzero checked |
| `0x1074` | `wheel_brake_request_first` | high | Four broadcast entries at stride 0xA4; physical torque units not certified |
| `0x1274` | `scaled_brake_request_first` | high | Four scaled entries at stride 0x24, with rear handbrake contribution |
| `0x13ac` | `processed_accelerator` | high | Original command processing result; not final torque |
| `0x13b0` | `processed_brake` | high | Original processed brake request |
| `0x13b4` | `processed_handbrake_candidate` | high | Adds rear axle brake request; interacts with coupling |
| `0x139c` | `clutch_coupling_candidate` | medium | Branch-controlled coupling, not proven physical clutch axis |
| `0x13ba` | `gear_index_candidate` | medium | Used to index gear ratios |
| `0x13bb` | `driveline_state_candidate` | medium | 0/free engine vs coupled states; not gear itself |
| `0x1428` | `effective_accelerator` | high | Manual wrapper copies +13ac; other producer policies remain |
| `0x13cc` | `engine_angular_rate_candidate` | medium | Integrated then converted to display RPM |
| `0x1414` | `engine_display_speed_candidate` | medium | RPM conversion; limiting semantics need full trace |
| `0x16d6` | `signed_output_encoding_candidate` | medium | Encoded bounded [-1,+1] output, not physical torque |
| `0x140c` | `motion_speed_candidate` | medium | Steering curve input; speed units/frame not certified |
