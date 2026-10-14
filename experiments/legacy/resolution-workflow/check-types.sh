#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)";cd "$root"
export PATH="/home/b/experiments/gt3-native-20261013/toolchain/bin:$PATH"
python3 tools/project.py type-assertions
clang++ -std=c++20 -fsyntax-only -I host -I runtime/include build/foundation/type-assertions.cpp
echo 'Partial type size/offset assertions PASS (observations are deliberately untyped)'
