#!/usr/bin/env bash
# All native regressions available in current source, without changing assertions.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 3 ]] || { echo "usage: $0 BUILD_ROOT ORIGINAL_ELF NEW_RESULTS_DIR" >&2; exit 2; }
build="$(realpath "$1")"; elf="$(realpath "$2")"; out="$(realpath -m "$3")"
[[ ! -e "$out" ]] || { echo 'results directory exists' >&2; exit 1; }
mkdir -p "$out"
exec > >(tee "$out/regressions.log") 2>&1
python3 - "$root" "$elf" "$build" <<'PY'
import hashlib,json,pathlib,sys
root,elf,build=map(pathlib.Path,sys.argv[1:])
assert (build/'build-identity.json').is_file()
assert hashlib.sha256(elf.read_bytes()).hexdigest()==json.loads((root/'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
PY
for mode in original observed; do
 ctest --test-dir "$build/$mode" --output-on-failure
done
for test in gt3_controls_test gt3_steering_trace_test gt3_synthetic_wheel_test gt3_pedal_discovery gt3_clean_steering_test anisotropic_test; do
 mode=original; [[ "$test" != gt3_clean_steering_test ]] || mode=observed
 clang++ -std=c++20 -O2 -I"$root/host" -I"$root/runtime/include" -I"$root/runtime/src" \
  "$root/tests/$test.cpp" -Wl,--start-group "$build/$mode/libps2game.a" \
  "$build/$mode/libgt3_recovered.a" "$build/$mode/libps2runtime.a" -Wl,--end-group \
  "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/$test"
 "$out/$test" "$elf"
done
(cd "$root" && just check && just test && just docs-build)
echo 'All current native baseline regressions PASS (no browser/physical-hardware claim)'
