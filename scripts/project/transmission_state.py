#!/usr/bin/env python3
"""Separate state authority; public checks never read proprietary artifacts."""
import argparse
from collections import Counter,defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).resolve().parents[2]
DB=ROOT/'decomp/gt3/transmission-state.json'
HOME='local/transmission-state-v1'
SOURCES=['host/gt3_transmission_state.cpp','host/gt3_transmission_state.hpp',
 'host/gt3_clean_transmission_admission.cpp','host/gt3_clean_transmission_admission.hpp',
 'scripts/validate_gt3_transmission_state.py','scripts/project/transmission_state.py',
 'tests/gt3_transmission_state_oracle.cpp','tests/gt3_transmission_state_host.inc',
 'tests/gt3_transmission_state_source_test.cpp','tests/gt3_transmission_state_test.py',
 'docs/site/docs/transmission-state-v1.md','transmission-state.just']
MODES=['original','build-off','trace-only','admission','frozen','pair','repeat']
SPECS={'cycle':(4501,5101),'moving':(5350,5701),'braked':(5350,5701),
       'brake-abort':(5350,5701),'reverse':(4501,5101),'positive':(5111,5312),
       'at-control':(4801,5101)}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text())
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def check_record(d):
 assert d['id']=='transmission-state-decisions-v1' and d['status']=='validated-bounded'
 assert d['source_base']=='511f8575325e8d585ead26e92f56d109780d5635'
 assert d['runtime']=={'canonical_installation':False,'build_default':False,'runtime_default':False,'replacement':'admission-only'}
 assert d['recovered']['admission']['boundary']==['001e6d48','001e6ec7']
 assert d['recovered']['admission']['whole_function'] is True
 assert d['recovered']['synchronization']['abi_replacement'] is False
 assert d['recovered']['selection']['abi_replacement'] is False
 assert d['proof']['admission_cases']==156464 and d['proof']['whole_ram_cases']==306
 assert d['proof']['semantic_cases']==628352 and d['proof']['mutation_free_rejections']==12
 assert d['proof']['native_runs']==49 and d['proof']['native_updates']==19278
 assert d['proof']['admission_substitutions']==8262 and d['proof']['selector_substitutions']==7362 and d['proof']['helper_substitutions']==6
 assert d['proof']['admission_shadows']==8262 and d['proof']['fallback']==0
 assert d['private']['members']>0 and re.fullmatch('[0-9a-f]{64}',d['private']['sha256']) and d['private']['sha256']!='0'*64
 assert len(d['remaining_gates'])>=5 and set(d['sources'])==set(SOURCES)
 assert not set(d['sources'])&set(d['protected'])
 for path,h in {**d['sources'],**d['protected']}.items():assert sha(ROOT/path)==h,path
 old=module('state_protected_speed',ROOT/'scripts/project/transmission_speed.py');old.check_record(load(old.DB))

def verify_members(root,manifest):
 assert manifest['schema_version']==1 and manifest['files']
 paths=[x['path'] for x in manifest['files']];assert paths==sorted(set(paths))
 for item in manifest['files']:
  p=Path(item['path']);assert not p.is_absolute() and '..' not in p.parts
  assert str(p).startswith(HOME+'/')
  target=root/p;assert target.resolve().is_relative_to((root/HOME).resolve())
  assert sha(target)==item['sha256'],str(p)

