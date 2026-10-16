#!/usr/bin/env python3
"""Additive helper oracle, then explicitly gated pair build. No old files edited."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
ELF=ROOT/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf'
CORE=['host/gt3_clean_transmission_speed.cpp','host/gt3_clean_transmission_speed.hpp',
      'tests/gt3_transmission_speed_oracle.cpp','scripts/validate_gt3_transmission_speed.py']


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def preflight(base):
    module('old_validation',ROOT/'scripts/validate_gt3_transmission.py').preflight(base)
    old=module('frozen_selector',ROOT/'scripts/project/transmission.py')
    old.check_record(json.loads(old.DB.read_text()))
    v=json.loads((base/'build-identity.json').read_text())
    assert v['source_commit']=='82987dec7a71d76414adfff8663da5494a280938'
    for p,h in v['inputs_and_executables'].items():assert sha(Path(p))==h,p
    for p,h in v['generated']['original'].items():assert sha(base/'generated-original'/p)==h,p
    for p,h in v['source_hashes'].items():
        if p.startswith(('host/','runtime/')) and Path(p).suffix in ('.cpp','.hpp'):assert sha(ROOT/p)==h,p
    return v

def run(args,log=None,env=None):
    if log:
        with log.open('x') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=f,check=True,env=env)
    else:subprocess.run(list(map(str,args)),check=True,env=env)

def identity(out,base,paths,extra):
    data=dict(base=str(base),baseline_identity_sha256=sha(base/'build-identity.json'),
              sources={p:sha(ROOT/p) for p in paths},files={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()},**extra)
    (out/'identity.json').write_text(json.dumps(data,indent=2)+'\n')

def build(base,out):
    preflight(base);out.mkdir(parents=True,exist_ok=False)
    text=(base/'generated-original/unit_0039.cpp').read_text()
    oracle=text.replace('void unit_0039(','void oracle_unit_0039(').replace('unit_0039(c,','oracle_unit_0039(c,').replace('entries_0039','oracle_entries_0039')
    assert oracle.replace('oracle_unit_0039','unit_0039').replace('oracle_entries_0039','entries_0039')==text
    (out/'oracle-unit.cpp').write_text(oracle)
    inc=['-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include'),'-I'+str(base/'generated-original')]
    cc=['clang++','-std=c++20','-O2',*inc]
    run([*cc,'-c',ROOT/'host/gt3_clean_transmission_speed.cpp','-o',out/'helper.o'])
    run([*cc,'-c',ROOT/'host/gt3_clean_transmission.cpp','-o',out/'frozen-selector.o'])
    run([*cc,'-c',out/'oracle-unit.cpp','-o',out/'oracle-unit.o'])
    libs=[base/'original/libps2game.a',base/'original/libgt3_recovered.a',base/'original/libps2runtime.a',ROOT/'third_party/wgpu-native/lib/libwgpu_native.a','-ldl','-lpthread','-lm']
    run([*cc,ROOT/'tests/gt3_transmission_speed_oracle.cpp',out/'helper.o',out/'oracle-unit.o',*libs,'-Wl,--wrap=_ZN3ps27preemptERNS_3CpuE','-o',out/'oracle'])
    run([out/'oracle',ELF],out/'oracle.log')
    identity(out,base,CORE+['host/gt3_clean_transmission.cpp','host/gt3_clean_transmission.hpp'],dict(stage='independent-helper-passing',canonical_installation=False))

def integrate(base,isolated,out,gate):
    preflight(base);i=json.loads((isolated/'identity.json').read_text())
    for p,h in i['sources'].items():assert sha(ROOT/p)==h,p
    for p,h in i['files'].items():assert sha(isolated/p)==h,p
    assert i['baseline_identity_sha256']==sha(base/'build-identity.json')
    out.mkdir(parents=True,exist_ok=False)
    run([isolated/'oracle',ELF],out/'independent-oracle-rerun.log')
    original=(base/'generated-original/unit_0039.cpp').read_text();s=original
    s=s.replace('#include "units.hpp"','#include "units.hpp"\n#include "gt3_clean_transmission.hpp"\n#include "gt3_clean_transmission_speed.hpp"\nnamespace gt3::speed_validation {extern unsigned depth;}',1)
    # Label entry, not just dispatch registration: direct generated calls reach it.
    begin=s.index('L_001E4E80:\n');end=s.index('L_001E4F10:\n',begin);body=s[begin:end]
    assert body.count(' c.pc = t; return; }')==3
    body=body.replace(' c.pc = t; return; }',' c.pc = t; ps2::probe(c,0xe4e80000u); return; }')
    body=body.replace('L_001E4E80:\n','L_001E4E80:\n    gt3::speed_validation::depth=depth;ps2::probe(c,0x1e4e80);\n#if GT3_ENABLE_SPEED_PAIR\n    if(gt3::transmission_speed::replace(c)){ps2::probe(c,0xe4e80000u);return;}\n#endif\n',1)
    s=s[:begin]+body+s[end:]
    assert s.count('L_001E5458:\n')==s.count('L_001E5730:\n')==1
    s=s.replace('L_001E5458:\n','L_001E5458:\n    gt3::speed_validation::depth=depth;ps2::probe(c,0x1e5458);\n#if GT3_ENABLE_SPEED_PAIR\n    if(gt3::transmission::replace_manual_selector(c,depth))return;\n#endif\n',1)
    s=s.replace('L_001E5730:\n','L_001E5730:\n    ps2::probe(c,0x1e5730);\n',1)
    (out/'unit_0039.cpp').write_text(s)
    host=(ROOT/'host/main.cpp').read_text()
    host=host.replace('#include <vector>','#include <vector>\n#include "gt3_transmission_speed_host.inc"',1)
    needle='        if (a == "--arg" && i + 1 < argc)';assert host.count(needle)==1
    host=host.replace(needle,'        if(a=="--gt3-clean-transmission") {if(!GT3_ENABLE_SPEED_PAIR)return usage();gt3::transmission::enabled=true;}\n        else if(a=="--gt3-clean-speed") {if(!GT3_ENABLE_SPEED_PAIR)return usage();gt3::transmission_speed::enabled=true;}\n        else if(a=="--gt3-speed-shadow")speed_shadow=true;\n        else if (a == "--arg" && i + 1 < argc)',1)
    host=host.replace('    if (gt3_triple) {','    if(gt3_triple || !ram_words.empty() || !ps2::g_options.axes.empty())return usage();\n    speed_install();\n    if (gt3_triple) {',1)
    (out/'host.cpp').write_text(host)
    inc=['-I'+str(ROOT/'host'),'-I'+str(ROOT/'tests'),'-I'+str(ROOT/'runtime/include'),'-I'+str(base/'generated-original')]
    cc=['clang++','-std=c++20','-O2',*inc,'-DGT3_ENABLE_SPEED_PAIR='+str(int(gate))]
    run([*cc,'-c',out/'unit_0039.cpp','-o',out/'unit.o'])
    objects=[out/'unit.o',isolated/'helper.o',isolated/'frozen-selector.o',isolated/'oracle-unit.o',ROOT/'tests/gt3_transmission_speed_context.cpp']
    libs=[base/'original/libps2game.a',base/'original/libgt3_recovered.a',base/'original/libps2runtime.a',ROOT/'third_party/wgpu-native/lib/libwgpu_native.a','-ldl','-lpthread','-lm']
    run([*cc,out/'host.cpp',*objects,*libs,'-o',out/'ps2run'])
    if gate:
        run([*cc,ROOT/'tests/gt3_transmission_speed_composition.cpp',*objects,*libs,'-o',out/'composition'])
        run([out/'composition',ELF],out/'composition.log')
        for label,source in [('selector','tests/gt3_transmission_oracle.cpp'),('consumer','tests/gt3_transmission_wrapper.cpp')]:
            run([*cc,ROOT/source,ROOT/'tests/gt3_transmission_speed_frozen_driver.cpp',*objects,*libs,'-o',out/label])
            for pair in [0,1]:run([out/label,ELF],out/f'{label}-pair{pair}.log',dict(os.environ,GT3_SPEED_PAIR_TEST=str(pair)))
    paths=CORE+['host/gt3_clean_transmission.cpp','host/gt3_clean_transmission.hpp','host/main.cpp',
        'tests/gt3_transmission_speed_host.inc','tests/gt3_transmission_speed_context.cpp',
        'tests/gt3_transmission_speed_composition.cpp','tests/gt3_transmission_speed_frozen_driver.cpp',
        'tests/gt3_transmission_oracle.cpp','tests/gt3_transmission_wrapper.cpp']
    identity(out,base,paths,dict(stage='integrated-passing' if gate else 'build-off',build_gate=gate,runtime_default=False,canonical_installation=False,isolated=str(isolated),isolated_identity_sha256=sha(isolated/'identity.json')))

def source():
    with tempfile.TemporaryDirectory(prefix='gt3-speed-source-') as d:
        binary=Path(d)/'source-test'
        run(['clang++','-std=c++20','-O2','-Wall','-Wextra','-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include'),ROOT/'host/gt3_clean_transmission_speed.cpp',ROOT/'tests/gt3_transmission_speed_source_test.cpp','-o',binary]);run([binary])

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('source');b=sub.add_parser('build');b.add_argument('baseline',type=Path);b.add_argument('output',type=Path)
    i=sub.add_parser('integrate');i.add_argument('baseline',type=Path);i.add_argument('isolated',type=Path);i.add_argument('output',type=Path);i.add_argument('--enable-clean',action='store_true')
    a=p.parse_args()
    if a.command=='source':source()
    elif a.command=='build':build(a.baseline.resolve(strict=True),a.output.resolve())
    else:integrate(a.baseline.resolve(strict=True),a.isolated.resolve(strict=True),a.output.resolve(),a.enable_clean)

if __name__=='__main__':main()
