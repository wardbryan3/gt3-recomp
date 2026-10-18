#pragma once
// Isolated memory-native projection; no product integration or complete EE ABI claim.
//
// Isolated eligibility-body projections; opaque dependencies stay explicit.
//
// Recovered economy checks FUN_0011bc18 / FUN_0011bce0, extracted from the
// original reference. These are recovered checks only:
//
//   * The dependency interface below names opaque original functions by
//     address; their behavior is not interpreted and no struct, profile,
//     or save layout is assumed for the addresses.
//   * Variable names are neutral, offset/address-based identifiers
//     (field_30d00, field_18, result_237bc0, ...).
//   * Address arithmetic wraps modulo 2^32, matching the original.
//   * No integration, enhancement, or whole-transaction claims are made
//     here. This header is a self-contained syntax-level recovery aid.
//
// Exact recovered behavior (verified against the original):
//   state1  = FUN_00218660();
//   ptr     = load32(state1 + 0x30d00);
//   state2  = FUN_00218660();
//   ptr    += 0x10;
//   balance = bit_cast<int64_t>(load64(state2 + 0x18));
//   flags   = FUN_00234380(ptr);
//   if (flags & mask) { FUN_001c4f80(4); return 0x30ff90; }
//   result_237bc0 = FUN_00237bc0(ptr);
//   if (balance < result_237bc0) { FUN_001c4f80(4); return 0x30ffa8; }
//   state3 = FUN_00218660();
//   value_219448 = FUN_00219448(state3);
//   if (value_219448 < 200) return 0;
//   FUN_001c4f80(4);
//   return 0x30ffb8;
//
// The two inline entry points share the detail check and differ only in
// the mask constant passed: FUN_0011bc18 passes mask1, FUN_0011bce0
// passes mask2.

#include <bit>
#include <cstdint>

namespace gt3::economy_recovery {

/// Opaque recovered addresses used by the checks. These are plain address
/// offsets; they are NOT struct/profile/save field names.
inline constexpr uint32_t field_30d00 = 0x30d00;
inline constexpr uint32_t ptr_offset_10 = 0x10;
inline constexpr uint32_t field_18 = 0x18;

/// Recovered mask constants passed to the shared detail check.
inline constexpr uint64_t mask1 = 0x1;
inline constexpr uint64_t mask2 = 0x2;

/// Abstract interface for the opaque original dependencies of the
/// recovered checks. Implementations are provided by the original-side
/// harness; no behavior is assumed here.
struct dependency {
  virtual ~dependency() = default;

  virtual uint32_t FUN_00218660() = 0;
  virtual uint32_t load32(uint32_t address) = 0;
  virtual uint64_t load64(uint32_t address) = 0;
  virtual uint64_t FUN_00234380(uint32_t address) = 0;
  virtual int64_t FUN_00237bc0(uint32_t address) = 0;
  virtual int64_t FUN_00219448(uint32_t address) = 0;
  virtual void FUN_001c4f80(uint32_t address) = 0;
};

namespace detail {

/// Shared recovered detail check. Exact ordering and wrapping address
/// arithmetic as verified from the original.
inline uint32_t check(dependency& dep, uint64_t mask) {
  uint32_t state1 = dep.FUN_00218660();
  uint32_t ptr = dep.load32(state1 + field_30d00);
  uint32_t state2 = dep.FUN_00218660();
  ptr += ptr_offset_10;
  const int64_t balance =
      std::bit_cast<int64_t>(dep.load64(state2 + field_18));
  const uint64_t flags = dep.FUN_00234380(ptr);
  if ((flags & mask) != 0) {
    dep.FUN_001c4f80(4);
    return 0x30ff90;
  }
  const int64_t result_237bc0 = dep.FUN_00237bc0(ptr);
  if (balance < result_237bc0) {
    dep.FUN_001c4f80(4);
    return 0x30ffa8;
  }
  uint32_t state3 = dep.FUN_00218660();
  const int64_t value_219448 = dep.FUN_00219448(state3);
  if (value_219448 < 200) {
    return 0;
  }
  dep.FUN_001c4f80(4);
  return 0x30ffb8;
}

}  // namespace detail

/// Recovered FUN_0011bc18: shared detail check with mask1.
inline uint32_t FUN_0011bc18(dependency& dep) {
  return detail::check(dep, mask1);
}

/// Recovered FUN_0011bce0: shared detail check with mask2.
inline uint32_t FUN_0011bce0(dependency& dep) {
  return detail::check(dep, mask2);
}

}  // namespace gt3::economy_recovery
