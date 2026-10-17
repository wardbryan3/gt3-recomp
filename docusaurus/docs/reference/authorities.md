---
title: Current authorities, proof and approval
---

`project/gt3/` is the central machine-readable authority. There are several small
records, not one universal runtime registry or duplicated gameplay implementation.
Public checks use explicit schema/ownership/identity invariants without proprietary
inputs. The JSON definitions are in `project/gt3/authority-schema.json`.

| Record | Meaning |
|---|---|
| `products.json` | Two product roles/defaults and future shared headless policy |
| `implementations.json` | Unique authoritative source ownership, four classifications and exact scope limitations |
| `migration-map.json` | Mechanical logical-old to active-new paths; not source-version equivalence |
| `retirements.json` | Obsolete active front doors/recipes and their exact historical preservation context |
| `historical-context.json` | Exact baseline Git identity and explicitly pinned private source predecessors |
| `source-manifest.json` (optional; absent in this checkout) | When explicitly recorded, **candidate** source/dependency identity; never integration permission |
| `proofs.json` | Independent bounded current proof/report identities and their dependency closures |
| `approvals.json` | Separate explicit bounded product approval, referring to required independent proof layers |
| `progress.json` | Derived execution progress, **not** source policy, proof or approval |
| Other existing knowledge records | Preserved original-profile findings and exact version-qualified historical proof |

## Historical logical paths stay historical

The selected original manifest, symbols, partial types, provenance and bounded
controls/transmission records retain their exact original bytes and expectations.
Their old `host/`, `tests/`, `decomp/` or documentation paths identify the evaluated
historical source context; they are not current filesystem lookup instructions.
Current type compilation/status views resolve a logical path through the mechanical
map. Historical verifiers resolve its **version**, not its current moved bytes.

Read [historical knowledge schema](historical-knowledge-schema.md) for that original format.
Do not change old source hashes, constant tables, fixture hashes or expectations to
make a move pass. A registered private predecessor is required when Git never held
the evaluated source. Missing context fails explicitly.

## Current identity and invalidation

The source candidate covers current gameplay, inherited execution/tooling sources,
validation/test code, shared build commands and semantic authority records. Adding
or changing an uncertain/shared dependency makes active approval stale. Exact
build receipts additionally bind original ELF/ISO, entry/VU discovery, generator
binaries, generated file sets, explicit source lists, compiler settings, File API
closures, executables and linker maps.

Candidate/proof/approval/progress records are not recursively hashed into their own
source identity. Instead proof and approval each carry the exact observed dependency
closure; active approval requires matching independent proof layers and exact current
source. Progress cannot approve anything. New candidates use exclusive creation and
must not overwrite the previous evaluated context or silently renew old approval.

A `passed-bounded` status in `proofs.json` records the evaluated report and its
dependency closure. Reading that status or passing `just check` does **not**
re-execute private reports or prove their artifacts are present in this checkout.
An absent optional candidate manifest is not a missing proof silently treated as
passed: candidate identity, recorded proof and private verification are different
claims.

`just check` validates public declared consistency. `just verify-approval` explicitly
requires every private current report and its exact artifacts, including fresh ISO
builds, current source oracles, complete original-default product matrix and public
development gates. A public clone can develop/build without those private reports;
that does not mean private verification silently passed.

## Current approval does not promote recovery

The restructuring approval scope is only `original-default-products`. The schema and
checks reject recovery/enhancement promotion under this scope. Original-default runs
cannot substitute for extension ON proof, hardware proof, headless correctness or
whole-engine recovery. Future product promotion needs a separately approved bounded
contract, independent original evidence and applicable enabled/disabled/trace-only
integration—not a directory name or an old Frozen label.
