> **Public checkpoint context:** historical lifecycle/runtime/live fields default to the preserved private experiment; the new pedal record explicitly overrides this with its current-main validation-only context. All inventories carry `snapshot_context`; canonical current main compiles recovery source but does not install it. Fresh isolated native validation is separately recorded in `current-validation.json`. Public `check` verifies schema/source/type relationships only. `verify-private EXPLICIT_ROOT` separately and strictly verifies all retained original hashes and IDs. Raw exports are never documentation download assets.

# Knowledge schema v1 and authority rules

These JSON files are the maintained knowledge authorities for the original GT3 USA v1.10 profile. `tools/project.py check` implements consistency/hash validation without an external schema package; `tools/check-types.sh` generates and compiles C++ size/offset assertions. The checker is intentionally not a semantic proof engine.

## manifest.json

Top-level `schema_version`, `profile`, `original_elf_sha256`, ordered `lifecycle_order`, `notes`, `functions`.
Each bounded implementation/identified original entry has:

- Unique `id`; normalized lowercase eight-digit `address` is ORIGINAL guest entry, not a host pointer. Multiple implementations/standalone variants may share entry.
- `name`, `component`, `lifecycle`, qualified `confidence`, retained `evidence` refs.
- `generated_oracle` locations and nullable `recovered_source`/`recovered_header`.
- Independent `differential {status,tests,evidence}`, `runtime {status,gate,default}`, `live {status,evidence}`. Original-only fixture is not differential-passing. Standalone helper is not installed runtime replacement.
- `dependencies`: candidate decompiler callee addresses, explicitly not complete verified edges; empty allowed.
- `uncertainties`, actionable `next_action`.
- Installed `frozen` replacements additionally require inclusive `boundary [start,end]`, `gate_address`, optional `resume_address`. An interior boundary must resume at `end+1`, and frozen status requires passing differential, opt-in integration/default generated and bounded live validation.

Lifecycle values: `unknown`, `identified`, `traced`, `recovered`, `differential-passing`, `opt-in-integrated`, `live-validated`, `frozen`. Promotion is manual and evidence-gated. The selected inventory is not an overall recovery-percentage denominator.

## symbols.json

`functions`: canonical provider address/native name, semantic name/confidence, evidence refs, requested selectors, candidate calls; replacement metadata where applicable. Selectors resolving inside another body are retained but NOT automatically independent symbols or aliases. Data entries carry address/name/confidence/evidence. All guest labels are profile-specific. Names containing `candidate` or `unknown` are deliberately uncertain.

## types.json

Guest endianness, pointer width and EE float representation are explicit. `layouts` refer to actual partial C++ header types, their sizes and fields with offset/storage/meaning/confidence/evidence. Assertions are generated against those exact source fields. `observations.fields` are separately untyped car-like offsets; they do not extend C++ structures, authorize writes or prove physical units. Opaque padding must never be bulk-written by a bridge. Preserve neutral unknown field names.

## provenance.json

Artifact IDs map to retained file path, SHA-256, evidence kind and limitations. Evidence-ID records map REA IDs to the containing hashed export and are verified against its `records`. Kinds distinguish static REA, live and generated-fixture records; prior clean summary includes mixed evidence and its own explanatory ledger. IDs beginning `artifact:` reference complete artifacts rather than individual REA predicates.

Evidence hashes are immutable expectations. A mismatch requires investigation, not blind rehashing. Add new observations under new artifact paths/IDs and qualify contradictions. The manifest may evolve after explicit new work; evidence itself must not be rewritten. New machine-readable status does not supersede limitations in retained source evidence.

## current-validation.json

Separate authority for fresh current-main baseline attempts/results. Historical
function lifecycle and evidence hashes are not overwritten by this record. It
pins the source commit, validation-only runtime scope, build/regression/live gates,
native-v3 fixture status and private artifact paths/hashes. A passing gate requires
retained artifacts. Artifacts of kind `file-manifest` pin a private list of nested
paths/hashes; explicit verification checks every member, not just the summary.
A passing fixture also requires a native `PS2STATE` v3 header at private verification. Public consistency checks do not read game files.

`just verify-current EXPLICIT_REPOSITORY_ROOT` strictly verifies every listed new
artifact and fails on missing/changed files. This is separate from historical
`verify-private EXPLICIT_DONOR_ROOT`; neither silently skips missing proof. The
isolated validation harness is not a canonical ps2run runtime installation. Never
promote a current live status based solely on historical evidence or a v2 header
rewrite. Generated current-status pages and JSON mirrors derive from this file.

## pedal-validation.json

Immutable authority for the original Frozen version; current structural admission
is separately versioned in `pedal-closure.json` below. Separate authority for the
explicitly resumed **001E48FC–001E4BA7** pedal region,
resume **001E4BA8**, over committed baseline46a32c7. It does not rewrite baseline
or historical evidence/status. The associated manifest record carries explicit
`pedal_validation`, `validation_context` and runtime `scope: validation-only`;
top-level historical snapshot context is a default, not this new record's context.
The parent native symbol remains001E4478; the interior seam is not a new function.

Both build/runtime defaults must be false. Passing/Frozen requires independently
pinned original/clean complete-CPU and exact-budget proof, wrapper/consumer full
RAM differentials, regressions, native-v3 fixture and bounded live equivalence.
Public consistency checks validate metadata/source hashes, not game semantics.
Frozen here means the exact bounded **validation-only** source is frozen, never
canonical installation or a hardware/physical-device guarantee. Published source
hashes reject silent alteration of the evaluated implementation/header.

