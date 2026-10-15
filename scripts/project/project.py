#!/usr/bin/env python3
"""Authoritative JSON inventories -> lookup/check/documentation. Never modifies evidence."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / 'decomp/gt3'
sys.path.insert(0,str(ROOT/'scripts'))
from characterize_gt3_pedal_profiles import check_record as check_profile_record, summarize as summarize_profiles
from audit_gt3_pedal_admission import check_record as check_admission_record
from gt3_pedal_authority import source_version
from verify_gt3_pedal_closure import check_record as check_closure_record
def load(name): return json.loads((DB / (name + '.json')).read_text())
def check_current():
    """Public consistency only. Private validation is explicit and never skipped."""
    v=load('current-validation')
    assert v['schema_version']==1
    assert v['context']=='current-main-source-with-validation-only-harness'
    assert v['runtime_installation']=='canonical-generated; recovered gates in isolated validation harness only'
    assert re.fullmatch(r'[0-9a-f]{40}',v['source_commit'])
    for key in ('build','regressions','live'):
        assert v[key] in ('pending','passing','failed','blocked'), (key,v[key])
    assert v['fixture']['status'] in ('pending','passing','failed','blocked')
    assert v['fixture']['version']==3, 'Current fixture must be native v3, never relabeled v2'
    ids=set()
    for a in v['artifacts']:
        assert a['id'] not in ids; ids.add(a['id'])
        assert re.fullmatch(r'[0-9a-f]{64}',a['sha256'])
        path=Path(a['path'])
        assert not path.is_absolute() and '..' not in path.parts
        assert path.parts and path.parts[0]=='local' and a['visibility']=='private'
        assert a.get('kind','file') in ('file','file-manifest')
    if any(v[k]=='passing' for k in ('build','regressions','live')) or v['fixture']['status']=='passing':
        assert ids, 'Passing current results require pinned private artifacts'
    if v['live']=='passing':
        assert v['build']==v['regressions']==v['fixture']['status']=='passing', 'Current live proof requires fresh build/regression/v3 fixture gates'
    if v['fixture']['status']=='passing':
        assert v['fixture']['artifact'] in ids, 'Current fixture must have its own pinned artifact'
    return v

def check_pedals():
    """Public source/metadata consistency, not execution of the private oracle."""
    v=load('pedal-validation'); baseline=check_current()
    assert v['schema_version']==1 and v['id']=='current-main-pedal-v1'
    assert v['context']=='current-main-validation-only-pedal-v1'
    assert re.fullmatch(r'[0-9a-f]{40}',v['source_commit'])
    assert v['runtime_installation']=='canonical-generated; pedal gate in isolated validation harness only'
    assert v['build_default'] is False and v['runtime_default'] is False
    assert v['boundary']==['0x001e48fc','0x001e4ba7'] and v['resume_address']=='0x001e4ba8'
    assert v['lifecycle'] in ('live-validated','frozen')
    for gate in ('build','differential','regressions','live'):
        assert v[gate] in ('pending','passing','failed','blocked')
    assert v['fixture']['version']==3 and v['fixture']['status']=='passing'
    for key in ('version','saved_frame','continuation_input_frame','clock_utc_epoch'):
        assert v['fixture'][key]==baseline['fixture'][key], 'Pedals must use authoritative native v3 context'
    ids=set()
    for a in v['artifacts']:
        assert a['id'] not in ids;ids.add(a['id'])
        assert re.fullmatch(r'[0-9a-f]{64}',a['sha256'])
        path=Path(a['path'])
        assert not path.is_absolute() and '..' not in path.parts and path.parts[0]=='local'
        assert a['visibility']=='private' and a.get('kind','file') in ('file','file-manifest')
    assert ids and v['fixture']['artifact'] in ids
    if v['lifecycle']=='frozen':
        assert v['frozen_evaluation']['status']=='passing' and v['frozen_evaluation']['stop'] is True
        assert v['frozen_evaluation']['artifact'] in ids and v['frozen_evaluation']['gates']
    pinned_fixture=next(a for a in v['artifacts'] if a['id']==v['fixture']['artifact'])
    baseline_fixture=next(a for a in baseline['artifacts'] if a['id']==baseline['fixture']['artifact'])
    assert pinned_fixture['path']==baseline_fixture['path'] and pinned_fixture['sha256']==baseline_fixture['sha256']
    original=next(a for a in v['artifacts'] if a['id']=='artifact:pedal-original-elf')
    assert original['sha256']==load('manifest')['original_elf_sha256']
    if v['live']=='passing' or v['lifecycle']=='frozen':
        assert all(v[g]=='passing' for g in ('build','differential','regressions','live'))
        for key in ('complete_cpu','exact_dynamic_budget','fallback_cpu_ram_unchanged',
                    'exact_defined_cpu_traces','exact_pedal_traces','exact_steering_traces',
                    'exact_captures','exact_complete_guest_dumps'):
            assert v['results'][key] is True, key
        assert v['results']['join_clean_cases']>0 and v['results']['whole_wrapper_cases']>0
        assert v['results']['clean_live_updates']>0 and v['results']['live_fallbacks']==0
    assert set(v['source_hashes'])=={'host/gt3_clean_pedals.cpp','host/gt3_clean_pedals.hpp'}
    for name,sha in v['source_hashes'].items():
        source_version(ROOT,name,sha)
    return v

def verify_pedals(root):
    v=check_pedals();verify_current(root)
    verify_current(root,v,'Pedal validation')
    baseline=check_current()
    summary=next(a for a in baseline['artifacts'] if a['id']=='artifact:current-live-summary')
    original_iso=json.loads((Path(root)/summary['path']).read_text())['iso_sha256']
    assert next(a for a in v['artifacts'] if a['id']=='artifact:pedal-original-iso')['sha256']==original_iso, 'Protected original ISO identity changed'
    closure=check_closure()
    verify_current(root,closure,'Current pedal closure')
    for name,count in v['results']['evidence_tree_members'].items():
        a=next(a for a in v['artifacts'] if a['id']==f'artifact:pedal-{name}-files')
        assert len(json.loads((Path(root)/a['path']).read_text())['files'])==count

def verify_current(root, validation=None, label='Current validation'):
    v=check_current() if validation is None else validation; root=Path(root).resolve()
    nested=0
    def verify_file(a):
        p=Path(a['path'])
        assert not p.is_absolute() and '..' not in p.parts and p.parts and p.parts[0]=='local'
        path=root/p
        assert path.is_file(), f'Missing current artifact: {a.get("id",a["path"])}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256'], f'CURRENT EVIDENCE CHANGED: {a.get("id",a["path"])}; do not rehash'
        return path
    for a in v['artifacts']:
        path=verify_file(a)
        if a.get('kind')=='file-manifest':
            members=json.loads(path.read_text())['files']
            assert members and len({m['path'] for m in members})==len(members)
            for member in members:verify_file(member);nested+=1
    assert v['artifacts'], 'No current evidence registered'
    if v.get('fixture',{}).get('status')=='passing':
        a=next(a for a in v['artifacts'] if a['id']==v['fixture']['artifact'])
        with (root/a['path']).open('rb') as stream:header=stream.read(12)
        assert header[:8]==b'PS2STATE' and int.from_bytes(header[8:12],'little')==3, 'Current fixture is not native v3'
    print(f"{label}: {len(v['artifacts'])} artifact hashes + {nested} evidence-tree members verified; no files changed")

def check_closure():
    return check_closure_record(load('pedal-closure'),ROOT)

def check_profiles():
    return check_profile_record(load('pedal-profiles'),ROOT)

def verify_profiles(root):
    verify_pedals(root)
    v=check_profiles();root=Path(root).resolve()
    verify_current(root,v,'Stopped profile characterization')
    artifacts={a['id']:a for a in v['artifacts']}
    plan=json.loads((root/artifacts['artifact:profiles-plan']['path']).read_text())
    assert summarize_profiles(plan)==v['observations'],'Observed profile inventory differs'
    stop=json.loads((root/artifacts['artifact:profiles-stop']['path']).read_text())
    assert len(stop['completed'])==v['results']['paired_cases_passed']
    assert sum(c['replaced'] for c in stop['completed'])==v['results']['exact_substitutions']
    log=(root/artifacts['artifact:profiles-time-trial-log']['path']).read_text()
    assert '[gt3-pedals] replaced=0 fallback=299 response_calls=0' in log
    snapshot=json.loads((root/artifacts['artifact:profiles-static']['path']).read_text())
    records=snapshot['evidence_bundle']['records']
    assert {r['evidence_id'] for r in records}==set(v['static_evidence_ids'])
    assert all(r['subject']['digest']['sha256']==load('manifest')['original_elf_sha256'] for r in records)
    print('Historical unsupported context retained; that stopped record makes no expanded claim. Current closure is a separate authority.')

def check():
    m, s, t, p = (load(n) for n in ('manifest', 'symbols', 'types', 'provenance'))
    for d in (m,s,t,p): assert d['schema_version'] == 1, 'Unsupported schema'
    artifacts = {a['id']:a for a in p['artifacts']}
    assert len(artifacts)==len(p['artifacts']), 'Duplicate artifact ID'
    pedals=check_pedals();check_profiles();check_closure()
    assert p['pedal_profile_characterization_registry']=='pedal-profiles.json'
    assert p['pedal_admission_audit_registry']=='pedal-admission-49af40.json'
    assert p['pedal_closure_registry']=='pedal-closure.json'
    check_admission_record(load('pedal-admission-49af40'))
    pedal_artifacts={a['id']:a for a in pedals['artifacts']}
    assert not set(artifacts)&set(pedal_artifacts), 'Evidence contexts must not collide'
    closure_artifacts={a['id']:a for a in check_closure()['artifacts']}
    assert not (set(artifacts)|set(pedal_artifacts)) & set(closure_artifacts)
    refs = set(artifacts)|set(pedal_artifacts)|set(closure_artifacts)
    for a in p['artifacts']:
        assert re.fullmatch(r'[0-9a-f]{64}', a['sha256']), 'Malformed artifact hash'
        assert a['visibility'] == 'private', 'Raw evidence must remain private'
        assert not Path(a['path']).is_absolute() and '..' not in Path(a['path']).parts
    for e in p['evidence_ids']:
        assert e['artifact'] in artifacts, e
        assert e['id'] not in refs, f'Duplicate evidence ID: {e}'
        refs.add(e['id'])
    assert re.fullmatch(r'[0-9a-f]{64}', m['original_elf_sha256'])
    assert m['snapshot_context']['validation_scope'] == 'preserved-private-experiment'
    assert m['snapshot_context']['current_main_runtime_integration'].startswith('not-installed')
    assert len({f['id'] for f in m['functions']})==len(m['functions']), 'Duplicate function ID'
    address=lambda a: bool(re.fullmatch(r'0x[0-9a-f]{8}', a))
    def evidence(es):
        assert es and all(e in refs for e in es), f'Unresolved/missing evidence: {es}'
    for f in m['functions']:
        assert address(f['address']), f['address']
        assert f['lifecycle'] in m['lifecycle_order'], f['lifecycle']
        for k in ('confidence','generated_oracle','uncertainties','next_action'):assert f[k], (f['id'],k)
        assert isinstance(f['dependencies'],list), f['id']
        evidence(f['evidence'])
        for dep in f['dependencies']:assert address(dep), dep
        for k in ('differential','runtime','live'):assert f[k]['status'], (f['id'],k)
        for k in ('differential','live'):
            if f[k].get('evidence'):evidence(f[k]['evidence'])
        for src in f['generated_oracle']:
            assert not Path(src).is_absolute() and '..' not in Path(src).parts, src
        if f['recovered_source']:assert (ROOT/f['recovered_source']).is_file(), f
        if f['lifecycle']=='frozen':
            assert f['differential']['status']=='passing' and f['runtime']['status']=='opt-in-integrated' and f['live']['status']=='validated-bounded', f['id']
            assert f['recovered_source'] and f['runtime']['default']=='generated', f['id']
            lo,hi=map(lambda x:int(x,16),f['boundary']); assert lo<=hi and address(f['gate_address'])
            assert lo==int(f['gate_address'],16), f['id']
            if lo!=int(f['address'],16):assert int(f['resume_address'],16)==hi+1, f['id']
    assert len({e['address'] for e in s['functions']})==len(s['functions']), 'Duplicate canonical symbol'
    for e in s['functions']+s['data']:
        assert address(e['address']) and e['name'];evidence(e['evidence'])
    for layout in t['layouts']:
        assert (ROOT/layout['source']).is_file()
        assert len({f['name'] for f in layout['fields']})==len(layout['fields'])
        for f in layout['fields']:
            assert 0<=int(f['offset'],16)<int(layout['size'],16);evidence(f['evidence'])
    for f in t['observations']['fields']:evidence(f['evidence'])
    current=check_current()
    for f in m['functions']:
        if 'current_validation' in f:assert f['current_validation']==current['id']
        if 'pedal_closure' in f:assert f['pedal_closure']==check_closure()['id']
        if 'pedal_validation' in f:
            assert f['pedal_validation']==pedals['id'] and f['lifecycle']==pedals['lifecycle']
            assert f['validation_context']==pedals['context'] and f['runtime']['scope']=='validation-only'
            assert f['boundary']==pedals['boundary'] and f['resume_address']==pedals['resume_address']
    return m,s,t,p

def docs():
    m,s,t,p=check(); dest=ROOT/'docs/site/docs'; (dest/'registry').mkdir(parents=True,exist_ok=True)
    def page(name,title,text):
        (dest/'registry'/name).write_text(f'---\ntitle: "{title}"\n---\n\n<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->\n\n'+text.rstrip()+'\n')
    counts=Counter(f['lifecycle'] for f in m['functions'])
    text='## Lifecycle inventory\n\nThe default context is the **preserved private experiment**, not canonical current-main installation. The new pedal record explicitly overrides that historical context: see [pedal validation](pedal-validation.md). Fresh isolated baseline validation is tracked in [current validation](current-validation.md); canonical ps2run retains generated execution.\n\nThis is **selected evidence inventory, not whole-game recovery coverage**. Identified entries are not authorized replacements. Dependencies from pseudocode remain candidates.\n\n'
    text+='\n'.join(f'- **{k}**: {counts[k]}' for k in m['lifecycle_order'])+'\n\n'
    text+='| Original entry | Semantic name | State | Diff | Runtime | Live |\n|---|---|---|---|---|---|\n'
    for f in m['functions']:text+=f"| `{f['address']}` | `{f['name']}` | {f['lifecycle']} | {f['differential']['status']} | {f['runtime']['status']} | {f['live']['status']} |\n"
    page('status.md','Decompilation status',text)
    text='Authoritative inventory: `decomp/gt3/symbols.json`. Names ending in `candidate` and unclassified names are deliberately uncertain. Requested selectors are NOT automatically independent function entries. Look up complete records with `just lookup ADDRESS`.\n\n| Canonical guest address | Semantic name | Name confidence | Evidence |\n|---|---|---|---|\n'
    for e in s['functions']+s['data']:
        text+=f"| `{e['address']}` | `{e['name']}` | {e.get('name_confidence',e.get('confidence','unknown'))} | "+', '.join('`'+x+'`' for x in e['evidence'])+' |\n'
    page('symbols.md','Address and symbol inventory',text)
    text='Authoritative inventory: `decomp/gt3/types.json`. Offset assertions are generated into `build/foundation/type-assertions.cpp` and compiled with `just check`. All guest pointers are 32-bit little-endian; EE floats retain bit patterns. **Do not treat opaque padding as recovered fields or bulk-write it.**\n'
    for l in t['layouts']:
        text+=f"\n## {l['name']}\n\nSize `{l['size']}`. {l['coverage']}. Source: `{l['source']}`.\n\n| Offset | Field | Representation | Meaning |\n|---|---|---|---|\n"
        for f in l['fields']:text+=f"| `{f['offset']}` | `{f['name']}` | `{f['type']}` | {f['meaning']} |\n"
    text+='\n## Untyped car observations\n\nThese offsets do **not** extend the C++ layout or authorize writes.\n\n| Offset | Provisional name | Confidence | Meaning |\n|---|---|---|---|\n'
    for f in t['observations']['fields']:text+=f"| `{f['offset']}` | `{f['name']}` | {f['confidence']} | {f['meaning']} |\n"
    page('types.md','Partial type knowledge',text)
    current=check_current()
    text='Historical function lifecycle remains separate. This page describes **current-main source with an isolated validation-only harness**, not canonical runtime installation.\n\n'
    text+=f"Source base: `{current['source_commit']}`.\n\n| Gate | Current result |\n|---|---|\n"
    for key in ('build','regressions','live'):text+=f"| {key} | {current[key]} |\n"
    text+=f"| native v3 fixture | {current['fixture']['status']} |\n\n"
    text+='\n'.join('- '+s for s in current['limitations'])+'\n\n'
    text+='Private evidence is fingerprinted in `decomp/gt3/current-validation.json`; use `just verify-current EXPLICIT_REPOSITORY_ROOT`. Raw snapshots, binaries, traces and captures are not published. See [current baseline](../current-baseline.md).\n'
    page('current-validation.md','Current-main native baseline',text)
    pedals=check_pedals()
    text=f"Source base: `{pedals['source_commit']}` plus documented source overlay. Lifecycle: **{pedals['lifecycle']}**. **Validation-only**, not canonical integration.\n\n"
    text+='| Gate | Result |\n|---|---|\n'+''.join(f'| {k} | {pedals[k]} |\n' for k in ('build','differential','regressions','live'))
    text+='\n'+''.join('- '+item+'\n' for item in pedals['limitations'])
    text+='\nUse `just verify-pedals EXPLICIT_REPOSITORY_ROOT` for strict private verification. See [pedal recovery](../pedal-v1.md) and [join contract](../pedal-join-contract.md).\n'
    page('pedal-validation.md','Pedal v1 validation',text)
    profiles=check_profiles()
    text='**Stopped at an unsupported reachable context; no Frozen expansion.**\n\n'
    text+=f"Original-only observations: {profiles['observations']['original_updates']}; descriptor families: 1; processing configurations: 5. Four paired cases pass 1,200 substitutions. Time Trial stops with 0 replacements / 299 protective fallbacks.\n\n"
    text+='Fresh full native regressions and remaining pairs were not run after stop. See [reachability report](../pedal-profiles.md). Strict retained-evidence check: `just verify-pedal-profiles EXPLICIT_REPOSITORY_ROOT`.\n'
    text+='\nThis is the immutable earlier stop, not the current admission result. See [observed-context closure](../pedal-closure.md).\n'
    page('pedal-profiles.md','Historical stopped pedal profile characterization',text)
    closure=check_closure()
    text=f"Lifecycle: **{closure['lifecycle']}**; isolated validation only, both gates default OFF. Boundary unchanged.\n\n"
    text+='| Gate | Result |\n|---|---|\n'+''.join(f'| {k} | {value} |\n' for k,value in closure['gates'].items())
    text+='\n4,199 actual-context full-CPU/32MiB/cost/mutation shadow comparisons and 4,199 guarded substitutions, zero fallback, across all 14 observed contexts / five processing classes. Not universal or physical-device proof.\n\n'
    text+='See [closure report](../pedal-closure.md). Strict private verification: `just verify-pedal-closure EXPLICIT_REPOSITORY_ROOT`. Historical stopped records/hashes are not rewritten.\n'
    page('pedal-closure.md','Pedal v1 observed-context closure',text)
    knowledge=ROOT/'docs/site/static/knowledge';knowledge.mkdir(parents=True,exist_ok=True)
    for name in ('manifest','symbols','types','provenance','current-validation','pedal-validation','pedal-profiles','pedal-admission-49af40','pedal-closure'):
        (knowledge/f'{name}.json').write_bytes((DB/f'{name}.json').read_bytes())
    print('Public documentation generated: facts/metadata only; no raw evidence copied')

def verify_private(root):
    m,s,t,p=check()
    root=Path(root).resolve()
    for a in p['artifacts']:
        path=root/a['path']
        assert path.is_file(), f'Missing private artifact: {a["id"]}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256'], f'EVIDENCE CHANGED: {a["id"]}; do not rehash'
    assert hashlib.sha256((root/'games/gt3-usa-v110/core.elf').read_bytes()).hexdigest()==m['original_elf_sha256'], 'Wrong original ELF profile'
    artifacts={a['id']:a for a in p['artifacts']}
    for e in p['evidence_ids']:
        raw=json.loads((root/artifacts[e['artifact']]['path']).read_text())
        assert any(r['evidence_id']==e['id'] for r in raw['records']), e
    print(f'Private original profile, {len(p["artifacts"])} artifact hashes and {len(p["evidence_ids"])} evidence IDs verified; no files changed')

def type_assertions():
    t=load('types');out=ROOT/'build/foundation/type-assertions.cpp';out.parent.mkdir(parents=True,exist_ok=True)
    lines=['#include "'+Path(source).name+'"' for source in sorted({l['source'] for l in t['layouts']})]+['#include <cstddef>']
    for l in t['layouts']:
        lines.append(f"static_assert(sizeof({l['cpp']}) == {l['size']});")
        for f in l['fields']:lines.append(f"static_assert(offsetof({l['cpp']}, {f['name']}) == {f['offset']});")
    out.write_text('\n'.join(lines)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['check','docs','status','lookup','evidence','type-assertions','verify-private','verify-current','verify-pedals','verify-pedal-profiles']);parser.add_argument('query',nargs='?');a=parser.parse_args()
    if a.command=='verify-private':
        if not a.query:parser.error('explicit private experiment root required')
        verify_private(a.query);return
    if a.command=='verify-current':
        if not a.query:parser.error('explicit current repository root required')
        verify_current(a.query);return
    if a.command=='verify-pedal-profiles':
        if not a.query:parser.error('explicit current repository root required')
        verify_profiles(a.query);return
    if a.command=='verify-pedals':
        if not a.query:parser.error('explicit current repository root required')
        verify_pedals(a.query);return
    if a.command=='type-assertions':type_assertions();return
    if a.command=='docs':docs();return
    m,s,t,p=check()
    if a.command=='check':print(f"Public metadata consistency PASS (not private verification): {len(m['functions'])} records, {len(s['functions'])} canonical functions, {len(p['artifacts'])} hashed artifacts");return
    if a.command=='status':print(json.dumps(Counter(f['lifecycle'] for f in m['functions']),indent=2));return
    if not a.query:parser.error('query required')
    q=a.query.lower()
    try:q=f'0x{int(q,16):08x}'
    except ValueError:pass
    if a.command=='lookup':
        results=[e for e in m['functions']+s['data'] if q in e['address'] or q in e['name'].lower()]
        for layout in t['layouts']+[dict(name='untyped car-like observations',fields=t['observations']['fields'])]:
            for f in layout['fields']:
                offset=f"0x{int(f['offset'],16):08x}"
                if q==offset or q in f['name'].lower():
                    results.append(dict(kind='field-offset-not-absolute-address',owner=layout['name'],**f))
        print(json.dumps(results,indent=2));return
    results=[f for f in m['functions'] if q in f['address'] or q in f['name'].lower()]
    refs={e for f in results for e in f['evidence']}
    print(json.dumps({'context':m['snapshot_context'], 'references':sorted(refs),
                      'private_verification':'just verify-private EXPLICIT_ROOT'},indent=2))
if __name__=='__main__':
    try:main()
    except (AssertionError,KeyError,OSError,ValueError) as e:print('Metadata FAIL:',e,file=sys.stderr);sys.exit(1)
