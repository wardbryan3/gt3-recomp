#pragma once
#include <cstddef>
#include <cstdint>
namespace ps2 { struct Cpu; }
namespace gt3::transmission {
// USA v1.10 MT selector ONLY: 001E5458..001E553B. Not a host controller.
// Partial views describe reads; opaque storage must never be bulk-written.
struct Requests { std::int8_t auxiliary, relative; };
struct CarPartial {
    std::byte unknown0000[0x20a];
    std::uint8_t maximum_index;
    std::byte unknown020b[0x13ac-0x20b];
    std::uint32_t accelerator_bits;
    std::byte unknown13b0[0x13ba-0x13b0];
    std::uint8_t selected_index;
    std::byte unknown13bb[3];
    std::uint8_t inhibition;
    std::byte unknown13bf[0x140c-0x13bf];
    std::uint32_t longitudinal_bits;
};
static_assert(sizeof(Requests)==2);
static_assert(offsetof(CarPartial,maximum_index)==0x20a);
static_assert(offsetof(CarPartial,accelerator_bits)==0x13ac);
static_assert(offsetof(CarPartial,selected_index)==0x13ba);
static_assert(offsetof(CarPartial,inhibition)==0x13be);
static_assert(offsetof(CarPartial,longitudinal_bits)==0x140c && sizeof(CarPartial)==0x1410);
struct Counts { std::uint64_t replaced=0, fallback=0, original_speed_calls=0; };
extern Counts counts;
extern bool enabled; // runtime default OFF; disposable validation overlay only
bool profile_matches();
// Complete native CPU/RAM/cost bridge, returns false BEFORE mutation on rejection.
// Result is original v0 (signed -1=no change), not an index committed here.
// Original 001E4E80 remains generated on the reverse-to-forward speed path.
bool replace_manual_selector(ps2::Cpu &, unsigned depth);
}
