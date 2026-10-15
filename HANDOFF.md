# Current project handoff

## Authoritative home

Active local checkout: `~/code/personal/gt3-recomp`. Global `pi` uses saved private
credentials/settings/sessions under `~/.pi/agent`; REA/Ghidra/JDK are installed only
under ignored `local/rea` and registered via ignored project `.pi/mcp.json`.
Original inputs/oracles/evidence are available under ignored `local/game-input`
and `local/legacy`. Full private history is preserved under `~/archives/gt3`.
See [development setup](docs/gt3/DEVELOPMENT.md). No credentials or installations
are public. The old experiment location is retired, not a development root.

This checkout and `wardbryan3/gt3-recomp` main are the source of truth. Do not resume
new development in copied historical runtime repositories. Supporting upstream
history, license and notices remain intact.

## Checkpoint contents

- New mapping helpers, clean steering implementation/partial types and independent
  synthetic-wheel source, plus original-dependent fixture source, are preserved.
- `gt3_recovered` is a compile-checked source library with source-only consistency
  tests. It is **not linked into ps2run or installed into generated bodies** on main.
- Registry:134 selected records /129 canonical functions; historical lifecycle,
  differential and live statuses describe the preserved old runtime, explicitly
  labeled in `snapshot_context`. Four old steering seams remain bounded/frozen.
- Curated Docusaurus site, compiled offset assertions, metadata lookup and strict
  optional private hash verification work without publishing raw exports.
- `experiments/legacy/ledger.json` and source patches preserve unique dirty source
  from old checkouts. Optional benchmark/presentation/LAN harness source is kept
  there, **not a portable/current-main runtime installation**.
- Newer main keeps Clang requirements, hardware/SIF regressions, upstream interrupt
  behavior, snapshot3, and optional SSE4.1 defaults. No old runtime overwrite.

## Commands

```bash
just --list
just check
just test
just setup
just docs-build
just status
just lookup 0x001e4478
just verify-private /absolute/path/to/preserved/resolution/repo
```

A missing/changed private artifact fails the explicit verifier. Source-only checks
never claim to have independently repeated an original-game differential or live
race. Public docs include factual references/fingerprints, not raw analysis/game
files. Existing private docs service and protected legacy builds remain unchanged.

## Latest: Handbrake Recovery v1 — Frozen bounded validation-only, stop

Separately authorized clean recovery substitutes only001E4BB8–001E4C5F,
resume001E4C60, inside001E4478. New partial views identify command flags/+14
(signed digital nonzero or analog Q12) and car+13B4 only. Digital ramps use the
prior processed value as history; analog zero bypasses the shared floor, nonzero
uses the original signed/extrapolating EE arithmetic with no generic clamp or
mode4 response evaluator. Original command builders/notification, shift handling,
`update_control_coupling_candidate`, rear brakes and downstream vehicle processing
remain generated. No coupling-to-clutch rename or adjacent recovery.

Proof:2,228,224 exact generated-entry CPU/output/cost cases (all65,536 halfwords ×
digital/analog ×16 histories plus randomized calibration/state),20,000 stateful
transitions,16 mutation-free rejections;4,752 whole original wrapper/coupling/
brake/engine full-CPU+32MiB comparisons and38,016 rear-only formula assertions.
Native-v3:23 runs, six generated/clean/repeat triplets plus five default controls;
1,800 actual clean substitutions,zero fallback; exact CPU/state/budget, original
shift-interface entry/decision/return, brake/engine, full dumps,captures,steering
and repetition. Native input reached **analog zero/full only**; intermediate and
digital behavior are exact fixtures, not live/physical reachability claims.

Digital release when its original backward-branch preemption might run remains
mutation-free generated fallback. Signed-negative-budget analog paths are admitted
and independently tested. Two initial live attempts matched exactly but had six
protective fallbacks and are **not accepted clean proof**; disproved depth
hypothesis and all attempts remain under ignored `local/handbrake-v1/`.

The exact bounded implementation is **Frozen**, with source pins and every named
gate passing; this is not canonical installation or universal coverage.
Full available native regressions and unchanged inherited strict suites pass.
Authority:`decomp/gt3/handbrake.json`; report:`docs/site/docs/handbrake-v1.md`.
The root `justfile` and `provenance.json` are themselves pinned by immutable
virtual-pedal proof and remain byte-identical; no hash exemption/rehash was made.
Use `just --justfile handbrake.just check`, `docs-build`, and
`verify-handbrake "$PWD"` for additive source/docs/strict proof. Root `just test`
also runs new source/authority tests. Canonical ps2run stays generated-only;
build/runtime defaults OFF. No raw files or local configuration may be staged.

