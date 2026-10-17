#pragma once
#include "ps2/cpu.hpp"
#include <array>
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

namespace gt3::synthetic {
struct Event { std::uint64_t frame; double value; };
struct Options {
    bool enabled = false;
    double value = 0;
    std::vector<Event> events; // strictly increasing guest-frame thresholds
    std::string trace_path;   // optional; trace-only does not inject
};
bool parse_value(const char *text, double &value);
bool parse_event(const char *text, Event &event);
int axis_for_value(double value); // finite [-1,1]; positive means positive GT3 command
bool profile_matches();

// Experiment-local, EE-thread-only. No runtime dispatch or model replacement.
class Experiment {
public:
    explicit Experiment(Options options);
    ~Experiment();
    Experiment(const Experiment &) = delete;
    Experiment &operator=(const Experiment &) = delete;
    bool open_trace();
    void probe(ps2::Cpu &cpu, std::uint32_t pc, std::uint64_t frame);
private:
    Options options_;
    FILE *trace_ = nullptr;
    std::uint32_t context_car_ = 0, player_car_ = 0;
    std::uint32_t input_ = 0, command_ = 0, channels_ = 0;
    std::array<std::uint32_t, 5> saved_{};
    std::uint8_t shift_ = 0;
    bool scoped_ = false;
    double value_ = 0;
    int axis_ = 512, q_ = 0;
    unsigned mode_ = 0, flags_ = 0;
    int policy_ = 0;
    float expected_ = 0, expected_high_ = 0, expected_low_ = 0;
    float rate_ = 0;
    double value_at(std::uint64_t frame) const;
    void record(const char *stage, std::uint32_t pc, std::uint64_t frame,
                double expected = 0, double error = 0);
};
}
