:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](../../developer-guide/workflow.md)
and [execution status](../checkpoints/restructuring.md) for maintained commands and actual gates.

:::

> Historical experiment record, not current-main validation or a service runbook. No service state, reachable endpoint or current firewall consent is established here. The old IPs, ports, connection directions and lifecycle commands below document only that private environment; do not use them to connect, restart services or change firewall rules. No services were inspected or operated during this cleanup.

# Historical GT3 LAN driving test

## Session recorded then

The report described an experiment-owned session on gpu-01 bound to
**0.0.0.0:8765**, with the private URL
`http://10.6.65.10:8765/#<access-token>` and token file `run/access-token`
(mode 0600). This was a trusted-LAN-only link, not a public deployment. Nothing
was installed as a system service; no active desktop/streaming/audio services
were changed in that experiment. Python dependencies were project-local. After
explicit approval for that session, two UFW exceptions were added: TCP 8765 and
UDP 8766, restricted to 10.6.65.0/24. The report stated that existing
firewall/streaming allowances were unchanged. That approval does not carry
forward to any new session.

## Historical MacBook client instructions {#macbook}

The original client instructions and control table follow for context only;
they are not current compatibility or endpoint guidance.

Chrome was recommended; Safari VP8 WebRTC support was expected, not certified. Click
**Connect**, **Enable sound**, and optionally **Fullscreen**. Keep the tab
focused. **Restart race** restores the initial Super Speedway snapshot if the
race has progressed while waiting. One active driver; a new authorized
connection replaces the old one. Leave the access token in the URL fragment.
No Mac microphone/camera permissions are required.

| Key | Action |
|---|---|
| Z | Accelerate / Cross / confirm |
| A | Brake / Square |
| Left / Right arrows | Steer |
| W | R1: toggle bumper/chase camera |
| Q, held | L1: look behind |
| Enter | Start: pause/menu |
| Arrow keys | Menu navigation |
| X | Circle: back/cancel where applicable |
| S | Triangle |
| 1 / 2 | L2 / R2 |
| Backspace | Select |

Browser gamepads are supported if the browser permits the API: bottom face
button accelerates, left face button brakes, left stick steers, right shoulder
changes camera, left shoulder looks behind, Start pauses. Plain HTTP can block
gamepad access; keyboard works independently. No rumble. Lost focus/connection
releases controls through a heartbeat watchdog.

## What the experiment tested {#what-is-being-tested}

- Parallel execution and opt-in SSE4.1 graphics preparation; FIFO presentation.
- Original full-width **5760×1080 window / 5760×1344 internal / 9×3** rendering.
- The transmitted **1920×1080 center crop** represents the middle display,
  **not the complete three-screen panorama**. Render detail is not reduced.
- Three asynchronous GPU readbacks of the actual swapchain feed a private
  seqlock shared-memory file. No active desktop capture or OS input injection.
- VP8 WebRTC targets 60 FPS, nominal 8 Mbps; 48 kHz stereo private PipeWire sink
  monitor is sent as Opus. No public STUN/TURN servers; LAN host ICE only, pinned to
  **10.6.65.10:8766** with MAX_BUNDLE (one shared UDP transport).
- Page reports actual decoded FPS, control-message RTT and video jitter-buffer
  delay. These are not end-to-end input-to-photon measurements.

Pre-color-fix local WebRTC loopback (transport/throughput only): connected,
**1920×1080**, 356 decoded video frames
and 307 audio frames over 6.219 seconds including startup (~57 FPS), non-silent
PCM; acceleration input exercised. Restart 200, unauthenticated offer 401,
asset route 404. GPU sampling/state conversion, hardware regressions and 20,480
controls differential tests passed on this build. Mac delivery/feel must be
checked by the user. Stream compression, capture/network/decoder latency and
extra streaming CPU load confound direct comparison with local-monitor timing.

### Color-channel correction

The first stream incorrectly interpreted the actual RGBA8 swapchain as BGRA,
swapping red/blue. The earlier compositor screenshots bypassed this streaming
path and were unaffected. The corrected native capture published its WebGPU format in
shared-memory metadata; the video track selects RGBA/BGRA accordingly. Offline
red/green/blue/white tests pass for both byte orders and their sRGB variants.
A live corrected frame showed blue sky/red taillights. A post-fix loopback test
was interrupted by the user's reconnect; no further takeover tests were run
while the user was driving. This fix does not change game/render algorithms.

No ISO/ELF/save/code directories are served. HTTP page and signaling are intended
only for a trusted LAN (not an internet deployment). WebRTC media/control use
DTLS/SRTP; the HTTP bootstrap itself is not TLS. Router settings were not changed. In that session, `firewall.sh` managed the two approved LAN-only UFW exceptions
and was designed to remove them when stopping the server. The old troubleshooting
note required direct LAN UDP connectivity; it is not permission to open ports now. Browser keyboard input reaches
only the isolated game, not the host desktop.

## Historical lifecycle transcript — not current commands {#lifecycle}

The experiment used `$GT3_LEGACY_ROOT` and reported original builds/default
launchers, ISO and existing saves untouched. The following old commands are
retained solely to explain process ownership, not to assert that anything is
running or installed. Maintained repository commands are in the
[current workflow](../../developer-guide/workflow.md), not these private harnesses.

```bash
# HISTORICAL ONLY: commands from the former private LAN session.
cd $GT3_LEGACY_ROOT
# Former stop command for that stream and its private display/audio:
lan-play/stop-server.sh
# Former restart command (no rebuild was needed then):
lan-play/start-server.sh
# Former isolated-copy rebuild command, used with the stream stopped:
lan-play/build.sh
```

`run-server.sh` reuses the private presentation session environment. The server
owns the native child, and SIGTERM performs window drain/cleanup. Native VU
still terminates via process exit rather than a fully joinable worker teardown.
`stop-server.sh` validates the server PID/command/group before signaling it;
private display/audio shutdown validates its own groups as well. The old start script re-added
that session's firewall allowances; stop removed exactly those two allowances.
This records script behavior, not current firewall state or reusable consent.
The project-local aioice patch reads `GT3_ICE_PORT` (set only in this server),
leaving the loopback client and system Python packages on normal ephemeral ports. Never use
blanket process-name kills. Logs: `logs/server.log`, `logs/game.log`,
`logs/audio-capture.log`, `logs/loopback-result.json`, `logs/regressions.log`.
The experimental default launcher outside this LAN service is unchanged.
