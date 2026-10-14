#!/usr/bin/env python3
"""Fresh normal-boot v3 race capture and isolated current-source live equivalence.
All output paths must be new. Never accepts/imports a previous snapshot. No RAM
patches, old runtime executables, or physical-device input are used.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recapture_padding_differences(a, b, layout):
    """Exact comparison of all defined bytes; only compiled host ABI holes vary."""
    assert len(a) == len(b), 'state sizes differ'
    assert layout == {'thread_size': 768, 'padding': [[60,64],[72,80]]}, 'unsupported compiled host layout'
    tag = b'eekern\0\0'
    assert a.count(tag) == b.count(tag) == 1, 'ambiguous kernel section'
    at = a.index(tag)
    assert b.index(tag) == at
    count = struct.unpack_from('<I', a, at+8)[0]
    assert count == struct.unpack_from('<I', b, at+8)[0] and 0 < count <= 256
    assert at+12+count*(4+layout['thread_size']) <= len(a), 'truncated kernel thread map'
    padding = set()
    for i in range(count):
        start = at+16+i*(4+layout['thread_size'])
        for lo, hi in layout['padding']:
            padding.update(range(start+lo, start+hi))
    differences = [i for i, (x,y) in enumerate(zip(a,b)) if x != y]
    assert set(differences) <= padding, 'defined serialized state differs between normal boots'
    return differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--elf', type=Path, required=True)
    parser.add_argument('--iso', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    build, elf, iso = (p.resolve(strict=True) for p in (args.build, args.elf, args.iso))
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    expected = json.loads((root/'decomp/gt3/manifest.json').read_text())['original_elf_sha256']
    assert digest(elf) == expected, 'wrong original profile'
    canonical = build/'original/ps2run'
    observed = build/'observed/gt3_baseline_host'
    identity = build/'build-identity.json'
    assert identity.is_file(), 'missing fresh build identity'
    pinned = json.loads(identity.read_text())['inputs_and_executables']
    clock = build/'fixed-clock.so'
    for p in (canonical, observed, elf, clock, build/'state-layout', build/'state-layout.json'):
        assert pinned[str(p)] == digest(p), f'changed build input: {p}'
    env = dict(os.environ, PS2_ONE_THREAD='1', SDL_AUDIODRIVER='dummy')
    # Remove ambient experiment settings; explicit rendering and inputs below.
    for key in list(env):
        if key.startswith('PS2_') and key != 'PS2_ONE_THREAD':
            del env[key]
    # Pin the external CD/DVD wall-clock input, not the monotonic runtime clock.
    # Required for independent normal boots to use identical original RNG/date inputs.
    epoch = '1791964800'  # 2026-10-14 08:00:00 UTC
    env.update(LD_PRELOAD=str(clock), GT3_BASELINE_UTC_EPOCH=epoch)
    summary = {'scope': 'current-main fresh builds; isolated validation harness only',
               'clock_epoch': epoch, 'clock_shim_sha256': digest(clock),
               'validator_sha256': digest(Path(__file__)),
               'build_script_sha256': digest(root/'scripts/build_gt3_baseline.sh'),
               'build_identity_sha256': digest(identity), 'elf_sha256': digest(elf),
               'iso_sha256': digest(iso), 'canonical_sha256': digest(canonical),
               'observed_sha256': digest(observed), 'cases': {}}
    base = [str(elf), '--disc', str(iso), '--ntsc', '--render-scale', '1',
            '--render-scale-y', '1', '--output-size', '1280x240', '--frame-every', '100']
    boot_inputs = ['--press', '300:start']
    for frame in range(600, 4501, 300):
        boot_inputs += ['--press', f'{frame}:cross']

    def run(tag, extra, binary=observed, trace=True, timeout=240):
        directory = out/tag
        directory.mkdir()
        (directory/'shots').mkdir()
        command = [str(binary), *base, '--memcard', str(directory/'card.ps2'),
                   '--frames-dir', str(directory/'shots'), *extra]
        if trace:
            command += ['--gt3-wheel-trace', str(directory/'trace.jsonl')]
        with (directory/'run.log').open('w') as log:
            subprocess.run(command, cwd=root,
                           env=dict(env, PS2_DUMP=str(directory/'memory.bin')),
                           stdout=log, stderr=log, timeout=timeout, check=True)
        text = (directory/'run.log').read_text()
        assert 'frame limit reached' in text, (tag, text[-1000:])
        captures = {p.name: digest(p) for p in sorted((directory/'shots').glob('*.ppm'))}
        assert captures, f'{tag}: no captures'
        item = {'argv': command, 'memory_sha256': digest(directory/'memory.bin'),
                'captures': captures}
        if binary == observed:
            match = re.search(r'\[gt3-clean\] normalized=(\d+) wheel_commands=(\d+) filters=(\d+) envelopes=(\d+)', text)
            assert match, tag
            item['clean_calls'] = dict(zip(['normalized','wheel_commands','filters','envelopes'],
                                          map(int, match.groups())))
        summary['cases'][tag] = item
        return [json.loads(s) for s in (directory/'trace.jsonl').read_text().splitlines()] if trace else []

    # The fixture is made only by normal main's --save-state, after boot/menu input.
    # A second independent normal boot must reproduce all guest state and every
    # defined serialized field. Raw host-struct padding is separately accounted
    # for from compiled current-source layout; neither state file is rewritten.
    for tag in ('capture', 'recapture'):
        state = out/tag/'race-start-v3.state'
        run(tag, [*boot_inputs, '--frames', '4802', '--save-state', f'4801:{state}'],
            binary=canonical, trace=False)
        with state.open('rb') as stream:
            assert stream.read(8) == b'PS2STATE'
            assert struct.unpack('<I', stream.read(4))[0] == 3
        assert '[state] saved frame 4801' in (out/tag/'run.log').read_text()
    snapshot = out/'capture/race-start-v3.state'
    recapture = out/'recapture/race-start-v3.state'
    a, b = snapshot.read_bytes(), recapture.read_bytes()
    layout = json.loads(subprocess.check_output([str(build/'state-layout')], text=True))
    assert layout == json.loads((build/'state-layout.json').read_text())
    differences = recapture_padding_differences(a, b, layout)
    assert summary['cases']['capture']['memory_sha256'] == summary['cases']['recapture']['memory_sha256'], 'complete normal boot guest dumps differ'
    assert summary['cases']['capture']['captures'] == summary['cases']['recapture']['captures'], 'normal boot captures differ'
    summary['fixture'] = {'path': str(snapshot), 'sha256': digest(snapshot), 'version': 3,
                          'saved_frame': 4801, 'normal_boot_recapture_exact': not differences,
                          'recapture_sha256': digest(recapture),
                          'defined_serialized_state_exact': True,
                          'complete_guest_dump_recapture_exact': True,
                          'host_padding_difference_offsets': differences,
                          'boot_inputs': boot_inputs}
    continuation = ['--load-state', str(snapshot), '--frames', '5001']
    # The saved vblank already sampled input for frame 4801. Schedule future
    # input at 4802 so snapshot and uninterrupted scenarios are equivalent.
    pad = ['--press', '4802:cross+left:1000']
    run('canonical_pad', [*continuation, *pad], binary=canonical, trace=False)
    run('canonical_replay', [*continuation, *pad], binary=canonical, trace=False)
    run('uninterrupted_pad', [*boot_inputs, '--frames', '5001', *pad],
        binary=canonical, trace=False)
    resumed = summary['cases']['canonical_pad']
    uninterrupted = summary['cases']['uninterrupted_pad']
    assert resumed['memory_sha256'] == uninterrupted['memory_sha256'], 'snapshot continuation differs from uninterrupted boot'
    assert all(uninterrupted['captures'].get(name) == sha for name, sha in resumed['captures'].items()), 'snapshot continuation captures differ from uninterrupted boot'
    summary['fixture']['uninterrupted_continuation_exact'] = True

    def equal(a, b, trace=False):
        left, right = summary['cases'][a], summary['cases'][b]
        assert left['captures'] == right['captures'], f'{a}/{b}: captures differ'
        assert left['memory_sha256'] == right['memory_sha256'], f'{a}/{b}: complete EE/IOP/SPU dump differs'
        if trace:
            assert (out/a/'trace.jsonl').read_bytes() == (out/b/'trace.jsonl').read_bytes(), f'{a}/{b}: trace differs'
        left.setdefault('exact_matches', []).append(b)

    equal('canonical_replay', 'canonical_pad')
    for tag, trace in [('disabled', False), ('trace_only', True)]:
        rows = run(tag, [*continuation, *pad], trace=trace)
        equal(tag, 'canonical_pad')
        assert not any(summary['cases'][tag]['clean_calls'].values()), tag
        if trace:
            assert not any(r['stage'] == 'mode4' for r in rows)
            assert any(r['stage'] == 'process' and r['mode'] in (2, 3) for r in rows)
            assert any(r['stage'] == 'angles' and abs(r['steering']) > 0 for r in rows)
    run('clean_pad', [*continuation, *pad, '--gt3-clean-steering'])
    equal('clean_pad', 'trace_only', trace=True)
    assert all(summary['cases']['clean_pad']['clean_calls'].values()), 'pad did not exercise all clean gates'

    def check(rows, value=None):
        stages = ['input', 'command', 'process', 'mode4', 'steering', 'consume', 'angles']
        counts = {s: sum(r['stage'] == s for r in rows) for s in stages}
        assert all(counts.values()), counts
        assert counts['consume'] == 4*counts['angles'], counts
        assert counts['mode4'] == counts['steering'] == counts['angles'], counts
        errors = [r['error'] for r in rows if r['stage'] in ['steering','consume','angles']]
        assert max(errors) <= 2e-6, max(errors)
        axes = {-1:1023, -.5:740, -.25:626, 0:512, .25:398, .5:284, 1:0}
        for r in rows:
            if r['stage'] in ['command','process','mode4','steering']:
                assert r['mode'] == 4 and r['flags'] & 1, r
                assert r['axis'] == axes[r['host']], r
                assert r['q'] == max(-4096,min(4096,(512-r['axis'])*9)), r
            if r['stage'] == 'steering':
                assert abs(r['steering']-r['expected']) <= 2e-6, r
                if value is not None:
                    assert r['host'] == value, r
                    assert (r['steering']*value > 0) if value else r['steering'] == 0, r
        return {'counts': counts, 'max_reconstruction_error': max(errors)}

    cases = [(f'axis_{value}', ['--gt3-wheel', str(value)], value)
             for value in [-1,-.5,-.25,0,.25,.5,1]]
    cases += [('transition', ['--gt3-wheel','.5','--gt3-wheel-at','4881:0',
                              '--gt3-wheel-at','4941:-.5'], None)]
    for sign in (1,-1):
        cases.append((f'moving_{sign}', ['--frames','5701','--gt3-wheel','0',
                                        '--gt3-wheel-at',f'5600:{sign*.5}'], None))
    for name, extra, value in cases:
        scenario = [*continuation, '--press', '4802:cross:2000', *extra]
        generated = run('generated_'+name, scenario)
        clean = run('clean_'+name, [*scenario, '--gt3-clean-steering'])
        for tag, rows in [('generated_'+name, generated), ('clean_'+name, clean)]:
            summary['cases'][tag].update(check(rows, value))
            if name == 'transition':
                for r in rows:
                    if r['stage'] == 'steering':
                        v = .5 if r['frame'] < 4881 else 0 if r['frame'] < 4941 else -.5
                        assert r['host'] == v and ((r['steering']*v > 0) if v else r['steering'] == 0), r
            if name.startswith('moving_'):
                sign = int(name.split('_')[1])
                assert next(r for r in reversed(rows) if r['stage'] == 'angles')['steering']*sign > 0
        equal('clean_'+name, 'generated_'+name, trace=True)
        calls = summary['cases']['clean_'+name]['clean_calls']
        assert calls['wheel_commands'] > 0 and calls['envelopes'] > 0
        assert not any(summary['cases']['generated_'+name]['clean_calls'].values())
        print(name, 'generated/clean traces, captures and complete dump PASS', flush=True)
    assert digest(snapshot) == summary['fixture']['sha256'], 'fixture changed'
    summary['evidence_note'] = ('clean seam rows are bridge observations, not skipped EE execution; '
                                'downstream original consumer probes execute; all comparison tolerances unchanged')
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print('Fresh v3 fixture, canonical replay, disabled/trace-only, pad and wheel live equivalence PASS')


if __name__ == '__main__':
    main()
