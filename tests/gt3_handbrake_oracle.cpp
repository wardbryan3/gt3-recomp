// Independent generated original at exact interior entry; no clean code in oracle.
#include "gt3_clean_handbrake.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <limits>
void register_generated_code();
namespace gen { void unit_0039(ps2::Cpu &,unsigned,unsigned); }
bool gt3_pedal_audit_stop=false;
bool gt3_handbrake_audit_stop=true;
namespace {
constexpr unsigned car=0x600000,command=0x502000;
unsigned seed=0x48425231;
unsigned random_word(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
void require(bool b,const char *why,unsigned i){if(!b){std::fprintf(stderr,"FAIL case=%u %s\n",i,why);std::exit(1);}}
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;
    if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    require(gt3::handbrake::profile_matches(),"ELF fingerprint",0);
    constexpr std::array<unsigned,16> history={0,0x80000000,1,0x80000001,0x3dcccccd,
        0x3effffff,0x3f000000,0x3f7fffff,0x3f800000,0x3f800001,0xbf800000,
        0x7f800000,0xff800000,0x7fc00000,0xffc00000,0x7f7fffff};
    unsigned cases=0,minimum=100,maximum=0;
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+0x2000000);
    // Cartesian full signed-halfword domain x analog/digital x 16 histories.
    for(unsigned h=0;h<17;++h)for(unsigned analog=0;analog<2;++analog)
    for(unsigned q=0;q<65536;++q) {
        const bool fuzz=h==16;
        ps2::st8(command,(random_word()&~16u)|(analog<<4));
        ps2::st16(command+14,q);ps2::st32(car+0x13b4,fuzz?random_word():history[h]);
        if(fuzz)for(unsigned a:{0x2d4940u,0x2d4944u,0x352990u})ps2::st32(a,random_word());
        ps2::Cpu before{};
        for(unsigned j=0;j<sizeof before;++j)reinterpret_cast<unsigned char *>(&before)[j]=random_word();
        before.pc=0x1e4bb8;before.budget=(q&4)?-1000:1000;
        if(!analog&&!q)before.budget=14; // exact no-preemption boundary
        ps2::set32(before.r[23],car);
        ps2::set32(before.r[16],car+0xf84);ps2::set32(before.r[18],command);ps2::set32(before.r[28],0x3579f0);
        const auto old=ps2::ld32(car+0x13b4);
        const unsigned depth=std::array<unsigned,4>{0,ps2::kMaxDepth-1,ps2::kMaxDepth,ps2::kMaxDepth+1}[q&3];
        auto original=before;gen::unit_0039(original,60000,depth);
        const auto expected=ps2::ld32(car+0x13b4);ps2::st32(car+0x13b4,old);
        auto clean=before;gt3::handbrake::enabled=true;
        require(gt3::handbrake::replace(clean,depth),"admission including depth boundary",cases);
        if(std::memcmp(&clean,&original,sizeof clean)){
            std::fprintf(stderr,"CPU budget %d/%d fcr %x/%x; f0 %x/%x f1 %x/%x f2 %x/%x\n",
             clean.budget,original.budget,clean.fcr31,original.fcr31,clean.f[0],original.f[0],clean.f[1],original.f[1],clean.f[2],original.f[2]);
            require(false,"complete CPU differential",cases);
        }
        require(ps2::ld32(car+0x13b4)==expected,"output",cases);
        auto stable=original;stable.pc=before.pc;stable.budget=before.budget;stable.fcr31=before.fcr31;
        stable.r[1]=before.r[1];stable.r[2]=before.r[2];for(unsigned n=0;n<3;++n)stable.f[n]=before.f[n];
        require(!std::memcmp(&stable,&before,sizeof stable),"CPU mutation surface",cases);
        require(clean.r[1].d[1]==before.r[1].d[1]&&clean.r[2].d[1]==before.r[2].d[1],"upper lanes",cases);
        require((clean.fcr31&~ps2::kFpuCondition)==(before.fcr31&~ps2::kFpuCondition),"FCR31",cases);
        unsigned cost=before.budget-original.budget;minimum=std::min(minimum,cost);maximum=std::max(maximum,cost);
        ++cases;
    }
    // Stateful chains: feed each original/clean output into the next step,
    // alternate analog/digital/zero, and retain CPU scratch between entries.
    unsigned transitions=0;
    for(unsigned a:{0x2d4940u,0x2d4944u,0x352990u})
        std::memcpy(ps2::g_ram+a,initial.data()+a,4);
    ps2::st32(car+0x13b4,0);ps2::Cpu chain{};
    ps2::set32(chain.r[23],car);ps2::set32(chain.r[16],car+0xf84);
    ps2::set32(chain.r[18],command);ps2::set32(chain.r[28],0x3579f0);
    for(unsigned n=0;n<20000;++n){
        ps2::st8(command,(n%7<3)?16:0);
        ps2::st16(command+14,std::array<unsigned,7>{0,1,4096,1,0,65535,0}[n%7]);
        chain.pc=0x1e4bb8;chain.budget=1000;
        auto old=ps2::ld32(car+0x13b4);auto original=chain;gen::unit_0039(original,60000,0);
        auto expected=ps2::ld32(car+0x13b4);ps2::st32(car+0x13b4,old);
        require(gt3::handbrake::replace(chain,0),"stateful admission",n);
        require(!std::memcmp(&chain,&original,sizeof chain)&&ps2::ld32(car+0x13b4)==expected,"stateful exact transition",n);
        ++transitions;
    }
    std::printf("Handbrake stateful transitions PASS cases=%u\n",transitions);
    // Reset the only allowed writes, then prove the entire 32MiB stayed unchanged.
    for(unsigned a:{0x2d4940u,0x2d4944u,0x352990u,car+0x13b4})
        std::memcpy(ps2::g_ram+a,initial.data()+a,4);
    std::memcpy(ps2::g_ram+command,initial.data()+command,16);
    require(!std::memcmp(ps2::g_ram,initial.data(),initial.size()),"whole-domain RAM mutation surface",cases);
    std::printf("Handbrake exact join PASS cases=%u CPU=complete RAM=32MiB-mutation-surface budget=%u..%u\n",cases,minimum,maximum);
    // Negative admission: complete CPU + all RAM unchanged, not fallback-as-proof.
    ps2::Cpu valid{};valid.budget=1000;valid.pc=0x1e4bb8;
    ps2::set32(valid.r[23],car);ps2::set32(valid.r[16],car+0xf84);
    ps2::set32(valid.r[18],command);ps2::set32(valid.r[28],0x3579f0);
    unsigned rejected=0;
    auto reject=[&](ps2::Cpu c,unsigned depth=0){auto before=c;
        require(!gt3::handbrake::replace(c,depth),"fallback",rejected);
        require(!std::memcmp(&before,&c,sizeof c)&&!std::memcmp(ps2::g_ram,initial.data(),initial.size()),"mutation-free fallback",rejected++);};
    gt3::handbrake::enabled=false;reject(valid);gt3::handbrake::enabled=true;
    for(unsigned r:{16u,18u,23u,28u}){auto c=valid;c.r[r].d[0]^=1;reject(c);}
    for(unsigned p:{0u,0x400000u,0x2000000u,0xffffffffu}){auto c=valid;c.r[23].d[0]=p;reject(c);}
    for(unsigned p:{0u,car,0x2000000u,0xffffffffu}){auto c=valid;c.r[18].d[0]=p;reject(c);}
    auto bad=valid;bad.budget=13;reject(bad); // digital release may preempt
    bad=valid;bad.budget=std::numeric_limits<int>::min();reject(bad);
    // Fingerprint failure, restoring it before the all-RAM fallback check.
    const auto byte=ps2::ld8(0x1e4bb8);ps2::st8(0x1e4bb8,byte^1);
    auto unchanged=valid;require(!gt3::handbrake::replace(unchanged,0),"profile fallback",0);
    require(!std::memcmp(&unchanged,&valid,sizeof valid),"profile CPU unchanged",0);
    ps2::st8(0x1e4bb8,byte);require(!std::memcmp(ps2::g_ram,initial.data(),initial.size()),"profile RAM unchanged",0);++rejected;
    std::printf("Handbrake mutation-free fallbacks PASS cases=%u\n",rejected);
}
