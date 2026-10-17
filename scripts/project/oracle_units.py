#!/usr/bin/env python3
"""Private generated-original fixture units. No recovered code enters the oracle.
Only names and explicit test entry/join checkpoints change; originals stay intact.
"""
import argparse
from pathlib import Path


def renamed(source, name):
    result = source.replace('void unit_0039(', 'void ' + name + '(').replace(
        'unit_0039(c,', name + '(c,').replace('entries_0039', name + '_entries')
    assert result.replace(name + '_entries', 'entries_0039').replace(name, 'unit_0039') == source
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('original', type=Path); p.add_argument('output', type=Path)
    args = p.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    original = args.original.read_text()
    for name in ['oracle_unit_0039', 'state_oracle_unit_0039']:
        (args.output / (name + '.cpp')).write_text(renamed(original, name))
    # Existing validation-only entry gates and read-only probes, NOT products.
    overlay = '#include "gt3_clean_pedals.hpp"\n#include "gt3_clean_handbrake.hpp"\n' + original
    begin = overlay.index('L_001E6FB4:\n'); end = overlay.index('L_001E6FE0:\n', begin)
    part = overlay[begin:end]
    key = '    c.r[31].d[0] = ld64((c.r[29].w[0] + 48u));\n    c.r[18].d[0]'
    assert part.count(key) == 1
    overlay = overlay[:begin] + part.replace(key, 'L_001E6FC8:\n' + key) + overlay[end:]
    for address in ['001E48FC', '001E4BA8', '001E4BB8', '001E4C60', '001E4C74', '001E6EC8', '001E6FC8', '001E7500']:
        key = 'L_' + address + ':\n'; assert overlay.count(key) == 1
        extra = '    ps2::probe(c,0x' + address + 'u);\n'
        if address == '001E48FC':
            extra += '#if GT3_PEDAL_VALIDATION_GATES\n    if(gt3::pedals::replace(c,depth))goto L_001E4BA8;\n#endif\n'
        if address == '001E4BB8':
            extra += '#if GT3_HANDBRAKE_VALIDATION_GATES\n    if(gt3::handbrake::replace(c,depth))goto L_001E4C60;\n#endif\n'
        overlay = overlay.replace(key, key + extra)
    (args.output / 'adapter_fixture_unit.cpp').write_text(overlay)
    for name, flag, entry, join in [('pedal', 'gt3_pedal_audit_stop', '001E48FC', '001E4BA8'),
                                     ('handbrake', 'gt3_handbrake_audit_stop', '001E4BB8', '001E4C60')]:
        text = 'extern bool ' + flag + ';\n' + original
        key = 'switch (entry) {'; assert text.count(key) == 1
        text = text.replace(key, key + '\n    case 60000u: goto L_' + entry + ';')
        label = 'L_' + join + ':\n'; assert text.count(label) == 1
        text = text.replace(label, label + '    if (' + flag + ') {c.pc=0x' + join + 'u;return;}\n')
        (args.output / (name + '_original_unit.cpp')).write_text(text)


if __name__ == '__main__': main()
