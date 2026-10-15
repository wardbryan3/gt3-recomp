#!/usr/bin/env bash
# New experiment only; immutable existing pedal build supplies generated oracle.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 || $# == 3 ]] || { echo 'usage: VERIFIED_PEDAL_BUILD NEW_OUTPUT [--enable-virtual-pedals]';exit 2; }
gate=0
if [[ $# == 3 ]]; then [[ "$3" == --enable-virtual-pedals ]] || exit 2;gate=1;fi
base="$(realpath "$1")";out="$(realpath -m "$2")";[[ ! -e "$out" ]];mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((base/'pedal-build-identity.json').read_text());assert v['build_opt_in'] is True
for path,expected in v['files'].items():assert sha(base/path)==expected,path
# All compiled source already present when that build was made must still match.
v=json.loads((base/'base/build-identity.json').read_text())
for path,expected in v['source_hashes'].items():
 if Path(path).suffix in ('.cpp','.hpp'):assert sha(root/path)==expected,path
s=(base/'validation-unit.cpp').read_text();key='L_001E4E68:\n';assert s.count(key)==1
s=s.replace(key,key+'    ps2::probe(c,0x001e4e68u);\n');(out/'virtual-unit.cpp').write_text(s)
s=(root/'tests/gt3_pedal_host.cpp').read_text();assert s.count('int main(')==1
s=s.replace('int main(','int pedal_validation_host_main(')
key='        experiment.probe(cpu,pc,ps2::frame_count());';assert s.count(key)==1
s=s.replace(key,key+'\n        gt3_virtual_probe(cpu,pc,ps2::frame_count());')
s='#include "gt3_virtual_pedals.hpp"\nvoid gt3_virtual_probe(ps2::Cpu &,unsigned,std::uint64_t);\n'+s
s+='\n#include "'+str(root/'tests/gt3_virtual_pedals_host.inc')+'"\n';(out/'virtual-host.cpp').write_text(s)
PY
inc=(-I"$root/host" -I"$root/runtime/include" -iquote "$root/tests" -I"$base/base/generated-observed")
clang++ -std=c++20 -O2 "${inc[@]}" -c "$root/host/gt3_virtual_pedals.cpp" -o "$out/adapter.o"
for mode in off on; do
 enabled=0;[[ "$mode" != on ]] || { [[ "$gate" == 1 ]] || continue;enabled=1; }
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$enabled" -c "$out/virtual-unit.cpp" -o "$out/unit-$mode.o"
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$enabled" -DGT3_VIRTUAL_PEDAL_GATE="$enabled" "$out/virtual-host.cpp" "$out/adapter.o" "$out/unit-$mode.o" "$base/response-unit.o" "$base/base/observed/libps2game.a" "$base/base/original/libgt3_recovered.a" "$base/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/virtual-$mode"
done
python3 - "$root" "$base" "$out" "$gate" <<'PY'
import hashlib,json,sys,subprocess
from pathlib import Path
root,base,out=map(Path,sys.argv[1:4]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'identity.json').write_text(json.dumps({'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'build_opt_in':sys.argv[4]=='1','runtime_default':False,'canonical_gate':False,'parent_build':str(base),
 'parent_identity_sha256':sha(base/'pedal-build-identity.json'),
 'sources':{p:sha(root/p) for p in ['host/gt3_virtual_pedals.cpp','host/gt3_virtual_pedals.hpp','tests/gt3_virtual_pedals_host.inc','scripts/build_gt3_virtual_pedals.sh']},
 'files':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='build.log'}},indent=2)+'\n')
PY
