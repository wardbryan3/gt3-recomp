:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

# Optional virtual clutch and H-pattern v1

## Classification and checkpoint

This is an **optional gameplay extension**, not recovered original input behavior,
not an original clutch API, and not a clean transmission replacement. It deliberately
changes two transmission policies within a bounded original-execution profile.
The original generated game remains the default behavioral authority.

At this historical checkpoint, canonical `ps2run`, root CMake/build authorities,
root `ALL` behavior, original archives, Frozen systems, clean implementations and
their expected evidence were unchanged. The separate experimental runner was named
`ps2run-extensions`, built only by an explicitly invoked additive builder; it was
not installed into canonical `ps2run`. No generalized plugin framework, controller
hardware backend or runtime source checkout was introduced. Build inclusion and
startup activation were independent.

The earlier [architecture proposal](architecture-proposal.md)
and stopped original-input boundary investigation preceded this bounded extension.
The latter's counterexamples are retained below. Subsequent authorization for this
historical experiment allowed the new policies; using original stores does **not**
make them original-equivalent. Neither that permission nor this proof is current
product installation approval. [Current architecture](../../architecture/index.md) separates
policy from PS2 binding, and neither current product links this extension.

## Separation and execution

Maintained source ownership is now
`src/gt3/gameplay/transmission/virtual/controller.{hpp,cpp}` for policy and
`src/gt3/bindings/ps2/virtual-transmission/` for the concrete EE binding. The
following paths and runner composition describe the **evaluated historical build**,
not the current root build graph or a supported installation command:

- `extensions/gt3/virtual_transmission/controller.{hpp,cpp}` owns typed host inputs,
  virtual Neutral, accepted H position, clutch and connection state. It has no
  `Cpu&`, guest-memory interface or calibration access.
- `extensions/gt3/native_bindings/` owns the concrete guarded EE binding and isolated
  host-input adapter. The builder creates private overlays, not canonical source edits.
- `scripts/build_gt3_extensions.py` names explicit sources and emits source/proof
  identities and a link map. It requires hash-checked passing continuation receipts and
  reruns their executable before building a runner. Output directories must be new.
- No recovered transmission library is linked or implicitly enabled. The initially
  supported composition is **original admission, original engine, original
  synchronization, original drivetrain, original ratio commit** plus this extension.
  Clean-admission/selector/helper options are rejected, not silently composed.
- Canonical and freshly linked unchanged baseline-control binaries have no extension
  symbols or extension link inputs. A separate build-gate-zero observer control lacks
  `Controller::step`; enabling its absent feature is rejected. Its diagnostic binding
  is not claimed to be binary-identical to baseline or to contain no observer code.

The old mixed `gt3_recovered` root-ALL target was a property of that historical
graph. It is not the current graph: current ownership separates recovered controls,
transmission, input adaptations, virtual policy and binding compile checks. See
[architecture](../../architecture/index.md) and [workflow](../../developer-guide/workflow.md). Compiling those source
contracts or gate-OFF/ON binding checks does not enable the extension in a product.

## Why original inputs cannot provide these guarantees

The stopped feasibility audit (`bea85fcc9bf76f55b1c28b3997d3b438b72388cb`)
established an **original-policy limitation at the inspected entry points**, not
an impossibility of a deliberate extension or a whole-program absence theorem.
Original [update order](../transmission/state-transitions-v1.md) is candidate/control → admission
→ drive → engine/synchronization → selection/ratio commit.

| Original mechanism | Counterexample to unconditional clutch/Neutral guarantees |
|---|---|
| Candidate zero at `001E6D48` | State 1 enters 0, but states 2/3 retain state and prepare rates; no guaranteed pre-drive cancellation |
| Candidate nonzero from state 0 | Directional-speed/accelerator or sampled-RPM tests can veto admission; release alone cannot guarantee synchronization |
| Engine aborts | Conditional, after drive, with completion taking priority; not an unconditional disconnect |
| Ratio-only `001E4E78` | Changes selected ratio without disengaging or starting synchronization |
| Selection phase `001E77F8` | Accepted nonzero state becomes 2/3; accepted state 0 stays 0; no nonzero→0 disconnect |
| Reset/moving initialization | Broad control/rate resets or setup, not a clutch API |

**54 original-only synthetic probes**, each with a whole-32MiB mutation-surface
check, comprised 18 whole admission calls, 4 engine interior semantic projections,
16 ratio-leaf calls and 16 selection-phase projections. The engine/selection
projections were **not whole-function ABI comparisons**. Key counterexamples:

- State 2 + candidate 0 remains 2; state 3 + candidate 0 remains 3 in admission.
- State 0, forward 1, candidate 1, speed 0, RPM 800, threshold 2500 remains 0 and
  clears candidate even at accelerator 0, 0.25 **and 1**.
