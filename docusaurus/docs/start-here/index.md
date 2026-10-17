---
title: Start Here
---

GT3 Recomp progressively recovers Gran Turismo 3 into readable, verified native
code. **Recover original behavior first; modernize or enhance only with separate
approval.** This is experimental recovery work, not a complete PC port.

## What runs today?

Both `ps2run` and `gt3-native` currently use original generated EE/VU execution and
the inherited PS2 runtime. Neither links recovered or enhanced gameplay libraries.
A native executable is not yet PS2-independent GT3. Physical simulator support,
correct headless training and complete native execution remain the
[three milestones](goals.md), not claims inferred from unit tests.

Bring a legally obtained supported ISO to build a game. Public source development
and the documentation need no game files. No ISO, original tables, generated game
translations, saves, captures or game-containing binaries are distributed.

## Choose a path

| Your goal | Begin here |
|---|---|
| Make a first public-source contribution | [Quick start](quick-start.md), then the [Developer Guide](../developer-guide/index.md) |
| Build and run your own game | [Environment](../developer-guide/environment.md) and [build/discovery](../developer-guide/build-and-run.md) |
| Learn recovery from a real example | [MT selector walkthrough](../developer-guide/worked-example-mt-selector/index.md) |
| Understand the product and source boundaries | [Architecture](../architecture/index.md) |
| Look up commands, fields or authority records | [Reference](../reference/index.md) |
| Examine original findings and evaluated experiments | [Research & Evidence](../research/index.md) |
| Continue an existing task | [Authoritative current continuation](../developer-guide/continuation.md) |

Read the [terminology](terminology.md) before interpreting “Recovered,” “Frozen,”
or “validated.” Use [current status](current-status.md), not old experiment counts,
to understand integration and approval. Historical reports preserve their evaluated
contexts; they do not authorize a new recovery or install a feature.
