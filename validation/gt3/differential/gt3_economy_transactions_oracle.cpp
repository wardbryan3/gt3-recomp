// Private bounded differential: original transaction bodies, opaque callees mocked.
#include "gt3_economy_transactions.hpp"
#include "units.hpp"
#include "ps2/system.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
using U=std::uint32_t;using Q=std::uint64_t;
constexpr U base=0x500000,field=base+24,other=base+0x100,sentinel=0xdeadbeec,sp=0x1f00000;
void require(bool b,const char*s){if(!b){std::fprintf(stderr,"FAIL %s\n",s);std::exit(1);}}
struct Event{U pc;Q arg,observed;bool operator==(const Event&)const=default;};
struct Boundary:gt3::economy_recovery::transaction_boundary{
 Q result,amount;bool mutate;std::vector<Event> trace;
 Boundary(Q r,Q a,bool m):result(r),amount(a),mutate(m){}
 Q load64(U a)override{return ps2::ld64(a);}
 void store64(U a,Q v)override{ps2::st64(a,v);}
 Q lookup(U pc,U a){trace.push_back({pc,a,ps2::ld64(field)});if(mutate)ps2::st64(field,ps2::ld64(field)^Q{0xfedcba9876543210});return result;}
 Q FUN_00219048(U a)override{return lookup(0x219048,a);}
 Q FUN_00219128(U a)override{return lookup(0x219128,a);}
 Q FUN_00237bc0(U a)override{trace.push_back({0x237bc0,a,ps2::ld64(field)});if(mutate)ps2::st64(field,ps2::ld64(field)+7);return amount;}
 void FUN_001d9f60(U a)override{trace.push_back({0x1d9f60,a,ps2::ld64(field)});ps2::st64(other,ps2::ld64(field)^amount);}
};
void original(U pc,Boundary&d){
 ps2::Cpu c{};c.pc=pc;c.budget=100000;ps2::set32(c.r[4],base);ps2::set32(c.r[29],sp);ps2::set32(c.r[31],sentinel);
 c.r[16].d[0]=0x123456789abcdef0;c.r[17].d[0]=0xfedcba9876543210;
 unsigned steps=0;
 while(c.pc!=sentinel){require(++steps<40,"termination");if(c.pc>=0x218000&&c.pc<0x21c000&&c.pc!=0x219048&&c.pc!=0x219128){U e=gen::entries_0046[(c.pc-0x218000)/4];require(e!=0,"entry");gen::unit_0046(c,e,ps2::kMaxDepth);continue;}
 Q r=0;switch(c.pc){case 0x219048:r=d.FUN_00219048(c.r[4].w[0]);break;case 0x219128:r=d.FUN_00219128(c.r[4].w[0]);break;case 0x237bc0:r=d.FUN_00237bc0(c.r[4].w[0]);break;case 0x1d9f60:d.FUN_001d9f60(c.r[4].w[0]);break;default:require(false,"unexpected callee");}c.r[2].d[0]=r;c.pc=c.r[31].w[0];}
 require(c.r[29].w[0]==sp&&c.r[16].d[0]==0x123456789abcdef0&&c.r[17].d[0]==0xfedcba9876543210,"callee saved/SP");
}
int main(int argc,char**argv){require(argc==2,"ELF argument");register_generated_code();U entry;require(ps2::load_elf(argv[1],entry),"load ELF");
 std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+ps2::kRamSize),expected(ps2::kRamSize);
 constexpr std::array<Q,8> values={0,1,99,100,101,0x7fffffffffffffffULL,0x8000000000000000ULL,~Q{0}};
 unsigned cases=0,missing=0,underflows=0;
 for(U pc:{0x219250u,0x2192a8u})for(Q result:{Q{0},Q{0x800000},Q{0xffffffff00800000ULL},Q{0xfffffff8}})for(Q old:values)for(Q amount:values)for(bool mutate:{false,true}){
  std::memcpy(ps2::g_ram,initial.data(),initial.size());ps2::st64(field,old);Boundary a(result,amount,mutate);original(pc,a);
  // Exclude the original 48-byte maximum ABI stack frame, not other writes.
  std::memcpy(ps2::g_ram+sp-48,initial.data()+sp-48,48);std::memcpy(expected.data(),ps2::g_ram,expected.size());
  std::memcpy(ps2::g_ram,initial.data(),initial.size());ps2::st64(field,old);Boundary d(result,amount,mutate);
  if(pc==0x219250)gt3::economy_recovery::FUN_00219250(d,base);else gt3::economy_recovery::FUN_002192a8(d,base);
  require(a.trace==d.trace,"ordered calls/args/observed state");require(std::memcmp(ps2::g_ram,expected.data(),expected.size())==0,"full nonstack RAM differential");
  if(result==0){require(a.trace.size()==1,"null short circuit");++missing;}
  else if(!mutate&&old<amount){require(ps2::ld64(field)==old-amount,"mod64 underflow, no admission check");++underflows;}
  ++cases;
 }
 require(missing>0&&underflows>0,"boundary coverage");std::printf("PASS transaction differentials=%u null-paths=%u underflows=%u; ordered opaque calls, dependency mutations, store-before-side-effect, full nonstack RAM\n",cases,missing,underflows);
 std::puts("Scope: FUN_00219250/FUN_002192a8 bodies only; lookup/value/post-store callees mocked. No whole transaction, original dependency behavior, or safe top-up claim.");
}
