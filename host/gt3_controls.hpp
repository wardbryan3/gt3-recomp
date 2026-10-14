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

// 0x00217998: bank stride 0x50, variant stride 0x28, action stride 4.
// The pointer must cover the selected bank/variant/action; dimensions are
// deliberately not inferred from these strides alone.
inline std::uint32_t binding_index(const std::uint32_t *mapping,
                                   unsigned bank, unsigned variant, unsigned action) {
    return mapping[bank * 20u + variant * 10u + action];
}

// Six-byte records at guest 0x002E2CF8. The first halfword's role is unknown.
struct BindingRecord {
    std::int16_t unknown;
    std::int16_t primary_channel;   // 0x002178C8, signed lh at +2
    std::int16_t secondary_channel; // 0x00217938, signed lh at +4
};
static_assert(sizeof(BindingRecord) == 6);
enum class MappingField { primary, secondary };

// 0x002115F8: wheel axis already resolved by the input object's virtual
// channel getter. No pad response curve or pad dead zone is applied here.
// This ordinary-integer reconstruction expects an axis in the tested 0..1023
// domain; that domain is a fixture, not a proven hardware report range.
inline std::int16_t wheel_steering_command(int axis) {
    return std::int16_t(std::clamp((512 - axis) * 9, -4096, 4096));
}

// 0x002115D8: inverted pedal with a caller-supplied threshold (75 or 80).
// Negative results are intentional: the caller writes only positive values,
// leaving a prior pad/digital command untouched otherwise. raw is 0..255.
inline int wheel_pedal_input(int raw, int threshold) {
    const int value = (255 - raw - threshold) * 2;
    return value > 255 ? 256 : value;
}

inline std::int16_t mapped_channel(const std::uint32_t *mapping,
                                   const BindingRecord *bindings, unsigned bank,
                                   unsigned variant, unsigned action, MappingField field) {
    const auto &binding = bindings[binding_index(mapping, bank, variant, action)];
    return field == MappingField::primary ? binding.primary_channel : binding.secondary_channel;
}

// Selective decompilation of 0x00211050 (primary) / 0x002111C0 (secondary).
// raw_channels corresponds to words at input-object +0x38. output is the
// first 16 bytes of the caller's block, not a declaration of its full layout.
// Negative mappings leave both flags and values intact; a zero *value* still
// sets the presence bit. Action labels remain numeric pending consumer RE.
inline void fill_mapped_actions(const std::array<std::uint32_t, 256> &raw_channels,
                                std::array<std::uint8_t, 16> &output,
                                const std::uint32_t *mapping, const BindingRecord *bindings,
                                unsigned bank, unsigned variant, MappingField field,
                                const std::array<std::uint8_t, 256> &response_curve) {
    for (unsigned action : {1u, 2u, 4u, 3u}) {
        const auto channel = mapped_channel(mapping, bindings, bank, variant, action, field);
        if (channel < 0) continue;
        const unsigned sensitivity = field == MappingField::primary ? 100u :
                                     action == 2u ? 65u : action == 4u ? 20u : 35u;
        const auto value = normalize_mapped_input(std::uint32_t(channel),
            raw_channels[unsigned(channel) & 0xffu], sensitivity, response_curve) << 4;
        output[0] |= std::uint8_t(1u << action);
        const unsigned offset = 6u + action * 2u;
        output[offset] = std::uint8_t(value);
        output[offset + 1u] = std::uint8_t(value >> 8);
    }
}
}
