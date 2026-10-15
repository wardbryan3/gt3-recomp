#!/usr/bin/env python3
"""Strict, read-only closure verification; no proprietary inputs for public checks."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from characterize_gt3_pedal_profiles import digest,read_rows,semantic
ROOT=Path(__file__).resolve().parents[1]

def semantic_prefix(path):
    return path.read_text().split('std::uint64_t fingerprint(',1)[0].encode()

def check_record(v,root=ROOT):
    assert v['schema_version']==1 and v['id']=='pedal-v1-observed-context-closure'
    assert v['lifecycle'] in ('validating','frozen') and v['stop'] is True
    assert re.fullmatch('[a-f0-9]{40}',v['source_commit'])
    assert v['build_default'] is False and v['runtime_default'] is False
    assert v['runtime_installation']=='canonical-generated; isolated validation only'
    assert v['boundary']==['0x001e48fc','0x001e4ba7'] and v['resume_address']=='0x001e4ba8'
    assert v['semantics_changed'] is False
    assert hashlib.sha256(semantic_prefix(root/'host/gt3_clean_pedals.cpp')).hexdigest()==v['semantic_prefix_sha256']
    assert len(v['cases'])==14 and len(set(v['cases']))==14
    assert v['results']=={'shadow_entries':4199,'live_substitutions':4199,'live_fallbacks':0,
        'observed_processing_classes':5,'join_cases':131072,'wrapper_cases':2160,'fallback_cases':24}
    assert v['admission']['kind']=='manual-activation-frame-and-return-chain'
    assert v['admission']['absolute_command_allowlist'] is False
    for name,sha in v['source_hashes'].items():
        assert re.fullmatch('[a-f0-9]{64}',sha) and digest(root/name)==sha,name
    ids=set()
    for a in v['artifacts']:
        p=Path(a['path']);assert a['id'] not in ids;ids.add(a['id'])
        assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
        assert a['visibility']=='private' and re.fullmatch('[a-f0-9]{64}',a['sha256'])
    assert v['artifacts'] and all(a in v['artifacts'] for a in v['historical_sources'].values())
    for name,a in v['historical_sources'].items():assert name in v['source_hashes']
    assert set(v['gates'])=={'shadow','differential','live','baseline','pedals','public'}
    assert all(s in ('pending','passing','failed') for s in v['gates'].values())
    if v['lifecycle']=='frozen':assert set(v['gates'].values())=={'passing'}
    return v

def check_summaries(v,shadow,live):
    assert shadow['mode']=='shadow' and live['mode']=='live'
    assert set(shadow['cases'])==set(live['cases'])==set(v['cases'])
    for name in v['cases']:
        s=shadow['cases'][name];l=live['cases'][name];n=299 if name=='time-trial' else 300
        assert s['entries']==l['entries']==n
        assert s['actual_entry_full_cpu_32mib_cost_mutation_differential'] is True
        assert l['exact_cpu_steering_ram_captures'] is True
        assert l['clean_counts']==[n,0,600 if name.startswith('compat-wheel-') else 0]
        assert s['threads']==[[10,0x493700,32768]] and s['parents']==[0x17c848]
        assert 48<=s['cost'][0]<=s['cost'][1]<=152
        assert s['hooks']==[0x1f14e8 if name=='free-run' else 0x1ed860]
    assert sum(s['entries'] for s in shadow['cases'].values())==4199

def verify(root):
    from project import project as registry
    v=check_record(registry.load('pedal-closure'))
    registry.verify_profiles(root)
    # The older audit remains an immutable stopped authority, independently checked.
    subprocess.run([sys.executable,str(ROOT/'scripts/audit_gt3_pedal_admission.py'),'verify','--root',str(root)],check=True)
    root=Path(root).resolve();registry.verify_current(root,v,'Pedal observed-context closure')
    paths={a['id']:root/a['path'] for a in v['artifacts']}
    shadow=json.loads(paths['artifact:closure-shadow-summary'].read_text())
    live=json.loads(paths['artifact:closure-live-summary'].read_text());check_summaries(v,shadow,live)
    assert shadow['validator_sha256']==live['validator_sha256']==v['source_hashes']['scripts/validate_gt3_pedal_closure.py']
    parent=registry.load('pedal-validation')
    old=paths[v['historical_sources']['host/gt3_clean_pedals.cpp']['id']]
    assert digest(old)==parent['source_hashes']['host/gt3_clean_pedals.cpp']
    assert semantic_prefix(old)==semantic_prefix(ROOT/'host/gt3_clean_pedals.cpp'),'Changed semantic body'
    base=root/'local/pedal-closure-v1'
    plan=json.loads((root/'local/pedal-profiles-v1/plan.json').read_text())
    assert shadow['plan_sha256']==live['plan_sha256']==digest(root/'local/pedal-profiles-v1/plan.json')
    for case in plan['cases']+plan['explorations']:
        name=case['id'];original=root/Path(case['directory']).relative_to(ROOT)
        reference=read_rows(original/'cpu.jsonl');n=sum(r['pc']==0x1e48fc for r in reference)
        assert n==live['cases'][name]['entries']
        def equal(d,traced=True):
            assert digest(d/'memory.bin')==digest(original/'memory.bin')
            shots={p.name:digest(p) for p in (d/'shots').glob('*.ppm')}
            assert shots and shots=={p.name:digest(p) for p in (original/'shots').glob('*.ppm')}
            if traced:
                assert semantic(read_rows(d/'cpu.jsonl'))==semantic(reference)
                assert (d/'steering.jsonl').read_bytes()==(original/'steering.jsonl').read_bytes()
        d=base/'shadow-live'/(name+'-shadow');equal(d)
        rows=read_rows(d/'closure.jsonl');entries=[r for r in rows if r['stage']=='entry'];joins=[r for r in rows if r['stage']=='join']
        assert len(entries)==len(joins)==n and all(r['exact'] is True for r in joins)
        for tag in ['build-off','disabled','trace','clean']+(['canonical'] if case['reachability']=='native-pad' else []):
            d=base/'live-matrix'/(name+'-'+tag);equal(d,tag not in ('disabled','canonical'))
            command=json.loads((d/'command.json').read_text());binary=root/Path(command['argv'][0]).relative_to(ROOT)
            assert digest(binary)==command['binary_sha256']
            assert digest(root/Path(command['state']['path']).relative_to(ROOT))==command['state']['sha256']
            if tag!='canonical':
                counts=re.search(r'\[gt3-pedals\] replaced=(\d+) fallback=(\d+) response_calls=(\d+)',(d/'run.log').read_text())
                assert counts and list(map(int,counts.groups()))==(live['cases'][name]['clean_counts'] if tag=='clean' else [0,0,0])
    assert '24 cases, zero CPU/RAM mutations' in (base/'candidate-build/join-differential.log').read_text()
    assert '131072 cases' in (base/'candidate-build/join-differential.log').read_text()
    assert '6480 complete CPU+32MiB' in (base/'candidate-build/wrapper-policy-differential.log').read_text()
    expected='b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a'
    assert digest(base/'candidate-build/base/original/ps2run')==expected
    build_identity=json.loads((base/'candidate-build/base/build-identity.json').read_text())
    assert build_identity['source_commit']==v['source_commit']
    # Python authority/reporting evolved after compilation. All compiled source
    # from that build must still match, not just the clean body's source prefix.
    for name,sha in build_identity['source_hashes'].items():
        if Path(name).suffix in ('.cpp','.hpp'):assert digest(ROOT/name)==sha,name
    for name,count,validator in [('current-live',28,'validate_gt3_baseline.py'),('pedal-live-accepted',19,'validate_gt3_pedals.py')]:
        summary=json.loads((base/name/'summary.json').read_text())
        assert len(summary['cases'])==count and summary['canonical_sha256']==expected
        assert summary['validator_sha256']==digest(ROOT/'scripts'/validator)
    baseline=json.loads((base/'current-live/summary.json').read_text())
    fixture=baseline['fixture'];assert fixture['version']==3 and fixture['saved_frame']==4801
    assert all(fixture[k] is True for k in ['defined_serialized_state_exact','complete_guest_dump_recapture_exact','uninterrupted_continuation_exact'])
    pedals=json.loads((base/'pedal-live-accepted/summary.json').read_text())
    clean=[c for name,c in pedals['cases'].items() if name.startswith('clean_')]
    assert len(clean)==7 and sum(c['pedal_calls']['replaced'] for c in clean)==2100
    assert all(c['pedal_calls']['fallback']==0 and c['exact_matches'] for c in clean)
    snapshot=json.loads(paths['artifact:closure-static'].read_text())['evidence_bundle']['records']
    assert {r['evidence_id'] for r in snapshot}==set(v['static_evidence_ids'])
    assert all(r['subject']['digest']['sha256']==registry.load('manifest')['original_elf_sha256'] for r in snapshot)
    ownership=json.loads(paths['artifact:closure-ownership'].read_text())
    assert ownership['original_return_leaf_exact_elf_word_check'] is True and ownership['mode_caller_frames']==[96,112]
    for name in ['trusted','time-trial','free-run','license']:
        observed=ownership['explicit_mode_entry_observations'][name]
        expected_lines=['[mode-frame] pc=1811b8 sp=49b350 ra=181ebc','[mode-frame] pc=181e90 sp=49b3b0 ra=17c5c0'] if name=='trusted' else ['[mode-frame] pc=1811b8 sp=49b340 ra=187a9c','[mode-frame] pc=187a50 sp=49b3b0 ra=17c5c0']
        assert observed==expected_lines
        assert all(line in (base/('context2-'+name)/'run.log').read_text() for line in observed)
    if v['lifecycle']=='frozen':assert 'All current native baseline regressions PASS' in (base/'full-regressions/regressions.log').read_text()
    print('PASS: 4199 actual-context shadow differentials and 4199 guarded substitutions; historical stops preserved; no universal/physical/canonical-integration claim')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);verify(p.parse_args().root)
