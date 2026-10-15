#!/usr/bin/env bash
# Fresh current-main baseline plus disposable validation-only pedal translations.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# != 2 && $# != 3 ]]; then
 echo "usage: $0 ORIGINAL_INPUT_ROOT NEW_OUTPUT_ROOT [--enable-validation-pedal-substitution]" >&2;exit 2
fi
enabled=0
if [[ $# == 3 ]]; then
 [[ "$3" == --enable-validation-pedal-substitution ]] || exit 2;enabled=1
fi
input="$(realpath "$1")";out="$(realpath -m "$2")"
[[ ! -e "$out" ]] || { echo "output exists: $out" >&2;exit 1; }
mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
"$root/scripts/build_gt3_baseline.sh" "$input" "$out/base"
python3 - "$root" "$out" <<'PY'
from pathlib import Path
import sys
root,out=map(Path,sys.argv[1:])
# Independent ORIGINAL-only exact-entry oracle; no clean header or gate.
s=(out/'base/generated-original/unit_0039.cpp').read_text()
s='extern bool gt3_pedal_audit_stop;\n'+s
assert s.count('switch (entry) {')==1
s=s.replace('switch (entry) {','switch (entry) {\n    case 60000u: goto L_001E48FC;')
key='L_001E4BA8:\n';assert s.count(key)==1
s=s.replace(key,key+'    if (gt3_pedal_audit_stop) { c.pc=0x001E4BA8; return; }\n')
(out/'audit-unit.cpp').write_text(s)
# Normal observed translation retains ALL original instructions and four frozen
# steering gates. New pedal gate is compiled out unless separately requested.
s=(out/'base/generated-observed/unit_0039.cpp').read_text()
s='#include "gt3_clean_pedals.hpp"\n'+s
for address in ['001E48FC','001E4BA8','001E4C74','001E6EC8','001E7500']:
 key='L_'+address+':\n';assert s.count(key)==1
 extra=f'    ps2::probe(c, 0x{address}u);\n'
 if address=='001E48FC':
  extra+='#if GT3_PEDAL_VALIDATION_GATES\n    if (gt3::pedals::replace(c, depth)) goto L_001E4BA8;\n#endif\n'
 s=s.replace(key,key+extra)
(out/'validation-unit.cpp').write_text(s)
s=(out/'base/generated-observed/unit_0036.cpp').read_text()
key='L_001D92E0:\n';assert s.count(key)==1
s=s.replace(key,key+'    ps2::probe(c, 0x001D92E0u);\n')
(out/'response-unit.cpp').write_text(s)
PY
inc=(-I"$root/runtime/include" -I"$root/host" -I"$out/base/generated-observed")
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/audit-unit.cpp" -o "$out/audit-unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/response-unit.cpp" -o "$out/response-unit.o"
libs=("$out/base/original/libgt3_recovered.a" "$out/base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm)
for mode in original differential; do
 defs=();[[ "$mode" != differential ]] || defs=(-DGT3_PEDAL_DIFFERENTIAL)
 clang++ -std=c++20 -O2 "${inc[@]}" "${defs[@]}" "$root/tests/gt3_pedal_abi_audit.cpp" "$out/audit-unit.o" "$out/base/original/libps2game.a" "${libs[@]}" -o "$out/join-$mode"
 "$out/join-$mode" "$input/core.elf" > "$out/join-$mode.log" 2>&1
 done
for mode in off on; do
 gate=0;[[ "$mode" != on ]] || { [[ "$enabled" == 1 ]] || continue;gate=1; }
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$gate" -c "$out/validation-unit.cpp" -o "$out/pedal-$mode.o"
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_VALIDATION_GATES="$gate" "$root/tests/gt3_pedal_host.cpp" "$out/pedal-$mode.o" "$out/response-unit.o" "$out/base/observed/libps2game.a" "${libs[@]}" -o "$out/pedal-$mode"
done
if [[ "$enabled" == 1 ]]; then
 clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_PEDAL_DIFFERENTIAL "$root/tests/gt3_pedal_discovery.cpp" "$out/pedal-on.o" "$out/response-unit.o" "$out/base/observed/libps2game.a" "${libs[@]}" -o "$out/wrapper-differential"
 "$out/wrapper-differential" "$input/core.elf" > "$out/wrapper-differential.log" 2>&1
 clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_pedal_wrapper_test.cpp" "$out/pedal-on.o" "$out/response-unit.o" "$out/base/observed/libps2game.a" "${libs[@]}" -o "$out/wrapper-policy-differential"
 "$out/wrapper-policy-differential" "$input/core.elf" > "$out/wrapper-policy-differential.log" 2>&1
fi
python3 - "$root" "$out" "$enabled" <<'PY'
import hashlib,json,subprocess,sys
from pathlib import Path
root,out=map(Path,sys.argv[1:3]);enabled=sys.argv[3]=='1'
files=[p for p in out.iterdir() if p.is_file() and p.name!='build.log']
record={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'build_opt_in':enabled,'runtime_default':False,'canonical_gate':False,
 'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(out/'pedal-build-identity.json').write_text(json.dumps(record,indent=2)+'\n')
PY
