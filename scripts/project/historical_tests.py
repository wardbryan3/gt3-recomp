#!/usr/bin/env python3
"""Preserved authority/reducer negatives with explicit historical SOURCE context.

Current relocated C++ protocol tests compile active source at its new paths.
Independent current product/approval tests run separately WITHOUT this view.
"""
from pathlib import Path
import subprocess
import sys
from run_historical import ROOT, REVISION, historical_env


def main():
    env = historical_env()
    tests = sorted((ROOT / "validation/gt3/integration").glob("*_test.py"))
    for test in tests:
        print("Historical authority negatives / current protocol:", test.relative_to(ROOT), flush=True)
        launcher = ("import sitecustomize,runpy,sys; assert sitecustomize.CONTEXT_READY == "
                    + repr((str(ROOT), REVISION)) + "; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')")
        subprocess.run([sys.executable, "-B", "-c", launcher, str(test)], cwd=ROOT, env=env, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
