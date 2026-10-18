// Private verification harness: unmodified generated original, mocked callees.
#include "gt3_economy_checks.hpp"
#include "units.hpp"
#include "ps2/system.hpp"
#include <array>
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <limits>
#include <utility>
#include <vector>
void register_generated_code();
using U=std::uint32_t; using Q=std::uint64_t; using I=std::int64_t;
using Event=std::pair<U,Q>;
constexpr U sp=0x1f00000, sentinel=0xdeadbeec;
void require(bool b,const char* why){if(!b){std::fprintf(stderr,"FAIL %s\n",why);std::exit(1);}}
struct Boundary : gt3::economy_recovery::dependency {
 Q flags; I result237bc0,result219448; unsigned index=0; std::vector<Event> trace;
 Boundary(Q f,I p,I n):flags(f),result237bc0(p),result219448(n){}
 U FUN_00218660() override {trace.emplace_back(0x218660,0); require(index<3,"getter count"); return std::array<U,3>{0x500000,0x600000,0x700000}[index++];}
 U load32(U a) override {return ps2::ld32(a);}
 Q load64(U a) override {return ps2::ld64(a);}
 Q FUN_00234380(U a) override {trace.emplace_back(0x234380,a);return flags;}
 I FUN_00237bc0(U a) override {trace.emplace_back(0x237bc0,a);return result237bc0;}
 I FUN_00219448(U a) override {trace.emplace_back(0x219448,a);return result219448;}
 void FUN_001c4f80(U a) override {trace.emplace_back(0x1c4f80,a);}
};
U original(U pc, Boundary& d) {
 ps2::Cpu c{}; c.pc=pc;c.budget=100000;ps2::set32(c.r[29],sp);ps2::set32(c.r[31],sentinel);
 c.r[16].d[0]=0x123456789abcdef0; c.r[17].d[0]=0xfedcba9876543210;
 unsigned steps=0;
 while(c.pc!=sentinel){
  require(++steps<50,"original termination");
  if(c.pc>=0x118000 && c.pc<0x11c000){
   U e=gen::entries_0006[(c.pc-0x118000)/4];require(e!=0,"original entry");
   gen::unit_0006(c,e,ps2::kMaxDepth);continue;
  }
  Q r=0;
  switch(c.pc){
   case 0x218660:r=d.FUN_00218660();break;
   case 0x234380:r=d.FUN_00234380(c.r[4].w[0]);break;
   case 0x237bc0:r=std::bit_cast<Q>(d.FUN_00237bc0(c.r[4].w[0]));break;
   case 0x219448:r=std::bit_cast<Q>(d.FUN_00219448(c.r[4].w[0]));break;
   case 0x1c4f80:d.FUN_001c4f80(c.r[4].w[0]);break;
   default:std::fprintf(stderr,"unexpected pc=%x\n",c.pc);require(false,"dependency");
  }
  c.r[2].d[0]=r;c.pc=c.r[31].w[0];
 }
 require(c.r[29].w[0]==sp,"restored SP");
 require(c.r[16].d[0]==0x123456789abcdef0 && c.r[17].d[0]==0xfedcba9876543210,"callee-saved registers");
 return c.r[2].w[0];
}
int main(int argc,char**argv){
 require(argc==2,"ELF argument");register_generated_code();U entry;require(ps2::load_elf(argv[1],entry),"load ELF");
 ps2::st32(0x500000+0x30d00,0x800000);
 // Poison the corresponding fields in other getter results to detect merged/reordered reads.
 ps2::st32(0x600000+0x30d00,0x900000);ps2::st64(0x500000+0x18,0xdeadbeef);
 std::vector<unsigned char> baseline(ps2::g_ram,ps2::g_ram+0x2000000);
 constexpr std::array<I,6> values={std::numeric_limits<I>::min(),-1,0,1,100,std::numeric_limits<I>::max()};
 constexpr std::array<I,7> counts={std::numeric_limits<I>::min(),-1,0,199,200,201,std::numeric_limits<I>::max()};
 constexpr std::array<Q,6> flags={0,1,2,3,0xffffffff00000000ULL,~Q{0}};
 unsigned cases=0;std::array<unsigned,4> outcomes{};
 for(U pc:{0x11bc18u,0x11bce0u})for(Q f:flags)for(I b:values)for(I p:values)for(I n:counts){
  ps2::st64(0x600000+0x18,std::bit_cast<Q>(b));
  Boundary a(f,p,n),d(f,p,n);U expected=original(pc,a);
  U actual=pc==0x11bc18?gt3::economy_recovery::FUN_0011bc18(d):gt3::economy_recovery::FUN_0011bce0(d);
  require(expected==actual,"return differential");require(a.trace==d.trace,"ordered dependency differential");
  require(a.index==d.index,"getter count differential");
  unsigned which=actual==0?0:actual==0x30ff90?1:actual==0x30ffa8?2:actual==0x30ffb8?3:4;
  require(which<4,"return domain");++outcomes[which];++cases;
  // Only the numeric input and the original 48-byte ABI stack frame may differ.
  std::memcpy(ps2::g_ram+0x600018,baseline.data()+0x600018,8);
  std::memcpy(ps2::g_ram+sp-48,baseline.data()+sp-48,48);
  require(std::memcmp(ps2::g_ram,baseline.data(),baseline.size())==0,"32MiB unknown state unchanged");
 }
 for(auto n:outcomes)require(n>0,"all outcomes exercised");
 std::printf("PASS checks=%u success=%u flag-reject=%u insufficient=%u limit=%u; ordered calls, distinct getter pointers, signed64 boundaries, non-stack RAM unchanged\n",cases,outcomes[0],outcomes[1],outcomes[2],outcomes[3]);
 std::puts("Scope: original generated check bodies; opaque callees mocked identically. No complete transaction, whole ABI, or live-game qualification.");
}
