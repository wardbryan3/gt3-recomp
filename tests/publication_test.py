"""Synthetic publication tests; no real game/analysis/credential data."""
import importlib.util
import json
import io
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('guard',Path(__file__).resolve().parents[1]/'scripts/audit_public.py')
guard=importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
class PublicationTests(unittest.TestCase):
    def run_guard(self,value):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'facts.json').write_text(json.dumps(value))
            with patch.object(guard,'ROOT',root),patch.object(guard,'git',side_effect=[b'',b'facts.json\0']), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                return guard.main()
    def test_private_reference_allowed(self):
        self.assertEqual(self.run_guard({'evidence':['private:id'], 'note':'pseudocode stays private'}),0)
    def test_nested_provider_body_rejected(self):
        self.assertEqual(self.run_guard({'items':[{'pseudocode':'synthetic placeholder'}]}),1)
if __name__=='__main__':unittest.main()
