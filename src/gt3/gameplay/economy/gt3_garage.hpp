#pragma once
#include <cstdint>

// USA v1.10 memory-native mechanisms, not Cpu/ABI replacements. Addresses are
// 32-bit guest addresses; addition and stored integer updates wrap. The memory
// binding must provide the original address mapping. No product binds this API.
namespace gt3::economy_recovery {
inline constexpr std::uint32_t garage_pool_offset = 0x138;
inline constexpr std::uint32_t garage_record_stride = 0x230;
inline constexpr std::uint32_t garage_pool_count = 200;
inline constexpr std::uint32_t garage_collection_offset = 0x1b6b8;
inline constexpr std::uint32_t record_field_228 = 0x228;
inline constexpr std::uint32_t record_field_22c = 0x22c;

struct garage_memory {
    virtual ~garage_memory() = default;
    virtual std::uint32_t load32(std::uint32_t address) = 0;
    virtual void store32(std::uint32_t address, std::uint32_t bits) = 0;
};
struct garage_boundary : garage_memory {
    // Unrecovered configuration reset. It may mutate memory. Tests distinguish
    // bounded boundary comparisons from executing the original callee.
    virtual void FUN_00237980(std::uint32_t record_plus_10) = 0;
};

std::uint32_t FUN_00218f88(garage_memory&, std::uint32_t base);
// The list's two endpoint pointers and the record's embedded links are retained.
// Insertion does NOT initialize every link: callers supply a detached node.
std::uint32_t FUN_0023c1b8(garage_memory&, std::uint32_t collection,
                          std::uint32_t record);
std::uint32_t FUN_0023c288(garage_memory&, std::uint32_t collection,
                          std::uint32_t record);
// Index query returns the sign-extended 32-bit index, or all-one bits for -1.
std::uint64_t FUN_0023c4a8(garage_memory&, std::uint32_t collection,
                          std::uint32_t record);
void FUN_00218fe0(garage_memory&, std::uint32_t base, std::uint32_t record);
// Reset delegates the configuration reset; it does not erase the model key.
void FUN_0023af40(garage_boundary&, std::uint32_t record);
void FUN_00219190(garage_boundary&, std::uint32_t base, std::uint32_t record);
}
