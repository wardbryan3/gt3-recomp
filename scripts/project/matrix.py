#!/usr/bin/env python3
"""Catalogue every retained accepted live row; never treat enhanced rows as defaults.

Original product rows are re-executed unmodified apart from executable, identical
ISO/ELF input locations and NEW output locations. Other rows remain explicitly
historical validation-host/extension evidence, NOT fresh product acceptance.
"""
import hashlib
import json
from pathlib import Path
from products import ROOT, sha

CANONICAL = 'b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a'
# These rejected controls are retained by broader historical manifests but were
# explicitly NOT accepted by their original validators. Never relax captures.
REJECTED = {
    'local/virtual-pedals-v1/live-attempt-1/canonical/command.json': 'first harness attempt omitted capture directories; separately rerun accepted',
    'local/transmission-recovery-v1/live-attempt-2/at-control-original/command.json': 'excluded 100-update AT control had no scheduled capture; accepted 300-update run is separate',
    'local/transmission-recovery-v1/live/cycle-original/command.json': 'initial excluded controls preceding corrected guarded integration',
}
# Explicit accepted authorities; failed-attempt collections are not positive proof.
MANIFESTS = {
    'current-validation': ['artifact:current-live-files'],
    'pedal-validation': ['artifact:pedal-live-files'],
    'pedal-profiles': ['artifact:profiles-files'],
    'pedal-closure': ['artifact:closure-native-files'],
    'virtual-pedals': ['artifact:virtual-pedals-primary-files'],
    'handbrake': ['local/handbrake-v1/accepted-live-files.json'],
    'virtual-handbrake': ['local/virtual-handbrake-v1/accepted-live-files.json'],
    'transmission': ['local/transmission-recovery-v1/manifest.json'],
    'transmission-speed': None, 'transmission-state': None, 'virtual-transmission': None,
}


def authority_manifests():
    found = {}
    for authority, selections in MANIFESTS.items():
        record = json.loads((ROOT / 'project/gt3' / (authority + '.json')).read_text())
        if selections is None:
            refs = [{'path': record['private']['manifest'], 'sha256': record['private']['sha256']}]
        else:
            refs = [next(a for a in record['artifacts'] if a.get('id', a['path']) == selection)
                    for selection in selections]
        for item in refs:
            path = ROOT / item['path']; assert sha(path) == item['sha256'], 'changed required manifest: ' + str(path)
            found[item['path']] = item['sha256']
    return found


def fixture_contract():
    path = ROOT / 'project/gt3/matrix-contract.json'; data = json.loads(path.read_text())
    assert data['default_state_comparison'] == 'all bytes exact'
    assert data['padding_layout'] == {'thread_size': 768, 'padding': [[60, 64], [72, 80]]}
    control = data['original_control']; manifest = ROOT / control['manifest']
    assert sha(manifest) == control['sha256'], 'missing/changed original padding-control manifest'
    for relative, digest in json.loads(manifest.read_text())['files'].items():
        assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
        assert sha(manifest.parent / relative) == digest, 'missing/changed independent ORIGINAL control'
    report = json.loads((manifest.parent / 'original-control.json').read_text())
    assert report['status'] == 'passed' and report['canonical_sha256'] == CANONICAL == control['canonical_sha256']
    assert report['full_guest_dump_and_capture_set_exact'] is True
    selectors = {(r['source'], r['key']) for r in data['recaptures']}
    assert len(selectors) == len(data['recaptures'])
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path), 'selectors': selectors}


