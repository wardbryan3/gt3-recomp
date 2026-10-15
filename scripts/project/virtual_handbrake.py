#!/usr/bin/env python3
"""Separate virtual-input authority; does not modify any Frozen authority/checker."""
import argparse,json,re,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from gt3_virtual_handbrake_proof import digest,read_rows,semantic,review_rows
DB=ROOT/'decomp/gt3/virtual-handbrake.json'
BASE='local/virtual-handbrake-v1'
CONTEXTS=['trusted','altezza-mt','alfa-at','mrs-at','time-trial','free-run','license','pad-left-stick-at','pad-left-stick-mt','pad-dpad-at','compat-wheel-at','compat-wheel-mt']
CASES=CONTEXTS+['zero','half','full','all-q12-native']
def check_record(v,root=ROOT):
 assert v['schema_version']==1 and v['id']=='synthetic-virtual-handbrake-v1'
 assert v['status'] in ['validating','validated-bounded'] and v['stop'] is True
 assert v['original_elf_sha256']=='b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763'
 assert v['mapping']==dict(host_type='finite-binary64',range=[0,1],scale=4096,rounding='nearest-positive-half-up',reject_out_of_range=True,physical_calibration=False)
 assert v['boundary']==dict(inject='0x001e4d5c',restore='0x001e4e68',command_bytes=[0,14,15],analog_flag=16,command_halfword=14)
 for field in ['build_default','runtime_default','canonical_installation','frozen_modified','writes_processed_car_state','physical_device_proof']:assert v[field] is False
 assert v['coverage']==dict(values_per_calibration=24585,calibrations=2,oracle_cases=49170,full_cpu_ram_comparisons=98340,original_semantic_observations=393360,rear_formula_checks=590040,mutation_free_rejections_per_calibration=10,invalid_values_per_calibration=7,live_cases=16,live_runs=52,live_substitutions=8596,live_injections=25788,live_fallbacks=0,live_q12_codes=4097,fixture_identities=7)
 assert v['unknowns'] and v['failures'] and re.fullmatch('[0-9a-f]{40}',v['source_commit'])
 frozen=json.loads((root/'decomp/gt3/handbrake.json').read_text())
 protected=set(frozen['sources'])|set(frozen['protected'])|{'decomp/gt3/handbrake.json','host/main.cpp','CMakeLists.txt','justfile','handbrake.just','host/gt3_virtual_pedals.cpp','host/gt3_virtual_pedals.hpp','decomp/gt3/virtual-pedals.json'}
 assert protected<=set(v['protected'])
 for section in ['sources','protected']:
  assert v[section]
  for path,sha in v[section].items():
   assert not Path(path).is_absolute() and '..' not in Path(path).parts
   assert digest(root/path)==sha,('source/protected drift',path)
 assert json.loads((root/'decomp/gt3/manifest.json').read_text())['virtual_handbrake']==dict(id=v['id'],registry='virtual-handbrake.json',scope='validation-only')
 required={BASE+'/'+name+'-files.json' for name in ['accepted-build','default-off-build','accepted-live','regression','failure']}
 assert required<={a['path'] for a in v['artifacts'] if a['kind']=='file-manifest'}
 for a in v['artifacts']:assert a['path'].startswith('local/') and re.fullmatch('[0-9a-f]{64}',a['sha256'])
 assert len(v['static_evidence_ids'])==3
 if v['status']=='validated-bounded':assert v['gates'] and all(s=='passing' for s in v['gates'].values())
 return v
