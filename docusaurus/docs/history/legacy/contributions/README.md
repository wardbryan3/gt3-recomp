:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../../workflow.md)
and [execution status](../../../development/restructuring.md) for maintained commands and actual gates.

:::

> Historical experiment record. Not current-main validation; referenced artifacts remain private and services may no longer be running.

# Source-only GT3 upstream contributions

Prepared from a **fresh network clone** of
https://github.com/snuri00/ps2-web-recomp.git at
`a02cdd56a8ab5077724da2b5ff8ca683024d7cf4`.
The original upstream history, MIT license and notices are preserved.
Nothing was cloned from the private experiment's Git object store/index.
**Combined draft:** https://github.com/snuri00/ps2-web-recomp/pull/11

Public fork (renamed by the user): https://github.com/wardbryan3/gt3-recomp

PRs #9 (SIF) and #10 (kernel) were closed as superseded; their branches remain.
The new `feature/gt3-bringup` branch has one audited commit (`a637c25`) and
16 source/doc files. It combines both fixes with limited i.Link initialization,
GT3 CORE detection, retained INTC-latch snapshot state, snapshot version 3 and
zero-length serialization guards. Five CTest groups pass in Release and
ASan/UBSan. Browser/title-level validation remains pending, hence draft status.
Only explicitly named contribution branches were pushed, never private files.

## Branches

| Worktree | Branch | Draft commit | Scope |
|---|---|---|---|
| `sif-scratchpad/` | `fix/sif-scratchpad-reads` | `4ad92c7` | EE descriptor-word reads use the memory resolver, including scratchpad |
| `kernel-exit-delete/` | `fix/kernel-exit-delete-idle` | `995a2d6` | Null/current-null/next scheduler case enters idle and unwinds |

Each original small-fix branch has exactly **one new commit and three changed source files**:
its runtime fix, a standalone synthetic C++ regression test, and a nine-line
opt-in native CMake test registration. They are independent branches based on
upstream/main, not a combined experiment port.

The primary clone is `ps2-web-recomp/`; these two worktrees share its clean
upstream-derived Git repository, not the experiment repository. Its `upstream`
fetch URL points to the original project, but the push URL is deliberately
`DISABLED` and `push.default=nothing`. `origin` points to the user's public
fork, https://github.com/wardbryan3/gt3-recomp.git.

## Validation

Both tests first failed against current upstream without the fixes, for the
intended reasons. Both then passed with their respective fixes:

- Clang 23.1.1, Release.
- Clang Debug, ASan + UBSan, leak detection and halt-on-UB enabled.
- Test-source `-Wall -Wextra -Werror` syntax checks.
- Default configurations confirmed not to enable the new tests.

SIF covers a two-descriptor scratchpad list with conflicting RAM descriptors,
five main-RAM address aliases and an untouched transfer boundary. Payload
sources remain ordinary main RAM; this is not complete scratchpad DMA support.

Kernel covers ordinary exit, deletion of the last thread, deletion with a
remaining dormant thread, idle/unwind/service behavior, and switching to a
ready worker with restored entry PC/argument.

GCC builds were attempted but blocked by pre-existing Clang-only vector
builtins in `vu_ops.hpp`. The same error was reproduced in unmodified upstream;
GCC support is not claimed or changed. Browser/title-level tests were not run
for these clean-upstream commits. No save-state format or game patch changes
are included.

Builds were serial, single-job and low-priority. The live game/stream and private
experiment's source, staging area, binaries and launchers were left alone.

## Files for review

- `PR-GT3.md`: combined public draft description; `gt3-bringup/docs/gt3.md`
  records scope, snapshot compatibility, reproduction and validation limits.
- `PR-1-SIF.md`, `PR-2-KERNEL.md`: superseded PR descriptions/reproduction.
- `patches/01-sif-scratchpad.patch`, `patches/02-kernel-exit-delete.patch`:
  source-only mail patches, bearing the user-approved author below.
- `audit.py`, `audit.json`: exact changed-file allowlists, source blob hashes,
  unchanged LICENSE, clean worktrees and one-commit/parent checks.
- `logs/`, `builds/`, `tmp/`: **private/local only**, outside the Git worktrees.

Added test content is synthetic, not extracted game data. No game files, game
translations, game-containing libraries/binaries, saves, captures, dumps,
decompilation/assembly reports, private configuration or unreviewed logs were
added to either branch. The publication audit concerns our additions; upstream
history itself is retained rather than rewritten.

## Publication

The user approved **Bryan Ward <wardbryan3@gmail.com>** as the public commit
identity. Both commits were amended to use it as author and committer; patches
were regenerated and the audit rerun. Source blob hashes are unchanged.

The user authenticated GitHub CLI as `wardbryan3`. The public upstream fork
was created under that account and subsequently renamed to `gt3-recomp` by the
user. The original two branches and combined replacement branch were pushed
explicitly using per-command GitHub CLI credentials (no global Git configuration
change). #11 is a draft; #9/#10 are closed as superseded. Published commit IDs
and changed-file allowlists were verified through GitHub against the local audit.
No blanket `push --all` or private experiment upload was performed.

The combined branch resolves the earlier overlapping CMake registrations in
one opt-in testing block. Its upstream INTC polling/delivery implementation is
preserved; only retained-latch serialization is new. Schema version 3 explicitly
rejects upstream version 2 snapshots before CPU/RAM mutation. No migration is
claimed, and memory-card files are unaffected. Private snapshot formats must
not be assumed interchangeable with this public branch.
