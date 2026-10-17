#!/usr/bin/env python3
"""Renewed current-source independent original fixtures, not product promotion."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from checkpoint import product_identity, write_new, no_history
from products import ROOT, sha
import project

RECIPE_AT_LOAD = sha(Path(__file__))
RUNTIME_FLOOR = '3dcccccc'  # Retained initialized native observation, adjacent to ELF's 3dcccccd.
TARGETS = [
    'gt3_original_controls', 'gt3_original_steering_trace', 'gt3_original_steering',
    'gt3_original_synthetic_wheel', 'gt3_original_pedal_discovery', 'gt3_original_pedal_abi',
    'gt3_original_handbrake', 'gt3_original_virtual_pedals', 'gt3_original_virtual_handbrake',
    'gt3_original_transmission', 'gt3_original_speed', 'gt3_original_state',
]


def run(receipt_path, output):
    no_history(); assert sha(Path(__file__)) == RECIPE_AT_LOAD, 'fixture recipe changed after load'
    receipt = product_identity(receipt_path)
    source_identity = project.source_files()
    output.relative_to(ROOT / 'local/restructuring')
    output.mkdir(parents=True, exist_ok=False)
    build = Path(receipt['products']['ps2run']['path']).parent
    subprocess.run(['cmake', '--build', str(build), '--target', 'gt3_original_differentials', '--parallel', '6'], check=True)
    assert source_identity == project.source_files(), 'source changed during build'
    files = {}
    for name in TARGETS:
        binary = build / name; binary_hash = sha(binary)
        log = output / (name + '.log')
        with log.open('x') as stream:
            subprocess.run([str(binary), receipt['original_elf']['path']], cwd=ROOT,
                           stdout=stream, stderr=stream, timeout=1800, check=True)
        assert sha(binary) == binary_hash
        files[name] = {'binary': str(binary), 'sha256': binary_hash, 'log_sha256': sha(log)}
        print('Current original source fixture PASS:', name, flush=True)
    # Existing second, runtime-observed original floor calibration. No expected
    # result comes from recovered code; the fixture computes its original table.
    name = 'virtual_handbrake_runtime_floor'
    binary = build / 'gt3_original_virtual_handbrake'
    with (output / (name + '.log')).open('x') as stream:
        subprocess.run([str(binary), receipt['original_elf']['path'], str(output / 'original-runtime-results.jsonl'), RUNTIME_FLOOR],
                       cwd=ROOT, stdout=stream, stderr=stream, timeout=1800, check=True)
    files[name] = {'binary': str(binary), 'sha256': sha(binary), 'log_sha256': sha(output / (name + '.log'))}
    assert source_identity == project.source_files(), 'source/dependency changed during qualification'
    report = {'schema_version': 1, 'kind': 'current-original-source-fixtures', 'status': 'passed-bounded',
              'product_receipt': {'path': str(receipt_path), 'sha256': sha(receipt_path)},
              'recipe_sha256': sha(Path(__file__)), 'dependencies': source_identity, 'runs': files,
              'original_runtime_results_sha256': sha(output / 'original-runtime-results.jsonl'),
              'limitations': ['source fixtures, not recovery installed into either product',
                             'engine/commit models are semantic projections, not whole ABI recovery',
                             'current extension gates compile only; historical native ON proof stays historical']}
    write_new(output / 'report.json', report); verify(output / 'report.json')


def verify(path):
    no_history(); report = json.loads(path.read_text())
    assert report['kind'] == 'current-original-source-fixtures' and report['status'] == 'passed-bounded'
    assert report['recipe_sha256'] == sha(Path(__file__))
    assert report['dependencies'] == project.source_files(), 'STALE source fixture proof'
    receipt = report['product_receipt']; assert sha(Path(receipt['path'])) == receipt['sha256']
    product_identity(Path(receipt['path']))
    assert set(report['runs']) == set(TARGETS + ['virtual_handbrake_runtime_floor']), 'incomplete original fixtures'
    for name, record in report['runs'].items():
        assert sha(Path(record['binary'])) == record['sha256']
        log = path.parent / (name + '.log'); assert sha(log) == record['log_sha256'] and log.stat().st_size
    assert sha(path.parent / 'original-runtime-results.jsonl') == report['original_runtime_results_sha256']
    print('Current source fixtures verified: 13 original-dependent runs, no product integration approval')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('run'); q.add_argument('receipt', type=Path); q.add_argument('output', type=Path)
    q = sub.add_parser('verify'); q.add_argument('report', type=Path)
    args = p.parse_args()
    try:
        if args.command == 'verify': verify(args.report.resolve(strict=True))
        else: run(args.receipt.resolve(strict=True), args.output.resolve())
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Current original source fixtures FAILED:', exc, file=sys.stderr); sys.exit(1)
