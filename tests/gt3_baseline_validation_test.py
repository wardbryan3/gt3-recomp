"""Synthetic tests of read-only native snapshot comparison; no game required."""
import importlib.util
from pathlib import Path
import struct
import unittest

spec = importlib.util.spec_from_file_location(
    'baseline', Path(__file__).resolve().parents[1]/'scripts/validate_gt3_baseline.py')
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
LAYOUT = {'thread_size': 768, 'padding': [[60,64],[72,80]]}


def fixture():
    return b'eekern\0\0' + struct.pack('<I',2) + b''.join(
        struct.pack('<I',i+1) + bytes(768) for i in range(2)) + b'end\0\0\0\0\0'


class SnapshotComparisonTests(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(baseline.recapture_padding_differences(fixture(),fixture(),LAYOUT), [])
    def test_only_proven_padding_allowed(self):
        a=fixture(); b=bytearray(a)
        allowed=[16+i*772+j for i in range(2) for lo,hi in LAYOUT['padding'] for j in range(lo,hi)]
        for i in allowed: b[i]=255
        self.assertEqual(baseline.recapture_padding_differences(a,b,LAYOUT), allowed)
    def test_every_nonpadding_byte_rejected(self):
        a=fixture()
        allowed={16+i*772+j for i in range(2) for lo,hi in LAYOUT['padding'] for j in range(lo,hi)}
        for at in range(len(a)):
            if at in allowed: continue
            b=bytearray(a); b[at]=255
            with self.subTest(at=at), self.assertRaises(AssertionError):
                baseline.recapture_padding_differences(a,b,LAYOUT)
    def test_non_thread_difference_rejected(self):
        a=fixture(); b=bytearray(a); b[-1]=1
        with self.assertRaises(AssertionError): baseline.recapture_padding_differences(a,b,LAYOUT)
    def test_wrong_size_or_missing_tag_rejected(self):
        for a,b in [(fixture(),fixture()[:-1]), (bytes(100),bytes(100))]:
            with self.assertRaises(AssertionError): baseline.recapture_padding_differences(a,b,LAYOUT)
    def test_unsupported_layout_rejected(self):
        with self.assertRaises(AssertionError):
            baseline.recapture_padding_differences(fixture(),fixture(),{'thread_size':768,'padding':[[0,768]]})
    def test_truncated_thread_map_rejected(self):
        a=fixture()[:30]
        with self.assertRaises(AssertionError): baseline.recapture_padding_differences(a,a,LAYOUT)


if __name__ == '__main__': unittest.main()
