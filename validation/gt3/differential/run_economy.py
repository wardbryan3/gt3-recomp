#!/usr/bin/env python3
"""Build/run isolated economy differentials against explicit private reference inputs.
Never edits/rebuilds the original libraries, executable, generated code, or ELF.
Reports are disposable; a passed function fixture is not integration approval.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
PROFILE_SHA='b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763'

def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--elf',type=Path,required=True)
    parser.add_argument('--reference-build',type=Path,required=True)
    parser.add_argument('--generated-dir',type=Path,default=ROOT/'generated/gt3-restructuring-fresh')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'local/economy-recovery/current')
    args=parser.parse_args()
    elf=args.elf.resolve();build=args.reference_build.resolve();generated=args.generated_dir.resolve();out=args.output_dir.resolve()
    if not out.is_relative_to(ROOT/'local'): parser.error('output directory must be under ignored local/')
    if sha(elf)!=PROFILE_SHA: parser.error('ELF does not match the recovered USA v1.10 profile')
    libs=[build/'libps2game.a',build/'libps2runtime.a']
    units=[generated/f'unit_{u:04X}.cpp' for u in [6,0x36,0x46,0x4c,0x4d,0x4e,0x4f]]
    gpu=ROOT/'third_party/wgpu-native/lib/libwgpu_native.a'
    protected=[elf,build/'ps2run',build/'gt3-native',*libs,*units,
               generated/'units.hpp',ROOT/'runtime/include/ps2/cpu.hpp',gpu]
    before={str(p):sha(p) for p in protected}
    out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'src/gt3/gameplay/economy';tests=ROOT/'validation/gt3/differential'
    suite=[('garage','gt3_garage_oracle.cpp',['gt3_garage.cpp','gt3_garage_list.cpp']),
           ('catalog','gt3_economy_catalog_oracle.cpp',['gt3_economy_catalog.cpp']),
           ('state','gt3_economy_state_oracle.cpp',[]),
           ('checks','gt3_economy_checks_oracle.cpp',[]),
           ('transactions','gt3_economy_transactions_oracle.cpp',[])]
    report={'status':'fail','elf_sha256':PROFILE_SHA,'integration_approval':False,'suites':[],
            'limitations':['Memory-native projections, not complete Cpu/ABI/stack/instruction-cost replacements.',
                          'Garage reset and floating configuration dependencies remain original in composed fixtures.',
                          'Existing check/transaction bodies use bounded dependency interceptions, not full transactions.',
                          'Synthetic instruction-contract fixtures are not automatically valid gameplay states.']}
    def run(command):
        result=subprocess.run([str(x) for x in command],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=300)
        print(result.stdout,end='',flush=True)
        if result.returncode: raise RuntimeError(f'command failed ({result.returncode}): {command[0]}\n{result.stdout}')
        return result.stdout
    try:
        for name,test,cpp in suite:
            executable=out/name
            command=['clang++','-std=c++20','-O2','-Wall','-Wextra','-UNDEBUG',
                     '-I'+str(ROOT/'runtime/include'),'-I'+str(generated),'-I'+str(source),tests/test,
                     *(source/f for f in cpp),'-Wl,--start-group',*libs,'-Wl,--end-group',gpu,
                     '-pthread','-ldl','-lm','-o',executable]
            compile_output=run(command)
            output=run([executable,elf])
            if 'PASS' not in output: raise RuntimeError('suite did not report PASS: '+name)
            report['suites'].append({'name':name,'status':'pass','compile_output':compile_output,'output':output})
        report['status']='pass'
    except Exception as exc:
        report['error']=str(exc)
    finally:
        after={str(p):sha(p) for p in protected}
        report['protected_inputs_unchanged']=after==before
        if after!=before: report['status']='fail'
        report['source_sha256']={str(p.relative_to(ROOT)):sha(p) for p in sorted(source.glob('*')) if p.is_file()}
        report['validation_sha256']={str(p.relative_to(ROOT)):sha(p) for p in
                                     [Path(__file__).resolve(),*(tests/test for _,test,_ in suite)]}
        report['protected_sha256']=before
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Economy differential result:',report['status'],'report:',out/'report.json')
    return 0 if report['status']=='pass' else 1
if __name__=='__main__': sys.exit(main())
