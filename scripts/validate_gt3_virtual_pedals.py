#!/usr/bin/env python3
"""Finite virtual pedal v1 replay. Immutable v3 inputs; exclusive new output root."""
import argparse,json,os,re,subprocess
from pathlib import Path
from characterize_gt3_pedal_profiles import digest,read_rows,semantic
from gt3_virtual_pedal_proof import review_rows
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 build=a.build.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 identity=json.loads((build/'identity.json').read_text());assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
 for name,sha in identity['files'].items():assert digest(build/name)==sha
 parent=Path(identity['parent_build']);clock=parent/'base/fixed-clock.so'
 env={k:v for k,v in os.environ.items() if not k.startswith(('PS2_','GT3_'))};env.update(PS2_ONE_THREAD='1',SDL_AUDIODRIVER='dummy',LD_PRELOAD=str(clock),GT3_BASELINE_UTC_EPOCH='1791964800')
 summary={'validator_sha256':digest(Path(__file__)),'identity_sha256':digest(build/'identity.json'),'clock_sha256':digest(clock),'cases':{},'defaults':{}}
 def run(name,scenario='trusted',binary='virtual-on',extra=(),virtual_trace=True,cpu=True):
  d=out/name;d.mkdir();(d/'shots').mkdir();meta=json.loads((ROOT/f'local/pedal-profiles-v1/{scenario}-original/command.json').read_text());state=meta['state'];assert digest(Path(state['path']))==state['sha256']
  args=meta['argv'][1:]
  for flag,file in [('--memcard','card.ps2'),('--frames-dir','shots'),('--gt3-pedal-trace','cpu.jsonl'),('--gt3-wheel-trace','steering.jsonl')]:args[args.index(flag)+1]=str(d/file)
  if not cpu:
   for flag in ['--gt3-pedal-trace','--gt3-wheel-trace']:
    i=args.index(flag);del args[i:i+2]
  exe=parent/'base/original/ps2run' if binary=='canonical' else build/binary
  cmd=[str(exe),*args,*extra]+(['--gt3-virtual-pedals-trace',str(d/'virtual.jsonl')] if virtual_trace else [])
  (d/'command.json').write_text(json.dumps({'argv':cmd,'binary_sha256':digest(exe),'state':state,'env':{k:env[k] for k in ['PS2_ONE_THREAD','LD_PRELOAD','GT3_BASELINE_UTC_EPOCH']}},indent=2)+'\n')
  with (d/'run.log').open('w') as f:subprocess.run(cmd,cwd=ROOT,env=dict(env,PS2_DUMP=str(d/'memory.bin')),stdout=f,stderr=f,check=True,timeout=300)
  assert 'frame limit reached' in (d/'run.log').read_text()
  return d
 def equal(d,e,cpu=True,virtual=True):
  assert digest(d/'memory.bin')==digest(e/'memory.bin'),('memory',d,e)
  def shots(x):return {p.name:digest(p) for p in (x/'shots').glob('*.ppm')}
  assert shots(d) and shots(d)==shots(e),('captures',d,e)
  if cpu:
   assert semantic(read_rows(d/'cpu.jsonl'))==semantic(read_rows(e/'cpu.jsonl')),('CPU',d,e)
   assert (d/'steering.jsonl').read_bytes()==(e/'steering.jsonl').read_bytes(),('steering',d,e)
  if virtual:assert (d/'virtual.jsonl').read_bytes()==(e/'virtual.jsonl').read_bytes()
 def counts(d,label):
  m=re.search(r'\['+label+r'\] ([^\n]+)',(d/'run.log').read_text());assert m
  return {k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',m[1])}
 try:
  canonical=run('canonical',binary='canonical',virtual_trace=False,cpu=False)
  default=run('default',virtual_trace=False);trace=run('trace-only');off=run('build-off-trace',binary='virtual-off')
  equal(default,canonical,cpu=False,virtual=False);equal(default,trace,virtual=False);equal(trace,off)
  retained=ROOT/'local/pedal-profiles-v1/trusted-original';equal(default,retained,virtual=False)
  for d in [default,trace,off]:assert counts(d,'gt3-virtual-pedals')['injected']==counts(d,'gt3-pedals')['replaced']==0
  summary['defaults']={'canonical_disabled_trace_build_off_exact':True}
  existing=trace/'virtual.jsonl';before=digest(existing)
  result=subprocess.run([str(build/'virtual-on'),'--gt3-virtual-pedals-trace',str(existing)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  assert result.returncode==2 and digest(existing)==before
  (out/'exclusive-trace-negative.log').write_text(result.stdout)
  for number,args in enumerate([['--gt3-virtual-pedals','0:0'],['--gt3-virtual-pedals','nan:0'],['--gt3-virtual-pedals','1.1:0'],['--gt3-virtual-pedals-at','1:0:0'],['--gt3-virtual-pedals','0:0','--gt3-virtual-pedals-at','5:0:0','--gt3-virtual-pedals-at','5:1:0']]):
   cmd=[str(build/('virtual-off' if number==0 else 'virtual-on')),*args]
   result=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env);assert result.returncode==2
   (out/f'parser-negative-{number}.log').write_text(result.stdout)
  def spec(value,events=(),wheel=()):return ['--gt3-virtual-pedals',value,*[x for e in events for x in ['--gt3-virtual-pedals-at',e]],*wheel]
  cases=[('zero','trusted',spec('0:0')),('throttle-half','trusted',spec('0.5:0')),('throttle-full','trusted',spec('1:0')),
   ('brake-half','trusted',spec('0:0.5')),('brake-full','trusted',spec('0:1')),
   ('throttle-steps','trusted',spec('0:0',['4850:0.25:0','4900:0.5:0','4950:1:0','5050:0:0'])),
   ('brake-steps','trusted',spec('0:0',['4850:0:0.25','4900:0:0.5','4950:0:1','5050:0:0'])),
   ('throttle-to-brake','trusted',spec('1:0',['4900:0:0.5','5000:0:1','5050:0:0'])),
   ('simultaneous','trusted',spec('0.5:0.5')),('native-turn','pad-left-stick-at',spec('0.5:0')),
   ('wheel-compatible','trusted',spec('0.5:0.25',wheel=['--gt3-wheel','0.25'])),
   ('time-trial','time-trial',spec('1:0',['4900:0:0.5','5000:0:1','5050:0:0']))]
  for name,scenario,extra in cases:
   generated=run(name+'-generated',scenario,extra=extra);clean=run(name+'-clean',scenario,extra=[*extra,'--gt3-clean-pedals']);repeat=run(name+'-repeat',scenario,extra=extra)
   equal(generated,clean);equal(generated,repeat)
   c=counts(clean,'gt3-pedals');v=counts(generated,'gt3-virtual-pedals');n=v['injected'];assert n>0 and c['replaced']==n and c['fallback']==0
   assert v['restored']==v['entries']==v['joins']==v['brakes']==v['engines']==n
   rows=read_rows(generated/'virtual.jsonl');entries=[r for r in rows if r['stage']=='entry'];joins=[r for r in rows if r['stage']=='join']
   assert len(entries)==len(joins)==n
   review_rows(rows,n)
   for row in entries:
    assert row['throttle_q']==int(row['host_throttle']*4096+0.5) and row['brake_q']==int(row['host_brake']*4096+0.5) and row['flags']&6==6
   summary['cases'][name]={'scenario':scenario,'argv_extra':extra,'entries':n,'counts':v,'pedal_counts':c,
     'command_values':sorted({(r['throttle_q'],r['brake_q']) for r in entries}),
     'processed_values':sorted({(r['accelerator_bits'],r['brake_bits']) for r in joins}),
     'exact_cpu_ram_captures_steering_and_repeat':True}
   print(name,'PASS',n,summary['cases'][name]['command_values'],flush=True)
 except Exception as e:
  (out/'STOP.json').write_text(json.dumps({'error':repr(e),'partial':summary},indent=2)+'\n');raise
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()