def native(root):
 h=root/HOME/'native-attempt-1';summaries={};totals=Counter();changes=[]
 for tag,(first,end) in SPECS.items():
  ref=h/(tag+'-original');canonical=None;stage_counts=Counter();group_changes=[]
  reference_command=load(ref/'command.json');refargs=reference_command['argv'];ref_input=[refargs[i+1] for i,x in enumerate(refargs) if x=='--press']
  for mode in MODES:
   d=h/(tag+'-'+mode);cmd=load(d/'command.json');args=cmd['argv'];assert load(d/'result.json')['exit']==0
   assert 'frame limit reached' in (d/'run.log').read_text();assert sha(Path(args[0]))==cmd['binary_sha256']
   assert cmd['scenario']==tag and cmd['mode']==mode and cmd['state']==reference_command['state']
   assert sha(Path(cmd['state']['path']))==cmd['state']['sha256']
   assert args[args.index('--frames')+1]==str(end) and args[args.index('--save-state')+1]==str(end-1)+':'+str(d/'final.state')
   assert [args[i+1] for i,x in enumerate(args) if x=='--press']==ref_input
   assert not any(x in args for x in ['--axis','--ram-word','--gt3-triple','--virtual-pedals','--virtual-handbrake'])
   clean=mode in ['admission','pair','repeat'];frozen=mode in ['frozen','pair','repeat']
   for flag,want in [('--gt3-clean-admission',clean),('--gt3-state-shadow',clean),('--gt3-clean-transmission',frozen),('--gt3-clean-speed',frozen),('--gt3-speed-shadow',frozen)]:assert (flag in args)==want
   assert (d/'final.state').read_bytes()[:12]==b'PS2STATE\x03\0\0\0' and (d/'memory.bin').stat().st_size==36*1024*1024
   for name in ['memory.bin','final.state']:assert sha(d/name)==sha(ref/name),(tag,mode,name)
   captures=lambda q:{p.name:sha(p) for p in (q/'shots').glob('*.ppm')}
   assert captures(ref) and captures(d)==captures(ref),(tag,mode,'captures')
   assert not (d/'card.ps2').exists()
   if mode=='original':continue
   text=(d/'run.log').read_text();state_line=next(x for x in text.splitlines() if x.startswith('STATE '));pair_line=next(x for x in text.splitlines() if x.startswith('PAIR '))
   a={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',state_line)};b={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',pair_line)}
   n=end-first
   assert a['admission_entries']==a['admission_exits']==a['engine_checks']==a['selection_checks']==n
   assert a['replaced']==a['shadows']==(n if clean else 0) and a['fallback']==0
   mt_entries=0 if tag=='at-control' else n
   assert b['mt_entries']==b['mt_exits']==mt_entries
   assert b['selector']==b['mt_shadows']==(mt_entries if frozen else 0) and b['selector_fallback']==b['helper_fallback']==0
   helpers=1 if tag in ['reverse','positive'] else 0
   assert b['helper_entries']==b['helper_exits']==helpers
   assert b['helper']==b['helper_shadows']==(helpers if frozen else 0)
   totals['admission']+=a['replaced'];totals['admission_shadows']+=a['shadows'];totals['selector']+=b['selector'];totals['helper']+=b['helper'];totals['selector_shadows']+=b['mt_shadows'];totals['helper_shadows']+=b['helper_shadows']
   rows=[load_line(x) for x in (d/'trace.jsonl').read_text().splitlines()]
   semantic=[{k:v for k,v in row.items() if k!='transport_pc'} for row in rows]
   if canonical is None:canonical=semantic
   assert canonical==semantic,(tag,mode,'completeCPU/cost traces')
   assert {r['frame'] for r in rows}==set(range(first,end))
   if mode=='trace-only':
    frames=defaultdict(dict)
    for row in rows:
     assert row['object']==0x1fbb7bc and row['owner']==0 and row['policy']==(0 if tag=='at-control' else 1)
     marker=row['marker'];assert marker not in frames[row['frame']];frames[row['frame']][marker]=row
    for frame,events in sorted(frames.items()):
     for left,right,stage in [(0x1e6d48,0x6d480000,'admission'),(0x1e7500,0x1e77b4,'engine'),(0x1e77f8,0x1e783c,'selection')]:
      a,b=events[left],events[right];key=f'{stage}:{a["state"]}->{b["state"]}';stage_counts[key]+=1
      if a['state']!=b['state']:group_changes.append({'frame':frame,'stage':stage,'from':a['state'],'to':b['state']})
  summaries[tag]={'updates_per_run':end-first,'transitions':dict(sorted(stage_counts.items())),'changes':group_changes}
  changes+=group_changes
 assert totals==Counter(admission=8262,admission_shadows=8262,selector=7362,selector_shadows=7362,helper=6,helper_shadows=6)
 assert any(x['stage']=='engine' and x['from']==3 and x['to']==0 for x in changes)
 assert any(x['stage']=='engine' and x['from']==2 and x['to']==0 for x in changes)
 return {'runs':49,'updates':19278,'totals':dict(sorted(totals.items())),'scenarios':summaries}
