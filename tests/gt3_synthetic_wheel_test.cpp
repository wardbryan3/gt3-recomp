#include "gt3_synthetic_wheel.hpp"
#include "gt3_controls.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <bit>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <limits>
void register_generated_code();
namespace {
constexpr unsigned car = 0x600000, input = 0x501000, command = 0x502000;
void require(bool ok, const char *what) { if (!ok) { std::fprintf(stderr, "FAIL synthetic wheel: %s\n", what); std::exit(1); } }
void clear(unsigned at, unsigned n) { for (unsigned i = 0; i < n; ++i) ps2::st8(at + i, 0); }
void sf(unsigned at, float v) { ps2::st32(at, std::bit_cast<unsigned>(v)); }
float lf(unsigned at) { return std::bit_cast<float>(ps2::ld32(at)); }
void guest_call(ps2::Cpu &c, unsigned pc, unsigned a0, unsigned a1 = 0, unsigned a2 = 0) {
    c.r[4].d[0] = a0; c.r[5].d[0] = a1; c.r[6].d[0] = a2;
    c.r[28].d[0] = 0x3579f0; c.r[29].d[0] = 0x800000; c.r[31].d[0] = 0x1000000;
    c.budget = 1000000;
    ps2::call(c, pc, 0);
    require(c.pc == 0x1000000 && c.r[29].w[0] == 0x800000, "generated return/stack");
}
}
int main(int argc, char **argv) {
    require(argc == 2, "requires original core.elf");
    using namespace gt3::synthetic;
    double parsed;
    for (auto s : {"-1", "-0.5", "-0.25", "0", "+0.25", "+0.5", "+1"}) require(parse_value(s, parsed), "valid value");
    for (auto s : {"", "nan", "inf", "-inf", "1.01", "-1.01", "0.5junk", "1e9999"}) require(!parse_value(s, parsed), "invalid value rejected");
    Event event;
    require(parse_event("5000:+0.5", event) && event.frame == 5000 && event.value == 0.5, "scheduled value");
    for (auto s : {"-1:0", "1:", "x:0", "1:nan", "1:2", "18446744073709551616:0"}) require(!parse_event(s, event), "invalid event rejected");
    require(axis_for_value(std::numeric_limits<double>::quiet_NaN()) == -1 && axis_for_value(2) == -1, "adapter rejects invalid domain");
    for (int i = -4096; i <= 4096; ++i) {
        const double v = i / 4096.0;
        const int axis = axis_for_value(v), q = gt3::wheel_steering_command(axis);
        require(axis >= 0 && axis <= 1023 && std::abs(q / 4096.0 - v) <= 4.5 / 4096.0, "quantization bound");
    }
    register_generated_code();
    unsigned entry;
    require(ps2::load_elf(argv[1], entry) && profile_matches(), "ELF steering profile");
    const unsigned saved_opcode = ps2::ld32(0x2107b0);
    ps2::st32(0x2107b0, 0); require(!profile_matches(), "wrong profile rejected"); ps2::st32(0x2107b0, saved_opcode);
    unsigned checked = 0;
    for (double value : {-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0})
        for (unsigned pad : {0u, 8u}) for (unsigned mask : {0u, 0x400u, 0xfc00u}) {
            clear(car, 0x1800); clear(input, 0x150);
            ps2::st32(car + 12, input); ps2::st32(input + 0xc0, 0x33f7e0);
            ps2::st32(input + 0x14, 0x100 | pad); ps2::st32(input + 0x2c, mask);
            for (unsigned i = 0; i < 32; ++i) ps2::st32(input + 0x38 + i * 4, 0xa50000 + i);
            std::array<unsigned char, 0x150> before_input{};
            std::array<unsigned char, 16> before_command{};
            for (unsigned i = 0; i < before_input.size(); ++i) before_input[i] = ps2::ld8(input + i);
            for (unsigned i = 0; i < 16; ++i) ps2::st8(command + i, before_command[i] = 0x20 + i);
            Options options; options.enabled = true; options.value = value;
            Experiment experiment(options);
            ps2::g_options.on_probe = [&](ps2::Cpu &cpu, unsigned pc) { experiment.probe(cpu, pc, 10); };
            ps2::Cpu c{}; c.r[4].d[0] = car;
            experiment.probe(c, 0x1e4d38, 10);
            c.r[16].d[0] = input; c.r[17].d[0] = command;
            experiment.probe(c, 0x2107ac, 10);
            require((ps2::ld32(input + 0x14) & 0xe0) == 0x20, "wheel type enabled");
            guest_call(c, 0x2115f8, input, command);
            experiment.probe(c, 0x2107b8, 10);
            for (unsigned i = 0; i < before_input.size(); ++i) require(ps2::ld8(input + i) == before_input[i], "all input state restored");
            for (unsigned i = 0; i < 16; ++i) if (i != 0 && i != 1 && i != 4 && i != 5)
                require(ps2::ld8(command + i) == before_command[i], "nonsteering command untouched");
            const int q = gt3::wheel_steering_command(axis_for_value(value));
            require(ps2::ld8(command) == (before_command[0] | 1) && ps2::ld8(command + 1) == 4 &&
                std::int16_t(ps2::ld16(command + 4)) == q, "original wheel command");
            // Original mode-4 policy 4, not a replacement: actual generated routines.
            ps2::st32(car + 4, 0x700000); clear(0x700000, 0xb800);
            ps2::st16(car + 0xa8, 2); ps2::st32(car + 0xac, 0x710000); ps2::st32(car + 0xb0, 0x710008);
            sf(0x710000, 0); sf(0x710004, 100); sf(0x710008, 0.5); sf(0x71000c, 0.5);
            sf(car + 0x68, 0.5); sf(car + 0xec0, 1.0f / 60); ps2::st8(car + 0x136f, 4);
            sf(car + 0x13a8, 7); sf(car + 0x120, 1); sf(car + 0x124, 0.75);
            guest_call(c, 0x1e4478, car, command, car + 0x1304);
            const float expected = 0.5f * (q / 4096.0f);
            require(std::abs(lf(car + 0x13a0) - expected) < 2e-6 && lf(car + 0x13a8) == 7, "generated mode4 steering");
            guest_call(c, 0x1e8978, car);
            require(std::abs(lf(car + 0xff0) - expected * (expected < 0 ? 0.75f : 1)) < 2e-6, "generated wheel consumer");
            ++checked;
        }
    // Off, AI, stale context and wrong vtable must not write input or command.
    for (unsigned scenario = 0; scenario < 4; ++scenario) {
        clear(car, 0x1800); clear(input, 0x150); clear(command, 16);
        ps2::st32(car + 12, input); ps2::st32(input + 0xc0, scenario == 3 ? 0 : 0x33f7e0);
        if (scenario == 1) ps2::st8(car + 0x136d, 2);
        Options options; options.enabled = scenario != 0; options.value = 0.5;
        Experiment experiment(options); ps2::Cpu c{}; c.r[4].d[0] = car;
        experiment.probe(c, 0x1e4d38, 0);
        if (scenario == 2) experiment.probe(c, 0x1e4d5c, 0);
        c.r[16].d[0] = input; c.r[17].d[0] = command;
        experiment.probe(c, 0x2107ac, 0); experiment.probe(c, 0x2107b8, 0);
        require(ps2::ld32(input + 0x14) == 0 && ps2::ld32(input + 0x38) == 0 && ps2::ld32(command) == 0, "off/scope/vtable guard");
    }
    // Scheduled transitions, including return to center.
    Options options; options.enabled = true; options.events = {{20, 0.5}, {30, -0.5}, {40, 0}};
    Experiment experiment(options); clear(car, 0x1800); clear(input, 0x150);
    ps2::st32(car + 12, input); ps2::st32(input + 0xc0, 0x33f7e0);
    ps2::g_options.on_probe = [](ps2::Cpu &, unsigned) {};
    for (unsigned frame : {19u, 20u, 29u, 30u, 39u, 40u}) {
        ps2::Cpu c{}; c.r[4].d[0] = car; experiment.probe(c, 0x1e4d38, frame);
        c.r[16].d[0] = input; c.r[17].d[0] = command;
        experiment.probe(c, 0x2107ac, frame); guest_call(c, 0x2115f8, input, command);
        experiment.probe(c, 0x2107b8, frame);
        const double value = frame < 20 || frame >= 40 ? 0 : frame < 30 ? 0.5 : -0.5;
        require(std::int16_t(ps2::ld16(command + 4)) == gt3::wheel_steering_command(axis_for_value(value)), "scheduled transition");
    }
    std::printf("GT3 synthetic wheel adapter PASS: 8193 quantization values, %u native integrations, guards/parser/schedule\n", checked);
}
