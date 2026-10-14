> Historical experiment record. Not current-main validation; referenced artifacts remain private and services may no longer be running.

# GT3 LAN driving test

Running on gpu-01, **0.0.0.0:8765**, in a new experiment-owned session. Open
`http://10.6.65.10:8765/#<access-token>`; token is stored in `run/access-token`
(mode 0600). Share the link only with trusted LAN clients. Nothing is installed
as a system service; no active desktop/streaming/audio services were changed.
Python dependencies are project-local. After explicit user approval, two UFW
exceptions were added: TCP 8765 and UDP 8766, restricted to 10.6.65.0/24. Existing
firewall/streaming allowances remain unchanged.

## MacBook

Chrome recommended; current Safari should also support VP8 WebRTC. Click
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

## What is being tested

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
path and were unaffected. Native capture now publishes its WebGPU format in
shared-memory metadata; the video track selects RGBA/BGRA accordingly. Offline
red/green/blue/white tests pass for both byte orders and their sRGB variants.
A live corrected frame shows blue sky/red taillights. A post-fix loopback test
was interrupted by the user's reconnect; no further takeover tests were run
while the user was driving. This fix does not change game/render algorithms.

No ISO/ELF/save/code directories are served. HTTP page and signaling are intended
only for a trusted LAN (not an internet deployment). WebRTC media/control use
DTLS/SRTP; the HTTP bootstrap itself is not TLS. Router settings were not changed. The two approved LAN-only UFW exceptions
are managed by `firewall.sh`; stopping the server removes them. If the page opens but video does not connect, report its error;
WebRTC also needs direct LAN UDP connectivity. Browser keyboard input reaches
only the isolated game, not the host desktop.

## Lifecycle

All files remain under `$GT3_LEGACY_ROOT`.
Original builds/default launchers, original ISO and existing saves are untouched.

```bash
cd $GT3_LEGACY_ROOT
# Currently running. To stop only this stream and its private display/audio:
lan-play/stop-server.sh
# Later restart (no rebuilding needed):
lan-play/start-server.sh
# Rebuild isolated copy, with stream stopped:
lan-play/build.sh
```

`run-server.sh` reuses the private presentation session environment. The server
owns the native child, and SIGTERM performs window drain/cleanup. Native VU
still terminates via process exit rather than a fully joinable worker teardown.
`stop-server.sh` validates the server PID/command/group before signaling it;
private display/audio shutdown validates its own groups as well. Start re-adds
the approved firewall allowances; stop removes exactly those two allowances.
The project-local aioice patch reads `GT3_ICE_PORT` (set only in this server),
leaving the loopback client and system Python packages on normal ephemeral ports. Never use
blanket process-name kills. Logs: `logs/server.log`, `logs/game.log`,
`logs/audio-capture.log`, `logs/loopback-result.json`, `logs/regressions.log`.
The experimental default launcher outside this LAN service is unchanged.
