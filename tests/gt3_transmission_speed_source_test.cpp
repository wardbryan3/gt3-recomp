// Artifact-free synthetic guard consistency, NOT original semantic proof.
#include "gt3_clean_transmission_speed.hpp"
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
}
static_assert(offsetof(ps2::Cpu,pc)==548 && offsetof(ps2::Cpu,budget)==552);
static_assert(offsetof(ps2::Cpu,f)==560 && sizeof(ps2::Cpu)==1440);
int main(){
    using namespace gt3::transmission_speed;
    if(enabled||profile_matches())return 1;
    ps2::Cpu c{};c.budget=30000;ps2::set32(c.r[4],0x600000);ps2::set32(c.r[28],0x3579f0);
    const auto before=c;const std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    if(replace(c))return 1;enabled=true;if(replace(c)||counts.fallback!=1)return 1;
    if(std::memcmp(&c,&before,sizeof c)||std::memcmp(ps2::g_ram,ram.data(),ram.size()))return 1;
    std::puts("Speed helper public source/default/profile guards PASS; NOT an original oracle");
}
