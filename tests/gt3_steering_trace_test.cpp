#include "gt3_controls.hpp"
#include "ps2/generated.hpp"
#include <array>
#include "ps2/system.hpp"
#include <algorithm>
#include <bit>
#include <cmath>
#include <cstdio>
#include <cstdlib>

void register_generated_code();
namespace {
constexpr unsigned device = 0x00500000, input = 0x00501000, packet = 0x00502000;
constexpr unsigned mapping = 0x00503000, car = 0x00600000, race = 0x00700000;
constexpr unsigned knots = 0x00710000, stack = 0x00800000;
void store_float(unsigned address, float value) { ps2::st32(address, std::bit_cast<unsigned>(value)); }
float load_float(unsigned address) { return std::bit_cast<float>(ps2::ld32(address)); }
void clear(unsigned address, unsigned size) {
    for (unsigned i = 0; i < size; ++i) ps2::st8(address + i, 0);
}
void call(unsigned entry, unsigned a0, unsigned a1 = 0, unsigned a2 = 0,
          unsigned a3 = 0, unsigned t0 = 0) {
    ps2::Cpu cpu{};
    cpu.budget = 1000000;
    cpu.r[4].d[0] = a0; cpu.r[5].d[0] = a1; cpu.r[6].d[0] = a2;
    cpu.r[7].d[0] = a3; cpu.r[8].d[0] = t0;
    cpu.r[28].d[0] = 0x003579f0; // gp-0x5080 resolves to shipped constant 0x00352970.
    cpu.r[29].d[0] = stack; cpu.r[31].d[0] = 0x01000000;
    cpu.pc = entry;
    ps2::call(cpu, entry, 0);
    if (cpu.pc != 0x01000000 || cpu.r[29].w[0] != stack) {
        std::fprintf(stderr, "FAIL steering trace return entry=%x pc=%x\n", entry, cpu.pc);
        std::exit(1);
    }
}
void near(unsigned address, float expected, unsigned raw, unsigned frame) {
    const float actual = load_float(address);
    if (!std::isfinite(actual) || std::abs(actual - expected) > 2e-6f) {
        std::fprintf(stderr, "FAIL steering raw=%u frame=%u address=%x native=%.9g expected=%.9g\n",
                     raw, frame, address, actual, expected);
        std::exit(1);
    }
}
// Exercise the real virtual calls, using the shipped input vtable rather
// than substituting host hooks. Native getter 0x0022E000 resolves word channels.
void wheel_commands() {
    unsigned checked = 0;
    // Device-state adapter: three recognized packed identifier pairs, plus
    // an unrecognized pair. These are synthetic state objects, not USB reports.
    for (const auto &id : std::array<std::array<unsigned, 2>, 4>{{
             {0xc293046d, 1}, {0x000406f8, 2}, {0xc294046d, 3}, {0x12345678, 7}}}) {
        for (unsigned axis : {0u, 512u, 1023u}) {
            clear(device, 0x64); clear(input, 0x150);
            ps2::st32(device, 1); ps2::st32(device + 0x58, id[0]);
            ps2::st32(device + 0x24, axis);
            ps2::st32(device + 0x3c, 255); ps2::st32(device + 0x40, 255);
            call(0x00230d10, device, input);
            if (ps2::ld32(input + 0x14) != id[1] * 32 ||
                ps2::ld32(input + 0x38) != axis ||
                ps2::ld32(input + 0x3c) != 255 || ps2::ld32(input + 0x40) != 255) {
                std::fprintf(stderr, "FAIL wheel state adapter identifier=%x axis=%u\n", id[0], axis);
                std::exit(1);
            }
            ++checked;
        }
    }
    for (unsigned type = 0; type < 8; ++type) {
        for (unsigned pad_type : {0u, 8u}) {
            clear(input, 0x150);
            ps2::st32(input + 0xc0, 0x0033f7e0);
            ps2::st32(input + 0x14, (type << 5) | pad_type);
            const unsigned base = pad_type ? 16 : 0;
            for (unsigned axis = 0; axis < 1024; ++axis) {
                // Both banks present, intentionally different to catch bank selection.
                ps2::st32(input + 0x38, 1023 - axis);
                ps2::st32(input + 0x78, 1023 - axis);
                ps2::st32(input + 0x38 + base * 4, axis);
                ps2::st32(input + 0x3c + base * 4, 255);
                ps2::st32(input + 0x40 + base * 4, 255);
                call(0x001f4330, packet);
                ps2::st8(packet, 1); ps2::st8(packet + 1, 2);
                ps2::st16(packet + 4, 1472); // a preceding stick command
                call(0x002115f8, input, packet);
                const bool enabled = type >= 1 && type <= 3;
                const int expected = enabled ? gt3::wheel_steering_command(axis) : 1472;
                if (int(std::int16_t(ps2::ld16(packet + 4))) != expected ||
                    ps2::ld8(packet + 1) != (enabled ? 4u : 2u) || ps2::ld8(packet) != 1) {
                    std::fprintf(stderr, "FAIL wheel command type=%u pad=%u axis=%u\n", type, pad_type, axis);
                    std::exit(1);
                }
                ++checked;
            }
        }
    }
    // Pedal thresholds, analog precedence, digital fallbacks and no-write cases.
    for (unsigned type : {1u, 2u, 3u}) for (unsigned pad_type : {0u, 8u}) {
        clear(input, 0x150);
        ps2::st32(input + 0xc0, 0x0033f7e0);
        ps2::st32(input + 0x14, (type << 5) | pad_type);
        const unsigned base = pad_type ? 16 : 0;
        ps2::st32(input + 0x38 + base * 4, 512);
        for (unsigned raw = 0; raw < 256; ++raw) for (unsigned buttons : {0u, 0xfc00u}) {
            ps2::st32(input + 0x2c, buttons);
            ps2::st32(input + 0x3c + base * 4, raw);
            ps2::st32(input + 0x40 + base * 4, raw);
            call(0x001f4330, packet);
            ps2::st8(packet, 0x1e); // existing pad analog commands
            ps2::st16(packet + 8, 777); ps2::st16(packet + 10, 999);
            ps2::st16(packet + 12, 321); ps2::st16(packet + 14, 456);
            call(0x002115f8, input, packet);
            unsigned flags = buttons ? 1 : 0x1f;
            for (unsigned pedal = 0; pedal < 2; ++pedal) {
                const int value = gt3::wheel_pedal_input(raw, pedal ? 80 : 75);
                const unsigned expected = value > 0 ? unsigned(value * 16) :
                                          buttons ? 1 : pedal ? 999 : 777;
                if (value > 0) flags |= 2u << pedal;
                if (ps2::ld16(packet + 8 + pedal * 2) != expected) {
                    std::fprintf(stderr, "FAIL wheel pedal=%u raw=%u buttons=%x\n", pedal, raw, buttons);
                    std::exit(1);
                }
            }
            if (ps2::ld8(packet) != flags || ps2::ld8(packet + 2) != (buttons ? 255u : 0u) ||
                ps2::ld16(packet + 12) != (buttons ? 1u : 321u) ||
                ps2::ld16(packet + 14) != (buttons ? 1u : 456u)) {
                std::fprintf(stderr, "FAIL wheel digital fallback raw=%u buttons=%x\n", raw, buttons);
                std::exit(1);
            }
            ++checked;
        }
    }
    std::printf("GT3 wheel native virtual channels/override/pedals PASS: %u commands\n", checked);
}
void wheel_driving() {
    constexpr float dt = 1.0f / 60.0f, mechanical_limit = 0.5f;
    unsigned checked = 0;
    for (int policy : {-1, 0, 1, 2, 3, 4, 5}) for (unsigned classification : {0u, 1u}) {
        for (unsigned axis : {0u, 57u, 58u, 511u, 512u, 513u, 966u, 967u, 1023u}) {
            clear(input, 0x150); clear(car, 0x1800); clear(race, 0xb800);
            ps2::st32(input + 0xc0, 0x0033f7e0);
            ps2::st32(input + 0x14, 0x20);
            ps2::st32(input + 0x38, axis);
            ps2::st32(input + 0x3c, 255); ps2::st32(input + 0x40, 255);
            call(0x001f4330, packet);
            call(0x002115f8, input, packet);
            ps2::st32(car + 4, race);
            // Race value 2 produces classification 1; race value 0 produces 0.
            ps2::st8(race + 0xb7ad, classification ? 2 : 0);
            ps2::st8(car + 0x136f, std::uint8_t(policy));
            store_float(car + 0xec0, dt); store_float(car + 0x68, mechanical_limit);
            // Distinct constant descriptors: stick=.45, wheel=.10, special=.30.
            for (unsigned curve = 0; curve < 3; ++curve) {
                const unsigned descriptor = car + 0x6c + curve * 0x3c;
                const unsigned data = knots + curve * 16;
                const float limit = curve == 0 ? 0.45f : curve == 1 ? 0.10f : 0.30f;
                ps2::st16(descriptor, 2);
                ps2::st32(descriptor + 4, data); ps2::st32(descriptor + 8, data + 8);
                store_float(data, 0); store_float(data + 4, 100);
                store_float(data + 8, limit); store_float(data + 12, limit);
            }
            // Nonzero mean tests policy-dependent envelope widening.
            store_float(car + 0x105c, 0.4f); store_float(car + 0x1100, 0.4f);
            store_float(car + 0x1430, 0.45f); store_float(car + 0x142c, -0.45f);
            store_float(car + 0x13a0, -0.2f); store_float(car + 0x13a8, 7.0f);
            ps2::st16(car + 0x16a4, 123);
            store_float(car + 0x120, 1); store_float(car + 0x124, 0.75f);
            store_float(car + 0xe30, 0); store_float(car + 0xe34, 0.02f);
            float high = classification ? 0.30f : 0.10f;
            if (policy == 1 || policy == 3)
                high = std::max(high, load_float(classification ? 0x00352984 : 0x00352980));
            else if (policy == 2)
                high = std::max(high, load_float(classification ? 0x0035298c : 0x00352988));
            float low = -high;
            if (policy != 3 && policy != 4) high = std::max(high, 0.4f);
            high = std::min(high, mechanical_limit); low = std::max(low, -mechanical_limit);
            float high_state = 0.45f, low_state = -0.45f;
            const float step = load_float(0x0035297c) * dt;
            const int fixed = gt3::wheel_steering_command(axis);
            auto approach = [step](float state, float target) {
                return state < target ? std::min(state + step, target) : std::max(state - step, target);
            };
            for (unsigned frame = 1; frame <= 60; ++frame) {
                call(0x001e4478, car, packet, car + 0x1304);
                float steering = 0;
                if (policy >= 0 && policy < 4) {
                    high_state = approach(high_state, high); low_state = approach(low_state, low);
                    steering = (fixed >= 0 ? high_state : -low_state) * (float(fixed) / 4096.0f);
                } else if (policy == 4) steering = mechanical_limit * (float(fixed) / 4096.0f);
                near(car + 0x13a0, steering, axis, frame);
                near(car + 0x13a8, 7, axis, frame); // no call to the stick filter
                near(car + 0x1430, high_state, axis, frame);
                near(car + 0x142c, low_state, axis, frame);
                if (ps2::ld8(car + 0x1307) != 0 ||
                    ps2::ld16(car + 0x16a4) != std::uint16_t(fixed) ||
                    ps2::ld16(car + 0x16a6) != (frame == 1 ? 123u : std::uint16_t(fixed))) {
                    std::fprintf(stderr, "FAIL wheel policy=%d history/state frame=%u\n", policy, frame);
                    std::exit(1);
                }
                call(0x001e8978, car);
                near(car + 0xff0, steering * (steering < 0 ? 0.75f : 1.0f), axis, frame);
                near(car + 0x1094, steering * (steering < 0 ? 1.0f : 0.75f), axis, frame);
                near(car + 0x1138, -0.02f, axis, frame); near(car + 0x11dc, 0.02f, axis, frame);
                ++checked;
            }
        }
    }
    std::printf("GT3 wheel mode-4 -> shared steering float -> wheel angles PASS: %u frames\n", checked);
}
}
int main(int argc, char **argv) {
    if (argc != 2) { std::fprintf(stderr, "usage: %s core.elf\n", argv[0]); return 1; }
    register_generated_code();
    unsigned entry;
    // Loads original tables/constants, but does not boot or execute the ELF entry.
    if (!ps2::load_elf(argv[1], entry)) return 1;
    constexpr float dt = 1.0f / 60.0f, limit = 0.5f, rate_limit = 10.0f;
    clear(mapping, 0xa0);
    ps2::st32(mapping + 0x50, 1); // bank 1, variant 0, action 0 -> shipped record 1 -> channel 2.
    if (ps2::ld16(0x002e2cfau + 6) != 2 ||
        load_float(0x00352970) != 100.0f || load_float(0x00352974) != 5.0f ||
        load_float(0x00352978) != 50.0f) {
        std::fprintf(stderr, "FAIL unexpected steering constants/binding in supplied ELF\n");
        return 1;
    }
    unsigned checked = 0;
    for (unsigned raw = 0; raw < 256; ++raw) {
        clear(device, 0x40); clear(input, 0x150); clear(car, 0x1800);
        clear(race, 0xb800); clear(packet, 16);
        ps2::st32(device, 1);
        ps2::st8(device + 0xc, 0x79); // DualShock 2 pressure-mode packet ID.
        ps2::st32(device + 0x10, 8);
        ps2::st8(device + 0x14, 0); ps2::st8(device + 0x15, 0x79);
        ps2::st8(device + 0x16, 0xff); ps2::st8(device + 0x17, 0xff); // no buttons
        for (unsigned i = 0; i < 4; ++i) ps2::st8(device + 0x18 + i, 128);
        ps2::st8(device + 0x1a, raw); // packet +6: left-stick X
        call(0x0022fc30, device, input);
        if (ps2::ld32(input + 0x40) != raw || (ps2::ld32(input + 0x14) & 31) != 8) {
            std::fprintf(stderr, "FAIL pad decode raw=%u channel2=%u type=%u\n", raw,
                         ps2::ld32(input + 0x40), ps2::ld32(input + 0x14));
            return 1;
        }
        call(0x001f4330, packet);
        // Type-8 dispatcher order: pressure D-pad first, mapped stick only if steering is zero.
        call(0x00210da8, input, packet);
        call(0x00210e68, input, packet, mapping, 1, 0);
        const int fixed = (256 - 2 * int(ps2::ld8(0x003416f8u + raw))) * 16;
        if (ps2::ld16(packet + 4) != std::uint16_t(fixed) ||
            ps2::ld8(packet) != 1 || ps2::ld8(packet + 1) != 2) {
            std::fprintf(stderr, "FAIL steering command raw=%u fixed=%d native=%d flags=%u mode=%u\n",
                         raw, fixed, int(std::int16_t(ps2::ld16(packet + 4))),
                         ps2::ld8(packet), ps2::ld8(packet + 1));
            return 1;
        }

        ps2::st32(car + 4, race);
        store_float(car + 0xec0, dt);
        store_float(car + 0x68, limit);
        ps2::st16(car + 0x6c, 2); // synthetic speed->steering-limit curve, constant 0.5
        ps2::st32(car + 0x70, knots); ps2::st32(car + 0x74, knots + 8);
        store_float(knots, 0); store_float(knots + 4, 100);
        store_float(knots + 8, limit); store_float(knots + 12, limit);
        store_float(0x0049d0a0, rate_limit); // synthetic runtime rate limit for selected class 0
        store_float(car + 0x120, 1.0f); store_float(car + 0x124, 0.75f);
        store_float(car + 0xe30, 0); store_float(car + 0xe34, 0.02f); // front/rear alignment
        float steering = 0, velocity = 0;
        const float target = limit * (float(fixed) / 4096.0f);
        for (unsigned frame = 1; frame <= 60; ++frame) {
            call(0x001e4478, car, packet, car + 0x1304);
            float acceleration = (target - steering) * 100.0f - velocity * 5.0f;
            if ((steering > 0 && target < steering) || (steering < 0 && target > steering))
                acceleration -= steering * 50.0f;
            velocity = std::clamp(velocity + acceleration * dt, -rate_limit, rate_limit);
            const float next = steering + velocity * dt;
            if ((steering <= target && target <= next) || (target <= steering && next <= target)) {
                steering = target; velocity = 0;
            } else steering = next;
            near(car + 0x13a0, steering, raw, frame);
            near(car + 0x13a8, velocity, raw, frame);
            call(0x001e8978, car);
            const float c0 = steering < 0 ? 0.75f : 1.0f;
            const float c1 = steering < 0 ? 1.0f : 0.75f;
            near(car + 0xff0, steering * c0, raw, frame);
            near(car + 0x1094, steering * c1, raw, frame);
            near(car + 0x1138, -0.02f, raw, frame);
            near(car + 0x11dc, 0.02f, raw, frame);
            ++checked;
            if (raw == 64 && (frame == 1 || frame == 60))
                std::printf("Steering fixture raw=64 curved=%u fixed=%d target=%.9g frame=%u steering=%.9g front=(%.9g,%.9g)\n",
                    ps2::ld8(0x003416f8u + raw), fixed, target, frame,
                    load_float(car + 0x13a0), load_float(car + 0xff0), load_float(car + 0x1094));
        }
    }
    std::printf("GT3 steering controller-state -> processing -> wheel-angle trace PASS: %u frames\n", checked);
    wheel_commands();
    wheel_driving();
}
