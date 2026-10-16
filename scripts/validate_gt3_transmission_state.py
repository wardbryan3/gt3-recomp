#!/usr/bin/env python3
"""Isolated state oracle and native validation builder; canonical files untouched."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def run(args,log=None):
    if log:
        with log.open('x') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=f,check=True)
    else:subprocess.run(list(map(str,args)),check=True)
def build(base,out):
    old=load(ROOT/'scripts/validate_gt3_transmission_speed.py','speed_build');old.preflight(base)
    check=load(ROOT/'scripts/project/transmission_speed.py','speed_check');check.check_record(json.loads(check.DB.read_text()))
    out.mkdir(parents=True,exist_ok=False)
    source=(base/'generated-original/unit_0039.cpp').read_text()
    oracle=source.replace('void unit_0039(','void state_oracle_unit_0039(').replace('unit_0039(c,','state_oracle_unit_0039(c,').replace('entries_0039','state_oracle_entries_0039')
    assert oracle.replace('state_oracle_unit_0039','unit_0039').replace('state_oracle_entries_0039','entries_0039')==source
    (out/'oracle-unit.cpp').write_text(oracle)
    cc=['clang++','-std=c++20','-O2','-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include'),'-I'+str(base/'generated-original')]
    for name,path in [('oracle-unit',out/'oracle-unit.cpp'),('model',ROOT/'host/gt3_transmission_state.cpp'),('admission',ROOT/'host/gt3_clean_transmission_admission.cpp')]:run([*cc,'-c',path,'-o',out/(name+'.o')])
    libs=[base/'original/libps2game.a',base/'original/libgt3_recovered.a',base/'original/libps2runtime.a',ROOT/'third_party/wgpu-native/lib/libwgpu_native.a','-ldl','-lpthread','-lm']
    run([*cc,ROOT/'tests/gt3_transmission_state_oracle.cpp',*[out/(n+'.o') for n in ['oracle-unit','model','admission']],*libs,'-o',out/'oracle'])
    old.identity(out,base,['host/gt3_transmission_state.cpp','host/gt3_transmission_state.hpp','host/gt3_clean_transmission_admission.cpp','host/gt3_clean_transmission_admission.hpp','tests/gt3_transmission_state_oracle.cpp','scripts/validate_gt3_transmission_state.py'],dict(stage='built-not-yet-tested',canonical_installation=False))
    run([out/'oracle',old.ELF],out/'oracle.log')
def native(base,isolated,out,gate):
    old=load(ROOT/'scripts/validate_gt3_transmission_speed.py','speed_native');old.preflight(base)
    i=json.loads((isolated/'identity.json').read_text())
    for path,h in i['sources'].items():assert old.sha(ROOT/path)==h,path
    for path,h in i['files'].items():assert old.sha(isolated/path)==h,path
    out.mkdir(parents=True,exist_ok=False)
    run([isolated/'oracle',old.ELF],out/'independent-rerun.log')
    prior=ROOT/'local/transmission-speed-v1/on-attempt-1';pi=json.loads((prior/'identity.json').read_text())
    assert old.sha(prior/'unit_0039.cpp')==pi['files']['unit_0039.cpp']
    s=(prior/'unit_0039.cpp').read_text()
    s=s.replace('namespace gt3::speed_validation {extern unsigned depth;}','namespace gt3::speed_validation {extern unsigned depth;}\n#include "gt3_clean_transmission_admission.hpp"\nnamespace gt3::state_validation {extern unsigned depth;}')
    begin=s.index('L_001E6D48:\n');end=s.index('L_001E6EC8:\n',begin);body=s[begin:end]
    assert body.count(' c.pc = t; return; }')==1
    body=body.replace(' c.pc = t; return; }',' c.pc = t; ps2::probe(c,0x6d480000u); return; }')
    body=body.replace('L_001E6D48:\n','L_001E6D48:\n    gt3::state_validation::depth=depth; ps2::probe(c,0x1e6d48);\n#if GT3_ENABLE_STATE_ADMISSION\n    if(ps2::ld8(c.r[4].w[0]+0x136d)==0 && gt3::transmission_admission::replace(c,depth)){ps2::probe(c,0x6d480000u);return;}\n#endif\n')
    s=s[:begin]+body+s[end:]
    for pc in ['001E7500','001E755C','001E7590','001E77B4','001E77F8','001E783C']:
        assert s.count('L_'+pc+':\n')==1;s=s.replace('L_'+pc+':\n','L_'+pc+':\n    ps2::probe(c,0x'+pc+'u);\n')
    (out/'unit_0039.cpp').write_text(s)
    host=(ROOT/'host/main.cpp').read_text().replace('#include <vector>','#include <vector>\n#include "gt3_transmission_state_host.inc"',1)
    needle='        if (a == "--arg" && i + 1 < argc)';assert host.count(needle)==1
    host=host.replace(needle,'        if(a=="--gt3-clean-admission"){if(!GT3_ENABLE_STATE_ADMISSION)return usage();gt3::transmission_admission::enabled=true;}\n        else if(a=="--gt3-state-shadow")state_shadow=true;\n        else if(a=="--gt3-clean-transmission"){if(!GT3_ENABLE_SPEED_PAIR)return usage();gt3::transmission::enabled=true;}\n        else if(a=="--gt3-clean-speed"){if(!GT3_ENABLE_SPEED_PAIR)return usage();gt3::transmission_speed::enabled=true;}\n        else if(a=="--gt3-speed-shadow")speed_shadow=true;\n        else if (a == "--arg" && i + 1 < argc)',1)
    host=host.replace('    if (gt3_triple) {','    if(gt3_triple || !ram_words.empty() || !ps2::g_options.axes.empty())return usage();\n    state_install();\n    if (gt3_triple) {',1)
    (out/'host.cpp').write_text(host)
    cc=['clang++','-std=c++20','-O2','-I'+str(ROOT/'host'),'-I'+str(ROOT/'tests'),'-I'+str(ROOT/'runtime/include'),'-I'+str(base/'generated-original'),'-DGT3_ENABLE_STATE_ADMISSION='+str(int(gate)),'-DGT3_ENABLE_SPEED_PAIR='+str(int(gate))]
    for name,path in [('unit',out/'unit_0039.cpp'),('frozen-selector',ROOT/'host/gt3_clean_transmission.cpp'),('frozen-helper',ROOT/'host/gt3_clean_transmission_speed.cpp')]:run([*cc,'-c',path,'-o',out/(name+'.o')])
    speed_oracle=ROOT/'local/transmission-speed-v1/isolated-attempt-1/oracle-unit.o';si=json.loads((speed_oracle.parent/'identity.json').read_text());assert old.sha(speed_oracle)==si['files']['oracle-unit.o']
    libs=[base/'original/libps2game.a',base/'original/libgt3_recovered.a',base/'original/libps2runtime.a',ROOT/'third_party/wgpu-native/lib/libwgpu_native.a','-ldl','-lpthread','-lm']
    run([*cc,out/'host.cpp',*[out/(n+'.o') for n in ['unit','frozen-selector','frozen-helper']],*[isolated/(n+'.o') for n in ['oracle-unit','model','admission']],speed_oracle,ROOT/'tests/gt3_transmission_speed_context.cpp',*libs,'-o',out/'ps2run'])
    old.identity(out,base,list(i['sources'])+['tests/gt3_transmission_state_host.inc','host/main.cpp','host/gt3_clean_transmission.cpp','host/gt3_clean_transmission.hpp','host/gt3_clean_transmission_speed.cpp','host/gt3_clean_transmission_speed.hpp','tests/gt3_transmission_speed_host.inc','tests/gt3_transmission_speed_context.cpp'],dict(stage='native-build-only',build_gate=gate,runtime_default=False,canonical_installation=False,isolated=str(isolated),isolated_identity_sha256=old.sha(isolated/'identity.json')))
def source():
    with tempfile.TemporaryDirectory(prefix='gt3-state-public-') as d:
        binary=Path(d)/'state-source-test'
        run(['clang++','-std=c++20','-O2','-Wall','-Wextra','-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include'),ROOT/'host/gt3_transmission_state.cpp',ROOT/'host/gt3_clean_transmission_admission.cpp',ROOT/'tests/gt3_transmission_state_source_test.cpp','-o',binary]);run([binary])
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('source')
    b=sub.add_parser('build');b.add_argument('baseline',type=Path);b.add_argument('output',type=Path)
    n=sub.add_parser('native');n.add_argument('baseline',type=Path);n.add_argument('isolated',type=Path);n.add_argument('output',type=Path);n.add_argument('--enable-clean',action='store_true')
    a=p.parse_args()
    if a.command=='source':source()
    elif a.command=='build':build(a.baseline.resolve(strict=True),a.output.resolve())
    else:native(a.baseline.resolve(strict=True),a.isolated.resolve(strict=True),a.output.resolve(),a.enable_clean)
if __name__=='__main__':main()