def catalogue():
    contract = fixture_contract()
    manifests = authority_manifests(); pins = {}
    for relative in manifests:
        data = json.loads((ROOT / relative).read_text())
        for item in data['files']:
            p, digest = item['path'], item['sha256']
            assert p not in pins or pins[p] == digest, 'conflicting evidence pins: ' + p
            pins[p] = digest
    def pinned_file(path, declared=None):
        digest = sha(path)
        key = path.resolve().relative_to(ROOT).as_posix()
        expected = pins.get(key, declared)
        assert expected is not None, 'required evidence has no immutable pin: ' + key
        assert digest == expected, 'changed required evidence: ' + key
        assert declared is None or digest == declared, 'changed command-qualified fixture: ' + key
        return digest
    rows = []; seen = set()
    for relative, digest in sorted(pins.items()):
        if not relative.endswith(('/command.json', '/summary.json')):
            continue
        path = ROOT / relative
        assert sha(path) == digest, 'changed required command/summary: ' + relative
        data = json.loads(path.read_text())
        candidates = []
        if isinstance(data, dict) and 'argv' in data:
            candidates.append(('', data, path.parent))
        if isinstance(data, dict) and isinstance(data.get('cases'), dict):
            candidates += [(key, value, path.parent / key) for key, value in data['cases'].items()
                           if isinstance(value, dict) and 'argv' in value]
        for key, record, directory in candidates:
            argv = record['argv']; assert isinstance(argv, list) and all(isinstance(x, str) for x in argv)
            executable = Path(argv[0]); assert executable.is_file(), 'missing retained executed binary: ' + str(executable)
            identity = sha(executable)
            if 'binary_sha256' in record: assert identity == record['binary_sha256']
            marker = (directory.resolve(), tuple(argv))
            if marker in seen: continue  # summary + command can describe the SAME execution.
            seen.add(marker)
            result = directory / 'result.json'
            failed = relative in REJECTED or (result.is_file() and json.loads(result.read_text()).get('exit', 0) != 0)
            kind = 'retained-failure' if failed else ('original-product' if identity == CANONICAL else 'historical-validation-host')
            if kind == 'original-product':
                assert not any(x.startswith('--gt3-') for x in argv), 'non-default original row needs an explicit scope decision'
                memory = directory / 'memory.bin'
                assert memory.is_file(), 'missing full dump: ' + str(memory)
                expected = {'memory.bin': pinned_file(memory)}
                assert memory.stat().st_size == 36 * 1024 * 1024, 'incomplete EE/IOP/SPU dump'
                captures = {p.relative_to(directory).as_posix(): pinned_file(p) for p in sorted((directory / 'shots').glob('*.ppm'))}
                assert captures, 'missing retained captures: ' + str(directory)
                expected.update(captures)
                state = None
                if '--save-state' in argv:
                    state = Path(argv[argv.index('--save-state') + 1].split(':', 1)[1])
                    assert state.is_file(), 'missing retained saved state'
                    expected[state.name] = pinned_file(state)
                card = Path(argv[argv.index('--memcard') + 1]) if '--memcard' in argv else None
                assert card is None or not card.exists(), 'requires independently pinned INITIAL card, not post-run card'
                inputs = {}
                if '--load-state' in argv:
                    fixture = Path(argv[argv.index('--load-state') + 1])
                    declared = record.get('state', {}).get('sha256')
                    inputs[str(fixture)] = pinned_file(fixture, declared)
            else:
                expected = {}; inputs = {}
            rows.append({'source': relative, 'key': key, 'directory': str(directory),
                         'kind': kind, 'rejection': REJECTED.get(relative),
                         'state_contract': 'defined-ABI-fixture-recapture' if (relative, key) in contract['selectors'] else 'all-bytes-exact',
                         'argv': argv, 'binary_sha256': identity,
                         'expected': expected, 'inputs': inputs})
    assert rows and any(r['kind'] == 'original-product' for r in rows)
    return {'schema_version': 1, 'scope': 'ALL retained original-product live rows; non-product rows explicitly historical',
            'state_contract_authority': {'path': contract['path'], 'sha256': contract['sha256']},
            'authorities': manifests, 'rows': rows}


if __name__ == '__main__':
    import argparse
    from collections import Counter
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('output', type=Path); args = p.parse_args()
    args.output.resolve().relative_to(ROOT / 'local/restructuring')
    data = catalogue()
    with args.output.open('x') as stream: json.dump(data, stream, indent=2); stream.write('\n')
    print(dict(Counter(r['kind'] for r in data['rows'])))
