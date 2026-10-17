:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](restructuring.md) for maintained commands and actual gates.

This is an accumulated pre-restructuring checkpoint history, not a current status
page or work queue. “Latest,” “current,” “fresh,” pass/fail claims and stop
instructions refer to the individual cycles described below. Later checkpoints may
resolve an earlier checkpoint's blocker without changing that earlier result.
Use [current authorities](../../reference/authorities.md) for present source,
proof and approval records. Historical validation-host results do not establish
current product integration or authorize further work.

:::

# Historical checkpoint status and evidence boundaries

## How to read this history

Each section retains its own result, population and source/fixture context;
counts from different cycles must not be added together or substituted for one
another. In particular, the earlier 20,480 control cases, later 25,600
normalization cases, old race snapshot and normal-boot native-v3 fixture are
separate evidence populations. A stopped attempt remains stopped even when a
later authorized cycle resolves its blocker.

Inline `decomp/`, `host/`, `tests/` paths and verifier invocations below describe
their historical cycles. For maintained operation use the root `justfile`:
`just status`, `just check`, `just test` and `just docs-build`. Explicit historical
verification is `just verify-historical PROFILE EXPLICIT_ROOT`; see the
[current workflow](../../developer-guide/workflow.md) for profile and private-input boundaries.
No result here installs recovered gameplay into either current product or
certifies a physical device, headless API or new work authorization.

## Historical virtual throttle/brake checkpoint {#latest-bounded-virtual-throttlebrake-experiment}

[Synthetic / Virtual Pedal v1](../pedals/virtual-input-v1.md) is a separate opt-in
command-input experiment, not a reopened Frozen pedal implementation. It maps
normalized [0,1] toQ12, restores temporary command fields, and reaches original
notification/pedal/brake/engine processing.12,291 oracle cases /24,582 complete
CPU+32MiB comparisons;12 native-v3 cases with generated/clean/repeat,3,599 actual
Frozen replacements and zero fallback. Unchanged baseline/pedal/profile/native/
public/strict proof suites pass. Canonical/default behavior and Frozen sources
remain unchanged. No physical/calibration/DriverInput or adjacent scope. **Stop.**
Authority: `decomp/gt3/virtual-pedals.json`; `just verify-virtual-pedals EXPLICIT_ROOT`.

## Historical observed-context Pedal v1 closure — re-frozen {#latest-observed-context-pedal-v1-closure--re-frozen}

[Closure](../pedals/closure.md), authority `decomp/gt3/pedal-closure.json`:
unchanged semantic body passes4,199 actual-entry complete CPU/32MiB/exact-cost/
mutation differentials and4,199 actual guarded substitutions, zero fallback, all14
observed contexts /five processing classes. The16-byte displacement is the original
96/112-byte mode-caller frame difference, within the same running-thread stack.
Structural frame/return-chain admission replaces the absolute-pointer exception.
Fresh pedal/profile/current baseline live and full native/public/private gates pass.
Both gates default OFF; canonical ps2run remains generated-only and byte-identical.
Historical stopped authorities below are unchanged. **Observed discovery closed;
stop.** No universal/physical proof, new API, canonical installation or adjacent work.

## Prior read-only 0049AF40 admission audit: stopped

[Audit](../pedals/admission-49af40.md): both observed addresses are
activation-local stack command positions, not independently established global
BSS objects. Same original layout/call chain and retained ABI/cost observations;
299 Time Trial entries compare exactly against protective fallback, **not clean
body execution**. Safe admission remains unproven; no expansion. Frozen source,
guard and prior authorities are unchanged. No new gameplay/build/instrumentation.
Authority: `decomp/gt3/pedal-admission-49af40.json`;
`just verify-pedal-admission EXPLICIT_REPOSITORY_ROOT` verifies retained evidence.

## Prior descriptor/profile characterization: stopped

