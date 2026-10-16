// Independent ORIGINAL generated body; fixture inputs never generate expected
// outputs. Scheduler wrapping below models API responses ONLY, not real timing.
#include "gt3_clean_transmission_speed.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <limits>
#include <vector>
void register_generated_code();
namespace gen {void oracle_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace {
unsigned object=0x600000,seed=0x4e804e80,cases=0,full=0,minimum=99999,maximum=0,rejections=0;
unsigned poll_calls=0;bool poll_yield=false;
unsigned random_word(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
void check(bool ok,const char *why){if(!ok){std::fprintf(stderr,"FAIL helper case=%u %s\n",cases,why);std::exit(1);}}
ps2::Cpu cpu(unsigned speed,int budget) {
    ps2::Cpu c{};for(unsigned i=0;i<sizeof c;++i)reinterpret_cast<unsigned char *>(&c)[i]=random_word();
    ps2::set32(c.r[4],object);ps2::set32(c.r[28],0x3579f0);c.f[12]=speed;c.budget=budget;c.pc=0x1e4e80;return c;
}
void compare(unsigned limit,unsigned rpm,unsigned speed,int budget=30000,bool whole=false) {
    ps2::st8(object+0x20a,limit);ps2::st16(object+0x236,rpm);const auto before=cpu(speed,budget);
    std::array<unsigned char,0x660> span;std::memcpy(span.data(),ps2::g_ram+object,span.size());
    std::vector<unsigned char> ram;
    if(whole || !(cases%1024)){ram.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);++full;}
    auto original=before;gen::oracle_unit_0039(original,47,0);
    if(!ram.empty())check(!std::memcmp(ps2::g_ram,ram.data(),ram.size()),"original wholeRAM readonly");
    auto clean=before;check(gt3::transmission_speed::replace(clean),"admission");
    if(std::memcmp(&clean,&original,sizeof clean)) {
        std::fprintf(stderr,"max=%u rpm=%u speed=%08x budget=%d/%d pc=%x/%x FCR=%08x/%08x\n",limit,rpm,speed,clean.budget,original.budget,clean.pc,original.pc,clean.fcr31,original.fcr31);
        for(unsigned i=0;i<32;++i)if(std::memcmp(&clean.r[i],&original.r[i],16))std::fprintf(stderr,"r%u %016llx/%016llx\n",i,(unsigned long long)clean.r[i].d[0],(unsigned long long)original.r[i].d[0]);
        check(false,"complete CPU/FCR/upper lanes/cost");
    }
    check(!std::memcmp(ps2::g_ram+object,span.data(),span.size()),"entire read span unchanged");
    if(!ram.empty())check(!std::memcmp(ps2::g_ram,ram.data(),ram.size()),"clean wholeRAM readonly");
    const unsigned cost=before.budget-original.budget;minimum=std::min(minimum,cost);maximum=std::max(maximum,cost);++cases;
}
void reject(ps2::Cpu c) {
    const auto before=c;const std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    check(!gt3::transmission_speed::replace(c),"required rejection");
    check(!std::memcmp(&c,&before,sizeof c)&&!std::memcmp(ps2::g_ram,ram.data(),ram.size()),"FULL CPU+RAM mutation-free fallback");++rejections;
}
}
extern "C" bool __wrap__ZN3ps27preemptERNS_3CpuE(ps2::Cpu &c) {++poll_calls;c.budget=9000;return poll_yield;}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    check(gt3::transmission_speed::profile_matches(),"original instruction fingerprint");gt3::transmission_speed::enabled=true;
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    constexpr unsigned scale_address=0x35040c;
    constexpr std::array<unsigned,18> bits={0,0x80000000,1,0x80000001,0x3f800000,0xbf800000,0x7f800000,0xff800000,0x7fc00000,0xffc00000,0x7f7fffff,0xff7fffff,0x00800000,0x80800000,0x3e800000,0x3e7fffff,0x3e800001,0x3dcccccd};
    for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,0x3f800000);
    // Complete unsigned-halfword domain, including RPM-500 negative/zero edges.
    for(unsigned rpm=0;rpm<65536;++rpm)for(unsigned speed:{0u,0x42200000u,0x49742400u})compare(6,rpm,speed);
    for(unsigned n=0;n<256;++n)for(unsigned ratio:bits) {
        for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,ratio);
        for(unsigned speed:bits)for(unsigned rpm:{0u,499u,500u,8000u,65535u})compare(n,rpm,speed);
    }
    for(unsigned scale:bits)for(unsigned ratio:bits) {
        ps2::st32(scale_address,scale);for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,ratio);
        for(unsigned speed:bits)for(unsigned n:{0u,1u,6u})for(unsigned rpm:{0u,499u,500u,501u,65535u})compare(n,rpm,speed);
    }
    // Threshold/neighbors construct INPUTS, never expected results. Nonuniform
    // ratios make successive search positions independently relevant.
    ps2::st32(scale_address,0x3f800000);
    for(unsigned i=1;i<255;++i)ps2::st32(object+0x264+4*i,ps2::fp::div(0x3f800000,ps2::fp::cvt_s_w(i)).value);
    for(unsigned rpm:{501u,65535u})for(unsigned i=1;i<255;++i) {
        unsigned threshold=ps2::fp::div(ps2::fp::cvt_s_w(rpm-500),ps2::ld32(object+0x264+4*i)).value;
        for(unsigned speed:{threshold-1,threshold,threshold+1})compare(255,rpm,speed,30000,true);
    }
    for(unsigned k=0;k<10000;++k) {
        for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,random_word());
        ps2::st32(scale_address,random_word());compare(random_word()&255,random_word()&65535,random_word());
    }
    for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,0x3f800000);
    ps2::st32(scale_address,0x3f800000);
    for(unsigned n=2;n<256;++n) {
        compare(n,8000,0x7f7fffff,16*n+16);compare(n,8000,0x7f7fffff,16*n+17);
        ps2::st8(object+0x20a,n);reject(cpu(0,16*n+15));
    }
    for(int budget:{0,-1,std::numeric_limits<int>::min()+32}) {
        for(unsigned n:{0u,1u})compare(n,8000,0,budget);
        compare(255,8000,0xbf800000,budget);
    }
    // Read at the admitted RAM upper edge; no wrap/slow/MMIO read is permitted.
    object=0x2000000-sizeof(gt3::transmission_speed::ObjectReadSpan);
    for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,0x3f800000);
    compare(255,65535,0x7f7fffff,4112,true);
    std::memcpy(ps2::g_ram+object,initial.data()+object,0x660);object=0x600000;
    std::memcpy(ps2::g_ram+object,initial.data()+object,0x660);ps2::st32(scale_address,ps2::load<unsigned>(initial.data()+scale_address));
    check(!std::memcmp(ps2::g_ram,initial.data(),initial.size()),"cumulative entire32MiB mutation surface");
    check(poll_calls==0,"no scheduler call in admitted domain");
    std::printf("Speed helper independent PASS cases=%u completeCPU=%u read-span=every-case whole32MiB=%u budget=%u..%u admitted-polls=0\n",cases,cases,full,minimum,maximum);
    auto valid=cpu(0,30000);gt3::transmission_speed::enabled=false;reject(valid);gt3::transmission_speed::enabled=true;
    for(unsigned r:{4u,28u}){auto c=valid;c.r[r].d[0]|=1ull<<32;reject(c);}
    for(unsigned address:{0u,0x4ffffcu,0x600001u,0x1fffffcu,0xffffffffu}){auto c=valid;c.r[4].d[0]=address;reject(c);}
    auto c=valid;c.budget=std::numeric_limits<int>::min();reject(c);
    const unsigned code=ps2::ld8(0x1e4e80);ps2::st8(0x1e4e80,code^1);reject(valid);ps2::st8(0x1e4e80,code);
    std::printf("Speed helper mutation-free completeCPU+32MiB fallback PASS cases=%u\n",rejections);
    // Controlled scheduler contract: both original backward-poll sites, yield
    // AND no-yield responses. No original instruction/control decision modified.
    for(unsigned i=0;i<255;++i)ps2::st32(object+0x264+4*i,0x3f800000);
    ps2::st8(object+0x20a,6);ps2::st16(object+0x236,8000);ps2::st32(scale_address,0x3f800000);
    unsigned scheduling=0;
    for(bool yield:{false,true})for(unsigned speed:{0u,0x7f7fffffu}) {
        poll_yield=yield;auto before=cpu(speed,-1);auto original=before;poll_calls=0;gen::oracle_unit_0039(original,47,0);check(poll_calls==1,"original poll");
        auto fallback=before;poll_calls=0;check(!gt3::transmission_speed::replace(fallback),"low-budget original fallback");check(!std::memcmp(&fallback,&before,sizeof before),"pre-poll CPU not touched");
        gen::oracle_unit_0039(fallback,47,0);check(poll_calls==1&&!std::memcmp(&original,&fallback,sizeof original),"original poll fullCPU fallback parity");
        if(yield) {
            check(original.pc==(speed?0x1e4ec9u:0x1e4e9du),"two original unwind destinations");
            original.pc&=~ps2::kUnwind;fallback.pc&=~ps2::kUnwind;
            gen::oracle_unit_0039(original,speed?49:48,0);ps2::dispatch(fallback,0,0);
            check(!std::memcmp(&original,&fallback,sizeof original),"original resume completeCPU parity");
        }
        ++scheduling;
    }
    std::printf("Speed helper controlled scheduler/fallback/resume PASS cases=%u; NOT native scheduler timing proof\n",scheduling);
}
