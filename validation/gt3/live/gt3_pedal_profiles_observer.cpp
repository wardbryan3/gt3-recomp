// Read-only host observation at existing pedal seams in disposable translations.
// Never edits guest memory/registers, calls the replacement, or injects inputs.
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
namespace {
struct Output {
    FILE *file{};
    Output() {
        if(const char *path=std::getenv("GT3_PEDAL_PROFILE_TRACE")) {
            file=std::fopen(path,"wx");
            if(!file)ps2::halt("cannot create exclusive pedal profile trace");
        }
    }
    ~Output(){if(file)std::fclose(file);}
};
unsigned current_car=0,current_command=0;
bool ram(unsigned p,unsigned n){return p<=0x2000000-n;}
}
void gt3_pedal_profile_observe(const ps2::Cpu &c,unsigned pc) {
    static Output output;if(!output.file)return;
    if(pc==0x1d92e0&&c.r[31].w[0]!=0x1e4ad4&&c.r[31].w[0]!=0x1e4b9c)return;
    if(pc==0x1e48fc){current_car=c.r[23].w[0];current_command=c.r[18].w[0];}
    const unsigned car=current_car,cmd=current_command,ctl=c.r[19].w[0],gp=c.r[28].w[0];
    if(!car||!ram(car,0x14bc)||!ram(cmd,16)||!ram(ctl,4)||gp<20576||!ram(gp-20576,4)) {
        std::fprintf(output.file,"{\"pc\":%u,\"invalid_observation_context\":true}\n",pc);
        ps2::halt("pedal survey observation outside bounded RAM context");return;
    }
    std::fprintf(output.file,"{\"frame\":%llu,\"pc\":%u,\"car\":%u,\"command\":%u,\"control\":%u,\"s0\":%u,\"gp\":%u,\"incoming_v1\":%lld,\"s1\":%llu,\"kind\":%d,\"stored_policy\":%u,\"policy_blocked\":%u,\"auxiliary_suppression\":%u,\"mode\":%u,\"flags\":%u,\"history\":%u,\"accelerator_q\":%u,\"brake_q\":%d,\"auxiliary_q\":%u,\"f12\":%u,\"a0\":%u,\"a1\":%u,\"ra\":%u",
        (unsigned long long)ps2::frame_count(),pc,car,cmd,ctl,c.r[16].w[0],gp,(long long)c.r[3].sd[0],(unsigned long long)c.r[17].d[0],
        (int)(signed char)ps2::ld8(car+0x136d),ps2::ld8(car+0x13e5),ps2::ld8(car+0x14b8),ps2::ld16(car+0x14ba),
        ps2::ld8(cmd+1),ps2::ld8(cmd),ps2::ld8(ctl+2),ps2::ld16(cmd+8),(int)(short)ps2::ld16(cmd+10),ps2::ld16(cmd+12),c.f[12],c.r[4].w[0],c.r[5].w[0],c.r[31].w[0]);
    auto words=[&](const char *key,unsigned address,unsigned count){
        std::fprintf(output.file,",\"%s\":[",key);
        for(unsigned i=0;i<count;++i)std::fprintf(output.file,"%s%u",i?",":"",ps2::ld32(address+4*i));
        std::fprintf(output.file,"]");
    };
    words("accelerator_descriptor",0x49d060,4);words("brake_descriptor",0x49d070,4);
    words("slew",0x2d4930,4);words("floor",gp-20576,1);
    const unsigned input=ps2::ld32(car+12);
    if(input&&ram(input,0x150))std::fprintf(output.file,",\"input_type_bits\":%u,\"input_vtable\":%u",ps2::ld32(input+0x14),ps2::ld32(input+0xc0));
    std::fprintf(output.file,"}\n");
    if(std::ferror(output.file))ps2::halt("pedal profile trace write failed");
}
