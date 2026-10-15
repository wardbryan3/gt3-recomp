#!/usr/bin/env python3
"""Finite explicit retained-survey replay; never edits input states or commands.
Shadow mode exercises the exact old body at actual rejected entries. Live mode
requires real guarded substitutions and compares original/default/trace paths.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from characterize_gt3_pedal_profiles import digest,read_rows,semantic
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['shadow','live'])
 for name in ['build','out','plan']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();build=a.build.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 plan=json.loads(a.plan.read_text());cases=plan['cases']+plan.get('explorations',[])
 assert len({c['id'] for c in cases})==len(cases)
 clock=ROOT/'local/pedal-v1-resume/candidate-build-3/base/fixed-clock.so'
 env={k:v for k,v in os.environ.items() if not k.startswith(('PS2_','GT3_PEDAL_'))}
 env.update(PS2_ONE_THREAD='1',SDL_AUDIODRIVER='dummy',LD_PRELOAD=str(clock),GT3_BASELINE_UTC_EPOCH='1791964800')
 summary={'mode':a.mode,'validator_sha256':digest(Path(__file__)),'plan_sha256':digest(a.plan),'cases':{}}
 def run(case,tag,binary,clean=False,trace=True):
  directory=out/(case['id']+'-'+tag);directory.mkdir();(directory/'shots').mkdir()
  meta=json.loads((Path(case['directory'])/'command.json').read_text());state=meta['state']
  assert digest(Path(state['path']))==state['sha256']
  args=meta['argv'][1:]
  for flag,name in [('--memcard','card.ps2'),('--frames-dir','shots'),('--gt3-pedal-trace','cpu.jsonl'),('--gt3-wheel-trace','steering.jsonl')]:
   index=args.index(flag);args[index+1]=str(directory/name)
  if not trace:
   for flag in ['--gt3-pedal-trace','--gt3-wheel-trace']:
    index=args.index(flag);del args[index:index+2]
  command=[str(binary),*args]+(['--gt3-clean-pedals'] if clean else [])
  (directory/'command.json').write_text(json.dumps({'argv':command,'binary_sha256':digest(binary),'state':state},indent=2)+'\n')
  with (directory/'run.log').open('w') as log:
   subprocess.run(command,cwd=ROOT,env=dict(env,PS2_DUMP=str(directory/'memory.bin'),GT3_PEDAL_CLOSURE_TRACE=str(directory/'closure.jsonl')),
    stdout=log,stderr=log,check=True,timeout=300)
  log=(directory/'run.log').read_text();assert 'frame limit reached' in log
  counts=re.search(r'\[gt3-pedals\] replaced=(\d+) fallback=(\d+) response_calls=(\d+)',log)
  info={'memory':digest(directory/'memory.bin'),'captures':{p.name:digest(p) for p in (directory/'shots').glob('*.ppm')},
        'counts':list(map(int,counts.groups())) if counts else None}
  assert info['captures'];return directory,info
 def equal(x,y,trace=True):
  d,i=x;e,j=y;assert i['memory']==j['memory'] and i['captures']==j['captures']
  if trace:
   assert semantic(read_rows(d/'cpu.jsonl'))==semantic(read_rows(e/'cpu.jsonl'))
   assert (d/'steering.jsonl').read_bytes()==(e/'steering.jsonl').read_bytes()
 try:
  for case in cases:
   original=Path(case['directory']);old={'memory':digest(original/'memory.bin'),'captures':{p.name:digest(p) for p in (original/'shots').glob('*.ppm')}}
   if a.mode=='shadow':
    result=run(case,'shadow',build/'closure-shadow');equal(result,(original,old))
    rows=read_rows(result[0]/'closure.jsonl');entries=[r for r in rows if r['stage']=='entry'];joins=[r for r in rows if r['stage']=='join']
    assert len(entries)==len(joins)>0 and all(r['exact'] for r in joins)
    item={'entries':len(entries),'actual_entry_full_cpu_32mib_cost_mutation_differential':True,
          'threads':sorted({(r['thread'],r['stack_base'],r['stack_size']) for r in entries}),
          'parents':sorted({r['parent_ra'] for r in entries}),'depths':sorted({r['depth'] for r in entries}),
          'hooks':sorted({r['target'] for r in rows if r['stage']=='hook'}),'cost':[min(r['cost'] for r in joins),max(r['cost'] for r in joins)]}
   else:
    off=run(case,'build-off',build/'pedal-off');disabled=run(case,'disabled',build/'pedal-on',trace=False)
    trace=run(case,'trace',build/'pedal-on');clean=run(case,'clean',build/'pedal-on',clean=True)
    equal(off,(original,old));equal(off,disabled,False);equal(off,trace);equal(off,clean)
    n=sum(r['pc']==0x1e48fc for r in read_rows(off[0]/'cpu.jsonl'))
    assert clean[1]['counts'][0]==n>0 and clean[1]['counts'][1]==0
    assert off[1]['counts']==trace[1]['counts']==disabled[1]['counts']==[0,0,0]
    if case['reachability']=='native-pad':
     canonical=run(case,'canonical',build/'base/original/ps2run',trace=False);equal(off,canonical,False)
    item={'entries':n,'clean_counts':clean[1]['counts'],'exact_cpu_steering_ram_captures':True}
   summary['cases'][case['id']]=item;print(case['id'],'PASS',item,flush=True)
 except Exception as error:
  (out/'STOP.json').write_text(json.dumps({'error':str(error),'partial':summary},indent=2)+'\n');raise
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()
