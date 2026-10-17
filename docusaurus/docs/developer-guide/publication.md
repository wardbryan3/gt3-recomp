# Public source / local game boundary

This is one GT3 project, not two competing implementations. Its source is public;
user-provided game material and translations are local build inputs/outputs.

## Included

Upstream framework/runtime source with its history/notices; newly written runtime
fixes; extraction/recompilation tools; fingerprint-gated patch recipes; tests
constructed from synthetic data; reviewed factual findings and original readable
reference implementations. `src/gt3/gameplay/controls/gt3_controls.hpp` is a newly written reference,
not copied decompiler output or a replacement currently enabled in gameplay.
Its differential test uses a user's translated game library locally.

Historical patch recipe address leads retain attribution to Silentwarior112's
PCSX2 patch work. The exact recipe is preserved as `scripts/gt3_triple.py` at Git
revision `aee79fba37937e4dc99dac4263589d005112c504`, not a second active builder.
Instruction-sized patch constants are metadata,
not a distributed executable or a whole recovered function. Preserve attribution;
re-review provenance if extending this recipe or copying external implementations.

## Excluded

ISO/disc contents, original/patched ELF/IRX files, original data tables, VU program
binaries, generated game C++/WebAssembly, game libraries and linked executables,
saves, memory snapshots, assembly/decompiler dumps, screenshots/audio from our
experiments, access tokens and machine/session configuration. Upstream historical
demo media remains in inherited Git history, but is removed from this fork's
current public tree. No new game media is published in maintained source files.

The ignored local directories are not separate public repositories. Builds can
use them directly; `.gitignore` prevents normal accidental staging. Forced adds,
renamed files and encoded blobs still require human review. The publication audit
checks common artifact paths/extensions/magic and credential signatures, not every
possible encoding or copyright issue. It scans the current tree, **not all history**.

## Decompilation/reconstruction policy

Recovered facts and original implementations may be useful project source, but
technical recovery does not automatically grant distribution rights. Do not paste
Ghidra output or translated function bodies into public files by default. Record
provenance, method, scope, test evidence and uncertainty; review proposed recovered
code before publication. The MIT license for the framework does not license game
code or data. This policy is not legal advice or a claim of clean-room provenance.

## Initial preparation

A fresh clone of upstream was used; only selected source/test changes were applied.
The experiment directory and its Git index were not copied. Upstream's existing
interrupt-latch fix was retained during rebase rather than replaced by the older
local equivalent. This fork uses snapshot version 3 because it adds i.Link PHY
state; upstream/private version-2 snapshots are deliberately rejected. Existing
private builds, ISO and saves were not modified.

The source-only fork has no game-containing release artifacts or dependency on a
published private archive. Game boot/discovery still requires user-owned files,
local exploration and validation for that revision.
