#pragma once

#include "cpu.hpp"

#include <cstdint>
#include <functional>
#include <string>
#include <vector>

namespace ps2 {

inline constexpr std::uint64_t kEeClock = 294912000ull;
inline constexpr std::uint32_t kHandlerReturn = 0x00001000u;
inline constexpr std::uint32_t kIdle = 0x00001010u;

extern Cpu g_cpu;

struct Press {
    std::uint64_t frame;
    std::uint32_t frames;
    std::uint16_t buttons;
};

struct AxisInput {
    std::uint64_t frame;
    std::uint32_t frames;
    unsigned axis;
    std::uint8_t value;
};

struct Options {
    std::uint32_t output_width = 0, output_height = 0;
    float presentation_aspect = 4.0f / 3.0f;
    bool trace_syscalls = false;
    bool trace_io = false;
    bool trace_threads = false;
    bool pal = true;
    bool rate_forced = false;
    std::uint64_t max_frames = 0;
    std::string misses_path;
    std::string disc_path;
    bool trace_iop_modules = false;
    bool trace_iop_hle = false;
    std::string frames_dir;
    std::uint32_t frame_every = 60;
    std::vector<Press> presses;
    std::vector<AxisInput> axes;
    std::function<void()> on_vblank;
    std::function<void(Cpu &, std::uint32_t)> on_probe;
    std::function<void()> on_scene_end;
    std::function<void(const std::string &name, const std::uint8_t *code, std::size_t size)> on_vu_program;
    std::string memcard_path;
    std::function<void()> on_memcard_saved;
    std::string save_state_path;
    std::uint64_t save_state_frame = 0;
};

extern Options g_options;

struct ThreadContext {
    Reg128 r[32];
    Reg128 hi, lo;
    std::uint32_t sa, pc;
    std::uint32_t f[32];
    std::uint32_t facc, fcr31;
};

void save_context(const Cpu &c, ThreadContext &t);
void load_context(Cpu &c, const ThreadContext &t);

std::uint64_t now();
std::uint64_t hblank_cycles();
void set_budget(Cpu &c, std::int64_t cycles);
void schedule(int event, std::uint64_t at, std::function<void()> action);
bool preempt(Cpu &c);

bool has_code(std::uint32_t pc);
void raise_intc(unsigned cause);
void request_reschedule();
void request_iop_sync();
void sync_iop();

bool load_elf(const std::string &path, std::uint32_t &entry);
void boot(std::uint32_t entry, const std::vector<std::string> &args);
int run();
void halt(const std::string &reason);
bool save_state(const std::string &path);
bool load_state(const std::string &path);
bool load_state(const std::uint8_t *data, std::size_t size);
bool halted();
std::uint64_t frame_count();

bool display_frame(std::vector<std::uint32_t> &rgba, std::uint32_t &width, std::uint32_t &height);

struct WindowTarget {
    enum Kind { X11, Wayland, Canvas } kind = X11;
    void *display = nullptr;
    std::uint64_t window = 0;
    void *surface = nullptr;
    const char *selector = nullptr;
    std::uint32_t width = 0, height = 0;
};

// Lets the WebGPU renderer present straight to a window or canvas instead of handing frames back.
bool attach_window(const WindowTarget &target);
void resize_window(std::uint32_t width, std::uint32_t height);
bool present_frame();
void init_graphics();
float presentation_aspect();
void scene_aspect(float aspect);
void start_render_thread();
void start_vu_thread();
void run_vu_thread();
double vu_thread_idle_ms();
std::uint64_t vu1_interpreted_calls();
void post_present();
enum class Rendered { idle, presented, busy };
Rendered render_pending(bool surface, const std::function<void(const std::uint32_t *rgba, std::uint32_t width, std::uint32_t height)> &copy,
                        const std::function<void()> &before_present, double budget_ms);
void wait_render_work(int timeout_ms);
void wake_render_thread();
bool copy_frame(std::vector<std::uint32_t> &rgba, std::uint32_t &width, std::uint32_t &height);
bool parse_press(const std::string &spec, Press &press);
double gpu_busy_ms();
void browser_yield();
std::uint64_t frames_run();
std::uint64_t primitives_drawn();
// pad 0 is the first controller port, pad 1 the second, which starts unplugged
void set_pad_buttons(std::uint16_t pressed, int pad = 0);
void set_pad_axis(int axis, std::uint8_t value, int pad = 0);
void set_pad_pressure(int button, std::uint8_t value, int pad = 0);
void set_pad_connected(int pad, bool connected);
std::uint16_t pad_rumble(int pad = 0);
void set_audio_sink(std::function<void(const std::int16_t *samples, std::size_t frames)> sink);

}
