# Additive handbrake tasks. The original justfile is hash-pinned by immutable
# virtual-pedal proof and intentionally remains byte-identical.
set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    just --justfile justfile check
    python3 scripts/project/handbrake.py check
    python3 -m unittest discover -s tests -p gt3_handbrake_test.py

test:
    just --justfile justfile test

docs-generate:
    just --justfile justfile docs-generate
    python3 scripts/project/handbrake.py docs

docs-build: docs-generate
    just --justfile justfile docs-build

verify-handbrake root:
    python3 scripts/project/handbrake.py verify '{{root}}'