**Stop at bounded handbrake recovery.** No digital/intermediate-pressure live,
all-mode/car/long-session/browser or physical proof is claimed. No synthetic or
physical handbrake input, transmission recovery, clutch rename, wheel-brake/physics
expansion, FFB, canonical integration or next subsystem. Source/build context is
the evaluated overlay over the pinned commit, not a new full game recompile or
publication commit. No commit/push was requested.

## Prior: Synthetic / Virtual Pedal Controller v1 — bounded, stop

Separately authorized virtual input now feeds deterministic normalized throttle /
brake through the original command-builder return001E4D5C, original notification,
unchanged pedal processing and original downstream brake/engine routines. No
processed car state is written by the adapter. Temporary flags2/4 and Q12 halfwords
atcommand+8/+10 are restored before owner unwind001E4E68; all other command bytes
are preserved and checked. Both build/runtime gates default OFF; canonical host,
runtime/recompiler and Frozen pedal/closure/steering/wheel source are unchanged.

Protocol: finite [0,1] binary64 unsigned decimal; Q=nearest(value*4096), positive
half ties up. Atomic throttle:brake pairs can be constant or strictly increasing
uint64 guest-frame schedules. Invalid/range/overflow/duplicate/order inputs fail,
not clamp/sort. This is a virtual Q12 protocol, **not physical calibration**;
original floor/history/arbitration/response still determines processed outputs.

Independent oracle:12,291 cases /24,582 full CPU+32MiB comparisons, every Q12 code,
original notification/manual/brake/engine, actual Frozen substitutions, command-only
writes/restoration and eight mutation-free unsupported-context rejections. Source-
only tests cover8,193 exact quantizations and strict parsing/scheduling.
Native-v3 proof:12 cases with generated/clean/repeat plus default comparisons,
40 runs,3,599 injections per active path /10,797 total, every activation restored;
3,599 actual Frozen-clean replacements, zero fallback; exact CPU/dumps/captures/
steering/repetition. Zero/partial/full throttle/brake, transitions, simultaneous,
native steering, wheel compatibility and Time Trial alternate stack are included.
Fresh unchanged19-run pedal,28-run baseline and14-profile/4,199-substitution suites,
complete native/public regressions and strict inherited/new proof verifiers pass.

Authority: `decomp/gt3/virtual-pedals.json`;
[report](docs/site/docs/virtual-pedals.md). Strict command:
`just verify-virtual-pedals "$PWD"`. Private proof `local/virtual-pedals-v1/` retains
failed missing-capture-directory and incomplete group-timeout attempts separately.
All prior Frozen authorities and their pinned source remain byte-identical.

**Stop at this bounded virtual-input checkpoint.** No physical pedals/calibration,
USB/HID, clutch/handbrake/transmission/coupling/FFB/hardware recovery, general
DriverInput, AI/reset/step or canonical integration. No universal scene/car/thread
or long-session claim. This task does not reopen Pedal v1 or steering. Evaluation
used the source overlay over publication commitdf24e2c. The user subsequently
authorized source-only commit/push; publication does not change that evaluated
context. Private evidence, original inputs and local configuration remain excluded.

## Prior: Pedal v1 observed-context closure — re-frozen, stop

The separately authorized closure proves the **unchanged semantic body** at all
**4,199 actual entries /14 retained runs /five processing classes**, including
Time Trial, Free Run and B-1 at0049AF40. Isolated shadow execution compared complete
CPU/32MiB RAM/exact budget and bounded mutations, then restored original state.
All entries have one running owner: native EE thread10, stack493700–49B700.
Explicit original mode-entry probes resolve the16-byte difference:00181E90 uses a
96-byte frame versus00187A50's112, entering common001811B8 at49B350/49B340 from
identical outer SP49B3B0. Earlier BSS/global-buffer attribution is superseded.

