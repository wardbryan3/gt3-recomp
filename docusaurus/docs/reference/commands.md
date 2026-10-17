---
title: Command reference
---

Run `just --list` in the repository root for the executable source of truth.
The [build guide](../developer-guide/build-and-run.md) supplies the ordered setup.

| Command | Scope and limits |
|---|---|
| `just setup` | Install locked documentation dependencies. |
| `just check` | Current consistency/layout checks, historical metadata/negative tests, publication audit and whitespace. No game execution. |
| `just test` | Build/run public software-runtime source contracts plus historical reducers and Python tests. No ISO or live fixture needed. |
| `just status` | Current product state versus selected historical findings. |
| `just lookup ADDRESS` / `just evidence ADDRESS` | Public knowledge lookup / historical manifest records, not original assembly or pseudocode. |
| `just docs-generate` | Regenerate four views in `reference/generated/` and public knowledge JSON. |
| `just docs-build` | Generate views, parse Mermaid diagrams, build strict links and old-route redirects. |
| `just docs-dev` | Generate views and run the development server. |
| `just audit` | Tracked/untracked publication scan using existing policy. |
| `just build-game ISO NEW_NAME` | Private original extraction, bounded discovery, identity-checked assembly and two-product build; new output name required. |

## Explicit historical verification

`just verify-historical PROFILE ROOT` reads registered exact predecessor contexts.
Named aliases include `verify-private`, `verify-current`, `verify-pedals`,
`verify-pedal-profiles`, `verify-pedal-admission`, `verify-pedal-closure`,
`verify-virtual-pedals`, `verify-handbrake`, `verify-virtual-handbrake`,
`verify-transmission`, `verify-transmission-speed`, `verify-transmission-state`
and `verify-extensions`, each taking an explicit private root.

Despite its inherited name, **`verify-current` selects the historical `baseline`
profile**, not present-product acceptance. Protected source/data hashes and
expected results must match; missing roots or artifacts are failures. Do not point
these commands at current source as an alias for its predecessor.

## Current original-only checkpoint

- `just qualify-products RECEIPT NEW_NAME`: build a retained-row catalogue and run
  the current two-product original-default matrix from its explicit fresh receipt.
- `just original-fixtures RECEIPT NEW_NAME`: run relocated source against independently
  generated original fixtures; `just verify-source-fixtures REPORT` verifies its report.
- `just verify-checkpoint REPORT`: verify an existing current matrix report and closure.
- `just verify-approval`: evaluate proof/approval state; it cannot create owner approval.

These require the private dependencies described in [validation](../developer-guide/validation.md).
No new private verification is implied by a documentation build or a historical result.
