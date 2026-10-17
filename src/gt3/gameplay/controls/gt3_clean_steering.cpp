#include "gt3_clean_steering.hpp"
#include "ps2/generated.hpp"
#include <algorithm>
#include <cstring>

namespace gt3::clean {
namespace {
namespace fp = ps2::fp;
thread_local ps2::Cpu *observation_cpu = nullptr;
void store_state(unsigned address, const CarPartial &car);
constexpr EeFloat zero = 0, one = 0x3f800000, fixed_scale = 0x39800000;
bool less(EeFloat a, EeFloat b) { return fp::key(a) < fp::key(b); }
bool le(EeFloat a, EeFloat b) { return fp::key(a) <= fp::key(b); }
EeFloat neg(EeFloat x) { return x ^ fp::kSign; }
EeFloat fixed(std::int16_t x) {
    return fp::mul(fp::cvt_s_w(std::uint32_t(std::int32_t(x))), fixed_scale);
}
// Explicit wrapping reproduces EE 32-bit arithmetic, including out-of-report inputs.
std::int32_t signed_word(std::uint32_t x) { return std::bit_cast<std::int32_t>(x); }
int pedal(std::uint32_t raw, unsigned threshold) {
    return std::min(signed_word((255u - raw - threshold) << 1), 256);
}
} // namespace
std::int32_t normalize_mapped_channel(std::uint32_t channel, std::uint32_t raw,
                                      std::int32_t sensitivity, const std::uint8_t *curve,
                                      Cost &cost) {
    if ((channel & 255) < 4) {
        const int response = curve[raw & 255];
        switch (channel & 0x300) {
        case 0x100:
            cost.add(23);
            return std::max(0, (128 - response) * 2);
        case 0x200:
            cost.add(25);
            return std::max(0, (response - 128) * 2);
        default:
            cost.add(20);
            return response;
        }
    }
    cost.add(21);
    const int numerator = std::min(int((raw & 255) * 2), 256) * 100;
    // EE DIV1 returns -1 for nonnegative numerator / zero. BREAK is handled by bridge.
    return std::min(sensitivity ? numerator / sensitivity : -1, 256);
}
void build_wheel_command(const InputPartial &input, Command &command, Cost &cost) {
    cost.add(13 + 2 + 8); // prologue + shipped digital getter + type decoding
    const unsigned type = (input.type_bits >> 5) & 7;
    if (type >= 4) {
        cost.add(1 + 5);
        return;
    }
    cost.add(2);
    if (!type) {
        cost.add(5);
        return;
    }
    const auto mask = input.digital_mask;
    // 0x00210EF8: digital actions clear analog bits, not the existing command wholesale.
    for (unsigned i = 0; i < 4; ++i)
        if (mask & (0x400u << i)) {
            if (i == 0)
                command.accelerator = 1;
            if (i == 1)
                command.brake = 1;
            if (i == 2)
                command.handbrake = 1;
            if (i == 3)
                command.auxiliary = 1;
            command.analog_flags &= ~(i == 2 ? 16u : i == 3 ? 8u : 2u << i);
            cost.add(4);
        }
    command.shift = mask & 0x8000 ? -1 : (mask >> 14) & 1;
    cost.add(2 + 15 + (mask & 0x8000 ? 2 : 4));
    const unsigned bank = (input.type_bits & 31) ? 16 : 0;
    const auto raw = input.channels[bank];
    const int q = signed_word((512u - raw) * 9u);
    command.steering = std::clamp(q, -4096, 4096);
    command.steering_mode = 4;
    command.analog_flags |= 1;
    cost.add(6 + 4 + 7 + 2 + 12 + 4);
    const int accelerator = pedal(input.channels[bank + 1], 75);
    cost.add(3 + 8 + 3);
    if (accelerator > 0) {
        command.accelerator = std::uint16_t(std::uint32_t(accelerator) << 4);
        command.analog_flags |= 2;
        cost.add(4);
    }
    cost.add(6 + 4);
    const int brake = pedal(input.channels[bank + 2], 80);
    cost.add(3 + 8 + 3);
    if (brake > 0) {
        command.brake = std::uint16_t(std::uint32_t(brake) << 4);
        command.analog_flags |= 4;
        cost.add(4);
    }
    cost.add(1 + 5);
}
EeFloat slew_limit(EeFloat current, EeFloat target, EeFloat step, Cost &cost) {
    cost.add(4);
    if (less(current, target)) {
        current = fp::add(current, step);
        cost.add(4 + 2);
        if (less(target, current))
            current = target;
    } else {
        cost.add(3);
        if (less(target, current)) {
            current = fp::sub(current, step);
            cost.add(3 + 2);
            if (less(current, target))
                current = target;
        }
    }
    cost.add(2);
    return current;
}
void filter_stick(CarPartial &car, EeFloat target, EeFloat outward_rate, EeFloat return_rate,
                  const Constants &k, Cost &cost) {
    if (enabled)
        ++counts.filters;
    const auto old = car.steering;
    auto acceleration =
        fp::sub(fp::mul(fp::sub(target, old), k.spring), fp::mul(car.steering_rate, k.damping));
    cost.add(15);
    bool returning = false;
    if (less(zero, old)) {
        cost.add(4);
        returning = less(target, old);
    }
    if (!returning) {
        cost.add(4);
        if (less(old, zero)) {
            cost.add(4);
            returning = less(old, target);
        }
    }
    if (returning) {
        outward_rate = return_rate;
        acceleration = fp::sub(acceleration, fp::mul(old, k.return_spring));
        cost.add(3);
    }
    // Positive/returning path reaches 43E0; nonnegative/nonreturning bypasses it.
    if (returning || less(old, zero))
        cost.add(1);
    auto rate = fp::add(car.steering_rate, fp::mul(acceleration, car.dt));
    cost.add(5);
    if (less(outward_rate, rate)) {
        rate = outward_rate;
        cost.add(1);
    } else {
        cost.add(5);
        if (less(rate, neg(outward_rate))) {
            rate = neg(outward_rate);
            cost.add(2);
        }
    }
    const auto next = fp::add(old, fp::mul(rate, car.dt));
    cost.add(4);
    bool crossed = false;
    if (le(old, target)) {
        cost.add(4);
        crossed = le(target, next);
    }
    if (!crossed) {
        cost.add(4);
        if (le(target, old)) {
            cost.add(4);
            crossed = le(next, target);
            if (crossed)
                cost.add(1);
        }
    }
    cost.add(2);
    car.steering = crossed ? target : next;
    car.steering_rate = crossed ? zero : rate;
}
bool process_steering(CarPartial &car, const Command &command, std::uint8_t &kind, EeFloat high,
                      EeFloat average, unsigned classification, const Constants &k, Cost &cost) {
    cost.add(4);
    bool extend = true;
    if (command.steering_mode == 4) {
        const int policy = car.wheel_policy;
        cost.add(2 + 2 + 4); // call signed policy getter
        EeFloat floor = high;
        if (policy == 2) {
            cost.add(2 + (classification == 1 ? 1 : 0));
            floor = k.policy2[classification == 1];
        } else {
            cost.add(2);
            if (policy < 3) {
                cost.add(2);
                if (policy != 1)
                    cost.add(2);
            } else {
                cost.add(2);
                if (policy == 3) {
                    extend = false;
                    cost.add(1);
                } else {
                    cost.add(2);
                    extend = false;
                    if (policy != 4) {
                        extend = true;
                        cost.add(2);
                    }
                }
            }
            if (policy == 1 || policy == 3) {
                floor = k.policy1[classification == 1];
                cost.add(2 + (classification == 1 ? 2 : 0));
            }
        }
        if (policy == 1 || policy == 2 || policy == 3) {
            cost.add(4);
            if (less(high, floor)) {
                high = floor;
                cost.add(1);
            } else
                cost.add(2);
        } else if (policy == 4)
            cost.add(1);
    } else
        cost.add(1);
    auto low = neg(high);
    cost.add(2);
    if (extend) {
        cost.add(3);
        bool outside = !le(low, average);
        if (!outside) {
            cost.add(3);
            outside = !le(average, high);
        }
        if (!outside) {
            car.envelope_ratio = zero;
            cost.add(2 + 1);
        } else {
            cost.add(4);
            if (less(zero, average)) {
                high = average;
                car.envelope_ratio = average;
                cost.add(3 + 1);
            } else {
                cost.add(4);
                if (less(average, zero)) {
                    low = average;
                    car.envelope_ratio = average;
                    cost.add(2 + 1);
                }
            }
        }
    }
    if (less(car.mechanical_limit, high))
        high = car.mechanical_limit;
    if (less(low, neg(car.mechanical_limit)))
        low = neg(car.mechanical_limit);
    car.unknown13a4 = one; // Assignment evidenced; field's larger purpose is not established.
    cost.add(4 + 5 + 7);
    const int q = command.steering;
    if (!(command.analog_flags & 1)) {
        kind = 1;
        car.positive_limit = high;
        car.negative_limit = low;
        cost.add(7);
        auto target = high;
        if (q <= 0) {
            cost.add(3);
            target = q < 0 ? low : zero;
            if (q == 0)
                cost.add(2);
        }
        if (q != 0)
            cost.add(1);
        cost.add(10);
        filter_stick(car, target, k.digital_outward[classification],
                     k.digital_return[classification], k, cost);
        cost.add(2);
    } else {
        cost.add(4);
        if (command.steering_mode == 4) {
            // Feed the independent, unchanged synthetic observer at its original semantic seams.
            // These are observations of clean execution, not execution of skipped EE instructions.
            if (observation_cpu) {
                observation_cpu->f[20] = high;
                observation_cpu->f[21] = low;
                ps2::probe(*observation_cpu, 0x1e471c);
            }
            kind = 0;
            car.previous_wheel_command = car.wheel_command;
            car.wheel_command = q;
            auto target = fixed(q);
            const int policy = car.wheel_policy;
            cost.add(12 + 2 + 3);
            if (policy < 0) {
                target = zero;
                cost.add(1);
            } else {
                cost.add(2);
                if (policy < 4) {
                    const auto step = fp::mul(k.limit_slew, car.dt);
                    cost.add(4);
                    car.positive_limit = slew_limit(car.positive_limit, high, step, cost);
                    cost.add(5);
                    car.negative_limit = slew_limit(car.negative_limit, low, step, cost);
                    cost.add(5 + 3);
                    target = fp::mul(
                        le(zero, target) ? car.positive_limit : neg(car.negative_limit), target);
                } else {
                    cost.add(2);
                    if (policy == 4) {
                        target = fp::mul(car.mechanical_limit, target);
                        cost.add(2);
                    } else {
                        target = zero;
                        cost.add(2 + 1);
                    }
                }
            }
            car.steering = target;
            cost.add(2 + 1);
            if (observation_cpu) {
                store_state(observation_cpu->r[23].w[0], car);
                ps2::st8(observation_cpu->r[19].w[0] + 3, kind);
                ps2::probe(*observation_cpu, 0x1e48a0);
            }
        } else {
            cost.add(4);
            if (command.steering_mode == 2 || command.steering_mode == 3) {
                car.positive_limit = high;
                car.negative_limit = low;
                auto target = fixed(q);
                cost.add(13);
                if (le(zero, target)) {
                    target = fp::mul(high, target);
                    cost.add(2);
                } else {
                    target = fp::mul(neg(low), target);
                    cost.add(1);
                }
                cost.add(2);
                if (q) {
                    kind = command.steering_mode == 3 ? 1 : 2;
                    cost.add(3 + (kind == 1 ? 1 : 0) + 1);
                }
                cost.add(4);
                if (kind == 1) {
                    cost.add(1 + 10);
                    filter_stick(car, target, k.digital_outward[classification],
                                 k.digital_return[classification], k, cost);
                    cost.add(2);
                } else {
                    cost.add(7);
                    filter_stick(car, target, k.analog_rate[classification],
                                 k.analog_rate[classification], k, cost);
                    cost.add(1);
                }
            }
        }
    }
    bool invalid = false;
    cost.add(5);
    if (fp::key(car.envelope_ratio) != fp::key(zero)) {
        const auto result = fp::div(car.steering, car.envelope_ratio);
        invalid = result.invalid;
        car.envelope_ratio = result.value;
        cost.add(8 + 1);
        if (less(car.envelope_ratio, zero)) {
            car.envelope_ratio = zero;
            cost.add(2);
        } else {
            cost.add(6);
            if (less(one, car.envelope_ratio))
                car.envelope_ratio = one;
        }
    }
    return invalid;
}
bool profile_matches() {
    return ps2::ld32(0x210f90) == 0x308300ff && ps2::ld32(0x1e4368) == 0xc4870ec0 &&
           ps2::ld32(0x1e45a8) == 0x92510001 && ps2::ld32(0x1e48fc) == 0x24020001;
}
bool enabled = false;
Counts counts;
namespace {
Constants constants(unsigned gp) {
    Constants k{};
    k.spring = ps2::ld32(gp - 20608);
    k.damping = ps2::ld32(gp - 20604);
    k.return_spring = ps2::ld32(gp - 20600);
    k.limit_slew = ps2::ld32(gp - 20596);
    for (unsigned i = 0; i < 2; ++i) {
        k.policy1[i] = ps2::ld32(gp - 20592 + i * 4);
        k.policy2[i] = ps2::ld32(gp - 20584 + i * 4);
    }
    for (unsigned i = 0; i < 3; ++i) {
        k.digital_outward[i] = ps2::ld32(0x49d080 + i * 4);
        k.digital_return[i] = ps2::ld32(0x49d090 + i * 4);
        k.analog_rate[i] = ps2::ld32(0x49d0a0 + i * 4);
    }
    return k;
}
template <class T> T read(unsigned address) {
    T result;
    std::memcpy(&result, ps2::g_ram + address, sizeof(T));
    return result;
}
void store_state(unsigned address, const CarPartial &car) {
    // Only evidenced writes; never bulk-write opaque vehicle padding.
    ps2::st32(address + 0x13a0, car.steering);
    ps2::st32(address + 0x13a4, car.unknown13a4);
    ps2::st32(address + 0x13a8, car.steering_rate);
    ps2::st32(address + 0x1420, car.envelope_ratio);
    ps2::st32(address + 0x142c, car.negative_limit);
    ps2::st32(address + 0x1430, car.positive_limit);
    ps2::st16(address + 0x16a4, car.wheel_command);
    ps2::st16(address + 0x16a6, car.previous_wheel_command);
}
} // namespace
bool replace(ps2::Cpu &cpu, std::uint32_t address) {
    if (!enabled)
        return false;
    Cost cost;
    if (address == 0x210f90) {
        if (!cpu.r[6].d[0] && (cpu.r[4].w[0] & 255) >= 4)
            ps2::breakpoint(cpu, 0x21102c);
        ps2::set32(cpu.r[2], normalize_mapped_channel(cpu.r[4].w[0], cpu.r[5].w[0], cpu.r[6].sw[0],
                                                      ps2::g_ram + 0x3416f8, cost));
        ++counts.normalized;
        cpu.pc = cpu.r[31].w[0];
    } else if (address == 0x2115f8) {
        if (cpu.r[4].w[0] > 0x2000000 - sizeof(InputPartial) ||
            cpu.r[5].w[0] > 0x2000000 - sizeof(Command))
            return false;
        const auto input = read<InputPartial>(cpu.r[4].w[0]);
        if (input.vtable != 0x33f7e0 || ps2::ld16(input.vtable + 0x28) ||
            ps2::ld16(input.vtable + 0x40) || ps2::ld32(input.vtable + 0x2c) != 0x22dfa8 ||
            ps2::ld32(input.vtable + 0x44) != 0x22e000)
            return false;
        auto command = read<Command>(cpu.r[5].w[0]);
        build_wheel_command(input, command, cost);
        std::memcpy(ps2::g_ram + cpu.r[5].w[0], &command, sizeof(command));
        ++counts.wheel_commands;
        cpu.pc = cpu.r[31].w[0];
    } else if (address == 0x1e4368) {
        const auto car_address = cpu.r[4].w[0];
        if (car_address > 0x2000000 - sizeof(CarPartial))
            return false;
        auto car = read<CarPartial>(car_address);
        filter_stick(car, cpu.f[12], cpu.f[13], cpu.f[14], constants(cpu.r[28].w[0]), cost);
        ps2::st32(car_address + 0x13a0, car.steering);
        ps2::st32(car_address + 0x13a8, car.steering_rate);
        cpu.pc = cpu.r[31].w[0];
    } else if (address == 0x1e45a8) {
        const auto car_address = cpu.r[23].w[0];
        if (car_address > 0x2000000 - sizeof(CarPartial) ||
            cpu.r[18].w[0] > 0x2000000 - sizeof(Command) || cpu.r[19].w[0] > 0x2000000 - 4)
            return false;
        auto car = read<CarPartial>(car_address);
        const auto command = read<Command>(cpu.r[18].w[0]);
        auto kind = ps2::ld8(cpu.r[19].w[0] + 3);
        if (cpu.r[21].w[0] > 2)
            return false; // unevidenced classification/table indices stay generated
        observation_cpu = &cpu;
        if (process_steering(car, command, kind, cpu.f[0], cpu.f[22], cpu.r[21].w[0],
                             constants(cpu.r[28].w[0]), cost))
            cpu.fcr31 |= 0x30000;
        observation_cpu = nullptr;
        store_state(car_address, car);
        ps2::st8(cpu.r[19].w[0] + 3, kind);
        cpu.r[3].sd[0] = car.control_kind136d;
        ++counts.envelopes;
        cpu.pc = 0x1e48fc;
    } else
        return false;
    cpu.budget -= cost.instructions;
    return true;
}
} // namespace gt3::clean
