#!/usr/bin/env python3
"""Read-only restructuring inventory and historical-source/backup preflight.

No evidence is rewritten, no approval is issued, and no runtime checkout is made.
Reports are private: paths, dependency context and failures may be machine-local.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
REVISION = re.compile(r"[0-9a-f]{40}\Z")
AUTHORITY_PATHS = (
    "decomp/gt3/current-validation.json", "decomp/gt3/handbrake.json",
    "decomp/gt3/manifest.json", "decomp/gt3/pedal-admission-49af40.json",
    "decomp/gt3/pedal-closure.json", "decomp/gt3/pedal-profiles.json",
    "decomp/gt3/pedal-validation.json", "decomp/gt3/provenance.json",
    "decomp/gt3/symbols.json", "decomp/gt3/transmission-speed.json",
    "decomp/gt3/transmission-state.json", "decomp/gt3/transmission.json",
    "decomp/gt3/types.json", "decomp/gt3/virtual-handbrake.json",
    "decomp/gt3/virtual-pedals.json",
    "extensions/gt3/virtual_transmission/validation.json",
)
HASH_MAPS = {"sources", "protected", "source_hashes", "protected_hashes",
             "frozen_source_hashes"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def relative_path(value):
    if not isinstance(value, str) or "\\" in value:
        raise ValueError("expected a portable relative path")
    p = PurePosixPath(value)
    if not value or p.is_absolute() or ".." in p.parts or str(p) != value or value == ".":
        raise ValueError(f"unsafe or noncanonical path: {value}")
    return value


def local_file(root, path):
    path = relative_path(path)
    p = root / path
    if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"symlink or escaped context: {path}")
    return p


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE)


def git_source(root, revision, path, expected):
    """Retrieve exact committed bytes. Never fall back to active files or HEAD."""
    if not REVISION.fullmatch(revision) or not SHA256.fullmatch(expected):
        raise ValueError("full revision and SHA-256 required")
    path = relative_path(path)
    body = git(root, "show", f"{revision}:{path}")
    if hashlib.sha256(body).hexdigest() != expected:
        raise ValueError(f"historical source mismatch: {revision}:{path}")
    return body


def historical_source(root, context, path, expected, private_root=None):
    """Resolve a named historical source, never the active implementation.

    Registered private predecessors are selected only by the exact logical path
    AND original hash. All other requests must match the explicit Git revision.
    This does not redirect runtime, generated-oracle or arbitrary evidence reads.
    """
    path = relative_path(path)
    if not isinstance(expected, str) or not SHA256.fullmatch(expected):
        raise ValueError("immutable expected source hash required")
    predecessor = context.get("private_sources", {}).get(path)
    if predecessor is not None and predecessor["sha256"] == expected:
        if private_root is None:
            raise ValueError(f"required private historical source unavailable: {path}")
        artifact = local_file(private_root, predecessor["path"])
        if digest(artifact) != expected:
            raise ValueError(f"private historical source changed: {path}")
        return artifact.read_bytes()
    return git_source(root, context["source_revision"], path, expected)


def verify_source_context(root, context, private_root, backup_root):
    """Verify declared source resolution; NOT an execution of old verifiers."""
    revision = context["source_revision"]
    authority = relative_path(context["private_sources_authority"])
    original = json.loads(git(root, "show", f"{revision}:{authority}"))
    registered = {name: {key: item[key] for key in ("path", "sha256")}
                  for name, item in original["historical_sources"].items()}
    if context["private_sources"] != registered:
        raise ValueError("private predecessor registration differs from immutable Git authority")
    # Current declarations must not silently drop a source requirement.
    data = inventory(root, revision)
    requests = {(p["path"], p["sha256"]) for p in data["source_pins"]}
    requests.update((p, item["sha256"]) for p, item in registered.items())
    for path, expected in sorted(requests):
        historical_source(root, context, path, expected, private_root)
    members = [{"path": p["path"], "sha256": p["sha256"]}
               for p in registered.values()]
    failures = verify_backup(private_root, backup_root, members)
    if failures:
        raise ValueError(f"historical predecessor backup failed: {failures}")
    return len(requests)


def source_pins(value, pointer=""):
    """Extract explicit path/hash maps without confusing artifact pins with source."""
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            here = pointer + "/" + key
            if key in HASH_MAPS and isinstance(child, dict):
                for path, expected in child.items():
                    if isinstance(expected, str) and SHA256.fullmatch(expected):
                        found.append({"pointer": here, "path": relative_path(path),
                                      "sha256": expected})
            else:
                found.extend(source_pins(child, here))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found.extend(source_pins(child, pointer + "/" + str(i)))
    return found


def target_path(path):
    """Mechanical destination candidates; not permission to split mixed files."""
    if path.startswith("docs/site/"):
        return "docusaurus/" + path.removeprefix("docs/site/")
    if path.startswith("docs/gt3/"):
        return "docusaurus/docs/development/" + path.removeprefix("docs/gt3/")
    if path == "decomp/gt3/schema.md":
        return "docusaurus/docs/reference/knowledge-schema.md"
    if path.startswith("decomp/gt3/") and path.endswith(".json"):
        return "project/gt3/" + path.removeprefix("decomp/gt3/")
    prose = {"HANDOFF.md": "docusaurus/docs/development/continuation.md",
             "CONTRIBUTING.md": "docusaurus/docs/development/contributing.md",
             "decomp/README.md": "docusaurus/docs/reference/recovery.md"}
    if path in prose:
        return prose[path]
    if path.startswith("host/gt3_"):
        domain = "transmission" if "transmission" in path else "controls"
        return "src/gt3/gameplay/" + domain + "/" + Path(path).name
    if path.startswith("extensions/gt3/virtual_transmission/"):
        name = Path(path).name
        if name == "validation.json":
            return "project/gt3/virtual-transmission.json"
        return "src/gt3/gameplay/transmission/virtual/" + name
    if path.startswith("extensions/gt3/native_bindings/"):
        return "src/gt3/bindings/ps2/virtual-transmission/" + Path(path).name
    if path == "tests/gt3_extensions/controller_test.cpp":
        return "src/gt3/gameplay/transmission/tests/virtual-controller_test.cpp"
    if path.startswith("tests/gt3_extensions/"):
        return "validation/gt3/integration/extensions/" + Path(path).name
    if path.startswith("tests/gt3_"):
        name = Path(path).name
        if name in {"gt3_hardware.cpp", "gt3_patch_test.py"}:
            return path
        domain = "transmission" if "transmission" in name else "controls"
        if ("source_test.cpp" in name or name in {
                "gt3_virtual_pedals_test.cpp", "gt3_virtual_handbrake_test.cpp",
                "gt3_virtual_handbrake_samples.hpp"}):
            return "src/gt3/gameplay/" + domain + "/tests/" + name
        if name.endswith(".py"):
            return "validation/gt3/integration/" + name
        if any(word in name for word in ("host", "observer", "layout", "baseline_clock")):
            return "validation/gt3/live/" + name
        return "validation/gt3/differential/" + name
    if path.startswith("experiments/legacy/") and path.endswith(".md"):
        return "docusaurus/docs/history/legacy/" + path.removeprefix("experiments/legacy/")
    return path


def inventory(root, revision):
    if not REVISION.fullmatch(revision):
        raise ValueError("full baseline revision required")
    paths = git(root, "ls-tree", "-r", "--name-only", "-z", revision).decode().split("\0")
    rows = []
    pins = []
    authorities = []
    for authority in AUTHORITY_PATHS:
        body = git(root, "show", f"{revision}:{authority}")
        data = json.loads(body)
        authorities.append({"path": authority, "sha256": hashlib.sha256(body).hexdigest(),
                            "git_revision": revision,
                            "private_manifest": data.get("private"),
                            "artifacts": data.get("artifacts", [])})
        pins.extend(dict(item, authority=authority) for item in source_pins(data))
    bodies = {path: git(root, "show", f"{revision}:{path}")
              for path in sorted(p for p in paths if p)}
    for path, body in bodies.items():
        full, name = path.encode(), Path(path).name.encode()
        consumers = [consumer for consumer, text in bodies.items()
                     if consumer != path and (full in text or name in text)]
        rows.append({"path": path, "destination": target_path(path),
                     "sha256": hashlib.sha256(body).hexdigest(),
                     "pin_owners": sorted({p["authority"] for p in pins if p["path"] == path}),
                     "literal_consumers": consumers})
    return {"schema_version": 1, "baseline_revision": revision,
            "scope": "inventory only; no integration approval",
            "files": rows, "authorities": authorities, "source_pins": pins,
            "limitations": [
                "Destination candidates do not authorize extraction of mixed gameplay/CPU files.",
                "Literal consumers are conservative search leads, not a complete dependency graph.",
                "Private verifier imports, nested manifests and absolute-path reads require separate audit.",
                "Passing hash checks is not differential execution or a fresh native matrix.",
                "Pin extraction covers named source maps, not every bespoke verifier predicate."]}


def verify_unchanged(root, report):
    failures = []
    for item in report["files"]:
        try:
            if digest(local_file(root, item["path"])) != item["sha256"]:
                failures.append({"path": item["path"], "error": "changed"})
        except (OSError, ValueError) as exc:
            failures.append({"path": item["path"], "error": str(exc)})
    return failures


def verify_backup(primary, backup, members):
    """Check BOTH copies against immutable expectations, never against each other alone."""
    primary, backup = primary.resolve(strict=True), backup.resolve(strict=True)
    if primary == backup or primary.is_relative_to(backup) or backup.is_relative_to(primary):
        raise ValueError("backup must be a separate non-overlapping context")
    seen = set()
    failures = []
    if not members:
        raise ValueError("empty backup scope")
    for item in members:
        path, expected = relative_path(item["path"]), item["sha256"]
        if path in seen or not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise ValueError("duplicate path or invalid hash in backup scope")
        seen.add(path)
        first, second = primary / path, backup / path
        if first.exists() and second.exists() and first.samefile(second):
            failures.append({"copy": "backup", "path": path, "error": "not an independent copy"})
        for label, root in [("primary", primary), ("backup", backup)]:
            try:
                if digest(local_file(root, path)) != expected:
                    failures.append({"copy": label, "path": path, "error": "changed"})
            except (OSError, ValueError) as exc:
                failures.append({"copy": label, "path": path, "error": str(exc)})
    return failures


def pinned_manifest(path, expected):
    if not SHA256.fullmatch(expected) or digest(path) != expected:
        raise ValueError("backup scope manifest mismatch; use the immutable authority expectation")
    data = json.loads(path.read_text())
    return data["files"]


def private_output(root, path, data):
    """Exclusive creation, restricted to ignored local/restructuring reports."""
    path = path.absolute()
    area = (root / "local/restructuring").resolve()
    if not path.resolve().is_relative_to(area):
        raise ValueError("reports must remain under ignored local/restructuring/")
    rel = path.relative_to(root).as_posix()
    subprocess.run(["git", "check-ignore", "-q", "--", rel], cwd=root, check=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as out:
        json.dump(data, out, indent=2)
        out.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inventory")
    p.add_argument("--revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("check-baseline")
    p.add_argument("report", type=Path)
    p = sub.add_parser("check-git-source")
    p.add_argument("revision")
    p.add_argument("path")
    p.add_argument("sha256")
    p = sub.add_parser("verify-source-context")
    p.add_argument("context", type=Path)
    p.add_argument("private_root", type=Path)
    p.add_argument("backup_root", type=Path)
    p = sub.add_parser("check-backup")
    p.add_argument("primary", type=Path)
    p.add_argument("backup", type=Path)
    p.add_argument("manifest", type=Path)
    p.add_argument("--manifest-sha256", required=True,
                   help="Immutable expected manifest hash, not a freshly computed replacement")
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            data = inventory(ROOT, args.revision)
            private_output(ROOT, args.output, data)
            print(f"Inventory: {len(data['files'])} files, {len(data['source_pins'])} explicit source pins; no approval")
        elif args.command == "verify-source-context":
            count = verify_source_context(ROOT, json.loads(args.context.read_text()),
                                          args.private_root, args.backup_root)
            print(f"{count} historical source requests resolved independently of active source paths; "
                  "private predecessors and backup verified. Not old-verifier execution or integration approval")
        elif args.command == "check-git-source":
            git_source(ROOT, args.revision, args.path, args.sha256)
            print("Exact historical Git bytes verified; no gameplay or integration claim")
        else:
            if args.command == "check-baseline":
                failures = verify_unchanged(ROOT, json.loads(args.report.read_text()))
            else:
                failures = verify_backup(args.primary, args.backup,
                                         pinned_manifest(args.manifest, args.manifest_sha256))
            if failures:
                print(json.dumps({"status": "failed", "failures": failures}, indent=2))
                return 1
            print("Required hashes verified; not live-game proof or product approval")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"Restructuring preflight FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
