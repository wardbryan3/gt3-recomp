// Entire original dispatch/selection/transition/commit chain remains generated,
// except the gated MT entry. This is an integrated ABI test, not a new gearbox.
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
namespace gen {void oracle_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace gt3::transmission_validation {unsigned entry_depth=0;}
namespace {
void check(bool ok,const char *why,unsigned n){if(!ok){std::fprintf(stderr,"FAIL wrapper %u %s\n",n,why);std::exit(1);}}
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    constexpr unsigned car=0x600000,sp=0x800000;unsigned cases=0;
    for(unsigned state=0;state<4;++state)for(unsigned selected=0;selected<7;++selected)
    for(unsigned inhibition:{0u,1u,255u})for(unsigned shift:{0u,1u,255u})
    for(unsigned auxiliary:{0u,1u})for(unsigned accelerator:{0u,0x3f800000u}) {
        std::memset(ps2::g_ram+car,0x5a,0x1500);
        ps2::st8(car+0x136d,0);ps2::st8(car+0x14b8,0);ps2::st16(car+0x14ba,0);ps2::st8(car+0x13e5,1);
        ps2::st8(car+0x20a,6);ps2::st16(car+0x236,8000);ps2::st8(car+0x1304,auxiliary);ps2::st8(car+0x1305,shift);
        ps2::st8(car+0x13bb,state);ps2::st8(car+0x13ba,selected);ps2::st8(car+0x13be,inhibition);
        ps2::st32(car+0x13ac,accelerator);ps2::st32(car+0x140c,0x40c00000);
        for(unsigned i=0;i<7;++i)ps2::st32(car+0x264+i*4,0x3f800000);
        ps2::Cpu before{};for(unsigned i=0;i<sizeof before;++i)reinterpret_cast<unsigned char *>(&before)[i]=static_cast<unsigned char>((i*73+cases*31));
        before.pc=0x1e77e0;before.budget=1000000;ps2::set32(before.r[4],car);ps2::set32(before.r[29],sp);ps2::set32(before.r[28],0x3579f0);ps2::set32(before.r[31],0x12345678);
        const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
        auto original=before;gen::oracle_unit_0039(original,153,0);
        const std::vector<unsigned char> expected(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
        std::memcpy(ps2::g_ram,initial.data(),initial.size());auto clean=before;
        gt3::transmission::enabled=true;ps2::call(clean,0x1e77e0,0);
        check(!std::memcmp(&clean,&original,sizeof clean),"complete CPU/ABI/dynamic-cost",cases);
        check(!std::memcmp(ps2::g_ram,expected.data(),expected.size()),"whole32MiB RAM + untouched downstream",cases);
        if(state==0)check(ps2::ld8(car+0x13bb)==0,"selection does not engage state0",cases);
        ++cases;
    }
    check(gt3::transmission::counts.replaced==cases && gt3::transmission::counts.fallback==0,"actual gated substitutions",cases);
    std::printf("MT integrated original001E77E0->5690->clean5458->original4E78 PASS cases=%u completeCPU+32MiB=%u substitutions=%llu fallback=0\n",cases,cases,(unsigned long long)gt3::transmission::counts.replaced);
}
