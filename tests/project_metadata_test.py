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
        self.data = {name:project.load(name) for name in ('manifest','symbols','types','provenance','current-validation','pedal-validation','pedal-profiles','pedal-admission-49af40','pedal-closure')}
    def rejected(self, mutation):
        data=copy.deepcopy(self.data);mutation(data)
        with patch.object(project,'load',side_effect=lambda name:data[name]):
            with self.assertRaises(AssertionError):project.check()
    def test_current(self): project.check()
    def test_closure_cannot_count_fallback_as_replacement(self):
        self.rejected(lambda d:d['pedal-closure']['results'].update(live_fallbacks=299))
    def test_closure_cannot_change_semantics_or_boundary(self):
        self.rejected(lambda d:d['pedal-closure'].update(semantics_changed=True))
        self.rejected(lambda d:d['pedal-closure'].update(resume_address='0x001e4c60'))
    def test_closure_requires_current_source_identity(self):
        self.rejected(lambda d:d['pedal-closure']['source_hashes'].update({'host/gt3_clean_pedals.cpp':'0'*64}))
    def test_closure_cannot_expand_absolute_allowlist(self):
        self.rejected(lambda d:d['pedal-closure']['admission'].update(absolute_command_allowlist=True))
    def test_closure_registry_required(self):
        self.rejected(lambda d:d['provenance'].update(pedal_closure_registry='invented.json'))
    def test_stopped_profiles_cannot_claim_success(self):
        self.rejected(lambda d:d['pedal-profiles'].update(status='passing'))
    def test_stopped_profiles_cannot_erase_fallback(self):
        self.rejected(lambda d:d['pedal-profiles']['results'].update(stop_case_fallbacks=0))
    def test_stopped_profiles_provenance_link_required(self):
        self.rejected(lambda d:d['provenance'].update(pedal_profile_characterization_registry='invented.json'))
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
    def test_current_live_requires_current_prerequisites(self):
        def mutate(d):
            v=d['current-validation'];v.update(live='passing',build='blocked')
        self.rejected(mutate)
    def test_current_passing_requires_pinned_artifacts(self):
        self.rejected(lambda d:d['current-validation'].update(build='passing',artifacts=[]))
    def test_current_fixture_cannot_be_v2(self):
        self.rejected(lambda d:d['current-validation']['fixture'].update(version=2))
    def test_current_harness_cannot_claim_canonical_installation(self):
        self.rejected(lambda d:d['current-validation'].update(runtime_installation='installed'))
    def test_current_artifact_path_cannot_escape_repository(self):
        self.rejected(lambda d:d['current-validation']['artifacts'].append(
            {'id':'bad','path':'../private','sha256':'a'*64,'visibility':'private'}))
    def test_pedal_cannot_claim_canonical_installation(self):
        self.rejected(lambda d:d['pedal-validation'].update(runtime_installation='installed'))
    def test_pedal_build_and_runtime_must_default_off(self):
        for key in ('build_default','runtime_default'):
            self.rejected(lambda d:d['pedal-validation'].update({key:True}))
    def test_pedal_cannot_widen_boundary(self):
        self.rejected(lambda d:d['pedal-validation'].update(resume_address='0x001e4c60'))
    def test_pedal_live_requires_exact_abi_and_budget(self):
        for key in ('complete_cpu','exact_dynamic_budget','exact_defined_cpu_traces'):
            self.rejected(lambda d:d['pedal-validation']['results'].update({key:False}))
    def test_pedal_requires_unchanged_pinned_source(self):
        self.rejected(lambda d:d['pedal-validation']['source_hashes'].update({'host/gt3_clean_pedals.cpp':'0'*64}))
    def test_pedal_frozen_requires_full_regressions(self):
        self.rejected(lambda d:d['pedal-validation'].update(lifecycle='frozen',regressions='blocked'))
    def test_pedal_frozen_requires_final_checkpoint(self):
        self.rejected(lambda d:d['pedal-validation']['frozen_evaluation'].update(status='pending'))
    def test_pedal_requires_pinned_private_artifacts(self):
        self.rejected(lambda d:d['pedal-validation'].update(artifacts=[]))
    def test_pedal_fixture_cannot_be_v2(self):
        self.rejected(lambda d:d['pedal-validation']['fixture'].update(version=2))
    def test_pedal_artifacts_cannot_escape_or_be_public(self):
        for mutation in ({'path':'../outside'},{'visibility':'public'}):
            self.rejected(lambda d:d['pedal-validation']['artifacts'][0].update(mutation))
    def test_current_tree_member_change_or_removal_fails(self):
        import tempfile, hashlib, json
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'local').mkdir(); member=root/'local/trace.jsonl'
            member.write_bytes(b'proof')
            tree=root/'local/files.json'
            tree.write_text(json.dumps({'files':[{'path':'local/trace.jsonl',
                'sha256':hashlib.sha256(b'proof').hexdigest()}]}))
            v={'artifacts':[{'id':'tree','path':'local/files.json','kind':'file-manifest',
                            'sha256':hashlib.sha256(tree.read_bytes()).hexdigest()}]}
            with patch.object(project,'check_current',return_value=v):
                project.verify_current(root)
                member.write_bytes(b'changed')
                with self.assertRaises(AssertionError):project.verify_current(root)
                member.unlink()
                with self.assertRaises(AssertionError):project.verify_current(root)
    def test_current_private_rejects_v2_even_with_matching_hash(self):
        import tempfile, hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'local').mkdir(); path=root/'local/race.state'
            body=b'PS2STATE'+(2).to_bytes(4,'little');path.write_bytes(body)
            v={'fixture':{'status':'passing','artifact':'fixture'},'artifacts':[
                {'id':'fixture','path':'local/race.state','sha256':hashlib.sha256(body).hexdigest()}]}
            with patch.object(project,'check_current',return_value=v):
                with self.assertRaises(AssertionError):project.verify_current(root)
    def test_current_private_missing_or_changed_hash_fails(self):
        import tempfile, hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'local').mkdir(); path=root/'local/proof.json'
            path.write_bytes(b'original')
            v={'artifacts':[{'id':'fixture','path':'local/proof.json',
                             'sha256':hashlib.sha256(b'original').hexdigest()}]}
            with patch.object(project,'check_current',return_value=v):
                project.verify_current(root)
                path.write_bytes(b'changed')
                with self.assertRaises(AssertionError):project.verify_current(root)
                path.unlink()
                with self.assertRaises(AssertionError):project.verify_current(root)
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
