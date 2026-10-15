#include "gt3_virtual_handbrake.hpp"
#include "ps2/memory.hpp"
#include <cstring>
#include <utility>
namespace gt3::virtual_handbrake {
namespace {
void require(bool value,const char *message){if(!value)throw std::runtime_error(message);}
bool car_ram(unsigned address){return address>=0x500000&&!(address&3)&&address<=ps2::kRamSize-0x1800;}
std::uint64_t fingerprint(unsigned first,unsigned end){std::uint64_t hash=14695981039346656037ull;for(;first<end;++first)hash=(hash^ps2::ld8(first))*1099511628211ull;return hash;}
}
bool profile_matches() {
    return fingerprint(0x1e4cb0,0x1e4e78)==0xd79ba29ed968508aull&&
        fingerprint(0x210740,0x2107d0)==0x47412f65574f97fcull&&
        fingerprint(0x1e4bb8,0x1e4c60)==0xcdb8e58e1936e8acull;
}
Experiment::Experiment(Options options):options_(std::move(options)){validate(options_);}
Experiment::~Experiment(){if(trace_)std::fclose(trace_);}
bool Experiment::open_trace(){if(options_.trace_path.empty())return true;trace_=std::fopen(options_.trace_path.c_str(),"wx");return trace_!=nullptr;}
void Experiment::record(const char *stage,unsigned pc,std::uint64_t frame) {
    if(!trace_||!player_)return;
    std::fprintf(trace_,"{\"stage\":\"%s\",\"pc\":%u,\"frame\":%llu,\"enabled\":%s,\"car\":%u,\"command\":%u,\"host_value\":%.17g,\"bytes\":[",stage,pc,(unsigned long long)frame,options_.enabled?"true":"false",player_,command_,value_);
    for(unsigned i=0;i<16;++i)std::fprintf(trace_,"%s%u",i?",":"",ps2::ld8(command_+i));
    std::fprintf(trace_,"],\"floor\":%u,\"processed\":%u,\"coupling_candidate\":%u,\"wheel_brake\":[",ps2::ld32(0x352990),ps2::ld32(player_+0x13b4),ps2::ld32(player_+0x139c));
    for(unsigned i=0;i<4;++i)std::fprintf(trace_,"%s%u",i?",":"",ps2::ld32(player_+0x1274+i*0x24));
    std::fprintf(trace_,"]}\n");
    require(!std::ferror(trace_)&&std::fflush(trace_)==0,"virtual handbrake trace write failed");
}
void Experiment::probe(ps2::Cpu &cpu,unsigned pc,std::uint64_t frame) {
    if(!options_.enabled&&!trace_)return;
    if(pc==0x1e4d38) {
        require(!active_&&!scoped_,"virtual handbrake nested owner");
        active_=true;car_=cpu.r[4].w[0];owner_sp_=cpu.r[29].w[0];
        eligible_=cpu.r[4].d[0]==car_&&car_ram(car_)&&ps2::ld8(car_+0x136d)==0&&
            (!ps2::ld8(car_+0x14b8)||ps2::ld16(car_+0x14ba));
    } else if(pc==0x1e4d5c&&active_&&eligible_) {
        const unsigned sp=cpu.r[29].w[0];
        require(owner_sp_>=0x400040&&owner_sp_<=0x500000&&!(owner_sp_&15)&&sp==owner_sp_-64&&
            cpu.r[29].d[0]==sp&&cpu.r[17].d[0]==car_&&cpu.r[16].d[0]==car_+0xf84&&
            cpu.r[28].d[0]==0x3579f0,"virtual handbrake activation mismatch");
        command_=sp;player_=car_;value_=at_frame(options_,frame);
        record("before-command",pc,frame);
        if(options_.enabled) {
            require(profile_matches(),"virtual handbrake original profile mismatch");
            std::memcpy(saved_.data(),ps2::g_ram+command_,16);expected_=saved_;
            const unsigned q=command_for_value(value_);
            expected_[0]|=0x10;expected_[14]=q&255;expected_[15]=q>>8;
            // Exactly three command bytes. No direct car state, calibration,
            // pad channel, mode, steering, throttle, brake, shift or aux writes.
            ps2::st8(command_,expected_[0]);ps2::st16(command_+14,q);
            scoped_=true;++counts.injected;
        }
        record("command",pc,frame);
    } else if(pc==0x1e4bb8&&player_&&cpu.r[23].w[0]==player_) {
        require(cpu.r[18].w[0]==command_,"virtual handbrake processor command mismatch");
        if(scoped_)require(!std::memcmp(expected_.data(),ps2::g_ram+command_,16),"virtual handbrake command changed before processing");
        ++counts.entries;record("entry",pc,frame);
    } else if(pc==0x1e4c60&&player_&&cpu.r[23].w[0]==player_) {
        ++counts.joins;record("join",pc,frame);
    } else if(pc==0x1e4e68&&active_) {
        if(scoped_) {
            require(cpu.r[29].d[0]==command_&&!std::memcmp(expected_.data(),ps2::g_ram+command_,16),"virtual handbrake command lifetime changed");
            ps2::st8(command_,saved_[0]);ps2::st16(command_+14,unsigned(saved_[14])|(unsigned(saved_[15])<<8));
            require(!std::memcmp(saved_.data(),ps2::g_ram+command_,16),"virtual handbrake restoration failed");
            scoped_=false;++counts.restored;record("restored",pc,frame);
        }
        active_=false;eligible_=false;
    } else if(player_) {
        if(pc==0x1e4c74&&cpu.r[23].w[0]==player_)record("coupling",pc,frame);
        if(pc==0x1e3aac&&cpu.r[17].w[0]==player_){++counts.shifts;record("shift",pc,frame);}
        if(pc==0x1e6fc8&&cpu.r[17].w[0]==player_+0xf84){++counts.brake_joins;record("brake-join",pc,frame);}
        if(cpu.r[4].w[0]==player_) {
            if(pc==0x1e6ec8){++counts.brakes;record("brake",pc,frame);}
            if(pc==0x1e7500){++counts.engines;record("engine",pc,frame);}
        }
    }
}
}
