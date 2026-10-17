:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../../workflow.md)
and [execution status](../../../development/restructuring.md) for maintained commands and actual gates.

:::

> Historical experiment record. Not current-main validation; referenced artifacts remain private and services may no longer be running.

# GT3: full-size virtual presentation and audio validation

## Verdict

**Partially demonstrated.** A real native Wayland/WebGPU window and compositor
capture work at **5760×1080**, with unchanged **5760×1344 / 9×3** internal
sampling and expanded view. Parallel execution maintains approximately 60 game
frame requests/sec with an actual SDL PulseAudio/PipeWire clocked stream.
However, presentation feedback still shows occasional 33.33 ms gaps. **Strict,
continuously smooth 60 FPS is not established. Physical-monitor presentation
and audible output are unverified.** No default launcher was replaced.

All changes/artifacts are under `presentation/`, a copy of the prior
`performance/repo`. Original resolution/performance executables, launchers and
performance source diff were verified unchanged. No desktop modes, streaming
configuration, services, packages, ISO or existing save were modified. All
experiment-owned compositor/audio services were stopped at completion.

## Why the old drawable was small

Read-only inspection found active **KWin 6.7.5**, DRM backend, enabled output
**Virtual-2**, physical mode **1920×1080 @ 60 Hz**, scale **1.7**. Wayland reports
**1129×635 logical pixels**; KScreen rounds its geometry to 1130×636. The prior
1129×577 client width matches this logical output constraint; its reduced height
is consistent with the available normal-window area/chrome. Exact allocation
of the remaining 58 logical pixels was not audited.

This is a desktop/window-sizing constraint, not an established rasterizer
ceiling. Also, the old benchmark logged the *initial* SDL pixel size and skipped
SDL event polling, so it did not establish subsequent fractional-scale resize
behavior. The active desktop still cannot provide a 5760-wide output.

A separate installed KWin **VirtualBackend**, scale 1, one 5760×1080 output at
60 Hz, removes that constraint. The native fullscreen SDL drawable, configured
WebGPU surface, and **Spectacle compositor screenshot** all verify 5760×1080.
This does not use the game's headless capture as proof of window dimensions.

Environment: gpu-01, Ryzen 7 5800X3D; Radeon RX 9070 XT; Mesa
26.2.3-arch3.1; SDL 2.32.72; Wayland client 1.26.0. Game uses RADV/Vulkan,
compositor uses radeonsi/OpenGL/EGL. All physical GPU display connectors were
reported disconnected; the active output itself is a virtual streaming output.
The installed RADV non-conformance warning remains, as in earlier tests.

## Isolation and instrumentation

- Private KWin, D-Bus, HOME/XDG directories and sockets; **no DRM modesetting**,
  no nesting into or changing the active desktop.
- Private PipeWire **1.6.9** core `pipewire-gt3`, Pulse socket `pulse-gt3`,
  `gt3-null` sink, **48000 Hz / 1024-frame quantum**. WirePlumber runs its
  **policy-only** profile: no ALSA/Bluetooth/video hardware monitoring.
  This is a clocked audio graph, **not SDL's dummy audio driver**, but it is
  still a virtual null sink, not a speaker/DAC/streaming-endpoint test.
- Window telemetry: request/start/submit timestamps, configured surface size,
  `wp_presentation` feedback on CLOCK_MONOTONIC, discard/failure status,
  audio queued bytes/produced frames, pace wait, queue-empty/drop/error counts.
- 1 Hz sampling of the actual game process CPU/RSS and whole-device GPU busy/
  VRAM; private `pw-top` graph error counts. The initial observer accidentally
  sampled the timeout supervisor for CPU. Those CPU fields are omitted from
  summaries; CPU-specific repeat runs corrected this and record the PID/name.
- GPU busy-time values from the existing runtime are estimates. Whole-device
  busy includes both compositors and other unchanged workloads; it cannot
  establish game-only GPU saturation.
- All scene runs were serial, with no competing builds/analysis. Audio graph,
  compositor and lightweight measurement observers are part of the test path.

