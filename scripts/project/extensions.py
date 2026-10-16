#!/usr/bin/env python3
"""Separate optional-extension acceptance; never promotes recovered-original status."""
import argparse,hashlib,importlib.util,json,os,re,struct,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DB=ROOT/'extensions/gt3/virtual_transmission/validation.json'
HOME='local/extensions/virtual-transmission-v1'
SOURCES=['extensions/gt3/virtual_transmission/controller.hpp','extensions/gt3/virtual_transmission/controller.cpp',
 'extensions/gt3/native_bindings/virtual_transmission.hpp','extensions/gt3/native_bindings/virtual_transmission.cpp',
 'extensions/gt3/native_bindings/profile.hpp','extensions/gt3/native_bindings/host.inc',
 'scripts/build_gt3_extensions.py','scripts/project/extensions.py','tests/gt3_extensions/controller_test.cpp',
 'tests/gt3_extensions/transmission_contract.cpp','tests/gt3_extensions/guard_rejection.cpp','tests/gt3_extensions/input_connection.cpp','tests/gt3_extensions_test.py',
 'extensions.just','docs/site/docs/virtual-transmission-v1.md',
 'docs/site/docs/optional-extensions-architecture-proposal.md','docs/site/docs/virtual-transmission-v1-boundary.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def check_record(d):
 assert d['kind']=='extension' and d['id']=='virtual-transmission-v1' and d['status']=='validated-bounded'
 assert d['source_base']=='bea85fcc9bf76f55b1c28b3997d3b438b72388cb'
 assert d['runtime']=={'canonical_installation':False,'build_default':False,'runtime_default':False,'startup_activation_only':True,'device_loss':'terminal-neutral-latch','clean_transmission_combination':'rejected'}
 assert d['proof']['contracts']==12288 and d['proof']['contract_whole_ram']==192
 assert d['proof']['off_runs']==42 and d['proof']['on_runs']==15 and d['proof']['off_updates']==16128 and d['proof']['on_updates']==6162
 assert d['proof']['active_guard_rejections']==15 and d['supported']['startup_fixtures']==5
 assert d['proof']['public_policy_checks']==46932 and d['proof']['startup_cli_rejections']==21
 assert d['proof']['real_entry_cpu_ram_shadows']==4108 and d['proof']['reproducible_objects_executables']==8 and d['proof']['typed_connection_mutation_free_cases']==2
 assert set(d['sources'])==set(SOURCES) and not set(d['sources'])&set(d['protected'])
 for p,h in {**d['sources'],**d['protected']}.items():assert sha(ROOT/p)==h,p
 assert d['private']['members']>0 and re.fullmatch('[0-9a-f]{64}',d['private']['sha256'])
 old=module('extension_parent_state',ROOT/'scripts/project/transmission_state.py');old.check_record(load(old.DB))
 assert 'extensions/' not in (ROOT/'CMakeLists.txt').read_text() and 'extensions/' not in (ROOT/'host/main.cpp').read_text()

def verify_members(root,manifest):
 items=manifest['files'];paths=[x['path'] for x in items];assert paths==sorted(set(paths)) and items
 for x in items:
  p=Path(x['path']);assert not p.is_absolute() and '..' not in p.parts and str(p).startswith(HOME+'/')
  q=root/p;assert q.resolve().is_relative_to((root/HOME).resolve());assert sha(q)==x['sha256'],str(p)

def key(x):
 if not x&0x7f800000:x&=0x80000000
 return -(x&0x7fffffff) if x&0x80000000 else x&0x7fffffff

def mul(a,b):
 sign=(a^b)&0x80000000;ea=(a>>23)&255;eb=(b>>23)&255
 if not ea or not eb:return sign
 m=((a&0x7fffff)|0x800000)*((b&0x7fffff)|0x800000);e=ea+eb-127
 if m>>47:m>>=24;e+=1
 else:m>>=23
 if e>255:return sign|0x7fffffff
 if e<=0:return sign
 return sign|(e<<23)|(m&0x7fffff)
def integer_bits(x):return struct.unpack('<I',struct.pack('<f',x))[0]
def cpu_word(row,offset):return int.from_bytes(bytes.fromhex(row['cpu'])[offset:offset+4],'little')
def artifacts(p):
 assert (p/'memory.bin').stat().st_size==36*1024*1024
 with (p/'final.state').open('rb') as f:assert f.read(12)==b'PS2STATE\x03\0\0\0'
 result={name:sha(p/name) for name in ['memory.bin','final.state']};result['shots']={x.name:sha(x) for x in (p/'shots').glob('*.ppm')};assert result['shots'];return result

def native(root):
 h=root/HOME;off=h/'off-native-attempt-5';on=h/'on-native-attempt-4';summary={'off_runs':0,'on_runs':0,'on_updates':0,'off_updates':0,'cases':{}}
 # Parent original memory supplies untouched calibration/EE constants, never new expected tables.
 memory=(root/'local/transmission-state-v1/native-attempt-1/cycle-original/memory.bin').read_bytes();car=0x1fbb7bc;gp=0x3579f0
 word=lambda at:int.from_bytes(memory[at:at+4],'little');half=lambda at:int.from_bytes(memory[at:at+2],'little')
 ratios=[word(car+0x244+4*i) for i in range(7)]
 idle=mul(integer_bits(half(car+0x1d6)),word(gp-30012));idle500=mul(integer_bits(half(car+0x1d6)+500),word(gp-30008));upper=mul(integer_bits(half(car+0x1d4)+10),word(gp-29996))
 for tag,n in {'cycle':600,'moving':351,'braked':351,'positive':201,'reverse':600,'state3':201}.items():
  reference=artifacts(off/(tag+'-original'));trace=None
  for mode in ['original','baseline','absent','absent-trace','extended-default','trace','trace-repeat']:
   p=off/(tag+'-'+mode);cmd=load(p/'command.json');assert load(p/'result.json')['exit']==0
   assert sha(Path(cmd['argv'][0]))==cmd['binary_sha256'];assert sha(Path(cmd['state']['path']))==cmd['state']['sha256']
   assert not any(x in cmd['argv'] for x in ['--virtual-transmission','--vt-at','--vt-initial','--ram-word','--gt3-triple']);assert artifacts(p)==reference
   if 'trace' in mode:
    data=(p/'trace.jsonl').read_bytes();assert data
    if trace is None:trace=data
    assert data==trace,'unmasked OFF CPU/cost/observations';rows=[json.loads(x) for x in data.splitlines()]
    assert sum(x['pc']==0x1e6d48 for x in rows)==sum(x['pc']==0x6d480000 for x in rows)==n
    assert 'VT entries=0 shadows=0 free=0 starts=0 ordinary=0 selectors=0 commits=0 rejected=0 lost=0' in (p/'run.log').read_text()
   summary['off_runs']+=1;summary['off_updates']+=n
 totals={k:0 for k in ['entries','shadows','free','starts','ordinary','selectors','commits','rejected']}
 for tag,n in {'long':800,'state3':201,'low-rpm':351,'moving':351,'loss':351}.items():
  reference=None;trace=None
  for mode in ['on','shadow','repeat']:
   p=on/(tag+'-'+mode);assert load(p/'result.json')['exit']==0;cmd=load(p/'command.json');assert sha(Path(cmd['argv'][0]))==cmd['binary_sha256'];assert sha(Path(cmd['state']['path']))==cmd['state']['sha256']
   assert '--virtual-transmission' in cmd['argv'] and not any(x in cmd['argv'] for x in ['--ram-word','--gt3-triple','--gt3-clean-admission'])
   result=artifacts(p)
   if reference is None:reference=result
   assert result==reference
   data=(p/'trace.jsonl').read_bytes()
   if trace is None:trace=data
   assert data==trace,'unmasked ON/repeat/shadow CPU/cost'
   match=re.search(r'VT entries=([^\n]+)',(p/'run.log').read_text());assert match
   counts={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)', 'entries='+match[1])}
   assert counts['entries']==counts['selectors']==n and counts['shadows']==(0 if mode=='on' else n)
   for k in totals:totals[k]+=counts[k]
   summary['on_runs']+=1;summary['on_updates']+=n
  rows=[json.loads(x) for x in trace.splitlines()];frames={}
  for x in rows:
   assert len(x['cpu'])==2880;by=frames.setdefault(x['frame'],{});assert x['pc'] not in by,'unqualified/duplicate player probe';by[x['pc']]=x
  assert len(frames)==n
  evidence={'free':0,'starts':[],'cancel2':[],'cancel3':[],'crossings':[],'original_aborts':[],'ratios':set(),'rejected':[],'held_rpm':set(),'lost_updates':0,'conflicting_native_commands':0}
  for fr,by in sorted(frames.items()):
   for pc in [0x1e6ec8,0x1e6d48,0x6d480000,0x1e5b98,0x1e5d54,0x1e7500,0x1e77e0,0x1e77f8,0x1e783c]:assert pc in by,(tag,fr,hex(pc))
   a=by[0x1e6d48];b=by[0x6d480000];drive=by[0x1e5b98];pre=by[0x1e5d54];e=by[0x1e7500];after=by[0x1e77e0];selection=by[0x1e77f8];end=by[0x1e783c]
   assert b['state']==drive['state']==e['state'];assert pre['term']==cpu_word(pre,560+21*4)&0x7fffffff
   assert e['rear']==mul(cpu_word(pre,560+21*4),ratios[pre['selected']]),(tag,fr,'original rear product')
   assert b['selected']==a['selected'] and b['engine']==a['engine'],'admission cannot commit or snap engine'
   if b['route']==1:
    assert b['state']==after['state']==0 and e['term']&0x7fffffff==e['rear']&0x7fffffff==0
    evidence['free']+=1;evidence['held_rpm'].add(e['rpm'])
    if a['state']==2:evidence['cancel2'].append(fr)
    if a['state']==3:evidence['cancel3'].append(fr)
   elif b['route']==2:
    assert a['state']==0 and b['state']==2 and b['saved_engine']==a['engine'];evidence['starts'].append(fr)
   else:assert b['state']==(0 if a['state']==1 and key(a['candidate'])==0 else a['state'])
   pending=b['gear']>=0 and b['gear']!=b['selected'];value=int.from_bytes(bytes.fromhex(selection['cpu'])[32:40],'little',signed=True)
   assert value==(b['gear'] if pending else -1)
   if pending:assert after['state']==end['state']==0 and end['selected']==b['gear']
   else:assert end['selected']==a['selected']
   assert 0<=end['selected']<=end['maximum'];evidence['ratios'].add(end['selected'])
   if b['rejected']:evidence['rejected'].append(fr)
   if b['lost']:assert b['route']==1 and b['gear']==-1 and not pending;evidence['lost_updates']+=1
   if b['relative'] and not pending:evidence['conflicting_native_commands']+=1
   # Original policy1 synchronization/clamp projection, not whole-engine ABI proof.
   if e['state']:
    q=by[0x1e7590];target=cpu_word(q,560);pred=q['state'];engine=q['engine'];inh=q['inhibition']
    if pred==1:engine=target
    elif pred in (2,3):
     crossed=(key(q['saved_engine'])<=key(q['target']) and key(target)<=key(engine)) or (key(q['target'])<=key(q['saved_engine']) and key(engine)<=key(target))
     if crossed:pred=1;engine=target;inh=12;evidence['crossings'].append(fr)
     elif pred==3 and key(q['target'])<=key(idle):pred=0;evidence['original_aborts'].append(fr)
     elif pred==2 and key(q['brake'])>key(0x3f400000) and (key(engine)<key(idle500) or key(word(gp-30000))<key(q['speed'])<key(word(gp-30004))):pred=0;evidence['original_aborts'].append(fr)
    engine=0 if key(engine)<0 else upper if key(upper)<=key(engine) else engine
    assert (after['state'],after['engine'],after['inhibition'])==(pred,engine,inh),(tag,fr,'original sync/clamp/completion')
  evidence['ratios']=sorted(evidence['ratios']);evidence['held_rpm']=len(evidence['held_rpm']);summary['cases'][tag]=evidence
 assert summary['cases']['state3']['cancel3']==[4522]
 assert summary['cases']['long']['ratios']==list(range(7)) and summary['cases']['long']['held_rpm']>20 and summary['cases']['long']['conflicting_native_commands']>0
 assert summary['cases']['long']['rejected'] and summary['cases']['low-rpm']['crossings']
 assert summary['cases']['loss']['cancel2'] and summary['cases']['loss']['lost_updates']==349
 assert summary['cases']['moving']['starts'][0]==5350 and summary['cases']['low-rpm']['starts'][0]==5351
 # Identical native moving first-entry CPU: original directional veto vs new admission2.
 oldrows=[json.loads(x) for x in (off/'moving-trace/trace.jsonl').read_text().splitlines()];newrows=[json.loads(x) for x in (on/'moving-on/trace.jsonl').read_text().splitlines()]
 first=lambda rr,pc:next(x for x in rr if x['pc']==pc)
 assert first(oldrows,0x1e6d48)['cpu']==first(newrows,0x1e6d48)['cpu']
 assert first(oldrows,0x6d480000)['state']==0 and first(newrows,0x6d480000)['state']==2
 # Braked fixture starts in gear4: original ratio-only commit1 occurs5350, then
 # start2 at5351. Exact original admission predicate on these observed native inputs.
 rr=[json.loads(x) for x in (on/'low-rpm-on/trace.jsonl').read_text().splitlines()]
 a=next(x for x in rr if x['pc']==0x1e6d48 and x['frame']==5351)
 directional=(key(word(gp-30060))<key(a['speed']) and a['selected']!=0) or (key(a['speed'])<key(word(gp-30056)) and a['selected']==0)
 signed_rpm=a['rpm']-65536 if a['rpm']&32768 else a['rpm']
 original_accept=(key(a['accelerator'])>key(0x3e800000)) if directional else half(car+0x234)<signed_rpm
 assert a['state']==0 and key(a['candidate'])!=0 and not original_accept and signed_rpm==799
 summary['totals']=totals;assert summary['off_runs']==42 and summary['on_runs']==15 and summary['off_updates']==16128 and summary['on_updates']==6162
 return summary

def public_test():
 with tempfile.TemporaryDirectory(prefix='gt3-extension-public-') as d:
  exe=Path(d)/'controller';subprocess.run(['clang++','-std=c++20','-O2','-Wall','-Wextra','-I'+str(ROOT),ROOT/'tests/gt3_extensions/controller_test.cpp',ROOT/'extensions/gt3/virtual_transmission/controller.cpp','-o',exe],check=True);subprocess.run([exe],check=True)

def private(root):
 d=load(DB);check_record(d);h=root/HOME;p=root/d['private']['manifest'];assert sha(p)==d['private']['sha256'];manifest=load(p);assert len(manifest['files'])==d['private']['members'];verify_members(root,manifest)
 index=load(h/'source-index-final.json');assert index=={'sources':d['sources'],'protected':d['protected'],'source_base':d['source_base']}
 before=load(root/'local/extension-architecture-v1/before.json')
 for p,v in before['tracked'].items():assert sha(root/p)==v,p
 old=module('extension_unchanged_state',ROOT/'scripts/project/transmission_state.py');old.private(root)
 for name in ['contracts-attempt-6','extended-off-attempt-5','extended-on-attempt-5','baseline-control-attempt-5']:
  out=h/name;i=load(out/'identity.json')
  for p,v in i['files'].items():assert sha(out/p)==v,p
  for p,v in i['sources'].items():assert sha(ROOT/p)==v,p
  assert i['canonical_installation'] is False
 result=subprocess.run([h/'contracts-attempt-6/contracts',root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf'],capture_output=True,check=True);assert result.stdout==(h/'contracts-attempt-6/contracts.log').read_bytes()
 result=subprocess.run([h/'contracts-reproduce-1/contracts',root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf'],capture_output=True,check=True);assert result.stdout==(h/'contracts-attempt-6/contracts.log').read_bytes()
 assert native(root)==load(h/'native-summary.json')
 exclusion=load(h/'binary-exclusion.json');assert exclusion['baseline_extension_symbols']==0 and exclusion['baseline_sha256']==sha(root/'local/baseline-v3/final-build/original/ps2run')
 for p,v in exclusion['files'].items():assert sha(Path(p))==v,p
 guards=load(h/'guard-tests-attempt-3/results.json');assert len(guards)==15
 state=load(root/'local/engagement-map-v1/states.json')['braked']['path']
 env={k:v for k,v in os.environ.items() if not k.startswith(('PS2_','GT3_'))};env['PS2_ONE_THREAD']='1'
 for item in guards:
  child=subprocess.run([h/'guard-test-complete',root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf',state,item['case'],root/'local/game-input/gt3-usa-v1.10.iso'],capture_output=True,env=env,timeout=30)
  assert child.returncode==item['exit']==1 and item['expected'].encode() in child.stderr and b'RPC server is missing' not in child.stderr and b'UNSAFE CONTINUATION' not in child.stderr
 for kind in ['initial','event']:
  child=subprocess.run([h/'input-connection-complete',root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf',state,kind,root/'local/game-input/gt3-usa-v1.10.iso'],capture_output=True,env=env,timeout=30);assert child.returncode==0 and b'unchanged PASS' in child.stdout
 cli=load(h/'cli-rejections/results.json');assert len(cli)==21
 for item in cli:
  e={k:v for k,v in env.items() if k!='PS2_ONE_THREAD'}
  if item['PS2_ONE_THREAD']:e['PS2_ONE_THREAD']='1'
  child=subprocess.run(item['argv'],capture_output=True,env=e,timeout=30);assert child.returncode==item['exit']==2
 for pair in load(h/'reproducible-builds.json'):assert sha(h/pair['left'])==sha(h/pair['right'])==pair['sha256']
 for exe in [root/'local/baseline-v3/final-build/original/ps2run',h/'baseline-control-attempt-5/ps2run-baseline-control']:
  assert b'gt3::extensions' not in subprocess.check_output(['nm','-C',exe])
 assert b'extensions/gt3' not in (h/'baseline-control-attempt-5/link.map').read_bytes()
 assert b'Controller::step' not in subprocess.check_output(['nm','-C',h/'extended-off-attempt-5/ps2run-extensions'])
 assert b'gt3::extensions::vt::Controller::step' in subprocess.check_output(['nm','-C',h/'extended-on-attempt-5/ps2run-extensions'])
 print('Virtual transmission bounded extension PASS:baseline excluded;12288 contracts/192 wholeRAM;42 OFF runs/16128 updates;15 ON runs/6162 updates;4108 real-entry controlled-original CPU+32MiB shadows;terminal loss latch. Not canonical/all-car/device/hardware or whole-engine ABI proof.')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','test','verify']);p.add_argument('root',nargs='?',type=Path);a=p.parse_args()
 if a.command=='check':check_record(load(DB));print('Optional extension authority/source isolation PASS; not native proof')
 elif a.command=='test':public_test()
 else:
  if a.root is None:p.error('verify requires explicit repository root')
  assert a.root.resolve(strict=True)==ROOT;private(a.root.resolve())
if __name__=='__main__':main()
