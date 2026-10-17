"""Source-only reducer/authority negatives; synthetic metadata is not game proof."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts'))
from verify_gt3_pedal_closure import check_record,check_summaries,ROOT

class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.v=json.loads((ROOT/'decomp/gt3/pedal-closure.json').read_text())
        self.shadow={'mode':'shadow','cases':{}}
        self.live={'mode':'live','cases':{}}
        for name in self.v['cases']:
            n=299 if name=='time-trial' else 300
            self.shadow['cases'][name]={'entries':n,'actual_entry_full_cpu_32mib_cost_mutation_differential':True,
                'threads':[[10,0x493700,32768]],'parents':[0x17c848],'cost':[63,72],
                'hooks':[0x1f14e8 if name=='free-run' else 0x1ed860]}
            self.live['cases'][name]={'entries':n,'exact_cpu_steering_ram_captures':True,
                'clean_counts':[n,0,600 if name.startswith('compat-wheel-') else 0]}
    def test_public_record(self):check_record(self.v)
    def test_reducer_shape(self):check_summaries(self.v,self.shadow,self.live)
    def reject(self,mutate):
        shadow=copy.deepcopy(self.shadow);live=copy.deepcopy(self.live);mutate(shadow,live)
        with self.assertRaises(AssertionError):check_summaries(self.v,shadow,live)
    def test_missing_case(self):self.reject(lambda s,l:l['cases'].pop('license'))
    def test_fallback_is_not_equivalence(self):
        self.reject(lambda s,l:l['cases']['time-trial'].update(clean_counts=[0,299,0]))
    def test_inexact_actual_context(self):
        self.reject(lambda s,l:s['cases']['time-trial'].update(actual_entry_full_cpu_32mib_cost_mutation_differential=False))
    def test_wrong_owner(self):self.reject(lambda s,l:s['cases']['trusted'].update(threads=[[11,0x49af40,16]]))
    def test_wrong_hook(self):self.reject(lambda s,l:s['cases']['free-run'].update(hooks=[0x1ed860]))
    def test_wrong_cost(self):self.reject(lambda s,l:s['cases']['trusted'].update(cost=[63,153]))
    def test_native_is_not_compatibility(self):self.reject(lambda s,l:l['cases']['trusted'].update(clean_counts=[300,0,600]))
    def test_frozen_cannot_skip_gate(self):
        v=copy.deepcopy(self.v);v['lifecycle']='frozen';v['gates']['baseline']='pending'
        with self.assertRaises(AssertionError):check_record(v)
    def test_historical_source_artifact_required(self):
        v=copy.deepcopy(self.v);v['artifacts'].remove(v['historical_sources']['host/gt3_clean_pedals.cpp'])
        with self.assertRaises(AssertionError):check_record(v)
    def test_private_tree_cannot_be_public(self):
        v=copy.deepcopy(self.v);v['artifacts'][0]['visibility']='public'
        with self.assertRaises(AssertionError):check_record(v)

if __name__=='__main__':unittest.main()
