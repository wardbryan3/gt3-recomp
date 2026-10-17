#include "gt3_virtual_pedals.hpp"
#include "ps2/memory.hpp"
#include <cstring>
#include <utility>
namespace gt3::virtual_pedals {
namespace {
bool ram(unsigned a,unsigned n){return a>=0x500000&&!(a&3)&&a<=ps2::kRamSize-n;}
std::uint64_t fingerprint(unsigned a,unsigned z){std::uint64_t h=14695981039346656037ull;for(;a<z;++a)h=(h^ps2::ld8(a))*1099511628211ull;return h;}
void require(bool v,const char *s){if(!v)throw std::runtime_error(s);}
}
bool profile_matches(){return fingerprint(0x1e4cb0,0x1e4e78)==0xd79ba29ed968508aull&&
    fingerprint(0x210740,0x2107d0)==0x47412f65574f97fcull&&
    fingerprint(0x1e48fc,0x1e4ba8)==0x6138166f2b0e6cfeull;}
Experiment::Experiment(Options o):options_(std::move(o)){validate(options_);}
Experiment::~Experiment(){if(trace_)std::fclose(trace_);}
bool Experiment::open_trace(){if(options_.trace_path.empty())return true;trace_=std::fopen(options_.trace_path.c_str(),"wx");return trace_!=nullptr;}
void Experiment::record(const char *stage,unsigned pc,std::uint64_t frame){
    if(!trace_||!player_)return;
    std::fprintf(trace_,"{\"stage\":\"%s\",\"pc\":%u,\"frame\":%llu,\"enabled\":%s,\"car\":%u,\"command\":%u,\"host_throttle\":%.17g,\"host_brake\":%.17g,\"flags\":%u,\"mode\":%u,\"throttle_q\":%u,\"brake_q\":%u,\"steering_q\":%d,\"shift\":%u,\"auxiliary_q\":%u,\"other_q\":%u,\"accelerator_bits\":%u,\"brake_bits\":%u,\"effective_accelerator_bits\":%u,\"steering_bits\":%u}\n",
        stage,pc,(unsigned long long)frame,options_.enabled?"true":"false",player_,command_,values_.throttle,values_.brake,
        ps2::ld8(command_),ps2::ld8(command_+1),ps2::ld16(command_+8),ps2::ld16(command_+10),
        int(std::int16_t(ps2::ld16(command_+4))),ps2::ld8(command_+2),ps2::ld16(command_+12),ps2::ld16(command_+14),
        ps2::ld32(player_+0x13ac),ps2::ld32(player_+0x13b0),ps2::ld32(player_+0x1428),ps2::ld32(player_+0x13a0));
    require(!std::ferror(trace_)&&std::fflush(trace_)==0,"virtual pedal trace write failed");
}
void Experiment::probe(ps2::Cpu &c,unsigned pc,std::uint64_t frame){
    // No trace/options: entirely inert. Trace-only observes without touching guest state.
    if(!options_.enabled&&!trace_)return;
    if(pc==0x1e4d38){
        require(!active_&&!scoped_,"virtual pedal nested owner");active_=true;car_=c.r[4].w[0];owner_sp_=c.r[29].w[0];
        eligible_=ram(car_,0x1800)&&ps2::ld8(car_+0x136d)==0&&(!ps2::ld8(car_+0x14b8)||ps2::ld16(car_+0x14ba));
    } else if(pc==0x1e4d5c&&active_&&eligible_){
        const unsigned sp=c.r[29].w[0];
        require(owner_sp_>=0x400040&&owner_sp_<=0x500000&&!(owner_sp_&15)&&sp==owner_sp_-64&&c.r[17].w[0]==car_&&c.r[16].w[0]==car_+0xf84,"virtual pedal command activation mismatch");
        command_=sp;player_=car_;values_=at_frame(options_,frame);
        record("before-command",pc,frame);
        if(options_.enabled){
            require(profile_matches(),"virtual pedal original profile mismatch");
            require(ps2::ld8(command_+1)>=2&&ps2::ld8(command_+1)<=4&&ps2::ld16(command_+12)==0,"virtual pedal unsupported mode/auxiliary context");
            std::memcpy(saved_.data(),ps2::g_ram+command_,16);expected_=saved_;
            expected_[0]|=6;
            for(unsigned i=0;i<2;++i){unsigned q=command_for_value(i?values_.brake:values_.throttle);expected_[8+2*i]=q&255;expected_[9+2*i]=q>>8;}
            // The ONLY guest writes are flags and two command halfwords. No car,
            // processed state, input channel, steering/mode/action or aux writes.
            ps2::st8(command_,expected_[0]);ps2::st16(command_+8,command_for_value(values_.throttle));ps2::st16(command_+10,command_for_value(values_.brake));
            scoped_=true;++counts.injected;
        }
        record("command",pc,frame);
    } else if(pc==0x1e48fc&&player_&&c.r[23].w[0]==player_){
        require(c.r[18].w[0]==command_,"virtual pedal processing command mismatch");
        if(scoped_)require(!std::memcmp(expected_.data(),ps2::g_ram+command_,16),"virtual pedal command changed before processing");
        ++counts.entries;record("entry",pc,frame);
    } else if(pc==0x1e4ba8&&player_&&c.r[23].w[0]==player_){++counts.joins;record("join",pc,frame);
    } else if(pc==0x1e4e68&&active_){
        if(scoped_){
            require(c.r[29].w[0]==command_&&!std::memcmp(expected_.data(),ps2::g_ram+command_,16),"virtual pedal command lifetime changed");
            ps2::st8(command_,saved_[0]);ps2::st16(command_+8,unsigned(saved_[8])|(unsigned(saved_[9])<<8));ps2::st16(command_+10,unsigned(saved_[10])|(unsigned(saved_[11])<<8));
            require(!std::memcmp(saved_.data(),ps2::g_ram+command_,16),"virtual pedal full command restoration failed");
            scoped_=false;++counts.restored;record("restored",pc,frame);
        }
        active_=false;eligible_=false;
    } else if(player_&&c.r[4].w[0]==player_){
        if(pc==0x1e6ec8){++counts.brakes;record("brake-consumer",pc,frame);}
        if(pc==0x1e7500){++counts.engines;record("engine-consumer",pc,frame);}
    }
}
}
