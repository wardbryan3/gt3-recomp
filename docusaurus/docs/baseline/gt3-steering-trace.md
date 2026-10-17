---
title: "Historical: gt3-steering-trace"
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../workflow.md)
and [execution status](../development/restructuring.md) for maintained commands and actual gates.

:::


> Historical technical reference: this detailed byte-to-wheel trace and its
> constructed fixtures remain educational, not current live or hardware proof.
> Recipes refer to retired historical tooling. See [workflow](../workflow.md) and
> [testing](../testing.md) for maintained root commands. Raw exports and game
> artifacts remain private.

# One complete GT3 steering path: DualShock 2 left-stick X

Target and digest are recorded in [gt3-controls.md](gt3-controls.md).
This trace follows a **configured left-stick-X mapping**, pressure-mode pad
ID `0x79`, no D-pad input, no wheel override, and the manual-driving branch.
It establishes the static producer/consumer chain and exercises the numerical
core with generated EE code. It is not an in-game capture or a claim that all
players use this mapping or these vehicle parameters. The separate
[wheel steering trace](gt3-wheel-steering-trace.md) follows the wheel override
through mode 4 to this same final steering float and wheel-angle consumer.

## Result at a glance

```
controller report byte +6 (left-stick X)
  -> cached report / pad-device +0x1A
  -> 0x0022FC30: input-object word +0x40 (raw channel 2)
  -> 0x00210E68: curve[raw], signed fixed-point steering at command +4
  -> 0x001E4478: command /4096, vehicle-dependent steering limit
  -> 0x001E4368: stateful steering filter
  -> car +0x13A0: filtered steering, floating-point angle
  -> 0x001E8978 / 0x001E8910: individual wheel angles
  -> car +0xFF0 + wheel*0xA4
  -> 0x001E7328: wheel-angle trig used in wheel-motion processing
```

The final value supplied to wheel-angle computation is **the float at
`car + 0x13A0`**, not the raw byte or the fixed-point command. The per-wheel
angles are a further geometric conversion of that float. Trig routines use
radian constants, establishing the angle convention at that consumer.

## 1. Controller state reaches the input object

`0x00272140` copies the selected libpad report into its destination. The
frame-side reader `0x0022F938` calls it for pad ports 0 and 1, writing caches
at `0x004A09CC` and `0x004A0B40`. Report layout for this path:

| Report offset | Field |
|---|---|
| +0 | status |
| +1 | device/mode ID (`0x79` here) |
| +2, +3 | active-low digital buttons |
| +4, +5 | right-stick X, Y |
| **+6, +7** | **left-stick X, Y** |
| +8 onward | pressure bytes |

The asynchronous poller `0x0022F328` also reads libpad reports into per-port
state, including a separate report area at +0x20; don't confuse that area
with the frame-side cache copied below.

`0x0022FB78` invokes `0x0022F9E8`, which copies 32 cached report bytes into
pad-device object `D + 0x14`. Thus left-stick X is at `D + 0x1A`.
`0x0022FBB0` validates the report ID and selects a device type using the
8-byte ID/type records at `0x00341A38`:

```
0x41 -> 4
0x73 -> 7
0x79 -> 8
```

The pad-device vtable `0x00341A00` points its state-output method (+0x14)
to `0x0022FC30`. That routine zero-extends 32 bytes beginning at `D + 0x18`
into 32 words beginning at input-object `I + 0x38`:

```
I[+0x38] = report[+4] = right-stick X
I[+0x3C] = report[+5] = right-stick Y
I[+0x40] = report[+6] = left-stick X
I[+0x44] = report[+7] = left-stick Y
```

It also inverts the report's digital-button bits and stores them at `I +0x30`.
Device type 8 goes into `I +0x14` for this report.

The port adapter's `0x0022E598` delegates to the composite state-output routine
`0x0022FFE8`. With only the pad active it copies the pad state via
`0x0022DC10`. With both sources active it still takes the first 16 raw-channel
words from the first (pad) source. Constructor `0x0022E470` establishes that
pad/wheel source ordering. These links come from code and vtable bytes, not
merely from guessed function names. [E1–E3]

## 2. GT3 converts channel 2 to a steering command

