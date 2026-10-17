// Whole original manual wrapper -> original coupling -> original brake/engine.
// Neither oracle nor downstream consumers are implemented in clean C++ here.
#include "gt3_clean_handbrake.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <algorithm>
#include <array>
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
bool gt3_pedal_audit_stop=false;
namespace {
constexpr unsigned car=0x600000,command=0x502000,race=0x700000,knots=0x710000;
void f(unsigned a,float v){ps2::st32(a,std::bit_cast<unsigned>(v));}
void check(bool x,const char *why,unsigned n){if(!x){std::fprintf(stderr,"FAIL wrapper %u: %s\n",n,why);std::exit(1);}}
}
int main(int argc,char **argv){
 if(argc!=2)return 2;register_generated_code();unsigned entry;if(!ps2::load_elf(argv[1],entry))return 1;
 ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
 unsigned cases=0;
 for(unsigned analog:{0u,16u})for(unsigned input:{0u,1u,455u,456u,3185u,3186u,4095u,4096u,32767u,32768u,65535u})
 for(unsigned history:{0u,0x3f000000u,0x3f800000u})for(unsigned policy=0;policy<9;++policy)
 for(unsigned context=0;context<8;++context){
    std::memset(ps2::g_ram+car,0,0x1800);std::memset(ps2::g_ram+race,0,0xb800);
    std::memset(ps2::g_ram+command,0,16);std::memset(ps2::g_ram+0x49d060,0,32);
    ps2::st32(car+4,race);f(car+0xec0,1.f/60);f(car+0x68,.5f);
    f(car+0x13ac,.5f);f(car+0x13b0,.5f);ps2::st32(car+0x13b4,history);
    ps2::st8(car+0x13e5,policy);ps2::st8(car+0x20b,context&1);
    ps2::st8(car+0x13bb,(context>>1)&1);ps2::st16(car+0x14ba,(context&4)?65535:0);
    ps2::st16(car+0x1d6,8000);ps2::st16(car+0x1414,4000);
    ps2::st8(command,analog|6);ps2::st8(command+1,(context&2)?4:0);
    ps2::st8(command+2,context&1);ps2::st16(command+8,2048);ps2::st16(command+10,(context&2)?2048:0);
    ps2::st16(command+12,(context&1)?1:0);ps2::st16(command+14,input);
    for(unsigned i=0;i<3;++i){unsigned d=car+0x6c+i*0x3c,k=knots+i*16;
        ps2::st16(d,2);ps2::st32(d+4,k);ps2::st32(d+8,k+8);
        f(k,0);f(k+4,100);f(k+8,.5f);f(k+12,.5f);}
    f(car+0xe38,1.25f);f(car+0xe3c,2.5f);f(car+0xe40,3.0f);
    ps2::st16(car+0x1d4,8000);f(car+0x13cc,100);f(car+0x2bc,1);f(car+0x1434,1);
    ps2::Cpu before{};before.pc=0x1e4cb0;before.budget=1000000;
    ps2::set32(before.r[4],car);ps2::set32(before.r[5],command);
    ps2::set32(before.r[28],0x3579f0);ps2::set32(before.r[29],0x800000);ps2::set32(before.r[31],0x1000000);
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+0x2000000);
    auto execute=[&](bool clean){auto c=before;gt3::handbrake::enabled=clean;
        for(unsigned address:{0x1e4cb0u,0x1e6ec8u,0x1e7500u}){
            ps2::set32(c.r[4],car);ps2::set32(c.r[5],command);ps2::set32(c.r[31],0x1000000);
            ps2::call(c,address,0);check(c.pc==0x1000000,"outgoing PC",cases);
            if(address==0x1e4cb0 && context==1 && policy!=3 && policy!=6){
                const bool inhibits=ps2::fp::key(ps2::ld32(0x350408))<ps2::fp::key(ps2::ld32(car+0x13b4));
                check(ps2::ld32(car+0x139c)==(inhibits?0u:0x3f800000u),"original coupling threshold effect",cases);
            }
            if(address==0x1e6ec8)for(unsigned i=0;i<4;++i){
                auto expected=ps2::fp::mul(ps2::ld32(car+0x1074+i*0xa4),ps2::ld32(car+0xe38+(i>>1)*4));
                if(i>=2)expected=ps2::fp::add(expected,ps2::fp::mul(ps2::ld32(car+0x13b4),ps2::ld32(car+0xe40)));
                check(ps2::ld32(car+0x1274+i*0x24)==expected,"rear-only original brake contribution",cases);
            }
        }return c;};
    const auto original=execute(false);const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+0x2000000);
    std::memcpy(ps2::g_ram,initial.data(),initial.size());const auto clean=execute(true);
    check(!std::memcmp(&original,&clean,sizeof clean),"complete outgoing CPU/budget",cases);
    check(!std::memcmp(ps2::g_ram,expected.data(),expected.size()),"complete 32MiB RAM",cases);
    ++cases;
 }
 check(gt3::handbrake::counts.replaced==cases&&gt3::handbrake::counts.fallback==0,"actual substitutions",cases);
 std::printf("Handbrake original wrapper/coupling/brake/engine PASS cases=%u full-CPU+32MiB-comparisons=%u rear-only-effects=%u\n",cases,cases,cases*8);
}
