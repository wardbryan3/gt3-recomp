#!/usr/bin/env bash
# Additive disposable full-function entry overlay. Default build gate OFF.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 3 || ( $# == 4 && "$4" == --enable-clean-transmission ) ]] || { echo 'usage: VERIFIED_BASELINE ISOLATED_BUILD NEW_OUTPUT [--enable-clean-transmission]'; exit 2; }
base="$(realpath "$1")"; iso="$(realpath "$2")"; out="$(realpath -m "$3")"; gate=0; [[ $# == 3 ]] || gate=1
[[ ! -e "$out" ]]; mkdir -p "$out"; exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$iso" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,iso=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((base/'build-identity.json').read_text());i=json.loads((iso/'identity.json').read_text())
for p,h in v['inputs_and_executables'].items():assert sha(Path(p))==h,p
for p,h in v['generated']['original'].items():assert sha(base/'generated-original'/p)==h,p
for p,h in v['source_hashes'].items():
 if p.startswith(('host/','runtime/')) and Path(p).suffix in ('.cpp','.hpp'):assert sha(root/p)==h,p
for p,h in i['sources'].items():assert sha(root/p)==h,p
for p,h in i['files'].items():assert sha(iso/p)==h,p
assert json.loads((iso/'parent-identity.json').read_text())['baseline_identity_sha256']==sha(base/'build-identity.json')
PY
# Freshly execute the independent original oracle BEFORE making a runtime gate.
"$iso/oracle" "$root/local/legacy/resolution-repo/games/gt3-usa-v110/core.elf" | tee "$out/pre-integration-oracle.log"
python3 - "$root" "$base" "$out" "$gate" <<'PY'
from pathlib import Path
import sys,json,hashlib
root,base,out=map(Path,sys.argv[1:4]);gate=int(sys.argv[4]);s=(base/'generated-original/unit_0039.cpp').read_text()
s=s.replace('#include "units.hpp"','#include "units.hpp"\n#include "gt3_clean_transmission.hpp"\nnamespace gt3::transmission_validation { extern unsigned entry_depth; }',1)
assert s.count('L_001E5458:\n')==s.count('L_001E5730:\n')==1
s=s.replace('L_001E5458:\n','L_001E5458:\n    gt3::transmission_validation::entry_depth=depth;\n    ps2::probe(c,0x001e5458);\n#if GT3_ENABLE_CLEAN_TRANSMISSION\n    if(gt3::transmission::replace_manual_selector(c,depth))return;\n#endif\n',1)
s=s.replace('L_001E5730:\n','L_001E5730:\n    ps2::probe(c,0x001e5730);\n',1);(out/'unit_0039.cpp').write_text(s)
h=(root/'host/main.cpp').read_text();assert h.count('#include <vector>')==1
h=h.replace('#include <vector>','#include <vector>\n#include "gt3_transmission_host.inc"',1)
needle='        if (a == "--arg" && i + 1 < argc)';assert h.count(needle)==1
h=h.replace(needle,'        if(a=="--gt3-clean-transmission") { if(!GT3_ENABLE_CLEAN_TRANSMISSION)return usage(); gt3::transmission::enabled=true; }\n        else if(a=="--gt3-transmission-shadow")transmission_shadow=true;\n        else if (a == "--arg" && i + 1 < argc)',1)
assert h.count('    if (gt3_triple) {')==1
h=h.replace('    if (gt3_triple) {','    if(gt3_triple || !ram_words.empty() || !ps2::g_options.axes.empty())return usage();\n    transmission_install();\n    if (gt3_triple) {',1)
(out/'host.cpp').write_text(h)
(out/'gate.json').write_text(json.dumps({'build_gate':bool(gate),'runtime_default':False,'canonical_installation':False,'overlay':'whole001E5458..001E553B; original001E4E80 unchanged','probe_sites':['001E5458','001E5730']},indent=2)+'\n')
PY
inc=(-I"$root/host" -I"$root/tests" -I"$root/runtime/include" -I"$base/generated-original")
clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_ENABLE_CLEAN_TRANSMISSION=$gate -c "$out/unit_0039.cpp" -o "$out/unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" -DGT3_ENABLE_CLEAN_TRANSMISSION=$gate "$out/host.cpp" "$out/unit.o" "$iso/clean.o" "$iso/oracle-unit.o" "$base/original/libps2game.a" "$base/original/libgt3_recovered.a" "$base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/ps2run"
if [[ "$gate" == 1 ]]; then
  clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_transmission_wrapper.cpp" "$out/unit.o" "$iso/clean.o" "$iso/oracle-unit.o" "$base/original/libps2game.a" "$base/original/libgt3_recovered.a" "$base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/wrapper"
  "$out/wrapper" "$root/local/legacy/resolution-repo/games/gt3-usa-v110/core.elf" | tee "$out/wrapper.log"
fi
python3 - "$root" "$base" "$iso" "$out" <<'PY'
from pathlib import Path
import sys,hashlib,json
root,base,iso,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'identity.json').write_text(json.dumps({'baseline':str(base),'isolated':str(iso),'baseline_identity_sha256':sha(base/'build-identity.json'),'isolated_identity_sha256':sha(iso/'identity.json'),'sources':{p:sha(root/p) for p in ['host/main.cpp','tests/gt3_transmission_host.inc','tests/gt3_transmission_wrapper.cpp','scripts/build_gt3_transmission_live.sh']},'files':{p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='build.log'}},indent=2)+'\n')
PY
