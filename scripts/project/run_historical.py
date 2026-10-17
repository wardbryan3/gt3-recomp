#!/usr/bin/env python3
"""Run a specifically registered OLD verifier against exact historical public source.

This verifies historical evidence only, never current integration. No old source
checkout is made. Current product verification must run without this source view.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REVISION = "aee79fba37937e4dc99dac4263589d005112c504"
COMMANDS = {
    "metadata": ("scripts/project/project.py", ["check"]),
    "original": ("scripts/project/project.py", ["verify-private"]),
    "baseline": ("scripts/project/project.py", ["verify-current"]),
    "pedals": ("scripts/project/project.py", ["verify-pedals"]),
    "profiles": ("scripts/project/project.py", ["verify-pedal-profiles"]),
    "admission": ("scripts/audit_gt3_pedal_admission.py", ["verify", "--root"]),
    "closure": ("scripts/verify_gt3_pedal_closure.py", []),
    "virtual-pedals": ("scripts/project/virtual_pedals.py", ["verify"]),
    "handbrake": ("scripts/project/handbrake.py", ["verify"]),
    "virtual-handbrake": ("scripts/project/virtual_handbrake.py", ["verify"]),
    "transmission": ("scripts/project/transmission.py", ["verify"]),
    "speed": ("scripts/project/transmission_speed.py", ["verify"]),
    "state": ("scripts/project/transmission_state.py", ["verify"]),
    "extensions": ("scripts/project/extensions.py", ["verify"]),
}


def historical_env():
    env = dict(os.environ, GT3_HISTORY_ROOT=str(ROOT), GT3_HISTORY_REVISION=REVISION,
               PYTHONDONTWRITEBYTECODE="1")
    hook = str(ROOT / "scripts/historical_context")
    env["PYTHONPATH"] = hook + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("profile", choices=COMMANDS)
    p.add_argument("evidence_root", type=Path)
    args = p.parse_args()
    evidence = args.evidence_root.resolve(strict=True)
    if args.profile != "original" and evidence != ROOT:
        p.error("this context's recorded executed identities require the explicit active evidence root")
    script, command = COMMANDS[args.profile]
    # Verify registered context and exact Git availability before enabling the view.
    context = json.loads((ROOT / "project/gt3/historical-context.json").read_text())
    if context["source_revision"] != REVISION:
        p.error("historical context drift; create a separately reviewed context")
    subprocess.run(["git", "cat-file", "-e", REVISION + ":" + script], cwd=ROOT, check=True)
    env = historical_env()
    launcher = (
        "import pathlib,sys,sitecustomize; "
        "assert sitecustomize.CONTEXT_READY == (" + repr(str(ROOT)) + "," + repr(REVISION) + "), 'historical context unavailable'; "
        "p=pathlib.Path(sys.argv[1]); "
        "sys.path.insert(0,str(p.parent)); sys.argv=sys.argv[1:]; "
        "exec(compile(p.read_bytes(),str(p),'exec'),"
        "{'__name__':'__main__','__file__':str(p)})"
    )
    print(f"HISTORICAL ONLY: {args.profile}; source {REVISION}; "
          "private/runtime reads unchanged; no current integration approval", flush=True)
    return subprocess.run([sys.executable, "-B", "-c", launcher,
                           str(ROOT / script), *command, str(evidence)],
                          cwd=ROOT, env=env).returncode


if __name__ == "__main__":
    sys.exit(main())
