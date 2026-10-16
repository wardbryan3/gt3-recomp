# Additive one-helper validation; canonical/Frozen build recipes are unchanged.
set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    just --justfile justfile check
    python3 scripts/project/transmission.py check
    python3 -m unittest discover -s tests -p gt3_transmission_test.py
    python3 scripts/validate_gt3_transmission.py source

test:
    just --justfile justfile test
    python3 -m unittest discover -s tests -p gt3_transmission_test.py
    python3 scripts/validate_gt3_transmission.py source

docs-build:
    just --justfile justfile docs-build

# All original evidence is required. A missing/changed artifact is a failure.
verify-transmission root:
    python3 scripts/project/transmission.py verify '{{root}}'

# Private original-dependent isolated oracle only; never installs runtime hooks.
# A new output directory is mandatory; prior attempts are not overwritten.
original-oracle baseline output:
    python3 scripts/validate_gt3_transmission.py original '{{baseline}}' '{{output}}'
