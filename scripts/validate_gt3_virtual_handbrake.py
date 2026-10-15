#!/usr/bin/env python3
"""Opt-in virtual handbrake native-v3 pairs, multiple independently pinned contexts."""
import argparse,json,os,re,struct,subprocess
from pathlib import Path
from gt3_virtual_handbrake_proof import digest,read_rows,semantic,review_rows
ROOT=Path(__file__).resolve().parents[1]
CONTEXTS=['trusted','altezza-mt','alfa-at','mrs-at','time-trial','free-run','license','pad-left-stick-at','pad-left-stick-mt','pad-dpad-at','compat-wheel-at','compat-wheel-mt']
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 for name in ['build','out']:parser.add_argument('--'+name,type=Path,required=True)
 parser.add_argument('--original-table',type=Path,nargs='+',required=True)
 args=parser.parse_args();build=args.build.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
 identity=json.loads((build/'identity.json').read_text());assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
 for p,h in identity['files'].items():assert digest(build/p)==h,p
 for p,h in identity['sources'].items():assert digest(ROOT/p)==h,p
 frozen=Path(identity['parent_build']);assert digest(frozen/'identity.json')==identity['parent_identity_sha256']
 parent=Path(json.loads((frozen/'identity.json').read_text())['parent_build']);clock=parent/'base/fixed-clock.so';canonical=parent/'base/original/ps2run'
 original_tables=[p.resolve() for p in args.original_table]
 table={(r['floor'],r['q']):r for p in original_tables for r in read_rows(p)}
 assert set(table)=={(floor,q) for floor in [0x3dcccccc,0x3dcccccd] for q in range(4097)}
 env={k:v for k,v in os.environ.items() if not k.startswith(('PS2_','GT3_'))}
 env.update(PS2_ONE_THREAD='1',SDL_AUDIODRIVER='dummy',LD_PRELOAD=str(clock),GT3_BASELINE_UTC_EPOCH='1791964800')
 plan=json.loads((ROOT/'local/pedal-profiles-v1/plan.json').read_text());labels={r['id']:r['labels'] for r in plan['cases']}
 summary=dict(validator_sha256=digest(Path(__file__)),identity_sha256=digest(build/'identity.json'),clock_sha256=digest(clock),canonical_sha256=digest(canonical),original_tables={str(p):digest(p) for p in original_tables},cases={},defaults={})
 def source(context):
  d=ROOT/f'local/pedal-profiles-v1/{context}-original';meta=json.loads((d/'command.json').read_text())
  # Use actual original observation frames, not guessed snapshot file names.
  frames=[]
  with (d/'cpu.jsonl').open() as f:
   for line in f:
    r=json.loads(line)
    if r['pc']==0x1e48fc:frames.append(r['frame'])
  assert frames and len(frames)==len(set(frames));return meta,min(frames),len(frames)
 def run(tag,context='trusted',binary='virtual-on',extra=(),trace=True,stop=None):
  d=out/tag;d.mkdir();(d/'shots').mkdir();meta,first,n=source(context)
  state=meta['state'];assert digest(state['path'])==state['sha256']
  with open(state['path'],'rb') as f:assert f.read(12)==b'PS2STATE'+struct.pack('<I',3)
  argv=meta['argv'][1:]
  for flag,file in [('--memcard','card.ps2'),('--frames-dir','shots'),('--gt3-wheel-trace','steering.jsonl')]:argv[argv.index(flag)+1]=str(d/file)
  for flag in ['--gt3-pedal-trace']+([] if trace else ['--gt3-wheel-trace']):
   i=argv.index(flag);del argv[i:i+2]
  if stop is not None:argv[argv.index('--frames')+1]=str(stop)
  exe=canonical if binary=='canonical' else build/binary
  cmd=[str(exe),*argv,*extra]
  if trace:cmd+=['--gt3-virtual-handbrake-trace',str(d/'virtual.jsonl'),'--gt3-handbrake-trace',str(d/'cpu.jsonl')]
  record=dict(argv=cmd,binary_sha256=digest(exe),state=state,context=context,labels=labels[context],source_command_sha256=digest(ROOT/f'local/pedal-profiles-v1/{context}-original/command.json'),env={k:env[k] for k in ['PS2_ONE_THREAD','LD_PRELOAD','GT3_BASELINE_UTC_EPOCH']})
  (d/'command.json').write_text(json.dumps(record,indent=2)+'\n')
  with (d/'run.log').open('w') as f:subprocess.run(cmd,cwd=ROOT,env=dict(env,PS2_DUMP=str(d/'memory.bin')),stdout=f,stderr=f,check=True,timeout=600)
  assert 'frame limit reached' in (d/'run.log').read_text()
  return d
 def counts(d,label):
  match=re.search(r'\['+label+r'\] ([^\n]+)',(d/'run.log').read_text());assert match
  return {k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',match[1])}
 def equal(a,b,trace=True):
  assert digest(a/'memory.bin')==digest(b/'memory.bin'),('full RAM/IOP/SPU',a,b)
  shots=lambda p:{f.name:digest(f) for f in (p/'shots').glob('*.ppm')}
  assert shots(a) and shots(a)==shots(b),('captures',a,b)
  if trace:
   assert (a/'virtual.jsonl').read_bytes()==(b/'virtual.jsonl').read_bytes(),('command/processed/consumers',a,b)
   assert semantic(read_rows(a/'cpu.jsonl'))==semantic(read_rows(b/'cpu.jsonl')),('defined CPU/budget',a,b)
   assert (a/'steering.jsonl').read_bytes()==(b/'steering.jsonl').read_bytes(),('steering',a,b)
 try:
  baseline=run('canonical',binary='canonical',trace=False)
  default=run('default',trace=False);trace=run('trace-only');off=run('build-off-trace',binary='virtual-off')
  equal(default,baseline,False);equal(trace,baseline,False);equal(trace,off)
  for d in [default,trace,off]:assert counts(d,'gt3-virtual-handbrake')['injected']==counts(d,'gt3-handbrake')['replaced']==0
  summary['defaults']['canonical_disabled_trace_build_off_exact']=True
  invalid=[['--gt3-virtual-handbrake',s] for s in ['-0.01','1.0000000000000002','nan','inf','-inf','1e-1','.5','0.',' 0.5','0.5x','-0','9999999999999999999999999999999999999999999999']]
  invalid += [['--gt3-virtual-handbrake-at','1:0'],['--gt3-virtual-handbrake','0','--gt3-virtual-handbrake-at','5:0','--gt3-virtual-handbrake-at','5:1'],['--gt3-virtual-handbrake','0','--gt3-virtual-handbrake-at','5:0','--gt3-virtual-handbrake-at','4:1'],['--gt3-virtual-handbrake','0','--gt3-virtual-handbrake-at','18446744073709551616:0'],['--gt3-virtual-handbrake','0','--gt3-virtual-handbrake','1']]
  for i,extra in enumerate(invalid):
   r=subprocess.run([str(build/'virtual-on'),*extra],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);assert r.returncode==2
   (out/f'invalid-{i}.log').write_text(r.stdout)
  r=subprocess.run([str(build/'virtual-off'),'--gt3-virtual-handbrake','0.5'],env=env,capture_output=True,text=True)
  assert r.returncode==2 and 'build gate is OFF' in r.stderr;(out/'build-off-rejection.log').write_text(r.stdout+r.stderr)
  before=digest(trace/'virtual.jsonl');r=subprocess.run([str(build/'virtual-on'),'--gt3-virtual-handbrake-trace',str(trace/'virtual.jsonl')],env=env,capture_output=True,text=True)
  assert r.returncode==2 and digest(trace/'virtual.jsonl')==before;(out/'exclusive-trace-rejection.log').write_text(r.stdout+r.stderr)
  cases=[]
  for context in CONTEXTS:
   _,first,n=source(context)
   extra=['--gt3-virtual-handbrake','0']
   for offset,value in [(25,'0.000244140625'),(50,'0.0625'),(80,'0.25'),(110,'0.5'),(140,'0.75'),(170,'1'),(220,'0.5'),(250,'0')]:extra+=['--gt3-virtual-handbrake-at',f'{first+offset}:{value}']
   if context=='altezza-mt':extra+=['--press',f'{first+200}:r2:25','--press',f'{first+250}:l2:25']
   if context.startswith('compat-wheel'):extra+=['--gt3-clean-steering']
   cases.append((context,context,extra,None,n))
  for name,value in [('zero','0'),('half','0.5'),('full','1')]:
   _,first,n=source('trusted');extra=['--gt3-virtual-handbrake',value]
   if name=='half':extra+=['--press',f'{first+200}:circle:50'] # Virtual action takes explicit priority, not native OR/max.
   cases.append((name,'trusted',extra,None,n))
  _,first,_=source('trusted');extra=['--gt3-virtual-handbrake','0']
  for q in range(1,4097):extra+=['--gt3-virtual-handbrake-at',f'{first+q}:{q/4096:.12f}']
  cases.append(('all-q12-native','trusted',extra,first+4097,4097))
  for name,context,extra,stop,n in cases:
   generated=run(name+'-generated',context,extra=extra,stop=stop)
   clean=run(name+'-clean',context,extra=[*extra,'--gt3-clean-handbrake'],stop=stop)
   repeat=run(name+'-repeat',context,extra=extra,stop=stop)
   equal(generated,clean);equal(generated,repeat)
   c=counts(clean,'gt3-handbrake');assert c['replaced']==n and c['fallback']==0
   expected_counts=dict(injected=n,restored=n,entries=n,joins=n,brakes=n,brake_joins=n,engines=n,shifts=n)
   for d in [generated,clean,repeat]:assert counts(d,'gt3-virtual-handbrake')==expected_counts
   assert counts(generated,'gt3-handbrake')['replaced']==counts(repeat,'gt3-handbrake')['replaced']==0
   rows=read_rows(generated/'virtual.jsonl');codes=review_rows(rows,n,table)
   cpu=read_rows(generated/'cpu.jsonl');stages=[0x1e4bb8,0x1e4c60,0x1e4c74,0x1e3a90,0x1e3aac,0x1e3ab8,0x1e6ec8,0x1e6fc8,0x1e7500]
   for pc in stages:assert sum(r['pc']==pc for r in cpu)==n
   byframe={r['frame']:r for r in rows if r['stage']=='entry'}
   for row in cpu:
    assert int(row['cpu'][1096:1104],16)==row['pc']
    if row['pc']==0x1e4bb8:
     command=byframe[row['frame']]['bytes'];assert row['input']==command[14]+256*command[15] and row['flags']==command[0]
    if row['pc']==0x1e3aac:assert int(row['cpu'][6*32:6*32+8],16)==(1 if row['processed']==0 else 0)
   if name=='all-q12-native':assert codes==set(range(4097))
   command=json.loads((generated/'command.json').read_text())
   summary['cases'][name]=dict(context=context,labels=labels[context],state=command['state'],argv_extra=extra,stop=stop,entries=n,counts=expected_counts,handbrake_counts=c,command_codes=sorted(codes),exact_cpu_ram_captures_steering_and_repeat=True,original_result_table_exact=True)
   print(name,'PASS',n,'updates /',len(codes),'Q12 codes',flush=True)
 except Exception as error:
  (out/'STOP.json').write_text(json.dumps(dict(error=repr(error),partial=summary),indent=2)+'\n');raise
 summary['total_clean_substitutions']=sum(r['entries'] for r in summary['cases'].values());summary['live_runs']=4+3*len(summary['cases'])
 assert len({r['state']['sha256'] for r in summary['cases'].values()})>=7
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('Virtual handbrake bounded multi-context native-v3 validation PASS',summary['live_runs'],summary['total_clean_substitutions'],flush=True)
if __name__=='__main__':main()
