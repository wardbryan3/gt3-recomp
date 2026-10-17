// Disposable native validation host ONLY; canonical main is never edited.
#include "gt3_clean_transmission_speed.hpp"
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
namespace gen {void oracle_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace gt3::speed_validation {extern unsigned depth;}
namespace {
bool speed_shadow=false,speed_in_shadow=false;
FILE *speed_trace=nullptr;
unsigned speed_mt_car=0,speed_mt_sp=0,speed_object=0,speed_sp=0,speed_ra=0,speed_mt_depth=0,speed_depth=0;
unsigned long long speed_mt_entries=0,speed_mt_exits=0,speed_entries=0,speed_exits=0,mt_shadows=0,helper_shadows=0;
void speed_fail(const char *why){std::fprintf(stderr,"PAIR VALIDATION FAIL: %s\n",why);std::abort();}
void speed_event(ps2::Cpu &c,unsigned marker,unsigned object,unsigned entry_depth) {
    if(!speed_trace)return;
    auto snapshot=c;
    // Only entry PC transport differs between direct generated and dispatched
    // calls. Keep raw transport_pc separately; normalize that field ONLY in the
    // trace copy. Actual shadow/outgoing CPU comparisons have NO normalization.
    if(marker==0x1e5458 || marker==0x1e4e80)snapshot.pc=marker;
    std::fprintf(speed_trace,"{\"frame\":%llu,\"marker\":%u,\"object\":%u,\"depth\":%u,\"transport_pc\":%u,\"ra\":%u,\"sp\":%u,\"maximum\":%u,\"rpm_bound\":%u,\"owner\":%u,\"policy\":%u,\"state\":%u,\"selected\":%u,\"inhibition\":%u,\"cpu\":\"",(unsigned long long)ps2::frame_count(),marker,object,entry_depth,c.pc,c.r[31].w[0],c.r[29].w[0],ps2::ld8(object+0x20a),ps2::ld16(object+0x236),ps2::ld8(object+0x136d),ps2::ld8(object+0x13e5),ps2::ld8(object+0x13bb),ps2::ld8(object+0x13ba),ps2::ld8(object+0x13be));
    for(unsigned j=0;j<sizeof snapshot;++j)std::fprintf(speed_trace,"%02x",reinterpret_cast<unsigned char *>(&snapshot)[j]);
    std::fputs("\"}\n",speed_trace);
}
void speed_compare(ps2::Cpu &c,bool selector) {
    const unsigned depth=gt3::speed_validation::depth;
    speed_in_shadow=true;
    const std::vector<unsigned char> before(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    auto original=c;gen::oracle_unit_0039(original,selector?60:47,depth);
    const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    std::memcpy(ps2::g_ram,before.data(),before.size());auto actual=c;
    const auto s=gt3::transmission::counts;const auto h=gt3::transmission_speed::counts;
    bool replaced=selector?gt3::transmission::replace_manual_selector(actual,depth):gt3::transmission_speed::replace(actual);
    if(!replaced)speed_fail("actual-entry shadow guard rejected");
    if(std::memcmp(&actual,&original,sizeof actual))speed_fail("actual-entry complete CPU/ABI/cost");
    if(std::memcmp(ps2::g_ram,expected.data(),expected.size()))speed_fail("actual-entry whole32MiB");
    gt3::transmission::counts=s;gt3::transmission_speed::counts=h;
    std::memcpy(ps2::g_ram,before.data(),before.size());gt3::speed_validation::depth=depth;speed_in_shadow=false;
    if(selector)++mt_shadows;else ++helper_shadows;
}
void speed_probe(ps2::Cpu &c,unsigned pc) {
    if(speed_in_shadow)return;
    if(pc==0x1e5458) {
        ++speed_mt_entries;speed_mt_car=c.r[4].w[0];speed_mt_sp=c.r[29].w[0];speed_mt_depth=gt3::speed_validation::depth;speed_event(c,pc,speed_mt_car,speed_mt_depth);
        if(speed_shadow&&gt3::transmission::enabled)speed_compare(c,true);
    } else if(pc==0x1e5730) {
        if(c.r[29].w[0]!=speed_mt_sp)speed_fail("MT stack lifetime");
        ++speed_mt_exits;speed_event(c,pc,speed_mt_car,speed_mt_depth);
    } else if(pc==0x1e4e80) {
        ++speed_entries;speed_object=c.r[4].w[0];speed_sp=c.r[29].w[0];speed_ra=c.r[31].w[0];speed_depth=gt3::speed_validation::depth;speed_event(c,pc,speed_object,speed_depth);
        if(speed_shadow&&gt3::transmission_speed::enabled)speed_compare(c,false);
    } else if(pc==0xe4e80000u) {
        if(c.r[29].w[0]!=speed_sp || c.r[31].w[0]!=speed_ra || c.pc!=speed_ra)speed_fail("helper return/lifetime");
        ++speed_exits;speed_event(c,pc,speed_object,speed_depth);
    }
}
void speed_finish() {
    const auto s=gt3::transmission::counts;const auto h=gt3::transmission_speed::counts;
    std::fprintf(stderr,"PAIR mt_entries=%llu mt_exits=%llu helper_entries=%llu helper_exits=%llu mt_shadows=%llu helper_shadows=%llu selector=%llu helper=%llu selector_fallback=%llu helper_fallback=%llu speed_dispatches=%llu\n",speed_mt_entries,speed_mt_exits,speed_entries,speed_exits,mt_shadows,helper_shadows,(unsigned long long)s.replaced,(unsigned long long)h.replaced,(unsigned long long)s.fallback,(unsigned long long)h.fallback,(unsigned long long)s.original_speed_calls);
    if(speed_trace&&std::fclose(speed_trace))speed_fail("trace close");
}
void speed_install() {
    const bool active=gt3::transmission::enabled||gt3::transmission_speed::enabled;
    if(speed_shadow&&!active)speed_fail("shadow requires explicit clean gate");
    const char *path=std::getenv("GT3_SPEED_TRACE");
    if(path){speed_trace=std::fopen(path,"wx");if(!speed_trace)speed_fail("new trace required");}
    if(path||active){ps2::g_options.on_probe=speed_probe;std::atexit(speed_finish);}
}
}
