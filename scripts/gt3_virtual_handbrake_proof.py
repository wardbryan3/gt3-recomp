"""Virtual handbrake trace reducer. Public synthetic tests are not a game oracle."""
from collections import Counter,defaultdict
import hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_rows(path):return [json.loads(line) for line in Path(path).read_text().splitlines()]
def semantic(rows):return [{k:v for k,v in row.items() if k!='transport_pc'} for row in rows]
def quantize(value):
 assert math.isfinite(value) and 0<=value<=1
 numerator,denominator=float(value).as_integer_ratio()
 return (8192*numerator+denominator)//(2*denominator)
def review_rows(rows,expected,table=None):
 counts=Counter(row['stage'] for row in rows)
 required=['before-command','command','entry','join','restored','coupling','brake','brake-join','engine','shift']
 assert all(counts[stage]==expected for stage in required),counts
 groups=defaultdict(dict)
 for row in rows:
  stage=row['stage'];assert stage in required and stage not in groups[row['frame']]
  assert len(row['bytes'])==16 and all(isinstance(n,int) and 0<=n<=255 for n in row['bytes'])
  assert len(row['wheel_brake'])==4 and row['enabled'] is True
  groups[row['frame']][stage]=row
 assert len(groups)==expected
 codes=set()
 for frame,group in groups.items():
  assert set(group)==set(required)
  before=group['before-command'];command=group['command'];entry=group['entry'];join=group['join'];restored=group['restored']
  value=command['host_value'];assert math.isfinite(value) and 0<=value<=1
  q=quantize(value);codes.add(q)
  packet=list(before['bytes']);packet[0]|=16;packet[14]=q&255;packet[15]=q>>8
  assert all(group[s]['bytes']==packet for s in ['command','entry','join','coupling'])
  assert restored['bytes']==before['bytes']
  assert all(row['car']==before['car'] and row['command']==before['command'] and row['host_value']==value for row in group.values())
  # Original processed state, not adapter-owned state. Exact generated reference
  # table is optional ONLY for game-free synthetic reducer tests.
  if table is not None:
   original=table[join['floor'],q];assert original['q']==q and original['floor']==join['floor']
   assert join['processed']==original['processed']
  assert 0<=join['processed']<=0x3f800000
  if q==0:assert join['processed']==0
  if q==4096:assert join['processed']==0x3f800000
  assert all(group[s]['processed']==join['processed'] for s in ['coupling','restored','brake','brake-join','engine','shift'])
 return codes
