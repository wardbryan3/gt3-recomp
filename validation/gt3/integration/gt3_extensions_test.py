"""Public extension checks: no ISO, ELF, generated body or native fixture required."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
s=importlib.util.spec_from_file_location('optional_extensions',ROOT/'scripts/project/extensions.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Extensions(unittest.TestCase):
 def test_authority(self):m.check_record(m.load(m.DB))
 def test_canonical_or_default_install_rejected(self):
  for k in ['canonical_installation','build_default','runtime_default']:
   d=copy.deepcopy(m.load(m.DB));d['runtime'][k]=True
   with self.assertRaises(AssertionError):m.check_record(d)
 def test_missing_startup_gate_or_loss_latch_rejected(self):
  for k,v in [('startup_activation_only',False),('device_loss','original-fallback'),('clean_transmission_combination','supported')]:
   d=copy.deepcopy(m.load(m.DB));d['runtime'][k]=v
   with self.assertRaises(AssertionError):m.check_record(d)
 def test_recovery_misclassification_rejected(self):
  d=copy.deepcopy(m.load(m.DB));d['kind']='recovery'
  with self.assertRaises(AssertionError):m.check_record(d)
 def test_counts_not_weakened(self):
  d=copy.deepcopy(m.load(m.DB));d['proof']['contracts']-=1
  with self.assertRaises(AssertionError):m.check_record(d)
 def test_source_tamper_rejected(self):
  d=copy.deepcopy(m.load(m.DB));d['sources'][m.SOURCES[0]]='0'*64
  with self.assertRaises(AssertionError):m.check_record(d)
 def test_missing_source_rejected(self):
  d=copy.deepcopy(m.load(m.DB));d['sources'].pop(m.SOURCES[0])
  with self.assertRaises(AssertionError):m.check_record(d)
 def test_manifest_faults(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/m.HOME/'fixture';p.parent.mkdir(parents=True);p.write_bytes(b'public synthetic fixture')
   manifest={'files':[{'path':str(p.relative_to(root)),'sha256':m.sha(p)}]};m.verify_members(root,manifest)
   p.write_bytes(b'changed')
   with self.assertRaises(AssertionError):m.verify_members(root,manifest)
   p.unlink()
   with self.assertRaises(FileNotFoundError):m.verify_members(root,manifest)
 def test_escape_and_duplicate_rejected(self):
  for files in [[{'path':'../outside','sha256':'0'*64}],[{'path':m.HOME+'/a','sha256':'0'*64}]*2]:
   with self.assertRaises(AssertionError):m.verify_members(ROOT,{'files':files})
 def test_ee_keys_and_product(self):
  self.assertEqual(m.key(0x80000000),m.key(0));self.assertEqual(m.key(1),0)
  self.assertLess(m.key(0xbf800000),m.key(0));self.assertEqual(m.mul(0x3f800000,0x40000000),0x40000000)
  self.assertEqual(m.mul(0x80000000,0x3f800000),0x80000000)
if __name__=='__main__':unittest.main()
