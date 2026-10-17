---
title: Repository layout and source ownership
---

| Path | Owner / purpose |
|---|---|
| `src/gt3/gameplay/controls/` | Recovered control bodies and separate input adapters |
| `src/gt3/gameplay/transmission/` | Selector/helper/admission recovery and explicitly partial state models |
| `src/gt3/gameplay/transmission/virtual/` | Virtual transmission domain policy, not installed |
| `src/gt3/bindings/ps2/virtual-transmission/` | Concrete PS2 extension binding; gates preserved |
| `src/gt3/gameplay/*/tests/` | Domain-local source/protocol contracts |
| `validation/gt3/{differential,integration,live}/` | Independent original fixtures, authority/reducer negatives, live support |
| `project/gt3/` | Products, ownership, knowledge, exact historical contexts, proof/approval and source identity |
| `cmake/` | Explicit current source ownership and optional private original fixtures |
| `scripts/project/` | Coordinated current build/check/knowledge/evidence commands |
| `recomp/`, `runtime/`, `host/` | Inherited compiler, execution runtime and generic host/platform internals |
| `docusaurus/` | Single installed documentation site |
| `docusaurus/docs/` | All maintained project prose and generated knowledge views |
| `local/`, `games/`, `generated/`, `build/` | Ignored private inputs, fixtures, generation, outputs and evidence |

There are no parallel active gameplay trees or maintained runtime checkouts.
Historical Git revisions and immutable private overlays are independent evidence,
not competing active source. The complete mechanical path map is
`project/gt3/migration-map.json`; retired front doors/recipes are recorded in
`project/gt3/retirements.json`, not silently kept working against stale active paths.

The concise root `README.md` and `AGENTS.md`, licenses/notices and necessary tooling
instructions are exceptions to documentation consolidation. Local machine/session,
installed tooling and legal game inputs remain ignored. Do not publish them through
static site copying or add a second documentation tree.