def load_line(line):return json.loads(line)

def private(root):
 assert root==ROOT,'explicit current repository root required';d=load(DB);check_record(d)
 p=root/d['private']['manifest'];assert sha(p)==d['private']['sha256'];manifest=load(p);assert len(manifest['files'])==d['private']['members'];verify_members(root,manifest)
 old_builder=module('state_old_builder',ROOT/'scripts/validate_gt3_transmission_speed.py');old_builder.preflight(root/'local/baseline-v3/final-build')
 h=root/HOME
 tracked=load(h/'tracked-head-identity.json');assert tracked['head']==d['source_base']
 for path,expected in tracked['files'].items():assert sha(root/path)==expected,path
 records=load(h/'inherited-records.json')+load(h/'static-new.json')['records']+load(h/'static-readers-attempt-1/evidence.json')['records']
 for e in records:assert e['subject']['digest']['sha256']==d['original_elf_sha256']
 assert set(d['evidence'].values())<={e['evidence_id'] for e in records}
 for name in ['isolated-attempt-3','on-attempt-1','off-attempt-1']:
  record=load(h/name/'identity.json')
  for path,expected in record['files'].items():assert sha(h/name/path)==expected,path
  for path,expected in record['sources'].items():assert sha(h/name/'evaluated-sources'/path)==expected,path
 reproduction=load(h/'reproducible-builds.json')
 for row in reproduction:
  assert sha(h/row['executed'])==sha(h/row['reproduced'])==row['sha256']
 for name in ['isolated-reproduce-1','on-reproduce-1','off-reproduce-1']:
  record=load(h/name/'identity.json')
  for path,expected in record['sources'].items():assert sha(root/path)==expected,path
  for path,expected in record['files'].items():assert sha(h/name/path)==expected,path
 assert native(root)==load(h/'native-summary.json')
 for name in ['gt3-clean-admission','gt3-clean-transmission','gt3-clean-speed']:
  r=load(h/'cli-rejections'/(name+'.json'));assert r['exit']==2 and r['gameplay_started'] is False
 exe=h/'isolated-reproduce-1/oracle';result=subprocess.run([str(exe),str(old_builder.ELF)],capture_output=True,check=True)
 assert result.stdout+result.stderr==(h/'isolated-reproduce-1/oracle.log').read_bytes()
 # Inherited immutable proof stays unchanged; API checked by public regression.
 old=module('state_inherited_speed',ROOT/'scripts/project/transmission_speed.py');old.private(root)
 print('State bounded private PASS: independent admission156464 completeCPU/cost,306 whole32MiB;628352 semantic projections;12 mutation-free fallbacks;49 native runs/19278 updates;8262 admission and7362 selector and6 helper substitutions+shadows,zero fallback. Engine/commit models are NOT ABI replacements; no canonical/all-policy/hardware claim.')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','verify']);p.add_argument('root',nargs='?',type=Path);a=p.parse_args()
 if a.command=='check':check_record(load(DB));print('State public authority PASS; existing Frozen/canonical sources unchanged')
 else:
  if a.root is None:p.error('verify requires explicit repository root')
  private(a.root.resolve(strict=True))
if __name__=='__main__':main()
