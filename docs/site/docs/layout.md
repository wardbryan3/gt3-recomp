# Authoritative project layout

| Path | Role |
|---|---|
| Root README/AGENTS/HANDOFF/justfile | Project intent, rules, current state, commands |
| recomp/runtime/host/web | Attributed upstream foundation and reviewed source |
| host/gt3_controls.hpp | Standalone input/mapping references |
| host/gt3_clean_steering.* | Bounded recovery source; not installed on current main |
| host/gt3_synthetic_wheel.* | Independent adapter source; not active on current main |
| decomp/gt3 | Authoritative selected knowledge JSON and schema |
| scripts/project | Portable schema/docs/type orchestration |
| docs/site | Source-only curated site; generated views of metadata |
| tests | Source-only regressions and original-dependent fixture source |
| experiments/legacy | Source restoration patches and historical harnesses, not runtime copies |
| local/build | Ignored private inputs/evidence/config and generated outputs |

Keep generated game C++ and CMake output in separate folders. No copies of full runtime repositories for new experiments. Preserve old artifacts externally; no cleanup deletion is required.
