set shell := ["bash", "-euo", "pipefail", "-c"]

# Explicit workflow only; not imported into the canonical justfile or build.
default:
    @just --justfile extensions.just --list

check:
    python3 -B scripts/project/extensions.py check

test:
    python3 -B scripts/project/extensions.py test
    python3 -B -m unittest discover -s tests -p gt3_extensions_test.py

verify-extensions root:
    python3 -B scripts/project/extensions.py verify "{{root}}"
