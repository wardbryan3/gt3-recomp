:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::

# Optional gameplay extensions — minimal architecture proposal

**Proposal only.** The project must retain an original-gameplay native baseline.
Virtual clutch/H-pattern is exclusively an extension, not clean recovery. No
transition-policy override is approved by this document. No implementation,
canonical/Frozen/build change, plugin framework, commit or push is included.

Inspected source context: `bea85fcc9bf76f55b1c28b3997d3b438b72388cb` plus the
previously untracked virtual-transmission boundary report. This is source/build
architecture inspection, not fresh binary recovery or gameplay validation.

## 1. Three categories, independent authorities

| Category | Contract | Default game use |
| --- | --- | --- |
| Original generated GT3 | Behavioral authority within the supported ELF/runtime profile | Yes |
| Clean recovery | Independently demonstrated original behavior at a specified boundary, including ABI/cost/guards where claimed | Currently validation-only; never silently substituted |
| Extensions | Deliberate new inputs, policies or gameplay behavior | Absent from baseline product; explicit build inclusion AND runtime enable required |

Clean recovery is not a prerequisite for an extension: an extension may bind to
original execution while preserving original calculations. A recovered body must
not acquire extension flags, a forced-admission mode, or alternate clutch rules.
Extension acceptance does not promote a clean function or change its authority.
Neither category claims universal original-console equivalence from native tests.

Virtual pedals, virtual handbrake and synthetic-wheel input are logically
extensions/input adaptations, despite their historical locations under `host/`.
Their existing source and proof remain untouched; new code follows the separation
below. Directory/target names alone are not behavioral evidence.

## 2. Existing mechanisms and gaps

- **Canonical linkage:** `CMakeLists.txt:125–156` builds `ps2game` from
 `PS2_GENERATED` and links `ps2run` to `ps2game`/`ps2runtime`, not `gt3_recovered`.
 `scripts/port.sh:110–115` explicitly builds the `ps2run` target. Standard
 `scripts/build_gt3.sh` uses this path; triple projection is a separate explicit
 option/output.
- **Not a pristine build-all graph:** `CMakeLists.txt:74–89` unconditionally defines
 native `gt3_recovered`, mixing clean steering/pedals/handbrake with
 `gt3_synthetic_wheel.cpp`. Developer all-target/test builds can compile extension
 source even though canonical `ps2run` does not link it. Transmission recovery is
 separately built by additive validators, not automatically installed by CMake.
- **Existing opt-in examples:** `scripts/build_gt3_virtual_{pedals,handbrake}.sh`
 create private, fresh-output validation hosts/units and compile-time gates;
 their `Options.enabled` defaults false and runtime CLI opt-ins are separate.
 Their off executables can still link adapter objects: these are useful
 validation controls, not proof of complete binary exclusion.
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
- **Frozen build boundary:** current authorities, including
 `decomp/gt3/{transmission,transmission-state,virtual-handbrake,handbrake}.json`, pin
 root CMake/host/build files. Moving existing source, editing those files or
 rewriting pins would violate the present preservation requirement.

## 3. Build separation: additive first, no root refactor

### Baseline product

Keep current canonical `ps2run`, original generated directory, runtime and
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

**Definition needing approval:** this is the default *game product/target*, not
an assertion that bare `cmake --build` compiles no legacy extension source. If
strict exclusion must also apply to root ALL/developer builds, the existing mixed
library requires a separately reviewed, versioned build-authority migration (or a
new explicit-source product build). Do not quietly edit pinned CMake or claim
this stricter property already holds.

### Extended product

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
changing the root recipes. All names here are proposed, not existing commands.

Build inclusion only makes a feature available. Each runtime enable defaults false;
inputs/schedules do not enable it implicitly. Absent/not-built, malformed or
conflicting requests fail before gameplay. No environment, saved preference,
card or loaded snapshot automatically activates an extension. Help/logs identify
the selected build features, actually enabled features and independent clean gates.

## 4. Code/state ownership and execution boundary

Suggested new layout; no relocation of historical sources:

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

## 5. Concrete clutch/H-pattern example — still NOT approved

Original order is admission -> drive -> engine/synchronization -> selection/commit.
The [boundary audit](virtual-transmission-v1-boundary.md) established why candidate
zero/one alone cannot implement the requested guarantees.

Proposed actions, pending permission and bounded proof:

| Need | Extension-owned decision | Original behavior to retain |
| --- | --- | --- |
| Clutch pressed / host Neutral | Pre-drive choose disengaged path, including cancellation from2/3; prevent ordinary re-admission while held | Original free-engine integration and state0 drivetrain routing |
| Released, valid committed ratio, currently free | Override normal admission predicates and choose state2 write plus original rate preparation | Original target derivation, samples, synchronization math and subsequent completion/abort decisions |
| Already synchronizing, still released | No repeated restart merely because input remains released | Original transition progression |
| Valid H-position change while free | Validate available ratio and commit without engagement | Original ratio-only001E4E78 behavior; Neutral remains host-only |
| Active H-authority | Suppress conflicting original selection results at a validated selection boundary | Original commit machinery and downstream processing |

These are deliberate **extension policies**, not recovered-original semantics.
Pre-drive2/3→0 cancellation and unconditional0→2 admission remain unapproved.
Selecting an original state-store path is not by itself sufficient justification
under the no-state-forcing constraint. No forced1, target/wheel-rate patch, fake
policy/configuration, new torque calculation, changed calibration or processed
candidate-as-clutch shortcut is proposed.

The precise ratio-commit/admission ordering still needs proof: synchronize only
against the newly committed ratio, not briefly against the old one. Unclutched
gear requests, Neutral entry/exit, activation, loss/handoff and simultaneous input
policies need deterministic acceptance tests and owner agreement where ambiguous.

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

## 7. Smallest changes and approval gates

If approved later, add only feature-owned source/input/state/policy, one guarded
binding for each necessary seam, one explicit isolated product builder, and its
additive tests/docs/acceptance authority. Reuse profile/hash preflight, reversible
source overlays, renamed independent oracles, original helpers, real-entry
CPU+RAM shadows, exact-budget comparisons, native-v3 fixtures, default controls,
exclusive output paths and strict evidence manifests. Do not reuse old artifacts
as proof of a new integration or automatically chain arbitrary probe callbacks.

Decisions requiring approval:

1. Product separation and the meaning of strict default exclusion: baseline
 target/artifact versus root ALL, plus disposition of legacy RAM-patch/presentation
 diagnostics. Literal root ALL purity cannot be claimed under current pinned files.
2. The explicit virtual transition-policy overrides, separately from architecture.
 Approval of this proposal alone does **not** approve them or the controller.
3. Supported initial profile/owner/policy contexts and incompatible clean/extension
 combinations; expand only with evidence, not a generalized conflict resolver.
4. Activation, unclutched requests, disconnection/unsupported-context and snapshot/
 handoff policies, plus the accounting contract for any new execution path.

**Recommendation:** preserve the baseline product and Frozen infrastructure;
introduce extensions additively as a separate opt-in product with no plugin system.
Resolve the above decisions, then prove the original-boundary bindings before
controller implementation. Stop here and await approval.
