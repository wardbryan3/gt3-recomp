// Disposable validation host only, never included by canonical host/main.cpp.
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
namespace gen { void oracle_unit_0039(ps2::Cpu &,unsigned,unsigned); }
namespace gt3::transmission_validation { unsigned entry_depth=0; }
namespace {
bool transmission_shadow=false;
FILE *transmission_trace=nullptr;
unsigned long long transmission_entries=0,transmission_exits=0,transmission_shadows=0;
unsigned transmission_car=0,transmission_sp=0;
void transmission_fail(const char *why) { std::fprintf(stderr,"transmission validation FAIL: %s\n",why);std::abort(); }
void transmission_event(ps2::Cpu &c,unsigned pc,unsigned car) {
    if(!transmission_trace)return;
    std::fprintf(transmission_trace,"{\"frame\":%llu,\"pc\":%u,\"car\":%u,\"sp\":%u,\"ra\":%u,\"budget\":%d,\"v0\":%u,\"aux\":%u,\"relative\":%u,\"selected\":%u,\"state\":%u,\"policy\":%u,\"owner\":%u,\"mode\":%u,\"suppression\":%u,\"inhibition\":%u,\"candidate_bits\":%u,\"accelerator_bits\":%u,\"speed_bits\":%u}\n",
        (unsigned long long)ps2::frame_count(),pc,car,c.r[29].w[0],c.r[31].w[0],c.budget,c.r[2].w[0],ps2::ld8(car+0x1304),ps2::ld8(car+0x1305),ps2::ld8(car+0x13ba),ps2::ld8(car+0x13bb),ps2::ld8(car+0x13e5),ps2::ld8(car+0x136d),ps2::ld8(car+0x14b8),ps2::ld16(car+0x14ba),ps2::ld8(car+0x13be),ps2::ld32(car+0x139c),ps2::ld32(car+0x13ac),ps2::ld32(car+0x140c));
}
void transmission_probe(ps2::Cpu &c,unsigned pc) {
    if(pc==0x1e5458) {
        ++transmission_entries;transmission_car=c.r[4].w[0];transmission_sp=c.r[29].w[0];
        transmission_event(c,pc,transmission_car);
        if(transmission_shadow) {
            // Real original entry CPU/RAM. Both executions are shadow copies;
            // restoring the entire pre-entry RAM leaves actual play untouched.
            const std::vector<unsigned char> before(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
            auto original=c;gen::oracle_unit_0039(original,60,gt3::transmission_validation::entry_depth);
            const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
            std::memcpy(ps2::g_ram,before.data(),before.size());auto clean=c;
            const auto counters=gt3::transmission::counts;
            if(!gt3::transmission::replace_manual_selector(clean,gt3::transmission_validation::entry_depth))transmission_fail("live shadow guard rejection");
            if(std::memcmp(&original,&clean,sizeof clean))transmission_fail("live FULL CPU/ABI/budget");
            if(std::memcmp(ps2::g_ram,expected.data(),expected.size()))transmission_fail("live whole32MiB RAM");
            gt3::transmission::counts=counters;std::memcpy(ps2::g_ram,before.data(),before.size());++transmission_shadows;
        }
    } else if(pc==0x1e5730) {
        if(c.r[29].w[0]!=transmission_sp)transmission_fail("entry/exit stack lifetime");
        ++transmission_exits;transmission_event(c,pc,transmission_car);
    }
}
void transmission_finish() {
    const auto &n=gt3::transmission::counts;
    std::fprintf(stderr,"MT validation entries=%llu exits=%llu shadows=%llu replaced=%llu fallback=%llu original_speed_calls=%llu\n",transmission_entries,transmission_exits,transmission_shadows,(unsigned long long)n.replaced,(unsigned long long)n.fallback,(unsigned long long)n.original_speed_calls);
    if(transmission_trace && std::fclose(transmission_trace))transmission_fail("trace close");
}
void transmission_install() {
    if(transmission_shadow&&!gt3::transmission::enabled)transmission_fail("shadow requires opt-in clean gate");
    const char *path=std::getenv("GT3_TRANSMISSION_RECOVERY_TRACE");
    if(path){transmission_trace=std::fopen(path,"wx");if(!transmission_trace)transmission_fail("new trace output required");}
    if(path||gt3::transmission::enabled){ps2::g_options.on_probe=transmission_probe;std::atexit(transmission_finish);}
}
}
