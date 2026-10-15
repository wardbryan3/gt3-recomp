#!/usr/bin/env bash
# Observation build only. Reuses verified Frozen archives; no runtime/source fork.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 ]] || { echo "usage: $0 VERIFIED_FROZEN_BUILD NEW_OUTPUT_ROOT" >&2;exit 2; }
base="$(realpath "$1")";out="$(realpath -m "$2")"
[[ ! -e "$out" ]] || { echo "output exists: $out" >&2;exit 1; }
mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
just -f "$root/justfile" verify-pedals "$root"
python3 - "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
base,out=map(Path,sys.argv[1:]);identity=json.loads((base/'pedal-build-identity.json').read_text())
assert identity['build_opt_in'] is True
for name,sha in identity['files'].items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==sha,name
for source,pc in [('validation-unit.cpp','001E48FC'),('response-unit.cpp','001D92E0')]:
 s=(base/source).read_text();s='extern void gt3_pedal_profile_observe(const ps2::Cpu &,unsigned);\n'+s
 # Declaration must follow includes so Cpu is declared; include its public header.
 s='#include "ps2/cpu.hpp"\n'+s
 sites=['001E48FC','001E4BA8'] if source.startswith('validation') else ['001D92E0']
 for address in sites:
  key='L_'+address+':\n';assert s.count(key)==1
  s=s.replace(key,key+f'    gt3_pedal_profile_observe(c,0x{address});\n')
 (out/source).write_text(s)
PY
inc=(-I"$root/runtime/include" -I"$root/host" -I"$base/base/generated-observed")
clang++ -std=c++20 -O2 "${inc[@]}" -c "$root/tests/gt3_pedal_profiles_observer.cpp" -o "$out/observer.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/response-unit.cpp" -o "$out/response.o"
for mode in off on; do
 gate=0;[[ "$mode" != on ]] || gate=1
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$gate" -c "$out/validation-unit.cpp" -o "$out/$mode.o"
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$gate" "$root/tests/gt3_pedal_host.cpp" "$out/$mode.o" "$out/response.o" "$out/observer.o" "$base/base/observed/libps2game.a" "$base/base/original/libgt3_recovered.a" "$base/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/survey-$mode"
done
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,subprocess,sys
root,base,out=map(Path,sys.argv[1:])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record={'scope':'read-only observation seams; unchanged Frozen archives and validation gates',
 'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'frozen_build_identity':{'path':str(base/'pedal-build-identity.json'),'sha256':sha(base/'pedal-build-identity.json')},
 'sources':{p:sha(root/p) for p in ['tests/gt3_pedal_profiles_observer.cpp','scripts/build_gt3_pedal_profiles.sh','tests/gt3_pedal_host.cpp','host/gt3_clean_pedals.cpp','host/gt3_clean_pedals.hpp']},
 'files':{str(p):sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='build.log'}}
(out/'identity.json').write_text(json.dumps(record,indent=2)+'\n')
PY
