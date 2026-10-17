#include "ps2/system.hpp"
#include "ps2/memory.hpp"
#include <array>

#ifdef PS2_WINDOW
#include "window.hpp"
#endif
#ifdef PS2_PROFILE
#include "profile.hpp"
#endif

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

void register_generated_code();
void register_generated_vu();

namespace {

int usage() {
    std::fprintf(stderr,
                 "usage: ps2run <elf> [--arg text]... [--frames n] [--ntsc] [--misses file]\n"
                 "              [--disc image.iso] [--memcard card.ps2] [--pal | --ntsc] [--trace-syscalls] [--trace-io] [--trace-threads]\n"
                 "              [--trace-iop] [--trace-iop-hle] [--frames-dir dir] [--frame-every n]\n"
                 "              [--press frame:button[+button][:frames]]... [--window] [--fullscreen]\n"
                 "              [--save-state frame:file] [--load-state file] [--output-size WxH] [--aspect W:H] [--render-scale 1..9] [--render-scale-y 1..9] [--ram-word address:expected:value] [--axis frame:axis:value:duration]\n"
#ifdef GT3_HOST_PRESENTATION
                 "              [--gt3-triple] (inherited opt-in presentation; default OFF)\n"
#endif
    );
    return 2;
}

}

int main(int argc, char **argv) {
    if (argc < 2) return usage();
    std::vector<std::string> args{argv[1]};
    [[maybe_unused]] bool window = false, fullscreen = false;
#ifdef GT3_HOST_PRESENTATION
    bool gt3_triple = false;
#endif
    std::string load_path;
    std::vector<std::array<unsigned, 3>> ram_words;
    for (int i = 2; i < argc; ++i) {
        const std::string a = argv[i];
        if (a == "--arg" && i + 1 < argc) args.push_back(argv[++i]);
        else if (a == "--frames" && i + 1 < argc) ps2::g_options.max_frames = std::strtoull(argv[++i], nullptr, 10);
        else if (a == "--ntsc" || a == "--pal") {
            ps2::g_options.pal = a == "--pal";
            ps2::g_options.rate_forced = true;
        }
        else if (a == "--misses" && i + 1 < argc) ps2::g_options.misses_path = argv[++i];
        else if (a == "--trace-syscalls") ps2::g_options.trace_syscalls = true;
        else if (a == "--trace-io") ps2::g_options.trace_io = true;
        else if (a == "--trace-threads") ps2::g_options.trace_threads = true;
        else if (a == "--disc" && i + 1 < argc) ps2::g_options.disc_path = argv[++i];
        else if (a == "--memcard" && i + 1 < argc) ps2::g_options.memcard_path = argv[++i];
        else if (a == "--trace-iop") ps2::g_options.trace_iop_modules = true;
        else if (a == "--trace-iop-hle") ps2::g_options.trace_iop_hle = true;
#ifdef GT3_HOST_PRESENTATION
        else if (a == "--gt3-triple") gt3_triple = true;
#endif
        else if (a == "--ram-word" && i + 1 < argc) {
            std::array<unsigned, 3> patch{}; char extra = 0;
            if (std::sscanf(argv[++i], "%x:%x:%x%c", &patch[0], &patch[1], &patch[2], &extra) != 3 || (patch[0] & 3) || patch[0] > ps2::kRamSize - 4) return usage();
            ram_words.push_back(patch);
        }
        else if (a == "--output-size" && i + 1 < argc) {
            unsigned w = 0, h = 0; char extra = 0;
            if (std::sscanf(argv[++i], "%ux%u%c", &w, &h, &extra) != 2 || !w || !h || w > 8192 || h > 8192) return usage();
            ps2::g_options.output_width = w; ps2::g_options.output_height = h;
        }
        else if (a == "--aspect" && i + 1 < argc) {
            unsigned w = 0, h = 0; char extra = 0;
            if (std::sscanf(argv[++i], "%u:%u%c", &w, &h, &extra) != 2 || !w || !h || w > 64 || h > 64) return usage();
            ps2::g_options.presentation_aspect = float(w) / float(h);
        }
        else if (a == "--render-scale-y" && i + 1 < argc) {
            char *end = nullptr; const long scale = std::strtol(argv[++i], &end, 10);
            if (*end || scale < 1 || scale > 9) return usage();
            setenv("PS2_SCALE_Y", argv[i], 1);
        }
        else if (a == "--render-scale" && i + 1 < argc) {
            char *end = nullptr; const long scale = std::strtol(argv[++i], &end, 10);
            if (*end || scale < 1 || scale > 9) return usage();
            setenv("PS2_SCALE", argv[i], 1);
        }
        else if (a == "--frames-dir" && i + 1 < argc) ps2::g_options.frames_dir = argv[++i];
        else if (a == "--press" && i + 1 < argc) {
            ps2::Press press;
            if (!ps2::parse_press(argv[++i], press)) return usage();
            ps2::g_options.presses.push_back(press);
        }
        else if (a == "--axis" && i + 1 < argc) {
            unsigned long long frame;
            unsigned axis, value, duration;
            char extra;
            if (std::sscanf(argv[++i], "%llu:%u:%u:%u%c", &frame, &axis, &value, &duration, &extra) != 4 || axis > 3 || value > 255 || !duration) return usage();
            ps2::g_options.axes.push_back({frame, duration, axis, static_cast<std::uint8_t>(value)});
        }
#ifdef PS2_WINDOW
        else if (a == "--window") window = true;
        else if (a == "--fullscreen") window = fullscreen = true;
#endif
        else if (a == "--frame-every" && i + 1 < argc) ps2::g_options.frame_every = static_cast<std::uint32_t>(std::strtoul(argv[++i], nullptr, 10));
        else if (a == "--save-state" && i + 1 < argc) {
            const std::string spec = argv[++i];
            const auto colon = spec.find(':');
            if (colon == std::string::npos) return usage();
            ps2::g_options.save_state_frame = std::strtoull(spec.substr(0, colon).c_str(), nullptr, 10);
            ps2::g_options.save_state_path = spec.substr(colon + 1);
        }
        else if (a == "--load-state" && i + 1 < argc) load_path = argv[++i];
        else return usage();
    }

#ifdef GT3_HOST_PRESENTATION
    if (gt3_triple) {
        // Address map is pinned to the fingerprint-checked GT3 PBPX-95503 v1.10 profile.
        ps2::g_options.on_probe = [](ps2::Cpu &, std::uint32_t pc) {
            if (pc == 0x0017e888u) {
                ps2::st32(0x002f424cu, 1u); // GT3 display configuration: widescreen enabled.
                ps2::scene_aspect(16.0f / 3.0f);
            }
        };
        ps2::g_options.on_scene_end = [] { ps2::st32(0x002f424cu, 0u); };
        ram_words.insert(ram_words.end(), {
            {0x34fd04u, 0x3fb6d98cu, 0x3eb6d98cu},
            {0x34fd74u, 0xc2d55556u, 0xc46e0000u},
            {0x34fd78u, 0x443aaaaau, 0x44c70000u},
            {0x34ffc8u, 0xc2d4dd70u, 0xc46e0000u},
            {0x34ffccu, 0x443a9baeu, 0x44c70000u},
        });
    }
#endif

#ifdef PS2_WINDOW
    if (window && !open_window(fullscreen)) return 1;
#endif
    register_generated_code();
    register_generated_vu();
    const auto emulate = [&]() -> int {
        std::uint32_t entry = 0;
        if (!ps2::load_elf(argv[1], entry)) {
            std::fprintf(stderr, "cannot load %s\n", argv[1]);
            return 1;
        }
        ps2::boot(entry, args);
        if (!load_path.empty() && !ps2::load_state(load_path)) return 1;
        for (const auto &p : ram_words) {
            const auto actual = ps2::ld32(p[0]);
            if (actual != p[1] && actual != p[2]) {
                std::fprintf(stderr, "[profile] data mismatch at %08x: got %08x\n", p[0], actual); return 1;
            }
        }
        for (const auto &p : ram_words) ps2::st32(p[0], p[2]);
#ifdef PS2_PROFILE
        const char *profile = std::getenv("PS2_PROFILE");
        const char *profile_from = std::getenv("PS2_PROFILE_FROM");
        if (profile) start_profile(profile_from ? std::strtoull(profile_from, nullptr, 10) : 0);
        const int result = ps2::run();
        if (profile) write_profile(profile);
        return result;
#else
        return ps2::run();
#endif
    };
#ifdef PS2_WINDOW
    if (window) return run_window(emulate);
#endif
    return emulate();
}
