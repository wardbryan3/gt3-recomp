#!/usr/bin/env bash
# Disposable handbrake-only unit overlay; no canonical or Frozen source edits.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 || $# == 3 ]] || { echo 'usage: VERIFIED_PEDAL_BUILD NEW_OUTPUT [--enable-clean-handbrake]';exit 2; }
gate=0
if [[ $# == 3 ]];then [[ "$3" == --enable-clean-handbrake ]] || exit 2;gate=1;fi
base="$(realpath "$1")";out="$(realpath -m "$2")";[[ ! -e "$out" ]];mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((base/'pedal-build-identity.json').read_text())
for p,h in v['files'].items():assert sha(base/p)==h,p
v=json.loads((base/'base/build-identity.json').read_text())
for p,h in v['source_hashes'].items():
 if Path(p).suffix in ('.cpp','.hpp'):assert sha(root/p)==h,p
# Truly original oracle: no clean includes/gates. Exact entry and stop only.
s=(base/'base/generated-original/unit_0039.cpp').read_text()
s='extern bool gt3_handbrake_audit_stop;\n'+s
key='switch (entry) {';assert s.count(key)==1
s=s.replace(key,key+'\n    case 60000u: goto L_001E4BB8;')
key='L_001E4C60:\n';assert s.count(key)==1
s=s.replace(key,key+'    if(gt3_handbrake_audit_stop){c.pc=0x1e4c60;return;}\n')
(out/'oracle-unit.cpp').write_text(s)
s=(base/'validation-unit.cpp').read_text()
s='#include "gt3_clean_handbrake.hpp"\n'+s
key='    c.r[31].d[0] = ld64((c.r[29].w[0] + 48u));\n    c.r[18].d[0]'
start=s.index('L_001E6FB4:\n');end=s.index('L_001E6FE0:\n',start)
part=s[start:end];assert part.count(key)==1
s=s[:start]+part.replace(key,'L_001E6FC8:\n'+key)+s[end:]
for address in ['001E4BB8','001E4C60','001E6FC8','001E5E1C','001E5EAC']:
 key='L_'+address+':\n';assert s.count(key)==1
 extra=f'    ps2::probe(c,0x{address}u);\n'
 if address=='001E4BB8':extra+='#if GT3_HANDBRAKE_VALIDATION_GATES\n    if(gt3::handbrake::replace(c,depth))goto L_001E4C60;\n#endif\n'
 s=s.replace(key,key+extra)
(out/'handbrake-unit.cpp').write_text(s)
# Read-only observations of the existing handbrake comparison at the shift
# interface. No shift instructions, helpers, policy, or dispatch are replaced.
s=(base/'base/generated-observed/unit_0038.cpp').read_text()
for address in ['001E3A90','001E3AAC','001E3AB8']:
 key='L_'+address+':\n';assert s.count(key)==1
 s=s.replace(key,key+f'    ps2::probe(c,0x{address}u);\n')
(out/'consumer-unit.cpp').write_text(s)
# Reuse canonical host and unchanged steering support, but never enable pedals.
s=(root/'tests/gt3_pedal_host.cpp').read_text()
s='#include "gt3_clean_handbrake.hpp"\nvoid handbrake_probe(ps2::Cpu &,unsigned,std::uint64_t);\n'+s
s=s.replace('int main(','int pedal_validation_host_main(')
key='        experiment.probe(cpu,pc,ps2::frame_count());';assert s.count(key)==1
s=s.replace(key,key+'\n        handbrake_probe(cpu,pc,ps2::frame_count());')
s+='\n#include "'+str(root/'tests/gt3_handbrake_host.inc')+'"\n'
(out/'handbrake-host.cpp').write_text(s)
PY
inc=(-I"$root/host" -I"$root/runtime/include" -iquote "$root/tests" -I"$base/base/generated-observed")
libs=("$base/base/original/libgt3_recovered.a" "$base/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm)
clang++ -std=c++20 -O2 "${inc[@]}" -c "$root/host/gt3_clean_handbrake.cpp" -o "$out/clean.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/oracle-unit.cpp" -o "$out/oracle-unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/consumer-unit.cpp" -o "$out/consumer-unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_handbrake_oracle.cpp" "$out/clean.o" "$out/oracle-unit.o" "$base/base/original/libps2game.a" "${libs[@]}" -o "$out/oracle"
for mode in off on;do
 enabled=0;[[ "$mode" != on ]] || { [[ "$gate" == 1 ]] || continue;enabled=1; }
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 -DGT3_HANDBRAKE_VALIDATION_GATES="$enabled" -c "$out/handbrake-unit.cpp" -o "$out/unit-$mode.o"
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES=0 -DGT3_HANDBRAKE_VALIDATION_GATES="$enabled" "$out/handbrake-host.cpp" "$out/clean.o" "$out/unit-$mode.o" "$out/consumer-unit.o" "$base/response-unit.o" "$base/base/observed/libps2game.a" "${libs[@]}" -o "$out/handbrake-$mode"
done
if [[ "$gate" == 1 ]];then
 clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_handbrake_wrapper.cpp" "$out/clean.o" "$out/unit-on.o" "$base/response-unit.o" "$base/base/observed/libps2game.a" "${libs[@]}" -o "$out/wrapper"
fi
python3 - "$root" "$base" "$out" "$gate" <<'PY'
import hashlib,json,sys,subprocess
from pathlib import Path
root,base,out=map(Path,sys.argv[1:4]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'identity.json').write_text(json.dumps({'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'build_opt_in':sys.argv[4]=='1','runtime_default':False,'canonical_gate':False,'parent_build':str(base),
 'parent_identity_sha256':sha(base/'pedal-build-identity.json'),
 'sources':{p:sha(root/p) for p in ['host/gt3_clean_handbrake.cpp','host/gt3_clean_handbrake.hpp','tests/gt3_handbrake_host.inc','tests/gt3_handbrake_oracle.cpp','tests/gt3_handbrake_wrapper.cpp','scripts/build_gt3_handbrake.sh']},
 'files':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='build.log'}},indent=2)+'\n')
PY
