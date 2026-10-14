#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
source "$root/session-env.sh"
mkdir -p "$root"/{runtime,home,config,cache,data,state,tmp,logs}
chmod 700 "$root/runtime"
for f in compositor audio audio-policy; do
 if [[ -f "$root/$f.pid" ]]; then echo "PID file exists: $root/$f.pid; inspect or stop the owned session first" >&2; exit 1; fi
done
setsid "$root/start-display.sh" > "$root/logs/compositor.log" 2>&1 < /dev/null & echo $! > "$root/compositor.pid"
for ((i=0;i<100;i++)); do [[ -S "$root/runtime/gt3-virtual" ]] && break; sleep .1; done
[[ -S "$root/runtime/gt3-virtual" ]]
setsid pipewire -c "$root/config/audio.conf" > "$root/logs/audio-server.log" 2>&1 < /dev/null & echo $! > "$root/audio.pid"
for ((i=0;i<100;i++)); do [[ -S "$root/runtime/pipewire-gt3" ]] && break; sleep .1; done
[[ -S "$root/runtime/pipewire-gt3" ]]
# Policy only: no ALSA, Bluetooth or video-device monitoring on this private core.
setsid wireplumber --profile policy > "$root/logs/audio-policy.log" 2>&1 < /dev/null & echo $! > "$root/audio-policy.pid"
for ((i=0;i<100;i++)); do [[ "$(pactl get-default-sink 2>/dev/null || true)" == gt3-null ]] && break; sleep .1; done
[[ "$(pactl get-default-sink)" == gt3-null ]]
wayland-info > "$root/environment/virtual-wayland-session.txt"
echo "Isolated Wayland gt3-virtual and private Pulse/PipeWire gt3-null ready"
