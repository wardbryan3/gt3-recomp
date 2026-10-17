#!/usr/bin/env python3
"""Explicit original-generation and two-product assembly; no gameplay substitutions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ELF_SHA = "b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763"


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(args):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True)


def generated_files(path):
    return {p.name: sha(p) for p in sorted(path.iterdir())
            if p.is_file() and p.suffix in {'.cpp', '.hpp'}}


def audit_graph(build):
    reply = build / '.cmake/api/v1/reply'
    index = json.loads(sorted(reply.glob('index-*.json'))[-1].read_text())
    model = json.loads((reply / index['reply']['codemodel-v2']['jsonFile']).read_text())
    configs = model['configurations']; assert len(configs) == 1
    targets = {x['id']: json.loads((reply / x['jsonFile']).read_text()) for x in configs[0]['targets']}
    roots = {x['name']: x['id'] for x in configs[0]['targets']}
    reports = {}
    for name in ['ps2run', 'gt3-native']:
        pending = [roots[name]]; closure = set(); sources = set()
        while pending:
            key = pending.pop()
            if key in closure: continue
            closure.add(key); target = targets[key]
            sources.update(x['path'] for x in target.get('sources', []))
            pending.extend(x['id'] for x in target.get('dependencies', []))
        names = sorted(targets[key]['name'] for key in closure)
        owner = 'ps2_native_host' if name == 'ps2run' else 'gt3_native_host'
        required = {name, owner, 'ps2game', 'ps2runtime'}
        allowed = required | {'ps2_profile_host', 'ps2_window_host'}
        assert required <= set(names) <= allowed, names
        host = targets[roots[owner]]
        defines = [d['define'] for group in host.get('compileGroups', []) for d in group.get('defines', [])]
        assert ('GT3_HOST_PRESENTATION=1' in defines) == (name == 'gt3-native'), defines
        assert not any('src/gt3/' in s or 'extensions/' in s for s in sources), 'unapproved source linkage'
        reports[name] = {'targets': names, 'sources': sorted(sources)}
    return reports


def assemble(name, iso, receipt=None):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
        raise ValueError('portable lowercase product name required')
    iso = iso.resolve(strict=True)
    game = ROOT / 'games' / name; generated = ROOT / 'generated' / name
    build = ROOT / 'build' / ('native-' + name)
    assert sha(game / 'core.elf') == ELF_SHA, 'wrong original executable profile'
    # Independently regenerate into fresh output and require exact file identity.
    receipt = receipt or name
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', receipt):
        raise ValueError('invalid receipt name')
    check = ROOT / 'local/restructuring/generation-checks' / receipt
    check.mkdir(parents=True, exist_ok=False)
    run([ROOT / 'build/tools/eerecomp', game / 'core.elf', '--entries', game / 'entries.txt', '--out', check])
    if list((game / 'vu1').glob('*.bin')):
        run([ROOT / 'build/tools/vurecomp', game / 'vu1', check])
    observed = generated_files(generated)
    assert observed == generated_files(check), 'stale/overlaid/extra generated input'
    units = sorted(p for p in observed if p.endswith('.cpp'))
    unit_list = check / 'original-sources.txt'; unit_list.write_text('\n'.join(units) + '\n')
    query = build / '.cmake/api/v1/query'; query.mkdir(parents=True, exist_ok=True)
    (query / 'codemodel-v2').touch()
    run(['cmake', '-S', ROOT, '-B', build, '-G', 'Ninja', '-DCMAKE_BUILD_TYPE=Release',
         '-DCMAKE_CXX_COMPILER=clang++', '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
         '-DBUILD_TESTING=ON', '-DGT3_ORIGINAL_ELF=' + str(game / 'core.elf'),
         '-DPS2_GENERATED=' + str(generated), '-DPS2_UNIT_LIST=' + str(unit_list)])
    run(['cmake', '--build', build, '--target', 'ps2run', 'gt3-native', '--parallel', '6'])
    graph = audit_graph(build)
    paths = [ROOT / 'CMakeLists.txt', ROOT / 'scripts/project/products.py', *sorted((ROOT / 'cmake').glob('*.cmake'))]
    for folder in ['runtime', 'host', 'recomp']:
        paths += [p for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in {'.cpp', '.hpp', '.wgsl'}]
    identity = {'schema_version': 1, 'kind': 'original-generated-products',
                'products': {p: {'path': str(build / p), 'sha256': sha(build / p)} for p in graph},
                'original_elf': {'path': str(game / 'core.elf'), 'sha256': ELF_SHA},
                'iso': {'path': str(iso), 'sha256': sha(iso)},
                'entries_sha256': sha(game / 'entries.txt'),
                'vu_discovery': {p.name: sha(p) for p in sorted((game / 'vu1').glob('*.bin'))},
                'generated_path': str(generated), 'generated': observed,
                'explicit_source_list': {'path': str(unit_list), 'sha256': sha(unit_list)},
                'generator_hashes': {str(p): sha(p) for p in [ROOT / 'build/tools/eerecomp', ROOT / 'build/tools/vurecomp']},
                'source_hashes': {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))},
                'graph': graph, 'compile_commands_sha256': sha(build / 'compile_commands.json'),
                'link_maps': {p: sha(build / (p + '.map')) for p in graph},
                'recovery_integration': False, 'enhancement_integration': False,
                'compiler': subprocess.check_output(['clang++', '--version'], text=True)}
    with (check / 'products.json').open('x') as stream:
        json.dump(identity, stream, indent=2); stream.write('\n')
    print('Products assembled and linkage audited:', check / 'products.json')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for cmd in ['generate', 'assemble']:
        c = sub.add_parser(cmd); c.add_argument('iso', type=Path); c.add_argument('name'); c.add_argument('--receipt')
    args = p.parse_args()
    if args.command == 'generate':
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', args.name): p.error('invalid name')
        for folder in [ROOT / 'games' / args.name, ROOT / 'generated' / args.name, ROOT / 'build' / ('native-' + args.name)]:
            if folder.exists(): p.error('output exists; choose a NEW name: ' + str(folder))
        run([ROOT / 'scripts/port.sh', args.name, args.iso.resolve(strict=True), '--native-only', '--frames', '5101', '--rounds', '8'])
    assemble(args.name, args.iso, args.receipt)


if __name__ == '__main__':
    try: main()
    except (AssertionError, OSError, ValueError) as exc:
        print('Product assembly FAILED:', exc, file=sys.stderr); sys.exit(1)
