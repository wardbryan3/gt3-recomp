# Testing: current source versus historical original proof

## Current main, source-only

`just check`: public metadata,34 compiled layout assertions,11 metadata positive/negative tests, publication guard. `just test`: newer-main hardware and SIF regressions, synthetic triple patch tests, compile/link of recovered source,6,400 positive-domain consistency cases and8,193 quantizations plus parser/release guards. Synthetic consistency is NOT a new independent original-game differential.

`just setup && just docs-build`: locked dependencies, ten Mermaid diagrams and strict links. `just verify-private EXPLICIT_ROOT`: original ELF identity,11 retained artifact hashes and66 evidence IDs. Missing/changed artifacts fail.

No runtime hook/CLI is installed on current main. Newer snapshot3 cannot load the preserved v2 race snapshot by a version-byte edit. Full-game equivalence must be established separately in the new integration context.

## Historical experiment detail

> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Validation and exact results
---

## Unchanged suite rerun

Command: `tests/run_gt3_clean_steering.sh`; log **`build/project-init/regressions.log`**. No runtime/test assertion changes.

| Test | Result |
|---|---|
| Clean normalization exact differential | PASS,28,160 cases |
| Clean wheel builder exact differential | PASS,16,384 cases |
| Clean stick filter exact differential | PASS,16,000 cases |
| Clean envelope / full-original tail exact differential | PASS,20,000 cases |
| Original control normalization | PASS,25,600 cases |
| Mapped actions / lookup chain / output guards | PASS,57,344 cases |
| Original pad trace / steering / wheel angles | PASS,15,360 frames |
| Wheel override / native getters / pedals | PASS,19,468 commands (also clean-enabled wheel fixture run) |
| Wheel mode4 / shared float / angles | PASS,7,560 frames (also clean-enabled run) |
| Synthetic adapter | PASS,8,193 quantizations,42 native integrations and guards/parser/schedule |
| Anisotropic GPU samples/state conversion | PASS |
| GT3 hardware/runtime regressions | PASS |

Relevant byte mutations, ABI return PC/SP, callee-saved state, exact EE dynamic instruction budget and existing **2e-6** floating tolerance remain unchanged. Counts repeated in different configurations are not summed into new unique-case claims.

## Fresh full-game baseline verification

Command:

```bash
scripts/validate_gt3_clean_steering.py \
 --snapshot $GT3_LEGACY_ROOT/validation/race-start.state \
 --out "$PWD/build/project-init/live"
```

Retained **`build/project-init/live/summary.json`**, log `build/project-init/live.log`, per-case traces/captures/dumps and separate `oracle_*` repetitions. **3,400** mode4 updates / **13,600** original wheel consumers; maximum error **5.96046448e-8**. All ten wheel cases match preserved generated executable traces, captures, final car and full EE/IOP/SPU dumps byte-for-byte. Clean pad path matches original; gates-off and read-only trace match baseline. No new physical/window/audio/pacing claim. Earlier authoritative evidence remains unchanged under both experiments' `live-final` directories.

## New discovery / tooling tests

- Original-only pedal propagation: **22** fixtures in `build/project-init/pedal-fixture.jsonl`, `.log`; not a replacement differential or live physical-pedal claim.
- Metadata/provenance check, generated partial type offset assertions and deliberate metadata-error unit tests.
- Root task parsing/bootstrap/status/lookup, isolated generated and clean native builds, production Docusaurus build with Mermaid and strict broken links.
- Shell/Python syntax, `git diff --check`, pre-existing source/evidence preservation audit and known-good artifact hashes.

Fresh isolated **clean executable matches the frozen validated SHA exactly**; the preserved baseline/default launcher, ISO/ELFs, snapshot, synthetic/clean executables and prior evidence remain intact. Initialization result logs are under `build/project-init`; the morning report records final command outcomes and limitations.

## Reproduction discipline

`just test` uses existing oracle/gated libraries, preserving generated bodies. `just test-discovery` writes only a fresh discovery executable and prints original fixture output; it does not overwrite retained initialization fixture evidence. `just validate NEW_ABSOLUTE_DIRECTORY` validates the identity-checked frozen executable with disposable cards and exclusive outputs. New APIs/changes require new differential/live evidence rather than a rerun of an unrelated fixture.
