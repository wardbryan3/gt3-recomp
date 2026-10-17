---
title: Troubleshooting without weakening proof
---

| Symptom | Check and response |
|---|---|
| Missing CMake/Ninja or Clang-only builtin errors | Check the [environment](environment.md). A cached executable is not a fresh build; report the blocked prerequisite. Do not claim GCC qualification. |
| Missing baseline Git revision | Fetch required history as described in [build/run](build-and-run.md). Current source is not a substitute for a historical blob. |
| Missing private artifacts | Use the correct explicit root and qualified inputs. Public success does not mean private proof passed. Never silently reduce a required matrix. |
| Snapshot v2 fails to load | Current runtime uses v3. Do not alter headers. A card is persistent save data, not a snapshot. See the [native-v3 investigation](../research/checkpoints/native-v3-baseline.md). |
| Outputs match but replacement count is zero | You proved fallback parity, not substitution. Inspect admission, scope and actual counters before changing any guard. |
| Correct scalar result but CPU differential fails | Compare scratch/upper lanes, stack, FPU flags, return state and exact budget. See the [worked implementation](worked-example-mt-selector/implementation.md). |
| Entry PC differs in an observer trace | Direct generated calls can carry dispatch transport state. Use only the explicitly qualified semantic probe convention; do not mask outgoing CPU/RAM comparisons. |
| GPU scale/window size not granted | Inspect actual backend, buffer limits and drawable dimensions. Software fallback and compositor limits invalidate assumed GPU/scanout claims. |
| A generated documentation edit disappears | Edit `scripts/project/project.py` or its public metadata inputs as appropriate, not the four generated Markdown views alone. Never repin historical authorities for presentation changes. |
| A documentation link fails after a move | Use the canonical new Markdown path, keep old published routes in redirect configuration, then run the strict build. A redirect is not a substitute for fixing internal links. |

## Learn from actual failures

The selector differential caught `+0x210` versus **`+0x20A`**. Its first native guard
rejected a legitimate stack because the protected region was too broad. The pedal
survey's stopped fallback result was later resolved by structural stack-frame proof,
not by declaring nearby addresses interchangeable. The presentation harness's extra
final present changed deinterlacing history; a non-presenting fence fixed the test.

In each case, preserve the failed observation, identify the assumption, and qualify
new evidence without rewriting the old outcome. See [lessons from the selector](worked-example-mt-selector/live-validation-and-lessons.md)
and [research](../research/index.md). These examples are not permission to expand a
recovery or operate historical services.
