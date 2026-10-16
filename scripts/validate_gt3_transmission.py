#!/usr/bin/env python3
"""Additive MT source checks or explicit private independent-original oracle."""
from pathlib import Path
import argparse
import hashlib
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


ARCHIVES = {
    'libps2game.a':'89c789634358b0972cc9664d103122f13414429a356285b70d8d0b2586706160',
    'libps2runtime.a':'4ec263c00c08f6e3542aca1fb2e7c651818350d7ed3020694c025d2f81d205ca',
    'libgt3_recovered.a':'f68910270bda107a4f9ff4026dcdc576fb0f851abb70c085db085d75bf2b0fe9',
}


def preflight(baseline):
    # Game/runtime match independent immutable parent proof. The unused clean
    # library is separately identified, not substituted for any original oracle.
    for name,expected in ARCHIVES.items():
        assert hashlib.sha256((baseline/'original'/name).read_bytes()).hexdigest()==expected, name


def source():
    # No original bytes, translations, SDK or generated runtime is needed.
    with tempfile.TemporaryDirectory(prefix='gt3-transmission-source-') as d:
        binary = str(Path(d) / 'source-test')
        subprocess.run(['clang++', '-std=c++20', '-O2', '-Wall', '-Wextra',
                        '-I'+str(ROOT/'host'), '-I'+str(ROOT/'runtime/include'),
                        str(ROOT/'host/gt3_clean_transmission.cpp'),
                        str(ROOT/'tests/gt3_transmission_source_test.cpp'), '-o', binary], check=True)
        subprocess.run([binary], check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('source')
    original = sub.add_parser('original')
    original.add_argument('baseline', type=Path)
    original.add_argument('new_output', type=Path)
    live = sub.add_parser('live-build')
    live.add_argument('baseline', type=Path)
    live.add_argument('isolated', type=Path)
    live.add_argument('new_output', type=Path)
    live.add_argument('--enable-clean-transmission', action='store_true')
    a = p.parse_args()
    if a.command == 'source':
        source()
    elif a.command == 'live-build':
        preflight(a.baseline.resolve(strict=True))
        args=['bash',str(ROOT/'scripts/build_gt3_transmission_live.sh'),str(a.baseline.resolve(strict=True)),str(a.isolated.resolve(strict=True)),str(a.new_output.resolve())]
        if a.enable_clean_transmission:args.append('--enable-clean-transmission')
        subprocess.run(args,check=True)
    else:
        preflight(a.baseline.resolve(strict=True))
        subprocess.run(['bash', str(ROOT/'scripts/build_gt3_transmission.sh'),
                        str(a.baseline.resolve(strict=True)), str(a.new_output.resolve())], check=True)
        # Builder refuses existing output; no overwritten proof or skipped oracle.
        with (a.new_output/'oracle.log').open('x') as log:
            subprocess.run([str(a.new_output.resolve()/'oracle'),
                            str(ROOT/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf')],
                           stdout=log, stderr=log, check=True)
        print((a.new_output/'oracle.log').read_text(), end='')


if __name__ == '__main__':
    main()