See [the survey matrix retained with closure](../pedals/closure.md) and
`decomp/gt3/pedal-profiles.json`: 4,199 original entries, one descriptor family,
five processing configurations. Four paired cases pass 1,200 substitutions;
Time Trial then records 0 replacements / 299 protective fallbacks with command
0049AF40 instead of previously audited 0049AF50. Remaining clean pairs and fresh
full native regressions were not run after stop. Frozen implementation/authority,
canonical runtime and gate defaults are unchanged. Any admission audit needs
separate authorization. `just verify-pedal-profiles EXPLICIT_REPOSITORY_ROOT`
checks retained stopped evidence, not expanded live equivalence.

## Prior authorized pedal continuation

Committed/pushed baseline `46a32c7` was followed by bounded recovery of
001E48FC–001E4BA7, resume001E4BA8. See [Pedal v1](../pedals/recovery-v1.md) and
`decomp/gt3/pedal-validation.json`:131,072 exact full-CPU/cost join cases,
2,160 wrapper cases/6,480 full-CPU+32MiB comparisons,19 v3 live runs/seven paired
scenarios,2,100 substitutions/zero accepted fallbacks and4,200 original player
brake/engine observations. Traces/captures/complete guest dumps match. Full native
regressions, final public gates and strict private/protected-input checks pass.
The exact bounded validation-only implementation is **Frozen; stop here**. Canonical ps2run
stays generated-only and byte-identical. No physical-pedal API or adjacent recovery.
`just verify-pedals EXPLICIT_REPOSITORY_ROOT` strictly verifies separate new proof.

## Selective-decompilation source checkpoint

At that checkpoint, main preserved the later controls/mapping, clean steering and synthetic
adapter source, partial layouts, original-dependent fixture source, inventories,
curated site and legacy restoration patches. Root justfile is the workflow.
Hardware/SIF and source consistency tests pass; documentation needs no private
artifacts. Strict optional verification checks eleven hashes and66 evidence IDs.

**Clean/synthetic source is compile checked, not installed into current runtime.**
Its exact original differentials/live results describe the preserved older build.
Snapshot3 was the state version at that checkpoint; old v2 race states were not
portable by changing a byte. The referenced HANDOFF.md and
experiments/legacy/README.md were historical handoff locations, not maintained
entry points. No pedal/physical-wheel/FFB/AI API had been implemented by this
checkpoint.

## Historical native baseline (source base 82987de + validation-only overlay) {#current-main-native-baseline-source-base-82987de--validation-only-overlay}

The documented missing CMake/Ninja dependencies are restored. Fresh software and
GPU/native builds pass; four canonical executables built in independent directories
are byte-identical. Current tools regenerate translations; old libraries are not
linked. All applicable native regressions pass, including the full unchanged clean,
controls, pad/wheel, synthetic, original-only pedal, GPU and hardware/SIF suites.

Normal boot produced an identity-pinned **v3** frame-4801 Super Speedway race state.
Defined serialized state and complete guest dumps reproduce; raw independent
snapshot hashes can differ only in compiled native Thread padding. Original files
are not normalized or relabeled. With external UTC input pinned and future pad
input at 4802, snapshot replay matches uninterrupted execution exactly.

Ten new wheel live scenarios pass: 3,400 clean mode-4 updates, 13,600 original
consumers, maximum error 5.96046448e-8, tolerance 2e-6. Clean pad, disabled and
trace-only cases also pass exact traces/captures/full-dump comparisons. These
results use a **validation-only isolated host**, not canonical ps2run installation.
No gameplay/control/render/state-format source changed. No physical proof added.

Authority for that cycle: `decomp/gt3/current-validation.json`; earlier lifecycle/evidence
remains separate. See [reproduction and limitations](native-v3-baseline.md).
Both strict private verifiers and `just check`, `just test`, `just docs-build` pass.
Stop here; pedals remain unimplemented.

## Pedal Recovery v1 audit (earlier stopped cycle, source base 82987de)

