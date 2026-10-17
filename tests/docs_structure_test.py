"""Documentation destinations and narrow publication exception contracts."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_audit", ROOT / "scripts/audit_public.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class DocsStructureTests(unittest.TestCase):
    def test_five_physical_pillars_and_unique_destinations(self):
        docs = ROOT / "docusaurus/docs"
        pillars = {"start-here", "developer-guide", "architecture", "reference", "research"}
        for page in docs.rglob("*.md"):
            self.assertIn(page.relative_to(docs).parts[0], pillars)
        moves = json.loads((ROOT / "docusaurus/doc-paths.json").read_text())
        self.assertEqual(len(moves), len(set(moves.values())))
        for old, new in moves.items():
            with self.subTest(old=old):
                self.assertNotIn("..", Path(new).parts)
                self.assertFalse(Path(new).is_absolute())
                self.assertTrue((docs / new).is_file())
                self.assertFalse((docs / old).exists())
        for pillar in pillars:
            self.assertTrue((docs / pillar / "index.md").is_file())

    def test_original_migration_map_points_to_real_current_documents(self):
        mapping = json.loads((ROOT / "project/gt3/migration-map.json").read_text())["paths"]
        for old, new in mapping.items():
            if new.startswith("docusaurus/docs/"):
                with self.subTest(old=old):
                    self.assertTrue((ROOT / new).is_file())

    def test_generated_directory_exception_is_exact(self):
        self.assertEqual(len(audit.PUBLIC_DOC_VIEWS), 4)
        for name in audit.PUBLIC_DOC_VIEWS:
            self.assertFalse(audit.forbidden_directory(name))
        for name in ["generated/status.md", "docusaurus/docs/reference/generated/other.md",
                     "docusaurus/docs/reference/generated/types.cpp",
                     "docusaurus/docs/reference/generated/local/types.md",
                     "docusaurus/docs/reference/generated/types.md/hidden.elf",
                     "docusaurus/docs/research/evidence/index.md"]:
            with self.subTest(name=name):
                self.assertTrue(audit.forbidden_directory(name))

    def test_public_views_still_reject_binary_and_secret_contents(self):
        name = "docusaurus/docs/reference/generated/types.md"
        for content in [b"\x7fELFsynthetic", b"-----BEGIN " + b"PRIVATE KEY-----"]:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                output = root / name
                output.parent.mkdir(parents=True)
                output.write_bytes(content)
                def git(*args):
                    return b"" if "--stage" in args else name.encode() + b"\0"
                with patch.object(audit, "ROOT", root), patch.object(audit, "git", git), \
                     contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(audit.main(), 1)
