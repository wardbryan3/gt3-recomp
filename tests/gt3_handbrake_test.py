"""Public proof-reducer negatives; no original game files."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('handbrake_proof', ROOT / 'scripts/project/handbrake.py')
proof = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proof)


def rows():
    result = []
    for pc in proof.STAGES:
        cpu = ['0'] * 3000
        cpu[1096:1104] = f'{pc:08x}'
        if pc == 0x1e3aac:
            cpu[6 * 32:6 * 32 + 8] = '00000001'
        result.append(dict(frame=4802, pc=pc, cpu=''.join(cpu), flags=16, input=0,
                           processed=0, wheel_brake=[0, 0, 0, 0]))
    return result


class HandbrakeProofTests(unittest.TestCase):
    def test_public_record(self):
        proof.check_record(json.loads(proof.DB.read_text()))

    def test_runtime_guardrails(self):
        base = json.loads(proof.DB.read_text())
        for key in ['build_default', 'runtime_default', 'canonical_installation']:
            changed = copy.deepcopy(base); changed['runtime'][key] = True
            with self.assertRaises(AssertionError):
                proof.check_record(changed)
        changed = copy.deepcopy(base); changed['coverage']['digital_live_proven'] = True
        with self.assertRaises(AssertionError):
            proof.check_record(changed)

    def test_required_evidence_cannot_disappear(self):
        changed = json.loads(proof.DB.read_text()); changed['artifacts'] = []
        with self.assertRaises(AssertionError):
            proof.check_record(changed)

    def test_frozen_requires_all_gates(self):
        changed = json.loads(proof.DB.read_text()); changed['gates']['native_v3'] = 'not-validated'
        changed['lifecycle'] = 'frozen'
        with self.assertRaises(AssertionError):
            proof.check_record(changed)

    def test_synthetic_rows(self):
        proof.review_rows(rows(), 1)

    def test_missing_stage(self):
        with self.assertRaises(AssertionError):
            proof.review_rows(rows()[:-1], 1)

    def test_bad_join(self):
        changed = rows(); changed[1]['processed'] = 0x3f800000
        with self.assertRaises(AssertionError):
            proof.review_rows(changed, 1)

    def test_wrong_shift_boundary(self):
        changed = rows(); row = next(r for r in changed if r['pc'] == 0x1e3aac)
        row['cpu'] = row['cpu'][:192] + '00000000' + row['cpu'][200:]
        with self.assertRaises(AssertionError):
            proof.review_rows(changed, 1)

    def test_wrong_semantic_pc(self):
        changed = rows(); changed[0]['cpu'] = '0' * 3000
        with self.assertRaises(AssertionError):
            proof.review_rows(changed, 1)

    def test_digital_not_promoted_to_live(self):
        changed = rows(); changed[0]['flags'] = 0
        with self.assertRaises(AssertionError):
            proof.review_rows(changed, 1)

    def test_transport_pc_only_is_normalized(self):
        a, b = rows(), rows(); a[0]['transport_pc'] = 1; b[0]['transport_pc'] = 2
        self.assertEqual(proof.semantic(a), proof.semantic(b))
        b[0]['cpu'] = 'f' * 3000
        self.assertNotEqual(proof.semantic(a), proof.semantic(b))


if __name__ == '__main__':
    unittest.main()
