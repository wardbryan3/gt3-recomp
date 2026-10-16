// Disposable validation only. Existing speed/selector instrumentation is reused
// byte-for-byte, not edited. Pure models never modify guest memory or CPU.
#include "gt3_transmission_speed_host.inc"
#include "gt3_transmission_state.hpp"
#include "gt3_clean_transmission_admission.hpp"
namespace gen {void state_oracle_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace gt3::state_validation {inline unsigned depth=0;}
namespace {
namespace state_model=gt3::transmission_state;
bool state_shadow=false,state_in_shadow=false;
unsigned admission_car=0,admission_sp=0,admission_ra=0,engine_car=0,selection_car=0;
unsigned long long admission_entries=0,admission_exits=0,admission_shadows=0,engine_checks=0,selection_checks=0;
std::array<unsigned long long,16> state_changes{};
state_model::AdmissionResult admission_prediction{};
unsigned admission_accel=0,admission_engine=0,admission_policy=0;
state_model::SynchronizationResult engine_prediction{};
state_model::SelectionResult selection_prediction{};
void state_assert(bool ok,const char *why){if(!ok)speed_fail(why);}
bool state_player(unsigned car){return car>=0x500000 && car<0x2000000-0x1500 && ps2::ld8(car+0x136d)==0;}
void state_compare(ps2::Cpu &c) {
    state_in_shadow=true;const auto depth=gt3::state_validation::depth;
    const auto incoming=c;const std::vector<unsigned char> before(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    auto original=incoming;gen::state_oracle_unit_0039(original,123,depth);
    const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    std::memcpy(ps2::g_ram,before.data(),before.size());auto actual=incoming;const auto counts=gt3::transmission_admission::counts;
    state_assert(gt3::transmission_admission::replace(actual,depth),"admission real-entry shadow rejected");
    state_assert(!std::memcmp(&actual,&original,sizeof actual),"admission real-entry complete CPU/ABI/cost");
    state_assert(!std::memcmp(ps2::g_ram,expected.data(),expected.size()),"admission real-entry whole32MiB");
    gt3::transmission_admission::counts=counts;std::memcpy(ps2::g_ram,before.data(),before.size());gt3::state_validation::depth=depth;state_in_shadow=false;++admission_shadows;
}
void state_probe(ps2::Cpu &c,unsigned pc) {
    if(state_in_shadow||speed_in_shadow)return;
    speed_probe(c,pc);
    using namespace ps2;
    if(pc==0x1e6d48 && state_player(c.r[4].w[0])) {
        admission_car=c.r[4].w[0];admission_sp=c.r[29].w[0];admission_ra=c.r[31].w[0];const unsigned a=admission_car;
        admission_prediction=state_model::admit({ld8(a+0x13bb),ld8(a+0x13ba),ld32(a+0x139c),ld32(a+0x140c),ld32(a+0x1428),static_cast<std::int16_t>(ld16(a+0x1414)),ld16(a+0x234),ld32(c.r[28].w[0]-30060),ld32(c.r[28].w[0]-30056)});
        admission_accel=ld32(a+0x1428);admission_engine=ld32(a+0x13cc);admission_policy=state_model::effective_policy(static_cast<std::int8_t>(ld8(a+0x136d)),ld8(a+0x14b8),ld8(a+0x13e5));
        ++admission_entries;speed_event(c,pc,a,gt3::state_validation::depth);
        if(state_shadow && gt3::transmission_admission::enabled)state_compare(c);
    } else if(pc==0x6d480000 && admission_car && c.r[29].w[0]==admission_sp && c.pc==admission_ra) {
        const unsigned a=admission_car;state_assert(ld8(a+0x13bb)==admission_prediction.state && ld32(a+0x139c)==admission_prediction.candidate,"native admission model");
        if(admission_prediction.sample_rates)state_assert(ld32(a+0x1310)==admission_engine && ld32(a+0x1428)==state_model::prepared_accelerator(admission_prediction.state,admission_policy,admission_engine,ld32(a+0x1314),admission_accel),"native preparation model");
        ++admission_exits;speed_event(c,pc,a,gt3::state_validation::depth);admission_car=0;
    } else if(pc==0x1e7500 && state_player(c.r[4].w[0])) {engine_car=c.r[4].w[0];speed_event(c,pc,engine_car,0);}
    else if(pc==0x1e755c && engine_car==c.r[17].w[0]) {
        engine_prediction={0,ld8(engine_car+0x13be),state_model::integrate_free_engine(ld32(engine_car+0x13cc),c.f[0],ld32(engine_car+0x2bc),c.f[21],c.f[20]),false,state_model::Cause::unchanged};
    } else if(pc==0x1e7590 && engine_car==c.r[17].w[0]) {
        const unsigned a=engine_car,gp=c.r[28].w[0];
        engine_prediction=state_model::synchronize({ld8(a+0x13bb),ld8(a+0x13be),state_model::effective_policy(static_cast<std::int8_t>(ld8(a+0x136d)),ld8(a+0x14b8),ld8(a+0x13e5)),ld32(a+0x139c),ld32(a+0x1310),ld32(a+0x1314),ld32(a+0x13cc),c.f[0],ld32(a+0x13b0),ld32(a+0x140c),fp::mul(fp::cvt_s_w(ld16(a+0x1d6)),ld32(gp-30012)),fp::mul(fp::cvt_s_w(ld16(a+0x1d6)+500),ld32(gp-30008)),ld32(gp-30004),ld32(gp-30000)});
        engine_prediction.engine=state_model::clamp_nonzero_engine(engine_prediction.engine,fp::mul(fp::cvt_s_w(ld16(a+0x1d4)+10),ld32(gp-29996)));
    } else if(pc==0x1e77b4 && engine_car==c.r[17].w[0]) {
        state_assert(ld8(engine_car+0x13bb)==engine_prediction.state && ld8(engine_car+0x13be)==engine_prediction.inhibition && ld32(engine_car+0x13cc)==engine_prediction.engine,"native engine decision/free integration/clamp model");
        ++engine_checks;++state_changes[static_cast<unsigned>(engine_prediction.cause)];speed_event(c,pc,engine_car,0);engine_car=0;
    } else if(pc==0x1e77f8 && state_player(c.r[16].w[0]-0xf84)) {
        selection_car=c.r[16].w[0]-0xf84;selection_prediction=state_model::select(ld8(selection_car+0x13bb),ld8(selection_car+0x13ba),c.r[2].d[0]);speed_event(c,pc,selection_car,0);
    } else if(pc==0x1e783c && selection_car==c.r[16].w[0]-0xf84) {
        state_assert(ld8(selection_car+0x13bb)==selection_prediction.state && ld8(selection_car+0x13ba)==selection_prediction.selected,"native selection commit model");++selection_checks;speed_event(c,pc,selection_car,0);selection_car=0;
    }
}
void state_finish() {
    const auto n=gt3::transmission_admission::counts;
    std::fprintf(stderr,"STATE admission_entries=%llu admission_exits=%llu shadows=%llu replaced=%llu fallback=%llu engine_checks=%llu selection_checks=%llu causes=",admission_entries,admission_exits,admission_shadows,(unsigned long long)n.replaced,(unsigned long long)n.fallback,engine_checks,selection_checks);
    for(auto n:state_changes)std::fprintf(stderr,"%llu,",n);std::fputc('\n',stderr);
    state_assert(admission_entries==admission_exits,"native admission lifetime/count");
}
void state_install() {
    speed_install();ps2::g_options.on_probe=state_probe;std::atexit(state_finish);
    if(state_shadow && !gt3::transmission_admission::enabled)speed_fail("state shadow needs explicit clean gate");
}
}
