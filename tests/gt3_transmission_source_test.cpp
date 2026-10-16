// PUBLIC synthetic guard consistency ONLY. No original bytes/tables/oracle.
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
namespace ps2 {
std::uint8_t g_ram[kRamSize]{},g_spr[kScratchpadSize]{};
std::uint8_t slow_ld8(unsigned){std::abort();}
std::uint16_t slow_ld16(unsigned){std::abort();}
std::uint32_t slow_ld32(unsigned){std::abort();}
std::uint64_t slow_ld64(unsigned){std::abort();}
void slow_st8(unsigned,std::uint8_t){std::abort();}
void slow_st64(unsigned,std::uint64_t){std::abort();}
void dispatch(Cpu &,unsigned,unsigned){std::abort();} // must NEVER reach a callee
}
int main(){
    using namespace gt3::transmission;
    if(enabled || profile_matches())return 1;
    ps2::Cpu c{};c.budget=20000;ps2::set32(c.r[4],0x600000);ps2::set32(c.r[5],0x601304);ps2::set32(c.r[29],0x49af30);ps2::set32(c.r[28],0x3579f0);
    const auto before=c;const std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    if(replace_manual_selector(c,0))return 1;
    enabled=true;if(replace_manual_selector(c,0)||counts.fallback!=1)return 1;
    if(std::memcmp(&c,&before,sizeof c)||std::memcmp(ps2::g_ram,ram.data(),ram.size()))return 1;
    std::puts("Transmission PUBLIC synthetic source/default/profile-guard PASS; NOT original equivalence or live proof");
}
