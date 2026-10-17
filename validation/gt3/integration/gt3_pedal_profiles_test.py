"""Public metadata/bit-identity tests, NOT new pedal behavior fixtures."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('profiles',ROOT/'scripts/characterize_gt3_pedal_profiles.py')
profiles=importlib.util.module_from_spec(spec);spec.loader.exec_module(profiles)

class ProfilesMetadata(unittest.TestCase):
    def row(self):
        return dict(pc=profiles.ENTRY,car=0x1000,s0=0x1f84,control=0x2304,command=0x9000,gp=0x3579f0,
                    incoming_v1=0,kind=0,policy_blocked=0,stored_policy=0,auxiliary_suppression=0,
                    mode=2,flags=14,accelerator_descriptor=[1,2,3,4],brake_descriptor=[1,2,3,4],
                    slew=[0,0,0,0],floor=[0])
    def test_exact_bit_identity_and_separate_selectors(self):
        a=self.row();identity=profiles.profile(a)[0]
        for field,value in [('mode',3),('stored_policy',1),('auxiliary_suppression',1),('flags',12)]:
            b=copy.deepcopy(a);b[field]=value;self.assertNotEqual(identity,profiles.profile(b)[0])
        for field in ['accelerator_descriptor','brake_descriptor','slew','floor']:
            b=copy.deepcopy(a);b[field][-1]^=0x80000000
            self.assertNotEqual(identity,profiles.profile(b)[0])
    def test_no_transient_or_address_identity_guess(self):
        a=self.row();b=dict(a,car=0x2000,s0=0x2f84,control=0x3304,command=0x9100,history=7,accelerator_q=4096)
        self.assertEqual(profiles.profile(a),profiles.profile(b))
        b['policy_blocked']=1;b['stored_policy']=9
        self.assertEqual(profiles.profile(a),profiles.profile(b))
    def test_bad_shape_rejected(self):
        a=self.row();a['accelerator_descriptor']=[1,2,3]
        with self.assertRaises(AssertionError):profiles.profile(a)
        a=self.row();a['s0']+=4
        with self.assertRaises(AssertionError):profiles.profile(a)
    def test_same_configuration_retains_different_admission_contexts(self):
        with tempfile.TemporaryDirectory() as directory:
            directory=Path(directory);cases=[]
            for n,command in enumerate([0x9000,0x9100]):
                p=directory/str(n);p.mkdir();r=dict(self.row(),command=command);j=dict(r,pc=profiles.JOIN,s1=0)
                (p/'profiles.jsonl').write_text(json.dumps(r)+'\n'+json.dumps(j)+'\n')
                cases.append(dict(id=str(n),directory=str(p),reachability='native-pad',labels={}))
            summary=profiles.summarize({'cases':cases})
            self.assertEqual(1,len(summary['profiles']))
            self.assertEqual([0x9000,0x9100],summary['profiles'][0]['command_contexts'])
            cases[0]['reachability']='physical-wheel'
            with self.assertRaises(AssertionError):profiles.summarize({'cases':cases})
    def test_stopped_registry_not_successful_expansion(self):
        record=json.loads((ROOT/'decomp/gt3/pedal-profiles.json').read_text())
        profiles.check_record(record,ROOT)
        for field,value in [('status','passing'),('build_default',True),('runtime_default',True),('resume_address','0x001e4ba9')]:
            bad=copy.deepcopy(record);bad[field]=value
            with self.assertRaises(AssertionError):profiles.check_record(bad,ROOT)
        for field,value in [('stop_case_fallbacks',0),('exact_substitutions',1499),('fresh_full_native_regressions','passing')]:
            bad=copy.deepcopy(record);bad['results'][field]=value
            with self.assertRaises(AssertionError):profiles.check_record(bad,ROOT)
if __name__=='__main__':unittest.main()