The following blockers describe that earlier attempt; native baseline prerequisites
are now restored as recorded above. They are retained as history, not current failures.

Stopped before clean implementation/integration. The candidate tail remains
`001E48FC–001E4BA7`, rejoin `001E4BA8`; no Frozen promotion. Current-runtime load
rejects the retained v2 race snapshot, and no validated v3 fixture/compatibility
path was found in inspected validation locations. Fresh `just test` and GPU build
attempts are blocked by missing `cmake`; `ninja` is also absent from PATH.

Available archive-linked unchanged controls, pad/wheel, clean steering, synthetic
and original-only pedal fixtures passed, as did cached hardware/SIF executables.
These are not fresh builds or new live evidence. Public check, strict private
verification and docs build passed. See [the audit](../pedals/stopped-prerequisite-audit.md)
for contracts, counts, source/build context and the exact prerequisite to resume.
No preserved files or runtime semantics were changed.

## Private experiment observations (before the public-tree rebase)

- GT3 USA v1.10 menus/races and scoped projection/camera changes exercised.
- 20,480 actual translated-routine versus reference input cases passed.
- 9×3 GPU sample addressing and isotropic/anisotropic state conversion passed.
- Hardware regressions, camera comparisons and same-frame save/reload captures
  passed. Full-size compositor captures were identical across execution paths.
- Parallel execution produced approximately 60 requests/sec in three repeatable
  scenes; virtual presentation still had occasional 33 ms gaps.
- A user tested center-cropped 1920×1080 WebRTC delivery and reported about 60
  decoded FPS. That includes streaming and is not physical-scanout validation.
- The stream initially swapped RGBA/BGRA channels; that was an added streaming
  bug, not a GS renderer defect, and was corrected in the private stream.

No private frames, recordings, game binaries, generated units or snapshots are
included as public evidence artifacts.

## Earlier rebased source tree {#this-clean-source-tree}

Started from upstream a02cdd56a8ab5077724da2b5ff8ca683024d7cf4 and selectively
rebased source/tests. The newer upstream interrupt-latch implementation was kept;
state version is bumped for the additional i.Link state. Experiment measurements
are not automatically measurements of this newly rebased code.

Publication guard, script syntax and synthetic patch tests passed. The rebased
software runtime compiled with Clang and both synthetic CTest regressions passed:
GT3 hardware behavior and SIF RAM/scratchpad descriptor reads. GCC configuration
exposed unsupported inherited Clang vector builtins; compiler requirements and CI
now explicitly select Clang, with an early diagnostic for unsupported compilers.
CI is configured for these source-only regressions. Fresh-clone native
boot/discovery, local GPU tests, browser/GT4 regression coverage and portable build
coverage must be established before a release. No release binaries are provided.

## Limits / follow-up recorded at the earlier checkpoints {#known-limits--follow-up}

These limits and suggested priorities belong to the snapshots above, not a
current subsystem inventory. See [execution status](restructuring.md) for present
bounded proof and [current authorities](../../reference/authorities.md) for
source ownership and absent product integration approval.

- Not complete game-source recovery; selected controls/steering source only at
  that stage, with newer-main integration still awaiting its own validation.
- Supported triple-profile fingerprint is specific to the tested USA revision.
- Overlay/replay issues and full game-mode coverage remain.
- i.Link initialization emulation does not implement network play.
- Native VU remains a detached worker; fully orderly joinable teardown is pending.
- Triple rendering, pacing and snapshot changes need broader upstream-style tests.
- SSE4.1 is optional, native x86-only, with no runtime dispatch.
- Physical scanout, hardware audio timing and all-adapter performance are unproven.

The recorded priority upstream candidates were SIF scratchpad reads and the
final-thread idle transition, each with a focused synthetic regression. Their
[contribution report](../provenance/upstream-contributions.md) retains the
historical publication/validation context, not network-reverified PR status.
