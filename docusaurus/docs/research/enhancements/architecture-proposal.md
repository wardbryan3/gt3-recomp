:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

This proposal predates the later bounded
[virtual-transmission implementation](virtual-transmission-v1.md). Its proposed
additive builders, source layout and approval questions describe that earlier
design stage, not the current build graph or an outstanding work order.
See [current architecture](../../architecture/index.md) and
[current authorities](../../reference/authorities.md) for present ownership and
approval boundaries. Neither this proposal nor the later historical extension
proof authorizes current product integration.

:::

# Historical optional gameplay extensions architecture proposal

**Historical proposal only.** The project must retain an original-gameplay native baseline.
Virtual clutch/H-pattern is exclusively an extension, not clean recovery. No
transition-policy override is approved by this document. No implementation,
canonical/Frozen/build change, plugin framework, commit or push is included.

Inspected source context: `bea85fcc9bf76f55b1c28b3997d3b438b72388cb` plus the
previously untracked virtual-transmission boundary report. This is source/build
architecture inspection, not fresh binary recovery or gameplay validation.

## 1. Three categories, independent authorities

The categories remain useful; the default-use column describes the inspected
historical context. For the current two-product graph and separate integration
approval, use [architecture](../../architecture/index.md) and
[current authorities](../../reference/authorities.md), not the proposed builder
below.

| Category | Contract | Default game use at this proposal |
| --- | --- | --- |
| Original generated GT3 | Behavioral authority within the supported ELF/runtime profile | Yes |
| Clean recovery | Independently demonstrated original behavior at a specified boundary, including ABI/cost/guards where claimed | Validation-only; never silently substituted |
| Extensions | Deliberate new inputs, policies or gameplay behavior | Absent from baseline product; explicit build inclusion AND runtime enable required |

Clean recovery is not a prerequisite for an extension: an extension may bind to
original execution while preserving original calculations. A recovered body must
not acquire extension flags, a forced-admission mode, or alternate clutch rules.
Extension acceptance does not promote a clean function or change its authority.
Neither category claims universal original-console equivalence from native tests.

Virtual pedals, virtual handbrake and synthetic-wheel input are logically
extensions/input adaptations, despite their historical locations under `host/`.
The proposal left their source and proof untouched and proposed the separation
below for new code. Maintained source ownership now lives under `src/gt3/`, as
explained in [architecture](../../architecture/index.md); directory/target names alone are not
behavioral evidence.

## 2. Historical mechanisms and gaps {#2-existing-mechanisms-and-gaps}

This inventory is specific to `bea85fc`, **not the current root graph**. The old
mixed library and additive scripts are no longer maintained build instructions;
exact evaluated versions remain in Git/private contexts. Current products share
original generated execution, exclude these gameplay libraries, and use the
[root workflow](../../developer-guide/workflow.md) with separate [validation layers](../../developer-guide/validation.md).

- **Historical canonical linkage:** root CMake built `ps2game` from `PS2_GENERATED`
 and linked `ps2run` to `ps2game`/`ps2runtime`, not `gt3_recovered`.
 `scripts/port.sh` explicitly built `ps2run`; `scripts/build_gt3.sh` used that path,
 with triple projection a separate explicit option/output.
- **Historical mixed build-all graph:** root CMake unconditionally defined
 `gt3_recovered`, mixing clean steering/pedals/handbrake with synthetic-wheel input.
 Developer all-target/test builds could compile extension source even though
 canonical `ps2run` did not link it. Transmission validators built recovery
 separately. This motivated the proposal; it does not describe today's separated
 controls/transmission/adaptation/policy/binding-check targets.
- **Historical opt-in examples:** `scripts/build_gt3_virtual_{pedals,handbrake}.sh`
 created private fresh-output validation hosts/units and compile-time gates;
 `Options.enabled` defaulted false, independently of runtime CLI opt-in.
 Their OFF executables could still link adapter objects: useful validation
 controls, not proof of complete binary exclusion.
- **Existing bounded integration:** transmission validators insert gates at
 generated labels, reuse original helpers, record identities, and run independent
 original oracles and real-entry shadows. Admission is whole-function recovered;
 engine/selection decision models are not whole-function ABI replacements.