- State 0, forward 1, candidate 1, speed 8 m/s, RPM 6000 remains 0 at accelerator
  0 or 0.25. Accelerator **strictly above** 0.25 admits 2 on that route; RPM 2501
  admits 2 on the low-speed route. Positive controls show the fixtures are active.

The original-only executable reproduced byte-for-byte and all 54 outputs matched.
The same audit rederived **77 retained state-2 drive stages with candidate zero
and nonzero engine-directed effort** from the earlier 4,508-update engagement
population described in [power transfer](../transmission/power-transfer.md).
This includes engine braking, not necessarily positive acceleration. It launched
**zero new native gameplay runs**: these are the same retained counterexamples,
not 77 additional independent observations or feature-ON results.

Overriding candidate alone therefore cannot meet the requested unconditional
pre-drive free/release behavior. Soliciting a brake/handbrake abort adds unwanted
braking and still cannot guarantee timing; state 3's zero transfer in observed
zero-coefficient fixtures is not universal. Calibration or policy-byte forcing
would not recover an original input interface either.

The audit stopped with no controller or OFF/ON acceptance. Its private original-only
proof remains `local/virtual-transmission-v1/`, separate from the later extension
proof below. The later implementation deliberately adds pre-drive 2/3→0 cancellation
and valid-gear 0→2 admission through guarded original continuations. Choosing an
original state store with a new predicate is **new policy**, even without a host
state-byte store. This resolves implementation feasibility only as an **Enhanced**
experiment; it does not contradict the original-input limitation or approve current
product integration.

## New policy, and what remains original

At the original `001E6D48` admission entry, the binding checks the caller, stack,
GP, depth, budget, original code/profile and player state before choosing a route:

1. **Clutch held, virtual Neutral, terminal input loss, or pending valid ratio
   change:** execute the original prefix/frame and original `001E6E18` zero-state
   continuation with a zero comparison operand. This reaches the original state-0
   store and epilogue **before drive**, including when entering in state 2 or 3.
2. **Released clutch, accepted valid gear, incoming state 0, no pending ratio
   change:** execute the original prefix and original state-2 preparation/store path.
   The normal speed/direction/accelerator/RPM admission veto is deliberately bypassed.
   Original effective-policy selection, saved engine/target rates, target helper,
   state-2 calculations, synchronization, completion, aborts and clamp remain original.
3. Otherwise, run the original admission body. In particular, the original state-1
   candidate-zero clearing and post-drive aborts are not suppressed. A held released
   request retries through original preparation on the next state-0 update; it never
   forces immediate state 1 or overrides an original completion/abort calculation.

The extension does not directly write state bytes, ratio bytes or drivetrain effort.
The only new routing is to the explicitly approved original continuations. The
controlled shadow temporarily executes/restores a separate original reference image;
those test restores are not the runtime control mechanism.

At original selector entry `001E5690`, accepted pending H selection returns the valid
ratio while already disengaged; otherwise it returns the original no-selection
sentinel. The original `001E77F8` path and `001E4E78` ratio-only leaf perform any commit.
Original relative/sequential shift requests cannot override the active virtual H
position. This deliberately bypasses the relative selector, including its own timer
processing; original engine completion stores remain intact. It is not an extra
input layered on top of an independently active original selector.

Changing H position is accepted while clutch is currently/prior-sample pressed,
while virtually Neutral, or while the original transmission is already free.
Otherwise the change is rejected and the accepted gear is retained. A new valid
ratio is committed while free; released-clutch synchronization starts on the next
update. This explicit one-update ordering avoids passing through original state 3
for a newly selected ratio or driving with a changed ratio while engaged.

`0` in original ratio memory remains **Reverse**. Neutral is host `-1`, never a
fabricated game ratio or HUD code. Available forward positions are bounded by the
original `car+0x20A` maximum; the qualified native vehicle has six forward gears,
not every GT3 vehicle. Unavailable positions do not reach a table lookup or commit.
`car+0x139C` remains an original candidate, not a physical clutch percentage.

There is no analog clutch/slip/friction model, damage model, engine-effort rewrite,
physics retune, calibration/parts/settings/save change or synthetic Neutral display.
Host policy work consumes no fabricated guest cycles. Executed original paths retain
their exact costs; the new selector return contract charges two guest instructions.
Feature-ON is not asserted to have the original selector's CPU output or cost.

## Activation, input contract and loss

The following CLI and lifecycle contract belongs to the historical experimental
runner, not either current product. The executable must be built **with** the feature and receive
`--virtual-transmission` at process startup. Default is OFF in both dimensions.
There is no live enable/disable/rearm command. `--vt-at` changes inputs, not activation.

