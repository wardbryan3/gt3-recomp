#!/usr/bin/env bash
# Revalidation only: current source/tools; original game material stays private.
# No legacy runtime source or compiled archives are linked. No canonical hooks.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# != 2 ]]; then
 echo "usage: $0 ORIGINAL_INPUT_ROOT NEW_OUTPUT_ROOT" >&2
 echo "input root supplies core.elf, entries.txt, vu1/; output must not exist" >&2
 exit 2
fi
input="$(realpath "$1")"; out="$(realpath -m "$2")"
[[ ! -e "$out" ]] || { echo "output already exists: $out" >&2; exit 1; }
mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$input" <<'PY'
import hashlib,json,pathlib,sys
root,src=map(pathlib.Path,sys.argv[1:])
expected=json.loads((root/'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
assert hashlib.sha256((src/'core.elf').read_bytes()).hexdigest()==expected,'wrong original profile'
assert (src/'entries.txt').is_file() and list((src/'vu1').glob('*.bin')),'missing discovery inputs'
PY
cmake -S "$root" -B "$out/tools" -G Ninja -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_CXX_COMPILER=clang++ -DPS2_WGPU_DIR="$root/build/no-gpu-sdk"
cmake --build "$out/tools" --target eerecomp vurecomp --parallel 6
for mode in original observed; do
 probes=(); [[ "$mode" != observed ]] || probes=(--probes "$root/scripts/gt3_wheel.probes")
 "$out/tools/eerecomp" "$input/core.elf" --entries "$input/entries.txt" \
  "${probes[@]}" --out "$out/generated-$mode"
 "$out/tools/vurecomp" "$input/vu1" "$out/generated-$mode"
done
# Four unchanged frozen gates in a disposable translation only. The original
# instructions remain present; unsupported contexts fall back to those bodies.
python3 - "$root" "$out/generated-observed" <<'PY'
import pathlib,sys
root,dst=map(pathlib.Path,sys.argv[1:])
(dst/'gt3_clean_steering.hpp').write_bytes((root/'host/gt3_clean_steering.hpp').read_bytes())
for name,sites in [('unit_0044.cpp',[('00210F90',None),('002115F8',None)]),
                   ('unit_0039.cpp',[('001E4368',None),('001E45A8','001E48FC')])]:
 p=dst/name;s=p.read_text();s='#include "gt3_clean_steering.hpp"\n'+s
 for address,target in sites:
  label='L_'+address+':\n';assert s.count(label)==1,(name,address)
  action='goto L_'+target+';' if target else 'return;'
  s=s.replace(label,label+f'    if (gt3::clean::replace(c, 0x{address}u)) {{ {action} }}\n')
 p.write_text(s)
PY
for mode in original observed; do
 cmake -S "$root" -B "$out/$mode" -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER=clang++ -DBUILD_TESTING=ON -DPS2_GENERATED="$out/generated-$mode"
 targets=(ps2game gt3_recovered gt3_hardware_test sif_scratchpad_test gt3_recovered_source_test)
 [[ "$mode" != original ]] || targets+=(ps2run)
 cmake --build "$out/$mode" --target "${targets[@]}" --parallel 6
done
clang++ -std=c++20 -O2 -I"$root/host" -I"$root/runtime/include" \
 "$root/tests/gt3_baseline_host.cpp" "$out/observed/libps2game.a" \
 "$out/observed/libgt3_recovered.a" "$out/observed/libps2runtime.a" \
 "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm \
 -o "$out/observed/gt3_baseline_host"
clang++ -std=c++20 -O2 -shared -fPIC "$root/tests/gt3_baseline_clock.cpp" -o "$out/fixed-clock.so"
clang++ -std=c++20 -O2 -I"$root/runtime/include" "$root/tests/gt3_baseline_layout.cpp" \
 "$out/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" \
 -ldl -lpthread -lm -o "$out/state-layout"
"$out/state-layout" > "$out/state-layout.json"
python3 - "$root" "$input" "$out" <<'PY'
import hashlib,json,pathlib,subprocess,sys
root,src,out=map(pathlib.Path,sys.argv[1:])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[src/'core.elf',src/'entries.txt',*sorted((src/'vu1').glob('*.bin')),
 root/'third_party/wgpu-native/lib/libwgpu_native.a',
 out/'original/ps2run',out/'observed/gt3_baseline_host',out/'fixed-clock.so',
 out/'state-layout',out/'state-layout.json']
sources={str(p.relative_to(root)):sha(p) for parent in ['host','runtime','recomp','tests','scripts']
 for p in sorted((root/parent).rglob('*')) if p.is_file() and p.suffix in ['.cpp','.hpp','.sh','.py','.probes']}
record={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'source_hashes':sources,'inputs_and_executables':{str(p):sha(p) for p in files},
 'generated':{mode:{p.name:sha(p) for p in sorted((out/('generated-'+mode)).glob('*')) if p.is_file()}
              for mode in ['original','observed']},
 'compiler':subprocess.check_output(['clang++','--version'],text=True),
 'scope':'current-main validation-only harness; canonical runtime and control source unchanged'}
(out/'build-identity.json').write_text(json.dumps(record,indent=2)+'\n')
PY
