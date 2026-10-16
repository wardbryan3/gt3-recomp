#!/usr/bin/env python3
"""Explicit isolated GT3 extension products; NEVER modifies canonical inputs/targets."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ELF=ROOT/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,log=None):
 if log:
  with log.open('x') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=f,check=True)
 else:subprocess.run(list(map(str,args)),check=True)
def preflight(base):
 s=importlib.util.spec_from_file_location('original_preflight',ROOT/'scripts/validate_gt3_transmission_speed.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.preflight(base)
 s=importlib.util.spec_from_file_location('unchanged_state',ROOT/'scripts/project/transmission_state.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.check_record(m.load(m.DB))
def named(s,name):return s.replace('void unit_0039(',f'void {name}(').replace('unit_0039(c,',name+'(c,').replace('entries_0039',name+'_entries')
def admission_label(s):
 a=s.index('L_001E6D48:\n');b=s.index('L_001E6EC8:\n',a);body=s[a:b];store=body.index('st8((');pos=body.rfind('    c.budget -= 2;',0,store);assert pos>0
 return s[:a]+body[:pos]+'L_VT_ADMIT:\n'+body[pos:]+s[b:]
GATE='''    switch (gt3::extensions::vt::admission_route(c,depth)) {
    case 1: set32(c.r[5],c.r[4].w[0]+520u); c.f[1]=0; goto L_001E6E18;
    case 2: set32(c.r[5],c.r[4].w[0]+520u); set32(c.r[2],2u); goto L_VT_ADMIT;
    default: break;
    }
'''
def actual(s):
 s=admission_label(s);a=s.index('L_001E6D48:\n');b=s.index('L_001E6EC8:\n',a);body=s[a:b];assert body.count('    c.budget -= 8;\n')==1
 body=body.replace('L_001E6D48:\n','L_001E6D48:\n    gt3::extensions::vt::admission_enter(c,depth);\n').replace('    c.budget -= 8;\n','    c.budget -= 8;\n'+GATE)
 s=s[:a]+body+s[b:];s=s.replace('L_001E5690:\n','L_001E5690:\n    if(gt3::extensions::vt::selector(c,depth))return;\n')
 return '#include "extensions/gt3/native_bindings/virtual_transmission.hpp"\n'+s

def reference(s):
 s=admission_label(s);key='    default: bad_entry';assert s.count(key)==1
 return named(s.replace(key,'    case 1000u: goto L_001E6E18;\n    case 1001u: goto L_VT_ADMIT;\n'+key),'vt_reference_unit_0039')
def includes(base):return ['-I'+str(ROOT),'-I'+str(ROOT/'runtime/include'),'-I'+str(base/'generated-original')]
def libs(base):return [base/'original/libps2game.a',base/'original/libps2runtime.a',ROOT/'third_party/wgpu-native/lib/libwgpu_native.a','-ldl','-lpthread','-lm']
def identity(out,base,extra):
 sources=['scripts/build_gt3_extensions.py','extensions/gt3/native_bindings/virtual_transmission.hpp']
 sources += [str(p.relative_to(ROOT)) for p in (ROOT/'extensions/gt3').rglob('*') if p.is_file() and p.suffix in ['.hpp','.cpp','.inc'] and str(p.relative_to(ROOT)) not in sources]
 for p in sources:
  copy=out/'evaluated-sources'/p;copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes((ROOT/p).read_bytes())
 files={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()}
 (out/'identity.json').write_text(json.dumps(dict(base=str(base),baseline_identity_sha256=sha(base/'build-identity.json'),sources={p:sha(ROOT/p) for p in sources},files=files,canonical_installation=False,**extra),indent=2)+'\n')
def contracts(base,out):
 preflight(base);out.mkdir(parents=True,exist_ok=False);s=(base/'generated-original/unit_0039.cpp').read_text()
 ref=reference(s);act=named(actual(s),'vt_contract_unit_0039');(out/'reference.cpp').write_text(ref);(out/'contract-unit.cpp').write_text(act)
 # Reverse the private extra-label/reference transformation exactly.
 stripped=ref.replace('vt_reference_unit_0039_entries','entries_0039').replace('vt_reference_unit_0039','unit_0039').replace('L_VT_ADMIT:\n','').replace('    case 1000u: goto L_001E6E18;\n    case 1001u: goto L_VT_ADMIT;\n','');assert stripped==s
 cc=['clang++','-std=c++20','-O2',*includes(base)]
 for n in ['reference','contract-unit']:run([*cc,'-c',out/(n+'.cpp'),'-o',out/(n+'.o')])
 run([*cc,ROOT/'tests/gt3_extensions/transmission_contract.cpp',out/'reference.o',out/'contract-unit.o',*libs(base),'-o',out/'contracts'])
 run([out/'contracts',ELF],out/'contracts.log');identity(out,base,dict(stage='contracts-passing',runtime_default=False,extension_installed=False,test_sha256=sha(ROOT/'tests/gt3_extensions/transmission_contract.cpp')))
def build(base,proof,out,gate):
 preflight(base);i=json.loads((proof/'identity.json').read_text());assert i['stage']=='contracts-passing'
 for p,h in i['files'].items():assert sha(proof/p)==h,p
 for p,h in i['sources'].items():assert sha(ROOT/p)==h,p
 assert sha(ROOT/'tests/gt3_extensions/transmission_contract.cpp')==i['test_sha256']
 out.mkdir(parents=True,exist_ok=False);run([proof/'contracts',ELF],out/'contracts-rerun.log')
 s=(base/'generated-original/unit_0039.cpp').read_text();u=actual(s) if gate else s
 # Read-only observations; identical sites and production code for OFF and ON.
 for pc in ['001E6D48','001E6EC8','001E5B98','001E5D54','001E7500','001E7590','001E77E0','001E77F8','001E783C']:
  key='L_'+pc+':\n';assert u.count(key)==1;u=u.replace(key,key+'    gt3::extensions::vt::observe(c,0x'+pc+'u);\n')
 if not gate:u='#include "extensions/gt3/native_bindings/virtual_transmission.hpp"\n'+u
 # One explicit post-admission observation, also on original no-hook unit.
 a=u.index('L_001E6D48:\n');b=u.index('L_001E6EC8:\n',a);body=u[a:b];key=' c.pc = t; return; }';assert body.count(key)==1;body=body.replace(key,' c.pc = t; gt3::extensions::vt::observe(c,0x6d480000u); return; }');u=u[:a]+body+u[b:]
 (out/'unit.cpp').write_text(u)
 host=(ROOT/'host/main.cpp').read_text();host=host.replace('#include <vector>','#include <vector>\n#include "extensions/gt3/native_bindings/host.inc"',1)
 key='        if (a == "--arg" && i + 1 < argc)';assert host.count(key)==1;host=host.replace(key,'        if(gt3_extension_arg(a,i,argc,argv)) {}\n        else if (a == "--arg" && i + 1 < argc)',1)
 key='    if (gt3_triple) {';assert host.count(key)==1;host=host.replace(key,'    if(!gt3_extension_start(gt3_triple || !ram_words.empty() || !ps2::g_options.axes.empty(),load_path))return 2;\n'+key,1)
 (out/'host.cpp').write_text(host);cc=['clang++','-std=c++20','-O2',*includes(base),'-DGT3_EXT_VIRTUAL_TRANSMISSION='+str(int(gate))]
 run([*cc,'-c',out/'unit.cpp','-o',out/'unit.o'])
 sources=[ROOT/'extensions/gt3/native_bindings/virtual_transmission.cpp']
 if gate:sources += [ROOT/'extensions/gt3/virtual_transmission/controller.cpp']
 run([*cc,out/'host.cpp',*sources,out/'unit.o',proof/'reference.o',*libs(base),'-Wl,-Map='+str(out/'link.map'),'-o',out/'ps2run-extensions'])
 identity(out,base,dict(stage='extended-build',build_extension=gate,runtime_default=False,contracts_identity_sha256=sha(proof/'identity.json')))
def baseline_control(base,out):
 preflight(base);out.mkdir(parents=True,exist_ok=False)
 run(['clang++','-std=c++20','-O2',*includes(base),'-DPS2_PROFILE',ROOT/'host/main.cpp',ROOT/'host/profile.cpp',*libs(base),'-Wl,-Map='+str(out/'link.map'),'-o',out/'ps2run-baseline-control'])
 identity(out,base,dict(stage='unchanged-canonical-host-control',build_extension=False,runtime_default=False,host_sha256=sha(ROOT/'host/main.cpp')))
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 c=sub.add_parser('contracts');c.add_argument('baseline',type=Path);c.add_argument('output',type=Path)
 c=sub.add_parser('baseline-control');c.add_argument('baseline',type=Path);c.add_argument('output',type=Path)
 b=sub.add_parser('build');b.add_argument('baseline',type=Path);b.add_argument('contracts',type=Path);b.add_argument('output',type=Path);b.add_argument('--with-virtual-transmission',action='store_true')
 a=p.parse_args()
 if a.command=='contracts':contracts(a.baseline.resolve(strict=True),a.output.resolve())
 elif a.command=='baseline-control':baseline_control(a.baseline.resolve(strict=True),a.output.resolve())
 else:build(a.baseline.resolve(strict=True),a.contracts.resolve(strict=True),a.output.resolve(),a.with_virtual_transmission)
if __name__=='__main__':main()
