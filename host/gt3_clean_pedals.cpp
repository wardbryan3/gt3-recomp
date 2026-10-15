// Newly written bounded semantic recovery; provenance: pedal-join-contract.md.
// Scratch assignments are the interior EE ABI, NOT additional recovered behavior.
// No host float arithmetic, general response evaluator, or downstream simulation.
#include "gt3_clean_pedals.hpp"
#include "ps2/generated.hpp"
#include <cstring>
#include <limits>
namespace gt3::pedals {
bool enabled=false;
Counts counts;
namespace {
using Bits=std::uint32_t;
template<class T> T read(unsigned address) {
    T result;std::memcpy(&result,ps2::g_ram+address,sizeof result);return result;
}
struct Execution {
    ps2::Cpu &cpu;
    unsigned car, command, control, depth;
    void reg(unsigned n,std::uint64_t x) { cpu.r[n].d[0]=x; }
    void cost(unsigned n) { cpu.budget-=n; }
    void condition(bool value) {
        cpu.fcr31=(cpu.fcr31&~ps2::kFpuCondition)|(value?ps2::kFpuCondition:0);
    }
    // Both original callers pass derivative=null. Preserve the actual generated
    // helper's CPU/FPU effects/cost and its original site-specific return address.
    void response(unsigned descriptor,unsigned return_pc) {
        reg(4,descriptor);reg(5,0);reg(31,return_pc);cost(4);
        cpu.pc=0x1d92e0;ps2::dispatch(cpu,0,depth+1);
        cpu.f[12]=cpu.f[0];cost(2);++counts.response_calls;
    }
};
void process(Execution &e,const CarPartial &car,const CommandPartial &cmd) {
    auto &c=e.cpu;
    auto &x=c.f[12];auto &a=c.f[0];auto &b=c.f[1];auto &z=c.f[2];auto &q=c.f[3];
    const auto floor=ps2::ld32(c.r[28].w[0]-20576);
    const auto fall=ps2::ld32(0x2d4934);
    constexpr Bits one=0x3f800000,q12=0x39800000;
    // Policy selection and unsigned arbitration. Delay-slot and branch-likely
    // costs are charged by semantic path; scratch lanes reflect the last writer.
    unsigned policy=0;
    e.reg(2,1);e.reg(17,0);e.cost(3);
    if(c.r[3].d[0]!=1) {
        e.reg(2,car.policy_suppression);e.cost(3);
        if(!car.policy_suppression)policy=car.numeric_policy;
    }
    e.reg(17,policy);
    unsigned accelerator=cmd.accelerator,auxiliary=cmd.auxiliary;
    bool analog=cmd.flags&2,aux_analog=cmd.flags&8;
    e.reg(3,cmd.flags);e.reg(7,1);e.reg(2,cmd.flags&2);e.reg(6,accelerator);e.cost(5);
    if(!analog) { accelerator=(accelerator<<12)&65535;e.reg(7,0);e.cost(3); }
    e.reg(2,cmd.flags&8);e.reg(5,auxiliary);e.reg(8,1);e.cost(4);
    if(!aux_analog) { auxiliary=(auxiliary<<12)&65535;e.reg(8,0);e.cost(3); }
    e.reg(2,car.auxiliary_suppression);e.reg(3,policy<7);e.cost(4);
    if(car.auxiliary_suppression)auxiliary=0;
    e.reg(5,auxiliary);e.reg(6,accelerator);
    if(policy<7) {
        e.reg(2,0x33c6c0);e.reg(3,0x33c6c0+4*policy);
        e.reg(4,ps2::ld32(0x33c6c0+4*policy));e.cost(7);
        if(policy<=2) {
            e.reg(2,auxiliary<accelerator);e.cost(3);
            if(auxiliary<accelerator)auxiliary=0;
            else { accelerator=auxiliary;analog=aux_analog;e.reg(7,analog);e.cost(3); }
        } else if(policy==5) { auxiliary=0;e.cost(1); }
        e.reg(5,auxiliary);e.reg(6,accelerator);
    }
    e.reg(2,auxiliary>0);x=0;e.cost(4);
    ps2::st8(e.control,auxiliary>0);
    unsigned history=car.control.accelerator_history;
    bool evaluate_response=true;
    if(!analog) {
        x=car.processed_accelerator;e.cost(2);
        if(accelerator) {
            e.reg(2,0x2d0000);e.reg(1,one);b=one;a=ps2::ld32(0x2d4930);
            x=ps2::fp::add(x,a);e.condition(ps2::fp::key(one)<ps2::fp::key(x));e.cost(9);
            if(c.fcr31&ps2::kFpuCondition)x=one;
            e.reg(2,2);e.cost(2);
            if(auxiliary) { history=2;e.reg(3,2);e.cost(3); }
            else { history=1;e.reg(2,1);e.reg(3,1);e.cost(4); }
            ps2::st8(e.control+2,history);e.cost(2);evaluate_response=false;
        } else {
            e.reg(2,0x2d0000);b=0;a=fall;x=ps2::fp::sub(x,a);
            const bool clamp=ps2::fp::key(x)<ps2::fp::key(b);e.condition(clamp);e.cost(8);
            if(clamp) { history=0;ps2::st8(e.control+2,0);x=b;e.cost(4); }
            e.reg(3,history);e.reg(2,2);e.cost(1);
            e.reg(2,1);e.cost(2);
            if(history==2) { ps2::st8(e.control,1);e.cost(1); }
            e.cost(2);evaluate_response=!history;
        }
    } else {
        e.reg(3,0);e.cost(2);
        if(accelerator) {
            q=ps2::fp::cvt_s_w(accelerator);e.reg(1,one);z=q12;b=one;a=floor;
            x=ps2::fp::mul(q,z);ps2::st8(e.control+2,0);
            b=ps2::fp::sub(b,x);a=ps2::fp::mul(a,b);x=ps2::fp::add(x,a);e.cost(13);
            e.cost(2);
        } else {
            e.reg(3,history);e.reg(2,0x2d0000);e.cost(3);
            if(history) {
                b=car.processed_accelerator;a=fall;z=0;x=ps2::fp::sub(b,a);
                const bool clamp=ps2::fp::key(x)<=ps2::fp::key(z);e.condition(clamp);
                e.reg(2,2);e.cost(8);
                if(clamp) {
                    history=0;ps2::st8(e.control+2,0);x=z;e.reg(3,0);e.cost(3);
                    e.reg(2,2);e.cost(1);
                }
                e.reg(2,1);e.cost(2);
                if(history==2) { ps2::st8(e.control,1);e.cost(1); }
                e.cost(2);evaluate_response=!history;
            }
        }
    }
    if(evaluate_response) {
        e.reg(3,cmd.mode);e.reg(2,4);e.cost(4);
        if(cmd.mode==4)e.response(0x49d060,0x1e4ad4);
    }
    ps2::st32(e.car+0x13ac,x);
    // Brake uses a SIGNED halfword. Digital nonzero is not a magnitude; analog
    // negative and >1 inputs are deliberately not generically saturated.
    e.reg(2,static_cast<std::int64_t>(cmd.brake));e.cost(4);
    if(!(cmd.flags&4)) {
        e.reg(2,0x2d0000);e.cost(2);
        a=car.processed_brake;
        bool clamp;
        if(cmd.brake) {
            b=ps2::ld32(0x2d4938);e.reg(1,one);z=one;a=ps2::fp::add(a,b);
            clamp=ps2::fp::key(z)<ps2::fp::key(a);e.cost(8);
        } else {
            b=ps2::ld32(0x2d493c);z=0;a=ps2::fp::sub(a,b);
            clamp=ps2::fp::key(a)<ps2::fp::key(z);e.cost(7);
        }
        e.condition(clamp);ps2::st32(e.car+0x13b0,a);e.cost(2);
        if(clamp) { ps2::st32(e.car+0x13b0,z);e.cost(1); }
        else e.cost(2);
    } else {
        e.reg(1,q12);z=q12;a=ps2::fp::cvt_s_w(static_cast<std::int32_t>(cmd.brake));b=0;
        x=ps2::fp::mul(a,z);const bool zero=ps2::fp::key(x)==ps2::fp::key(b);
        e.condition(zero);e.reg(3,cmd.mode);e.cost(10);
        if(!zero) {
            e.reg(1,one);a=one;b=floor;a=ps2::fp::sub(a,x);
            b=ps2::fp::mul(b,a);x=ps2::fp::add(x,b);e.cost(6);
        }
        e.reg(2,4);e.cost(3);
        if(cmd.mode==4)e.response(0x49d070,0x1e4b9c);
        ps2::st32(e.car+0x13b0,x);e.cost(1);
    }
    e.reg(2,car.auxiliary_suppression);c.pc=0x1e4ba8;
}
std::uint64_t fingerprint(unsigned start,unsigned end) {
    std::uint64_t h=14695981039346656037ull;
    for(unsigned p=start;p<end;++p)h=(h^ps2::ld8(p))*1099511628211ull;
    return h;
}
}
bool profile_matches() {
    // Whole bounded instruction/helper/dispatch fingerprints, not stock writable
    // response calibration. Filled from the identity-verified original ELF.
    return fingerprint(0x1e48fc,0x1e4ba8)==0x6138166f2b0e6cfeull &&
           fingerprint(0x1d92e0,0x1d93c0)==0x31302544155cf954ull &&
           fingerprint(0x33c6c0,0x33c6dc)==0xd0cc805a2a50d290ull &&
           fingerprint(0x1e4cb0,0x1e4e78)==0xd79ba29ed968508aull;
}
bool replace(ps2::Cpu &c,unsigned depth) {
    if(!enabled)return false;
    const unsigned car=c.r[23].w[0],command=c.r[18].w[0];
    const auto overlap=[](unsigned a,unsigned n,unsigned b,unsigned m) {return a<b+m&&b<a+n;};
    // Observed low-RAM commands are activation-local, not global BSS buffers.
    // Verify the actual manual wrapper frames, never an absolute command address.
    // Short-circuit bounds before reading the saved-register/return slots.
    const unsigned sp=c.r[29].w[0];
    const bool stack_command=sp>=0x400000 && !(sp&15) &&
        sp<=0x500000-272 && c.r[29].d[0]==sp && command==sp+208 &&
        !overlap(sp,272,0x49d060,0x50) &&
        ps2::ld64(sp)==car && ps2::ld64(sp+128)==0x1e4cc8 &&
        ps2::ld64(command-32)==car+0xf84 &&
        ps2::ld64(command-16)==0x1e4dfc && ps2::ld64(command+48)==0x1f3b6c;
    if(depth>=ps2::kMaxDepth || c.budget<std::numeric_limits<int>::min()+2048 ||
       (car&3)||(command&1)||car>0x2000000-sizeof(CarPartial)||command>0x2000000-sizeof(CommandPartial)||
       c.r[16].d[0]!=car+0xf84 || c.r[19].d[0]!=car+0x1304 || c.r[28].d[0]!=0x3579f0 ||
       overlap(car,sizeof(CarPartial),command,sizeof(CommandPartial)) ||
       overlap(car,sizeof(CarPartial),0x100000,0x400000) ||
       (overlap(command,sizeof(CommandPartial),0x100000,0x400000)&&!stack_command) || !profile_matches()) {
        ++counts.fallback;return false;
    }
    const auto state=read<CarPartial>(car);
    if(c.r[3].sd[0]!=state.control_kind) { ++counts.fallback;return false; }
    const auto cmd=read<CommandPartial>(command);
    Execution e{c,car,command,car+0x1304,depth};process(e,state,cmd);
    ++counts.replaced;return true;
}
} // namespace gt3::pedals