def load():return check_record(json.loads(DB.read_text()))
def docs():
 v=load();(ROOT/'docs/site/static/knowledge/virtual-handbrake.json').write_bytes(DB.read_bytes())
 text='---\ntitle: Virtual handbrake authority\n---\n\n# Virtual handbrake v1 authority\n\n'
 text+=f"Status: **{v['status']}**. Separate virtual-input experiment, not a Frozen processor change or canonical installation.\n\n"
 text+='Protocol: finite normalized binary64 [0,1], nearest Q12 / positive half ties up; invalid input rejects, never clamps. Original floor/processing/downstream remain in GT3.\n\n'
 text+='| Gate | Result |\n|---|---|\n'+''.join(f'| {k} | {s} |\n' for k,s in v['gates'].items())
 text+='\n49,170 original oracle cases /98,340 complete final CPU+32MiB comparisons;52 native-v3 runs /8,596 clean substitutions /zero fallback; all4,097 Q12 codes reached live.\n\n'
 text+='12 representative contexts, seven v3 fixture identities, five UI-identified cars plus an unidentified Time Trial preset; Arcade Single Race/Time Trial/Free Run and Simulation B-1, AT and MT. This is bounded evidence, not all-game/browser/physical proof.\n\n'
 text+='[Full report](../virtual-handbrake.md). Strict proof: `just --justfile virtual-handbrake.just verify-virtual-handbrake EXPLICIT_ROOT`. No raw evidence is published.\n'
 (ROOT/'docs/site/docs/registry/virtual-handbrake.md').write_text(text)
