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
            for (unsigned sensitivity : {35u, 65u, 90u, 100u})
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
}