The input builder `0x00210740` clears a 16-byte command with `0x001F4330`,
then calls `0x00211430` for active live input. For type 8 the relevant order is:

1. `0x00210DA8`: derive steering from D-pad pressure.
2. `0x00210E68`: fill mapped analog steering **only if command +4 is zero**.

This priority matters: nonzero D-pad pressure steering suppresses the mapped
stick for that command. We choose no D-pad input.

`0x00210E68` looks up action ID **0**, using the primary mapping field:

```
index = *(uint32 *)(mapping + bank*0x50 + variant*0x28 + action*4)
channel = *(int16 *)(0x002E2CF8 + index*6 + 2)
```

`0x00211430` supplies bank 1 and variant `I[+0x144]`. For this trace variant
is 0 and the selected binding index is 1. The **shipped** record at
`0x002E2CFE` is `(0, 2, 2)`, so primary channel is 2.

Unlike the four-action normalizer, this steering routine does not mask the
channel to eight bits before indexing. A valid steering mapping must identify
the intended raw channel; a half-axis code such as `0x102` is not interchangeable
with channel 2 here.

It reads the low byte of `I +0x38 +channel*4`, curves it with the shipped
256-byte table at `0x003416F8`, and writes:

```cpp
command.flags |= 1;
command.steering_mode = 2;
command.steering_q12 = (256 - 2 * curve[raw]) * 16;
```

`steering_q12` is a signed halfword at command +4. It ranges from +4096 to
-4064, with center 0. The table is **not identity**: bytes 91 through 164
inclusive map to 128, yielding a substantial dead zone. Examples:

| Raw stick byte | Curved byte | Command +4 | Command /4096 |
|---|---|---|---|
| 0 | 0 | +4096 | +1.0 |
| **64** | **82** | **+1472** | **+0.359375** |
| 128 | 128 | 0 | 0 |
| 192 | 175 | -1504 | -0.3671875 |
| 255 | 255 | -4064 | -0.9921875 |

The pressure-mode left-stick report convention identifies low X as left;
the observed GT3 arithmetic gives that side a positive command. World-space
handedness is not needed to establish this sign conversion.

`0x002115F8` can subsequently overwrite steering for wheel devices. Its branch
requires wheel-type bits `(I[+0x14] >>5)&7` in the range 1–3. Those bits are zero in our
selected pad-only path, so it leaves the stick command unchanged. [E4–E6]

## 3. The manual driving code consumes that command

The race-update function `0x001F39D8` visits each car and calls
`0x001E4D38` before `0x001E8978` and then `0x001E7328`.

`0x001E4D38` asks `0x00210740` for a stack-local command. For the manual
branch (`car[+0x136D] ==0`, and `car[+0x14B8] ==0` or +0x14BA nonzero),
`0x001E4CB0` passes that command to:

```
0x001E4478(car, command, car +0x1304)
```

There is an earlier optional virtual command hook in `0x001E4D38` when
`car[+0x136E] ==0`. The trace assumes that hook does not modify steering;
its implementation is not resolved here. Replay/AI/special driving branches
are not included in this trace.

`0x001E4478` first derives a steering-limit envelope from vehicle state. On
the normal stick path it interpolates the vehicle's curve using nonnegative
`car[+0x140C]`, selecting a curve descriptor at +0x6C or +0xE4 depending on
surface/race classification. It can widen the envelope to include the mean
of state values at +0x105C and +0x1100, and caps it by `car[+0x68]`.
Calling these speed/surface/slip-related values is a semantic inference;
the addresses, selection, interpolation, and clamps are established by code.

Let the resulting positive and negative limits be `hi` and `lo` (lo <=0).
For analog flag 1 and steering mode 2 it computes:

```cpp
u = int16(command[+4]) / 4096.0f;
target = u >= 0 ? hi * u : (-lo) * u;
```

It stores the limits at car +0x1430 and +0x142C, sets steering state byte
`car[+0x1307]` to 2 when the command is nonzero, and calls `0x001E4368`.
Stick mode 2 uses the class-selected rate limit at
`0x0049D0A0 +class*4` for both outward and returning motion. Pressure steering
(mode 3) has a different path. [E7–E8]

## 4. The filter produces the actual steering float

`0x001E4368` uses:

| Address | Role |
|---|---|
| car +0x13A0 | current filtered steering `s` |
| car +0x13A8 | steering rate `v` |
| car +0xEC0 | time step `dt` |
| 0x00352970 | spring coefficient 100 |
| 0x00352974 | damping coefficient 5 |
| 0x00352978 | extra return coefficient 50 |

The constants are GP-relative loads in assembly. For this ELF's data layout,
`gp=0x003579F0` makes `gp-0x5080` resolve to +0x352970. These constants are
separate from the class-selected runtime rate-limit table at +0x49D0A0.

For ordinary finite values the recovered update is:

```cpp
a = (target - s) * 100 - v * 5;
if ((s > 0 && target < s) || (s < 0 && target > s)) {
    a -= s * 50;
    rate_limit = return_rate_limit;
}
v_next = clamp(v + a * dt, -rate_limit, rate_limit);
s_next = s + v_next * dt;
if (this step crosses target) {
    s_next = target;
    v_next = 0;
}
car[+0x13A0] = s_next;
car[+0x13A8] = v_next;
```

Thus one controller byte alone does **not** determine the final steering
angle: previous steering/rate, vehicle envelope, rate limit, and time step
all matter. [E9]

## 5. The driving code turns that float into wheel angles

`0x001E8978` loads steering at instruction **0x001E89B8**:

```
s3 = car +0xF84
lwc1 f12, 0x41C(s3)  // car +0x13A0
```

It supplies `a0=car+0x10`, `a1=wheel_index` to `0x001E8910` and writes the
result to `car +0xFF0 +index*0xA4`. The pseudocode shows an extra zero float
argument; assembly establishes that the zero in f13 is unused by this callee.

For wheel indices 0–3 the calculation is:

```cpp
float angle = 0;
if (index < 2) {
    coefficient_index = steering < 0 ? 1-index : index;
    angle = steering * float_at(car +0x120 +4*coefficient_index);
}
float alignment = float_at(car +0xE30 +4*(index >>1));
angle += (index &1) ? alignment : -alignment;
```

So indices 0 and 1 receive steering multiplied by potentially different
coefficients, swapped by steering sign. Indices 2 and 3 receive alignment
only in this routine. This supports interpreting 0/1 as the front pair and
2/3 as the rear pair; exact left/right labels and the vehicle-setup provenance
of the coefficients are not recovered here.

Stored angles are at **+0xFF0, +0x1094, +0x1138, +0x11DC**. The routine also
stores sine/cosine approximations in the wheel-transform area with stride
0x24. `0x001E7328`, called next by the race update, reads the angles and
uses their sine/cosine to combine wheel-state components before calling
`0x001E7068`. This establishes a driving/wheel-processing consumer, rather
than stopping at a UI percentage or an input buffer. [E10–E11]

## Executed example and regression

Current fixture locator: `validation/gt3/differential/gt3_steering_trace_test.cpp`,
from `project/gt3/migration-map.json`. The following historical path and result
refer to their exact evaluated version, not newly executed current source proof.

`tests/gt3_steering_trace_test.cpp` loads the original ELF's data and executes
these generated EE routines directly, in order:

```
0x0022FC30 -> 0x001F4330 -> 0x00210DA8 -> 0x00210E68
then each frame: 0x001E4478 -> 0x001E8978
```

The test is a composed fixture, **not** execution of the entire port manager,
race-update wrapper, virtual hook, libpad/SIF stack, or physical hardware.
Static evidence connects those wrappers. The fixture uses mapping index 1,
vehicle limits ±0.5, dt=1/60, rate limit 10, initial steering/rate 0,
front coefficients (1, 0.75), front alignment 0 and rear alignment 0.02.
Those vehicle values are deliberate test choices, not measured stock-car data.

For report left-X byte **64**:

```
raw 64 -> curve 82 -> command +1472 -> normalized +0.359375
-> target +0.1796875
frame 1: car steering +0.0049913195
         front angles (+0.0049913195, +0.00374348951)
frame 60: car steering +0.1796875
          front angles (+0.1796875, +0.134765625)
rear angles remain (-0.02, +0.02)
```

