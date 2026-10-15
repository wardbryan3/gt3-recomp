#!/usr/bin/env python3
"""Handbrake authority: public consistency vs explicit strict private proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / 'decomp/gt3/handbrake.json'
ELF = 'b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763'
SCENARIOS = ['neutral', 'handbrake_hold', 'accel_handbrake_release', 'brake_handbrake', 'turn_shift', 'wheel_compatibility']
STAGES = [0x1e4bb8, 0x1e4c60, 0x1e4c74, 0x1e3a90, 0x1e3aac, 0x1e3ab8, 0x1e6ec8, 0x1e6fc8, 0x1e7500]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_record(v, root=ROOT):
    assert v['schema_version'] == 1 and v['id'] == 'clean-handbrake-v1'
    assert v['original_elf_sha256'] == ELF
    assert v['lifecycle'] in ['live-validated', 'frozen']
    assert v['boundary'] == ['0x001e4bb8', '0x001e4c5f'] and v['resume'] == '0x001e4c60'
    assert v['parent_function'] == '0x001e4478'
    assert v['runtime'] == {'scope': 'validation-only', 'build_default': False, 'runtime_default': False, 'canonical_installation': False, 'fallback': 'generated'}
    assert v['coverage']['join_cases'] == 2228224 and v['coverage']['transitions'] == 20000
    assert v['coverage']['wrapper_cases'] == 4752 and v['coverage']['live_runs'] == 23
    assert v['coverage']['live_substitutions'] == 1800 and v['coverage']['live_fallbacks'] == 0
    assert v['coverage']['live_inputs'] == ['analog-zero', 'analog-full']
    assert v['coverage']['digital_live_proven'] is False
    assert v['unknowns'] and v['stop'] is True
    record = next(f for f in json.loads((root / 'decomp/gt3/manifest.json').read_text())['functions'] if f['id'] == 'clean:process_handbrake')
    assert record['lifecycle'] == v['lifecycle'] and record['handbrake_authority'] == v['id']
    assert record['boundary'] == v['boundary'] and record['resume_address'] == v['resume']
    assert record['runtime']['scope'] == 'validation-only' and record['runtime']['default'] == 'generated'
    for group in ['sources', 'protected']:
        assert v[group]
        for p, expected in v[group].items():
            assert not Path(p).is_absolute() and '..' not in Path(p).parts
            assert sha(root / p) == expected, ('source/protected drift', p)
    for a in v['artifacts']:
        assert a['path'].startswith('local/') and re.fullmatch('[0-9a-f]{64}', a['sha256'])
    required = {f'local/handbrake-v1/{name}-files.json' for name in ['final-build', 'default-off-build', 'accepted-live', 'regressions', 'failed-attempt', 'checkpoint']}
    assert required <= {a['path'] for a in v['artifacts'] if a['kind'] == 'file-manifest'}
    if v['lifecycle'] == 'frozen':
        assert v['gates'] and all(s == 'passing' for s in v['gates'].values())
        assert v['frozen_evaluation']['status'] == 'passing' and v['frozen_evaluation']['stop'] is True
    return v


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def semantic(rows):
    return [{k: v for k, v in r.items() if k != 'transport_pc'} for r in rows]


def review_rows(rows, expected=300):
    counts = Counter(r['pc'] for r in rows)
    assert all(counts[pc] == expected for pc in STAGES), counts
    entries = [r for r in rows if r['pc'] == 0x1e4bb8]
    joins = [r for r in rows if r['pc'] == 0x1e4c60]
    assert [r['frame'] for r in entries] == [r['frame'] for r in joins]
    assert len({r['frame'] for r in entries}) == expected
    assert all(r['flags'] & 16 and r['input'] in [0, 4096] for r in entries)
    assert all(r['processed'] == (0x3f800000 if e['input'] else 0) for e, r in zip(entries, joins))
    for row in rows:
        assert len(row['wheel_brake']) == 4 and re.fullmatch('[0-9a-f]+', row['cpu'])
        # Defined trace layout: 32 GPRs, HI, LO, SA, semantic PC, budget, base.
        assert int(row['cpu'][1096:1104], 16) == row['pc']
        if row['pc'] == 0x1e3aac:
            a2 = int(row['cpu'][6 * 32:6 * 32 + 8], 16)
            # Original shift-interface comparison is processed < stock .1.
            assert a2 == (1 if row['processed'] == 0 else 0)
    return counts


def verify(root, inherited=True):
    v = check_record(json.loads(DB.read_text()))
    root = Path(root).resolve(strict=True)
    count = 0
    def file(a):
        p = Path(a['path'])
        assert not p.is_absolute() and '..' not in p.parts and p.parts[0] == 'local'
        p = root / p
        assert p.is_file() and sha(p) == a['sha256'], ('MISSING/CHANGED handbrake evidence', a['path'])
        return p
    for a in v['artifacts']:
        p = file(a)
        if a.get('kind') == 'file-manifest':
            members = json.loads(p.read_text())['files']
            assert members and len({m['path'] for m in members}) == len(members)
            for m in members:
                file(m); count += 1
    base = root / 'local/handbrake-v1'
    build = base / 'final-build'
    identity = json.loads((build / 'identity.json').read_text())
    assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
    for p, h in identity['files'].items():
        assert sha(build / p) == h
    for p, h in identity['sources'].items():
        assert sha(ROOT / p) == h
    parent = root / Path(identity['parent_build']).relative_to(ROOT)
    assert sha(parent / 'pedal-build-identity.json') == identity['parent_identity_sha256']
    old = json.loads((parent / 'base/build-identity.json').read_text())
    for p, h in old['source_hashes'].items():
        if Path(p).suffix in ('.cpp', '.hpp'):
            assert sha(ROOT / p) == h, p
    off = base / 'default-off-build'
    assert not json.loads((off / 'identity.json').read_text())['build_opt_in']
    assert not (off / 'handbrake-on').exists()
    assert 'build gate is OFF' in (base / 'default-off-rejection.log').read_text()
    oracle = (base / 'final-oracle.log').read_text()
    assert 'exact join PASS cases=2228224' in oracle and 'budget=14..21' in oracle
    assert 'stateful transitions PASS cases=20000' in oracle
    assert 'mutation-free fallbacks PASS cases=16' in oracle
    assert 'cases=4752 full-CPU+32MiB-comparisons=4752 rear-only-effects=38016' in (base / 'final-wrapper.log').read_text()
    live = base / 'accepted-live'; summary = json.loads((live / 'summary.json').read_text())
    assert len(summary['cases']) == 23 and summary['elf_sha256'] == ELF
    assert summary['build_identity_sha256'] == sha(build / 'identity.json')
    assert summary['validator_sha256'] == sha(ROOT / 'scripts/validate_gt3_handbrake.py')
    canonical_hash = 'b22b692a3bf8dbcce7c3defb57605a96b8763efae10685cc7a082e1d77410d4a'
    assert summary['canonical_sha256'] == sha(parent / 'base/original/ps2run') == canonical_hash
    for name, item in summary['cases'].items():
        d = live / name
        assert sha(d / 'memory.bin') == item['memory_sha256']
        assert {p.name: sha(p) for p in (d / 'shots').glob('*.ppm')} == item['captures'] and item['captures']
        argv = item['argv']
        for flag, expected in [('--load-state', summary['fixture_sha256']), ('--disc', summary['iso_sha256'])]:
            p = root / Path(argv[argv.index(flag) + 1]).relative_to(ROOT)
            assert sha(p) == expected
        snapshot = root / Path(argv[argv.index('--load-state') + 1]).relative_to(ROOT)
        with snapshot.open('rb') as f:
            assert f.read(12) == b'PS2STATE' + struct.pack('<I', 3)
        assert sha(root / Path(argv[0]).relative_to(ROOT)) == sha(parent / 'base/original/ps2run' if name == 'canonical' else build / ('handbrake-off' if name.startswith('build_off') else 'handbrake-on'))
        assert Path(argv[1]).name == 'core.elf' and sha(root / Path(argv[1]).relative_to(ROOT)) == ELF
        if name != 'canonical':
            m = re.search(r'\[gt3-handbrake\] replaced=(\d+) fallback=(\d+) depth_boundary=(\d+)', (d / 'run.log').read_text()); assert m
            replaced, fallback, depth = map(int, m.groups())
            assert (replaced, fallback) == (item['replaced'], item['fallback'])
            assert replaced == (300 if name.startswith('clean_') else 0) and fallback == depth == 0
        if (d / 'handbrake.jsonl').exists():
            review_rows(read_rows(d / 'handbrake.jsonl'))
        for other in item.get('exact_matches', []):
            e = live / other
            assert sha(d / 'memory.bin') == sha(e / 'memory.bin')
            assert item['captures'] == summary['cases'][other]['captures']
            if (d / 'handbrake.jsonl').exists() and (e / 'handbrake.jsonl').exists():
                assert semantic(read_rows(d / 'handbrake.jsonl')) == semantic(read_rows(e / 'handbrake.jsonl'))
                assert (d / 'steering.jsonl').read_bytes() == (e / 'steering.jsonl').read_bytes()
    for name in SCENARIOS:
        for tag in ['clean_', 'repeat_']:
            assert 'generated_' + name in summary['cases'][tag + name]['exact_matches']
    records = json.loads((base / 'static-final.json').read_text())['records']
    assert len(records) == 18 and {r['evidence_id'] for r in records} == set(v['static_evidence_ids'])
    assert all(r['subject']['digest']['sha256'] == ELF for r in records)
    assert 'All current native baseline regressions PASS' in (base / 'regressions/regressions.log').read_text()
    evaluation = json.loads((base / 'frozen-evaluation.json').read_text())
    assert evaluation['status'] == 'passing' and evaluation['stop'] is True
    assert evaluation['implementation_sources'] == {p: v['sources'][p] for p in ['host/gt3_clean_handbrake.cpp', 'host/gt3_clean_handbrake.hpp']}
    if inherited:
        subprocess.run(['just', 'verify-virtual-pedals', str(root)], cwd=ROOT, check=True)
    print(f'Handbrake strict proof PASS: {count} pinned members; 2228224 exact cases, 4752 original downstream cases, 23 native-v3 runs / 1800 substitutions / zero fallback; bounded, not physical proof')


def docs():
    v = check_record(json.loads(DB.read_text()))
    (ROOT / 'docs/site/static/knowledge/handbrake.json').write_bytes(DB.read_bytes())
    text = '---\ntitle: Handbrake v1 authority\n---\n\n<!-- Generated from decomp/gt3/handbrake.json. -->\n\n'
    text += f"Lifecycle: **{v['lifecycle']}**, bounded validation-only. Build/runtime default OFF. Canonical gameplay is generated-only.\n\n"
    text += '| Gate | Result |\n|---|---|\n' + ''.join(f'| {k} | {s} |\n' for k, s in v['gates'].items())
    text += '\nOnly 001E4BB8–001E4C5F is substituted, resume001E4C60. See [semantics, proof and limits](../handbrake-v1.md).\n\nStrict private proof: `just --justfile handbrake.just verify-handbrake EXPLICIT_REPOSITORY_ROOT`.\n'
    (ROOT / 'docs/site/docs/registry/handbrake.md').write_text(text)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['check', 'docs', 'verify'])
    p.add_argument('root', nargs='?', type=Path)
    a = p.parse_args()
    if a.command == 'check':
        check_record(json.loads(DB.read_text())); print('Handbrake public consistency PASS (not private/game proof)')
    elif a.command == 'docs':
        docs()
    else:
        if not a.root:
            p.error('explicit private repository root required')
        verify(a.root)
