#!/usr/bin/env python3
"""Read-only analysis of retained original/fallback traces; never admits a pedal.
CPU encoding is the defined-field hexadecimal stream from gt3_pedal_host.cpp.
No guest execution, RAM patching, relocation or implementation/guard bypass.
"""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from characterize_gt3_pedal_profiles import digest,read_rows,semantic,profile
from gt3_pedal_authority import source_version


def cpu_words(row):
    text=row['cpu']
    assert len(text)==363*8,'unexpected defined-CPU encoding'
    return [int(text[i:i+8],16) for i in range(0,len(text),8)]


def reg(words,index):return words[index*4]|(words[index*4+1]<<32)


def observe_case(directory):
    rows=read_rows(directory/'cpu.jsonl');observations=read_rows(directory/'profiles.jsonl')
    entries=[r for r in rows if r['pc']==0x1e48fc];joins=[r for r in rows if r['pc']==0x1e4ba8]
    configs=[r for r in observations if r['pc']==0x1e48fc]
    assert len(entries)==len(joins)==len(configs)>0
    costs=[];addresses=set();sp_values=set();matched=0;wrapper=None
    for row in rows:
        if row['pc']==0x1e4d38:wrapper=cpu_words(row)
        if row['pc']==0x1e48fc:
            w=cpu_words(row);command=reg(w,18);sp=reg(w,29)
            assert command==sp+0xd0,'not the documented active-frame relation'
            if wrapper is not None:
                assert command==reg(wrapper,29)-0x40
                assert reg(wrapper,31)==0x1f3b6c
                matched+=1;wrapper=None
    for entry,join,config in zip(entries,joins,configs):
        assert (entry['frame'],entry['car'])==(join['frame'],join['car'])==(config['frame'],config['car'])
        a,b=cpu_words(entry),cpu_words(join)
        assert reg(a,18)==reg(b,18)==config['command']
        assert reg(a,29)==reg(b,29) and reg(a,28)==reg(b,28)==0x3579f0
        assert reg(b,2)==config['auxiliary_suppression']
        assert reg(b,17)==profile(config)[1]['effective_policy']
        cost=(a[138]-b[138])&0xffffffff
        assert 0<cost<2048,'unexpected budget encoding or interval'
        costs.append(cost);addresses.add(reg(a,18));sp_values.add(reg(a,29))
    return {'entries':len(entries),'wrapper_entry_links':matched,'command_addresses':sorted(addresses),
            'pedal_entry_sp':sorted(sp_values),'original_region_cost_min':min(costs),
            'original_region_cost_max':max(costs),'observed_join_v0_s1_sp_gp':True,
            'trace_sha256':digest(directory/'cpu.jsonl')}


def analyze(root):
    survey=root/'local/pedal-profiles-v1';plan=json.loads((survey/'plan.json').read_text())
    cases={c['id']:observe_case(Path(c['directory'])) for c in plan['cases']+plan['explorations']}
    original=survey/'time-trial-original';fallback=survey/'paired-1/time-trial'
    assert semantic(read_rows(original/'cpu.jsonl'))==semantic(read_rows(fallback/'cpu.jsonl'))
    for name in ['profiles.jsonl','steering.jsonl','memory.bin']:
        assert digest(original/name)==digest(fallback/name),name
    shots={p.name:digest(p) for p in (original/'shots').glob('*.ppm')}
    assert shots and shots=={p.name:digest(p) for p in (fallback/'shots').glob('*.ppm')}
    assert '[gt3-pedals] replaced=0 fallback=299 response_calls=0' in (fallback/'run.log').read_text()
    return {'status':'stopped-unproven-admission','cases':cases,
            'entries':sum(c['entries'] for c in cases.values()),
            'wrapper_entry_links':sum(c['wrapper_entry_links'] for c in cases.values()),
            'fallback_comparison':{'entries':299,'replaced':0,'fallback':299,'defined_cpu_budget_exact':True,
              'observations_steering_dump_captures_exact':True,'capture_count':len(shots)},
            'actual_49af40_clean_body_differential':'not established; guard unchanged and no bypass',
            'new_live_execution':False,'instrumentation_added':False}


def check_record(record):
    assert record['schema_version']==1 and record['status']=='stopped-unproven-admission'
    assert record['guard_expansion_authorized'] is False and record['safe_admission_established'] is False
    assert record['command_storage']=='activation-local stack object; backing allocation not established'
    for source,sha in record['protected_hashes'].items():source_version(ROOT,source,sha)
    assert record['analysis']['entries']==4199 and record['analysis']['fallback_comparison']['replaced']==0
    assert record['analysis']['new_live_execution'] is False
    source_version(ROOT,'scripts/audit_gt3_pedal_admission.py',record['analyzer_sha256'])
    for a in record['artifacts']:
        p=Path(a['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
        assert a['visibility']=='private' and len(a['sha256'])==64
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['analyze','check','verify']);parser.add_argument('--root',type=Path)
    parser.add_argument('--out',type=Path);args=parser.parse_args()
    if args.command=='analyze':
        assert args.root and args.out,'explicit repository and new output required'
        with args.out.open('x') as f:json.dump(analyze(args.root.resolve()),f,indent=2);f.write('\n')
        return
    record=check_record(json.loads((ROOT/'decomp/gt3/pedal-admission-49af40.json').read_text()))
    if args.command=='verify':
        assert args.root,'explicit private repository root required'
        sys.path.insert(0,str(ROOT/'scripts/project'));import project
        project.verify_profiles(args.root)
        project.verify_current(args.root,record,'Read-only admission audit')
        assert analyze(args.root.resolve())==record['analysis']
        snapshot=next(a for a in record['artifacts'] if a['id']=='artifact:admission-static')
        bundle=json.loads((args.root/snapshot['path']).read_text())['evidence_bundle']
        assert {r['evidence_id'] for r in bundle['records']}==set(record['static_evidence_ids'])
    print('Historical read-only audit verified: its stopped result is unchanged. Current admission closure, if any, is a separate authority.')
if __name__=='__main__':main()
