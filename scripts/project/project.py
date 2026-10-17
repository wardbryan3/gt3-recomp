#!/usr/bin/env python3
"""Current repository consistency, public knowledge views and explicit history.

Historical evidence is not an integration approval for relocated source. Current
source manifests are candidates until separately bound to checkpoint evidence.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "project/gt3"
BASE = "aee79fba37937e4dc99dac4263589d005112c504"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((DB / (name + ".json")).read_text())


def current_path(logical):
    return ROOT / load("migration-map")["paths"].get(logical, logical)


def source_files():
    paths = set()
    for folder in ("src/gt3", "runtime", "recomp", "host", "scripts", "cmake", "validation", "tests"):
        for p in (ROOT / folder).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix in {".cpp", ".hpp", ".inc", ".py", ".sh", ".probes", ".cmake", ".wgsl"}:
                paths.add(p.relative_to(ROOT).as_posix())
    paths.add("CMakeLists.txt")
    paths.add("justfile")
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / '.github/workflows').glob('*.yml'))
    for p in DB.rglob("*"):
        if p.is_file() and p.suffix in {".json", ".probes"} and p.name not in {"source-manifest.json", "proofs.json", "approvals.json", "progress.json"}:
            paths.add(p.relative_to(ROOT).as_posix())
    return {p: sha(ROOT / p) for p in sorted(paths)}


def shape(kind, record):
    definition = load('authority-schema')['$defs'][kind]
    assert set(definition['required']) <= set(record) <= set(definition['properties']), 'invalid ' + kind + ' fields'


def check_approvals(proofs, approvals, observed):
    for proof in proofs['records']:
        shape('proof', proof)
        assert proof['report'].startswith('local/restructuring/') and '..' not in Path(proof['report']).parts
        assert len(proof['report_sha256']) == 64 and all(c in '0123456789abcdef' for c in proof['report_sha256'])
    by_id = {p['id']: p for p in proofs['records']}
    assert len(by_id) == len(proofs['records']), 'duplicate proof IDs'
    for approval in approvals['records']:
        shape('approval', approval)
        assert approval['scope'] == 'original-default-products', 'restructuring cannot approve recovery/enhancement'
        assert approval['status'] in {'approved-bounded', 'superseded'}
        if approval['status'] == 'superseded': continue
        assert approval['dependencies'] == observed, 'STALE approval: source/dependency closure changed'
        assert approval['products'] == ['ps2run', 'gt3-native']
        assert approval['proofs'] and len(set(approval['proofs'])) == len(approval['proofs']), 'approval requires unique independent current proof'
        required = {'current-original-product-matrix', 'current-original-source-fixtures',
                    'fresh-public-source-iso-build', 'public-development-gates'}
        assert required <= {by_id[p]['kind'] for p in approval['proofs']}, 'incomplete checkpoint proof layers'
        for identity in approval['proofs']:
            proof = by_id[identity]
            assert proof['status'] == 'passed-bounded'
            assert proof['dependencies'] == observed, 'STALE proof: dependencies changed'
            assert proof['historical_only'] is False, 'historical proof cannot approve current integration'
            assert len(proof['report_sha256']) == 64


def check():
    assert not os.environ.get('GT3_HISTORY_ROOT'), 'current checks cannot run in a historical source view'
    assert load('progress')['integration_approval'] is False, 'progress cannot grant approval'
    mapping = load("migration-map")
    assert mapping["baseline_revision"] == BASE
    for old, new in mapping["paths"].items():
        assert (ROOT / new).is_file(), f"missing relocated file: {new}"
        assert not (ROOT / old).exists(), f"duplicate active predecessor: {old}"
    implementations = load("implementations")
    owners = {}
    for module in implementations["modules"]:
        shape('module', module)
        assert module["classification"] in {"Recovered", "Modernized", "Enhanced / Extended", "Original"}
        assert module["product_integration"] == "not-approved", "restructuring cannot promote recovery"
        for name in module["sources"]:
            assert name not in owners, f"duplicate source owner: {name}"
            owners[name] = module["id"]
            assert (ROOT / name).is_file(), name
    actual_sources = {p.relative_to(ROOT).as_posix() for p in (ROOT / "src/gt3").rglob("*")
                      if p.is_file() and p.suffix in {".cpp", ".hpp", ".inc"} and "tests" not in p.parts}
    assert actual_sources == set(owners), f"unowned/missing gameplay sources: {actual_sources ^ set(owners)}"
    products = load("products")
    assert products["ps2run"]["enhancements"] == "excluded"
    assert products["gt3-native"]["default_behavior"] == "original-equivalent"
    assert products["gt3-native"]["recovered_integration"] == []
    assert products["gt3-native"]["enhanced_integration"] == []
    if (DB / "source-manifest.json").is_file():
        expected = load("source-manifest")
        shape('candidate', expected)
        assert expected["status"] == "candidate" and expected['integration_approval'] is False, "source identity is not an approval"
        observed = source_files()
        assert expected["files"] == observed, "source/dependency drift: record a NEW candidate; old approval is stale"
    # Original authority bodies remain exact historical facts, never rehashed to
    # make a migration pass. Their source pointers are resolved/displayed via map.
    for old in [*sorted(p for p in mapping["paths"] if p.startswith("decomp/gt3/") and p.endswith(".json")),
                "extensions/gt3/virtual_transmission/validation.json"]:
        original = subprocess.check_output(["git", "show", f"{BASE}:{old}"], cwd=ROOT)
        assert current_path(old).read_bytes() == original, f"historical authority drift: {old}"
    for retired in load('retirements')['retired']:
        assert not (ROOT / retired).exists(), 'obsolete active front door: ' + retired
    check_approvals(load('proofs'), load('approvals'), source_files())
    print(f"Current source/ownership consistency PASS: {len(implementations['modules'])} modules; "
          "no recovered/enhanced product integration. Historical proof is separate.")


def type_assertions():
    types = load("types")
    out = ROOT / "build/foundation/type-assertions.cpp"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ['#include "' + str(current_path(p)) + '"' for p in sorted({x["source"] for x in types["layouts"]})]
    lines.append("#include <cstddef>")
    for layout in types["layouts"]:
        lines.append(f'static_assert(sizeof({layout["cpp"]}) == {layout["size"]});')
        lines += [f'static_assert(offsetof({layout["cpp"]}, {field["name"]}) == {field["offset"]});'
                  for field in layout["fields"]]
    out.write_text("\n".join(lines) + "\n")
    subprocess.run(["clang++", "-std=c++20", "-fsyntax-only", "-I" + str(ROOT / "runtime/include"), str(out)], check=True)


def docs():
    check()
    dest = ROOT / "docusaurus/docs/registry"
    dest.mkdir(parents=True, exist_ok=True)
    def page(name, title, body):
        (dest / (name + ".md")).write_text(f"---\ntitle: {title}\n---\n\n<!-- Generated; edit project/gt3 authorities, not this view. -->\n\n" + body + "\n")
    modules = load("implementations")["modules"]
    text = "These are **current source identities**, not runtime promotion. Both products initially use original generated execution.\n\n| Module | Classification | Current product integration |\n|---|---|---|\n"
    text += "\n".join(f'| {m["id"]} | {m["classification"]} | {m["product_integration"]} |' for m in modules)
    text += '\n\n## Separate bounded product approvals\n\n'
    approvals = load('approvals')['records']
    text += ('\n'.join(f'- `{a["id"]}`: {a["status"]}; scope `{a["scope"]}`.' for a in approvals)
             if approvals else 'No current product approval recorded yet.')
    text += '\n\nPublic consistency checks validate declared source/dependency closure; actual private proof requires `just verify-approval`. No recovery or enhancement promotion follows.\n\n## Execution progress (not approval)\n\n'
    text += '\n'.join(f'- {p["id"]}: {p["name"]} — **{p["status"]}**' for p in load('progress')['phases'])
    page("current-products", "Current products and source ownership", text)
    manifest = load("manifest")
    counts = Counter(f["lifecycle"] for f in manifest["functions"])
    page("status", "Historical selected recovery inventory",
         f"Source context: `{BASE}` and explicitly versioned predecessors. **Not current integration approval or whole-game coverage.**\n\n" +
         "\n".join(f"- {name}: {count}" for name, count in counts.items()) +
         "\n\nSee [current products](current-products.md) for active ownership and integration status.")
    symbols = load("symbols")
    text = "Historical original-profile findings; names with `candidate` remain uncertain.\n\n| Address | Name |\n|---|---|\n"
    text += "\n".join(f'| `{s["address"]}` | `{s["name"]}` |' for s in symbols["functions"] + symbols["data"])
    page("symbols", "Original symbol knowledge", text)
    text = "Partial guest layouts are compiled against **current relocated headers**. This is layout consistency, not gameplay proof.\n"
    for layout in load("types")["layouts"]:
        text += f'\n## {layout["name"]}\n\n`{current_path(layout["source"]).relative_to(ROOT)}`; size `{layout["size"]}`.\n\n| Offset | Field | Meaning |\n|---|---|---|\n'
        text += "\n".join(f'| `{f["offset"]}` | `{f["name"]}` | {f["meaning"]} |' for f in layout["fields"]) + "\n"
    page("types", "Partial type knowledge", text)
    knowledge = ROOT / "docusaurus/static/knowledge"
    knowledge.mkdir(parents=True, exist_ok=True)
    for p in sorted(DB.glob("*.json")):
        if p.name == "source-manifest.json":
            continue
        (knowledge / p.name).write_bytes(p.read_bytes())
    print("Public metadata views generated; no private source/evidence copied")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "docs", "type-assertions", "status", "lookup", "evidence", "record-candidate"])
    parser.add_argument("query", nargs="?")
    args = parser.parse_args()
    if args.command == "record-candidate":
        out = Path(args.query) if args.query else DB / "source-manifest.json"
        # Explicit candidate capture is NOT evidence, historical rehash or approval.
        with out.open("x") as stream:
            json.dump({"schema_version": 1, "status": "candidate", "files": source_files(),
                       "integration_approval": False}, stream, indent=2)
            stream.write("\n")
        return
    if args.command == "check": check()
    elif args.command == "docs": docs()
    elif args.command == "type-assertions": type_assertions()
    elif args.command == "status":
        check()
        print(json.dumps(load("products"), indent=2))
    elif args.command == "lookup":
        if not args.query: parser.error("query required")
        q = args.query.lower()
        try: q = f"0x{int(q,16):08x}"
        except ValueError: pass
        records = load("manifest")["functions"] + load("symbols")["data"]
        print(json.dumps({"context": "historical findings, not current approval",
                          "records": [r for r in records if q in r["address"] or q in r["name"].lower()]}, indent=2))
    else:
        if not args.query: parser.error("query required")
        print(json.dumps({"context": "historical evidence references only",
                          "records": [r for r in load("manifest")["functions"] if args.query.lower() in (r["address"] + r["name"]).lower()]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        print("Project check FAILED:", exc, file=sys.stderr)
        sys.exit(1)