- **Dispatcher limitation:** `recomp/codegen.cpp` emits direct calls and local
 gotos. Changing only `runtime/src/dispatch.cpp` cannot own every entry or resume.
 Existing `on_probe` is a mutable, single callback, not a safe extension bus; an
 extension must not silently replace another observer or presentation callback.
- **Legacy diagnostic exceptions:** `host/main.cpp` already contains explicit
 `--ram-word` and `--gt3-triple` paths. Neither is active by default; arbitrary RAM
 patching is not an approved future gameplay-extension API. Strict parity runs
 must reject these options. Removing/reclassifying their compiled support would
 be a separate change to a protected host, not something this proposal performs.
- **Historical Frozen build boundary:** authorities including
 `decomp/gt3/{transmission,transmission-state,virtual-handbrake,handbrake}.json` pinned
 root CMake/host/build files. That proposal did not permit moving source or editing
 those files/pins. Later restructuring preserves the exact old proof contexts;
 these pins are not a description of current source ownership.

## 3. Historical build proposal: additive first, no root refactor {#3-build-separation-additive-first-no-root-refactor}

The requirements in this section describe the proposed isolated experiment. They
are not an instruction to recreate a parallel product or undo current architecture.
The later [implementation](virtual-transmission-v1.md) records the bounded experiment;
[current architecture](../../architecture/index.md) owns today's product graph.

### Proposed baseline product {#baseline-product}

The proposal would keep canonical `ps2run`, original generated directory, runtime and
`--target ps2run` build path unchanged. New extension directories are not added
to root source lists, includes, generated-code globs or linkage. No extension
initializer, parser, input backend, state or seam binding is compiled into that
product. Baseline launch defaults contain no extension flags/configuration.
Authenticate the baseline generated-input manifest and generation recipe; a stale
`PS2_GENERATED` path must not accidentally select an extended output directory.
The canonical target name alone does not authenticate its game input.

Prove exclusion from compile commands, dependency/link maps and source manifests;
symbol inspection is supplementary, not sufficient under optimization/LTO.
Do not rely on a false runtime boolean, archive dead stripping, or weak no-op hooks.

**Historical approval question:** the proposal distinguished the default *game
product/target* from bare `cmake --build`, which could compile legacy extension
source. Root-ALL exclusion would have required a separately reviewed build-authority
change; the proposal did not authorize editing pinned CMake. The mixed-library
observation must not be repeated as a claim about the restructured current graph.

### Proposed extended product {#extended-product}

Propose a new additive builder, e.g. `scripts/build_gt3_extensions.py`, that
requires an explicit feature selection and creates a distinct
`ps2run-extensions` in a fresh ignored build directory. It reuses authenticated
original sources/archives; only explicitly named generated units are overlaid
into that private output. Original generated files, baseline outputs and game
RAM instruction bytes are not patched in place.

No root CMake option/include is necessary for the first version. Reuse the
existing isolated-builder method rather than copy a runtime checkout. Explicit
source lists replace directory discovery. Exactly one active definition of each
replaced generated unit/entry table is allowed; independently named oracle units
must remain unhooked. Check the link map rather than permit duplicate symbols.
Unselected extensions are not compiled or linked. An optional additive `extensions.just` can expose the workflow without
changing the root recipes. These names were proposals at that stage. The later
historical experiment used them; those builders/companion recipes are now retired,
not maintained alternatives to root commands.

Build inclusion only makes a feature available. Each runtime enable defaults false;
inputs/schedules do not enable it implicitly. Absent/not-built, malformed or
conflicting requests fail before gameplay. No environment, saved preference,
card or loaded snapshot automatically activates an extension. Help/logs identify
the selected build features, actually enabled features and independent clean gates.

## 4. Historical code/state ownership and execution-boundary proposal {#4-codestate-ownership-and-execution-boundary}

The following was a suggested layout, without relocating source at that stage.
Maintained virtual policy is now in `src/gt3/gameplay/transmission/virtual/` and
its concrete binding in `src/gt3/bindings/ps2/virtual-transmission/`;
[architecture](../../architecture/index.md) is the current ownership reference.

Historical proposed layout:

```text
extensions/gt3/virtual_transmission/   typed inputs, host state, policy, acceptance metadata
extensions/gt3/native_bindings/       feature-specific guarded EE boundary adapter
scripts/build_gt3_extensions.py       explicit product/source/overlay selection
tests/...                            public pure-policy tests + private-oracle test source
local/extensions/...                 generated overlays, builds, traces and proof (ignored)
```

