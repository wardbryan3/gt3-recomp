"""Metadata/trace-decoder checks only; no synthetic pedal behavior fixture."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('admission',ROOT/'scripts/audit_gt3_pedal_admission.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
class AdmissionMetadata(unittest.TestCase):
    def test_decoder_preserves_low_64_bit_lanes(self):
        words=[0]*363;words[29*4]=0x12345678;words[29*4+1]=0x9abcdef0
        row={'cpu':''.join(f'{w:08x}' for w in words)}
        self.assertEqual(audit.reg(audit.cpu_words(row),29),0x9abcdef012345678)
        with self.assertRaises(AssertionError):audit.cpu_words({'cpu':row['cpu'][:-8]})
    def test_audit_cannot_promote_or_authorize(self):
        record=json.loads((ROOT/'decomp/gt3/pedal-admission-49af40.json').read_text())
        audit.check_record(record)
        for key,value in [('status','passing'),('guard_expansion_authorized',True),('safe_admission_established',True),('command_storage','global BSS command buffer')]:
            bad=copy.deepcopy(record);bad[key]=value
            with self.assertRaises(AssertionError):audit.check_record(bad)
    def test_fallback_is_not_body_differential(self):
        record=json.loads((ROOT/'decomp/gt3/pedal-admission-49af40.json').read_text())
        self.assertEqual(record['analysis']['fallback_comparison']['replaced'],0)
        self.assertIn('not established',record['analysis']['actual_49af40_clean_body_differential'])
        self.assertFalse(record['analysis']['new_live_execution'])
if __name__=='__main__':unittest.main()