## Repeatable measurements

17 scene runs, **72,000 guest frames** total; each 3600 or 7200 frames (about
60 or 120 seconds when keeping up). Same saved scene and scheduled input across
paths. Skip first 300 requests; hold throttle for the first 2000 guest frames,
then release. No steering/race-winning input tuning. Later stationary/barrier
views, especially Midfield, are not representative full-lap performance.

The existing renderer selects **Mailbox**. Only the opt-in FIFO comparison
changes present mode; CPU/VU/render algorithms and detail remain unchanged.
SSE4.1 optimization is **OFF** in this checkout.

| Scene/path | Requests/sec | Distinct virtual feedback timestamps/sec | p99 gap | SDL empty-at-push observations after 5 s |
|---|---:|---:|---:|---:|
| Super, single/Mailbox, repeat | 49.10 | 48.96 | 33.33 ms | 1793 |
| Super, parallel/Mailbox, repeat | 60.00 | 52.49 | 33.33 ms | 0 |
| Super, parallel/FIFO, 120 s | 59.99 | 59.76 | 16.67 ms | 1 |
| Trial, single/Mailbox | 59.99 | 53.16 | 33.33 ms | 36 |
| Trial, parallel/Mailbox | 60.01 | 57.91 | 33.33 ms | 0 |
| Trial, parallel/FIFO, final repeat | 59.98 | 59.76 | 16.67 ms | 0 |
| Midfield, single/Mailbox | 60.00 | 57.24 | 33.33 ms | 0 |
| Midfield, parallel/Mailbox | 60.00 | 50.43 | 33.33 ms | 0 |
| Midfield, parallel/FIFO | 59.99 | 59.95 | 16.67 ms | 0 |

**Do not equate feedback callbacks with distinct displayed frames.** KWin's
virtual backend sometimes supplies multiple callbacks with the same refresh
timestamp. Its sequence values are zero and its reported flags are not proof
of hardware scanout. The table de-duplicates timestamps conservatively; it is
not a physical-display FPS measurement. Average callback throughput near 60
alone would have hidden the cadence problem.

Super FIFO 120-second repeats gave **59.60–59.76 distinct timestamps/sec**.
The latest run had **28 gaps >25 ms**, max 33.33 ms, among the post-warm-up
intervals. Mailbox repeats varied substantially: **52.49–57.24** distinct
timestamps/sec, despite virtually identical 60 requests/sec. FIFO improved
cadence but did not eliminate all gaps.

Matched Super frame interval 5101–5701: single **29.00 ms/request**, parallel
Mailbox **16.66**, parallel FIFO **16.66** including normal audio/presentation
pacing. These are *paced* window numbers, not replacements for earlier headless
compute costs. Longer Super single samples improve when the view becomes less
expensive; they still fail the full-detail 60-FPS target.

CPU-specific repeats, after five seconds: single **82.4% of one core**;
parallel Mailbox **125.8%**; FIFO **110.8%**. Whole-device GPU busy averaged
**59.1 / 72.4 / 68.3%** respectively, not isolated game GPU utilization.
Surface-call CPU p99: **1.23 / 1.55 / 16.11 ms**; FIFO blocks for backpressure.
Median request-to-feedback latency was **18.2 / 26.8 / 62.5 ms**. Thus FIFO's
cadence improvement carries a significant buffering/latency tradeoff.

## Audio, correctness and shutdown

Private PipeWire graph **ERR stayed zero**, and SDL queue failures/dropped
frames stayed zero in all timed scene runs. Parallel Mailbox had no observed
queue starvation; FIFO had 0–4 empty-at-push observations. These observations
are warning indicators, not proof of an audible underrun: Pulse/PipeWire has
additional buffering. Single Super repeatedly emptied SDL's queue and produced
60 seconds of samples over roughly 75.8 seconds of wall time.

