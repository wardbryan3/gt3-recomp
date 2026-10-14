#!/usr/bin/env bash
root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOME="$root/home" XDG_RUNTIME_DIR="$root/runtime" XDG_CONFIG_HOME="$root/config" XDG_CACHE_HOME="$root/cache" XDG_DATA_HOME="$root/data" XDG_STATE_HOME="$root/state" TMPDIR="$root/tmp"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$root/runtime/bus" WAYLAND_DISPLAY=gt3-virtual QT_QPA_PLATFORM=wayland SDL_VIDEODRIVER=wayland
export PIPEWIRE_REMOTE=pipewire-gt3 PULSE_SERVER="unix:$root/runtime/pulse-gt3" SDL_AUDIODRIVER=pulseaudio
export PS2_SCRIPTED_INPUT=1 PS2_REQUIRE_DRAWABLE=1 PS2_REQUIRE_AUDIO=1
unset DISPLAY PS2_TIME PS2_WINDOW_BENCH PS2_PROFILE PS2_NO_VU_THREAD PS2_ONE_THREAD
