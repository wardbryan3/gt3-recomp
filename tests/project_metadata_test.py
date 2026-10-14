"""Negative consistency tests; never write or weaken immutable evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('project', Path(__file__).resolve().parents[1] / 'scripts/project/project.py')
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)
class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.data = {name:project.load(name) for name in ('manifest','symbols','types','provenance')}
    def rejected(self, mutation):
        data=copy.deepcopy(self.data);mutation(data)
        with patch.object(project,'load',side_effect=lambda name:data[name]):
            with self.assertRaises(AssertionError):project.check()
    def test_current(self): project.check()
    def test_unknown_state_rejected(self):
        self.rejected(lambda d:d['manifest']['functions'][0].update(lifecycle='looks-good'))
    def test_missing_evidence_rejected(self):
        self.rejected(lambda d:d['manifest']['functions'][0].update(evidence=['invented']))
    def test_frozen_requires_independent_validation(self):
        def mutate(d):
            f=next(f for f in d['manifest']['functions'] if f['lifecycle']=='frozen')
            f['live']['status']='not-validated'
        self.rejected(mutate)
    def test_partial_boundary_resume_rejected(self):
        def mutate(d):
            f=next(f for f in d['manifest']['functions'] if f.get('resume_address'))
            f['resume_address']='0x001e48f8'
        self.rejected(mutate)
    def test_malformed_hash_rejected(self):
        self.rejected(lambda d:d['provenance']['artifacts'][0].update(sha256='not-a-hash'))
    def test_duplicate_symbol_rejected(self):
        self.rejected(lambda d:d['symbols']['functions'].append(d['symbols']['functions'][0]))
    def test_offset_outside_partial_layout_rejected(self):
        self.rejected(lambda d:d['types']['layouts'][0]['fields'][0].update(offset='0x20000'))
    def test_current_context_cannot_claim_installation(self):
        self.rejected(lambda d:d['manifest']['snapshot_context'].update(current_main_runtime_integration='installed'))
    def test_raw_evidence_cannot_be_public(self):
        self.rejected(lambda d:d['provenance']['artifacts'][0].update(visibility='public'))
    def test_private_missing_or_changed_hash_fails(self):
        import tempfile, hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); body=b'original'; (root/'proof.json').write_bytes(body)
            (root/'games/gt3-usa-v110').mkdir(parents=True)
            (root/'games/gt3-usa-v110/core.elf').write_bytes(body)
            digest=hashlib.sha256(body).hexdigest()
            m={'original_elf_sha256':digest}
            p={'artifacts':[{'id':'fixture','path':'proof.json','sha256':digest}], 'evidence_ids':[]}
            with patch.object(project,'check',return_value=(m,{}, {},p)):
                project.verify_private(root)
                (root/'proof.json').write_bytes(b'changed')
                with self.assertRaises(AssertionError):project.verify_private(root)
                (root/'proof.json').unlink()
                with self.assertRaises(AssertionError):project.verify_private(root)
if __name__ == '__main__':unittest.main()
