#!/usr/bin/env bash
# Isolated, explicit closure experiment; never patches original files or gates.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 ]] || { echo 'usage: VERIFIED_PEDAL_BUILD NEW_OUTPUT_ROOT' >&2;exit 2; }
base="$(realpath "$1")";out="$(realpath -m "$2")";[[ ! -e "$out" ]];mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,out=map(Path,sys.argv[1:])
identity=json.loads((base/'pedal-build-identity.json').read_text())
for p,sha in identity['files'].items():assert hashlib.sha256((base/p).read_bytes()).hexdigest()==sha
s=(base/'validation-unit.cpp').read_text()
s='#include "ps2/cpu.hpp"\nextern void gt3_pedal_closure_probe(ps2::Cpu &,unsigned,unsigned);\n'+s
for pc in ['001E4D38','001E4D90','001E48FC','001E4BA8','001E4E68']:
 key='L_'+pc+':\n';assert s.count(key)==1
 s=s.replace(key,key+f'    gt3_pedal_closure_probe(c,0x{pc},depth);\n')
key='    { const std::uint32_t t = c.r[2].w[0]; c.r[31].sd[0] = static_cast<std::int32_t>(0x001E4D90u);'
assert s.count(key)==1;s=s.replace(key,'    gt3_pedal_closure_probe(c,0x001E4D88,depth);\n'+key)
(out/'closure-unit.cpp').write_text(s)
s=(root/'host/gt3_clean_pedals.cpp').read_text()
# Identical complete implementation prefix. Only a test-only body entry appended.
s+='\nvoid gt3_pedal_closure_body(ps2::Cpu &c,unsigned depth) {\n using namespace gt3::pedals;\n const auto car=c.r[23].w[0],command=c.r[18].w[0];\n Execution e{c,car,command,car+0x1304,depth};\n process(e,read<CarPartial>(car),read<CommandPartial>(command));\n}\n'
(out/'frozen-body.cpp').write_text(s)
PY
inc=(-I"$root/runtime/include" -I"$root/host" -I"$base/base/generated-observed")
clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 -c "$out/closure-unit.cpp" -o "$out/unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/frozen-body.cpp" -o "$out/body.o"
clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 "$root/tests/gt3_pedal_host.cpp" "$root/tests/gt3_pedal_closure_observer.cpp" "$out/unit.o" "$out/body.o" "$base/response-unit.o" "$base/base/observed/libps2game.a" "$base/base/original/libgt3_recovered.a" "$base/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/closure-shadow"
python3 - "$root" "$out" <<'PY'
import hashlib,json,sys
from pathlib import Path
root,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'identity.json').write_text(json.dumps({'source_hashes':{p:sha(root/p) for p in ['host/gt3_clean_pedals.cpp','host/gt3_clean_pedals.hpp','tests/gt3_pedal_closure_observer.cpp','scripts/build_gt3_pedal_closure.sh']},'files':{p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='build.log'}},indent=2)+'\n')
PY
