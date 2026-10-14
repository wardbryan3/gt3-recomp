> **Public checkpoint context:** historical lifecycle/runtime/live fields describe the preserved private experiment. All inventories carry `snapshot_context`; canonical current main compiles recovery source but does not install it. Fresh isolated native validation is separately recorded in `current-validation.json`. Public `check` verifies schema/source/type relationships only. `verify-private EXPLICIT_ROOT` separately and strictly verifies all retained original hashes and IDs. Raw exports are never documentation download assets.

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

## Generated views

`just docs-generate` regenerates status/symbol/type pages and mirrors five baseline Markdown narratives into the site, touching no original evidence. `just lookup QUERY` returns full maintained records. `just evidence ADDRESS` prints retained canonical batch pseudocode with citation, not fresh decompiler output. `just check` checks these authorities and compiles asserted layouts.
