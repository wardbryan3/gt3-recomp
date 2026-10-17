"""Current identities/approval/link-closure negatives; no historical source view or game."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/project'))
import project
import products
import checkpoint


class CurrentApproval(unittest.TestCase):
    def records(self):
        deps = {'source.cpp': '1' * 64}
        kinds = ['current-original-product-matrix', 'current-original-source-fixtures',
                 'fresh-public-source-iso-build', 'public-development-gates']
        proofs = {'records': [{'id': kind, 'kind': kind, 'status': 'passed-bounded', 'dependencies': deps,
                              'historical_only': False, 'report_sha256': '2' * 64,
                              'report': 'local/restructuring/synthetic/report.json', 'limitations': ['synthetic schema fixture']} for kind in kinds]}
        approvals = {'records': [{'id': 'synthetic', 'authorization': 'synthetic schema fixture', 'limitations': ['synthetic'],
                                 'status': 'approved-bounded', 'scope': 'original-default-products',
                                 'products': ['ps2run', 'gt3-native'], 'proofs': kinds, 'dependencies': deps}]}
        return deps, proofs, approvals

    def test_separate_current_proof_and_approval(self):
        deps, proofs, approvals = self.records()
        project.check_approvals(proofs, approvals, deps)
        self.assertEqual(approvals['records'][0]['scope'], 'original-default-products')

    def test_stale_shared_dependency_fails(self):
        deps, proofs, approvals = self.records()
        with self.assertRaisesRegex(AssertionError, 'STALE approval'):
            project.check_approvals(proofs, approvals, {**deps, 'shared.hpp': '3' * 64})

    def test_historical_proof_cannot_approve_current(self):
        deps, proofs, approvals = self.records(); proofs['records'][0]['historical_only'] = True
        with self.assertRaisesRegex(AssertionError, 'historical proof'):
            project.check_approvals(proofs, approvals, deps)

    def test_implementation_proof_is_not_product_permission(self):
        deps, proofs, approvals = self.records()
        approvals['records'][0]['scope'] = 'new-recovery'
        with self.assertRaisesRegex(AssertionError, 'cannot approve'):
            project.check_approvals(proofs, approvals, deps)

    def test_changed_proof_dependency_fails(self):
        deps, proofs, approvals = self.records(); proofs['records'][0]['dependencies'] = {}
        with self.assertRaisesRegex(AssertionError, 'STALE proof'):
            project.check_approvals(proofs, approvals, deps)

    def test_missing_required_proof_fails(self):
        deps, proofs, approvals = self.records(); proofs['records'] = []
        with self.assertRaises(KeyError): project.check_approvals(proofs, approvals, deps)

    def test_missing_native_or_fresh_build_layer_fails(self):
        deps, proofs, approvals = self.records()
        approvals['records'][0]['proofs'] = [proofs['records'][1]['id']]
        with self.assertRaisesRegex(AssertionError, 'incomplete checkpoint'):
            project.check_approvals(proofs, approvals, deps)

    def test_new_candidate_cannot_overwrite_old(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'candidate.json'; p.write_text('preserved')
            with patch.object(sys, 'argv', ['project.py', 'record-candidate', str(p)]):
                with self.assertRaises(FileExistsError): project.main()
            self.assertEqual(p.read_text(), 'preserved')


class ProductClosure(unittest.TestCase):
    def graph(self, root):
        reply = root / '.cmake/api/v1/reply'; reply.mkdir(parents=True)
        names = ['ps2run', 'gt3-native', 'ps2_native_host', 'gt3_native_host', 'ps2game', 'ps2runtime']
        targets = []
        for name in names:
            if name in ['ps2run', 'gt3-native']:
                dependencies = ['ps2_native_host' if name == 'ps2run' else 'gt3_native_host']
            elif name.endswith('_host'): dependencies = ['ps2game', 'ps2runtime']
            elif name == 'ps2game': dependencies = ['ps2runtime']
            else: dependencies = []
            record = {'name': name, 'dependencies': [{'id': n} for n in dependencies],
                      'sources': [{'path': 'runtime/original.cpp'}],
                      'compileGroups': [{'defines': [{'define': 'GT3_HOST_PRESENTATION=1'}] if name == 'gt3_native_host' else []}]}
            (reply / (name + '.json')).write_text(json.dumps(record))
            targets.append({'name': name, 'id': name, 'jsonFile': name + '.json'})
        (reply / 'model.json').write_text(json.dumps({'configurations': [{'targets': targets}]}))
        (reply / 'index-test.json').write_text(json.dumps({'reply': {'codemodel-v2': {'jsonFile': 'model.json'}}}))
        return reply

    def test_original_shared_graph_and_reference_exclusion(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.graph(root)
            self.assertEqual(set(products.audit_graph(root)), {'ps2run', 'gt3-native'})

    def test_unapproved_source_even_without_named_target_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); reply = self.graph(root); p = reply / 'ps2game.json'
            data = json.loads(p.read_text()); data['sources'].append({'path': 'src/gt3/gameplay/controls/unapproved.cpp'})
            p.write_text(json.dumps(data))
            with self.assertRaisesRegex(AssertionError, 'unapproved source'): products.audit_graph(root)

    def test_reference_presentation_definition_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); reply = self.graph(root); p = reply / 'ps2_native_host.json'
            data = json.loads(p.read_text()); data['compileGroups'][0]['defines'] = [{'define': 'GT3_HOST_PRESENTATION=1'}]
            p.write_text(json.dumps(data))
            with self.assertRaises(AssertionError): products.audit_graph(root)

    def test_unapproved_dependency_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); reply = self.graph(root); p = reply / 'ps2run.json'
            data = json.loads(p.read_text()); data['dependencies'].append({'id': 'gt3_native_host'})
            p.write_text(json.dumps(data))
            with self.assertRaises(AssertionError): products.audit_graph(root)


class CheckpointBoundaries(unittest.TestCase):
    def test_missing_receipt_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError): checkpoint.product_identity(Path(d) / 'missing.json')

    def test_historical_context_cannot_qualify_current(self):
        with patch.dict('os.environ', {'GT3_HISTORY_ROOT': '/historical'}):
            with self.assertRaisesRegex(AssertionError, 'historical source view'): checkpoint.no_history()

    def test_pilot_not_acceptance(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'report.json'; p.write_text(json.dumps({'kind': 'current-original-product-matrix', 'complete': False}))
            with self.assertRaisesRegex(AssertionError, 'pilot'): checkpoint.verify(p)

    def test_no_card_template_stays_no_card(self):
        receipt = {'products': {'ps2run': {'path': '/new/ps2run'}},
                   'original_elf': {'path': '/new/core.elf'}, 'iso': {'path': '/same/game.iso'}}
        original = ['/old/ps2run', '/old/core.elf', '--disc', '/same/game.iso', '--frames-dir', '/old/shots', '--press', '10:cross']
        observed = checkpoint.rewrite_argv(original, receipt, 'ps2run', Path('/new/output'))
        self.assertNotIn('--memcard', observed)
        self.assertEqual(observed[-2:], original[-2:])
        self.assertEqual(original[0], '/old/ps2run')
        with self.assertRaisesRegex(AssertionError, 'missing --frames-dir'):
            checkpoint.rewrite_argv(original[:4], receipt, 'ps2run', Path('/new/output'))

    def test_live_continuation_stays_raw_exact_and_fixture_defined_fields_stay_exact(self):
        import struct
        from types import SimpleNamespace
        layout = {'thread_size': 768, 'padding': [[60, 64], [72, 80]]}
        original = b'eekern\0\0' + struct.pack('<II', 1, 7) + bytes(768)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); source = root / 'source'; (source / 'shots').mkdir(parents=True)
            binary = root / 'synthetic'; binary.write_text('synthetic identity, never executed')
            clock = root / 'synthetic-clock'; clock.write_text('synthetic, never loaded')
            for name, data in [('memory.bin', b'synthetic guest memory'), ('capture.state', original), ('shots/synthetic.ppm', b'synthetic capture')]:
                (source / name).write_bytes(data)
            receipt = {'products': {'ps2run': {'path': str(binary), 'sha256': products.sha(binary)}},
                       'original_elf': {'path': 'synthetic.elf'}, 'iso': {'path': 'synthetic.iso'}}
            row = {'directory': str(source), 'inputs': {}, 'source': 'synthetic-command', 'key': '',
                   'state_contract': 'all-bytes-exact',
                   'expected': {p.relative_to(source).as_posix(): products.sha(p) for p in source.rglob('*') if p.is_file()},
                   'argv': [str(binary), 'synthetic.elf', '--disc', 'synthetic.iso', '--load-state', 'synthetic-input.state',
                            '--frames-dir', 'synthetic-shots', '--save-state', '1:synthetic/capture.state']}
            defined_change = False
            def simulate(argv, **kwargs):
                out = Path(argv[argv.index('--frames-dir') + 1]).parent
                for name in ['memory.bin', 'shots/synthetic.ppm']: (out / name).write_bytes((source / name).read_bytes())
                state = bytearray(original); state[16 + (80 if defined_change else 60)] = 1
                (out / 'capture.state').write_bytes(state)
                kwargs['stdout'].write('frame limit reached\n')
                return SimpleNamespace(returncode=0)
            with patch.object(checkpoint.subprocess, 'run', side_effect=simulate):
                with self.assertRaisesRegex(AssertionError, 'exact native mismatch'):
                    checkpoint.execute(row, 'ps2run', receipt, root / 'live', clock, layout)
                row['state_contract'] = 'defined-ABI-fixture-recapture'
                checkpoint.execute(row, 'ps2run', receipt, root / 'fixture', clock, layout)
                defined_change = True
                with self.assertRaisesRegex(AssertionError, 'defined serialized state'):
                    checkpoint.execute(row, 'ps2run', receipt, root / 'invalid-fixture', clock, layout)

    def test_only_existing_compiled_host_padding_rule(self):
        import struct
        a = b'eekern\0\0' + struct.pack('<II', 1, 7) + bytes(768)
        b = bytearray(a); b[16 + 60] = 1
        layout = {'thread_size': 768, 'padding': [[60, 64], [72, 80]]}
        self.assertEqual(checkpoint.padding_differences(a, b, layout), [76])
        b[16 + 80] = 1
        with self.assertRaisesRegex(AssertionError, 'defined serialized state'):
            checkpoint.padding_differences(a, b, layout)
        with self.assertRaisesRegex(AssertionError, 'unsupported compiled'):
            checkpoint.padding_differences(a, a, {'thread_size': 768, 'padding': [[0, 768]]})


class MechanicalSource(unittest.TestCase):
    def test_relocated_gameplay_bodies_are_unchanged(self):
        import subprocess
        mapping = project.load('migration-map')['paths']
        for old, new in mapping.items():
            if not new.startswith('src/gt3/') or Path(new).suffix not in {'.cpp', '.hpp', '.inc'}: continue
            original = subprocess.check_output(['git', 'show', project.BASE + ':' + old], cwd=ROOT).decode()
            expected = original.replace('extensions/gt3/virtual_transmission/', 'src/gt3/gameplay/transmission/virtual/').replace(
                'extensions/gt3/native_bindings/', 'src/gt3/bindings/ps2/virtual-transmission/')
            self.assertEqual((ROOT / new).read_text(), expected, new + ': nonmechanical source change')

    def test_runtime_floor_is_the_retained_observation_not_an_assumption(self):
        import source_fixtures
        import subprocess
        self.assertEqual(source_fixtures.RUNTIME_FLOOR, '3dcccccc')
        historical = subprocess.check_output(['git', 'show', project.BASE + ':docs/site/docs/virtual-handbrake.md'], cwd=ROOT).decode()
        self.assertIn('**3DCCCCCD**', historical)
        self.assertIn('**3DCCCCCC**', historical)

    def test_existing_extension_fixture_and_host_syntax_both_gates(self):
        import subprocess
        sources = sorted((ROOT / 'validation/gt3/integration/extensions').glob('*.cpp'))
        self.assertEqual(len(sources), 3)
        for gate in ['0', '1']:
            cc = ['clang++', '-std=c++20', '-fsyntax-only', '-I' + str(ROOT),
                  '-I' + str(ROOT / 'runtime/include'), '-DGT3_EXT_VIRTUAL_TRANSMISSION=' + gate]
            for source in sources: subprocess.run([*cc, str(source)], check=True, capture_output=True)
            text = '#include <cstdio>\n#include <cstdlib>\n#include <string>\n#include <utility>\n#include "src/gt3/bindings/ps2/virtual-transmission/host.inc"\n'
            subprocess.run([*cc, '-x', 'c++', '-'], input=text, text=True, check=True, capture_output=True)


class ImmutableMatrixInputs(unittest.TestCase):
    def test_changed_required_capture_is_not_repinned(self):
        import matrix
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); directory = root / 'local/native'; (directory / 'shots').mkdir(parents=True)
            executable = directory / 'ps2run'; executable.write_text('synthetic executable identity only')
            memory = directory / 'memory.bin'
            with memory.open('wb') as stream: stream.truncate(36 * 1024 * 1024)
            capture = directory / 'shots/synthetic.ppm'; capture.write_bytes(b'synthetic fixture, not a game capture')
            command = directory / 'command.json'; command.write_text(json.dumps({'argv': [str(executable), 'synthetic.elf']}))
            members = [{'path': p.relative_to(root).as_posix(), 'sha256': products.sha(p)} for p in [command, memory, capture]]
            manifest = root / 'local/pins.json'; manifest.write_text(json.dumps({'files': members}))
            with patch.object(matrix, 'ROOT', root), patch.object(matrix, 'CANONICAL', products.sha(executable)), patch.object(matrix, 'fixture_contract', return_value={'path': 'synthetic-contract', 'sha256': '0' * 64, 'selectors': set()}), patch.object(matrix, 'authority_manifests', return_value={'local/pins.json': products.sha(manifest)}):
                self.assertEqual(matrix.catalogue()['rows'][0]['kind'], 'original-product')
                capture.write_bytes(b'changed synthetic capture')
                with self.assertRaisesRegex(AssertionError, 'changed required evidence'): matrix.catalogue()
                capture.unlink()
                with self.assertRaisesRegex(AssertionError, 'missing retained captures'): matrix.catalogue()


if __name__ == '__main__': unittest.main()
