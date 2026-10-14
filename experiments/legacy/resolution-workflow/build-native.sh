#!/usr/bin/env bash
# New project outputs only. Never rebuild an earlier known-good experiment in-place.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"; cd "$root"
export PATH="/home/b/experiments/gt3-native-20261013/toolchain/bin:$PATH"
mode="${1:?generated or clean}"
[[ "$mode" == generated || "$mode" == clean ]] || exit 2
sha256sum -c build/project-init/preservation.sha256
mkdir -p build/foundation/tools build/foundation/tmp
export TMPDIR="$root/build/foundation/tmp"
if [[ "$mode" == generated ]]; then
 cmake -S . -B build/foundation/tools -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++
 cmake --build build/foundation/tools --target eerecomp vurecomp -j 8
 build/foundation/tools/eerecomp games/gt3-usa-v110/core-triple.elf --entries games/gt3-usa-v110/entries.txt --probes scripts/gt3_wheel.probes --out build/foundation/generated-source
 build/foundation/tools/vurecomp games/gt3-usa-v110/vu1 build/foundation/generated-source
else
 [[ -f build/foundation/generated-source/table.cpp ]] || { echo 'Run just build-generated first' >&2; exit 1; }
 python3 - <<'PY'
import pathlib,shutil,json
src=pathlib.Path('build/foundation/generated-source'); dst=pathlib.Path('build/foundation/clean-source'); dst.mkdir(parents=True,exist_ok=True)
for p in src.iterdir():
 if p.is_file() and p.suffix in ('.cpp','.hpp','.h'): shutil.copy2(p,dst/p.name)
manifest=json.loads(pathlib.Path('decomp/gt3/manifest.json').read_text())
for f in manifest['functions']:
 if f['lifecycle']!='frozen': continue
 address=f['gate_address'][2:].upper().zfill(8)
 candidates=[p for p in dst.glob('unit_*.cpp') if ('L_'+address+':\n') in p.read_text()]
 assert len(candidates)==1, (address,candidates)
 p=candidates[0]; s=p.read_text(); include='#include "gt3_clean_steering.hpp"\n'
 if not s.startswith(include): s=include+s
 target=f.get('resume_address'); action='goto L_'+target[2:].upper().zfill(8)+';' if target else 'return;'
 key='L_'+address+':\n'; assert s.count(key)==1
 s=s.replace(key,key+f'    if (gt3::clean::replace(c, 0x{address}u)) {{ {action} }}\n');p.write_text(s)
PY
fi
source="$root/build/foundation/generated-source"; clean=OFF
if [[ "$mode" == clean ]]; then source="$root/build/foundation/clean-source"; clean=ON; fi
[[ "$source" != "$root/build/foundation/$mode" ]] # source/build trees must never collide
cmake -S . -B "build/foundation/$mode" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ \
 -DPS2_GENERATED="$source" -DPS2_GT3_SYNTHETIC_WHEEL=ON -DPS2_GT3_CLEAN_STEERING="$clean"
cmake --build "build/foundation/$mode" --target ps2run -j 8
sha256sum -c build/project-init/preservation.sha256