The low-address exception is now a bounded structural manual-frame/return-chain
check, plus original wrapper fingerprint. No arithmetic/helper/consumer/steering
or runtime/recompiler/save-format semantics changed. It admits the actual command,
not a relocated surrogate. Complete CPU/RAM/budget equality at the join preserves
any retained alias; no whole-game no-retention theorem is claimed. Reentry was
not encountered in the observed original owner/hook lifetimes.

Fresh proof:131,072 exact join cases,24 mutation-free fallbacks,2,160 wrapper cases /
6,480 full comparisons;68 profile-path runs with4,199 guarded substitutions and
zero accepted fallback;19 original Pedal v1 live runs with2,100 substitutions;
28 fresh baseline runs with normal-boot v3 capture; complete native regressions,
public gates and strict inherited/closure/private verifiers. Canonical ps2run
remains generated-only, baseline hash unchanged; build/runtime gates default OFF.

Current authority: `decomp/gt3/pedal-closure.json`;
[closure report](docs/site/docs/pedal-closure.md). Strict verification:
`just verify-pedal-closure "$PWD"`. Private proof: `local/pedal-closure-v1/`.
Old Frozen/survey/audit authorities and failed runs are unchanged. Their original
CPP and audit analyzer are separately pinned historical artifacts; source version
resolution checks both the new source hash and old immutable expectation, never
silently skips a mismatch. Missing historical bytes fail private verification.

**All observed representative admission discovery is closed; stop.** This is not
all modes/cars/calibrations/threads/long sessions, browser, physical hardware,
clean-room certification or canonical installation. No unsupported observed class
remains; unmatched contexts retain original fallback, while unobserved matching
contexts acquire no live-proof guarantee. The guard is not a scene allowlist. No pedal API,
adjacent coupling/transmission/clutch/handbrake, steering rewrite, physical/FFB,
AI/reset/step or next recovery is authorized. Evaluation used the source overlay
over46a32c7; the subsequent source-only publication commit does not change that
validation context. Private evidence, original inputs and local configuration are
excluded from publication.

## Prior: read-only 0049AF40 admission audit — stopped

The separately authorized audit established that 0049AF40/0049AF50 are observed
positions of the **same activation-local 16-byte stack command layout**, owned by
001E4D38's64-byte frame, not two independently identified global BSS commands.
The earlier BSS attribution (including the Frozen comment) is qualified by the new
report, not rewritten in protected source/authorities. At Time Trial command49AF40,
49AF50 is a saved-s0 slot; at Single Race command49AF50,49AF40 is nested saved-ra.
They are not interchangeable pointers within one activation.

Reanalysis of4,199 retained original entries establishes command=entrySP+D0 and
original join v0/s1/SP/GP;4,185 have preceding wrapper-entry links. Original native
pad region costs63–72, compatibility costs123–132. The retained Time Trial original
versus unmodified-guard run now compares exactly across defined CPU/budget traces,
observations, steering, complete dump and3 captures:0 replacements/299 fallbacks.
This is **fallback equality**, not actual49AF40 clean-body equivalence.

**Safe admission remains unproven; stop without expansion.** Upstream stack-position
cause/backing allocation, complete indirect-hook lifetime/reentrancy and actual-
context clean ABI/cost/mutation proof remain open. No new runtime build/gameplay,
relocation, guard bypass or new instrumentation was performed. Protected CPP/HPP,
Frozen authority and stopped-survey authority hashes are unchanged.

Authority: `decomp/gt3/pedal-admission-49af40.json`;
[report](docs/site/docs/pedal-admission-49af40.md). Four new private artifacts/eight
static REA records under `local/pedal-admission-49af40-v1/`; REA project closed.
`just verify-pedal-admission "$PWD"` verifies inherited proof and recomputes this
read-only analysis. Final unchanged `just check`, `just test`, `just docs-build`,
strict admission/inherited proof and historical private verification passed, as did
all four protected source/authority hash checks. These are not a fresh full native
gameplay regression or expanded live validation.
No guard/source change, next recovery, physical/synthetic pedals or adjacent work
is authorized. Changes remain local/uncommitted over46a32c7 and the prior overlay.

## Prior: descriptor/profile characterization — stopped

Separately authorized original-only survey: 4,199 entries across 12 selected and
2 exploratory cases, one descriptor family / five processing configurations.
UI-reviewed cars include ALTEZZA, Alfa 156, MR-S, SLK230 Kompressor and New Beetle
2.0, plus a Time Trial preset whose exact model is unverified. Native pad and
existing synthetic steering compatibility observations remain separate.

