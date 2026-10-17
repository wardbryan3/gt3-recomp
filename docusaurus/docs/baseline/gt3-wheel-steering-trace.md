---
title: "Historical: gt3-wheel-steering-trace"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


> Historical technical reference: wheel override, policies and shared consumers
> remain educational; synthetic fixtures do not qualify physical hardware.
> Recipes refer to retired historical tooling. See [workflow](../workflow.md) and
> [testing](../testing.md) for maintained root commands. Raw exports and game
> artifacts remain private.

# GT3 wheel steering: input override and shared driving consumer

Target: GT3 USA v1.10 `games/gt3-usa-v110/core.elf`, SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
This extends [the stick trace](gt3-steering-trace.md). Addresses below are
static guest addresses, not a capture of current in-game objects.

## Where the paths meet

```text
wheel device state
  -> 0x00230D10: raw axis/pedals and wheel-type bits
  -> 0x0022FFE8: wheel-only or combined pad/wheel input state
  -> 0x002115F8: virtual channel read, wheel steering command at +4, mode 4
  -> same 16-byte command used by the manual driving branch
  -> 0x001E4478: separate mode-4 steering branch
       wheel: normalize command, optionally slew limits, directly write steering
       stick: normalize command, call spring/damping filter 0x001E4368
  -> SAME car +0x13A0 steering float
  -> SAME 0x001E8978 / 0x001E8910 individual-wheel-angle computation
  -> SAME car +0xFF0 +wheel_index*0xA4
  -> SAME 0x001E7328 wheel-motion consumer
```

There are two joins: **the common command representation** and **the final
steering float**. The wheel does **not** rejoin at the pad response table or
at the stick's spring/damping filter. Within `0x001E4478`, its steering branch
joins the common tail at `0x001E48A0` (then `0x001E48A4`). The previously
recovered manual caller chain and optional virtual command hook still apply;
this investigation does not establish that hook's live effects. [W1, W2]

## State and channel selection

`0x00230D10` exports an active wheel-device object's axis word at `D +0x24`
and pedal words at `D +0x3C/+0x40` into state `I +0x38/+0x3C/+0x40`.
It selects these wheel-type bits based on device identifier fields:

| Observed identifier test | `I +0x14` | Wheel type |
|---|---:|---:|
| Halfwords at `D +0x58/+0x5A`: `0x046D/0xC293` | `0x20` | 1 |
| Word at `D +0x58`: `0x000406F8` | `0x40` | 2 |
| Halfwords at `D +0x58/+0x5A`: `0x046D/0xC294` | `0x60` | 3 |
| Unrecognized active device | `0xE0` | 7 |

These are code comparisons, not proof of particular marketed model names,
USB enumeration success, or hardware axis/report ranges. Lower-level device
polling and USB report decoding have not been reconstructed here. [W2]

With both sources active, `0x0022FFE8` ORs their type bits and digital masks,
copies the first 16 pad channels, and copies the three wheel channels into
`I +0x78/+0x7C/+0x80` (channel indices **16/17/18**). With just the wheel
active it copies the wheel state, leaving its channels at **0/1/2**. Prior
source-order evidence is in the stick trace. [W2, previous E3]

`0x002115F8` obtains the combined digital mask through the virtual method
at vtable `+0x2C`. It reads axes through vtable `+0x44`, applying the signed
`this` adjustment at `+0x40`. For the input vtable at **`0x0033F7E0`**,
these methods are `0x0022DFA8` and `0x0022E000`, with zero adjustments:

```text
0x0022DFA8(I)          = word at I +0x2C
0x0022E000(I, channel) = word at I +0x38 +channel*4
base = (I[+0x14] &31) != 0 ? 16 : 0
wheel_type = (I[+0x14] >>5) &7
```

Only types **1, 2, 3** enable the override. Type 0 and types 4–7 leave the
command untouched (although the digital-mask virtual call occurs before
that check). Thus a nonzero wheel-type field alone is insufficient. [W1, W3]

## `0x002115F8`: wheel wins over preceding pad steering

The builder `0x00210740` clears the command, runs `0x00211430` for pad input,
then runs `0x002115F8`, then passes the command to `0x001F4998`. In the enabled
wheel branch, it first applies the digital helper `0x00210EF8`, then reads
channel `base` and writes:

```cpp
q = clamp((512 - axis) * 9, -4096, +4096);
command[+1] = 4;         // steering mode
int16(command[+4]) = q;
command[+0] |= 1;        // analog steering present
```

This overwrites a prior stick or D-pad command **even at wheel center**.
There is no mapping lookup, pad response curve, or pad dead zone in this
conversion. Examples within the synthetic tested axis domain:

| Axis | Command | Command /4096 |
|---:|---:|---:|
| 0–56 | +4096 | +1 |
| 57 | +4095 | +0.999755859375 |
| 512 | 0 | 0 |
| 967 | -4095 | -0.999755859375 |
| 968–1023 | -4096 | -1 |

Center 512 is established by arithmetic. **The 0–1023 hardware range remains
unverified**; it is the deliberately chosen test domain. [W1, W2]

The two adjacent channels also produce pedal commands. `0x002115D8(raw,t)`
computes `v = (255 - raw - t)*2`, replacing values above 255 with 256.
The caller uses thresholds **75** and **80**, respectively, writes `v*16`
to command `+8/+10`, and ORs flags 2/4 **only when v >0**. Otherwise it leaves
any earlier pad/digital command in place. The digital helper can first set
these fields to 1 and clear their analog flags. Full pedal-to-vehicle
calibration is outside this steering trace. [W1, W4]

## `0x001E4478`: direct steering, with stateful envelope options

