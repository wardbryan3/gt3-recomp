"""Virtual-pedal proof reduction. Synthetic metadata tests are not runtime evidence."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def review_rows(rows,n):
    stages=['before-command','command','entry','join','restored','brake-consumer','engine-consumer']
    groups={s:[r for r in rows if r['stage']==s] for s in stages}
    assert set(r['stage'] for r in rows)==set(stages)
    assert all(len(g)==n for g in groups.values()) and n>0
    nonpedal=['car','command','mode','steering_q','shift','auxiliary_q','other_q']
    for i in range(n):
        before,command,entry,join,restored,brake,engine=[groups[s][i] for s in stages]
        assert all(r['frame']==before['frame'] and r['enabled'] is True for r in [command,entry,join,restored,brake,engine])
        for r in [command,entry,restored]:assert all(r[k]==before[k] for k in nonpedal)
        for r in [command,entry]:
            assert r['flags']==before['flags']|6
            assert r['throttle_q']==int(r['host_throttle']*4096+0.5) and r['brake_q']==int(r['host_brake']*4096+0.5)
        assert all(restored[k]==before[k] for k in ['flags','throttle_q','brake_q'])
        assert all(brake[k]==engine[k]==join[k] for k in ['accelerator_bits','brake_bits'])
    return {'entries':n,'injected_values':sorted({(r['throttle_q'],r['brake_q']) for r in groups['entry']})}

def check_record(v,root=ROOT):
    assert v['schema_version']==1 and v['id']=='synthetic-virtual-pedals-v1'
    assert v['status'] in ('validating','validated-bounded')
    assert v['build_default'] is False and v['runtime_default'] is False and v['canonical_installation'] is False
    assert v['boundary']=={'inject':'0x001e4d5c','restore':'0x001e4e68','fields':['flags|6','command+8:uint16','command+10:int16-positive']}
    assert v['mapping']=={'domain':[0,1],'scale':4096,'rounding':'binary64 nearest, positive half ties up','physical_calibration':False}
    assert v['frozen_modified'] is False and v['writes_processed_car_state'] is False
    assert v['case_count']==12 and v['required_substitutions']==3599
    assert re.fullmatch('[a-f0-9]{40}',v['source_commit'])
    for p,h in v['sources'].items():assert sha(root/p)==h,p
    for p,h in v['protected'].items():assert sha(root/p)==h,('Protected source/authority changed',p)
    ids=set()
    for a in v['artifacts']:
        p=Path(a['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
        assert a['visibility']=='private' and re.fullmatch('[a-f0-9]{64}',a['sha256'])
        assert a['id'] not in ids;ids.add(a['id'])
    assert v['artifacts'] and set(v['gates'])=={'parser','oracle','live','regressions','strict','public'}
    assert all(s in ('pending','passing') for s in v['gates'].values())
    if v['status']=='validated-bounded':assert set(v['gates'].values())=={'passing'}
    return v
