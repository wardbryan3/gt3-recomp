#!/usr/bin/env python3
"""One MT helper authority: public consistency != original/clean/live proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT/'decomp/gt3/transmission.json'
ELF = 'b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763'
HOME = Path('local/transmission-recovery-v1')
MODES = ['original', 'build-off', 'trace-only', 'clean', 'repeat']
GATES = {'identify_trace','exact_isolated','original_consumer_chain','actual_entry_live',
         'actual_substitution','default_off','source_regressions','docs_public_audit',
         'inherited_proof','strict_evidence'}
COUNTS = re.compile(r'MT validation entries=(\d+) exits=(\d+) shadows=(\d+) replaced=(\d+) fallback=(\d+) original_speed_calls=(\d+)')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_record(v, root=ROOT):
    assert v['schema_version'] == 1 and v['id'] == 'clean-mt-selector-v1'
    assert v['lifecycle'] in ['live-validated', 'frozen']
    assert v['boundary'] == ['0x001e5458', '0x001e553b'] and v['entry'] == '0x001e5458'
    assert v['boundary_kind'] == 'whole-function' and v['resume'] is None
    assert v['original_elf_sha256'] == ELF and v['oracle_kind'] == 'independent-generated-original'
    assert v['dependencies_generated'] == ['0x001e4e80']
    assert v['runtime'] == dict(scope='validation-only', build_default=False, runtime_default=False,
                                canonical_installation=False, fallback='generated')
    assert v['coverage'] == dict(isolated_cases=663959, full_cpu_cases=663959,
        isolated_full_ram_cases=649, wrapper_cases=1008, fallback_cases=20,
        accepted_live_runs=15, live_substitutions=2400, live_shadows=2400,
        live_full_ram_shadows=2400, live_fallbacks=0, accepted_total_updates=7500,
        live_generated_speed_calls=2, budget=[13,4103],
        all_cars_modes=False, physical_proof=False)
    assert v['source_base_commit'] == 'edc65a105ba682449391a2d62c513af8b9005e53'
    assert v['baseline_oracle_source_commit'] == '82987dec7a71d76414adfff8663da5494a280938'
    assert v['source_context'] == 'uncommitted additive source hashes over source_base_commit; not a new full retranslation'
    assert v['stop'] is True and v['unknowns'] and v['fields']
    assert v['parent_manifest_sha256']=='bdf55a7d6bad6bbde63b56a9463d8325c9142696d0c61cb5df4e79027a00d6ac'
    versions=v['historical_public_versions']
    assert {x['path'] for x in versions}=={'HANDOFF.md','docs/site/docs/transmission.md','docs/site/sidebars.js'}
    for item in versions:
        assert sha(root/item['path'])==item['current_sha256'],('new documentation drift',item['path'])
        assert item['git_source_commit']==v['source_base_commit']
        assert item['historical_artifact']==str(HOME/'historical-public'/item['path'])
        assert re.fullmatch('[a-f0-9]{64}',item['historical_sha256'])
    assert v['field_offsets'] == {'maximum_index':'0x20a','accelerator_bits':'0x13ac','selected_index':'0x13ba','inhibition':'0x13be','longitudinal_bits':'0x140c'}
    for group in ['sources','protected']:
        assert v[group]
        for name, expected in v[group].items():
            p=Path(name);assert not p.is_absolute() and '..' not in p.parts
            assert sha(root/p)==expected,('source/protected drift',name)
    assert v['artifacts'] and {a['kind'] for a in v['artifacts']} >= {'file-manifest'}
    assert v['artifacts'][0]['path']==str(HOME/'manifest.json')
    assert set(v['gates'])==GATES
    assert {'CMakeLists.txt','justfile','host/main.cpp','host/gt3_clean_handbrake.cpp',
            'decomp/gt3/handbrake.json','decomp/gt3/virtual-handbrake.json',
            'decomp/gt3/manifest.json','runtime/include/ps2/fpu.hpp'} <= set(v['protected'])
    for a in v['artifacts']:
        p=Path(a['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='local'
        assert re.fullmatch('[a-f0-9]{64}',a['sha256'])
    if v['lifecycle']=='frozen':
        assert v['gates'] and all(x=='passing' for x in v['gates'].values())
        assert any(a['path']==str(HOME/'fault-check-result.json') for a in v['artifacts'])
    return v


def review_trace(rows, expected):
    if not expected:
        assert rows == []
        return dict(entries=0, accepted=0, inhibit_entries=0, auxiliary_entries=0,
                    shifts=[], selected=[], states=[])
    assert len(rows)==2*expected
    frames=[];accepted=0;inhibited=0;auxiliary=0;shifts=set();selected=set();states=set()
    for before,after in zip(rows[::2],rows[1::2]):
        assert before['pc']==0x1e5458 and after['pc']==0x1e5730
        assert before['frame']==after['frame'] and after['budget']<before['budget']
        for r in [before,after]:
            assert r['car']==0x1fbb7bc and r['sp']==0x49af30 and r['ra']==0x1e5730
            assert r['owner']==0 and r['policy']==1 and r['mode']==0 and r['suppression']==0
        for name in ['car','sp','ra','aux','relative','selected','state','candidate_bits','accelerator_bits','speed_bits']:
            assert before[name]==after[name],('MT selector illegally committed/changed input',name)
        assert after['v0']==0xffffffff or 0<=after['v0']<=6
        accepted+=after['v0']!=0xffffffff;inhibited+=before['inhibition']!=0;auxiliary+=before['aux']!=0
        frames.append(before['frame']);shifts.add(before['relative']);selected.add(before['selected']);states.add(before['state'])
    assert frames==list(range(4501,4501+expected))
    return dict(entries=expected,accepted=accepted,inhibit_entries=inhibited,auxiliary_entries=auxiliary,
                shifts=sorted(shifts),selected=sorted(selected),states=sorted(states))


def verify_live(root):
    home=root/HOME;summary={};total_sub=total_shadow=total_speed=0
    for scenario,folder,updates in [('cycle','live-attempt-2',600),('reverse','live-attempt-2',600),('at-control','live-attempt-3-at',300)]:
        reference=home/folder/f'{scenario}-original';assert json.loads((reference/'result.json').read_text())=={'exit':0}
        captures={p.name:sha(p) for p in (reference/'shots').glob('*.ppm')};assert captures
        trace=None
        for mode in MODES:
            d=home/folder/f'{scenario}-{mode}';cmd=json.loads((d/'command.json').read_text());argv=cmd['argv']
            assert cmd['mode']==mode and cmd['input_delivery']=='original --press only'
            assert json.loads((d/'result.json').read_text())=={'exit':0}
            expected_binary=(root/'local/baseline-v3/final-build/original/ps2run' if mode=='original' else home/('live-off-attempt-2' if mode=='build-off' else 'live-on-attempt-3')/'ps2run')
            assert Path(argv[0])==expected_binary and sha(expected_binary)==cmd['binary_sha256']
            env=cmd['env'];assert env['PS2_ONE_THREAD']=='1' and env['GT3_BASELINE_UTC_EPOCH']=='1791964800'
            assert env['SDL_AUDIODRIVER']=='dummy' and Path(env['LD_PRELOAD'])==root/'local/baseline-v3/final-build/fixed-clock.so'
            donor={'cycle':'mt-cycle-observed','reverse':'mt-reverse-observed','at-control':'at-auto-observed'}[scenario]
            donor_path=root/'local/transmission-map-v1'/donor/'command.json';old=json.loads(donor_path.read_text())
            assert sha(donor_path)==cmd['source_command_sha256'] and cmd['state']==old['state']
            delivered=argv[argv.index('--save-state')+2:]
            if mode in ['clean','repeat']:assert delivered[-2:]==['--gt3-clean-transmission','--gt3-transmission-shadow'];delivered=delivered[:-2]
            assert delivered==old['argv'][old['argv'].index('--save-state')+2:]
            assert argv[argv.index('--frames')+1]=='5101'
            assert Path(argv[argv.index('--memcard')+1])==d/'card.ps2'
            assert sha(Path(cmd['state']['path']))==cmd['state']['sha256']
            assert Path(cmd['state']['path'])==Path(argv[argv.index('--load-state')+1])
            assert Path(argv[argv.index('--load-state')+1]).read_bytes()[:12]==b'PS2STATE\x03\x00\x00\x00'
            assert not ({'--ram-word','--axis','--gt3-triple'} & set(argv))
            assert ('--gt3-clean-transmission' in argv)==(mode in ['clean','repeat'])
            assert ('--gt3-transmission-shadow' in argv)==(mode in ['clean','repeat'])
            assert not (d/'card.ps2').exists()
            assert (d/'memory.bin').stat().st_size==36*1024*1024
            for name in ['memory.bin','final.state']:assert sha(d/name)==sha(reference/name),(scenario,mode,name)
            assert {p.name:sha(p) for p in (d/'shots').glob('*.ppm')}==captures
            assert 'frame limit reached' in (d/'run.log').read_text()
            if mode=='original':continue
            rows=[json.loads(x) for x in (d/'trace.jsonl').read_text().splitlines()]
            stats=review_trace(rows,0 if scenario=='at-control' else updates)
            if trace is None:trace=sha(d/'trace.jsonl');summary[scenario]=stats
            assert sha(d/'trace.jsonl')==trace
            matches=COUNTS.findall((d/'run.log').read_text());assert len(matches)==1
            entries,exits,shadows,replaced,fallback,speed=map(int,matches[0])
            assert entries==exits==(0 if scenario=='at-control' else updates) and fallback==0
            assert shadows==replaced==(entries if mode in ['clean','repeat'] else 0)
            assert speed==(1 if scenario=='reverse' and mode in ['clean','repeat'] else 0)
            total_sub+=replaced;total_shadow+=shadows;total_speed+=speed
        summary[scenario]['updates_per_run']=updates;summary[scenario]['capture_count']=len(captures)
    assert total_sub==total_shadow==2400 and total_speed==2
    return summary


def verify_parent(root,v):
    # Exact archived documentation bytes only. The raw parent verifier's rejection
    # of current docs is retained; no parent hash or runtime/evidence read changes.
    import importlib.util
    base=root/'local/transmission-deep-v1';assert sha(base/'manifest.json')==v['parent_manifest_sha256']
    manifest=json.loads((base/'manifest.json').read_text());pins={x['path']:x['sha256'] for x in manifest['files']}
    versions={}
    for item in v['historical_public_versions']:
        assert pins[item['path']]==item['historical_sha256']
        p=root/item['historical_artifact'];assert sha(p)==item['historical_sha256']
        versions[root/item['path']]=p
    spec=importlib.util.spec_from_file_location('transmission_original_parent',base/'verify.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    original_digest=parent.digest
    parent.digest=lambda p:original_digest(versions.get(p,p))
    parent.verify()
    print('Parent proof PASS with THREE explicit historical DOCUMENTATION versions; all runtime/private reads and expected pins unchanged. Raw current-document rejection remains retained.')


def verify(root):
    v=check_record(json.loads(DB.read_text()));root=Path(root).resolve(strict=True)
    def required(a):
        p=root/a['path'];assert sha(p)==a['sha256'],('changed required evidence',a['path']);return p
    count=0
    for a in v['artifacts']:
        p=required(a)
        if a['kind']=='file-manifest':
            members=json.loads(p.read_text())['files'];assert members and len({m['path'] for m in members})==len(members)
            for m in members:
                assert m['path'].startswith(str(HOME)+'/') and '..' not in Path(m['path']).parts
                required(m);count+=1
    if v['lifecycle']=='frozen':
        assert json.loads((root/HOME/'fault-check-result.json').read_text())=={'missing':'FileNotFoundError','changed':'AssertionError'}
    assert sha(root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf')==ELF
    assert sha(root/'local/game-input/gt3-usa-v1.10.iso')=='0946bb943a766d0afe057fbff5aa96132b16a797f3e3edc985a3b6d2f3afee0e'
    home=root/HOME;base=root/'local/baseline-v3/final-build'
    static=json.loads((home/'native-boundary/evidence.json').read_text())
    dossiers={r['parameters']['procedure']:r for r in static['records'] if r['operation']=='analyze_function'}
    assert set(dossiers)=={'0x001e5458','0x001e4e80','0x001e5690'}
    assert all(r['subject']['digest']['sha256']==ELF for r in dossiers.values())
    assert dossiers['0x001e5458']['normalized_result']['procedure']['body']['ranges']==[{'start':'0x1e5458','end':'0x1e553b'}]
    import importlib.util
    spec=importlib.util.spec_from_file_location('transmission_validation',ROOT/'scripts/validate_gt3_transmission.py')
    validation=importlib.util.module_from_spec(spec);spec.loader.exec_module(validation);validation.preflight(base)
    reproduction=json.loads((home/'reproducible-builds.json').read_text());assert len(reproduction)==4
    for item in reproduction:assert sha(home/item['executed'])==sha(home/item['fresh_archive_preflight_rebuild'])==item['sha256']
    identity=json.loads((base/'build-identity.json').read_text())
    for p,h in identity['inputs_and_executables'].items():assert sha(Path(p))==h,p
    for p,h in identity['generated']['original'].items():assert sha(base/'generated-original'/p)==h,p
    for name in ['live-on-attempt-3','live-off-attempt-2','build-attempt-5','final-build','final-live-on','final-live-off']:
        build=home/name;i=json.loads((build/'identity.json').read_text())
        for p,h in i['files'].items():assert sha(build/p)==h,p
        for p,h in i['sources'].items():assert sha(ROOT/p)==h,p
    assert json.loads((home/'live-on-attempt-3/gate.json').read_text())['build_gate'] is True
    assert json.loads((home/'live-off-attempt-2/gate.json').read_text())['build_gate'] is False
    assert 'build-off-clean-request-exit=2' in (home/'build-off-rejection.log').read_text()
    summary=verify_live(root)
    assert summary==json.loads((home/'live-summary.json').read_text())
    assert json.loads((home/'live/cycle-clean/result.json').read_text())=={'exit':-6}
    assert 'live shadow guard rejection' in (home/'live/cycle-clean/run.log').read_text()
    assert 'at-control' in (home/'live-attempt-2.log').read_text() and 'captures' in (home/'live-attempt-2.log').read_text()
    # Fresh independent oracle execution, not merely accepting retained PASS text.
    replay=subprocess.run([str(home/'build-attempt-5/oracle'),str(root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf')],capture_output=True,text=True,check=True)
    assert replay.stdout==(home/'oracle-attempt-5.log').read_text()
    wrapper=subprocess.run([str(home/'live-on-attempt-3/wrapper'),str(root/'local/legacy/resolution-repo/games/gt3-usa-v110/core.elf')],capture_output=True,text=True,check=True)
    assert wrapper.stdout==(home/'live-on-attempt-3/wrapper.log').read_text()
    verify_parent(root,v)
    print(f'Transmission bounded private PASS: {count} pinned members; 663959 original differentials; 1008 original wrappers; 15 accepted native runs; 2400 real-entry full-CPU+32MiB shadows and substitutions, fallback0. Not canonical/all-car/physical proof.')


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('check');q=sub.add_parser('verify');q.add_argument('root',type=Path);a=p.parse_args()
    if a.command=='check':check_record(json.loads(DB.read_text()));print('Transmission public source/authority PASS; NOT an original/live verification')
    else:verify(a.root)


if __name__=='__main__':main()
