// Four-way original / unchanged Frozen selector / helper / BOTH composition.
// Original 77E0 orchestration, policy routing and 4E78 commit stay generated.
#include "gt3_clean_transmission_speed.hpp"
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
namespace gen {void oracle_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace {void check(bool b,const char *why,unsigned n){if(!b){std::fprintf(stderr,"FAIL composition %u %s\n",n,why);std::exit(1);}}}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    constexpr unsigned car=0x600000;unsigned cases=0;unsigned long long selectors[4]{},helpers[4]{};
    for(unsigned state=0;state<4;++state)for(unsigned index=0;index<7;++index)
    for(unsigned count:{0u,1u,255u})for(unsigned shift:{0u,1u,255u})
    for(unsigned aux:{0u,1u})for(unsigned accel:{0u,0x3f800000u}) {
        std::memset(ps2::g_ram+car,0x5a,0x1500);
        ps2::st8(car+0x136d,0);ps2::st8(car+0x14b8,0);ps2::st16(car+0x14ba,0);ps2::st8(car+0x13e5,1);
        ps2::st8(car+0x20a,6);ps2::st16(car+0x236,8000);ps2::st8(car+0x1304,aux);ps2::st8(car+0x1305,shift);
        ps2::st8(car+0x13bb,state);ps2::st8(car+0x13ba,index);ps2::st8(car+0x13be,count);
        ps2::st32(car+0x13ac,accel);ps2::st32(car+0x140c,0x40c00000);
        for(unsigned i=0;i<7;++i)ps2::st32(car+0x264+4*i,0x3f800000);
        ps2::Cpu before{};for(unsigned j=0;j<sizeof before;++j)reinterpret_cast<unsigned char *>(&before)[j]=(j*71+cases*31)&255;
        before.pc=0x1e77e0;before.budget=1000000;ps2::set32(before.r[4],car);ps2::set32(before.r[29],0x800000);ps2::set32(before.r[28],0x3579f0);ps2::set32(before.r[31],0x12345678);
        const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
        auto original=before;gen::oracle_unit_0039(original,153,0);
        const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
        for(unsigned mode=0;mode<4;++mode) {
            std::memcpy(ps2::g_ram,initial.data(),initial.size());auto actual=before;
            gt3::transmission::enabled=mode&1;gt3::transmission_speed::enabled=mode&2;
            const auto s=gt3::transmission::counts;const auto h=gt3::transmission_speed::counts;
            ps2::call(actual,0x1e77e0,0);
            check(!std::memcmp(&actual,&original,sizeof actual),"complete CPU/FCR/ABI/cost",cases);
            check(!std::memcmp(ps2::g_ram,expected.data(),expected.size()),"whole32MiB+original commit/state",cases);
            check(!gt3::transmission::counts.fallback && !gt3::transmission_speed::counts.fallback,"unexpected fallback",cases);
            selectors[mode]+=gt3::transmission::counts.replaced-s.replaced;helpers[mode]+=gt3::transmission_speed::counts.replaced-h.replaced;
            if(state==0)check(ps2::ld8(car+0x13bb)==0,"selection must not engage state0",cases);
        }
        ++cases;
    }
    check(cases==1008 && selectors[0]==0 && selectors[1]==1008 && selectors[2]==0 && selectors[3]==1008,"actual selector routes",cases);
    check(helpers[0]==0 && helpers[1]==0 && helpers[2]==36 && helpers[3]==36,"actual helper direct AND Frozen-dispatch routes",cases);
    std::printf("Four-way composition PASS cases=%u completeCPU+32MiB=%u selector=[0,1008,0,1008] helper=[0,0,36,36] fallback=0\n",cases,cases*4);
}
