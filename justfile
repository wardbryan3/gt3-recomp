# One public entry point. Public development needs no game/private fixtures.
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

setup:
    npm --prefix docusaurus ci --no-audit --no-fund

build:
    cmake -S . -B build/gt3-public-source -G Ninja -DCMAKE_CXX_COMPILER=clang++ -DBUILD_TESTING=ON -DPS2_WGPU_DIR="$PWD/build/no-gpu-sdk"
    cmake --build build/gt3-public-source --parallel 6

test: build
    ctest --test-dir build/gt3-public-source --output-on-failure
    python3 -B scripts/project/historical_tests.py
    python3 -B -m unittest discover -s tests -p '*_test.py'

check:
    python3 -B scripts/project/project.py check
    python3 -B scripts/project/project.py type-assertions
    python3 -B scripts/project/run_historical.py metadata "$PWD"
    python3 -B -m unittest discover -s tests -p '*_test.py'
    python3 -B scripts/audit_public.py
    git diff --check

status:
    python3 -B scripts/project/project.py status

lookup query:
    python3 -B scripts/project/project.py lookup '{{query}}'

evidence query:
    python3 -B scripts/project/project.py evidence '{{query}}'

docs-generate:
    python3 -B scripts/project/project.py docs

docs-build: docs-generate
    npm --prefix docusaurus run diagrams
    npm --prefix docusaurus run build

docs-dev: docs-generate
    npm --prefix docusaurus run start

audit:
    python3 -B scripts/audit_public.py

# NEW names are required: discovery/build outputs never overwrite accepted ones.
build-game iso name:
    python3 -B scripts/project/products.py generate '{{iso}}' '{{name}}'

# These commands explicitly verify OLD contexts, not the current integration.
verify-historical profile root:
    python3 -B scripts/project/run_historical.py '{{profile}}' '{{root}}'

verify-private root:
    python3 -B scripts/project/run_historical.py original '{{root}}'

verify-current root:
    python3 -B scripts/project/run_historical.py baseline '{{root}}'

verify-pedals root:
    python3 -B scripts/project/run_historical.py pedals '{{root}}'

verify-pedal-profiles root:
    python3 -B scripts/project/run_historical.py profiles '{{root}}'

verify-pedal-admission root:
    python3 -B scripts/project/run_historical.py admission '{{root}}'

verify-pedal-closure root:
    python3 -B scripts/project/run_historical.py closure '{{root}}'

verify-virtual-pedals root:
    python3 -B scripts/project/run_historical.py virtual-pedals '{{root}}'

verify-handbrake root:
    python3 -B scripts/project/run_historical.py handbrake '{{root}}'

verify-virtual-handbrake root:
    python3 -B scripts/project/run_historical.py virtual-handbrake '{{root}}'

verify-transmission root:
    python3 -B scripts/project/run_historical.py transmission '{{root}}'

verify-transmission-speed root:
    python3 -B scripts/project/run_historical.py speed '{{root}}'

verify-transmission-state root:
    python3 -B scripts/project/run_historical.py state '{{root}}'

verify-extensions root:
    python3 -B scripts/project/run_historical.py extensions '{{root}}'

# Current checkpoint verification is deliberately separate from historical proof.
# Names select NEW ignored outputs; no result or expectation is overwritten.
qualify-products receipt name:
    python3 -B scripts/project/matrix.py 'local/restructuring/{{name}}-catalogue.json'
    python3 -B scripts/project/checkpoint.py run '{{receipt}}' 'local/restructuring/{{name}}-catalogue.json' 'local/restructuring/{{name}}-products'

original-fixtures receipt name:
    python3 -B scripts/project/source_fixtures.py run '{{receipt}}' 'local/restructuring/{{name}}-fixtures'

verify-source-fixtures report:
    python3 -B scripts/project/source_fixtures.py verify '{{report}}'

verify-checkpoint report:
    python3 -B scripts/project/checkpoint.py verify '{{report}}'

verify-approval:
    python3 -B scripts/project/acceptance.py
