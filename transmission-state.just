# Additive workflow; earlier proof-pinned build/recipe files stay unchanged.
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

check:
    python3 scripts/project/transmission_state.py check

test:
    python3 tests/gt3_transmission_state_test.py
    python3 scripts/validate_gt3_transmission_state.py source

docs-build:
    just docs-build

verify-state root:
    python3 scripts/project/transmission_state.py verify '{{root}}'
