#pragma once
// Isolated memory-native projection; no product integration or complete EE ABI claim.
#include <cstdint>

// Recovered field operations for unit46 (economy-recovery investigation).
//
// Status: RECOVERED only. These operations were derived from generated
// unit46 symbol FUN_0021a6d0 / FUN_0021a740 / FUN_0021a7d8.
//
// - They are NOT production credit APIs until caller identity is proven.
// - The semantic link to the session object is still caller-qualified; the
//   base pointer argument is left neutral (named `base`) for that reason.
// - FUN_0021a7d8 is a raw setter and is deliberately NOT
//   a safe developer feature: it writes an unvalidated 64-bit value.
//
// No clamping, no overflow checks, no hidden state, no dependencies beyond
// <cstdint>. All arithmetic is the natural unsigned wrap of C++:
//   - address addition wraps modulo 2^32 (uint32_t)
//   - value addition wraps modulo 2^64 (uint64_t)

namespace gt3::economy_recovery {

// Abstract memory backend. Concrete implementations bind this to a specific
// memory image; the pure operations below depend only on this interface.
class state_memory {
public:
    virtual ~state_memory() = default;
    virtual uint64_t load64(uint32_t address) = 0;
    virtual void store64(uint32_t address, uint64_t value) = 0;
};

namespace detail {
// Recovered field offset, address-named. Neutral name: the semantic
// meaning of this field is not yet caller-qualified.
inline constexpr uint32_t kFieldOffset = 0x18u;
} // namespace detail

// FUN_0021a6d0: return the 64-bit field at base + 0x18.
// Address addition wraps modulo 2^32.
inline uint64_t FUN_0021a6d0(state_memory& mem, uint32_t base) {
    const uint32_t address = base + detail::kFieldOffset; // uint32_t wraps
    return mem.load64(address);
}

// FUN_0021a740: sequential read-modify-write; no concurrency guarantee.
// Value addition wraps modulo 2^64.
inline void FUN_0021a740(state_memory& mem, uint32_t base, uint64_t value) {
    const uint32_t address = base + detail::kFieldOffset; // uint32_t wraps
    const uint64_t old = mem.load64(address);
    mem.store64(address, value + old); // uint64_t wraps (mod 2^64)
}

// FUN_0021a7d8: raw setter. Deliberately NOT a safe developer feature;
// it stores `value` verbatim with no validation or clamping.
inline void FUN_0021a7d8(state_memory& mem, uint32_t base, uint64_t value) {
    const uint32_t address = base + detail::kFieldOffset; // uint32_t wraps
    mem.store64(address, value);
}

} // namespace gt3::economy_recovery