A separate, untimed null-sink monitor recording verified actual non-silent
stereo PCM: 48 kHz, 5.005 s, RMS ~7223 in signed-16 units. Audio data is genuinely
flowing through the isolated graph. No claim is made about real speakers,
streaming latency, subjective fidelity or hardware-clock behavior.

Passed:
- Existing hardware/runtime regressions, actual 9×3 GPU addressing and snapshot
  conversion, **20,480 controls differential cases**.
- **Byte-identical 5760×1080 compositor screenshot pixels** across single and
  parallel: bumper, R1 chase, L1 look-behind.
- Save at frame 5650 into a *new* experiment-only snapshot; reload into both
  paths; compositor pixels match uninterrupted execution at frame 5701.
- Timed frame-limit exits and explicit SIGTERM/SDL window-close tests return 0.
  Corrected parallel window drain reports equal posted/completed presents.
- Zero surface failures or missing feedback among **66,900 post-warm-up
  requests**. Known overlay/replay defects remain outside these checks.

The initial test drain used an extra final present. That changed deinterlacing
history and caused screenshot mismatch/ghosting differences. Failure log and
preview/diff artifacts are preserved. An ordered **non-presenting validation
fence** fixes the harness, and all capture comparisons then passed. This is not
reported as a proven game-rendering regression. Final timing repeat runs use
the corrected fence. VU still uses a detached worker and process `_Exit`;
proper joinable worker teardown is **not** established.

## Reproduction and retention

```bash
cd $GT3_LEGACY_ROOT
presentation/build.sh
presentation/start-session.sh
presentation/run-scene.sh super single 3600 repeat-single
presentation/run-scene.sh super parallel 3600 repeat-mailbox
PS2_PRESENT_MODE=fifo presentation/run-scene.sh super parallel 7200 repeat-fifo
# Also supported: trial, midfield. Do not overlap controlled runs/builds.
python3 presentation/summarize.py
presentation/capture-checks.sh
TMPDIR="$PWD/presentation/tmp" presentation/repo/tests/run_resolution_tests.sh \
  "$PWD/presentation/repo/build/presentation"
presentation/stop-session.sh
```

Capture checks expect the saved `presentation/captures/window.state`, already
retained here. To repeat the same save operation without overwriting it:

```bash
presentation/start-session.sh
source presentation/session-env.sh
export PS2_PRESENT_MODE=fifo PS2_PRESENT_CSV="$root/logs/new-save.csv"
cd "$root/repo"
test ! -e "$root/captures/new-window.state" && \
build/presentation/ps2run games/gt3-usa-v110/core-triple.elf \
  --disc games/gt3-usa-v110/disc.iso --load-state "$root/../validation/race-start.state" \
  --ntsc --gt3-triple --render-scale 9 --render-scale-y 3 --output-size 5760x1080 \
  --fullscreen --press 4801:cross:2000 --frames 5701 \
  --save-state "5650:$root/captures/new-window.state"
"$root/stop-session.sh"
```

Original save/screenshot evidence is in `logs/capture-test.log` and `captures/`;
create new save paths rather than overwrite existing user saves. `start-session.sh` refuses existing PID files, and `stop-session.sh`
validates and terminates only the owned process groups. Start/stop commands were
smoke-tested after the measurements.

**Retain:** isolated session scripts, instrumentation, corrected test fence and
regression evidence. **FIFO: retain as an opt-in experiment only**, not a default
recommendation yet. Mailbox average throughput is not smooth-presentation proof;
FIFO's remaining gaps, queue-low observations and latency need investigation.
Next useful experiment: reconcile audio-clock/quantum pacing with presentation
backpressure and reduce buffered latency, changing one thing at a time.
Physical scanout/real audio tests require an explicitly approved environment;
do not alter the current desktop or streaming configuration to obtain them.

Sources: `instrumentation.patch` (incremental to `performance/repo`), scripts,
`environment/`, `results/summary.json`, per-run CSV/load/PipeWire logs,
`captures/`, and `logs/final-regressions.log`. Game imagery/audio/snapshots remain
private/local. The preserved default stays unchanged.
