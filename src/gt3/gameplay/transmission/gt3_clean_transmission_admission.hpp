#pragma once
#include "ps2/cpu.hpp"
#include <cstdint>
#include <cstddef>
namespace gt3::transmission_admission {
// Partial view for the mapped state fields; not the original complete car type.
struct CarTransitionPartial {
    std::byte before_samples[0x1310];
    std::uint32_t saved_engine, saved_target;
    std::byte before_candidate[0x139c-0x1318];
    std::uint32_t candidate;
    std::byte before_selection[0x13ba-0x13a0];
    std::uint8_t selected, state;
    std::byte before_inhibition[2];
    std::uint8_t inhibition;
    std::byte before_engine[0x13cc-0x13bf];
    std::uint32_t engine;
    std::byte before_rpm[0x1414-0x13d0];
    std::int16_t sampled_rpm;
    std::byte before_effective_accelerator[0x1428-0x1416];
    std::uint32_t effective_accelerator;
};
static_assert(offsetof(CarTransitionPartial,saved_engine)==0x1310);
static_assert(offsetof(CarTransitionPartial,saved_target)==0x1314);
static_assert(offsetof(CarTransitionPartial,candidate)==0x139c);
static_assert(offsetof(CarTransitionPartial,selected)==0x13ba);
static_assert(offsetof(CarTransitionPartial,state)==0x13bb);
static_assert(offsetof(CarTransitionPartial,inhibition)==0x13be);
static_assert(offsetof(CarTransitionPartial,engine)==0x13cc);
static_assert(offsetof(CarTransitionPartial,sampled_rpm)==0x1414);
static_assert(offsetof(CarTransitionPartial,effective_accelerator)==0x1428);
static_assert(sizeof(CarTransitionPartial)==0x142c);
// Whole 001E6D48..001E6EC7 only. Original target-rate helper remains original.
extern bool enabled;
struct Counts { std::uint64_t replaced=0, fallback=0; };
extern Counts counts;
bool profile_matches();
bool replace(ps2::Cpu &, unsigned depth);
}
