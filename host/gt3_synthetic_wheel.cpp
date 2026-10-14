#include "gt3_synthetic_wheel.hpp"
#include "ps2/memory.hpp"
#include "ps2/system.hpp"
#include <algorithm>
#include <bit>
#include <cerrno>
#include <cmath>
#include <cstdlib>
#include <utility>

namespace gt3::synthetic {
namespace {
bool ram(std::uint32_t address, unsigned size) {
    return address && !(address & 3) && address <= ps2::kRamSize - size;
}
float f(std::uint32_t address) { return std::bit_cast<float>(ps2::ld32(address)); }
float approach(float state, float target, float step) {
    return state < target ? std::min(state + step, target) : std::max(state - step, target);
}
}
bool parse_value(const char *text, double &value) {
    if (!text || !*text) return false;
    char *end = nullptr;
    errno = 0;
    const double parsed = std::strtod(text, &end);
    if (errno || end == text || *end || !std::isfinite(parsed) || parsed < -1 || parsed > 1) return false;
    value = parsed;
    return true;
}
bool parse_event(const char *text, Event &event) {
    if (!text || *text < '0' || *text > '9') return false;
    char *end = nullptr;
    errno = 0;
    const auto frame = std::strtoull(text, &end, 10);
    if (errno || end == text || *end != ':') return false;
    double value;
    if (!parse_value(end + 1, value)) return false;
    event = {frame, value};
    return true;
}
int axis_for_value(double value) {
    if (!std::isfinite(value) || value < -1 || value > 1) return -1;
    if (value == 1) return 0;
    if (value == -1) return 1023;
    return 512 - int(std::lround(value * (4096.0 / 9.0)));
}
bool profile_matches() {
    // Unmodified steering instructions in original and triple GT3 v1.10.
    // Full source/profile SHA-256 checks are additionally enforced by the build script.
    for (const auto &word : std::array<std::array<unsigned, 2>, 8>{{
             {0x2107ac, 0x0200202d}, {0x2107b0, 0x0c08457e},
             {0x2107b8, 0x260400cc}, {0x2115f8, 0x27bdffc0},
             {0x1e470c, 0x24020004}, {0x1e48a0, 0xc601049c},
             {0x1e8910, 0x44800800}, {0x1e7328, 0x27bdffb0}}})
        if (ps2::ld32(word[0]) != word[1]) return false;
    return ps2::ld32(0x33f824) == 0x22e000 && ps2::ld32(0x33f808) == 0;
}
Experiment::Experiment(Options options) : options_(std::move(options)) {}
Experiment::~Experiment() { if (trace_) std::fclose(trace_); }
bool Experiment::open_trace() {
    if (options_.trace_path.empty()) return true;
    trace_ = std::fopen(options_.trace_path.c_str(), "wx"); // never overwrite existing evidence
    if (!trace_) { std::perror("synthetic wheel trace"); return false; }
    return true;
}
double Experiment::value_at(std::uint64_t frame) const {
    double value = options_.value;
    for (const auto &event : options_.events) {
        if (event.frame > frame) break;
        value = event.value;
    }
    return value;
}
void Experiment::record(const char *stage, std::uint32_t pc, std::uint64_t frame,
                        double expected, double error) {
    if (!trace_ || !player_car_) return;
    std::fprintf(trace_,
        "{\"stage\":\"%s\",\"pc\":%u,\"frame\":%llu,\"enabled\":%s,"
        "\"car\":%u,\"input\":%u,\"host\":%.9g,\"axis\":%d,\"q\":%d,\"mode\":%u,\"flags\":%u,"
        "\"policy\":%d,\"steering\":%.9g,\"high\":%.9g,\"low\":%.9g,\"mechanical\":%.9g,"
        "\"rate\":%.9g,\"wheel0\":%.9g,\"wheel1\":%.9g,\"expected\":%.9g,\"error\":%.9g}\n",
        stage, pc, static_cast<unsigned long long>(frame), options_.enabled ? "true" : "false",
        player_car_, input_, value_, axis_, q_, mode_, flags_, policy_,
        f(player_car_ + 0x13a0), f(player_car_ + 0x1430), f(player_car_ + 0x142c),
        f(player_car_ + 0x68), f(player_car_ + 0x13a8),
        f(player_car_ + 0xff0), f(player_car_ + 0x1094), expected, error);
}
void Experiment::probe(ps2::Cpu &c, std::uint32_t pc, std::uint64_t frame) {
    if (pc == 0x1e4d38) {
        const auto car = c.r[4].w[0];
        context_car_ = ram(car, 0x1800) && ps2::ld8(car + 0x136d) == 0 &&
            (!ps2::ld8(car + 0x14b8) || ps2::ld16(car + 0x14ba)) ? car : 0;
    } else if (pc == 0x1e4d5c) {
        context_car_ = 0; // input builder has returned; no stale scope in menus/other callers
    } else if (pc == 0x2107ac) {
        const auto input = c.r[16].w[0], command = c.r[17].w[0];
        if (!context_car_ || !ram(input, 0x150) || !ram(command, 16) ||
            ps2::ld32(context_car_ + 12) != input || ps2::ld32(input + 0xc0) != 0x33f7e0) return;
        player_car_ = context_car_; input_ = input; command_ = command;
        value_ = value_at(frame); axis_ = axis_for_value(value_);
        if (options_.enabled) {
            if (scoped_ || axis_ < 0) { ps2::halt("synthetic wheel invalid/nested scope"); return; }
            channels_ = input + ((ps2::ld32(input + 0x14) & 31) ? 0x78 : 0x38);
            saved_ = {ps2::ld32(input + 0x14), ps2::ld32(input + 0x2c),
                      ps2::ld32(channels_), ps2::ld32(channels_ + 4), ps2::ld32(channels_ + 8)};
            shift_ = ps2::ld8(command + 2);
            ps2::st32(input + 0x14, (saved_[0] & ~0xe0u) | 0x20u);
            ps2::st32(input + 0x2c, 0); // pad already built; don't reapply its digital actions
            ps2::st32(channels_, axis_);
            ps2::st32(channels_ + 4, 255); ps2::st32(channels_ + 8, 255); // no synthetic pedals
            scoped_ = true;
        }
        record("input", pc, frame);
    } else if (pc == 0x2107b8) {
        if (c.r[16].w[0] != input_ || c.r[17].w[0] != command_) return;
        if (scoped_) {
            ps2::st32(input_ + 0x14, saved_[0]); ps2::st32(input_ + 0x2c, saved_[1]);
            for (unsigned i = 0; i < 3; ++i) ps2::st32(channels_ + 4 * i, saved_[i + 2]);
            ps2::st8(command_ + 2, shift_); // digital helper sets this even for a zero mask
            scoped_ = false;
        }
        q_ = std::int16_t(ps2::ld16(command_ + 4));
        mode_ = ps2::ld8(command_ + 1); flags_ = ps2::ld8(command_);
        record("command", pc, frame);
    } else if (pc == 0x1e4478 && c.r[4].w[0] == player_car_ && player_car_) {
        const auto command = c.r[5].w[0];
        if (!ram(command, 16)) return;
        q_ = std::int16_t(ps2::ld16(command + 4)); mode_ = ps2::ld8(command + 1);
        flags_ = ps2::ld8(command); policy_ = std::int8_t(ps2::ld8(player_car_ + 0x136f));
        record("process", pc, frame);
    } else if (pc == 0x1e471c && c.r[23].w[0] == player_car_ && player_car_) {
        const float step = f(0x35297c) * f(player_car_ + 0xec0);
        expected_high_ = f(player_car_ + 0x1430); expected_low_ = f(player_car_ + 0x142c);
        rate_ = f(player_car_ + 0x13a8);
        expected_ = 0;
        if (policy_ >= 0 && policy_ < 4) {
            expected_high_ = approach(expected_high_, std::bit_cast<float>(c.f[20]), step);
            expected_low_ = approach(expected_low_, std::bit_cast<float>(c.f[21]), step);
            expected_ = (q_ >= 0 ? expected_high_ : -expected_low_) * (float(q_) / 4096.0f);
        } else if (policy_ == 4) expected_ = f(player_car_ + 0x68) * (float(q_) / 4096.0f);
        record("mode4", pc, frame, expected_);
    } else if (pc == 0x1e48a0 && c.r[23].w[0] == player_car_ && player_car_ && mode_ == 4 && (flags_ & 1)) {
        const float error = std::max({std::abs(f(player_car_ + 0x13a0) - expected_),
            std::abs(f(player_car_ + 0x1430) - expected_high_),
            std::abs(f(player_car_ + 0x142c) - expected_low_),
            std::abs(f(player_car_ + 0x13a8) - rate_)});
        record("steering", pc, frame, expected_, error);
    } else if (pc == 0x1e8910 && c.r[4].w[0] == player_car_ + 0x10 && player_car_) {
        record("consume", pc, frame, f(player_car_ + 0x13a0),
               std::abs(std::bit_cast<float>(c.f[12]) - f(player_car_ + 0x13a0)));
    } else if (pc == 0x1e7328 && c.r[4].w[0] == player_car_ && player_car_) {
        const float steering = f(player_car_ + 0x13a0);
        float error = 0;
        for (unsigned i = 0; i < 4; ++i) {
            const float angle = (i < 2 ? steering * f(player_car_ + 0x120 +
                4 * (steering < 0 ? 1 - i : i)) : 0) +
                (i & 1 ? 1 : -1) * f(player_car_ + 0xe30 + 4 * (i >> 1));
            error = std::max(error, std::abs(f(player_car_ + 0xff0 + i * 0xa4) - angle));
        }
        record("angles", pc, frame, steering, error);
    }
}
}
