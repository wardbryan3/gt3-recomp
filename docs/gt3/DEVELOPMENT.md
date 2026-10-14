# Development environment and private storage

The active checkout is `~/code/personal/gt3-recomp`. Start the globally installed
Pi normally:

```bash
cd ~/code/personal/gt3-recomp
pi
```

Pi uses standard private `~/.pi/agent` storage for saved credentials, preferences
and sessions. Project REA configuration/skills are under ignored `.pi/`; REA is
not globally installed. Trust only reviewed project resources. Session history
must never be published without separate review.

## Local REA layout

The ignored `local/rea/` directory contains the private REA6.4.0 installation,
its Ghidra12.1.4/JDK dependencies, home/cache and integration history. The reviewed
`scripts/project/rea-local.sh mcp` launcher resolves everything relative to this
checkout and uses global Node. A private `.pi/mcp.json` registers it only for this
repository, with the Ghidra r5900 little-endian default profile and deferred tools.

A fresh public clone does not contain these installations or credentials. Obtain
required software separately under its license; do not commit downloaded packages,
engine databases, raw analysis or personal MCP configuration. The launcher itself
contains no secret or user-specific absolute paths.

## Private evidence and original inputs

Migrated game input is under ignored `local/game-input/`; preserved original
oracles/evidence and v2 snapshots are under `local/legacy/`. Verify explicitly:

```bash
just verify-private "$PWD/local/legacy/resolution-repo"
```

Current-main source checks/docs remain independent of those files. Historical
exact/live proof is not a newly installed clean runtime. Do not spoof v2 state
headers to run on newer snapshot3.

A complete private historical-workspace backup and the retired original are kept
outside the repository under `~/archives/gt3/`. Their tools/caches are historical,
not active global REA installations. Private migration manifests/logs and a stable
conversation continuation reference are in `local/migration/`.

## Publication and operational rules

`.gitignore` excludes agent state, REA installations/databases, game inputs,
generated code, builds, dependencies, sessions and private evidence. The public
audit also rejects these paths if forcibly staged: ignoring is not a security
boundary. Saved credentials are mode600 in private user storage, not Git files.

The local docs service can serve this checkout on3100 behind the existing private
Tailscale proxy. It does not change public exposure, UFW or unrelated port3000.
The old workspace path may temporarily be a compatibility symlink for a running
old agent/shell; no new work should use it. Remove that link only after leaving
old sessions. Do not delete retained history as part of ordinary source cleanup.