def verify(root):
 v=load();root=Path(root).resolve(strict=True);count=0
 def file(a):
  path=Path(a['path']);assert not path.is_absolute() and '..' not in path.parts and path.parts[0]=='local'
  path=root/path;assert path.is_file() and digest(path)==a['sha256'],('MISSING/CHANGED virtual handbrake evidence',a['path']);return path
 def remap(path):return root/Path(path).relative_to(ROOT)
 for a in v['artifacts']:
  path=file(a)
  if a['kind']=='file-manifest':
   members=json.loads(path.read_text())['files'];assert members and len({m['path'] for m in members})==len(members)
   for member in members:file(member);count+=1
 base=root/BASE;build=base/'accepted-build';identity=json.loads((build/'identity.json').read_text())
 assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
 for p,h in identity['files'].items():assert digest(build/p)==h,p
 for p,h in identity['sources'].items():assert digest(ROOT/p)==h,p
 frozen=remap(identity['parent_build']);assert digest(frozen/'identity.json')==identity['parent_identity_sha256']
 old=json.loads((frozen/'identity.json').read_text());parent=remap(old['parent_build']);old_build=json.loads((parent/'base/build-identity.json').read_text())
 elf=root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf';iso=root/'local/game-input/gt3-usa-v1.10.iso';clock=parent/'base/fixed-clock.so';canonical=parent/'base/original/ps2run'
 assert digest(elf)==v['original_elf_sha256']
 for p in [elf,clock,canonical]:assert old_build['inputs_and_executables'][str(ROOT/p.relative_to(root))]==digest(p)
 frozen_authority=json.loads((ROOT/'decomp/gt3/handbrake.json').read_text())
 iso_pin=next(a for a in frozen_authority['artifacts'] if a['path']=='local/game-input/gt3-usa-v1.10.iso')
 assert digest(iso)==iso_pin['sha256']
 for p,h in old_build['source_hashes'].items():
  if Path(p).suffix in ['.cpp','.hpp']:assert digest(ROOT/p)==h,p
 off=base/'default-off-build';assert not json.loads((off/'identity.json').read_text())['build_opt_in'] and not (off/'virtual-on').exists()
 assert 'build gate is OFF' in (base/'default-off-rejection.log').read_text()
 assert digest(off/'virtual-off')==digest(build/'virtual-off')
 for i in range(17):
  log=(base/f'live-attempt-2/invalid-{i}.log').read_text()
  assert log.startswith('Virtual handbrake: ') and '[gt3-virtual-handbrake] injected=' not in log
 for name in ['oracle-initial.log','oracle-runtime-accepted.log']:
  log=(base/name).read_text();assert 'cases=24585 full-CPU+32MiB-comparisons=49170 semantic-observations=196680 rear-formula-checks=295020 rejected-contexts=10 invalid-values=7' in log
 table={(r['floor'],r['q']):r for name in ['original-initial-results.jsonl','original-runtime-accepted-results.jsonl'] for r in read_rows(base/name)}
 assert set(table)=={(floor,q) for floor in [0x3dcccccc,0x3dcccccd] for q in range(4097)}
 for floor in [0x3dcccccc,0x3dcccccd]:
  values=[table[floor,q]['processed'] for q in range(4097)]
  assert values[0]==0 and values[-1]==0x3f800000 and all(a<b for a,b in zip(values,values[1:]))
 static=json.loads((base/'static.json').read_text());assert {r['evidence_id'] for r in static['records']}==set(v['static_evidence_ids'])
 live=base/'live-attempt-2';summary=json.loads((live/'summary.json').read_text())
 assert summary['identity_sha256']==digest(build/'identity.json') and summary['validator_sha256']==digest(ROOT/'scripts/validate_gt3_virtual_handbrake.py')
 assert summary['clock_sha256']==digest(clock) and summary['canonical_sha256']==digest(canonical)
 assert summary['total_clean_substitutions']==8596 and summary['live_runs']==52 and set(summary['cases'])==set(CASES)
 for p,h in summary['original_tables'].items():assert digest(remap(p))==h
 def equal(left,right,trace=True):
  assert digest(left/'memory.bin')==digest(right/'memory.bin')
  shots=lambda d:{p.name:digest(p) for p in (d/'shots').glob('*.ppm')}
  assert shots(left) and shots(left)==shots(right)
  if trace:
   assert (left/'virtual.jsonl').read_bytes()==(right/'virtual.jsonl').read_bytes()
   assert semantic(read_rows(left/'cpu.jsonl'))==semantic(read_rows(right/'cpu.jsonl'))
   assert (left/'steering.jsonl').read_bytes()==(right/'steering.jsonl').read_bytes()
 equal(live/'default',live/'canonical',False);equal(live/'trace-only',live/'canonical',False);equal(live/'trace-only',live/'build-off-trace')
 def counts(d,label):
  match=re.search(r'\['+label+r'\] ([^\n]+)',(d/'run.log').read_text());assert match
  return {k:int(s) for k,s in re.findall(r'(\w+)=(\d+)',match[1])}
 for d in ['default','trace-only','build-off-trace']:assert counts(live/d,'gt3-virtual-handbrake')['injected']==counts(live/d,'gt3-handbrake')['replaced']==0
 def scheduled(extra,frame):
  value=float(extra[extra.index('--gt3-virtual-handbrake')+1]);events=[]
  for i,flag in enumerate(extra):
   if flag=='--gt3-virtual-handbrake-at':
    at,val=extra[i+1].split(':');events.append((int(at),float(val)))
  assert all(a[0]<b[0] for a,b in zip(events,events[1:]))
  for at,val in events:
   if at>frame:break
   value=val
  return value
 labels={r['id']:r['labels'] for r in json.loads((root/'local/pedal-profiles-v1/plan.json').read_text())['cases']}
 fixtures=set();all_codes=set()
 for name,item in summary['cases'].items():
  n=item['entries'];assert n==(4097 if name=='all-q12-native' else 299 if name=='time-trial' else 300)
  context=item['context'];assert context in CONTEXTS
  original_meta=json.loads((root/f'local/pedal-profiles-v1/{context}-original/command.json').read_text())
  assert item['state']==original_meta['state'] and item['labels']==labels[context];fixtures.add(item['state']['sha256'])
  state=remap(item['state']['path']);assert digest(state)==item['state']['sha256']
  with state.open('rb') as f:assert f.read(12)==b'PS2STATE'+struct.pack('<I',3)
  g,c,r=[live/(name+'-'+suffix) for suffix in ['generated','clean','repeat']]
  equal(g,c);equal(g,r)
  for d,clean in [(g,False),(c,True),(r,False)]:
   assert 'frame limit reached' in (d/'run.log').read_text()
   cmd=json.loads((d/'command.json').read_text());assert cmd['binary_sha256']==digest(build/'virtual-on') and cmd['state']==item['state']
   assert cmd['source_command_sha256']==digest(root/f'local/pedal-profiles-v1/{context}-original/command.json')
   assert cmd['context']==context and cmd['labels']==labels[context]
   assert remap(cmd['argv'][cmd['argv'].index('--load-state')+1])==state
   assert int(cmd['argv'][cmd['argv'].index('--frames')+1])==int(item['stop'] if item['stop'] is not None else original_meta['argv'][original_meta['argv'].index('--frames')+1])
   assert remap(cmd['argv'][1])==elf and remap(cmd['argv'][cmd['argv'].index('--disc')+1])==iso
   assert cmd['env']['PS2_ONE_THREAD']=='1' and cmd['env']['GT3_BASELINE_UTC_EPOCH']=='1791964800' and remap(cmd['env']['LD_PRELOAD'])==clock
   assert ('--gt3-clean-handbrake' in cmd['argv']) is clean
   expected=dict(injected=n,restored=n,entries=n,joins=n,brakes=n,brake_joins=n,engines=n,shifts=n)
   assert counts(d,'gt3-virtual-handbrake')==expected
   hb=counts(d,'gt3-handbrake');assert hb['replaced']==(n if clean else 0) and hb['fallback']==0
   rows=read_rows(d/'virtual.jsonl');codes=review_rows(rows,n,table);all_codes|=codes
   assert codes==set(item['command_codes'])
   entries={row['frame']:row for row in rows if row['stage']=='entry'}
   for frame,row in entries.items():assert row['host_value']==scheduled(item['argv_extra'],frame)
   cpu=read_rows(d/'cpu.jsonl')
   for pc in [0x1e4bb8,0x1e4c60,0x1e4c74,0x1e3a90,0x1e3aac,0x1e3ab8,0x1e6ec8,0x1e6fc8,0x1e7500]:assert sum(row['pc']==pc for row in cpu)==n
   for row in cpu:
    assert int(row['cpu'][1096:1104],16)==row['pc']
    if row['pc']==0x1e4bb8:
     packet=entries[row['frame']]['bytes'];assert row['input']==packet[14]+256*packet[15] and row['flags']==packet[0]
    if row['pc']==0x1e3aac:assert int(row['cpu'][6*32:6*32+8],16)==(1 if row['processed']==0 else 0)
  if name=='all-q12-native':assert codes==set(range(4097))
 assert len(fixtures)==7 and all_codes==set(range(4097))
 assert 'All current native baseline regressions PASS' in (base/'regressions/regressions.log').read_text()
 fresh_base=base/'fresh-handbrake';fresh=json.loads((fresh_base/'summary.json').read_text())
 assert len(fresh['cases'])==23 and sum(row.get('replaced',0) for row in fresh['cases'].values())==1800
 assert all(row.get('fallback',0)==0 for row in fresh['cases'].values())
 assert fresh['validator_sha256']==digest(ROOT/'scripts/validate_gt3_handbrake.py') and fresh['build_identity_sha256']==digest(frozen/'identity.json')
 for name,item in fresh['cases'].items():
  d=fresh_base/name;assert digest(d/'memory.bin')==item['memory_sha256']
  assert {p.name:digest(p) for p in (d/'shots').glob('*.ppm')}==item['captures']
 for scenario in ['neutral','handbrake_hold','accel_handbrake_release','brake_handbrake','turn_shift','wheel_compatibility']:
  g,c,r=[fresh_base/(prefix+'_'+scenario) for prefix in ['generated','clean','repeat']]
  for d in [c,r]:
   assert digest(d/'memory.bin')==digest(g/'memory.bin')
   assert semantic(read_rows(d/'handbrake.jsonl'))==semantic(read_rows(g/'handbrake.jsonl'))
   assert (d/'steering.jsonl').read_bytes()==(g/'steering.jsonl').read_bytes()
  assert fresh['cases']['clean_'+scenario]['replaced']==300
 subprocess.run(['just','--justfile','handbrake.just','verify-handbrake',str(root)],cwd=ROOT,check=True)
 print(f'Virtual handbrake strict proof PASS: {count} pinned members;49170 original cases /98340 full CPU+32MiB comparisons;52 native runs /8596 substitutions /4097 codes /7 fixtures /zero fallback; Frozen and canonical unchanged')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','docs','verify']);p.add_argument('root',nargs='?');args=p.parse_args()
 if args.command=='check':load();print('Virtual handbrake public consistency PASS (not original-game proof)')
 elif args.command=='docs':docs()
 else:
  if not args.root:p.error('explicit private root required')
  verify(args.root)
if __name__=='__main__':main()