Four original/unchanged-Frozen pairs pass 1,200 exact substitutions. **Time Trial
then stopped the cycle: 299 original entries, 0 replacements, 299 protective
fallbacks**, at command buffer **0049AF40**, outside the previously audited
0049AF50 context. Free Run/B-1 also observed 0049AF40 original-only; their clean
pairs were not attempted. Remaining pairs/full native regressions were not run
after stop. This is not an output mismatch or a Frozen regression/promotion.

Authority: `decomp/gt3/pedal-profiles.json`; [report](docs/site/docs/pedal-profiles.md).
Private evidence: `local/pedal-profiles-v1/`, 501 pinned files, failed attempt
retained. `just verify-pedal-profiles "$PWD"` verifies this stopped evidence plus
unchanged prior baseline/Frozen proof. Frozen CPP/HPP and `pedal-validation.json`
are byte-identical to before the survey. No runtime/default/algorithm changes.
Final public check/test/docs, strict stopped/baseline/Frozen/historical evidence
verification and Frozen source/authority hash checks passed. These are not a new
full native gameplay regression run. Source base remains46a32c7 plus the existing
Frozen overlay and new read-only survey tooling/docs; no commit/push was made.
**Stop.** Any 0049AF40 alias/admission audit or guard expansion needs separate
bounded authorization. No new gameplay runs or adjacent recovery are authorized.

## Pedal Recovery v1 — prior Frozen checkpoint

Baseline was committed and pushed as `46a32c7` before this continuation. New source
recovers only **001E48FC–001E4BA7**, resume **001E4BA8**, in an isolated validation
host. Canonical ps2run is still generated-only and byte-identical to baseline
(`b22b692a…10d4a`). No steering/synthetic algorithm, runtime, renderer, recompiler,
original input/card/snapshot or save-state-format change. CMake only adds the new
source to the existing compile-checked test library, not canonical linkage.

Authority: `decomp/gt3/pedal-validation.json`; operational report:
[Pedal v1](docs/site/docs/pedal-v1.md), [join contract](docs/site/docs/pedal-join-contract.md).
131,072 original and exact clean join cases compare complete CPU/scratch/FCR31,
mutation surface and dynamic budget (observed48–152). 2,160 wrapper/policy cases
produce6,480 full-CPU/32MiB comparisons through original coupling/brake/engine.
14 fallbacks leave CPU and all RAM unchanged. 19 v3 live runs/seven paired cases
pass:2,100 substitutions,zero accepted fallbacks,1,800 original descriptor calls,
4,200 original player brake/engine observations,exact CPU/pedal/steering traces,
captures and complete guest dumps. Existing2e-6 tolerance remains unchanged.
Fresh full native regressions, `just check`, `just test`, `just docs-build`, strict
historical/current/pedal verifiers and protected ISO/ELF/card checks pass. The exact
bounded validation-only implementation is **Frozen**, recorded in the new authority
rather than inferred from historical statuses.

Build and runtime gates both default OFF; canonical gameplay has no pedal gate.
`just verify-pedals "$PWD"` strictly verifies new private proof and the unchanged
baseline/v3 fixture. Private accepted trees under `local/pedal-v1-resume/` pin
623 build/129 live/7 regression files; failed attempts are retained. Do not update
hashes to hide failures. No raw game/evidence/tooling files may be staged.

**That Frozen evaluation passed and remains unchanged.** The later separately
authorized characterization above stopped at an unsupported admission context;
it did not reopen this implementation. Do not start any broader pedal API,
coupling, transmission, clutch, handbrake, physical devices, FFB or AI/reset/step.
Original 001E4180 remains `update_control_coupling_candidate`.

## Proven historical results (not new-main validation)

- Controls:25,600 normalization /57,344 mapped-action cases.
- Pad/wheel traces:15,360 pad frames;19,468 commands /7,560 driving frames.
- Synthetic adapter:8,193 quantizations /42 integrations and scoped guards.
- Clean:28,160 normalization /16,384 wheel /16,000 filter /20,000 envelope/tail
  original differentials, including ABI/PC/SP/budget.
- Fresh private live repetition:3,400 updates /13,600 original consumers;
  maximum reconstruction error5.96046448e-8, tolerance2e-6. All ten wheel cases,
  pad and disabled/trace-only paths matched their independent original context.
