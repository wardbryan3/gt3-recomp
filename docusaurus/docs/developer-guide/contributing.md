---
title: Contributing and review boundaries
---

Read the root README/AGENTS, [goals](../start-here/goals.md), [architecture](../architecture/index.md),
[workflow](workflow.md) and [publication policy](publication.md). The root `just`
workflow is authoritative; do not revive old recipe variants or develop in a donor
runtime tree. Preserve upstream Git history, license/notices and reviewed fixes.
Generic infrastructure fixes should be proposed upstream separately where useful.

Work only within explicit approved scope. Queue entries, source classification and
old Frozen status do not authorize a new recovery, modernization or integration.
Recover original behavior first. A product promotion requires its own bounded
contract, independent original oracle and applicable ABI/mutation/numerical/dynamic
cost and enabled/disabled/trace-only integration evidence. Interior gates and partial
models must not be represented as whole-function recovery. Build/runtime gates
used in isolated validation are not permission to install code in either product.
Use the [methodology evidence ladder](recovery-method.md) to distinguish static
findings, original-only fixtures, differentials, live integration and hardware
proof before seeking separate owner approval.

One gameplay owner serves future playable/headless hosts; do not create a training
physics fork or parallel actively maintained implementation. Use partial types,
explicit padding/offset assertions, original EE FP and integer semantics, and the
existing `2e-6` tolerance. Preserve original downstream physics unless separately
authorized. Keep uncertain names neutral/candidate-qualified.

Run `just check`, `just test` and `just docs-build` before a checkpoint. Passing
public checks is not private proof or permission to install code. Exact private
verification must fail on missing/changed required inputs. Preserve old expectations,
failed attempts and evaluated contexts; changed dependencies invalidate approval.
Do not bulk add/reset/stash/clean, rewrite hashes or weaken assertions to hide failure.

Public onboarding needs only the dependencies in [build and discovery](build-and-run.md).
The tracked REA launcher supports an optional private installation; it does not make
REA, agent configuration or analysis databases public build/test prerequisites.

No ISO/ELF, generated translations, original tables, states/cards, raw exports,
captures, credentials or machine/session configuration belongs in a public patch.
Publication checks supplement human provenance/legal review; they do not certify
clean-room derivation or distribution rights. Do not commit, push, delete retained
archives or install hooks without explicit authorization.
