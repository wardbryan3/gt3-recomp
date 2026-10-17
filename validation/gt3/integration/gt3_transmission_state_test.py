#!/usr/bin/env python3
"""Artifact-free authority, isolation and fail-closed regression tests."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[3]
s=importlib.util.spec_from_file_location('state_authority',ROOT/'scripts/project/transmission_state.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class StateAuthority(unittest.TestCase):
 def test_public_authority(self):m.check_record(m.load(m.DB))
 def bad(self,change):
  d=copy.deepcopy(m.load(m.DB));change(d)
  with self.assertRaises(AssertionError):m.check_record(d)
 def test_no_canonical(self):self.bad(lambda d:d['runtime'].__setitem__('canonical_installation',True))
 def test_no_default_runtime(self):self.bad(lambda d:d['runtime'].__setitem__('runtime_default',True))
 def test_no_default_build(self):self.bad(lambda d:d['runtime'].__setitem__('build_default',True))
 def test_no_engine_abi_promotion(self):self.bad(lambda d:d['recovered']['synchronization'].__setitem__('abi_replacement',True))
 def test_no_selection_abi_promotion(self):self.bad(lambda d:d['recovered']['selection'].__setitem__('abi_replacement',True))
 def test_boundary_not_whole_program(self):self.bad(lambda d:d['recovered']['admission'].__setitem__('boundary',['001e6d48','001e77df']))
 def test_source_pins_required(self):self.bad(lambda d:d['sources'].pop('host/gt3_transmission_state.cpp'))
 def test_source_drift(self):self.bad(lambda d:d['sources'].__setitem__('host/gt3_transmission_state.cpp','0'*64))
 def test_counts_not_promoted(self):self.bad(lambda d:d['proof'].__setitem__('whole_ram_cases',156464))
 def test_protected_drift(self):self.bad(lambda d:d['protected'].__setitem__('host/gt3_clean_transmission.cpp','0'*64))
 def test_inherited_api(self):
  old=m.module('state_test_inherited',ROOT/'scripts/project/transmission_speed.py');self.assertTrue(callable(old.private));self.assertIn('old.private(root)',Path(m.__file__).read_text())
 def test_isolation(self):
  for p in ['CMakeLists.txt','host/main.cpp','justfile']:
   text=(ROOT/p).read_text();self.assertNotIn('gt3_clean_transmission_admission',text);self.assertNotIn('--gt3-clean-admission',text)
 def test_member_missing_changed(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/m.HOME/'example';p.parent.mkdir(parents=True);p.write_text('observed')
   manifest={'schema_version':1,'files':[{'path':str(p.relative_to(root)),'sha256':m.sha(p)}]};m.verify_members(root,manifest)
   p.write_text('changed')
   with self.assertRaises(AssertionError):m.verify_members(root,manifest)
   p.unlink()
   with self.assertRaises(FileNotFoundError):m.verify_members(root,manifest)
 def test_member_paths(self):
  for paths in [['/tmp/outside'],[m.HOME+'/../outside'],[m.HOME+'/a',m.HOME+'/a'],[m.HOME+'/b',m.HOME+'/a']]:
   with self.assertRaises(AssertionError):m.verify_members(ROOT,{'schema_version':1,'files':[{'path':p,'sha256':'0'*64} for p in paths]})
if __name__=='__main__':unittest.main()
