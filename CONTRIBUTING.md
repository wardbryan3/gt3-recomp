# Contributing to GT3 Recomp

This project's scope is GT3 recompilation, compatible runtime behavior, and
readable reconstructions. Preserve upstream attribution and third-party notices.

1. Keep changes focused; distinguish a generic PS2 runtime fix from a GT3-specific
   profile. Prefer synthetic reproductions that need no game file in CI.
2. Record the supported game revision, observed behavior, and confidence level.
   Analyst-assigned names are not recovered original symbols.
3. Keep original game code/assets and generated translations local. Never attach
   ISOs, ELF files, translated units, memory dumps or save states to PRs/issues.
4. Run `python3 scripts/audit_public.py` before a commit/push and review the actual
   file list/diff. The scanner is a guardrail, not a provenance certificate.
5. Enable the optional local push guard: `git config core.hooksPath .githooks`.
6. Document unchanged defaults and test coverage. Do not claim browser support,
   physical scanout, complete compatibility, or FPS beyond what was measured.
7. General fixes can go upstream as small PRs without changing this fork's GT3
   focus. Keep upstream as the `upstream` remote and your fork as `origin`.

No game files or game-containing builds should be published through releases,
Actions artifacts, Git LFS, branches or tags either. Read
`docs/gt3/PUBLICATION.md` before adding decompilation/reconstruction material.
