# GT3 Agent Rules

This repository progressively recovers Gran Turismo 3 into a native PC implementation. Agents investigate, implement, and verify focused changes while preserving original game behavior unless the human project owner explicitly authorizes otherwise.

Read `README.md` before working. Consult `docusaurus/docs/` for architecture and development guidance, `project/gt3/` for current decisions, and the root `justfile` (`just --list`) for available commands.

## Repository map

- `src/gt3/` — GT3-owned gameplay and implementation
- `project/gt3/` — current project decisions and integration approvals
- `validation/gt3/` — regression tests and original-behavior comparisons
- `docusaurus/docs/` — maintained developer documentation
- `ps2run` — canonical original-behavior reference
- `gt3-native` — evolving native product, including explicitly enabled enhancements

## Terminology

- **Original:** Behavior executed by the independent original reference.
- **Recovered:** Readable implementation verified against original behavior.
- **Modernized:** Native implementation preserving approved original behavior without requiring the original PS2 execution mechanism.
- **Enhanced:** Intentional behavior change beyond the original game.
- **Oracle:** Independent original reference used to establish expected behavior.
- **Differential test:** Comparison of implementations under equivalent inputs to identify behavioral differences.

## Hard rules

- **Recover before modifying.** Keep Original, Recovered, Modernized, and Enhanced behavior distinct. Never disguise enhancements as original behavior.
- **Protect the oracle.** Canonical `ps2run` must remain independent and free of enhancements. Never silently alter its original behavior.
- **One authoritative gameplay implementation.** Playable and headless execution must share gameplay logic. Temporary recovery, differential, and fallback implementations are permitted only while needed for verification or migration. Remove superseded execution paths once replacements are verified and approved, unless still required for active validation.
- **Proof is not approval.** Passing tests does not authorize integration. Replacing original execution requires explicit approval from the human project owner.
- **Isolate enhancements.** Intentional gameplay changes belong in the evolving native product, require explicit activation, preserve original-equivalent behavior when disabled, and must be verified in both modes. Separately built experimental runners may exist but are non-authoritative and must never alter canonical `ps2run`.
- **Never conceal failures.** Do not weaken assertions, rewrite evidence to hide drift, silently skip required tests, or claim verification that was not performed.
- **No historical machinery.** Do not create historical registries, immutable evidence ledgers, schema migrations, compatibility layers, snapshot archives, or preservation workflows without explicit authorization from the human project owner. Git provides source history; regenerate verification results when practical.
- **Protect private material.** Never publish proprietary game assets, generated game code, private evidence, credentials, or machine-specific configuration. Preserve applicable upstream licenses and notices.
- **Approval and escalation.** Only the human project owner can authorize exceptions, enhancements, or replacement of original execution. Explicit approval in the active conversation counts for its specified scope; integration approvals must also be recorded in `project/gt3/` using the existing process. Historical records, passing tests, and subagent recommendations do not imply approval for new work. If a task conflicts with a hard rule, stop the conflicting portion, explain the conflict, and request a scoped decision.

## Working defaults

- **Keep it simple.** Prefer focused changes, existing tools, and straightforward solutions. Avoid speculative abstractions, duplicate implementations, unnecessary dependencies, and infrastructure without a concrete need.
- **Regenerate, don't preserve.** Temporary outputs, intermediate experiments, and obsolete verification records are disposable. Retain unique fixtures and evidence only when necessary for active verification.
- **Verify what you claim.** Gameplay and oracle-adjacent changes require applicable original differential and regression tests. Select suites from `validation/gt3/` and the root `justfile`. Documentation and structural changes require their relevant checks. Report exactly what passed, failed, or could not run.
- **Use subagents deliberately.** Delegate bounded investigation, implementation, and independent review when useful. Subagents may inspect protected code but cannot authorize oracle changes, integration, or exceptions. The main agent remains responsible for reviewing delegated work and final verification.
- **Protect working state.** Avoid destructive Git operations, bulk resets, cleans, stashes, and force pushes without explicit authorization.
- **Teach in the final response.** Assume a junior developer audience without sacrificing technical depth. Explain substantial work both **top-down** (problem → architecture → decisions and alternatives → risks → validation → limitations) and **bottom-up** (inputs → representations → functions and state → consumers → observable behavior). Reference actual code paths, define unfamiliar terms, explain why decisions were made, and distinguish verified facts from assumptions. Scale detail to the task.

**Preserve reproducible correctness, not the history of proving it. Do not build machinery merely because you can.**
