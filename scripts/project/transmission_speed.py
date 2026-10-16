#!/usr/bin/env python3
"""Separate bounded helper authority. Never rewrites the Frozen selector record."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import struct
import subprocess

ROOT=Path(__file__).resolve().parents[2]
DB=ROOT/'decomp/gt3/transmission-speed.json'
HOME='local/transmission-speed-v1'
SOURCES=['host/gt3_clean_transmission_speed.cpp','host/gt3_clean_transmission_speed.hpp',
 'scripts/validate_gt3_transmission_speed.py','scripts/project/transmission_speed.py',
 'tests/gt3_transmission_speed_oracle.cpp','tests/gt3_transmission_speed_source_test.cpp',
 'tests/gt3_transmission_speed_composition.cpp','tests/gt3_transmission_speed_context.cpp',
 'tests/gt3_transmission_speed_frozen_driver.cpp','tests/gt3_transmission_speed_host.inc',
 'tests/gt3_transmission_speed_test.py','docs/site/docs/transmission-speed-v1.md','transmission-speed.just']
PROTECTED=['HANDOFF.md','README.md','CMakeLists.txt','justfile','decomp/gt3/schema.md','decomp/gt3/transmission.json',
 'docs/site/docs/transmission.md','docs/site/docs/transmission-recovery-v1.md','docs/site/sidebars.js',
 'host/gt3_clean_transmission.cpp','host/gt3_clean_transmission.hpp','scripts/build_gt3_transmission.sh',
 'scripts/build_gt3_transmission_live.sh','scripts/project/transmission.py','scripts/validate_gt3_transmission.py',
 'tests/gt3_transmission_host.inc','tests/gt3_transmission_oracle.cpp','tests/gt3_transmission_source_test.cpp',
 'tests/gt3_transmission_test.py','tests/gt3_transmission_wrapper.cpp','transmission.just']
COVERAGE=dict(independent_cases=710850,independent_whole_ram=2219,fallback_cases=264,controlled_scheduler_cases=4,
 frozen_cases_each=663959,frozen_helper_routes=6571,consumer_cases_each=1008,consumer_helper_routes=36,
 four_way_cases=1008,four_way_paths=4032,matrix_native_runs=28,original_fixture_runs=3,native_updates=13740,
 native_selector_substitutions=4203,native_selector_shadows=4203,native_helper_substitutions=6,native_helper_shadows=6)
GATES=['identify','trace','independent-original','four-way-composition','unchanged-frozen-tests',
 'default-off-build-runtime','real-entry-native','seven-way-parity','original-positive-fixture',
 'reproducible-builds','unchanged-selector-authority','public-checks','strict-private','missing-changed-faults']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def check_record(d):
 assert d['id']=='clean-speed-search-v1' and d['lifecycle']=='frozen'
 assert d['boundary']=={'entry':'0x001e4e80','last_byte':'0x001e4f0f','bytes':144,'fnv1a64':'0xd24c603536aba561'}
 assert d['source_base_commit']=='e9d8cb83caa383502d8935fc309aaeb27ecad63f'
 assert d['baseline_source_commit']=='82987dec7a71d76414adfff8663da5494a280938'
 assert d['validation_only'] is True and d['canonical_installation'] is False
 assert d['build_default'] is False and d['runtime_default'] is False
 assert d['low_budget_policy']=='mutation-free-original-fallback; original resume labels untouched'
 assert d['selector_authority']=='decomp/gt3/transmission.json' and d['selector_modified'] is False
 assert d['coverage']==COVERAGE and set(d['gates'])==set(GATES) and all(v=='passing' for v in d['gates'].values())
 assert d['limitations']==['not-all-policies-owners-cars','not-hardware-proof','not-new-scheduler-or-resume-recovery',
   'native-loop-covers-first-positive-candidate-only','no-clutch-neutral-engagement-calibration-recovery','not-canonical-runtime']
 assert set(d['sources'])==set(SOURCES) and set(d['protected'])==set(PROTECTED)
 for key in ['sources','protected']:
  for p,h in d[key].items():assert sha(ROOT/p)==h,p
 assert d['private']['manifest']==HOME+'/manifest-final.json' and d['private']['members']>0
 assert re.fullmatch('[0-9a-f]{64}',d['private']['sha256'])

def verify_members(root,manifest):
 rows=manifest['files'];assert [x['path'] for x in rows]==sorted({x['path'] for x in rows})
 for row in rows:
  p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts and str(p).startswith(HOME+'/')
  data=(root/p).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],str(p)

def semantic(rows):return [{k:v for k,v in r.items() if k!='transport_pc'} for r in rows]
def rows(d):return [json.loads(s) for s in (d/'trace.jsonl').read_text().splitlines()]
def cpuword(r,offset,signed=False):return int.from_bytes(bytes.fromhex(r['cpu'])[offset:offset+4],'little',signed=signed)
def captures(d):return {p.name:sha(p) for p in (d/'shots').glob('*.ppm')}
def parity(dirs):
 ref=dirs[0];assert captures(ref)
 observed=[]
 for d in dirs:
  assert load(d/'result.json')['exit']==0 and not (d/'card.ps2').exists()
  assert 'frame limit reached' in (d/'run.log').read_text()
  assert (d/'memory.bin').stat().st_size==36*1024*1024
  assert all(sha(ref/p)==sha(d/p) for p in ['memory.bin','final.state'])
  assert captures(d)==captures(ref)
  c=load(d/'command.json');assert sha(Path(c['argv'][0]))==c['binary_sha256']
  assert sha(Path(c['state']['path']))==c['state']['sha256']
  assert '--axes' not in c['argv'] and '--ram-word' not in c['argv']
  if (d/'trace.jsonl').exists():
   rs=rows(d)
   for r in rs:
    assert len(bytes.fromhex(r['cpu']))==1440
    if r['marker'] in [0x1e5458,0x1e4e80]:assert cpuword(r,548)==r['marker']
    else:assert cpuword(r,548)==r['transport_pc']
   observed.append(semantic(rs))
 assert all(r==observed[0] for r in observed)

def native(root):
 h=root/HOME;modes=['original','build-off','trace-only','helper-only','selector-only','pair','repeat'];summary={};totals=dict(selector=0,helper=0,mt_shadows=0,helper_shadows=0)
 for scenario,n,folder,prefix in [('cycle',600,'live-attempt-1','cycle'),('reverse',600,'live-attempt-1','reverse'),('at-control',300,'live-attempt-1','at-control'),('positive',201,'positive-attempt-1','positive')]:
  ds=[h/folder/f'{prefix}-{m}' for m in modes];parity(ds);stats={}
  for mode,d in zip(modes[1:],ds[1:]):
   text=(d/'run.log').read_text();line=re.findall(r'^PAIR (.*)$',text,re.M);assert len(line)==1
   v={k:int(a) for k,a in re.findall(r'(\w+)=(\d+)',line[0])};mt=0 if scenario=='at-control' else n;helper=int(scenario in ['reverse','positive'])
   assert v['mt_entries']==v['mt_exits']==mt and v['helper_entries']==v['helper_exits']==helper
   se=mode in ['selector-only','pair','repeat'];he=mode in ['helper-only','pair','repeat']
   assert v['selector']==v['mt_shadows']==mt*se and v['helper']==v['helper_shadows']==helper*he
   assert v['speed_dispatches']==helper*se and v['selector_fallback']==v['helper_fallback']==0
   for k in totals:totals[k]+=v[k]
   flags=load(d/'command.json')['argv'];assert ('--gt3-clean-transmission' in flags)==se and ('--gt3-clean-speed' in flags)==he
   stats[mode]=v
  raw=rows(ds[1]);entries=[r for r in raw if r['marker']==0x1e4e80];exits=[r for r in raw if r['marker']==0xe4e80000]
  helper_detail=[]
  for e,x in zip(entries,exits):
   assert e['object']==x['object']==0x1fbb7bc and e['owner']==0 and e['policy']==1 and e['maximum']==6
   assert e['sp']==x['sp']==0x49af20 and e['ra']==x['ra']==0x1e54a8 and e['depth']==5
   cost=cpuword(e,552,True)-cpuword(x,552,True);speed=cpuword(e,608)
   assert cost==(7 if scenario=='reverse' else 28)
   assert bool(speed&0x80000000)==(scenario=='reverse')
   assert cpuword(x,32)==(0 if scenario=='reverse' else 1)
   helper_detail.append(dict(frame=e['frame'],speed_sign='negative' if speed&0x80000000 else 'positive',cost=cost,result=cpuword(x,32),state=e['state']))
  summary[scenario]=dict(updates_each=n,modes=stats,helper_calls=helper_detail)
 parity([h/'positive-attempt-1'/('prepare-'+m) for m in ['original','observer','repeat']])
 assert totals==dict(selector=4203,helper=6,mt_shadows=4203,helper_shadows=6)
 for name in ['gt3-clean-speed','gt3-clean-transmission']:
  j=load(h/'cli-rejections'/(name+'.json'));assert j['exit']==2 and j['phase']=='argument parse; no gameplay'
 return dict(matrix_runs=28,fixture_runs=3,updates=13740,totals=totals,scenarios=summary)

def import_file(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def verify_selector(root):
 old=import_file('unchanged_selector',root/'scripts/project/transmission.py');old.verify(root)

def private(root):
 assert root==ROOT,'explicit current repository root required';d=load(DB);check_record(d)
 p=root/d['private']['manifest'];assert sha(p)==d['private']['sha256'];manifest=load(p);assert len(manifest['files'])==d['private']['members'];verify_members(root,manifest)
 h=root/HOME
 b=import_file('speed_builder',ROOT/'scripts/validate_gt3_transmission_speed.py');b.preflight(root/'local/baseline-v3/final-build')
 for key in ['isolated-attempt-1','on-attempt-1','off-attempt-1','isolated-reproduce-1','on-reproduce-1','off-reproduce-1']:
  v=load(h/key/'identity.json')
  for p,expected in v['sources'].items():assert sha(root/p)==expected,p
  for p,expected in v['files'].items():assert sha(h/key/p)==expected,p
 for p,v in load(h/'reproducible-builds.json').items():assert sha(h/p)==sha(h/v['repeat'])==v['sha256']
 assert native(root)==load(h/'native-summary.json')
 # Re-execute original-dependent CPU/RAM proofs, NOT a retained-log-only claim
 # and NOT another launch of the native gameplay matrices.
 elf=root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf'
 commands=[(h/'isolated-attempt-1/oracle',h/'isolated-attempt-1/oracle.log',None),
           (h/'on-attempt-1/composition',h/'on-attempt-1/composition.log',None)]
 for label in ['selector','consumer']:
  for pair in [0,1]:commands.append((h/'on-attempt-1'/label,h/'on-attempt-1'/f'{label}-pair{pair}.log',dict(os.environ,GT3_SPEED_PAIR_TEST=str(pair))))
 for exe,expected,env in commands:
  actual=subprocess.run([str(exe),str(elf)],capture_output=True,check=True,env=env)
  assert actual.stdout+actual.stderr==expected.read_bytes(),str(exe)
 verify_selector(root)
 print(f'Speed search bounded private PASS: {len(manifest["files"])} pinned members; independent710850; four-way4032; unchanged Frozen663959 OFF/ON + consumer1008 OFF/ON; 28 matrix +3 original fixture runs; helper6/selector4203 substitutions and real-entry fullCPU+32MiB shadows, fallback0. Not canonical/all-car/physical proof.')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','verify']);p.add_argument('root',nargs='?',type=Path);a=p.parse_args()
 if a.command=='check':check_record(load(DB));print('Speed search additive public authority PASS; old selector files unchanged')
 else:
  if a.root is None:p.error('verify requires explicit repository root')
  private(a.root.resolve(strict=True))
if __name__=='__main__':main()
