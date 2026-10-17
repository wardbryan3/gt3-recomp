---
title: Current continuation — authoritative working checklist
---

**This is the one maintained onboarding/continuation checklist for ongoing tasks.**
Start a new checkout with the [environment](environment.md) and
[build/run guide](build-and-run.md). Historical handoffs, queues, “next” recommendations
and stop instructions apply only to their evaluated cycles; they are not new work orders.

## Before work

<span id="read-first"></span>

1. Read root `README.md` / `AGENTS.md`, [goals](../start-here/goals.md),
   [Architecture](../architecture/index.md), [publication](publication.md) and
   [authorization](../reference/authorization.md).
2. Confirm the owner's active scope. Documentation approval is not recovery,
   modernization, enhancement or gameplay integration approval.
3. Inspect working state; preserve unrelated edits. Use this repository, not a
   donor runtime tree, old experiment path or compatibility symlink.
4. Read [current status](../start-here/current-status.md) and the exact relevant
   authorities. `project/gt3/` separates source ownership, historical knowledge,
   bounded proof and explicit product approval. A candidate or progress label
   cannot approve anything.

## During work

<span id="current-source-boundary"></span>
<span id="preservation-and-stop-rules"></span>

Both current products use original generated gameplay. Neither links recovered or
enhanced gameplay. Keep the independent `ps2run` enhancement-free. Future playable
and headless consumers must share gameplay logic/settings, not fork training physics.

Preserve original expectations, exact historical hashes, failed attempts and private
inputs needed for active verification. Do not rehash mismatches, weaken assertions,
spoof snapshot versions or relabel fallback as substitution. Existing archives are
not disposable without separate deletion approval; no new preservation machinery
is needed. Public prose may reference private evidence but must not embed it.

## Before delivery

<span id="current-checkpoint"></span>
<span id="gates-before-a-checkpoint"></span>

Run `just check`, `just test` and `just docs-build`. Use [validation](validation.md)
to choose applicable original differential/integration checks for behavioral changes.
Explicit private verification must fail on missing/changed inputs, not silently skip.

Report exactly what ran, its source/input context, failures and exclusions. The
[restructuring report](../research/checkpoints/restructuring.md) records older evaluated
private proof; documentation/tooling edits do not renew it. Do not rewrite its
proof dependencies or issue owner acceptance on the basis of public checks.

Check links, generated view ownership and publication. No proprietary game material,
credentials, machine/session configuration, generated bodies or captures belongs in
a patch. Do not commit, push, install runtime hooks, change services or delete retained
source/archives without explicit permission. Stop at the requested scope; further
recovery, hardware/FFB, reset/step or product integration needs a separate decision.
