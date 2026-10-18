#include "gt3_economy_catalog.hpp"

#include <bit>

namespace gt3::economy_recovery {

// Statically established native projection of the original USA v1.10 catalog
// table mechanics; this is not a full ABI. Addresses wrap at 32 bits via the
// binding's guest memory access.
std::uint32_t FUN_00231548(catalog_memory& memory, std::uint32_t handle,
                          std::uint32_t selector) {
    // Original load order: root, mask, encoded, offset.
    const std::uint32_t root = memory.load32(handle);
    const std::uint32_t mask = memory.load32(root + 12u);
    const std::uint32_t encoded = memory.load32(root + selector * 4u + 16u);
    const std::uint32_t offset = memory.load32(root + 8u);
    // Native unsigned arithmetic preserves the original uint32 wrap.
    return root + (encoded & ~mask) + offset;
}

// Binary search over a nonempty sorted table (count/stride at +8/+10).
// Returns the sign-extended 32-bit row index, or all-one bits for not found.
// Original has no empty-table guard or validation.
std::uint64_t FUN_002316e8(catalog_memory& memory, std::uint32_t table,
                          std::uint64_t key) {
    const std::uint16_t stride = memory.load16(table + 10u);
    const std::uint16_t count = memory.load16(table + 8u);
    std::uint32_t lower = ~std::uint32_t(0);
    std::uint32_t upper = count;
    do {
        const std::uint32_t mid = static_cast<std::uint32_t>(
            std::bit_cast<std::int32_t>(lower + upper) >> 1);
        const std::uint64_t row_key =
            memory.load64(table + 16u + stride * mid);
        if (row_key == key) {
            // Sign-extend the 32-bit index into 64-bit bits.
            return static_cast<std::uint64_t>(
                static_cast<std::int64_t>(std::bit_cast<std::int32_t>(mid)));
        }
        if (key < row_key) {
            upper = mid;
        } else {
            lower = mid;
        }
    } while (lower + 1 != upper);
    return ~std::uint64_t(0);
}

// Resolves the table, then the row index; returns 0 for not found. The table
// is re-resolved after the index lookup, matching the original call sequence.
std::uint32_t FUN_002315d8(catalog_memory& memory, std::uint32_t handle,
                          std::uint32_t selector, std::uint64_t key) {
    std::uint32_t table = FUN_00231548(memory, handle, selector);
    const std::uint64_t index_bits = FUN_002316e8(memory, table, key);
    if (index_bits == ~std::uint64_t(0)) {
        return 0;
    }
    table = FUN_00231548(memory, handle, selector);
    const std::uint16_t stride = memory.load16(table + 10u);
    return table + 16u + static_cast<std::uint32_t>(index_bits) * stride;
}

// GP-relative global predicate; the mode is deliberately unnamed.
bool FUN_00231680(catalog_memory& memory, std::uint32_t gp) {
    return memory.load32(gp - 18968u) == 0;
}

// Preserves the caller's missing-row read at offset 0xec; no invented
// fallback. The mode branch multiplies the raw bits by 100 (not a percentage).
// Mode branches and low-32-bit truncation have separate original-function
// differential fixtures; their presence is not a semantic name for the mode.
std::int64_t FUN_00237bc0(catalog_memory& memory, std::uint32_t record_plus_10,
                         std::uint32_t gp) {
    const std::uint64_t key = memory.load64(record_plus_10);
    const std::uint32_t row =
        FUN_002315d8(memory, record_plus_10 + 464u, 30u, key);
    std::uint32_t bits = memory.load32(row + 236u);
    if (FUN_00231680(memory, gp)) {
        bits *= 100u;
    }
    return static_cast<std::int64_t>(std::bit_cast<std::int32_t>(bits));
}

// Transports the float32 bits returned by the post-debit boundary; no host
// arithmetic or invented interpretation of record field 0x208.
void FUN_001d9ce8(post_debit_boundary& dep, std::uint32_t subrecord) {
    const std::uint32_t bits = dep.FUN_001dac48(0x2d2b00u);
    dep.store32(subrecord + 4u, bits);
}

// Forwards to FUN_001d9ce8.
void FUN_001d9f60(post_debit_boundary& dep, std::uint32_t subrecord) {
    FUN_001d9ce8(dep, subrecord);
}

}  // namespace gt3::economy_recovery
