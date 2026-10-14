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

def verify_current(root):
    v=check_current(); root=Path(root).resolve()
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
    print(f"Current validation: {len(v['artifacts'])} artifact hashes + {nested} evidence-tree members verified; no files changed")

def check():
    m, s, t, p = (load(n) for n in ('manifest', 'symbols', 'types', 'provenance'))
    for d in (m,s,t,p): assert d['schema_version'] == 1, 'Unsupported schema'
    artifacts = {a['id']:a for a in p['artifacts']}
    assert len(artifacts)==len(p['artifacts']), 'Duplicate artifact ID'
    refs = set(artifacts)
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
    return m,s,t,p

def docs():
    m,s,t,p=check(); dest=ROOT/'docs/site/docs'; (dest/'registry').mkdir(parents=True,exist_ok=True)
    def page(name,title,text):
        (dest/'registry'/name).write_text(f'---\ntitle: "{title}"\n---\n\n<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->\n\n'+text.rstrip()+'\n')
    counts=Counter(f['lifecycle'] for f in m['functions'])
    text='## Lifecycle inventory\n\nStatuses describe the **preserved private experiment**, not canonical current-main installation. Fresh isolated validation is tracked separately in [current validation](current-validation.md); canonical ps2run retains generated execution.\n\nThis is **selected evidence inventory, not whole-game recovery coverage**. Identified entries are not authorized replacements. Dependencies from pseudocode remain candidates.\n\n'
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
    knowledge=ROOT/'docs/site/static/knowledge';knowledge.mkdir(parents=True,exist_ok=True)
    for name in ('manifest','symbols','types','provenance','current-validation'):
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
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['check','docs','status','lookup','evidence','type-assertions','verify-private','verify-current']);parser.add_argument('query',nargs='?');a=parser.parse_args()
    if a.command=='verify-private':
        if not a.query:parser.error('explicit private experiment root required')
        verify_private(a.query);return
    if a.command=='verify-current':
        if not a.query:parser.error('explicit current repository root required')
        verify_current(a.query);return
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
