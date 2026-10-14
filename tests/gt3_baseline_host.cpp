// Validation-only entry point. The canonical ps2run target and control source
// are unchanged. This wrapper uses the normal boot/load/run/save implementation.
#include "gt3_clean_steering.hpp"
#include "gt3_synthetic_wheel.hpp"
#include "ps2/generated.hpp"
#include <algorithm>
#include <memory>
#define main canonical_host_main
#include "../host/main.cpp"
#undef main

int main(int argc, char **argv) {
    gt3::synthetic::Options options;
    bool clean = false;
    std::vector<char *> forwarded{argv[0]};
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--gt3-clean-steering") clean = true;
        else if (arg == "--gt3-wheel" && i + 1 < argc) {
            options.enabled = true;
            if (!gt3::synthetic::parse_value(argv[++i], options.value)) return 2;
        } else if (arg == "--gt3-wheel-at" && i + 1 < argc) {
            gt3::synthetic::Event event;
            if (!gt3::synthetic::parse_event(argv[++i], event)) return 2;
            options.events.push_back(event);
        } else if (arg == "--gt3-wheel-trace" && i + 1 < argc) {
            options.trace_path = argv[++i];
        } else if (arg == "--gt3-triple") {
            // This baseline uses the unpatched original profile, not triple mode.
            return 2;
        } else forwarded.push_back(argv[i]);
    }
    forwarded.push_back(nullptr);
    std::stable_sort(options.events.begin(), options.events.end(),
                     [](const auto &a, const auto &b) { return a.frame < b.frame; });
    gt3::synthetic::Experiment experiment(options);
    if (!experiment.open_trace()) return 1;
    gt3::clean::enabled = clean;
    bool checked = false;
    ps2::g_options.on_probe = [&](ps2::Cpu &cpu, unsigned pc) {
        if (!checked) {
            checked = true;
            if (!gt3::synthetic::profile_matches() || !gt3::clean::profile_matches()) {
                ps2::halt("validation profile mismatch");
                return;
            }
        }
        experiment.probe(cpu, pc, ps2::frame_count());
    };
    const int result = canonical_host_main(int(forwarded.size()) - 1, forwarded.data());
    const auto &c = gt3::clean::counts;
    std::fprintf(stderr, "[gt3-clean] normalized=%llu wheel_commands=%llu filters=%llu envelopes=%llu\n",
                 (unsigned long long)c.normalized, (unsigned long long)c.wheel_commands,
                 (unsigned long long)c.filters, (unsigned long long)c.envelopes);
    if (!checked && (clean || options.enabled || !options.trace_path.empty())) return 1;
    return result;
}
