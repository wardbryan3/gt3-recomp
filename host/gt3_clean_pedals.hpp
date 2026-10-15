#pragma once
#include "ps2/cpu.hpp"
#include <cstddef>
#include <cstdint>
namespace gt3::pedals {
// USA v1.10 partial views, not full object definitions. EE floats are raw bits.
struct CommandPartial {
    std::uint8_t flags, mode;
    std::byte unknown02[6];
    std::uint16_t accelerator;
    std::int16_t brake;
    std::uint16_t auxiliary;
    std::byte unknown0e[2];
};
struct ControlPartial {
    std::uint8_t auxiliary_active;
    std::byte unknown01;
    std::uint8_t accelerator_history;
    std::byte unknown03;
};
struct CarPartial {
    std::byte unknown0000[0x1304];
    ControlPartial control;
    std::byte unknown1308[0x65];
    std::int8_t control_kind;
    std::byte unknown136e[0x3e];
    std::uint32_t processed_accelerator, processed_brake;
    std::byte unknown13b4[0x31];
    std::uint8_t numeric_policy;
    std::byte unknown13e6[0xd2];
    std::uint8_t policy_suppression;
    std::byte unknown14b9;
    std::uint16_t auxiliary_suppression;
};
static_assert(sizeof(CommandPartial)==16 && offsetof(CommandPartial,accelerator)==8 &&
              offsetof(CommandPartial,brake)==10 && offsetof(CommandPartial,auxiliary)==12);
static_assert(sizeof(ControlPartial)==4 && offsetof(ControlPartial,accelerator_history)==2);
static_assert(sizeof(CarPartial)==0x14bc && offsetof(CarPartial,control)==0x1304 &&
              offsetof(CarPartial,control_kind)==0x136d && offsetof(CarPartial,processed_accelerator)==0x13ac &&
              offsetof(CarPartial,processed_brake)==0x13b0 && offsetof(CarPartial,numeric_policy)==0x13e5 &&
              offsetof(CarPartial,policy_suppression)==0x14b8 && offsetof(CarPartial,auxiliary_suppression)==0x14ba);
// Only a validation translation may call this bridge. No canonical dispatcher hook.
extern bool enabled;
struct Counts { std::uint64_t replaced{}, fallback{}, response_calls{}; };
extern Counts counts;
bool profile_matches();
bool replace(ps2::Cpu &, unsigned depth=0);
} // namespace gt3::pedals
