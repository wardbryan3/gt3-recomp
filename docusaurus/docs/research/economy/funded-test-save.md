---
title: Funded test save — private fixture
---

## Goal and current status

A private master memory-card image now provides **99,999,999 starting credits**
for bounded tests. Each session uses a writable disposable copy. Normal purchase
costs, sale proceeds and garage limits stay unchanged.

**This is temporary fixture tooling, not clean production code, Recovered
gameplay or a general save editor.** The owner explicitly approved testing
99,999,999 and other candidate values through controlled temporary state changes,
provided the behavioral Oracle is not permanently changed and the work is not
presented as clean code. Only 99,999,999 was tested as a funded candidate.

The independent **Oracle**, `ps2run`, and its sources remain unchanged. Its
executable is byte-identical to the previously qualified reference. The funded
card is a **Fixture**: an artificial test input, not evidence of naturally earned
credits or an installed runtime enhancement.

**99,999,999 is a tested starting value, not the game's proven maximum.** The
checks below cover the Original USA v1.10 profile and selected purchase, sale and
persistence paths. They do not establish safety for every economy operation.

## Use a fresh session

These tools, cards and captures are private local artifacts, not distributed
checkout contents. Missing prerequisites must cause refusal, not use of a normal
user card.

```sh
python3 -B local/funded-test-save/session.py --name funded-play-01
```

The default session lasts at most 36,001 game frames, captures a screenshot every
3,600 frames and has a 900-second wall-clock timeout. Use the normal controls to
enter Simulation Mode and play. For example, this shorter check enters Simulation
Mode through ordinary scheduled button presses:

```sh
python3 -B local/funded-test-save/session.py \
  --name funded-check-01 --frames 1601 --every 200 --timeout 180 \
  --press 300:start --press 1020:down --press 1100:cross
```

Use a **new name** for every session. Existing output directories are refused.
The working card is:

```text
local/purchase-scenarios/runs/<name>/card.ps2
```

Buy, sell and save normally. The launcher does not refill the balance. When more
funds are needed, stop the game and start a new session from the protected master.
Do not replace a card underneath a running process.

**A fresh session resets all progress to the master: day 1, no garage cars.**
Cars, parts and progress from the previous working copy are not carried over.
“Unlimited credits” means the starting fixture is reusable; each running balance
is finite. Refilling an ongoing save while keeping its new progress is out of
scope.

## Files and protection

| File | Role |
|---|---|
| `local/funded-test-save/master.ps2` | Qualified private memory-card image; read-only input, never the active card. |
| `local/funded-test-save/session.py` | Temporary private session wrapper; pins the qualified master's SHA-256 and copies it through the existing scenario launcher. |
| `local/funded-test-save/prepare.py` | Temporary preparation hack; edits only a disposable snapshot's credit field. Not used during ordinary test sessions. |
| Per-session `card.ps2` | Independent writable copy. Normal game persistence writes here. |
| Per-session snapshots, dumps and captures | Disposable verification outputs, not substitutes for the master or card-load tests. |

The master has read-only file permissions, but permissions alone are not the
write boundary: a writable parent directory can permit replacement. The existing
`local/purchase-scenarios/run.py` uses bubblewrap to mount the host filesystem
read-only, with the fresh run directory writable for game outputs. It supplies
an explicit working-card path and keeps snapshots and captures in that directory.
The same boundary remains active through process exit.

The session wrapper refuses a missing, non-regular, writable, wrong-size or
wrong-digest master, symbolic-link aliases, unsafe or existing output paths, and
unavailable system bubblewrap. It exposes no card override or snapshot-load
option. There is no fallback to normal persistence.

The underlying launcher now accepts `--card-sha256`. The wrapper always supplies
its pinned digest. Both the source card and the copied working card must match
**before the game starts**. The source inputs and master are checked again after
the run, including failure returns. Legacy scenario calls without that optional
argument do not gain the trusted-master check.

## How the fixture was prepared

The first prerequisite test used no credit edits: the game formatted a disposable
card at 18,000 credits, saved the legitimately purchased Demio state at 3,340
credits, then cold-loaded that card with the correct balance and car.

Funded preparation then used this bounded method:

