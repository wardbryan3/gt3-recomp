#!/usr/bin/env python3
"""Handbrake-only native-v3 validation; native buttons only, no injected commands."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic(rows):
    return [{k: v for k, v in r.items() if k != 'transport_pc'} for r in rows]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['build', 'out', 'elf', 'iso']:
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    build, elf, iso = (v.resolve(strict=True) for v in [a.build, a.elf, a.iso])
    out = a.out.resolve(); out.mkdir(parents=True, exist_ok=False)
    identity = json.loads((build / 'identity.json').read_text())
    assert identity['build_opt_in'] and not identity['runtime_default'] and not identity['canonical_gate']
    for name, expected in identity['files'].items():
        assert sha(build / name) == expected, name
    for name, expected in identity['sources'].items():
        assert sha(root / name) == expected, name
    parent = Path(identity['parent_build'])
    assert sha(parent / 'pedal-build-identity.json') == identity['parent_identity_sha256']
    authority = json.loads((root / 'decomp/gt3/current-validation.json').read_text())
    fixture = next(v for v in authority['artifacts'] if v['id'] == authority['fixture']['artifact'])
    snapshot = root / fixture['path']
    assert sha(snapshot) == fixture['sha256']
    with snapshot.open('rb') as f:
        assert f.read(12) == b'PS2STATE' + struct.pack('<I', 3)
    assert sha(elf) == json.loads((root / 'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
    canonical = parent / 'base/original/ps2run'; clock = parent / 'base/fixed-clock.so'
    base = json.loads((parent / 'base/build-identity.json').read_text())
    for f in [canonical, clock, elf]:
        assert base['inputs_and_executables'][str(f)] == sha(f)
    canonical_pin = next(v for v in authority['artifacts'] if v['id'] == 'artifact:current-canonical-executable')
    assert sha(canonical) == canonical_pin['sha256']
    env = {k: v for k, v in os.environ.items() if not k.startswith('PS2_')}
    env.update(PS2_ONE_THREAD='1', SDL_AUDIODRIVER='dummy', LD_PRELOAD=str(clock),
               GT3_BASELINE_UTC_EPOCH=str(authority['fixture']['clock_utc_epoch']))
    off, on = build / 'handbrake-off', build / 'handbrake-on'
    rejected = subprocess.run([str(off), '--gt3-clean-handbrake'], env=env, cwd=root, capture_output=True, text=True)
    (out / 'gate-rejection.log').write_text(rejected.stdout + rejected.stderr)
    assert rejected.returncode == 2 and 'build gate is OFF' in rejected.stderr
    common = [str(elf), '--disc', str(iso), '--ntsc', '--render-scale', '1', '--render-scale-y', '1',
              '--output-size', '1280x240', '--frame-every', '100', '--load-state', str(snapshot), '--frames', '5101']
    result = {'source_commit': identity['source_commit'], 'fixture_sha256': sha(snapshot),
              'elf_sha256': sha(elf), 'iso_sha256': sha(iso), 'canonical_sha256': sha(canonical),
              'build_identity_sha256': sha(build / 'identity.json'), 'validator_sha256': sha(Path(__file__)),
              'scope': 'handbrake only; native input; original downstream; validation-only', 'cases': {}}

    def run(tag, inputs, binary=on, trace=True):
        d = out / tag; d.mkdir(); (d / 'shots').mkdir()
        argv = [str(binary), *common, '--memcard', str(d / 'card.ps2'), '--frames-dir', str(d / 'shots'), *inputs]
        if trace:
            argv += ['--gt3-handbrake-trace', str(d / 'handbrake.jsonl'), '--gt3-wheel-trace', str(d / 'steering.jsonl')]
        with (d / 'run.log').open('w') as log:
            subprocess.run(argv, cwd=root, env=dict(env, PS2_DUMP=str(d / 'memory.bin')),
                           stdout=log, stderr=log, timeout=240, check=True)
        text = (d / 'run.log').read_text(); assert 'frame limit reached' in text
        item = {'argv': argv, 'memory_sha256': sha(d / 'memory.bin'),
                'captures': {f.name: sha(f) for f in sorted((d / 'shots').glob('*.ppm'))}}
        assert item['captures']
        if binary != canonical:
            m = re.search(r'\[gt3-handbrake\] replaced=(\d+) fallback=(\d+)', text); assert m
            item['replaced'], item['fallback'] = map(int, m.groups())
        rows = [json.loads(line) for line in (d / 'handbrake.jsonl').read_text().splitlines()] if trace else []
        if trace:
            item['stages'] = {hex(k): v for k, v in Counter(r['pc'] for r in rows).items()}
            entries = [r for r in rows if r['pc'] == 0x1e4bb8]
            item['observed_inputs'] = sorted({(r['flags'] & 16, r['input']) for r in entries})
            assert item['stages'].get('0x1e4bb8', 0) == item['stages'].get('0x1e4c60', 0) > 0
        result['cases'][tag] = item
        return rows

    def equal(left, right, rows=None, other=None):
        l, r = (result['cases'][v] for v in [left, right])
        assert l['memory_sha256'] == r['memory_sha256'], (left, right, 'full dump')
        assert l['captures'] == r['captures'], (left, right, 'captures')
        if rows is not None:
            assert semantic(rows) == semantic(other), (left, right, 'CPU/state/budget')
            assert (out / left / 'steering.jsonl').read_bytes() == (out / right / 'steering.jsonl').read_bytes()
        l.setdefault('exact_matches', []).append(right)

    buttons = ['--press', '4802:cross+circle:100', '--press', '4952:square:100']
    run('canonical', buttons, canonical, False)
    for tag, binary in [('build_off_disabled', off), ('runtime_disabled', on)]:
        run(tag, buttons, binary, False); equal(tag, 'canonical')
    trace = run('trace_only', buttons); equal('trace_only', 'canonical')
    off_trace = run('build_off_trace', buttons, off); equal('build_off_trace', 'trace_only', off_trace, trace)
    scenarios = [('neutral', []), ('handbrake_hold', ['--press', '4802:circle:200']),
                 ('accel_handbrake_release', buttons),
                 ('brake_handbrake', ['--press', '4802:square+circle:200']),
                 ('turn_shift', ['--press', '4802:cross+left+circle:100', '--press', '4902:r2+circle:50', '--press', '5002:l2:50']),
                 ('wheel_compatibility', [*buttons, '--gt3-wheel', '.5', '--gt3-clean-steering'])]
    for name, inputs in scenarios:
        original = run('generated_' + name, inputs)
        clean = run('clean_' + name, [*inputs, '--gt3-clean-handbrake'])
        repeat = run('repeat_' + name, inputs)
        equal('clean_' + name, 'generated_' + name, clean, original)
        equal('repeat_' + name, 'generated_' + name, repeat, original)
        n = result['cases']['clean_' + name]
        assert n['replaced'] == sum(r['pc'] == 0x1e4bb8 for r in clean) > 0 and n['fallback'] == 0
        for pc in [0x1e4c74, 0x1e6ec8, 0x1e6fc8, 0x1e7500]:
            assert any(r['pc'] == pc for r in original), hex(pc)
        if name not in ['neutral', 'turn_shift']:
            assert any(r['input'] for r in original if r['pc'] == 0x1e4bb8), 'handbrake not reached'
        print(name, 'exact CPU/state/budget + full dump + captures + steering + repeat PASS', flush=True)
    for tag, n in result['cases'].items():
        if not tag.startswith('clean_') and tag != 'canonical':
            assert n['replaced'] == n['fallback'] == 0
    assert sha(snapshot) == fixture['sha256']
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Handbrake bounded native-v3 validation PASS')


if __name__ == '__main__':
    main()
