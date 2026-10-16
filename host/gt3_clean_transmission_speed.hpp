#pragma once
#include <cstddef>
#include <cstdint>
namespace ps2 { struct Cpu; }
namespace gt3::transmission_speed {
// Whole USA v1.10 001E4E80..001E4F0F. A search, NOT a selection commit.
// Partial read span only: invalid maxima can address later object words. The
// 255-word bound is NOT evidence of an original 255-ratio physical table.
struct ObjectReadSpan {
    std::byte unknown0000[0x20a];
    std::uint8_t maximum_index;
    std::byte unknown020b[0x236-0x20b];
    std::uint16_t upper_rate_bound;
    std::byte unknown0238[0x264-0x238];
    std::uint32_t possible_ratio_words[255];
};
static_assert(offsetof(ObjectReadSpan,maximum_index)==0x20a);
static_assert(offsetof(ObjectReadSpan,upper_rate_bound)==0x236);
static_assert(offsetof(ObjectReadSpan,possible_ratio_words)==0x264);
static_assert(sizeof(ObjectReadSpan)==0x660);
struct Counts { std::uint64_t replaced=0, fallback=0; };
extern Counts counts;
extern bool enabled; // Runtime default OFF; never installed in canonical ps2run.
bool profile_matches();
// a0=original object, f12=original EE speed bits; v0=result index.
// No RAM writes. All outgoing CPU/FCR/scratch/cost effects preserved.
// Low looping budgets reject BEFORE mutation; original owns all poll/resume paths.
bool replace(ps2::Cpu &);
}
