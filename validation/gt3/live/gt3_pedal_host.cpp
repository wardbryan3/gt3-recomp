// Validation-only host; normal canonical main and unchanged steering/synthetic
// modules. Pedal substitution needs BOTH compile-time and runtime opt-in.
#include "gt3_clean_pedals.hpp"
#include "gt3_clean_steering.hpp"
#include "gt3_synthetic_wheel.hpp"
#include "ps2/generated.hpp"
#include <algorithm>
#include <memory>
#define main canonical_host_main
#include "../../../host/main.cpp"
#undef main
bool gt3_pedal_audit_stop=false;
namespace {
void trace_cpu(FILE *out,const ps2::Cpu &c,unsigned pc) {
    // Semantic PC is the explicit probe address. Cpu.pc between direct generated
    // branches is dispatch transport, retained separately, not an ISA instruction
    // counter. Serialize defined fields only (no native struct padding).
    auto word=[&](unsigned x) { std::fprintf(out,"%08x",x); };
    auto reg=[&](const ps2::Reg128 &r) { for(auto w:r.w)word(w); };
    std::fprintf(out,"\"cpu\":\"");
    for(auto &r:c.r)reg(r);reg(c.hi);reg(c.lo);word(c.sa);word(pc);word(c.budget);word(c.base);
    for(auto f:c.f)word(f);word(c.facc);word(c.fcr31);
    for(auto &v:c.vu0.vf)reg(v);reg(c.vu0.acc);for(auto v:c.vu0.vi)word(v);
    for(auto v:{c.vu0.q,c.vu0.p,c.vu0.i,c.vu0.r,c.vu0.mac,c.vu0.status,c.vu0.clip,c.vu0.cmsar0,c.vu0.tpc})word(v);
    for(auto v:c.cop0)word(v);std::fprintf(out,"\",\"transport_pc\":%u",c.pc);
}
}
int main(int argc,char **argv) {
    gt3::synthetic::Options options;bool clean=false,pedals=false;
    std::string trace;std::vector<char *> forwarded{argv[0]};
    for(int i=1;i<argc;++i) {
        const std::string arg=argv[i];
        if(arg=="--gt3-clean-pedals") {
#if GT3_PEDAL_VALIDATION_GATES
            pedals=true;
#else
            std::fprintf(stderr,"Pedal validation build gate is OFF\n");return 2;
#endif
        } else if(arg=="--gt3-pedal-trace"&&i+1<argc)trace=argv[++i];
        else if(arg=="--gt3-clean-steering")clean=true;
        else if(arg=="--gt3-wheel"&&i+1<argc) {
            options.enabled=true;if(!gt3::synthetic::parse_value(argv[++i],options.value))return 2;
        } else if(arg=="--gt3-wheel-at"&&i+1<argc) {
            gt3::synthetic::Event event;if(!gt3::synthetic::parse_event(argv[++i],event))return 2;
            options.events.push_back(event);
        } else if(arg=="--gt3-wheel-trace"&&i+1<argc)options.trace_path=argv[++i];
        else if(arg=="--gt3-triple")return 2;
        else forwarded.push_back(argv[i]);
    }
    forwarded.push_back(nullptr);
    std::unique_ptr<FILE,decltype(&std::fclose)> output(trace.empty()?nullptr:std::fopen(trace.c_str(),"wx"),&std::fclose);
    if(!trace.empty()&&!output)return 1;
    std::stable_sort(options.events.begin(),options.events.end(),[](auto &a,auto &b){return a.frame<b.frame;});
    gt3::synthetic::Experiment experiment(options);if(!experiment.open_trace())return 1;
    gt3::clean::enabled=clean;gt3::pedals::enabled=pedals;bool checked=false;unsigned car=0,command=0;
    ps2::g_options.on_probe=[&](ps2::Cpu &cpu,unsigned pc) {
        if(!checked) {
            checked=true;
            if(!gt3::synthetic::profile_matches()||!gt3::clean::profile_matches()||!gt3::pedals::profile_matches()) {
                ps2::halt("validation profile mismatch");return;
            }
        }
        experiment.probe(cpu,pc,ps2::frame_count());
        if(pc==0x1e48fc) { car=cpu.r[23].w[0];command=cpu.r[18].w[0]; }
        if(!output||!car)return;
        const bool response=pc==0x1d92e0&&(cpu.r[31].w[0]==0x1e4ad4||cpu.r[31].w[0]==0x1e4b9c);
        if(pc!=0x1e48fc&&pc!=0x1e4ba8&&pc!=0x1e4c74&&pc!=0x1e4d38&&
           pc!=0x1e8910&&pc!=0x1e7328&&pc!=0x1e6ec8&&pc!=0x1e7500&&!response)return;
        if(pc==0x1e8910&&cpu.r[4].w[0]!=car+0x10)return;
        if((pc==0x1e7328||pc==0x1e6ec8||pc==0x1e7500||pc==0x1e4d38)&&cpu.r[4].w[0]!=car)return;
        std::fprintf(output.get(),"{\"frame\":%llu,\"pc\":%u,\"car\":%u,",(unsigned long long)ps2::frame_count(),pc,car);
        trace_cpu(output.get(),cpu,pc);
        std::fprintf(output.get(),",\"flags\":%u,\"mode\":%u,\"accelerator_q\":%u,\"brake_q\":%d,\"auxiliary_q\":%u",ps2::ld8(command),ps2::ld8(command+1),ps2::ld16(command+8),static_cast<short>(ps2::ld16(command+10)),ps2::ld16(command+12));
        std::fprintf(output.get(),",\"accelerator\":%u,\"brake\":%u,\"effective_accelerator\":%u,\"coupling_candidate\":%u,\"auxiliary\":%u,\"history\":%u}\n",
            ps2::ld32(car+0x13ac),ps2::ld32(car+0x13b0),ps2::ld32(car+0x1428),ps2::ld32(car+0x139c),ps2::ld8(car+0x1304),ps2::ld8(car+0x1306));
    };
    const int result=canonical_host_main(int(forwarded.size())-1,forwarded.data());
    const auto &p=gt3::pedals::counts;const auto &s=gt3::clean::counts;
    std::fprintf(stderr,"[gt3-pedals] replaced=%llu fallback=%llu response_calls=%llu\n",(unsigned long long)p.replaced,(unsigned long long)p.fallback,(unsigned long long)p.response_calls);
    std::fprintf(stderr,"[gt3-clean] normalized=%llu wheel_commands=%llu filters=%llu envelopes=%llu\n",(unsigned long long)s.normalized,(unsigned long long)s.wheel_commands,(unsigned long long)s.filters,(unsigned long long)s.envelopes);
    if(!checked&&(pedals||clean||options.enabled||!trace.empty()||!options.trace_path.empty()))return 1;
    return result;
}
