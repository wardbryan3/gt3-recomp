---
title: Development environment
---

## Public prerequisites

The qualified path is Linux with Git (including required history), Python 3,
CMake, Ninja, **Clang with C++20**, `just`, **Node 22+** and npm. Inherited VU
vector builtins require Clang; GCC support is not claimed. No platform installer
or package-manager operation is performed by this documentation.

Follow [build and run](build-and-run.md) for the maintained executable commands.
Public software-runtime checks require no legal ISO, SDL window, Vulkan, wgpu or
historical private workspace. For a native game window add SDL2 development files;
GPU execution additionally requires Vulkan/driver support and the locally fetched
wgpu SDK. The supported game identity is in [Reference](../reference/supported-profile.md).

Keep a full clone. Historical public checks require revision
`aee79fba37937e4dc99dac4263589d005112c504`; absent Git blobs must fail rather
than silently reading current relocated source. CI fetches full history.

## Optional private analysis tools

REA is an analysis aid, not a public build dependency or semantic authority.
`scripts/project/rea-local.sh` expects a separately installed licensed stack under
ignored `local/rea/`. Review its prerequisites before use. Public source development
and fresh ISO generation do not need REA. Credentials, personal agent/MCP settings,
analysis databases, sessions and downloaded tooling remain private.

## Workspace discipline

Use this repository as the active source root. Keep original assets, generated
translations, disposable cards, builds and captures in ignored local storage.
Do not develop in donor checkouts or compatibility symlinks. Use new output names;
never overwrite user saves or original fixtures. Machine-specific migration,
service and restore instructions are not public onboarding requirements.

Continue with [build/discovery](build-and-run.md), then [workflow](workflow.md).
The sole ongoing handoff checklist is [current continuation](continuation.md).
