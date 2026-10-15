# Additive workflow: all earlier proof-pinned justfiles/CMake/checkers stay intact.
set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    just --justfile handbrake.just check
    python3 scripts/project/virtual_handbrake.py check
    python3 -m unittest discover -s tests -p gt3_virtual_handbrake_test.py

test:
    just --justfile justfile test
    python3 -m unittest discover -s tests -p gt3_virtual_handbrake_test.py

docs-generate:
    just --justfile handbrake.just docs-generate
    python3 scripts/project/virtual_handbrake.py docs

docs-build: docs-generate
    just --justfile justfile docs-build

verify-virtual-handbrake root:
    python3 scripts/project/virtual_handbrake.py verify '{{root}}'
