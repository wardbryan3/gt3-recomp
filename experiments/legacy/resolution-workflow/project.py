#!/usr/bin/env python3
"""Authoritative JSON inventories -> lookup/check/documentation. Never modifies evidence."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'decomp/gt3'
def load(name): return json.loads((DB / (name + '.json')).read_text())
def check():
    m, s, t, p = (load(n) for n in ('manifest', 'symbols', 'types', 'provenance'))
    for d in (m,s,t,p): assert d['schema_version'] == 1, 'Unsupported schema'
    artifacts = {a['id']:a for a in p['artifacts']}
    assert len(artifacts)==len(p['artifacts']), 'Duplicate artifact ID'
    refs = set(artifacts)
    for a in p['artifacts']:
        path=ROOT/a['path'];assert path.is_file(), f'Missing retained evidence: {path}'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256'], f'EVIDENCE CHANGED: {path}; do not silently rehash'
    for e in p['evidence_ids']:
        assert e['artifact'] in artifacts, e
        assert e['id'] not in refs, f'Duplicate evidence ID: {e}'
        raw=json.loads((ROOT/artifacts[e['artifact']]['path']).read_text())
        assert any(r['evidence_id']==e['id'] for r in raw['records']), e
        refs.add(e['id'])
    elf=ROOT/'games/gt3-usa-v110/core.elf'
    assert hashlib.sha256(elf.read_bytes()).hexdigest()==m['original_elf_sha256'], 'Wrong ELF profile'
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
        for src in f['generated_oracle']:assert (ROOT/src).is_dir(), src
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
    return m,s,t,p

def docs():
    m,s,t,p=check(); dest=ROOT/'docs/site/docs'; (dest/'generated').mkdir(parents=True,exist_ok=True)
    def page(name,title,text):
        (dest/'generated'/name).write_text(f'---\ntitle: "{title}"\n---\n\n<!-- Generated from decomp/gt3 JSON; edit metadata, not this page. -->\n\n'+text+'\n')
    counts=Counter(f['lifecycle'] for f in m['functions'])
    text='## Lifecycle inventory\n\nThis is **selected evidence inventory, not whole-game recovery coverage**. Identified entries are not authorized replacements. Dependencies from pseudocode remain candidates.\n\n'
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
    baseline=dest/'baseline';baseline.mkdir(exist_ok=True)
    for name in ['gt3-controls','gt3-steering-trace','gt3-wheel-steering-trace','gt3-clean-steering','gt3-synthetic-wheel-experiment']:
        text=(ROOT/'docs'/f'{name}.md').read_text()
        # Render-only URL adaptation: immutable source and download bytes remain unchanged.
        text=re.sub(r'\]\((gt3-[a-z-]+\.json)\)', r'](/docs/baseline/\1)', text)
        (baseline/f'{name}.md').write_text('---\ntitle: "Retained: '+name+'"\n---\n\n> Mirrored from the unchanged repository evidence narrative. Edit the source document, not this generated mirror.\n\n'+text)
    static=ROOT/'docs/site/static/docs/baseline';static.mkdir(parents=True,exist_ok=True)
    for name in ['gt3-controls-evidence','gt3-steering-evidence','gt3-wheel-evidence','gt3-clean-steering-evidence']:
        (static/f'{name}.json').write_bytes((ROOT/'docs'/f'{name}.json').read_bytes())
    knowledge=ROOT/'docs/site/static/knowledge';knowledge.mkdir(parents=True,exist_ok=True)
    for name in ('manifest','symbols','types','provenance'):
        (knowledge/f'{name}.json').write_bytes((DB/f'{name}.json').read_bytes())
    print('Documentation generated; retained evidence untouched')

def type_assertions():
    t=load('types');out=ROOT/'build/foundation/type-assertions.cpp';out.parent.mkdir(parents=True,exist_ok=True)
    lines=['#include "'+Path(source).name+'"' for source in sorted({l['source'] for l in t['layouts']})]+['#include <cstddef>']
    for l in t['layouts']:
        lines.append(f"static_assert(sizeof({l['cpp']}) == {l['size']});")
        for f in l['fields']:lines.append(f"static_assert(offsetof({l['cpp']}, {f['name']}) == {f['offset']});")
    out.write_text('\n'.join(lines)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['check','docs','status','lookup','evidence','type-assertions']);parser.add_argument('query',nargs='?');a=parser.parse_args()
    if a.command=='type-assertions':type_assertions();return
    if a.command=='docs':docs();return
    m,s,t,p=check()
    if a.command=='check':print(f"Metadata/provenance PASS: {len(m['functions'])} records, {len(s['functions'])} canonical functions, {len(p['artifacts'])} hashed artifacts");return
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
    found=0
    for art in p['artifacts']:
        if art['kind']!='static-rea':continue
        data=json.loads((ROOT/art['path']).read_text())
        for r in data.get('records',[]):
            if r.get('operation')=='batch_decompile':
                for i in r['normalized_result']['items']:
                    if i['status']=='ok' and f"0x{int(i['procedure']['address'],16):08x}"==q:
                        print(r['evidence_id'],art['path'],i['procedure']);print(i['pseudocode']);found+=1
    if not found:print('No retained batch pseudocode for this canonical entry; inspect provenance/static dossier. Absence is not proof.',file=sys.stderr);sys.exit(1)
if __name__=='__main__':
    try:main()
    except (AssertionError,KeyError,OSError,ValueError) as e:print('Metadata FAIL:',e,file=sys.stderr);sys.exit(1)
