// Public synthetic consistency tests; not a generated-original oracle.
#include "gt3_transmission_state.hpp"
#include "gt3_clean_transmission_admission.hpp"
#include "ps2/generated.hpp"
#include <cassert>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <vector>
namespace ps2 {
std::uint8_t g_ram[kRamSize]{},g_spr[kScratchpadSize]{};
std::uint8_t slow_ld8(unsigned){std::abort();}
std::uint16_t slow_ld16(unsigned){std::abort();}
std::uint32_t slow_ld32(unsigned){std::abort();}
std::uint64_t slow_ld64(unsigned){std::abort();}
void slow_st8(unsigned,std::uint8_t){std::abort();}
void slow_st32(unsigned,std::uint32_t){std::abort();}
void slow_st64(unsigned,std::uint64_t){std::abort();}
void dispatch(Cpu &,std::uint32_t,std::uint32_t){std::abort();}
}
int main() {
 namespace m=gt3::transmission_state;namespace a=gt3::transmission_admission;
 assert(!a::enabled&&!a::profile_matches());ps2::Cpu c{};ps2::set32(c.r[4],0x600000);ps2::set32(c.r[29],0x900000);ps2::set32(c.r[28],0x3579f0);c.budget=10000;const auto before=c;
 const std::vector<unsigned char> ram(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
 assert(!a::replace(c,0));a::enabled=true;assert(!a::replace(c,0));
 assert(!std::memcmp(&c,&before,sizeof c)&&!std::memcmp(ps2::g_ram,ram.data(),ram.size()));
 m::Admission x{0,1,0x3f800000,0x41000000,0x3e800000,3000,2500,0x4031c71d,0xc031c71d};
 assert(m::admit(x).state==0);x.effective_accelerator++;assert(m::admit(x).state==2);x.speed=0;x.sampled_rpm=2500;assert(m::admit(x).candidate==0);x.sampled_rpm=2501;assert(m::admit(x).state==2);
 x.state=1;x.candidate=0x80000000;assert(m::admit(x).state==0);
 assert(m::effective_policy(1,0,6)==0&&m::effective_policy(2,0,6)==6&&m::effective_policy(0,8,6)==0);
 assert(m::select(0,2,1).state==0&&m::select(1,0,1).state==2&&m::select(1,1,1).state==3);
 assert(!m::select(3,2,~0ull).commit&&m::select(3,2,0xffffffffull).commit);
 m::Synchronization s{3,7,1,0x3f800000,0x40000000,0x3f800000,0x40000000,0x40000000,0,0,0x3f800000,0x40000000,0x4031c71d,0xc031c71d};
 auto r=m::synchronize(s);assert(r.state==1&&r.inhibition==12);s.policy=3;r=m::synchronize(s);assert(r.state==1&&r.inhibition==7&&r.rewrite_axle_and_wheel_rates);
 s.policy=1;s.current_target=0;r=m::synchronize(s);assert(r.state==0&&r.cause==m::Cause::low_target_abort);
 s.state=2;s.brake=0x3f400000;r=m::synchronize(s);assert(r.state==2);s.brake++;r=m::synchronize(s);assert(r.state==0&&r.cause==m::Cause::brake_abort);
 assert(m::clamp_nonzero_engine(0xbf800000,0x40000000)==0);
 assert(m::drive_route(255)==m::DriveRoute::synchronization);
 std::puts("State public synthetic model/default/profile/partial-layout PASS; NOT original proof");
}
