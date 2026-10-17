#!/usr/bin/env python3
"""Explicit private verification of the separate current checkpoint approval.
Public checks validate declared identities; THIS command requires every report.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import project
from products import ROOT, sha
import checkpoint
import source_fixtures


def item(record):
    path = Path(record['path'])
    if not path.is_absolute(): path = ROOT / path
    assert sha(path) == record['sha256'], 'missing/changed required context: ' + str(path)
    return path


def process(record):
    assert record['exit'] == 0, 'recorded process failed'
    log = item(record['log']); assert log.stat().st_size, 'empty required process evidence'
    return log


def verify_generic(path, kind):
    data = json.loads(path.read_text())
    assert data['kind'] == kind and data['status'] == 'passed-bounded'
    assert data['dependencies'] == project.source_files(), 'STALE current checkpoint dependency closure'
    item(data['recipe'])
    if kind == 'public-development-gates':
        assert [r['argv'] for r in data['commands']] == [['just', 'check'], ['just', 'test'], ['just', 'docs-build']]
        for record in data['commands']: process(record)
    else:
        assert kind == 'fresh-public-source-iso-build'
        assert data['isolation']['historical_workspace_available'] is False
        assert data['isolation']['old_generated_inputs_available'] is False
        assert data['isolation']['legal_iso_only'] is True
        item(data['public_source_snapshot'])
        receipt_path = item(data['product_receipt']); receipt = checkpoint.product_identity(receipt_path)
        assert [r['argv'] for r in data['public_checks']] == [['just', 'check'], ['just', 'test']]
        for record in data['public_checks']: process(record)
        process(data['build'])
        assert set(data['runs']) == {'ps2run', 'gt3-native'}
        for name, record in data['runs'].items():
            log = process(record)
            assert 'frame limit reached' in log.read_text()
            assert record['binary_sha256'] == receipt['products'][name]['sha256']
            assert record['argv'][0] == receipt['products'][name]['path']
            assert '--load-state' not in record['argv'], 'fresh-clone run must boot, not import an old fixture'
            assert item(record['memory']).stat().st_size == 36 * 1024 * 1024
            assert record['captures'], 'fresh boot produced no captures'
            for capture in record['captures']: item(capture)
    return data


def verify():
    checkpoint.no_history(); project.check()
    proofs = {r['id']: r for r in project.load('proofs')['records']}
    approvals = [r for r in project.load('approvals')['records'] if r['status'] == 'approved-bounded']
    assert len(approvals) == 1, 'requires one current bounded original-only approval'
    for identity in approvals[0]['proofs']:
        proof = proofs[identity]
        path = item({'path': proof['report'], 'sha256': proof['report_sha256']})
        if proof['kind'] == 'current-original-product-matrix': checkpoint.verify(path)
        elif proof['kind'] == 'current-original-source-fixtures': source_fixtures.verify(path)
        else: verify_generic(path, proof['kind'])
    print('Current bounded original-product approval verified; no recovered/enhanced integration or hardware/headless/full-game claim')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.parse_args()
    try: verify()
    except (AssertionError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print('Current approval verification FAILED:', exc, file=sys.stderr); sys.exit(1)
