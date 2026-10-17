# Sourced by setup.sh and port.sh: sets cxx_flags to the CMake arguments for a
# C++ compiler that has <format>. $CXX wins when it works; otherwise the newest
# clang++ (with its own libc++ if the system libstdc++ predates GCC 13).
# An absent version-suffixed executable is not a compiler failure.
cxx_flags=()
cxx_probe=$(mktemp -d)
printf '#include <format>\nint main() { return std::format("{}", 1).size() != 1; }\n' > "$cxx_probe/t.cpp"
cxx_candidates=()
[ -n "${CXX:-}" ] && cxx_candidates+=("$CXX")
cxx_candidates+=($( { compgen -c clang++- || true; } | { grep -E '^clang\+\+-[0-9]+$' || true; } | sort -t- -k2 -rn | uniq) clang++)
for cxx in "${cxx_candidates[@]}"; do
  command -v "$cxx" > /dev/null || continue
  "$cxx" --version | grep -qi clang || continue
  for stdlib in "" -stdlib=libc++; do
    if "$cxx" -std=c++20 $stdlib "$cxx_probe/t.cpp" -o "$cxx_probe/t" 2> /dev/null; then
      cxx_flags=(-DCMAKE_CXX_COMPILER="$(command -v "$cxx")")
      [ -z "$stdlib" ] || cxx_flags+=(-DCMAKE_CXX_FLAGS="$stdlib")
      break 2
    fi
  done
done
rm -rf "$cxx_probe"
if [ ${#cxx_flags[@]} -eq 0 ]; then
  echo "no supported Clang compiler here has <format>: install Clang with a C++20 standard library or point CXX at it" >&2
  exit 1
fi