- Pedal discovery:22 original-only fixtures, not clean/live/physical-pedal proof.

## Pedal Recovery v1 — historical stopped audit

The blockers below describe that earlier cycle; the native-baseline restoration
section now records their resolution. Pedal implementation itself remains stopped.

The requested accelerator/brake cycle audited the candidate tail and stopped at
current-main prerequisites. `just test` cannot rebuild in the current environment:
`cmake` is missing from PATH; `ninja` is also absent. All 22 inspected retained
validation states are v2, and a current-runtime load probe rejected race-start as
expected. No validated v3 race fixture/compatibility path was found in the inspected
build/validation locations. No header spoofing or runtime hooks were installed.

Unchanged controls, pad/wheel traces, clean steering differential, synthetic-wheel
and 22 original-only pedal fixtures passed when compiled against available runtime
and retained generated archives. Those archives were not freshly rebuilt. Cached
hardware/SIF/source executables also passed. `just check`, strict private evidence
verification and `just docs-build` passed; fresh full/GPU regressions and live
validation remain blocked/not run. Do not promote these fixture results to new-main
live equivalence or Frozen pedal status.

See [the dedicated audit](docs/site/docs/pedal-recovery-v1.md) for the candidate
contract, evidence, exact counts and limitations. Private new logs are under ignored
`local/pedal-v1/`; old evidence/assets remain unchanged. Next dependency is the
working documented build toolchain and a safe identity-pinned v3 race fixture with
current-main original/clean steering and synthetic baseline revalidation. Do not
start adjacent transmission/clutch/handbrake recovery.

## Prior completed checkpoint: current-main native baseline restored

CMake 4.4.4 / Ninja 1.13.2 and their required dependencies were restored. Fresh
current-main tools regenerated EE/VU translations from the fingerprint-verified
original and retained discovery inputs; no old compiled library was reused.
Four independent fresh canonical builds are byte-identical. Complete applicable
native regressions pass, including GPU, controls/mapping, pad/wheel traces,
clean exact differentials, synthetic adapter, original-only pedals, hardware/SIF,
patch, metadata/publication and docs. `just check`, `just test`, `just docs-build`
and both strict evidence verifiers pass.

A **normal boot** produced a native v3 Super Speedway Arcade fixture at frame 4801:
`local/baseline-v3/accepted-live/capture/race-start-v3.state`, SHA-256
`da2661b490f977bd2d1b4d076d957bd8580aebf301f3c02e83b25964312c895a`.
Old v2 states were never imported or relabeled. The process-local external UTC
clock input is pinned; native thread padding can vary between independent raw
states, but every defined serialized byte, full guest dump and captures agree.
Canonical replay and uninterrupted continuation match exactly with future input
starting at 4802 (4801 was already sampled before saving).

Fresh isolated live validation: ten wheel scenarios, 3,400 clean mode-4 updates /
13,600 original consumers; maximum error 5.96046448e-8, unchanged tolerance 2e-6.
Clean pad ran 800 normalizations, 200 wheel builders, 200 filters/envelopes. Every
clean/generated semantic trace, capture and complete EE/IOP/SPU dump matched;
disabled/trace-only matched canonical. Captures were reviewed. No physical proof.

Authority: `decomp/gt3/current-validation.json`; strict command:
`just verify-current "$PWD"` (15 artifact hashes + 302 evidence-tree members).
Historical function states/hashes remain separate. Canonical ps2run still has no
recovered gates: integration exists only in the explicit validation-only wrapper.
No host/runtime/recompiler/CMake gameplay source or frozen control semantics changed.
See [the recipe and limitations](docs/site/docs/current-baseline.md). All new game
outputs remain ignored under `local/baseline-v3/`; failed attempts were retained.

That baseline task stopped without resuming pedals. The subsequent explicit user
request authorized only the bounded continuation recorded above; it did not
supersede protections or authorize old loaders/neighboring work.

The originally proposed tail001E48FC–001E4BA7, resume001E4BA8, is now recovered
and independently tested in a validation-only host. Historical stop reports remain
historical; the new authority controls the present bounded Frozen evaluation. No physical wheel/pedal/clutch/FFB, physics, AI/reset/step implementation
is authorized by this source checkpoint. See the site's queue and unknowns.
