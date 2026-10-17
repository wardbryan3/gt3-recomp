---
title: Live validation, historical results and lessons
---

# 5. Live validation, lessons and limits

## Historical live controls (this checkpoint only)

The native matrix used original `--press` schedules from unchanged original
snapshots — no virtual shifter, no forced policy, no edited calibration.
Historical counts, source-pinned in
[mt-selector-v1](../../research/transmission/mt-selector-v1.md):

| Layer | Count |
|---|---|
| Accepted native runs / total updates | **15** / **7,500** (MT cycle 600 + MT Reverse 600 + AT control 300, five modes each) |
| Real-entry live shadow | **2,400** complete CPU + 32 MiB + exact-budget comparisons |
| Actual live substitution | **2,400**, zero fallback; **2** retained generated speed-helper calls |
| Whole native parity | Exact final snapshots, 36 MiB EE/IOP/SPU dumps, capture sets, repeated entry/exit traces |

Each scenario ran five ways: untouched original, build-OFF trace,
build-ON/runtime-OFF trace, clean + shadow, clean + shadow repeat. Actual
entry identity: owner 0, stored/effective policy 1, mode 0, no suppression,
car `0x01FBB7BC`, stack `0x0049AF30`, return `0x001E5730`. The MT cycle
observed 10 accepted selections across states 0–3; Reverse observed 2
accepted selections, 160 auxiliary-held entries, one original speed call per
clean/repeat run; the AT control entered the MT body **zero** times.

**Shadow vs replacement, precisely.** Shadow runs execute original and clean
bodies on *copies* of the actual entry CPU and entire actual RAM, restoring
pre-entry RAM before any actual substitution proceeds. Shadow counters are
separate from actual replacement counters; the original native control has
neither probe nor clean execution. These are finite original-context
observations, not all-state reachability claims.

Process accounting: **24** attempted native processes — 15 accepted, 8
completed exclusions (original/trace controls and five short AT runs), 1
aborted guard attempt — all separate records.

## Actual retained mistakes

- First isolated link failed on a duplicated generated entry-array symbol; the
  oracle now renames that symbol too.
- The first differential caught the incorrect maximum offset `+0x210`; the
  original addressing resolves to **`+0x20A`**. Failed source, fixture and log
  retained; the corrected rerun weakened nothing.
- First live-host compile used an unavailable frame symbol; separate corrected
  build.
- The first clean native launch stopped on a guard rejection, not a CPU
  mismatch: the protected-region guard wrongly included the real native stack
  `0x0049AF30` (original ELF loaded end `0x003531E3`). Guard corrected;
  native-stack and budget-boundary differentials added first.
- The initial helper budget guard was an arbitrary 10,000; it now derives
  `16*maximum+64`.
- A completed 100-update AT control produced **no scheduled capture**; it was
  excluded, not accepted on dump equality. A 300-update five-way AT control
  supplied the capture.

Final raw parent verification rejected three legitimately updated public
files (handoff, transmission navigation, sidebar); the successful result is a
**version-qualified** parent verification against their exact historical
versions, raw failure retained.

## Limitations

Not all cars, modes or threads; single-thread deterministic setup; no
physical-controller proof; the speed helper `0x001E4E80` remains generated with
its own separate composition; AT and policies 2–6, clutch/parts/config 205 and
power-transfer recovery stay original and open.

## Separate approval

Passing every layer is **proof, not approval**. "Frozen" froze the exact
evaluated **disposable validation overlay** — build and runtime default OFF,
fallback to generated code, no canonical installation, no new shifter/clutch/
Neutral API. Replacing original execution requires explicit approval from the
human project owner, recorded through the current approval process in
`project/gt3/approvals.json`. The historical `transmission.json` labels
`lifecycle: "frozen"` and `stop: true` record an evaluated boundary and stop, **not**
that integration approval. The historical report ends the iteration
with "stop after this iteration": no commit, no push, no adjacent Frozen
modification.
