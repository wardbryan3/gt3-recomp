#pragma once
// Version/profile fingerprints only, not original tables or code.
#include <cstdint>
namespace gt3::extensions::vt {
struct Span {unsigned at,size;};
inline constexpr Span calibration_spans[]={{0x1d4,4},{0x208,4},{0x234,4},{0x244,28},{0x284,8},{0x2a4,4},{0x2bc,4}};
inline constexpr std::uint64_t calibration_hash=0x93368536b85ba0fcull;
struct Code {unsigned at,size;std::uint64_t hash;};
inline constexpr Code code_profile[]={{0x1e6d48,384,0xc7c63d5513981e62ull},{0x1e5690,216,0x6a00840565cd9961ull},{0x1e77e0,104,0x49e9c391e13204cull},{0x1e4e78,8,0xf69e524f2a33a4cbull},{0x1e6c28,216,0x2a3eee9640d15f42ull},{0x1e7500,736,0xf518aacd69b18d17ull},{0x1e5b98,4240,0x3b6760a6fba82846ull}};
inline constexpr std::uint64_t startup_hashes[]={0x5d4d22338389c01eull,0x166e0eeaa29ee2f5ull,0xe54bdca4bd202084ull,0x64996d60be781ac2ull,0x1bf0f7a9c1624dacull};
}
