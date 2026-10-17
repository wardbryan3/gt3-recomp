"""Public fail-closed tests; no game inputs or private workspace required."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("restructuring", ROOT / "scripts/project/restructuring.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RestructuringTests(unittest.TestCase):
    def test_portable_relative_paths(self):
        for value in ["/tmp/x", "../x", "a/../x", "a//b", "./a", ".", "", "a\\b"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.relative_path(value)
        self.assertEqual(m.relative_path("src/gt3/file.cpp"), "src/gt3/file.cpp")

    def test_explicit_source_maps_not_private_artifact_payloads(self):
        data = {"sources": {"host/x.cpp": "a" * 64},
                "artifacts": [{"path": "local/input.bin", "sha256": "b" * 64}],
                "nested": {"frozen_source_hashes": {"host/old.cpp": "c" * 64}}}
        self.assertEqual({p["path"] for p in m.source_pins(data)}, {"host/x.cpp", "host/old.cpp"})

    def test_corrected_documentation_destination(self):
        self.assertEqual(m.target_path("docs/site/docs/architecture.md"),
                         "docusaurus/docs/architecture/index.md")
        self.assertEqual(m.target_path("decomp/gt3/schema.md"),
                         "docusaurus/docs/reference/historical-knowledge-schema.md")
        self.assertEqual(m.target_path("runtime/src/system.cpp"), "runtime/src/system.cpp")
        self.assertIsNone(m.target_path("docs/site/docs/unclassified.md"))
        self.assertIsNone(m.target_path("docs/gt3/unclassified.md"))

    def test_historical_git_source_never_uses_active_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root)
            git("init", "-q")
            git("config", "user.name", "Synthetic Test")
            git("config", "user.email", "test@example.invalid")
            (root / "source.cpp").write_text("original\n")
            git("add", "source.cpp")
            git("commit", "-qm", "synthetic source")
            revision = git("rev-parse", "HEAD").decode().strip()
            expected = hashlib.sha256(b"original\n").hexdigest()
            (root / "source.cpp").write_text("changed\n")
            self.assertEqual(m.git_source(root, revision, "source.cpp", expected), b"original\n")
            with self.assertRaises(ValueError):
                m.git_source(root, revision, "source.cpp", "0" * 64)
            with self.assertRaises(ValueError):
                m.git_source(root, "HEAD", "source.cpp", expected)
            with self.assertRaises(subprocess.CalledProcessError):
                m.git_source(root, revision, "missing.cpp", expected)

    def test_private_predecessor_is_exact_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            artifact = root / "local/history/source.cpp"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"private predecessor")
            expected = m.digest(artifact)
            context = {"source_revision": "0" * 40,
                       "private_sources": {"host/source.cpp": {
                           "path": "local/history/source.cpp", "sha256": expected}}}
            self.assertEqual(m.historical_source(root, context, "host/source.cpp", expected, root),
                             b"private predecessor")
            with self.assertRaises(ValueError):
                m.historical_source(root, context, "host/source.cpp", expected)
            artifact.write_bytes(b"modified")
            with self.assertRaises(ValueError):
                m.historical_source(root, context, "host/source.cpp", expected, root)
            artifact.unlink()
            with self.assertRaises(FileNotFoundError):
                m.historical_source(root, context, "host/source.cpp", expected, root)

    def test_baseline_detects_missing_and_changed_source(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / "source.cpp"
            p.write_bytes(b"original")
            report = {"files": [{"path": p.name, "sha256": m.digest(p)}]}
            self.assertEqual(m.verify_unchanged(root, report), [])
            p.write_bytes(b"changed")
            self.assertEqual(len(m.verify_unchanged(root, report)), 1)
            p.unlink()
            self.assertEqual(len(m.verify_unchanged(root, report)), 1)

    def test_backup_checks_both_copies_against_expectations(self):
        with tempfile.TemporaryDirectory() as d:
            primary, backup = Path(d) / "primary", Path(d) / "backup"
            primary.mkdir()
            backup.mkdir()
            for root in [primary, backup]:
                (root / "fixture").write_bytes(b"synthetic")
            members = [{"path": "fixture", "sha256": m.digest(primary / "fixture")}]
            self.assertEqual(m.verify_backup(primary, backup, members), [])
            (backup / "fixture").unlink()
            self.assertEqual(m.verify_backup(primary, backup, members)[0]["copy"], "backup")
            (backup / "fixture").write_bytes(b"changed")
            (primary / "fixture").write_bytes(b"changed")
            self.assertEqual(len(m.verify_backup(primary, backup, members)), 2)
            with self.assertRaises(ValueError):
                m.verify_backup(primary, primary, members)
            with self.assertRaises(ValueError):
                m.verify_backup(primary, backup, [])
            with self.assertRaises(ValueError):
                m.verify_backup(primary, backup, members * 2)

    def test_backup_hardlinks_do_not_establish_independent_preservation(self):
        with tempfile.TemporaryDirectory() as d:
            primary, backup = Path(d) / "primary", Path(d) / "backup"
            primary.mkdir()
            backup.mkdir()
            (primary / "fixture").write_bytes(b"synthetic")
            (backup / "fixture").hardlink_to(primary / "fixture")
            members = [{"path": "fixture", "sha256": m.digest(primary / "fixture")}]
            self.assertIn("independent", m.verify_backup(primary, backup, members)[0]["error"])

    def test_scope_manifest_cannot_be_silently_replaced(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "manifest.json"
            path.write_text(json.dumps({"files": [{"path": "fixture", "sha256": "a" * 64}]}))
            expected = m.digest(path)
            self.assertEqual(len(m.pinned_manifest(path, expected)), 1)
            path.write_text(json.dumps({"files": []}))
            with self.assertRaises(ValueError):
                m.pinned_manifest(path, expected)

    def test_record_does_not_grant_gameplay_approval(self):
        record = json.loads((ROOT / "project/gt3/restructuring.json").read_text())
        self.assertEqual(record["integration_approvals_issued_by_restructuring"], [])
        self.assertEqual(record["ownership"]["documentation_root"], "docusaurus/docs/")
        self.assertEqual(set(record["classifications"]),
                         {"Original", "Recovered", "Modernized", "Enhanced / Extended"})
        progress = json.loads((ROOT / record['progress_authority']).read_text())
        self.assertFalse(progress['integration_approval'])
        self.assertEqual(progress['policy_authority'], 'project/gt3/restructuring.json')
        self.assertEqual([p["id"] for p in progress["phases"]], list(range(8)))
        self.assertTrue(all(p["status"] in {"not-started", "in-progress", "blocked", "accepted"}
                            for p in progress["phases"]))

    def test_escaped_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "context"
            root.mkdir()
            (root / "escape").symlink_to(Path(d))
            with self.assertRaises(ValueError):
                m.local_file(root, "escape/outside")

    def test_reports_cannot_be_published_or_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            subprocess.run(["git", "init", "-q", root], check=True)
            (root / ".gitignore").write_text("/local/\n")
            with self.assertRaises(ValueError):
                m.private_output(root, root / "report.json", {})
            target = root / "local/restructuring/report.json"
            m.private_output(root, target, {"status": "inventory"})
            self.assertEqual(json.loads(target.read_text())["status"], "inventory")
            with self.assertRaises(FileExistsError):
                m.private_output(root, target, {})


if __name__ == "__main__":
    unittest.main()