All **256 raw bytes ×60 frames =15,360 frames passed**, checking decoded
state, fixed-point command/flags, steering/rate, and all four wheel angles.
Float checks use 2e-6 absolute tolerance; they are not bit-exact assertions
against IEEE reconstruction. The existing controls, anisotropic GPU, and
hardware regressions also passed. The runner for this historical result was
`tests/run_resolution_tests.sh`, not a maintained current recipe.

## Evidence ledger and remaining boundaries

Full IDs below resolve into retained records in
`docs/gt3-steering-evidence.json`, with earlier mapping/dispatcher evidence
in `docs/gt3-controls-evidence.json`.

- **E1:** cached libpad report/copy:
  `ev_d551f4b44bec60a26c21766e254c21a2772d2639cb403afbfd3594d9bac277f8`,
  `ev_8bf8689be242952693a2af4f43653e88b9503d2ca73e7906e26361abc1eafdbd`.
- **E2:** packet decode / source initialization:
  `ev_38d04db7d6b5135860dbb44a8d3e576f180b3e7f0b260fcbf82db00b24cd498a`;
  vtable and type bytes:
  `ev_d672dcef0a0107c16a676c2fe1fcaac4e383b59bb2c88b8571028780131648a8`.
- **E3:** port output/composition:
  `ev_6327bdb002de9de96c202cffbb54a2456b37721a6b7c4f4d61591abe9990daed`,
  `ev_f38920dea6e5dd0c8ed64f5922ccbdf694ffd890252d22ddd43933e777c64179`,
  `ev_316f6b1b113558103f94f3537ef210b894b769a2e6d1fa70b733f9f0d8113e0a`.
- **E4:** input builder/D-pad:
  `ev_85de94bb76e4b62497c487d7aa5790ae4a60476f58df62d7f6d3c518db1550ea`;
  analog steering assembly:
  `ev_af08025aa4ce66661994f2de52d44157081e710b4b472f22b6fcb553da020c6c`.
- **E5:** binding record and response curve bytes:
  `ev_81f831b387d62a8070ea895f174039c83189c21074354e8e11654dd6d393ea1e`,
  `ev_7a7e7689b85f8d238c6ec03dbe3f9bb8a0607a45acfe3c71a571e0a66e77145c`.
- **E6:** wheel override / command initialization:
  `ev_028d7b45b1a9cff15e5c8966b14b0feea66295226a7b6fff16f2cb24b4859de6`.
- **E7:** race/car call chain:
  `ev_3a3552772c621fa1a7a5ef53b281aa72606cbb03ad551c8c60fe5380ff33f873`,
  `ev_258503eb44a72bbfba935881d62a546fddbd2f7400ba1d97c66d3b557b0d5ae7`,
  `ev_817743565b2b263540e4c0e8f0c7cd82fe3367e1ce4aeb51dd8ae0eee7b39059`.
- **E8:** driving command processing:
  `ev_4827844f7d8db4d5eae4302c47de04a2f2d0a72fee6ddfa4856e821bf4004958`;
  curve interpolation:
  `ev_e555a6259e2c5e108e5ce8560ddf19c07a3c0874d952675829b973cbf082011d`.
- **E9:** filter assembly:
  `ev_67389fdd72969c49440306f79a8c71a31fd08d161d23fc51c862ac51beea078f`;
  constant bytes:
  `ev_73399956aa65cd8b44f5b967461daa408d96d3eb350584c299a7da744f90b6ff`.
- **E10:** wheel consumer assembly:
  `ev_464ad4dc56725a0bbce11f13295d37e02a91f7a1dd622e71a3404b712bfa85b9`,
  `ev_e9a9679bdbb3b9a5852265471de6bd5dcf087f264adda19144cf18d43e142806`.
- **E11:** downstream wheel-motion processing:
  `ev_68b9d2a98b2acf90c85fbda52eca856fa3fef3be8efc4e07c2ca6d336024b9e0`;
  radian trig functions:
  `ev_4255a44477d79bb26d836a40202151a69e68c20648fc72ff8d86565a51d314f0`.

**Answered:** report byte -> state word -> mapping/curve -> command ->
vehicle envelope/filter -> actual steering float -> wheel-angle consumer.
**Not claimed:** current in-game object addresses, an observed live mapping,
stock-vehicle numeric limits, virtual-hook effects, full tire-force/yaw
reconstruction, or exact physical-PS2 floating-point equivalence.