`just verify-pedals EXPLICIT_REPOSITORY_ROOT` strictly verifies baseline proof,
new artifact and complete build/live/regression manifests, native-v3 header and
unchanged baseline fixture/ISO/ELF identities. Missing/changed files fail; no silent
skip or rehash. New provenance points at this registry; eleven historical artifact
hashes/66 REA IDs still belong to the historical verifier unchanged. All raw files
stay private. Generated pedal validation page/knowledge mirror derive from this
new authority, and typed partial pedal layouts have generated offset assertions.

## pedal-profiles.json

Separate schema-version1 authority for the finite, original-only descriptor/profile
reachability survey and its **stopped-unsupported-context** outcome. Provenance
links this registry separately; it does not update any function lifecycle or the
Frozen pedal authority. Exact descriptor/rate fingerprints, processing selectors,
command contexts and native-versus-existing-synthetic reachability stay distinct.
Only factual fingerprints/metadata are public; raw descriptor words/captures and
the five static REA records stay in pinned ignored artifacts.

The record preserves four passing pairs/1,200 substitutions and the Time Trial
stop:299 original entries,0 replacements,299 protective fallbacks. Remaining
pairs/full native regressions are explicitly not run after stop. Public checks
validate these distinctions, source hashes and unchanged Frozen authority hash.
`just verify-pedal-profiles EXPLICIT_REPOSITORY_ROOT` additionally verifies prior
baseline/Frozen proof, seven new artifacts/501 evidence-tree members, recomputes
the observed inventory, and checks the stopped log and retained static records.
Missing/changed evidence fails, with no skip/rehash or broader equivalence claim.
The executed validator is separately preserved; later reducer-only reporting
additions do not masquerade as an independently repeated gameplay run.

## pedal-admission-49af40.json

Separately linked read-only audit authority, status `stopped-unproven-admission`.
It pins the unchanged Frozen and stopped-survey authorities/source, the analyzer,
four new private artifacts and eight retained static REA records. Recomputed
retained trace analysis establishes activation-local stack ownership/layout and
bounded original/fallback equality, not actual49AF40 clean-body execution.
`safe_admission_established` and `guard_expansion_authorized` must remain false.
Public checks/tests require no game artifacts; explicit
`just verify-pedal-admission EXPLICIT_REPOSITORY_ROOT` verifies all inherited proof,
new files and recomputed analysis. No lifecycle or prior evidence hash is changed.
The earlier BSS command-object attribution is qualified by this new audit, not by
rewriting the Frozen source comment or prior immutable authorities.

## pedal-closure.json

Separate current admission authority: `pedal-v1-observed-context-closure`, same
bounded region/resume and semantic prefix as original Frozen. It pins current
source/tool hashes, explicit historical source artifacts, actual-entry shadow and
actual guarded live summaries, original-frame diagnostics, static evidence and
complete private proof manifests. Lifecycle may be `validating` or `frozen`;
Frozen requires every named gate passing. Build/runtime defaults must remain false,
canonical generated-only, semantics unchanged, five observed processing classes,
14 cases,4,199 actual-entry comparisons and4,199 substitutions with zero fallback.
Structural-frame admission cannot become an absolute command allowlist.

Public `check` requires the exact current source hashes and the original immutable
historical expectations. A changed current file is accepted only as an explicitly
pinned new version whose predecessor is registered as a private artifact; no hash
mismatch is silently ignored. `verify-pedals` additionally verifies these closure
artifacts, including the actual original CPP/analyzer bytes. The old Frozen,
stopped-survey and stopped-audit registries remain unchanged and recompute their
original outcomes. `just verify-pedal-closure EXPLICIT_REPOSITORY_ROOT` verifies
all inherited evidence and independently rechecks every retained shadow/live
trace, count, dump, capture, input/binary identity and semantic-prefix equality.
Missing evidence, fallback-as-proof or source drift fails closed. Generated
`registry/pedal-closure` and knowledge JSON expose facts, never raw game material.

The finite observed-context closure is not universal coverage, physical-device or
canonical integration proof, and does not authorize another recovery.

## virtual-pedals.json

Separate `synthetic-virtual-pedals-v1` experimental authority, not a recovered
function or Frozen lifecycle change. Source checks and private verification live
in `scripts/project/virtual_pedals.py`; the Frozen project checker is unchanged.
It pins new source/tool hashes, unchanged protected Frozen/runtime/recompiler
hashes, exact virtual Q12 protocol, command-only boundary/restore fields, original
static records and complete private build/oracle/live/regression manifests.

Status `validated-bounded` requires every named gate passing. Build/runtime defaults
must remain false, canonical installation and processed-car writes false, and
physical calibration false. Public checks/reducer negatives require no game input.
The explicit `just verify-virtual-pedals EXPLICIT_REPOSITORY_ROOT` verifies every
private artifact/member, native-v3 input and executable identities, full CPU/RAM/
capture/steering/repetition parity, independent frame schedules, command restoration
and original downstream observations, then invokes unchanged inherited verifiers.
Missing/changed proof fails, never silently skips. Historical failures/incomplete
runs remain retained; no earlier authority/hash is rewritten. Generated views and
knowledge mirror publish facts only, not raw game artifacts.

## Generated views

`just docs-generate` regenerates status/symbol/type pages and mirrors five baseline Markdown narratives into the site, touching no original evidence. `just lookup QUERY` returns full maintained records. `just evidence ADDRESS` prints retained canonical batch pseudocode with citation, not fresh decompiler output. `just check` checks these authorities and compiles asserted layouts.
