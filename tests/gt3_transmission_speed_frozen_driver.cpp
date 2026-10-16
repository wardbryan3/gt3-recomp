// Test-only gate driver: the EXACT unchanged Frozen test still defines main.
// Separate processes run helper OFF / ON; no original test/assertion is rewritten.
#include "gt3_clean_transmission_speed.hpp"
#include "gt3_clean_transmission.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
namespace {
void report() {
    const auto h=gt3::transmission_speed::counts;
    const auto s=gt3::transmission::counts;
    if(h.fallback || (gt3::transmission_speed::enabled ? h.replaced!=s.original_speed_calls : h.replaced!=0)) {
        std::fprintf(stderr,"FAIL Frozen test helper routing\n");std::fflush(stdout);std::_Exit(1);
    }
    std::printf("Frozen test routing PASS helper=%llu selector-speed-DISPATCHES=%llu (old field unchanged; not an original-body count in pair mode)\n",(unsigned long long)h.replaced,(unsigned long long)s.original_speed_calls);
}
__attribute__((constructor)) void setup() {
    const char *gate=std::getenv("GT3_SPEED_PAIR_TEST");
    if(!gate || (std::strcmp(gate,"0")&&std::strcmp(gate,"1")))std::exit(2);
    gt3::transmission_speed::enabled=!std::strcmp(gate,"1");std::atexit(report);
}
}
