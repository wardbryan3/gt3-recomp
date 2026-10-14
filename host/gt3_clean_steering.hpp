#pragma once
#include "ps2/cpu.hpp"
#include <cstddef>
#include <cstdint>

// GT3 USA v1.10 only. Addresses and evidence ledger: docs/gt3-clean-steering.md.
namespace gt3::clean {
// Floating fields store EE bit patterns, not host arithmetic values.
using EeFloat = std::uint32_t;
struct Command {
    std::uint8_t analog_flags, steering_mode;
    std::int8_t shift;
    std::uint8_t unknown03;
    std::int16_t steering, opposing_pressure, accelerator, brake, auxiliary, handbrake;
};
struct InputPartial {
    std::byte unknown00[0x14];
    std::uint32_t type_bits;
    std::byte unknown18[0x14];
    std::uint32_t digital_mask;
    std::byte unknown30[8];
    std::uint32_t channels[32];
    std::byte unknownb8[8];
    std::uint32_t vtable;
};
struct CarPartial {
    std::byte unknown00[0x68];
    EeFloat mechanical_limit;
    std::byte unknown6c[0xec0 - 0x6c];
    EeFloat dt;
    std::byte unknownec4[0x136d - 0xec4];
    std::int8_t control_kind136d, unknown136e, wheel_policy;
    std::byte unknown1370[0x13a0 - 0x1370];
    EeFloat steering, unknown13a4, steering_rate;
    std::byte unknown13ac[0x1420 - 0x13ac];
    EeFloat envelope_ratio;
    std::byte unknown1424[8];
    EeFloat negative_limit, positive_limit;
    std::byte unknown1434[0x16a4 - 0x1434];
    std::int16_t wheel_command, previous_wheel_command;
};
static_assert(sizeof(Command) == 16 && offsetof(Command, steering) == 4 &&
              offsetof(Command, accelerator) == 8);
static_assert(offsetof(InputPartial, digital_mask) == 0x2c &&
              offsetof(InputPartial, channels) == 0x38 && offsetof(InputPartial, vtable) == 0xc0);
static_assert(offsetof(CarPartial, mechanical_limit) == 0x68 && offsetof(CarPartial, dt) == 0xec0);
static_assert(offsetof(CarPartial, wheel_policy) == 0x136f &&
              offsetof(CarPartial, steering) == 0x13a0);
static_assert(offsetof(CarPartial, steering_rate) == 0x13a8 &&
              offsetof(CarPartial, envelope_ratio) == 0x1420);
static_assert(offsetof(CarPartial, negative_limit) == 0x142c &&
              offsetof(CarPartial, positive_limit) == 0x1430);
static_assert(offsetof(CarPartial, wheel_command) == 0x16a4 && sizeof(CarPartial) == 0x16a8);
struct Constants {
    EeFloat spring, damping, return_spring, limit_slew;
    EeFloat policy1[2], policy2[2];
    EeFloat digital_outward[3], digital_return[3], analog_rate[3];
};
struct Cost {
    unsigned instructions = 0;
    void add(unsigned n) { instructions += n; }
};
std::int32_t normalize_mapped_channel(std::uint32_t channel, std::uint32_t raw,
                                      std::int32_t sensitivity, const std::uint8_t *curve,
                                      Cost &cost);
void build_wheel_command(const InputPartial &input, Command &command, Cost &cost);
EeFloat slew_limit(EeFloat current, EeFloat target, EeFloat step, Cost &cost);
void filter_stick(CarPartial &car, EeFloat target, EeFloat outward_rate, EeFloat return_rate,
                  const Constants &constants, Cost &cost);
// Original prefix supplies curve result, averaged wheel quantity and classification.
// This is NOT a replacement for the pedal/control tail of 0x001E4478.
bool process_steering(CarPartial &car, const Command &command, std::uint8_t &steering_kind,
                      EeFloat curve_limit, EeFloat averaged_wheel_quantity, unsigned classification,
                      const Constants &constants, Cost &cost);
bool profile_matches();
extern bool enabled;
struct Counts {
    std::uint64_t normalized = 0, wheel_commands = 0, filters = 0, envelopes = 0;
};
extern Counts counts;
// Called only by the isolated generated copy. Returns false for unsupported input vtables.
bool replace(ps2::Cpu &cpu, std::uint32_t address);
} // namespace gt3::clean
