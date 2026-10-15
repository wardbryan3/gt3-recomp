#!/usr/bin/env python3
"""Separate virtual-pedal authority; never edits Frozen source or registries."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from gt3_virtual_pedal_proof import check_record,review_rows,sha
from characterize_gt3_pedal_profiles import read_rows,semantic
DB=ROOT/'decomp/gt3/virtual-pedals.json'
def load():return check_record(json.loads(DB.read_text()))
def docs():
 v=load();(ROOT/'docs/site/static/knowledge/virtual-pedals.json').write_bytes(DB.read_bytes())
 text='---\ntitle: Virtual pedal v1 experiment\n---\n\n<!-- Generated from decomp/gt3/virtual-pedals.json. -->\n\n'
 text+=f"Status: **{v['status']}**. Isolated validation only; build/runtime gates default OFF; no canonical installation.\n\n"
 text+='| Gate | Result |\n|---|---|\n'+''.join(f'| {k} | {s} |\n' for k,s in v['gates'].items())
 text+='\nHost [0,1] maps to Q12 0–4096, positive half ties up, at original command-builder return. No processed car writes or physical calibration. See [experiment report](../virtual-pedals.md).\n\nStrict private verification: `just verify-virtual-pedals EXPLICIT_REPOSITORY_ROOT`.\n'
 (ROOT/'docs/site/docs/registry/virtual-pedals.md').write_text(text)
def verify(root):
 v=load();root=Path(root).resolve()
 # Invoke unchanged inherited authorities, including every original private hash.
 subprocess.run(['just','verify-pedal-closure',str(root)],cwd=ROOT,check=True)
 subprocess.run(['just','verify-private',str(root/'local/legacy/resolution-repo')],cwd=ROOT,check=True)
 count=0
 def file(a):
  p=Path(a['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
  p=root/p;assert p.is_file() and sha(p)==a['sha256'],('MISSING/CHANGED virtual-pedal evidence',a['path']);return p
 for a in v['artifacts']:
  p=file(a)
  if a.get('kind')=='file-manifest':
   members=json.loads(p.read_text())['files'];assert members and len({m['path'] for m in members})==len(members)
   for m in members:file(m);count+=1
 base=root/'local/virtual-pedals-v1';live=base/'accepted-live';summary=json.loads((live/'summary.json').read_text())
 default=json.loads((base/'default-off-build/identity.json').read_text());gate=json.loads((base/'default-off-check.json').read_text())
 assert default['build_opt_in'] is False and default['runtime_default'] is False and not (base/'default-off-build/virtual-on').exists()
 assert gate['build_default'] is False and gate['runtime_enable_exit']==2 and 'build gate is OFF' in gate['stderr']
 assert gate['binary_sha256']==sha(base/'default-off-build/virtual-off')
 assert summary['validator_sha256']==sha(ROOT/'scripts/validate_gt3_virtual_pedals.py')
 assert len(summary['cases'])==12 and sum(c['entries'] for c in summary['cases'].values())==3599
 assert summary['defaults']['canonical_disabled_trace_build_off_exact'] is True
 identity=json.loads((base/'final-build/identity.json').read_text());assert summary['identity_sha256']==sha(base/'final-build/identity.json')
 assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
 for p,h in identity['sources'].items():assert sha(ROOT/p)==h
 for p,h in identity['files'].items():assert sha(base/'final-build'/p)==h
 parent=base/'final-parent';assert sha(parent/'pedal-build-identity.json')==identity['parent_identity_sha256']
 old_build=json.loads((parent/'base/build-identity.json').read_text())
 for p,h in old_build['source_hashes'].items():
  if Path(p).suffix in ('.cpp','.hpp'):assert sha(ROOT/p)==h,p
 assert sha(parent/'base/original/ps2run')=='b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a'
 def equal(d,e,cpu=True):
  assert sha(d/'memory.bin')==sha(e/'memory.bin')
  shots=lambda x:{p.name:sha(p) for p in (x/'shots').glob('*.ppm')}
  assert shots(d) and shots(d)==shots(e)
  if cpu:
   assert semantic(read_rows(d/'cpu.jsonl'))==semantic(read_rows(e/'cpu.jsonl'))
   assert (d/'steering.jsonl').read_bytes()==(e/'steering.jsonl').read_bytes()
 for name,c in summary['cases'].items():
  d=live/(name+'-generated');clean=live/(name+'-clean');repeat=live/(name+'-repeat');equal(d,clean);equal(d,repeat)
  assert (d/'virtual.jsonl').read_bytes()==(clean/'virtual.jsonl').read_bytes()==(repeat/'virtual.jsonl').read_bytes()
  rows=read_rows(d/'virtual.jsonl');review_rows(rows,c['entries'])
  for path in [d,clean,repeat]:
   cmd=json.loads((path/'command.json').read_text());argv=cmd['argv']
   assert sha(root/Path(argv[0]).relative_to(ROOT))==cmd['binary_sha256']
   state=root/Path(cmd['state']['path']).relative_to(ROOT);assert sha(state)==cmd['state']['sha256']
   with state.open('rb') as f:assert f.read(12)==b'PS2STATE'+(3).to_bytes(4,'little')
   assert cmd['env']['PS2_ONE_THREAD']=='1' and cmd['env']['GT3_BASELINE_UTC_EPOCH']=='1791964800'
  argv=json.loads((d/'command.json').read_text())['argv'];initial=tuple(map(float,argv[argv.index('--gt3-virtual-pedals')+1].split(':')))
  events=[argv[i+1].split(':') for i,a in enumerate(argv) if a=='--gt3-virtual-pedals-at']
  for row in rows:
   expected=initial
   for event in events:
    if int(event[0])<=row['frame']:expected=tuple(map(float,event[1:]))
   assert (row['host_throttle'],row['host_brake'])==expected,('wrong scheduled frame',name,row['frame'])
  assert c['pedal_counts']['replaced']==c['entries'] and c['pedal_counts']['fallback']==0
  assert c['counts']['injected']==c['counts']['restored']==c['counts']['brakes']==c['counts']['engines']==c['entries']
 equal(live/'default',live/'canonical',False);equal(live/'default',live/'trace-only');equal(live/'trace-only',live/'build-off-trace')
 assert '12291 cases / 24582 complete CPU+32MiB comparisons' in (base/'oracle-final.log').read_text()
 assert '8 mutation-free rejections' in (base/'oracle-final.log').read_text()
 for p,n in [('unchanged-pedal-live',19),('unchanged-current-live-accepted',28)]:assert len(json.loads((base/p/'summary.json').read_text())['cases'])==n
 closure=json.loads((base/'unchanged-profile-live/summary.json').read_text());assert sum(c['entries'] for c in closure['cases'].values())==4199
 assert all(c['clean_counts'][0]==c['entries'] and c['clean_counts'][1]==0 for c in closure['cases'].values())
 snapshot=json.loads((base/'static.snapshot.json').read_text())['evidence_bundle']['records']
 assert {r['evidence_id'] for r in snapshot}==set(v['static_evidence_ids'])
 assert all(r['subject']['digest']['sha256']=='b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763' for r in snapshot)
 assert json.loads((base/'protected-before.json').read_text())==v['protected']
 if v['status']=='validated-bounded':assert 'All current native baseline regressions PASS' in (base/'regressions/regressions.log').read_text()
 print(f'Virtual pedal proof PASS: {len(v["artifacts"])} artifacts / {count} members; 3599 generated/clean/repeated virtual updates; immutable Frozen proof preserved; no physical calibration claim')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','docs','verify']);p.add_argument('root',nargs='?',type=Path);a=p.parse_args()
 if a.command=='check':load();print('Virtual pedal public consistency PASS (not private/game proof)')
 elif a.command=='docs':docs()
 else:
  if not a.root:p.error('explicit private repository root required')
  verify(a.root)