Use a small concrete module and explicit calls, not registration/discovery APIs.
One compile-time feature list and a short supported-combination check are enough.
No dynamic libraries, plugin ABI, hook priorities, automatic scanning, generic
memory-patching interface, or generalized DriverInput system.

Control flow is conceptually:

```text
qualified boundary
  -> extension absent/inactive: unchanged original execution
  -> active: typed feature decision -> guarded feature-specific adapter
                                      -> approved original execution path
```

Keep input parsing/policy separate from EE binding. Proposed input is a connected
sample containing binary clutch and `Reverse | Neutral | forward index`; distinguish
Neutral, no new sample and disconnection. Host state owns accepted H-position,
Neutral, input sequencing and qualified owner/lifetime identity. Forward-gear
bounds come from original `car+20A`, not a six-gear assumption. No new original
ratio index, HUD state or save/card format fields.

Bindings expose only bounded operations, not arbitrary state-byte addresses or
`Cpu&` to policy code. Validate profile, caller/owner, pointer/frame lifetime,
call depth and scheduling/budget context before extension mutation. A narrow
adapter cannot make an unvalidated continuation safe merely by naming it an API.

Recovery implementations/headers/guards remain byte-identical. Bindings may use
an unchanged validated recovered entry only under its existing contract and
separately tested composition. **Initial virtual transmission should bind to
original admission execution.** A clean whole-admission substitution can bypass
an interior generated gate; reject that unsupported combination rather than edit
the recovery or assume hooks compose. Enabling an extension never enables clean
substitution automatically. Unaffected clean combinations require their own proof.

Lifecycle is explicit: attach only in qualified context; invalidate host ownership
on guest reload/reset/owner change; do not auto-arm from a snapshot. Keep feature-ON
outputs separate from original oracle fixtures. Deactivation cannot undo earlier
changes to the game world; it must hand off at a validated boundary, not restore
old ratio/state bytes. Input-loss and unsupported-runtime-context behavior require
an approved policy; silent fallback must not be advertised as a held-clutch safety
guarantee. Original snapshot format and originals remain unchanged.

## 5. Historical clutch/H-pattern example — not approved by this proposal {#5-concrete-clutchh-pattern-example--still-not-approved}

