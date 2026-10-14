#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$root"/{runtime,tmp,config,cache,data,home,logs}
chmod 700 "$root/runtime"
export HOME="$root/home" XDG_RUNTIME_DIR="$root/runtime" XDG_CONFIG_HOME="$root/config" XDG_CACHE_HOME="$root/cache" XDG_DATA_HOME="$root/data" TMPDIR="$root/tmp"
unset DISPLAY WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS SESSION_MANAGER
export QT_QPA_PLATFORM=offscreen
exec dbus-run-session --config-file "$root/config/dbus.conf" -- kwin_wayland --virtual --width 5760 --height 1080 --scale 1 \
 --output-count 1 --socket gt3-virtual --no-lockscreen --no-global-shortcuts --no-kactivities
