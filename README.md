# GT3 Recomp

Experimental Gran Turismo 3 recovery and native reconstruction, based on
[snuri00/ps2-web-recomp](https://github.com/snuri00/ps2-web-recomp).
**Recover original behavior first; modernize or enhance only with separate approval.**

Bring your own legally obtained disc image. No ISO, executable, original tables,
generated game translations, saves or game-containing binaries are distributed.

## One workflow, two products

```sh
just check                 # public source/ownership/authority/publication checks
just test                  # public source and historical reducer negatives; no ISO
just setup && just docs-build
just status
just lookup 0x001e4478
just build-game /absolute/path/to/GT3.iso my-gt3-build
```

- **`ps2run`**: permanent, enhancement-free original generated reference. Runtime,
  recompiler and platform updates are reviewed and version-qualified, not frozen forever.
- **`gt3-native`**: evolving playable product, eventually the default. Initially
  original generated execution, with **no recovered or enhanced gameplay linked**.
  Default gameplay remains original-equivalent. Existing inherited opt-in presentation
  code is not a new simulator/hardware qualification.

Playable and future headless execution share authoritative gameplay sources/settings;
there is no training physics fork. The three six-month project milestones remain
**real simulator play**, **correct headless AI training**, and **complete playable
native GT3 without PS2 execution/translation machinery**. ISO assets remain required.
Restructuring does not implement those milestones or authorize another recovery.

## Repository

- [`src/gt3/`](src/gt3/): domain-owned gameplay, with separate concrete PS2 bindings.
- [`project/gt3/`](project/gt3/): current authorities, historical knowledge, proof and
  product approval records. Historical source hashes are preserved, not repinned.
- [`validation/gt3/`](validation/gt3/): differential/integration/live support;
  domain-local contracts live beside their sources.
- [`docusaurus/docs/`](docusaurus/docs/): **all maintained project documentation**.
- `recomp/`, `runtime/`, `host/`: inherited execution/tooling; notices and reviewed fixes retained.

Start with [build and discovery](docusaurus/docs/getting-started.md),
[architecture](docusaurus/docs/architecture.md),
[restructuring status](docusaurus/docs/development/restructuring.md),
[continuation](docusaurus/docs/development/continuation.md), and
[publication rules](docusaurus/docs/development/PUBLICATION.md).

Historical evidence verification is explicit:

```sh
just verify-private /absolute/path/to/retained-original-evidence-root
just verify-historical extensions "$PWD"
just verify-checkpoint /absolute/path/to/NEW-current-report.json
```

These are different claims. Historical verification never approves current source
integration. Missing/changed private inputs fail; public checks need no private files.
Do not confuse bounded fixtures or software-native observations with full-game,
physical wheel/FFB, headless correctness, or PS2-independent native completion.

## Requirements and provenance

Linux is the qualified development path: Git with required history, Python 3,
CMake, Ninja, Clang/C++20, Node 22+, npm and `just`; SDL2 development files for a
window. Native GPU execution also needs Vulkan and the locally fetched wgpu SDK.
Clang is required by inherited VU builtins. Public source tests use software runtime.
See the build guide for explicit dependencies, shallow-clone history and discovery.

Upstream supplies the static EE/VU recompilers, PS2 runtime, WebGPU GS renderer,
browser frontend and parallel architecture. Its Git history, [MIT license](LICENSE)
and third-party notices, including `runtime/src/ipu/NOTICE`, are preserved.
This license does not cover GT3 or generated game translations. Gran Turismo and
PlayStation are their owners' trademarks; this project is unaffiliated with Sony,
Polyphony Digital or the upstream maintainer.
