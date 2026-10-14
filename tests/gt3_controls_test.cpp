#include "gt3_controls.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
void register_generated_code();
int main() {
    register_generated_code();
    unsigned checked = 0;
    for (unsigned curve_kind : {0u, 1u}) {
        std::array<std::uint8_t, 256> curve{};
        for (unsigned i = 0; i < 256; ++i) {
            curve[i] = curve_kind ? std::uint8_t(255-i) : std::uint8_t(i);
            ps2::st8(0x003416f8u+i, curve[i]);
        }
        for (unsigned channel : {0u, 1u, 2u, 3u, 0x100u, 0x200u, 0x300u, 4u, 14u, 15u})
            for (unsigned sensitivity : {20u, 35u, 65u, 90u, 100u})
                for (unsigned raw = 0; raw < 256; ++raw) {
                    ps2::Cpu cpu{};
                    cpu.budget = 1000000;
                    cpu.r[4].d[0] = channel; cpu.r[5].d[0] = raw; cpu.r[6].d[0] = sensitivity;
                    cpu.r[31].d[0] = 0x01000000;
                    cpu.pc = 0x00210f90;
                    ps2::call(cpu, cpu.pc, 0);
                    const unsigned expected = gt3::normalize_mapped_input(channel, raw, sensitivity, curve);
                    if (cpu.r[2].w[0] != expected || cpu.pc != 0x01000000) {
                        std::fprintf(stderr,"FAIL channel=%x raw=%u sensitivity=%u native=%u readable=%u pc=%x\n",channel,raw,sensitivity,cpu.r[2].w[0],expected,cpu.pc);
                        return 1;
                    }
                    ++checked;
                }
    }
    std::printf("GT3 control normalization differential PASS: %u cases\n", checked);

    constexpr unsigned input_address = 0x00500000, mapping_address = 0x00600000;
    constexpr unsigned output_address = 0x00610000, stack_address = 0x00700000;
    constexpr std::array<std::int16_t, 14> codes{
        -1, -32768, 0, 1, 2, 3, 0x100, 0x201, 0x302, 4, 14, 15, 0xff, 0x704};
    std::array<std::uint32_t, 40> mapping{};
    std::array<gt3::BindingRecord, 14> bindings{};
    for (unsigned i = 0; i < mapping.size(); ++i) {
        mapping[i] = (i * 3u + 1u) % bindings.size();
        ps2::st32(mapping_address + i * 4u, mapping[i]);
    }
    unsigned actions_checked = 0;
    for (unsigned curve_kind : {0u, 1u}) {
        std::array<std::uint8_t, 256> curve{};
        for (unsigned i = 0; i < curve.size(); ++i) {
            curve[i] = curve_kind ? std::uint8_t((i * i + 17u) & 255u) : std::uint8_t(i);
            ps2::st8(0x003416f8u + i, curve[i]);
        }
        for (unsigned scenario = 0; scenario < codes.size(); ++scenario) {
            for (unsigned i = 0; i < bindings.size(); ++i) {
                bindings[i] = {std::int16_t(0x1234), codes[(i + scenario) % codes.size()],
                              codes[(i * 5u + scenario) % codes.size()]};
                ps2::st16(0x002e2cf8u + i * 6u, std::uint16_t(bindings[i].unknown));
                ps2::st16(0x002e2cfau + i * 6u, std::uint16_t(bindings[i].primary_channel));
                ps2::st16(0x002e2cfcu + i * 6u, std::uint16_t(bindings[i].secondary_channel));
            }
            for (unsigned raw = 0; raw < 256; ++raw) {
                std::array<std::uint32_t, 256> channels{};
                for (unsigned i = 0; i < channels.size(); ++i) {
                    // The normalization routine must ignore all but the low byte.
                    channels[i] = 0xa5a50000u | ((raw + i * 13u) & 255u);
                    ps2::st32(input_address + 0x38u + i * 4u, channels[i]);
                }
                for (unsigned bank : {0u, 1u}) for (unsigned variant : {0u, 1u})
                    for (auto field : {gt3::MappingField::primary, gt3::MappingField::secondary}) {
                        std::array<std::uint8_t, 16> output{};
                        for (unsigned i = 0; i < 32; ++i) {
                            const auto sentinel = std::uint8_t(0xa0u + i + (raw & 31u));
                            ps2::st8(output_address + i, sentinel);
                            if (i < output.size()) output[i] = sentinel;
                        }
                        gt3::fill_mapped_actions(channels, output, mapping.data(), bindings.data(),
                                                bank, variant, field, curve);
                        ps2::Cpu cpu{};
                        cpu.budget = 1000000;
                        cpu.r[4].d[0] = input_address;
                        cpu.r[5].d[0] = output_address;
                        cpu.r[6].d[0] = mapping_address;
                        cpu.r[7].d[0] = bank;
                        cpu.r[8].d[0] = variant; // EE fifth argument is t0, not the stack.
                        cpu.r[29].d[0] = stack_address;
                        cpu.r[31].d[0] = 0x01000000;
                        cpu.pc = field == gt3::MappingField::primary ? 0x00211050 : 0x002111c0;
                        const auto entry = cpu.pc;
                        ps2::call(cpu, cpu.pc, 0);
                        if (cpu.pc != 0x01000000 || cpu.r[29].w[0] != stack_address) {
                            std::fprintf(stderr, "FAIL action return/stack entry=%x pc=%x\n", entry, cpu.pc);
                            return 1;
                        }
                        for (unsigned i = 0; i < 32; ++i) {
                            const auto expected = i < output.size() ? output[i] :
                                std::uint8_t(0xa0u + i + (raw & 31u));
                            if (ps2::ld8(output_address + i) != expected) {
                                std::fprintf(stderr, "FAIL actions entry=%x curve=%u scenario=%u raw=%u bank=%u variant=%u byte=%u native=%u readable=%u\n",
                                    entry, curve_kind, scenario, raw, bank, variant, i,
                                    ps2::ld8(output_address + i), expected);
                                return 1;
                            }
                        }
                        ++actions_checked;
                    }
            }
        }
    }
    std::printf("GT3 mapped actions differential PASS: %u cases (including lookup chain and output guards)\n", actions_checked);
}
