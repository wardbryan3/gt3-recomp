"""Game-free schema/reducer negatives and compiled pure parser/mapping tests."""
import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from gt3_virtual_pedal_proof import check_record,review_rows
class VirtualPedalTests(unittest.TestCase):
 def test_compiled_parser_mapping_schedule(self):
  with tempfile.TemporaryDirectory() as tmp:
   exe=Path(tmp)/'test'
   subprocess.run(['clang++','-std=c++20','-O2','-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include'),str(ROOT/'tests/gt3_virtual_pedals_test.cpp'),'-o',str(exe)],check=True)
   run=subprocess.run([str(exe)],check=True,text=True,capture_output=True);self.assertIn('8193 exact quantizations',run.stdout)
 def test_current_record(self):check_record(json.loads((ROOT/'decomp/gt3/virtual-pedals.json').read_text()))
 def test_no_canonical_or_physical_claim(self):
  original=json.loads((ROOT/'decomp/gt3/virtual-pedals.json').read_text())
  for field in ['canonical_installation','frozen_modified','writes_processed_car_state','build_default','runtime_default']:
   v=copy.deepcopy(original);v[field]=True
   with self.assertRaises(AssertionError):check_record(v)
  v=copy.deepcopy(original);v['mapping']['physical_calibration']=True
  with self.assertRaises(AssertionError):check_record(v)
 def fixture(self):
  before=dict(stage='before-command',frame=10,enabled=True,car=0x600000,command=0x49af40,flags=1,mode=2,steering_q=-100,shift=0,auxiliary_q=0,other_q=0,throttle_q=4096,brake_q=0,host_throttle=.5,host_brake=0,accelerator_bits=0x3f000000,brake_bits=0)
  rows=[]
  for stage in ['before-command','command','entry','join','restored','brake-consumer','engine-consumer']:
   row=dict(before,stage=stage)
   if stage in ('command','entry','join'):row.update(flags=7,throttle_q=2048)
   rows.append(row)
  return rows
 def test_reducer_synthetic_shape_only(self):review_rows(self.fixture(),1)
 def test_reducer_rejects_wrong_path(self):
  for field,value,index in [('throttle_q',4096,2),('steering_q',100,2),('flags',7,4),('brake_bits',1,6),('frame',11,1)]:
   rows=self.fixture();rows[index][field]=value
   with self.assertRaises(AssertionError):review_rows(rows,1)
  with self.assertRaises(AssertionError):review_rows(self.fixture()[:-1],1)
 def test_source_or_protection_drift_rejected(self):
  for section in ['sources','protected']:
   v=json.loads((ROOT/'decomp/gt3/virtual-pedals.json').read_text());v[section][next(iter(v[section]))]='0'*64
   with self.assertRaises(AssertionError):check_record(v)
 def test_success_requires_all_gates(self):
  v=json.loads((ROOT/'decomp/gt3/virtual-pedals.json').read_text());v['status']='validated-bounded';v['gates']['oracle']='pending'
  with self.assertRaises(AssertionError):check_record(v)
if __name__=='__main__':unittest.main()
