#!/usr/bin/env python3
"""Bounded v3 pedal validation only. Uses (never rewrites) authoritative fixture.
Canonical, build-gate-OFF, runtime-disabled, trace-only and enabled comparisons.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic(rows):
    # Cpu.pc is transport between direct translated branches; serialize the
    # explicit semantic probe PC in cpu instead. Keep transport in raw evidence.
    return [{k:v for k,v in row.items() if k != 'transport_pc'} for row in rows]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['build','elf','iso','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    build,elf,iso=(p.resolve(strict=True) for p in [args.build,args.elf,args.iso])
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    subprocess.run(['just','verify-current',str(root)],cwd=root,check=True)
    authority=json.loads((root/'decomp/gt3/current-validation.json').read_text())
    fixture=next(a for a in authority['artifacts'] if a['id']==authority['fixture']['artifact'])
    snapshot=root/fixture['path'];assert digest(snapshot)==fixture['sha256']
    assert snapshot.read_bytes()[:12]==b'PS2STATE'+struct.pack('<I',3),'not native v3'
    assert digest(elf)==json.loads((root/'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
    identity=build/'pedal-build-identity.json';pinned=json.loads(identity.read_text())
    assert pinned['build_opt_in'] is True and pinned['runtime_default'] is False
    for name,sha in pinned['files'].items():assert digest(build/name)==sha,f'changed build file: {name}'
    base_identity=json.loads((build/'base/build-identity.json').read_text())
    canonical=build/'base/original/ps2run';clock=build/'base/fixed-clock.so'
    for p in [canonical,clock,elf]:assert base_identity['inputs_and_executables'][str(p)]==digest(p)
    expected_canonical=next(a for a in authority['artifacts'] if a['id']=='artifact:current-canonical-executable')
    assert digest(canonical)==expected_canonical['sha256'],'canonical generated-only executable changed'
    summary={'source_commit':pinned['source_commit'],'scope':'pedal validation-only; generated downstream',
             'build_identity_sha256':digest(identity),'validator_sha256':digest(Path(__file__)),
             'fixture_sha256':fixture['sha256'],'fixture_version':3,'elf_sha256':digest(elf),
             'iso_sha256':digest(iso),'canonical_sha256':digest(canonical),'cases':{}}
    env={k:v for k,v in os.environ.items() if not k.startswith('PS2_')}
    env.update(PS2_ONE_THREAD='1',SDL_AUDIODRIVER='dummy',LD_PRELOAD=str(clock),
               GT3_BASELINE_UTC_EPOCH=str(authority['fixture']['clock_utc_epoch']))
    off=build/'pedal-off';on=build/'pedal-on'
    rejected=subprocess.run([str(off),'--gt3-clean-pedals'],env=env,cwd=root,capture_output=True,text=True)
    (out/'build-gate-rejection.log').write_text(rejected.stdout+rejected.stderr)
    assert rejected.returncode==2 and 'build gate is OFF' in rejected.stderr
    common=[str(elf),'--disc',str(iso),'--ntsc','--render-scale','1','--render-scale-y','1',
            '--output-size','1280x240','--frame-every','100','--load-state',str(snapshot),'--frames','5101']

    def run(tag,inputs,binary=on,trace=True):
        directory=out/tag;directory.mkdir();(directory/'shots').mkdir()
        command=[str(binary),*common,'--memcard',str(directory/'card.ps2'),'--frames-dir',str(directory/'shots'),*inputs]
        if trace:command+=['--gt3-pedal-trace',str(directory/'pedals.jsonl'),'--gt3-wheel-trace',str(directory/'steering.jsonl')]
        with (directory/'run.log').open('w') as log:
            subprocess.run(command,cwd=root,env=dict(env,PS2_DUMP=str(directory/'memory.bin')),
                           stdout=log,stderr=log,check=True,timeout=240)
        text=(directory/'run.log').read_text();assert 'frame limit reached' in text,tag
        item={'argv':command,'memory_sha256':digest(directory/'memory.bin'),
              'captures':{p.name:digest(p) for p in sorted((directory/'shots').glob('*.ppm'))}}
        assert item['captures'],tag
        if binary!=canonical:
            match=re.search(r'\[gt3-pedals\] replaced=(\d+) fallback=(\d+) response_calls=(\d+)',text)
            assert match,tag
            item['pedal_calls']=dict(zip(['replaced','fallback','response_calls'],map(int,match.groups())))
        rows=[json.loads(line) for line in (directory/'pedals.jsonl').read_text().splitlines()] if trace else []
        if trace:
            item['stages']={hex(k):v for k,v in Counter(row['pc'] for row in rows).items()}
            assert item['stages'].get('0x1e48fc',0)==item['stages'].get('0x1e4ba8',0)>0
        summary['cases'][tag]=item
        return rows

    def equal(left,right,rows=None,other=None):
        a,b=(summary['cases'][tag] for tag in [left,right])
        assert a['memory_sha256']==b['memory_sha256'],f'{left}/{right}: complete EE/IOP/SPU dump'
        assert a['captures']==b['captures'],f'{left}/{right}: captures'
        if rows is not None:
            assert semantic(rows)==semantic(other),f'{left}/{right}: complete defined CPU/pedal trace'
            assert (out/left/'steering.jsonl').read_bytes()==(out/right/'steering.jsonl').read_bytes(),f'{left}/{right}: unchanged steering trace'
        a.setdefault('exact_matches',[]).append(right)

    pedal_inputs=['--press','4802:cross:100','--press','4902:square:100']
    run('canonical',pedal_inputs,canonical,False)
    run('build_off_disabled',pedal_inputs,off,False);equal('build_off_disabled','canonical')
    run('runtime_disabled',pedal_inputs,on,False);equal('runtime_disabled','canonical')
    trace=run('trace_only',pedal_inputs);equal('trace_only','canonical')
    off_rows=run('build_off_trace',pedal_inputs,off);equal('build_off_trace','trace_only',off_rows,trace)
    for tag in ['build_off_disabled','runtime_disabled','trace_only','build_off_trace']:
        assert not any(summary['cases'][tag]['pedal_calls'].values()),tag
    scenarios=[('neutral',[]),('accel_brake',pedal_inputs),
               ('simultaneous',['--press','4802:cross+square:200']),
               ('pad_turn',['--press','4802:cross+left:150','--press','4952:square+right:100']),
               ('wheel_left',[*pedal_inputs,'--gt3-wheel','-.5']),
               ('wheel_right',[*pedal_inputs,'--gt3-wheel','.5','--gt3-clean-steering']),
               ('wheel_transition',[*pedal_inputs,'--gt3-wheel','.5','--gt3-wheel-at','4902:0','--gt3-wheel-at','5002:-.5','--gt3-clean-steering'])]
    for name,inputs in scenarios:
        original=run('generated_'+name,inputs)
        clean=run('clean_'+name,[*inputs,'--gt3-clean-pedals'])
        equal('clean_'+name,'generated_'+name,clean,original)
        calls=summary['cases']['clean_'+name]['pedal_calls']
        assert calls['replaced']==sum(row['pc']==0x1e48fc for row in clean)>0
        assert calls['fallback']==0
        assert not any(summary['cases']['generated_'+name]['pedal_calls'].values())
        if name.startswith('wheel'):
            response_rows=[row for row in original if row['pc']==0x1d92e0]
            assert len(response_rows)==calls['response_calls']>0
            assert any(row['mode']==4 and row['flags']&6==6 for row in original if row['pc']==0x1e48fc)
        assert any(row['pc']==0x1e4c74 for row in original),'generated coupling continuation not observed'
        for pc in [0x1e8910,0x1e6ec8,0x1e7500]:
            assert any(row['pc']==pc for row in original),f'original player consumer {pc:x} not observed'
        print(name,'exact CPU/pedal/steering traces, captures, complete dumps PASS',flush=True)
    assert digest(snapshot)==fixture['sha256'],'trusted fixture changed'
    summary['runtime_default']=False;summary['canonical_gate']=False
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('Pedal bounded v3 validation PASS (no physical-device proof)')

if __name__=='__main__':main()
