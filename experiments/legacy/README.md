# Preserved source experiments — not additional active repositories

The project root is authoritative. This directory preserves authored source and
restoration patches from independently tested old experiments so their progress is
not stranded in dirty checkouts. It contains no game input, translated game bodies,
installed dependencies, snapshots, credentials, raw decompiler exports or captures.

`ledger.json` records each donor's exact base and patch SHA-256. Patches include
tracked staged/unstaged source plus untracked authored source. They are restoration
records against their stated bases, **not patches to apply wholesale to main**.
Review feature deltas and newer upstream equivalents before integration.

- `resolution-repo/source.patch`: controls/steering, opt-in CLI/build/probe source,
  fixtures and the old runtime foundation in which exact comparisons passed.
- Performance/presentation/LAN patches: distinct window/render/probe/input changes.
- Initial/validation/repro and contribution-baseline patches: older bring-up/test
  variants; many fixes already exist in newer main.
- Non-repository harness scripts and reviewed historical reports are retained in
  performance/presentation/lan-play/resolution/contributions subdirectories.

These scripts have legacy sibling-directory and pinned-archive dependencies.
They are **not runnable current-main profiles**. They do not start automatically.
Firewall/service/input changes require separate explicit consent. A historical
README saying "running" does not establish current service state. Rejected
optimizations remain rejected, not current runtime code.

The current main directly contains readable controls, clean steering and synthetic
adapter source plus tests, inventories and docs. The newer foundation remains
unchanged; clean/synthetic runtime installation needs fresh newer-main original-
oracle/live validation. Private old executables/artifacts remain untouched outside
this repository. See HANDOFF.md and docs/site/docs/testing.md.