| Argument | Meaning |
| --- | --- |
| `--virtual-transmission` | Explicit startup activation |
| `--vt-initial C:G` | Initial binary clutch and H position; defaults to `1:N` |
| `--vt-at F:C:G` | Complete input sample at guest frame F |
| `--vt-disconnect F` | Terminal source-disconnection notification at guest frame F |
| `--extensions-shadow` | Independently controlled-original admission shadows; requires activation |
| `--extensions-trace NEW_FILE` | Read-only qualified player CPU/field observations; does not enable anything |

C is exactly `0` or `1`; G is `N`, `R`, or unsigned decimal `1..255`.
`0` is not a textual H position: use `R`. Unavailable forward positions are rejected
by the controller. Frame values are unsigned 64-bit decimals. Events must be strictly
increasing, with no duplicate frame across input/loss events. Conflicting events,
malformed/overflowed values, absent-build activation, shadow-only activation and
unsupported clean combinations are rejected before gameplay. RAM-patch, axes and
triple diagnostic combinations are rejected by the extended host even while OFF;
the existing canonical diagnostics were not changed.

The v1 host source is a startup-configured **virtual event stream**, not a physical
USB/HID driver, keyboard mapping or a hot-pluggable device backend. The typed input
contract represents connection explicitly; either a disconnected initial/sample
packet or a loss notification permanently latches host Neutral/free. Later connected
samples cannot rearm it. Polling and handoff occur at the guarded per-update boundary,
not at arbitrary sub-instruction time. Physical adapters/FFB remain out of scope.

Loss keeps the extension active, zeroes engine-directed transfer through the original
state-0 path before each drive, and suppresses original shifting. There is **no silent
original-controls fallback** while active, and no restoration of an old ratio/state.
Restart from a supported original fixture is required to rearm.

Unsupported active code, calibration, owner/mode/policy, GP, pointer, caller, stack,
depth, state, budget or update sequence causes a fail-closed process stop. Qualified
player authority must precede every vehicle drive in the supported update order;
a missing/moved owner cannot simply leave all vehicle updates running original while
an active clutch feature is inert. Nonplayer behavior otherwise remains original.

## Bounded supported contexts

Activation requires `PS2_ONE_THREAD=1` and one of **five authenticated original
native-v3 startup states**: existing MT cycle, moving, braked and positive-helper
fixtures, plus a new original-only MT-cycle snapshot already in state 3. Fingerprints
are profile guards, not a claim of cryptographic anti-tamper protection. Private
acceptance separately authenticates the originals and artifacts with SHA-256.

The evaluated player/car/configuration, owner 0, mode 0, stored policy 1, caller depth 3,
fixed observed SP/RA/GP and continuous racing update order are intentionally narrow.
No AT, policies 2–6, alternate owners/callers/cars/configurations, initialized-from-menu
session, arbitrary snapshot, pause/reset/mode-change, parallel-mode, windowed/device
or long-session acceptance is claimed. Unknown active contexts stop rather than
promise a held-clutch-safe fallback. Existing original gameplay remains available
in canonical `ps2run` without any extension constraints.

Host extension state is not serialized into the original game save format. A saved
feature-ON world is not an approved activation fixture. Restarting or returning to
original gameplay does not retroactively establish parity after deliberate ON actions.

## Evidence and acceptance

All expected continuation results come from independently controlled **original**
generated bodies, not the recovered state models. The private reference changes only
function/table names and exposes test entries at the two continuations. Inverse
transformation must reproduce the authenticated original source exactly. Engine,
synchronization, drive and commit bodies remain original.

- **46,932 public pure-policy checks**, including maximum 255, invalid positions,
  Neutral/Reverse distinction, release ordering and terminal loss. No proprietary input.
- **12,288 complete CPU/FCR/ABI/exact-cost continuation comparisons**, comprising 8,192
  admission OFF/free/start cases and 4,096 selector-to-original-commit cases; **192**
  whole-32MiB comparisons plus object/stack comparisons on every case. These establish
  controlled-original boundary contracts, not whole-engine replacement ABI.
- **15 standalone active guard rejections**: GP/SP/RA/upper pointer, budget/depth,
  code/calibration, state/gear/owner/mode/policy, missing-player authority and duplicate
  update. Deliberately invalid fixtures are standalone tests, not injected gameplay.
  Two positive typed-source tests separately establish disconnected initial/event
  packets choose free before guest execution, leaving complete CPU and 32MiB unchanged.
  **21 startup/CLI rejections** separately cover absent inclusion/activation, malformed
  input, event ordering, unsupported startup/mode, clean and diagnostic combinations.
