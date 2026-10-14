#pragma once
#include <algorithm>
#include <array>
#include <cstdint>
#include <stdexcept>

namespace gt3 {
// Selective decompilation of PBPX-95503 v1.10 EE routine 0x00210F90.
// This helper normalizes a mapped input. Action names belong to its callers.
inline std::uint32_t normalize_mapped_input(std::uint32_t channel_code,
                                           std::uint32_t raw_value,
                                           std::uint32_t sensitivity_percent,
                                           const std::array<std::uint8_t, 256> &response_curve) {
    if ((channel_code & 0xffu) < 4u) {
        const std::uint32_t curved_value = response_curve[raw_value & 0xffu];
        switch (channel_code & 0x300u) {
        case 0x100u: return std::uint32_t(std::max(0, (128 - int(curved_value)) * 2));
        case 0x200u: return std::uint32_t(std::max(0, (int(curved_value) - 128) * 2));
        default: return curved_value;
        }
    }
    if (!sensitivity_percent) throw std::invalid_argument("zero input sensitivity");
    const std::uint32_t doubled_pressure = std::min((raw_value & 0xffu) * 2u, 256u);
    return std::min(doubled_pressure * 100u / sensitivity_percent, 256u);
}
}
