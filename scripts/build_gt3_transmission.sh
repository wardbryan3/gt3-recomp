#!/usr/bin/env bash
# One isolated MT-selector recovery. No canonical or Frozen file is edited.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
[[ $# == 2 ]] || { echo 'usage: VERIFIED_BASELINE_BUILD NEW_OUTPUT'; exit 2; }
base="$(realpath "$1")"; out="$(realpath -m "$2")"; [[ ! -e "$out" ]]; mkdir -p "$out"
exec > >(tee "$out/build.log") 2>&1
python3 - "$root" "$base" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,base,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((base/'build-identity.json').read_text())
for p,h in v['inputs_and_executables'].items():assert sha(Path(p))==h,p
for p,h in v['generated']['original'].items():assert sha(base/'generated-original'/p)==h,p
for p,h in v['source_hashes'].items():
 if p.startswith(('host/','runtime/')) and Path(p).suffix in ('.cpp','.hpp'):assert sha(root/p)==h,p
s=(base/'generated-original/unit_0039.cpp').read_text()
# Original instructions/control flow unchanged. Separate symbol/self-calls permit
# an independent original oracle alongside a later disposable guarded overlay.
assert s.count('void unit_0039(')==1
oracle=s.replace('void unit_0039(','void oracle_unit_0039(').replace('unit_0039(c,','oracle_unit_0039(c,').replace('entries_0039','oracle_entries_0039')
assert oracle.replace('oracle_unit_0039','unit_0039').replace('oracle_entries_0039','entries_0039')==s
(out/'oracle-unit.cpp').write_text(oracle)
(out/'parent-identity.json').write_text(json.dumps({'baseline_identity_sha256':sha(base/'build-identity.json'),'baseline_source_commit':v['source_commit'],'source_commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'canonical_installation':False,'runtime_default':False,'baseline':str(base)},indent=2)+'\n')
PY
inc=(-I"$root/host" -I"$root/runtime/include" -I"$base/generated-original")
clang++ -std=c++20 -O2 -Wall -Wextra "${inc[@]}" -c "$root/host/gt3_clean_transmission.cpp" -o "$out/clean.o"
clang++ -std=c++20 -O2 "${inc[@]}" -c "$out/oracle-unit.cpp" -o "$out/oracle-unit.o"
clang++ -std=c++20 -O2 "${inc[@]}" "$root/tests/gt3_transmission_oracle.cpp" "$out/clean.o" "$out/oracle-unit.o" "$base/original/libps2game.a" "$base/original/libgt3_recovered.a" "$base/original/libps2runtime.a" "$root/third_party/wgpu-native/lib/libwgpu_native.a" -ldl -lpthread -lm -o "$out/oracle"
python3 - "$root" "$out" <<'PY'
from pathlib import Path
import hashlib,json,sys
root,out=map(Path,sys.argv[1:]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=['host/gt3_clean_transmission.hpp','host/gt3_clean_transmission.cpp','tests/gt3_transmission_oracle.cpp','scripts/build_gt3_transmission.sh']
(out/'identity.json').write_text(json.dumps({'sources':{p:sha(root/p) for p in paths},'files':{p.name:sha(p) for p in out.iterdir() if p.is_file() and p.name!='build.log'},'scope':'isolated-differential-build; no integration gate yet'},indent=2)+'\n')
PY