- **42 final OFF native runs / 16,128 updates**: six scenarios × original, unchanged
  baseline control, build-gate-zero OFF/trace, included-default-OFF, trace and trace
  repeat. Exact native snapshots, complete 36MiB dumps and captures; three-way
  **unmasked complete CPU/cost traces**. OFF was tested before ON.
- **15 final ON native runs / 6,162 updates**: five scenarios × ON, shadow and repeat.
  Exact snapshots/dumps/captures and unmasked CPU/cost traces across shadow/repeat.
  Actual counters: **4,023 free routes, 57 synchronization starts, 2,082 original
  admission routes, 6,162 selector returns, 63 original ratio commits, 90 rejected
  H-position samples; 4,108 real-entry complete CPU/cost/32MiB controlled-original
  admission shadows**. Host intent alone is not counted as execution.
- ON covers cancellation of original state 2 and original state 3 before drive,
  all six supported forward positions plus Reverse, held clutch and released Neutral
  under high throttle, an 800-update sequence, rejected unavailable/unclutched shifts,
  and suppression of conflicting native relative commands. The long held/free stages
  contain **255 distinct sampled RPM values**; zero engine-directed transfer is checked
  before engine integration, not inferred from stopped wheels.
- Moving first-entry CPU is identical to original: ordinary directional admission
  remains 0, extension starts 2 at frame 5350. The braked fixture first commits gear
  4→1 while free at 5350, then starts 2 at **799 RPM** at 5351 despite the original
  RPM veto. This is new admission policy, not recovered input equivalence.
- Original synchronization crossing/completion is independently checked at frames
  **5458 and 5557** in each low-RPM run. It is not an immediate host-written state 1.
  All observed nonzero engine synchronization/clamp projections and rear drive
  bit-pattern products are checked against original phase inputs/calibration.
- Loss during original state 2 at 5352 leaves **349 successive updates** latched free
  per loss run, despite throttle and subsequent connection/input samples. This proves
  the virtual loss-notification contract, **not physical device unplug behavior**.
- **Eight objects/executables** reproduce byte-identically in fresh directories.
  Canonical/baseline binary symbol and link-input exclusion is checked independently.

The state-3 fixture used **three original-only preparation/parity runs (66 updates)**
and a separate original observer qualification (18 updates); no guest state/policy
forcing was used to manufacture a transition. Earlier build/native candidates,
contract receipts and a completed 201-update diagnostic pilot remain private.
The pilot's post-admission observer ambiguously tagged NPC returns as player rows;
it is excluded from final proof. Actual returned caller registers now qualify the
owner, with one player row per stage/update. Corrected contracts, OFF and ON matrices
were rerun; no row normalization, oracle weakening or frozen-hash rewrite was used.
Reducer-development assertions also retained the legitimate original state-1→0
clear and pending-ratio first-update ordering; those were audit expectation errors,
not original-game mismatches. A standalone fixture initially omitted original boot/HLE
server registration; its load failure also triggered the exit coverage check, making
an overly generic negative-test check insufficient. Those attempts are excluded.
The final harness performs original boot/load, requires the **specific** intended
rejection message, and has the two positive entry tests above. A test-only `ntsc`
option-name compile error was corrected to the existing `pal=false` API. No runtime
binding change or native-evidence reuse was needed for these harness corrections.

The separate authority is `extensions/gt3/virtual_transmission/validation.json`.
Private raw code, snapshots, traces, captures, source receipts, attempts and manifest
remain ignored under `local/extensions/virtual-transmission-v1/`. Public audit covers
current-tree publication checks, not all history or a definitive provenance opinion.
No physical hardware, full-game, all-car, whole-engine ABI or clean-composition proof.

## Current checks and historical reproduction {#commands}

Use the root commands, not the retired companion justfile or bespoke builder:

```sh
just check
just test
just docs-build
just verify-extensions "$PWD" # explicit retained historical OFF/ON proof
```

Public checks need no game artifacts. Historical verification includes the unchanged
inherited proof and independent original oracle reexecution; it does **not** relaunch
gameplay or approve current product integration. Missing/changed required artifacts
fail rather than silently skipping. See [workflow](../../developer-guide/workflow.md) and [testing](../../developer-guide/validation.md)
for current-source proof and product qualification as separate claims.

The exact `extensions.just`, `scripts/build_gt3_extensions.py` contracts/build/
baseline-control recipes and accepted per-run commands remain in their historical
Git/private contexts. Their `--with-virtual-transmission` inclusion gate and separate
startup activation belong to that evaluated runner, not a current product option.
An illustrative old schedule started at frame 4501 with `1:1`, requested `4600:1:3`,
`4620:0:3`, `4800:0:N`, and disconnected at 4900; it was not the native acceptance
matrix. No current installation, broader recovery or physical-controller work is
authorized by this checkpoint.
