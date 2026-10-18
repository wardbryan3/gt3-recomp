#include "gt3_garage.hpp"
#include <bit>

namespace gt3::economy_recovery {
std::uint32_t FUN_00218f88(garage_memory& memory, std::uint32_t base) {
    // Original unit_0046: first zero occupancy word, not a heap allocation.
    for (std::uint32_t i = 0; i < garage_pool_count; ++i) {
        const auto record = base + garage_pool_offset + i * garage_record_stride;
        if (memory.load32(record + record_field_228) == 0) return record;
    }
    return 0;
}

std::uint64_t FUN_0023c4a8(garage_memory& memory, std::uint32_t collection,
                          std::uint32_t record) {
    auto node = memory.load32(collection);
    std::uint32_t index = 0;
    while (node != 0) {
        if (node == record)
            return std::bit_cast<std::uint64_t>(static_cast<std::int64_t>(
                std::bit_cast<std::int32_t>(index)));
        node = memory.load32(node);
        index += 1u;
    }
    return ~std::uint64_t{0};
}

void FUN_00218fe0(garage_memory& memory, std::uint32_t base, std::uint32_t record) {
    memory.store32(record + record_field_22c, memory.load32(base + 0x2cu));
    memory.store32(base + 0x2cu, memory.load32(base + 0x2cu) + 1u);
    FUN_0023c1b8(memory, base + garage_collection_offset, record);
    const auto count = memory.load32(base + 0x38u);
    // Original reads +0x30 before publishing the incremented count. Keep this
    // sequence even when an ordinary-RAM backend would produce the same values.
    const auto field_30 = memory.load32(base + 0x30u);
    memory.store32(base + 0x38u, count + 1u);
    if (std::bit_cast<std::int32_t>(field_30) >= 0)
        memory.store32(base + 0x30u, field_30 + 1u);
}

void FUN_0023af40(garage_boundary& boundary, std::uint32_t record) {
    // The external reset remains opaque. In particular, do not bulk-erase the
    // record or replace that reset with our observed normal-path byte pattern.
    boundary.FUN_00237980(record + 0x10u);
    boundary.store32(record + record_field_228, 0);
    boundary.store32(record + record_field_22c, 0xffffffffu);
}

void FUN_00219190(garage_boundary& boundary, std::uint32_t base, std::uint32_t record) {
    if (record == 0) return;
    const auto index_bits = FUN_0023c4a8(boundary, base + garage_collection_offset, record);
    auto field_30 = boundary.load32(base + 0x30u);
    const auto signed_field = static_cast<std::int64_t>(std::bit_cast<std::int32_t>(field_30));
    if (index_bits == std::bit_cast<std::uint64_t>(signed_field)) {
        field_30 = 0xffffffffu;
        boundary.store32(base + 0x30u, field_30);
    } else if (std::bit_cast<std::int64_t>(index_bits) < signed_field) {
        field_30 -= 1u;
        boundary.store32(base + 0x30u, field_30);
    }
    boundary.store32(base + 0x34u, field_30);
    FUN_0023c288(boundary, base + garage_collection_offset, record);
    boundary.store32(base + 0x38u, boundary.load32(base + 0x38u) - 1u);
    for (std::uint32_t i = 0; i < garage_pool_count; ++i) {
        if (base + garage_pool_offset + i * garage_record_stride == record) {
            FUN_0023af40(boundary, record);
            break;
        }
    }
}
}
