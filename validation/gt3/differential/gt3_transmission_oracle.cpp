// Independent generated-original oracle. The clean implementation is never an
// expected-value generator. Synthetic fixture writes are not live game edits.
#include "gt3_clean_transmission.hpp"
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
constexpr unsigned car=0x600000,request=car+0x1304;
unsigned sp=0x510000;
unsigned seed=0x54585458,cases=0,full=0,minimum=100000,maximum=0;
unsigned rnd(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
void require(bool ok,const char *why){if(!ok){std::fprintf(stderr,"FAIL case=%u %s\n",cases,why);std::exit(1);}}
void compare(unsigned selected,unsigned maximum_index,unsigned inhibition,unsigned auxiliary,unsigned shift,unsigned accelerator=0,unsigned speed=0,unsigned rpm=8000,int budget=20000,unsigned depth=0) {
    ps2::st8(car+0x13ba,selected);ps2::st8(car+0x20a,maximum_index);ps2::st8(car+0x13be,inhibition);
    ps2::st8(request,auxiliary);ps2::st8(request+1,shift);ps2::st32(car+0x13ac,accelerator);ps2::st32(car+0x140c,speed);
    ps2::st16(car+0x236,rpm);
    ps2::st8(car+0x13bb,rnd());ps2::st8(car+0x13e5,rnd());
    ps2::Cpu before{};for(unsigned i=0;i<sizeof before;++i)reinterpret_cast<unsigned char *>(&before)[i]=rnd();
    ps2::set32(before.r[4],car);ps2::set32(before.r[5],request);ps2::set32(before.r[29],sp);ps2::set32(before.r[28],0x3579f0);
    before.pc=0x1e5458;before.budget=budget;
    std::array<unsigned char,16> stack;std::memcpy(stack.data(),ps2::g_ram+sp-16,16);
    const unsigned old_count=ps2::ld8(car+0x13be);
    auto original=before;gen::oracle_unit_0039(original,60,depth);
    std::array<unsigned char,0x1500> expected_car;std::memcpy(expected_car.data(),ps2::g_ram+car,expected_car.size());
    std::array<unsigned char,16> expected_stack;std::memcpy(expected_stack.data(),ps2::g_ram+sp-16,16);
    std::vector<unsigned char> expected_ram;
    if((cases%1024)==0){expected_ram.assign(ps2::g_ram,ps2::g_ram+0x2000000);++full;}
    ps2::st8(car+0x13be,old_count);std::memcpy(ps2::g_ram+sp-16,stack.data(),16);
    auto clean=before;require(gt3::transmission::replace_manual_selector(clean,depth),"admission");
    if(std::memcmp(&clean,&original,sizeof clean)) {
        std::fprintf(stderr,"selected=%u max=%u count=%u aux=%u shift=%u accel=%08x budgets=%d/%d pc=%x/%x\n",selected,maximum_index,inhibition,auxiliary,shift,accelerator,clean.budget,original.budget,clean.pc,original.pc);
        for(unsigned i=0;i<32;++i)if(std::memcmp(&clean.r[i],&original.r[i],sizeof clean.r[i]))std::fprintf(stderr,"r%u %016llx/%016llx\n",i,(unsigned long long)clean.r[i].d[0],(unsigned long long)original.r[i].d[0]);
        require(false,"FULL CPU/ABI/budget differential");
    }
    require(!std::memcmp(ps2::g_ram+car,expected_car.data(),expected_car.size()),"entire car + padding");
    require(!std::memcmp(ps2::g_ram+sp-16,expected_stack.data(),16),"entire stack frame");
    if(!expected_ram.empty())require(!std::memcmp(ps2::g_ram,expected_ram.data(),expected_ram.size()),"whole32MiB");
    unsigned cost=before.budget-original.budget;minimum=std::min(minimum,cost);maximum=std::max(maximum,cost);++cases;
}
}
int main(int argc,char **argv) {
    if(argc!=2&&argc!=3)return 2;register_generated_code();unsigned entry;
    if(!ps2::load_elf(argv[1],entry))return 1;
    if(argc==3){FILE *f=std::fopen(argv[2],"rb");if(!f)return 2;require(std::fread(ps2::g_ram,1,0x2000000,f)==0x2000000,"native-memory seed");std::fclose(f);}
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    require(gt3::transmission::profile_matches(),"original code fingerprints");gt3::transmission::enabled=true;
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+0x2000000);
    // Selected x inhibition x signed direction: all byte states and rearm values.
    for(unsigned i=0;i<256;++i)for(unsigned h=0;h<256;++h)for(unsigned s:{0u,1u,255u})compare(i,6,h,0,s);
    // Independent exhaustive configured limit x selected, including invalid indices.
    for(unsigned m=0;m<256;++m)for(unsigned i=0;i<256;++i)for(unsigned s:{0u,1u,127u,128u,255u})compare(i,m,0,0,s);
    // Full signed byte domains; auxiliary priority and inhibition bypass.
    for(unsigned q=0;q<256;++q)for(unsigned i=0;i<256;++i){compare(i,6,0,0,q);compare(i,6,255,q,128);}
    constexpr std::array<unsigned,18> fp={0,0x80000000,1,0x80000001,0x3f800000,0xbf800000,0x7f800000,0xff800000,0x7fc00000,0xffc00000,0x7f7fffff,0xff7fffff,0x00800000,0x80800000,0x3e800000,0x3e7fffff,0x3e800001,0x3dcccccd};
    for(unsigned a:fp)for(unsigned v:fp)for(unsigned n:{0u,1u,2u,6u,255u})for(unsigned rpm:{0u,499u,500u,8000u,65535u}) {
        for(unsigned j=1;j<256;++j)ps2::st32(car+0x264+4*j,fp[(j+a+v)%fp.size()]);
        compare(0,n,12,0,255,a,v,rpm);
    }
    // Force the entire 254-iteration original speed traversal, not only early
    // FP exits, and retain original comparisons for zero/invalid limits.
    for(unsigned j=1;j<256;++j)ps2::st32(car+0x264+4*j,0x3f800000);
    for(unsigned n:{0u,1u,2u,6u,255u})for(unsigned rpm:{0u,500u,65535u})for(unsigned v:fp)
        compare(0,n,0,0,1,0x3f800000,v,rpm);
    for(int budget:{0,-1,100,std::numeric_limits<int>::min()+128})for(unsigned depth:{0u,ps2::kMaxDepth})
        for(unsigned i:{0u,1u,255u})for(unsigned h:{0u,1u,255u})for(unsigned s:{0u,1u,255u})
            compare(i,6,h,0,s,0,0,8000,budget,depth);
    // Independently observed native stack is in writable RAM above the original
    // ELF's loaded end3531E3, not in the overly broad first rejected guard.
    sp=0x49af30;
    for(unsigned i:{0u,1u,6u,255u})for(unsigned s:{0u,1u,255u})compare(i,6,0,0,s);
    compare(0,6,0,0,1,0x3f800000,0x7f7fffff,8000,160);
    std::memcpy(ps2::g_ram+sp-16,initial.data()+sp-16,16);sp=0x510000;
    // Restore ONLY fixture-owned bytes. Detect any cumulative out-of-contract RAM
    // mutation; complete car/frame are already compared at every individual case.
    std::memcpy(ps2::g_ram+car,initial.data()+car,0x1500);std::memcpy(ps2::g_ram+sp-16,initial.data()+sp-16,16);
    require(!std::memcmp(ps2::g_ram,initial.data(),initial.size()),"cumulative32MiB mutation surface");
    std::printf("MT selector differential PASS cases=%u CPU=complete car+padding=every-case stack=every-case full32MiB=%u budget=%u..%u original_speed_calls=%llu\n",cases,full,minimum,maximum,(unsigned long long)gt3::transmission::counts.original_speed_calls);
    ps2::Cpu valid{};valid.budget=20000;ps2::set32(valid.r[4],car);ps2::set32(valid.r[5],request);ps2::set32(valid.r[29],sp);ps2::set32(valid.r[28],0x3579f0);
    unsigned rejected=0;
    auto reject=[&](ps2::Cpu c,unsigned depth=0){const auto before=c;std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+0x2000000);
        require(!gt3::transmission::replace_manual_selector(c,depth),"required fallback");
        require(!std::memcmp(&c,&before,sizeof c)&&!std::memcmp(ps2::g_ram,ram.data(),ram.size()),"mutation-free FULL CPU+RAM fallback");++rejected;};
    gt3::transmission::enabled=false;reject(valid);gt3::transmission::enabled=true;
    for(unsigned r:{4u,5u,28u,29u}){auto c=valid;c.r[r].d[0]|=1ull<<32;reject(c);}
    for(unsigned r:{4u,5u,29u})for(unsigned a:{0u,0xffffffffu,0x2000001u}){auto c=valid;c.r[r].d[0]=a;reject(c);}
    auto c=valid;ps2::set32(c.r[29],car+0x1300);reject(c);
    c=valid;ps2::set32(c.r[5],car+0x1303);reject(c);
    c=valid;c.budget=std::numeric_limits<int>::min();reject(c);
    const auto old=ps2::ld8(0x1e5458);ps2::st8(0x1e5458,old^1);reject(valid);ps2::st8(0x1e5458,old);
    ps2::st8(request,0);ps2::st8(car+0x13ba,0);ps2::st32(car+0x13ac,0x3f800000);
    c=valid;c.budget=159;ps2::st8(car+0x20a,6);reject(c);reject(valid,ps2::kMaxDepth);
    std::printf("MT selector mutation-free fallback PASS cases=%u\n",rejected);
}