Original order is admission -> drive -> engine/synchronization -> selection/commit.
The [retained boundary counterexamples](virtual-transmission-v1.md#why-original-inputs-cannot-provide-these-guarantees)
explain why candidate zero/one alone cannot implement the unconditional guarantees.
The later historical extension was deliberately different from original policy;
that result is not current product installation approval.

The following actions awaited permission and bounded proof **at proposal time**:

| Need | Extension-owned decision | Original behavior to retain |
| --- | --- | --- |
| Clutch pressed / host Neutral | Pre-drive choose disengaged path, including cancellation from2/3; prevent ordinary re-admission while held | Original free-engine integration and state0 drivetrain routing |
| Released, valid committed ratio, currently free | Override normal admission predicates and choose state2 write plus original rate preparation | Original target derivation, samples, synchronization math and subsequent completion/abort decisions |
| Already synchronizing, still released | No repeated restart merely because input remains released | Original transition progression |
| Valid H-position change while free | Validate available ratio and commit without engagement | Original ratio-only001E4E78 behavior; Neutral remains host-only |
| Active H-authority | Suppress conflicting original selection results at a validated selection boundary | Original commit machinery and downstream processing |

These are deliberate **extension policies**, not recovered-original semantics.
This proposal did not approve pre-drive2/3→0 cancellation or unconditional0→2
admission. Selecting an original state-store path is not by itself sufficient justification
under the no-state-forcing constraint. No forced1, target/wheel-rate patch, fake
policy/configuration, new torque calculation, changed calibration or processed
candidate-as-clutch shortcut is proposed.

At proposal time, precise ratio-commit/admission ordering still needed proof:
synchronize only against the newly committed ratio, not briefly against the old
one. Unclutched requests, Neutral entry/exit, activation, loss/handoff and simultaneous
inputs also needed deterministic tests and owner agreement. The later
[implementation contract](virtual-transmission-v1.md#new-policy-and-what-remains-original)
records its accepted-position ordering and terminal-loss policy; it does not
establish a general runtime handoff or physical-device contract.

## 6. Parity and validation plan — not results

Use the same original ELF, generated-input identities, compiler/runtime context,
original snapshots, pad schedules, external clock and qualified execution mode.

| Product/run | Required relationship |
| --- | --- |
| O: authenticated unmodified generated-original reference | Authority, never feature-enabled |
| B: canonical baseline product | Exact O parity; no extension objects/bindings linked |
| E0: extended product, all extensions disabled | Exact O/B parity; zero extension actions and independent clean gates OFF |
| ET: extended trace-only, extensions disabled | Same guest results; observers read-only; cannot prime controller state |
| E1: explicitly enabled extension + repeat | New-policy assertions plus preserved original-path/calculation checks, **not equality to O** |

For O/B/E0 compare exact complete CPU/ABI/FCR/PC/SP/budget at relevant boundaries,
final native-v3 state, entire EE/IOP/SPU dumps and deterministic captures. Use
paired original/read-only-observed builds where traces require instrumentation;
production-artifact comparisons are also required. No blanket PC/RAM masks,
weakened comparisons or hash rewrites. Pin any existing narrowly qualified trace
transport convention explicitly, never apply it to outgoing/shadow CPU or RAM.
Guest cost/scheduling equality is not a host-performance or physical-hardware claim.

Also prove: default CLI cannot enable an absent feature; schedules without enable
reject; disabled paths do not mutate CPU/RAM/guest budget, install active input
handling or consume input into controller state. Check build/link exclusion and
startup side effects, not only zero gameplay counters. Do not use shared build
caches/output directories to overwrite original unit objects.

After transition-policy approval: independently validate each seam/continuation
contract and allowed mutation surface; replay original execution with explicit
controller decisions as a controlled reference; then native shadows, real enabled
runs and repeats covering the requested edges and longer high-throttle holds.
ON is intentionally different from original admission, so mark each deviation
rather than claiming whole-function ABI equivalence for decision models.

Test ON->OFF handoff separately against original continuation from the same
handoff guest state; it cannot equal the untouched original history retroactively.
Keep unchanged Frozen suites/strict authorities and relevant steering/pedal/
handbrake/selector regressions. Public tests need no game artifacts; explicit
private verification must fail on missing/changed required evidence. Root check,
test, docs and audit remain required, not substitutes for native proof.

## 7. Historical minimum change and approval gates {#7-smallest-changes-and-approval-gates}

These were the proposal's gates, not outstanding permission to implement or install
anything now. Current approval boundaries are recorded separately in
[current authorities](../../reference/authorities.md).

If approved at that stage, add only feature-owned source/input/state/policy, one guarded
binding for each necessary seam, one explicit isolated product builder, and its
additive tests/docs/acceptance authority. Reuse profile/hash preflight, reversible
source overlays, renamed independent oracles, original helpers, real-entry
CPU+RAM shadows, exact-budget comparisons, native-v3 fixtures, default controls,
exclusive output paths and strict evidence manifests. Do not reuse old artifacts
as proof of a new integration or automatically chain arbitrary probe callbacks.

Decisions requiring approval:

1. Product separation and the meaning of strict default exclusion: baseline
 target/artifact versus root ALL, plus disposition of legacy RAM-patch/presentation
 diagnostics. Literal root ALL purity was not established by the then-pinned files.
2. The explicit virtual transition-policy overrides, separately from architecture.
 Approval of this proposal alone does **not** approve them or the controller.
3. Supported initial profile/owner/policy contexts and incompatible clean/extension
 combinations; expand only with evidence, not a generalized conflict resolver.
4. Activation, unclutched requests, disconnection/unsupported-context and snapshot/
 handoff policies, plus the accounting contract for any new execution path.

**Historical recommendation:** preserve the baseline and Frozen infrastructure,
introduce an additive opt-in experiment without a plugin system, resolve policy
decisions and prove original-boundary bindings before implementation. The later
[extension checkpoint](virtual-transmission-v1.md) records that bounded result.
Neither page authorizes current product integration, new hardware work or a new
builder; maintained commands and gates are in [workflow](../../developer-guide/workflow.md) and
[testing](../../developer-guide/validation.md).
