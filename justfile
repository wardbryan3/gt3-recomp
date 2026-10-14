# GT3 selective-decompilation checkpoint. No game files needed for default checks.
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @"{{just_executable()}}" --list

# Locked project-local documentation dependencies; no system installation.
setup:
    npm --prefix docs/site ci --no-audit --no-fund

# Source-only compiler/runtime and reviewed recovered-source library; no game SDK.
build:
    cmake -S . -B build/source -DCMAKE_CXX_COMPILER=clang++ -DBUILD_TESTING=ON -DPS2_WGPU_DIR="$PWD/build/no-gpu-sdk"
    cmake --build build/source --parallel 4

# Hardware, SIF, synthetic patch, metadata and recovered-source consistency.
test: build
    ctest --test-dir build/source --output-on-failure
    python3 tests/gt3_patch_test.py
    python3 -m unittest discover -s tests -p gt3_baseline_validation_test.py
    python3 -m unittest discover -s tests -p project_metadata_test.py
    python3 -m unittest discover -s tests -p publication_test.py

# Public schema/source/type checks, NOT a claim to verify private artifacts.
check:
    python3 scripts/project/project.py check
    scripts/project/check-types.sh
    python3 -m unittest discover -s tests -p project_metadata_test.py
    python3 -m unittest discover -s tests -p publication_test.py
    python3 scripts/audit_public.py
    git diff --check

status:
    python3 scripts/project/project.py status

lookup query:
    python3 scripts/project/project.py lookup '{{query}}'

evidence query:
    python3 scripts/project/project.py evidence '{{query}}'

# Explicit strict check of retained historical evidence; never silently rehash.
verify-private root:
    python3 scripts/project/project.py verify-private '{{root}}'

# Strict current-main evidence verification, separate from the historical root.
verify-current root:
    python3 scripts/project/project.py verify-current '{{root}}'

docs-generate:
    python3 scripts/project/project.py docs

docs-build: docs-generate
    npm --prefix docs/site run diagrams
    npm --prefix docs/site run build

# Binds all interfaces; use trusted networks only. Existing private server unchanged.
docs-dev: docs-generate
    npm --prefix docs/site run start

audit:
    python3 scripts/audit_public.py

# Original-behavior game build; ISO and resulting translations stay local.
build-game iso:
    scripts/build_gt3.sh '{{iso}}'