With analog steering flag 1 and mode 4, execution enters **`0x001E470C`**.
It clears `car +0x1307`, saves current/previous wheel commands at
`car +0x16A4/+0x16A6`, and computes signed `u = command[+4]/4096`.

Its envelope differs from the pad envelope. For the ordinary classification,
the interpolated curve descriptor is at **car +0xA8**, not stick +0x6C.
Classification 1 uses the descriptor at **+0xE4**. The curve input is the
nonnegative value at car +0x140C. The classification comes from the race
state via `0x001F2F68`; race values 1 and 2 yield classifications 2 and 1.
Semantic speed/surface labels remain inferred. [W2, W5]

The signed byte at **car +0x136F**, returned by `0x001E4470`, selects another
policy. Its UI/configuration provenance and names are not established:

| Policy | Envelope adjustment | Actual steering calculation |
|---:|---|---|
| 0 | No extra minimum | Slewed limits × signed normalized command |
| 1 | Minimum magnitude 8°; classification 1: 15° | Same |
| 2 | Minimum magnitude 12°; classification 1: 20° | Same |
| 3 | Same minimum as policy 1; no mean-state widening | Same |
| 4 | No mean-state widening | `car[+0x68] * u` directly |
| Negative or above 4 | Envelope may still be computed | Writes steering zero |

Policies other than 3/4 can widen the envelope to include the mean of
car +0x105C/+0x1100. Bounds are then capped by car +0x68. The minimum-angle
constants are radians at `0x00352980/84/88/8C`; they are not steering-input
dead zones. [W2, W6]

For policies 0–3, `0x001E4320` moves stored positive/negative limits at
**car +0x1430/+0x142C** toward the computed bounds by at most
`float(0x0035297C) * dt` per frame. That constant is approximately **π/2**.
It then directly writes:

```cpp
car[+0x13A0] = u >= 0 ? car[+0x1430] * u : -car[+0x142C] * u;
```

Policy 4 skips this limit slewing. Neither path calls `0x001E4368`, nor
updates the stick-filter rate at car +0x13A8. Therefore wheel mode avoids
stick spring/damping, but policies 0–3 can still depend on previous-frame
**limits**. The final float is consumed by the unchanged wheel-angle code
described in the stick trace. [W2, W4]

## Reconstruction and executed verification

Current locators from `project/gt3/migration-map.json` are
`src/gt3/gameplay/controls/gt3_controls.hpp` and
`validation/gt3/differential/gt3_steering_trace_test.cpp`. The historical paths and
counts below describe their evaluated versions, not current product installation.

At this checkpoint, `host/gt3_controls.hpp` exposed the two bounded-domain arithmetic helpers
`wheel_steering_command` and `wheel_pedal_input`. They are standalone
reconstructions, not guest replacements or host wheel-device integration.

`tests/gt3_steering_trace_test.cpp` additionally executes generated EE code
with original ELF data/vtable/constants:

- Device adapter identifier/channel fixtures: **12** cases.
- Native virtual-channel override/type/bank sweep and pedal/digital cases:
  **19,456** commands, plus those 12 adapter fixtures (**19,468** total).
- `0x002115F8 -> 0x001E4478 -> 0x001E8978`: **7,560 frames**, covering
  policies -1/0/1/2/3/4/5, both curve classifications, nine axes, 60 frames.
- Checks include signed command/history, steering float, retained filter-rate
  sentinel, independently advanced limit states, and all four wheel angles.

Vehicle curves, starting limits, mean-state values, dt, wheel coefficients,
and the 0–1023 axis range are synthetic fixtures, not measured stock-car or
physical-wheel values. Virtual reads use the shipped vtable, not host stubs.
The fixture does not boot the game, execute the full race wrapper or optional
command hook, or poll a real USB device. Float tolerance is 2e-6.
The historical runner was `tests/run_resolution_tests.sh`; the original
**15,360** stick frames, controls, GPU and hardware regressions also passed.
That recipe is not a maintained current command.

## Evidence ledger and remaining boundaries

Records are retained in `docs/gt3-wheel-evidence.json`:

- **W1:** wheel assembly: `ev_0c1f4be70fd4e5794a059276b8aa8d6fd1ff32f9ff8cd823afc9ba8e2c306c4c`;
  wheel/pedal/policy-getter pseudocode: `ev_ab529eae84b77c8495bdcd745a9d14a640718910b26e4fb2b412c53fcb9a4de3`.
- **W2:** builder, state adapter/composition, complete driving processor:
  `ev_bd75205028a72307c6662fe769c9a5cb673340ce549400fac86ff1b2139eb2dc`.
- **W3:** shipped vtable bytes: `ev_affec8e5645b9c17f0e62dfcec73ae27cf6b2f0071326558a5277a29374822fe`;
  getter instruction bytes: `ev_cac888fa7ead83b0f4981c8cec23fa7a44884e163e36ef920f2b6b252b791c35`.
- **W4:** digital helper, limit approach helper, mask getter and input-vtable use:
  `ev_6d791be32090b211f598a7fffe668ef1f0ecc94bf2dcef2f48ac3bf69e712a44`.
- **W5:** race classification and pad/wheel source constructor:
  `ev_af3dd19042062aa9b513801fcc06cea1a5bd623e0da069a56aef983d37a92302`.
- **W6:** wheel constants: `ev_379041ecd32a588fe6cfc746aca7a510bc96282ca502d87065aca4691b73b5c8`.

**Answered:** existing wheel steering override, channel selection, mode-4
vehicle processing, and exact shared steering/wheel-angle consumer.
**Not claimed:** physical report range, live policy selection, branded model
identification, optional-hook effects, force feedback, full pedal calibration,
or physical-PS2 floating-point equivalence. Force feedback requires a separate
output-side trace; this input-side investigation establishes none of it.
