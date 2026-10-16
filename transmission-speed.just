# Additive helper authority; existing Frozen/canonical recipes are untouched.
set shell := ["bash", "-euo", "pipefail", "-c"]

check:
    python3 scripts/project/transmission_speed.py check

test:
    python3 scripts/validate_gt3_transmission_speed.py source
    python3 -m unittest discover -s tests -p gt3_transmission_speed_test.py

docs-build:
    just --justfile justfile docs-build

# Explicit local root; missing/changed originals/evidence fail, never skip.
verify-speed root:
    python3 scripts/project/transmission_speed.py verify {{quote(root)}}
