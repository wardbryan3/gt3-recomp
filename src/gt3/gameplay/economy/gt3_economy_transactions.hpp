#pragma once
// Isolated memory-native projection; no product integration or complete EE ABI claim.
// Bounded transaction-body projection; opaque construction is not recovered.
//
// Isolated recovery, step 1: neutral address-level projection of two economy
// transaction functions recovered from the original unit46 lines 2173-2226.
//
// Scope and limits:
//   - This header is a tiny, self-contained, header-only declaration. It
//     is not linked into either product. It assigns no purchase/sell semantics,
//     adds no balance sufficiency check or clamping, and invents no stats.
//   - The `void` return types below are a *native observable projection*: the
//     recovered original functions are modeled as void at the native address
//     level. That is NOT a claim about the full original EE/ABI return
//     contract (original return/scratch registers are not modeled here).
//   - The dependency object is the abstract `transaction_boundary`
//     interface: six neutral address operations. Concrete bindings live
//     outside this header (integration is explicitly NOT part of this step).
//   - Address arithmetic is 32-bit (`uint32_t`) and wraps modulo 2^32,
//     matching the original PS2 address space; the balance subtraction is
//     64-bit unsigned wrap (modulo 2^64).
//
// Exact original call/load/store order is preserved per function, including
// the unknown side-effect call (FUN_001d9f60) that occurs AFTER the store in
// FUN_00219250.

#include <cstdint>

namespace gt3::economy_recovery {

// Abstract boundary of the transaction address space. Neutral operations
// only: raw 64-bit load/store plus four opaque call sites keyed by their
// original symbol names. Concrete implementations are supplied by the caller;
// this header never instantiates or binds them.
struct transaction_boundary {
  virtual ~transaction_boundary() = default;

  // Raw 64-bit memory load/store at a 32-bit PS2 address.
  virtual std::uint64_t load64(std::uint32_t addr) = 0;
  virtual void store64(std::uint32_t addr, std::uint64_t value) = 0;

  // Projected call sites, NOT complete original callee signatures. A binding
  // would also have to retain the incoming constructor arguments in its
  // dependency environment. Current fixtures do not qualify their forwarding
  // or configuration construction; do not use this as a complete transaction.
  virtual std::uint64_t FUN_00219048(std::uint32_t base) = 0;
  virtual std::uint64_t FUN_00219128(std::uint32_t base) = 0;
  virtual std::uint64_t FUN_00237bc0(std::uint32_t addr) = 0;
  virtual void FUN_001d9f60(std::uint32_t addr) = 0;
};

// FUN_00219250 — original unit46 lines 2173-2226, first transaction path.
//
// Order (exact):
//   1. result_219048 = dep.FUN_00219048(base)
//   2. if result == 0 -> return
//   3. ptr = uint32(result)
//   4. result237bc0  = dep.FUN_00237bc0(ptr + 0x10)   (uint32 wrap)
//   5. old           = dep.load64(base + 0x18)       (uint32 wrap)
//   6. dep.store64(base + 0x18, old - result237bc0)  (64-bit unsigned wrap)
//   7. dep.FUN_001d9f60(ptr + 0x204)                 (unknown side effect,
//                                                     after the store)
//
// No balance sufficiency check and no clamping exist in the original.
inline void FUN_00219250(transaction_boundary &dep, std::uint32_t base) {
  const std::uint64_t result_219048 = dep.FUN_00219048(base);
  if (result_219048 == 0) {
    return;
  }
  const std::uint32_t ptr = static_cast<std::uint32_t>(result_219048);
  const std::uint64_t result237bc0 = dep.FUN_00237bc0(ptr + std::uint32_t(0x10));
  const std::uint64_t old = dep.load64(base + std::uint32_t(0x18));
  dep.store64(base + std::uint32_t(0x18), old - result237bc0);
  dep.FUN_001d9f60(ptr + std::uint32_t(0x204));
}

// FUN_002192a8 — original unit46, second transaction path.
//
// Order (exact):
//   1. result_219128 = dep.FUN_00219128(base)
//   2. if result == 0 -> return
//   3. result237bc0  = dep.FUN_00237bc0(uint32(result) + 0x10) (uint32 wrap)
//   4. old           = dep.load64(base + 0x18)   (uint32 wrap)
//   5. dep.store64(base + 0x18, old - result237bc0) (64-bit unsigned wrap)
//
// No FUN_001d9f60 call, no sufficiency check, no clamping.
inline void FUN_002192a8(transaction_boundary &dep, std::uint32_t base) {
  const std::uint64_t result_219128 = dep.FUN_00219128(base);
  if (result_219128 == 0) {
    return;
  }
  const std::uint64_t result237bc0 =
      dep.FUN_00237bc0(static_cast<std::uint32_t>(result_219128) + std::uint32_t(0x10));
  const std::uint64_t old = dep.load64(base + std::uint32_t(0x18));
  dep.store64(base + std::uint32_t(0x18), old - result237bc0);
}

} // namespace gt3::economy_recovery