1. Read the known Original seed snapshot at 18,000 credits and zero cars.
2. Check the `PS2STATE` magic, version 3, `ee` section tag, known state pointer and
   original credit/car fields. Check the Original build identities.
3. Derive the RAM start from the actual serialization in
   `runtime/src/system.cpp::machine_state` and a compiled `sizeof(ps2::Cpu)`
   helper. For this build, the CPU is 1,440 bytes and RAM starts at file byte
   1,460. These are **snapshot coordinates, not memory-card offsets**.
4. Copy the snapshot and change only the eight-byte credit field at state
   `+0x18` to 99,999,999. Compare the entire prefix and suffix to prove no other
   bytes changed. Leave the original seed and snapshot version unchanged.
5. Let the unchanged game load that temporary snapshot and write a disposable
   card through its normal Save Game flow. The game handles its save format and
   integrity data; no card-file offsets or checksums are guessed.
6. Cold-load the resulting card in new processes **without a state snapshot**.
   Validate display, transactions and persistence before accepting the master.
7. Copy the tested initial card into the read-only master and verify fresh
   sessions through the guarded wrapper.

The master is a memory-card image, not the edited snapshot. Ordinary sessions do
not load the preparation snapshot, modify RAM, call the Recovered credit setter
or install a runtime hook. Another candidate value requires new validation; the
script's signed64 input range is not a claim that all representable values work.

## Observed results

| Check | Result |
|---|---|
| Funded card cold load | UI and RAM show 99,999,999 credits; garage count 0. No state snapshot loaded. |
| Demio purchase | Normal price 14,660; credits become 99,985,339; garage count becomes 1 and the Demio is visible. |
| Purchase save/cold load | Normal Save Game reports “Complete”; new-process card load retains 99,985,339 and the Demio. |
| Demio sale | Normal proceeds 3,665; credits become 99,989,004; UI reports “Sold” and then an empty garage. |
| Sale save/cold load | Normal save and new-process card load retain 99,989,004 and garage count 0. |
| Guarded master session | A complete cold-start purchase/save run through `session.py` changes only the independent working card; master digest stays unchanged. |
| Fresh-copy reset | A second guarded cold start returns to 99,999,999 and garage count 0. Its working card matches the pristine master, not the purchased-car card. |
| Failure checks | 15 private harness tests cover master validity, aliases, output paths, isolation availability, CLI overrides, and rejection of bad source/copied-card digests before execution. The 12 existing scenario safety tests also pass. |
| Live write-boundary probe | A disposable outside canary rejects direct, symbolic-link and host-parent `/proc` write paths, plus hard-link creation. An exit callback still cannot write outside, but can write a disposable output. |
| Missing isolation | A real wrapper invocation with bubblewrap unavailable refuses before creating a run directory. |

The harness unit tests use dummy cards and mocked launches; they are **not**
Original gameplay evidence. The transaction and cold-load rows above used the
unchanged Original executable. Source input hashes were unchanged across those
runs. The checks do not compare every normal user file or constitute a full
sandbox security review.

One purchase-save navigation attempt reached wheel settings instead of Save
Game. It is not counted as a successful save. The corrected attempt used
Triangle to return from Garage to Home, reached “Complete”, and passed cold load.

The runtime can flush dirty card data independently of the save UI. Normal saves,
disk persistence and process exit were tested within the write boundary. The
game's separate autosave option was **not** exercised; protection does not depend
on avoiding that option. No claim of all save branches or full economy recovery
is made.

## Scope and remaining limits

This delivers a private, reusable funded starting fixture, not a product feature.
No developer menu, refill hook, free purchases, price change, expanded garage or
Recovered gameplay integration was added. No maximum balance was established;
there is no need to search larger values for the present testing goal.

The general save format, all balance writers, complete transactions and a safe
production credit-assignment API remain unresolved. Passing these fixture tests
is not approval to replace Original execution. See the
[economy investigation](index.md) for the wider recovery limits and
[economy verification commands](../../reference/commands.md#isolated-economy-verification)
for separate function-level differentials.

Keep cards, snapshots, dumps and captures private. No commit or push is implied
by creating these local artifacts or updating this page.
