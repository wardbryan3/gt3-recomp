#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$root/scripts/project/project.py" type-assertions
"${CXX:-clang++}" -std=c++20 -fsyntax-only -I"$root/host" -I"$root/runtime/include" "$root/build/foundation/type-assertions.cpp"
