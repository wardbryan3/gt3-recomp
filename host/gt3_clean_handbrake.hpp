#pragma once
#include <cstddef>
#include <cstdint>
namespace ps2 { struct Cpu; }
namespace gt3::handbrake {
using Bits = std::uint32_t; // EE bit pattern, not a host float.
// Independent partial views; opaque bytes have no inferred meaning or write API.
struct CommandPartial {
    std::uint8_t flags;
    std::byte unknown01[13];
    std::int16_t handbrake;
};
struct CarPartial {
    std::byte unknown0000[0x13b4];
    Bits processed_handbrake;
};
static_assert(sizeof(CommandPartial)==16 && offsetof(CommandPartial,handbrake)==14);
static_assert(sizeof(CarPartial)==0x13b8 && offsetof(CarPartial,processed_handbrake)==0x13b4);
struct Calibration { Bits rise, fall, floor; };
// Arithmetic + outgoing scratch contract of interior region 001E4BB8..001E4C5F.
// No producer, steering, pedal, coupling, shift or wheel physics substitution.
struct Result {
    Bits value, f0, f1, f2;
    std::uint32_t v0, at;
    unsigned cost;
    bool condition, writes_at;
};
Result process(std::uint8_t flags, std::int16_t input, Bits previous, Calibration);
bool profile_matches();
extern bool enabled; // runtime default OFF; only disposable validation unit calls replace
struct Counts { std::uint64_t replaced=0, fallback=0, depth_boundary=0; };
extern Counts counts;
bool replace(ps2::Cpu &, unsigned depth);
} // namespace gt3::handbrake
