// Independent generated wrapper/suffix/consumers, never clean downstream code.
#include "gt3_clean_pedals.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
namespace {
constexpr unsigned car=0x600000,command=0x502000,race=0x700000,knots=0x710000;
void f(unsigned a,float v){ps2::st32(a,std::bit_cast<unsigned>(v));}
void compare(unsigned entry,unsigned case_id) {
    ps2::Cpu before{};before.pc=entry;before.budget=1000000;before.r[4].d[0]=car;before.r[5].d[0]=command;
    before.r[28].d[0]=0x3579f0;before.r[29].d[0]=0x800000;before.r[31].d[0]=0x1000000;
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+0x2000000);
    auto original=before;gt3::pedals::enabled=false;ps2::call(original,entry,0);
    if(original.pc!=0x1000000||original.r[29].w[0]!=0x800000)std::abort();
    const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+0x2000000);
    std::memcpy(ps2::g_ram,initial.data(),initial.size());
    auto clean=before;gt3::pedals::enabled=true;ps2::call(clean,entry,0);gt3::pedals::enabled=false;
    if(std::memcmp(&clean,&original,sizeof clean)||std::memcmp(ps2::g_ram,expected.data(),expected.size())) {
        std::fprintf(stderr,"FAIL pedal whole-wrapper/consumer case=%u entry=%08x\n",case_id,entry);std::abort();
    }
}
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;
    if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    unsigned cases=0;
    for(unsigned mode:{0u,4u})for(unsigned flags:{0u,2u,4u,8u,14u})
    for(unsigned policy:{0u,1u,2u,3u,4u,5u,6u,7u,255u})
    for(unsigned history:{0u,1u,2u,255u})for(unsigned suppression:{0u,65535u})
    for(unsigned pressure:{0u,4096u,65535u}) {
        std::memset(ps2::g_ram+car,0,0x1800);std::memset(ps2::g_ram+race,0,0xb800);
        std::memset(ps2::g_ram+command,0,16);std::memset(ps2::g_ram+0x49d060,0,32);
        ps2::st32(car+4,race);f(car+0xec0,1.f/60);f(car+0x68,.5f);
        f(car+0x13ac,.5f);f(car+0x13b0,.5f);ps2::st8(car+0x1306,history);
        ps2::st8(car+0x13e5,policy);ps2::st16(car+0x14ba,suppression);
        ps2::st8(command,flags);ps2::st8(command+1,mode);
        ps2::st16(command+8,pressure);ps2::st16(command+10,pressure);ps2::st16(command+12,pressure);
        for(unsigned i=0;i<3;++i) {
            unsigned d=car+0x6c+i*0x3c,k=knots+i*16;
            ps2::st16(d,2);ps2::st32(d+4,k);ps2::st32(d+8,k+8);
            f(k,0);f(k+4,100);f(k+8,.5f);f(k+12,.5f);
        }
        compare(0x1e4cb0,cases);compare(0x1e6ec8,cases);
        f(car+0xe38,1);f(car+0xe3c,1);f(car+0xe40,1);
        ps2::st16(car+0x1d4,8000);f(car+0x13cc,100);f(car+0x2bc,1);f(car+0x1434,1);
        compare(0x1e7500,cases);++cases;
    }
    if(gt3::pedals::counts.replaced!=cases)std::abort();
    std::printf("Pedal wrapper/generated coupling/original brake+engine consumers PASS: %u cases, %u complete CPU+32MiB differentials\n",cases,cases*3);
}
