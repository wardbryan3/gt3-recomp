"""Prove the historical view is explicit/source-only and does not hide evidence drift."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

HOOK = Path(__file__).resolve().parents[1] / "scripts/historical_context"


class HistoricalContextTests(unittest.TestCase):
    def test_git_source_import_private_reads_and_write_protection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE)
            git("init", "-q")
            git("config", "user.name", "Synthetic Test")
            git("config", "user.email", "test@example.invalid")
            (root / "source.json").write_text('{"version":1}')
            (root / "module.py").write_text('version = 1\n')
            git("add", "source.json", "module.py")
            git("commit", "-qm", "synthetic immutable source")
            revision = git("rev-parse", "HEAD").decode().strip()
            (root / "source.json").unlink()
            (root / "module.py").write_text('raise RuntimeError("active implementation must not execute")\n')
            (root / "private.bin").write_bytes(b"changed evidence")
            program = '''
import json,module
from pathlib import Path
assert module.version == 1
p=Path('source.json')
assert p.is_file() and json.loads(p.read_text()) == {'version':1}
assert Path('private.bin').read_bytes() == b'changed evidence'
try: p.write_text('mutation')
except PermissionError: pass
else: raise AssertionError('historical source write allowed')
'''
            env = dict(os.environ, PYTHONPATH=str(HOOK), GT3_HISTORY_ROOT=str(root),
                       GT3_HISTORY_REVISION=revision, PYTHONDONTWRITEBYTECODE="1")
            child = subprocess.run([sys.executable, "-B", "-c", program], cwd=root,
                                   env=env, capture_output=True, text=True)
            self.assertEqual(child.returncode, 0, child.stderr)
            # The view is not installed globally and did not restore active files.
            self.assertFalse((root / "source.json").exists())
            self.assertEqual((root / "private.bin").read_bytes(), b"changed evidence")
            plain = subprocess.run([sys.executable, "-B", "-c", "import module"],
                                   cwd=root, capture_output=True, text=True)
            self.assertNotEqual(plain.returncode, 0)


if __name__ == "__main__":
    unittest.main()
