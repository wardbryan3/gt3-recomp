#!/usr/bin/env python3
"""Read-only observation reduction and immutable-Frozen representative replay.
Raw descriptor words and captures stay private; public summaries use fingerprints.
A finite explicit plan is coverage, never an exhaustive game/profile inventory.
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

ENTRY=0x1e48fc
JOIN=0x1e4ba8
HELPER=0x1d92e0
REACHABILITY={'native-pad','existing-synthetic-wheel-compatibility'}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def words_digest(words):return hashlib.sha256(struct.pack('<'+'I'*len(words),*words)).hexdigest()
def read_rows(path):return [json.loads(line) for line in path.read_text().splitlines()]
def semantic(rows):return [{k:v for k,v in row.items() if k!='transport_pc'} for row in rows]
def descriptor_id(words):
    assert len(words)==4,'descriptor must be exactly 16 bytes'
    return 'descriptor:'+words_digest(words)

def profile(row):
    """Exact configuration/selector identity, not transient pressure/history.
    Do NOT infer vehicle, gearbox or device identity from guest addresses.
    mode2/3 are intentionally not collapsed even if their pedal paths coincide.
    """
    assert row['pc']==ENTRY
    assert not row.get('invalid_observation_context',False)
    assert row['incoming_v1']==row['kind'],'entry classification outside documented manual contract'
    assert row['s0']==row['car']+0xf84 and row['control']==row['car']+0x1304,'unsupported entry aliases; stop'
    assert row['gp']==0x3579f0,'unsupported GP; stop'
    policy=0 if row['incoming_v1']==1 or row['policy_blocked'] else row['stored_policy']
    key={'accelerator_descriptor':descriptor_id(row['accelerator_descriptor']),
         'brake_descriptor':descriptor_id(row['brake_descriptor']),
         'rates_and_floor_sha256':words_digest(row['slew']+row['floor']),
         'mode':row['mode'],'representation_flags':row['flags']&14,'kind':row['kind'],
         'effective_policy':policy,'auxiliary_suppressed':bool(row['auxiliary_suppression'])}
    identity='profile:'+hashlib.sha256(json.dumps(key,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return identity,key

def summarize(plan):
    profiles={};descriptors={};case_results=[];updates=0;calls=Counter()
    for case in plan['cases']+plan.get('explorations',[]):
        assert case['reachability'] in REACHABILITY,'physical reachability cannot be inferred'
        directory=Path(case['directory']);rows=read_rows(directory/'profiles.jsonl')
        assert rows and all(not r.get('invalid_observation_context') for r in rows)
        entries=[r for r in rows if r['pc']==ENTRY];joins=[r for r in rows if r['pc']==JOIN]
        assert len(entries)==len(joins)>0,'no observed live pedal region or unmatched joins'
        assert all(r['pc'] in (ENTRY,JOIN,HELPER) for r in rows),'unexpected observation site'
        ids=set()
        for r,j in zip(entries,joins):
            identity,key=profile(r);assert j['s1']==key['effective_policy']
            ids.add(identity);updates+=1
            item=profiles.setdefault(identity,dict(id=identity,selectors=key,cases=[],reachability=[],command_contexts=[],observed_updates=0))
            if r['command'] not in item['command_contexts']:item['command_contexts'].append(r['command'])
            item['observed_updates']+=1
            if case['id'] not in item['cases']:item['cases'].append(case['id'])
            if case['reachability'] not in item['reachability']:item['reachability'].append(case['reachability'])
            for name in ['accelerator_descriptor','brake_descriptor']:
                did=descriptor_id(r[name]);d=descriptors.setdefault(did,{'id':did,'mode':r[name][0],'sites':[]})
                if name not in d['sites']:d['sites'].append(name)
        for r in rows:
            if r['pc']==HELPER:
                assert r['a1']==0 and r['a0'] in (0x49d060,0x49d070),'response ABI outside bounded contract; stop'
                calls[hex(r['a0'])]+=1
        case_results.append({'id':case['id'],'reachability':case['reachability'],'labels':case['labels'],
                             'profiles':sorted(ids),'updates':len(entries),
                             'command_contexts':sorted({r['command'] for r in entries}),
                             'original_trace_sha256':digest(directory/'profiles.jsonl')})
    return {'scope':'finite observed matrix, not exhaustive reachability','descriptors':list(descriptors.values()),
            'profiles':list(profiles.values()),'cases':case_results,'original_updates':updates,'original_response_calls':dict(calls)}

def validate(plan,build,out,root):
    """Use original observation cases, not modified descriptors/guest memory.
    Stops on the FIRST unsupported admission or equality failure. Never retries
    by changing Frozen code, guards, tolerance, assertions or snapshot headers.
    """
    identity=json.loads((build/'identity.json').read_text())
    for p,sha in identity['files'].items():assert digest(Path(p))==sha,f'observer build changed: {p}'
    for p,sha in identity['sources'].items():assert digest(root/p)==sha,f'build source changed: {p}'
    baseline=json.loads((root/'decomp/gt3/current-validation.json').read_text())
    frozen=json.loads((root/'decomp/gt3/pedal-validation.json').read_text())
    assert frozen['lifecycle']=='frozen'
    for p,sha in frozen['source_hashes'].items():assert digest(root/p)==sha,'Frozen source changed'
    parent_identity=Path(identity['frozen_build_identity']['path'])
    assert digest(parent_identity)==identity['frozen_build_identity']['sha256']
    parent=parent_identity.parent
    clock=parent/'base/fixed-clock.so'
    pinned=json.loads((parent/'base/build-identity.json').read_text())['inputs_and_executables']
    assert digest(clock)==pinned[str(clock)]
    env={k:v for k,v in os.environ.items() if not k.startswith('PS2_')}
    env.update(PS2_ONE_THREAD='1',SDL_AUDIODRIVER='dummy',LD_PRELOAD=str(clock),
               GT3_BASELINE_UTC_EPOCH=str(baseline['fixture']['clock_utc_epoch']))
    summary=summarize(plan);results=[]
    # Only supplied normal-host inputs are accepted. No RAM-word/patch/reset API.
    allowed={'--disc','--ntsc','--render-scale','--render-scale-y','--output-size','--frame-every','--frames',
             '--memcard','--frames-dir','--load-state','--gt3-pedal-trace','--gt3-wheel-trace',
             '--press','--axis','--gt3-wheel','--gt3-wheel-at'}
    try:
        for case in plan['cases']:
            original=Path(case['directory']);target=out/case['id'];target.mkdir();(target/'shots').mkdir()
            metadata=json.loads((original/'command.json').read_text())
            assert metadata['binary_sha256']==digest(build/'survey-off')
            state=metadata['state'];assert state and digest(Path(state['path']))==state['sha256']
            assert Path(state['path']).read_bytes()[:12]==b'PS2STATE'+struct.pack('<I',3)
            args=metadata['argv'][1:]
            assert all(not a.startswith('--') or a in allowed for a in args)
            assert digest(Path(args[0]))==json.loads((root/'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
            for flag,name in [('--memcard','card.ps2'),('--frames-dir','shots'),('--gt3-pedal-trace','cpu.jsonl'),('--gt3-wheel-trace','steering.jsonl')]:
                index=args.index(flag)+1;args[index]=str(target/name)
            command=[str(build/'survey-on'),*args,'--gt3-clean-pedals']
            (target/'command.json').write_text(json.dumps({'argv':command,'state':state},indent=2)+'\n')
            with (target/'run.log').open('w') as log:
                subprocess.run(command,cwd=root,env=dict(env,PS2_DUMP=str(target/'memory.bin'),
                     GT3_PEDAL_PROFILE_TRACE=str(target/'profiles.jsonl')),stdout=log,stderr=log,check=True,timeout=300)
            text=(target/'run.log').read_text();assert 'frame limit reached' in text
            match=re.search(r'\[gt3-pedals\] replaced=(\d+) fallback=(\d+) response_calls=(\d+)',text)
            assert match;replaced,fallback,responses=map(int,match.groups())
            assert fallback==0,'reachable context outside Frozen admission; stop, do not alter implementation'
            original_rows=read_rows(original/'profiles.jsonl')
            count=sum(r['pc']==ENTRY for r in original_rows)
            assert replaced==count>0,'missing actual substitutions'
            assert read_rows(target/'profiles.jsonl')==original_rows,'exact descriptor/context observations differ'
            assert semantic(read_rows(target/'cpu.jsonl'))==semantic(read_rows(original/'cpu.jsonl')),'defined CPU/budget/pedal trace mismatch'
            assert (target/'steering.jsonl').read_bytes()==(original/'steering.jsonl').read_bytes(),'steering trace mismatch'
            assert digest(target/'memory.bin')==digest(original/'memory.bin'),'complete guest dump mismatch'
            shots={p.name:digest(p) for p in (original/'shots').glob('*.ppm')}
            assert shots and shots=={p.name:digest(p) for p in (target/'shots').glob('*.ppm')},'capture mismatch'
            results.append({'id':case['id'],'updates':count,'replaced':replaced,'fallback':fallback,'response_calls':responses,
                            'memory_sha256':digest(target/'memory.bin'),'captures':shots,'status':'passing'})
            print(case['id'],'PASS',count,'actual Frozen substitutions',flush=True)
    except (AssertionError,OSError,subprocess.SubprocessError) as error:
        (out/'STOP.json').write_text(json.dumps({'status':'stopped','reason':str(error),'completed':results},indent=2)+'\n')
        raise
    summary['validation']=results
    summary['frozen_source_hashes']=frozen['source_hashes'];summary['frozen_registry_sha256']=digest(root/'decomp/gt3/pedal-validation.json')
    summary['observer_identity_sha256']=digest(build/'identity.json')
    summary['plan_sha256']=digest(plan['_path']) if plan.get('_path') else None
    summary['validator_sha256']=digest(Path(__file__))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

def check_record(record,root):
    """Source-only consistency; does not substitute for private verification."""
    assert record['schema_version']==1 and record['status']=='stopped-unsupported-context'
    assert record['runtime_installation']=='none; canonical-generated and Frozen validation gates unchanged'
    assert record['boundary']==['0x001e48fc','0x001e4ba7'] and record['resume_address']=='0x001e4ba8'
    assert record['build_default'] is False and record['runtime_default'] is False
    assert digest(root/'decomp/gt3/pedal-validation.json')==record['frozen_registry_sha256'],'Frozen authority changed'
    frozen=json.loads((root/'decomp/gt3/pedal-validation.json').read_text())
    assert frozen['source_hashes']==record['frozen_source_hashes']
    for source,sha in record['source_hashes'].items():assert digest(root/source)==sha,f'characterization source changed: {source}'
    r=record['results']
    assert r['paired_cases_passed']==4 and r['exact_substitutions']==1200
    assert r['stop_case']=='time-trial' and r['stop_case_original_entries']==299
    assert r['stop_case_replaced']==0 and r['stop_case_fallbacks']==299
    assert r['remaining_pairs']=='not run after stop' and r['fresh_full_native_regressions']=='not run after stop'
    assert record['observations']['original_updates']==4199
    assert len(record['observations']['profiles'])==5 and len(record['observations']['descriptors'])==1
    ids=set()
    for a in record['artifacts']:
        assert a['id'] not in ids;ids.add(a['id'])
        p=Path(a['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
        assert a['visibility']=='private' and re.fullmatch('[0-9a-f]{64}',a['sha256'])
        assert a.get('kind','file') in ('file','file-manifest')
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['reduce','validate'])
    parser.add_argument('--plan',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--build',type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    plan=json.loads(args.plan.read_text());plan['_path']=args.plan.resolve()
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    if args.command=='reduce':(out/'summary.json').write_text(json.dumps(summarize(plan),indent=2)+'\n')
    else:
        assert args.build,'explicit observation build required'
        validate(plan,args.build.resolve(strict=True),out,root)
if __name__=='__main__':main()
