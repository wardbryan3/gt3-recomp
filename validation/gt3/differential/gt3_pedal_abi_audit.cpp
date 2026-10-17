// Original-only interior ABI/cost audit. Requires a disposable generated unit
// with test entry 60000 -> 001E48FC and a return checkpoint at 001E4BA8.
#include "ps2/generated.hpp"
#ifdef GT3_PEDAL_DIFFERENTIAL
#include "gt3_clean_pedals.hpp"
#include <limits>
#include <vector>
#endif
#include "ps2/system.hpp"
#include <array>
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
void register_generated_code();
namespace gen { void unit_0039(ps2::Cpu &, unsigned, unsigned); }
bool gt3_pedal_audit_stop = true;
namespace {
constexpr unsigned car=0x600000, command=0x502000, stack=0x800000;
unsigned rng=0x50454431;
unsigned random_word() { rng^=rng<<13; rng^=rng>>17; rng^=rng<<5; return rng; }
void require(bool ok, const char *why, unsigned i) {
    if (!ok) { std::fprintf(stderr,"FAIL pedal original ABI case=%u: %s\n",i,why); std::exit(1); }
}
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;
    register_generated_code();unsigned entry;
    if(!ps2::load_elf(argv[1],entry))return 1;
    constexpr std::array<unsigned,12> floats={0,0x80000000,1,0x80000001,0x3f000000,
        0x3f800000,0xbf800000,0x7f800000,0xff800000,0x7fc00000,0xffc00000,0x7f7fffff};
    constexpr std::array<unsigned,8> pressure={0,1,15,16,4095,4096,32768,65535};
    unsigned minimum=100000,maximum=0;
    constexpr unsigned cases=131072;
    for(unsigned i=0;i<cases;++i) {
        const unsigned command=(i&1)?((i&2)?0x49af40:0x49af50):0x502000;
        // Low-RAM fixtures now supply the proven caller frame, not the obsolete
        // absolute-address exception. Assertions and semantic coverage unchanged.
        const unsigned stack=(i&1)?command-208:0x800000;
        for(unsigned j=0;j<0x1800;++j)ps2::st8(car+j,random_word());
        for(unsigned j=0;j<16;++j)ps2::st8(command+j,random_word());
        for(unsigned j=0;j<512;++j)ps2::st8(stack+j,random_word());
        const unsigned policy=(i>>4)&255,flags=i&15,mode=(i&256)?4:0;
        ps2::st8(car+0x136d,0);ps2::st8(car+0x14b8,0);ps2::st8(car+0x13e5,policy);
        ps2::st16(car+0x14ba,(i&512)?0xffff:0);
        ps2::st32(car+0x13ac,floats[random_word()%floats.size()]);
        ps2::st32(car+0x13b0,floats[random_word()%floats.size()]);
        ps2::st8(car+0x1306,(i>>10)&3);
        ps2::st8(command,flags);ps2::st8(command+1,mode);
        for(unsigned off:{8u,10u,12u})ps2::st16(command+off,pressure[random_word()%pressure.size()]);
        for(unsigned d:{0x49d060u,0x49d070u}) {
            ps2::st32(d,(i>>12)%4);
            for(unsigned off:{4u,8u,12u})ps2::st32(d+off,floats[random_word()%floats.size()]);
        }
        if(i>=32768) {
            ps2::st8(car+0x136d,random_word());ps2::st8(car+0x14b8,(i&32)?0:random_word());
            ps2::st8(car+0x1306,random_word());ps2::st8(command,random_word());
            ps2::st8(command+1,(i&64)?4:random_word());
            for(unsigned off:{8u,10u,12u})ps2::st16(command+off,(i&128)?random_word():0);
            for(unsigned address:{0x352990u,0x2d4930u,0x2d4934u,0x2d4938u,0x2d493cu})
                ps2::st32(address,floats[random_word()%floats.size()]);
            for(unsigned d:{0x49d060u,0x49d070u})ps2::st32(d,(i&256)?random_word():i%4);
        }
        ps2::Cpu c{};
        for(unsigned off=0;off<sizeof c;++off)reinterpret_cast<unsigned char *>(&c)[off]=random_word();
        const unsigned depth=i%ps2::kMaxDepth;
        c.pc=0x1e48fc;c.budget=(i&1024)?-1000:100000;
        ps2::set32(c.r[3],static_cast<int>(static_cast<signed char>(ps2::ld8(car+0x136d))));ps2::set32(c.r[16],car+0xf84);ps2::set32(c.r[18],command);
        ps2::set32(c.r[19],car+0x1304);ps2::set32(c.r[23],car);
        ps2::set32(c.r[28],0x3579f0);ps2::set32(c.r[29],stack);
        if(i&1) {
            ps2::st64(stack,car);ps2::st64(stack+128,0x1e4cc8);
            ps2::st64(command-32,car+0xf84);ps2::st64(command-16,0x1e4dfc);
            ps2::st64(command+48,0x1f3b6c);
        }
        const auto before=c;
        std::array<unsigned char,0x1800> old_car;std::memcpy(old_car.data(),ps2::g_ram+car,old_car.size());
        std::array<unsigned char,512> old_stack;std::memcpy(old_stack.data(),ps2::g_ram+stack,old_stack.size());
        std::array<unsigned char,16> old_command;std::memcpy(old_command.data(),ps2::g_ram+command,16);
        std::array<unsigned char,32> old_descriptors;std::memcpy(old_descriptors.data(),ps2::g_ram+0x49d060,32);
        gen::unit_0039(c,60000,depth);
        require(c.pc==0x1e4ba8,"join PC",i);
        require(c.r[2].d[0]==ps2::ld16(car+0x14ba),"v0 suppression",i);
        const unsigned expected_policy=ps2::ld8(car+0x136d)==1||ps2::ld8(car+0x14b8)?0:policy;
        require(c.r[17].d[0]==expected_policy,"s1 policy",i);
        auto stable=c;
        for(unsigned r:{1u,2u,3u,4u,5u,6u,7u,8u,17u,31u})stable.r[r].d[0]=before.r[r].d[0];
        for(unsigned r:{0u,1u,2u,3u,12u})stable.f[r]=before.f[r];
        stable.pc=before.pc;stable.budget=before.budget;stable.fcr31=before.fcr31;
        require(!std::memcmp(&stable,&before,sizeof before),"complete stable CPU including high lanes/HI/LO/SA/FACC/VU/COP0",i);
        for(unsigned r=0;r<32;++r)if(!(r>=1&&r<=8)&&r!=17&&r!=31)
            require(!std::memcmp(&c.r[r],&before.r[r],16),"stable GPR",i);
        for(unsigned r=0;r<32;++r)if(r>3&&r!=12)require(c.f[r]==before.f[r],"stable FPR",i);
        require((c.fcr31&~ps2::kFpuCondition)==(before.fcr31&~ps2::kFpuCondition),"non-condition FCR31",i);
        require(!std::memcmp(old_stack.data(),ps2::g_ram+stack,512),"stack unchanged",i);
        require(!std::memcmp(old_command.data(),ps2::g_ram+command,16),"command unchanged",i);
        require(!std::memcmp(old_descriptors.data(),ps2::g_ram+0x49d060,32),"descriptor unchanged (null derivative)",i);
        for(unsigned off=0;off<old_car.size();++off)
            if(off!=0x1304&&off!=0x1306&&!(off>=0x13ac&&off<0x13b4))
                require(old_car[off]==ps2::ld8(car+off),"write outside mutation surface",i);
#ifdef GT3_PEDAL_DIFFERENTIAL
        std::array<unsigned char,0x1800> expected_car;
        std::memcpy(expected_car.data(),ps2::g_ram+car,expected_car.size());
        std::memcpy(ps2::g_ram+car,old_car.data(),old_car.size());
        auto clean=before;gt3::pedals::enabled=true;
        require(gt3::pedals::replace(clean,depth),"supported clean entry",i);
        if(std::memcmp(&clean,&c,sizeof c)) {
            for(unsigned r=0;r<32;++r)if(std::memcmp(&clean.r[r],&c.r[r],16))
                std::fprintf(stderr,"r%u clean=%016llx original=%016llx\n",r,
                    (unsigned long long)clean.r[r].d[0],(unsigned long long)c.r[r].d[0]);
            for(unsigned r=0;r<32;++r)if(clean.f[r]!=c.f[r])
                std::fprintf(stderr,"f%u clean=%08x original=%08x\n",r,clean.f[r],c.f[r]);
            std::fprintf(stderr,"budget clean=%d original=%d; fcr clean=%08x original=%08x\n",
                clean.budget,c.budget,clean.fcr31,c.fcr31);
            require(false,"complete CPU differential",i);
        }
        require(!std::memcmp(expected_car.data(),ps2::g_ram+car,expected_car.size()),"complete car differential",i);
        require(!std::memcmp(old_stack.data(),ps2::g_ram+stack,512),"clean stack unchanged",i);
        require(!std::memcmp(old_command.data(),ps2::g_ram+command,16),"clean command unchanged",i);
        require(!std::memcmp(old_descriptors.data(),ps2::g_ram+0x49d060,32),"clean descriptors unchanged",i);
        gt3::pedals::enabled=false;
#endif
        const unsigned cost=before.budget-c.budget;
        if(cost<minimum)minimum=cost;if(cost>maximum)maximum=cost;
    }
#ifdef GT3_PEDAL_DIFFERENTIAL
    ps2::Cpu valid{};valid.pc=0x1e48fc;valid.budget=1000;
    ps2::set32(valid.r[3],static_cast<int>(static_cast<signed char>(ps2::ld8(car+0x136d))));
    ps2::set32(valid.r[16],car+0xf84);ps2::set32(valid.r[18],command);
    ps2::set32(valid.r[19],car+0x1304);ps2::set32(valid.r[23],car);ps2::set32(valid.r[28],0x3579f0);
    unsigned guards=0;
    auto fallback=[&](ps2::Cpu candidate,unsigned depth=0) {
        const auto before=candidate;
        const std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+0x2000000);
        require(!gt3::pedals::replace(candidate,depth),"fallback taken",guards);
        require(!std::memcmp(&candidate,&before,sizeof before),"fallback complete CPU unchanged",guards);
        require(!std::memcmp(ps2::g_ram,ram.data(),ram.size()),"fallback complete RAM unchanged",guards);++guards;
    };
    gt3::pedals::enabled=false;fallback(valid);gt3::pedals::enabled=true;
    fallback(valid,ps2::kMaxDepth);
    auto bad=valid;bad.budget=std::numeric_limits<int>::min();fallback(bad);
    for(unsigned r:{16u,19u,28u,3u}) { bad=valid;bad.r[r].d[0]^=1;fallback(bad); }
    bad=valid;bad.r[23].d[0]=0x2000000;fallback(bad);
    bad=valid;bad.r[18].d[0]=0x2000000;fallback(bad);
    bad=valid;bad.r[18].d[0]=car+0x1304;fallback(bad);
    bad=valid;bad.r[18].d[0]=0x49d060;fallback(bad);
    for(unsigned address:{0x1e48fcu,0x1d92e0u,0x33c6c0u}) {
        const unsigned byte=ps2::ld8(address);ps2::st8(address,byte^1);fallback(valid);ps2::st8(address,byte);
    }
    // Structural negative cases must be mutation-free, including forged or
    // neighboring saved-register pointers at formerly hard-coded addresses.
    bad=valid;ps2::set32(bad.r[18],0x49af40);ps2::set32(bad.r[29],0x49af40-208);
    ps2::st64(0x49af40-208,car);ps2::st64(0x49af40-80,0x1e4cc8);
    ps2::st64(0x49af40-32,car+0xf84);ps2::st64(0x49af40-16,0x1e4dfc);ps2::st64(0x49af40+48,0x1f3b6c);
    for(unsigned address:{0x49af40-208,0x49af40-80,0x49af40-32,0x49af40-16,0x49af40+48}) {
        const auto w=ps2::ld64(address);ps2::st64(address,w^1);fallback(bad);ps2::st64(address,w);
    }
    auto wrong=bad;wrong.r[29].d[0]+=16;fallback(wrong);
    wrong=bad;wrong.r[18].d[0]+=16;fallback(wrong);
    wrong=bad;wrong.r[29].d[0]=0xffffffff;fallback(wrong);
    wrong=bad;wrong.r[29].d[0]=0x2000000;fallback(wrong);
    const auto owner=ps2::ld8(0x1e4cb0);ps2::st8(0x1e4cb0,owner^1);fallback(valid);ps2::st8(0x1e4cb0,owner);
    gt3::pedals::enabled=false;
    std::printf("Pedal default-OFF/profile/context/depth/budget/alias fallback PASS: %u cases, zero CPU/RAM mutations\n",guards);
#endif
    std::printf("Original generated pedal join audit PASS: %u cases; cost=%u..%u; complete mutation/stability checks\n",cases,minimum,maximum);
#ifdef GT3_PEDAL_DIFFERENTIAL
    std::printf("Clean pedal full-CPU/car/command/stack/descriptor/budget differential PASS: %u cases\n",cases);
#endif
}
