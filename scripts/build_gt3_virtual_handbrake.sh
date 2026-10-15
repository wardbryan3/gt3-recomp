#!/usr/bin/env bash
# Isolated input overlay over the immutable, verified Frozen handbrake build.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 || $# == 3 ]] || { echo 'usage: VERIFIED_HANDBRAKE_BUILD NEW_OUTPUT [--enable-virtual-handbrake]';exit 2; }
gate=0
if [[ $# == 3 ]];then [[ "$3" == --enable-virtual-handbrake ]] || exit 2;gate=1;fi
base="$(realpath "$1")";out="$(realpath -m "$2")";[[ ! -e "$out" ]];mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((base/'identity.json').read_text());assert v['build_opt_in'] and not v['runtime_default'] and not v['canonical_gate']
for p,h in v['files'].items():assert sha(base/p)==h,p
for p,h in v['sources'].items():assert sha(root/p)==h,p
s=(base/'handbrake-unit.cpp').read_text();key='L_001E4E68:\n';assert s.count(key)==1
s=s.replace(key,key+'    ps2::probe(c,0x001e4e68u);\n');(out/'virtual-unit.cpp').write_text(s)
s=(base/'handbrake-host.cpp').read_text()
key='        handbrake_probe(cpu,pc,ps2::frame_count());';assert s.count(key)==1
s=s.replace(key,key+'\n        virtual_handbrake_probe(cpu,pc,ps2::frame_count());')
key='#include "'+str(root/'tests/gt3_handbrake_host.inc')+'"';assert s.count(key)==1
s=s.replace(key,'#define main handbrake_validation_host_main\n'+key+'\n#undef main')
s='#include "gt3_virtual_handbrake.hpp"\nvoid virtual_handbrake_probe(ps2::Cpu &,unsigned,std::uint64_t);\n'+s
s+='\n#include "'+str(root/'tests/gt3_virtual_handbrake_host.inc')+'"\n';(out/'virtual-host.cpp').write_text(s)
PY
parent="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["parent_build"])' "$base/identity.json")"
inc=(-I"$root/host" -I"$root/runtime/include" -iquote "$root/tests" -I"$parent/base/generated-observed")
libs=("$base/clean.o" "$base/consumer-unit.o" "$parent/response-unit.o" "$parent/base/observed/libps2game.a" "$parent/base/original/libgt3_recovered.a" "$parent/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm)
clang++ -std=c++20 -O2 "${inc[@]}" -c "$root/host/gt3_virtual_handbrake.cpp" -o "$out/adapter.o"
for mode in off on;do
 enabled=0;[[ "$mode" != on ]] || { [[ "$gate" == 1 ]] || continue;enabled=1; }
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 -DGT3_HANDBRAKE_VALIDATION_GATES="$enabled" -c "$out/virtual-unit.cpp" -o "$out/unit-$mode.o"
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 -DGT3_HANDBRAKE_VALIDATION_GATES="$enabled" -DGT3_VIRTUAL_HANDBRAKE_GATE="$enabled" "$out/virtual-host.cpp" "$out/adapter.o" "$out/unit-$mode.o" "${libs[@]}" -o "$out/virtual-$mode"
done
if [[ "$gate" == 1 ]];then
 clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_virtual_handbrake_oracle.cpp" "$out/adapter.o" "$out/unit-on.o" "${libs[@]}" -o "$out/oracle"
fi
python3 - "$root" "$base" "$out" "$gate" <<'PY'
import hashlib,json,sys,subprocess
from pathlib import Path
root,base,out=map(Path,sys.argv[1:4]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'identity.json').write_text(json.dumps(dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 build_opt_in=sys.argv[4]=='1',runtime_default=False,canonical_gate=False,parent_build=str(base),parent_identity_sha256=sha(base/'identity.json'),
 sources={p:sha(root/p) for p in ['host/gt3_virtual_handbrake.cpp','host/gt3_virtual_handbrake.hpp','tests/gt3_virtual_handbrake_host.inc','tests/gt3_virtual_handbrake_oracle.cpp','tests/gt3_virtual_handbrake_samples.hpp','scripts/build_gt3_virtual_handbrake.sh']},
 files={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='build.log'}),indent=2)+'\n')
PY
