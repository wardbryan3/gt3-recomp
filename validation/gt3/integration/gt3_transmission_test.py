"""Public authority/reducer negatives; synthetic rows are NOT original proof."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('transmission_proof',ROOT/'scripts/project/transmission.py')
proof=importlib.util.module_from_spec(spec);spec.loader.exec_module(proof)


def rows():
    before=dict(frame=4501,pc=0x1e5458,car=0x1fbb7bc,sp=0x49af30,ra=0x1e5730,
        budget=5000,v0=123,aux=0,relative=0,selected=1,state=0,policy=1,owner=0,
        mode=0,suppression=0,inhibition=0,candidate_bits=0,accelerator_bits=0,speed_bits=0)
    after=dict(before,pc=0x1e5730,budget=4980,v0=0xffffffff)
    return [before,after]


class TransmissionTests(unittest.TestCase):
    def test_public_authority(self):
        proof.check_record(json.loads(proof.DB.read_text()))

    def test_default_and_installation_negatives(self):
        for name in ['build_default','runtime_default','canonical_installation']:
            changed=json.loads(proof.DB.read_text());changed['runtime'][name]=True
            with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_no_unearned_coverage(self):
        for name in ['all_cars_modes','physical_proof']:
            changed=json.loads(proof.DB.read_text());changed['coverage'][name]=True
            with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_frozen_requires_passing_gates(self):
        changed=json.loads(proof.DB.read_text());changed['lifecycle']='frozen';changed['gates']['strict_evidence']='not-validated'
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_required_gate_cannot_disappear(self):
        changed=json.loads(proof.DB.read_text());changed['gates'].pop('strict_evidence')
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_missing_evidence_rejected(self):
        changed=json.loads(proof.DB.read_text());changed['artifacts']=[]
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_boundary_not_broadened(self):
        changed=json.loads(proof.DB.read_text());changed['boundary'][1]='0x001e5540'
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_generated_dependency_not_silently_recovered(self):
        changed=json.loads(proof.DB.read_text());changed['dependencies_generated']=[]
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_historical_documentation_not_skipped(self):
        changed=json.loads(proof.DB.read_text());changed['historical_public_versions']=[]
        with self.assertRaises(AssertionError):proof.check_record(changed)

    def test_synthetic_pair(self):
        self.assertEqual(proof.review_trace(rows(),1)['entries'],1)

    def test_missing_exit(self):
        with self.assertRaises(AssertionError):proof.review_trace(rows()[:-1],1)

    def test_owner_lifetime_and_cost(self):
        for field,value in [('owner',1),('sp',0x49af40),('ra',0x1e5734),('budget',5001),('car',0x1fbb790)]:
            changed=rows();changed[1][field]=value
            with self.assertRaises(AssertionError):proof.review_trace(changed,1)

    def test_selection_state_not_committed_by_selector(self):
        for field in ['selected','state','candidate_bits','relative','aux']:
            changed=rows();changed[1][field]^=1
            with self.assertRaises(AssertionError):proof.review_trace(changed,1)

    def test_at_noninterference_not_mt_coverage(self):
        self.assertEqual(proof.review_trace([],0)['entries'],0)
        with self.assertRaises(AssertionError):proof.review_trace(rows(),0)


if __name__=='__main__':unittest.main()
