#pragma once
// Explicit, version-bound original-execution binding. Not a plugin API.
#include "ps2/cpu.hpp"
#include "src/gt3/gameplay/transmission/virtual/controller.hpp"
#include <string>
#include <vector>
namespace gt3::extensions::vt {
struct Event {std::uint64_t frame=0;Input input;bool disconnect=false;};
struct Config {bool enabled=false,shadow=false;Input initial;std::vector<Event> events;std::string trace;};
bool configure(Config,const std::string &load_path);
void finish();
void admission_enter(ps2::Cpu &,unsigned depth);
unsigned admission_route(ps2::Cpu &,unsigned depth);
bool selector(ps2::Cpu &,unsigned depth);
void observe(ps2::Cpu &,unsigned pc);
}
