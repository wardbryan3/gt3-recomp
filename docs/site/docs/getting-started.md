# Getting started

From the authoritative Git checkout, install just separately if needed (no automatic system installs). Requires Python3, Clang/CMake and Node>=20 for docs.

```bash
just --list
just check
just test
just setup
just docs-build
just status
just lookup 0x001e4478
just evidence 0x001e4478
```

No game files or raw exports are needed. `just build-game /absolute/path/GT3.iso` is separately asset-dependent and retains original behavior. `just docs-dev` binds0.0.0.0:3100: trusted networks only. It does not configure firewall/Tailscale or replace the existing private server.

`just verify-private /absolute/path/to/preserved/resolution/repo` explicitly verifies original ELF, eleven private hashes and66 retained IDs. Missing or changed evidence fails, without rewriting it. Current main has no run-clean/build-clean command: the compiled recovery source is not installed into the runtime. See [testing](testing.md).
