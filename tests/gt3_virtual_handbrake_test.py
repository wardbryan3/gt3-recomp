"""Game-free compiled protocol and authority/reducer negatives, not EE proof."""
import copy,importlib.util,json,math,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('virtual_handbrake_authority',ROOT/'scripts/project/virtual_handbrake.py')
proof=importlib.util.module_from_spec(spec);spec.loader.exec_module(proof)
from gt3_virtual_handbrake_proof import review_rows,quantize
class VirtualHandbrakeTests(unittest.TestCase):
 def record(self):return json.loads(proof.DB.read_text())
 def test_compiled_protocol_and_adapter(self):
  with tempfile.TemporaryDirectory() as tmp:
   exe=Path(tmp)/'test';includes=['-I'+str(ROOT/'host'),'-I'+str(ROOT/'runtime/include')]
   subprocess.run(['clang++','-std=c++20','-O2',*includes,str(ROOT/'tests/gt3_virtual_handbrake_test.cpp'),'-o',str(exe)],check=True)
   result=subprocess.run([str(exe)],check=True,capture_output=True,text=True);self.assertIn('24585 independent exact mappings',result.stdout)
   subprocess.run(['clang++','-std=c++20','-O2',*includes,'-c',str(ROOT/'host/gt3_virtual_handbrake.cpp'),'-o',str(Path(tmp)/'adapter.o')],check=True)
 def test_exact_python_boundary_reference(self):
  for q in range(4097):self.assertEqual(quantize(q/4096),q)
  for q in range(4096):
   tie=(2*q+1)/8192
   for value,expected in [(math.nextafter(tie,0),q),(tie,q+1),(math.nextafter(tie,1),q+1)]:self.assertEqual(quantize(value),expected)
  for value in [-math.ulp(0.0),math.nextafter(1,2),math.inf,math.nan]:
   with self.assertRaises(AssertionError):quantize(value)
 def test_current_record(self):proof.check_record(self.record())
 def test_default_gates_and_scope(self):
  for field in ['build_default','runtime_default','canonical_installation','frozen_modified','writes_processed_car_state','physical_device_proof']:
   changed=self.record();changed[field]=True
   with self.assertRaises(AssertionError):proof.check_record(changed)
 def test_protocol_cannot_be_reinterpreted(self):
  for field,value in [('scale',255),('range',[0,2]),('reject_out_of_range',False),('physical_calibration',True),('rounding','clamp')]:
   changed=self.record();changed['mapping'][field]=value
   with self.assertRaises(AssertionError):proof.check_record(changed)
 def test_source_or_frozen_drift_rejected(self):
  for section in ['sources','protected']:
   changed=self.record();changed[section][next(iter(changed[section]))]='0'*64
   with self.assertRaises(AssertionError):proof.check_record(changed)
 def test_proof_cannot_disappear(self):
  changed=self.record();changed['artifacts']=[]
  with self.assertRaises(AssertionError):proof.check_record(changed)
  changed=self.record();del changed['protected']['host/gt3_clean_handbrake.cpp']
  with self.assertRaises(AssertionError):proof.check_record(changed)
 def test_validation_requires_every_gate(self):
  changed=self.record();changed['status']='validated-bounded';changed['gates']['native_v3']='pending'
  with self.assertRaises(AssertionError):proof.check_record(changed)
 def fixture(self):
  packet=[1,2,0,90,0,0,0,0,0,8,0,4,0,0,17,0]
  before=dict(stage='before-command',pc=0x1e4d5c,frame=10,enabled=True,car=0x600000,command=0x49af40,host_value=0,bytes=packet,floor=0x3dcccccc,processed=0,coupling_candidate=0,wheel_brake=[0,0,0,0])
  rows=[]
  for stage in ['before-command','command','entry','join','coupling','restored','shift','brake','brake-join','engine']:
   row=copy.deepcopy(before);row['stage']=stage
   if stage in ['command','entry','join','coupling']:row['bytes'][0]|=16;row['bytes'][14:16]=[0,0]
   rows.append(row)
  return rows
 def test_synthetic_reducer_shape_only(self):self.assertEqual(review_rows(self.fixture(),1),{0})
 def test_reducer_rejects_unrelated_mutations_or_wrong_state(self):
  for index,field,value in [(1,'host_value',.5),(2,'car',0x600004),(3,'processed',1),(4,'command',0x49af50),(7,'processed',1),(2,'frame',11)]:
   rows=self.fixture();rows[index][field]=value
   with self.assertRaises(AssertionError):review_rows(rows,1)
  for index,byte in [(1,14),(2,2),(3,8),(5,0)]:
   rows=self.fixture();rows[index]['bytes'][byte]^=1
   with self.assertRaises(AssertionError):review_rows(rows,1)
 def test_reducer_requires_every_original_stage(self):
  with self.assertRaises(AssertionError):review_rows(self.fixture()[:-1],1)
  rows=self.fixture();rows.append(copy.deepcopy(rows[2]))
  with self.assertRaises(AssertionError):review_rows(rows,1)
 def test_reducer_uses_exact_observed_calibration(self):
  table={(0x3dcccccc,0):dict(q=0,floor=0x3dcccccc,processed=0)}
  self.assertEqual(review_rows(self.fixture(),1,table),{0})
  table[0x3dcccccc,0]['processed']=1
  with self.assertRaises(AssertionError):review_rows(self.fixture(),1,table)
  with self.assertRaises(KeyError):review_rows(self.fixture(),1,{(0x3dcccccd,0):dict(q=0,floor=0x3dcccccd,processed=0)})
if __name__=='__main__':unittest.main()
