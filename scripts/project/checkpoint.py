#!/usr/bin/env python3
"""Current two-product bounded matrix, separate from historical validation.

All required inputs are explicit and fail closed. NEW output directories only.
No recovery/extension installation, input rewriting, or expectation updates.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from products import ROOT, sha, generated_files, audit_graph
import matrix

RECIPE_AT_LOAD = sha(Path(__file__))
SUPPORT_SOURCES = ['validation/gt3/live/gt3_baseline_clock.cpp', 'validation/gt3/live/gt3_baseline_layout.cpp',
                   'project/gt3/matrix-contract.json']


def no_history():
    assert not os.environ.get('GT3_HISTORY_ROOT'), 'current proof cannot run in a historical source view'


def read(path): return json.loads(path.read_text())


def write_new(path, data):
    with path.open('x') as stream: json.dump(data, stream, indent=2); stream.write('\n')


def product_identity(path):
    no_history(); receipt = read(path)
    assert receipt['kind'] == 'original-generated-products'
    assert not receipt['recovery_integration'] and not receipt['enhancement_integration']
    for relative, digest in receipt['source_hashes'].items():
        assert sha(ROOT / relative) == digest, 'stale build source/dependency: ' + relative
    for name in ['ps2run', 'gt3-native']:
        p = receipt['products'][name]
        assert sha(Path(p['path'])) == p['sha256'], 'changed executable: ' + name
    for key in ['original_elf', 'iso', 'explicit_source_list']:
        item = receipt[key]; assert sha(Path(item['path'])) == item['sha256'], 'changed input: ' + key
    game = Path(receipt['original_elf']['path']).parent
    assert sha(game / 'entries.txt') == receipt['entries_sha256'], 'changed entry discovery'
    assert {p.name: sha(p) for p in sorted((game / 'vu1').glob('*.bin'))} == receipt['vu_discovery'], 'changed/missing VU discovery'
    assert len(receipt['generator_hashes']) == 2
    for tool, digest in receipt['generator_hashes'].items(): assert sha(Path(tool)) == digest, 'changed/missing generator tool'
    assert generated_files(Path(receipt['generated_path'])) == receipt['generated'], 'generated input drift'
    build = Path(receipt['products']['ps2run']['path']).parent
    assert audit_graph(build) == receipt['graph'], 'stale product graph'
    assert sha(build / 'compile_commands.json') == receipt['compile_commands_sha256']
    for name, digest in receipt['link_maps'].items(): assert sha(build / (name + '.map')) == digest
    return receipt


def padding_differences(a, b, layout):
    # EXACT same bounded ABI rule as the retained original normal-boot checker.
    # Never applied to guest dumps, captures, or ordinary live continuation state.
    # Explicit independent fixture recaptures require the protected-original control.
    assert len(a) == len(b), 'state sizes differ'
    assert layout == {'thread_size': 768, 'padding': [[60, 64], [72, 80]]}, 'unsupported compiled host layout'
    tag = b'eekern\0\0'
    assert a.count(tag) == b.count(tag) == 1, 'ambiguous kernel section'
    at = a.index(tag); assert b.index(tag) == at
    count = struct.unpack_from('<I', a, at + 8)[0]
    assert count == struct.unpack_from('<I', b, at + 8)[0] and 0 < count <= 256
    assert at + 12 + count * (4 + layout['thread_size']) <= len(a), 'truncated thread map'
    padding = set()
    for i in range(count):
        start = at + 16 + i * (4 + layout['thread_size'])
        for lo, hi in layout['padding']: padding.update(range(start + lo, start + hi))
    differences = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    assert set(differences) <= padding, 'defined serialized state differs between normal boots'
    return differences


def rewrite_argv(template, receipt, name, output):
    argv = list(template); argv[0] = receipt['products'][name]['path']; argv[1] = receipt['original_elf']['path']
    for flag, value in [('--disc', receipt['iso']['path']), ('--memcard', str(output / 'card.ps2')),
                        ('--frames-dir', str(output / 'shots'))]:
        # Preserve an original NO-card command as NO-card, not a new input flag.
        if flag == '--memcard' and flag not in argv: continue
        assert flag in argv, 'unqualified command layout: missing ' + flag
        argv[argv.index(flag) + 1] = value
    if '--save-state' in argv:
        pos = argv.index('--save-state') + 1; frame, old = argv[pos].split(':', 1)
        argv[pos] = frame + ':' + str(output / Path(old).name)
    return argv


def execute(row, name, receipt, output, clock, layout):
    output.mkdir(parents=True, exist_ok=False); (output / 'shots').mkdir()
    source = Path(row['directory'])
    for name_in, digest in row['inputs'].items(): assert sha(Path(name_in)) == digest, 'changed fixture'
    for relative, digest in row['expected'].items(): assert sha(source / relative) == digest, 'changed original expectation'
    argv = rewrite_argv(row['argv'], receipt, name, output)
    assert sha(Path(argv[0])) == receipt['products'][name]['sha256']
    # Same existing external CD/DVD clock-input contract, process-local only.
    # No monotonic runtime clocks, simulation timing, or guest state are changed.
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PS2_', 'GT3_')) and k != 'LD_PRELOAD'}
    env.update(PS2_ONE_THREAD='1', SDL_AUDIODRIVER='dummy', LD_PRELOAD=str(clock),
               GT3_BASELINE_UTC_EPOCH='1791964800', PS2_DUMP=str(output / 'memory.bin'))
    write_new(output / 'command.json', {'argv': argv, 'product': name,
              'product_sha256': receipt['products'][name]['sha256'],
              'template': {'source': row['source'], 'key': row['key']},
              'clock_sha256': sha(clock), 'inputs': row['inputs']})
    with (output / 'run.log').open('x') as log:
        result = subprocess.run(argv, cwd=ROOT, env=env, stdout=log, stderr=log, timeout=600)
    write_new(output / 'result.json', {'exit': result.returncode})
    assert result.returncode == 0 and 'frame limit reached' in (output / 'run.log').read_text(), 'native process failure: ' + str(output)
    assert not (output / 'card.ps2').exists(), 'unexpected card write'
    actual_captures = {p.relative_to(output).as_posix() for p in (output / 'shots').glob('*.ppm')}
    assert actual_captures == {p for p in row['expected'] if p.startswith('shots/')}, 'capture set changed'
    observed = {}; padding = {}
    for relative, expected in row['expected'].items():
        actual = sha(output / relative); observed[relative] = actual
        if actual != expected:
            assert relative.endswith('.state') and row['state_contract'] == 'defined-ABI-fixture-recapture', 'exact native mismatch: ' + str(output / relative)
            padding[relative] = padding_differences((source / relative).read_bytes(), (output / relative).read_bytes(), layout)
    comparison = {'product': name, 'template': row['source'], 'key': row['key'],
                  'files': observed, 'fixture_recapture_host_padding_only': padding, 'status': 'pass'}
    write_new(output / 'comparison.json', comparison)
    print(name, row['source'], row['key'], 'exact guest/capture PASS', flush=True)
    return {'directory': str(output), 'comparison_sha256': sha(output / 'comparison.json'),
            'process_records': {p: sha(output / p) for p in ['command.json', 'result.json', 'run.log']}}


def run(receipt_path, catalogue_path, output, pilot=False):
    assert sha(Path(__file__)) == RECIPE_AT_LOAD, 'verifier changed after process load'
    output.relative_to(ROOT / 'local/restructuring')
    support = {p: sha(ROOT / p) for p in SUPPORT_SOURCES}
    matrix_recipe = sha(ROOT / 'scripts/project/matrix.py')
    receipt = product_identity(receipt_path); catalogue = read(catalogue_path)
    assert catalogue == matrix.catalogue(), 'stale/partial/changed retained matrix catalogue'
    output.mkdir(parents=True, exist_ok=False)
    build = Path(receipt['products']['ps2run']['path']).parent
    subprocess.run(['cmake', '--build', str(build), '--target', 'gt3_fixture_clock', 'gt3_state_layout', '--parallel', '6'], check=True)
    clock = build / 'fixed-clock.so'; assert clock.is_file()
    layout = json.loads(subprocess.check_output([str(build / 'gt3_state_layout')], text=True))
    assert layout == {'thread_size': 768, 'padding': [[60, 64], [72, 80]]}
    rows = [r for r in catalogue['rows'] if r['kind'] == 'original-product']
    if pilot: rows = rows[:1]
    jobs = [(r, name, receipt, output / f'{i:03d}-{name}', clock, layout)
            for i, r in enumerate(rows) for name in ['ps2run', 'gt3-native']]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda args: execute(*args), jobs))
    assert sha(Path(__file__)) == RECIPE_AT_LOAD, 'verifier changed during qualification'
    assert support == {p: sha(ROOT / p) for p in SUPPORT_SOURCES}, 'support source changed during qualification'
    assert matrix_recipe == sha(ROOT / 'scripts/project/matrix.py'), 'matrix recipe changed during qualification'
    report = {'support_sources': support, 'schema_version': 1, 'kind': 'current-original-product-matrix', 'complete': not pilot,
              'scope': catalogue['scope'], 'recipe_sha256': sha(Path(__file__)),
              'matrix_recipe_sha256': sha(ROOT / 'scripts/project/matrix.py'),
              'product_receipt': {'path': str(receipt_path), 'sha256': sha(receipt_path)},
              'catalogue': {'path': str(catalogue_path), 'sha256': sha(catalogue_path)},
              'clock': {'path': str(clock), 'sha256': sha(clock)}, 'layout': layout,
              'retained_row_kinds': dict(Counter(r['kind'] for r in catalogue['rows'])),
              'current_runs': results, 'runtime_promotion': False,
              'limitations': ['bounded original product rows only', 'other validation-host/extension rows are HISTORICAL, not fresh product proof',
                             'no all-game/hardware/headless/modernization/enhancement integration claim']}
    write_new(output / 'report.json', report)
    verify(output / 'report.json', allow_pilot=pilot)


def verify(path, allow_pilot=False):
    no_history(); report = read(path)
    assert report['kind'] == 'current-original-product-matrix'
    assert report['complete'] or allow_pilot, 'pilot is not checkpoint acceptance'
    assert report['recipe_sha256'] == sha(Path(__file__)), 'stale verifier dependency'
    assert report['matrix_recipe_sha256'] == sha(ROOT / 'scripts/project/matrix.py'), 'stale matrix dependency'
    assert set(report['support_sources']) == set(SUPPORT_SOURCES)
    for relative, digest in report['support_sources'].items(): assert sha(ROOT / relative) == digest, 'stale validation support'
    for key in ['product_receipt', 'catalogue', 'clock']:
        item = report[key]; assert sha(Path(item['path'])) == item['sha256'], 'missing/changed required proof: ' + key
    product_identity(Path(report['product_receipt']['path']))
    catalogue = read(Path(report['catalogue']['path'])); assert catalogue == matrix.catalogue()
    required = sum(r['kind'] == 'original-product' for r in catalogue['rows']) * 2
    assert len(report['current_runs']) == (2 if allow_pilot else required), 'incomplete retained default matrix'
    rows = [r for r in catalogue['rows'] if r['kind'] == 'original-product']
    if allow_pilot: rows = rows[:1]
    ordered = [(r, product) for r in rows for product in ['ps2run', 'gt3-native']]
    assert len({r['directory'] for r in report['current_runs']}) == len(ordered), 'duplicate purported executions'
    for record, (row, product) in zip(report['current_runs'], ordered):
        directory = Path(record['directory'])
        assert set(record['process_records']) == {'command.json', 'result.json', 'run.log'}
        for relative, digest in record['process_records'].items(): assert sha(directory / relative) == digest
        assert sha(directory / 'comparison.json') == record['comparison_sha256']
        comparison = read(directory / 'comparison.json'); assert comparison['status'] == 'pass'
        assert (comparison['template'], comparison['key'], comparison['product']) == (row['source'], row['key'], product), 'scope/order mismatch'
        assert set(comparison['files']) == set(row['expected']), 'missing required comparisons'
        assert read(directory / 'result.json')['exit'] == 0
        assert 'frame limit reached' in (directory / 'run.log').read_text()
        for relative, digest in comparison['files'].items():
            assert sha(directory / relative) == digest
            if digest != row['expected'][relative]:
                assert relative.endswith('.state') and row['state_contract'] == 'defined-ABI-fixture-recapture'
                differences = padding_differences((Path(row['directory']) / relative).read_bytes(), (directory / relative).read_bytes(), report['layout'])
                assert differences == comparison['fixture_recapture_host_padding_only'][relative]
            else:
                assert relative not in comparison['fixture_recapture_host_padding_only']
    print('Current original product matrix PASS:', len(report['current_runs']), 'fresh runs;',
          'PILOT ONLY' if allow_pilot else 'no recovery/enhancement integration approval', flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest='command', required=True)
    for name in ['run', 'pilot']:
        q = sub.add_parser(name); q.add_argument('receipt', type=Path); q.add_argument('catalogue', type=Path); q.add_argument('output', type=Path)
    q = sub.add_parser('verify'); q.add_argument('report', type=Path)
    args = p.parse_args()
    if args.command == 'verify': verify(args.report.resolve(strict=True))
    else: run(args.receipt.resolve(strict=True), args.catalogue.resolve(strict=True), args.output.resolve(), args.command == 'pilot')


if __name__ == '__main__':
    try: main()
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print('Current checkpoint FAILED:', exc, file=sys.stderr); sys.exit(1)
