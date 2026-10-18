#pragma once
#include <cstdint>

namespace gt3::economy_recovery {
// Original USA v1.10 table mechanics. No schema/vehicle class is inferred.
// Addresses wrap at 32 bits; the binding supplies original guest memory access.
struct catalog_memory {
    virtual ~catalog_memory() = default;
    virtual std::uint16_t load16(std::uint32_t address) = 0;
    virtual std::uint32_t load32(std::uint32_t address) = 0;
    virtual std::uint64_t load64(std::uint32_t address) = 0;
};
std::uint32_t FUN_00231548(catalog_memory&, std::uint32_t handle,
                          std::uint32_t selector);
// Requires an accessible nonempty sorted table (header count/stride at +8/+10),
// as established for fixtures. Original has no empty-table safety guard.
// Return is the sign-extended 32-bit index, or all-one bits for not found.
std::uint64_t FUN_002316e8(catalog_memory&, std::uint32_t table, std::uint64_t key);
std::uint32_t FUN_002315d8(catalog_memory&, std::uint32_t handle,
                          std::uint32_t selector, std::uint64_t key);
// GP-relative global predicate. Meaning of the mode is deliberately unnamed.
bool FUN_00231680(catalog_memory&, std::uint32_t gp);
// Preserves the caller's missing-row read at address 0xec; no invented fallback.
// Returns the sign-extended low 32 bits of the original price calculation.
std::int64_t FUN_00237bc0(catalog_memory&, std::uint32_t record_plus_10,
                         std::uint32_t gp);

struct post_debit_boundary {
    virtual ~post_debit_boundary() = default;
    // Original returns through f0. This API transports its float32 bits without
    // host arithmetic or an invented interpretation of record field +0x208.
    virtual std::uint32_t FUN_001dac48(std::uint32_t argument) = 0;
    virtual void store32(std::uint32_t address, std::uint32_t bits) = 0;
};
void FUN_001d9ce8(post_debit_boundary&, std::uint32_t subrecord);
void FUN_001d9f60(post_debit_boundary&, std::uint32_t subrecord);
}
