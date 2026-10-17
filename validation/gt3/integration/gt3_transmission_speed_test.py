"""Public authority/guard negatives. No game inputs, executables or private reads."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=module('speed_authority',ROOT/'scripts/project/transmission_speed.py')
class Authority(unittest.TestCase):
 def setUp(self):self.record=json.loads(M.DB.read_text())
 def test_current(self):M.check_record(self.record)
 def test_reject_claim_expansion(self):
  for field,value in [('canonical_installation',True),('validation_only',False),('build_default',True),('runtime_default',True),('selector_modified',True),('lifecycle','identified'),('source_base_commit','0'*40),('baseline_source_commit','0'*40),('low_budget_policy','ignore polls'),('selector_authority','other.json'),('limitations',[])]:
   with self.subTest(field=field):
    d=copy.deepcopy(self.record);d[field]=value
    with self.assertRaises(AssertionError):M.check_record(d)
 def test_exact_boundary(self):
  d=copy.deepcopy(self.record);d['boundary']['bytes']=143
  with self.assertRaises(AssertionError):M.check_record(d)
 def test_exact_coverage(self):
  for k in M.COVERAGE:
   with self.subTest(k=k):
    d=copy.deepcopy(self.record);d['coverage'][k]+=1
    with self.assertRaises(AssertionError):M.check_record(d)
 def test_missing_or_unpassed_gate(self):
  for action in ['missing','unpassed']:
   d=copy.deepcopy(self.record)
   if action=='missing':del d['gates']['real-entry-native']
   else:d['gates']['real-entry-native']='unknown'
   with self.assertRaises(AssertionError):M.check_record(d)
 def test_required_source_and_protected_hashes(self):
  for group in ['sources','protected']:
   for action in ['missing','changed']:
    d=copy.deepcopy(self.record);key=next(iter(d[group]))
    if action=='missing':del d[group][key]
    else:d[group][key]='0'*64
    with self.assertRaises(AssertionError):M.check_record(d)
 def test_manifest_requires_exact_read(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);p=root/M.HOME/'synthetic';p.parent.mkdir(parents=True);p.write_bytes(b'synthetic')
   manifest={'files':[dict(path=str(p.relative_to(root)),bytes=9,sha256=M.sha(p))]}
   M.verify_members(root,manifest);p.write_bytes(b'changed')
   with self.assertRaises(AssertionError):M.verify_members(root,manifest)
   p.unlink()
   with self.assertRaises(FileNotFoundError):M.verify_members(root,manifest)
 def test_manifest_does_not_escape_root(self):
  for path in ['/etc/passwd','../outside','local/elsewhere']:
   with self.assertRaises(AssertionError):M.verify_members(ROOT,{'files':[dict(path=path)]})
 def test_manifest_duplicate(self):
  with self.assertRaises(AssertionError):M.verify_members(ROOT,{'files':[dict(path=M.HOME+'/a')]*2})
 def test_trace_preserves_every_other_field(self):
  self.assertEqual(M.semantic([dict(transport_pc=1,cpu='abc')]),M.semantic([dict(transport_pc=2,cpu='abc')]))
  self.assertNotEqual(M.semantic([dict(transport_pc=1,cpu='abc')]),M.semantic([dict(transport_pc=1,cpu='abd')]))
 def test_build_is_off_unless_explicit(self):
  b=module('speed_builder',ROOT/'scripts/validate_gt3_transmission_speed.py')
  with tempfile.TemporaryDirectory() as tmp:
   for enabled in [False,True]:
    args=['builder','integrate',tmp,tmp,tmp]+(['--enable-clean'] if enabled else [])
    with patch.object(sys,'argv',args),patch.object(b,'integrate') as run:
     b.main();self.assertEqual(run.call_args.args[-1],enabled)
 def test_unchanged_selector_verifier_api(self):
  old=module('selector_contract',ROOT/'scripts/project/transmission.py')
  self.assertTrue(callable(old.verify))
  with patch.object(M,'import_file') as imported:
   M.verify_selector(ROOT);imported.return_value.verify.assert_called_once_with(ROOT)
 def test_verify_requires_explicit_root(self):
  # The OLD CLI is a version-qualified Git source, not an active executable.
  launcher="import pathlib,sys,sitecustomize; assert sitecustomize.CONTEXT_READY; p=pathlib.Path(sys.argv[1]); sys.path.insert(0,str(p.parent)); sys.argv=sys.argv[1:]; exec(compile(p.read_bytes(),str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
  p=subprocess.run([sys.executable,'-B','-c',launcher,str(ROOT/'scripts/project/transmission_speed.py'),'verify'],capture_output=True,text=True)
  self.assertEqual(p.returncode,2);self.assertIn('explicit repository root',p.stderr)
if __name__=='__main__':unittest.main()
