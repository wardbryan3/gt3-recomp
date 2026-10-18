// Private differential fixture: native field operations versus untouched original leaves.
#include "gt3_economy_state.hpp"
#include "units.hpp"
#include "ps2/system.hpp"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
using U=std::uint32_t;using Q=std::uint64_t;
constexpr U sentinel=0xdeadbeec;
void require(bool b,const char* why){if(!b){std::fprintf(stderr,"FAIL %s\n",why);std::exit(1);}}
struct Event { bool store; U address; Q value; bool operator==(const Event&)const=default; };
struct Memory:gt3::economy_recovery::state_memory {
 std::vector<Event> trace;
 Q load64(U a)override{trace.push_back({false,a,0});return ps2::ld64(a);}
 void store64(U a,Q v)override{trace.push_back({true,a,v});ps2::st64(a,v);}
};
Q random_state=0x8ac773151267abde;
Q random_word(){random_state^=random_state<<13;random_state^=random_state>>7;random_state^=random_state<<17;return random_state;}
ps2::Cpu initial_cpu(){ps2::Cpu c{};for(auto&r:c.r){r.d[0]=random_word();r.d[1]=random_word();}c.budget=100000;ps2::set32(c.r[31],sentinel);return c;}
int main(int argc,char**argv){
 require(argc==2,"ELF argument");register_generated_code();U entry;require(ps2::load_elf(argv[1],entry),"ELF load");
 const std::vector<unsigned char> baseline(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
 constexpr std::array<Q,8> edges={0,1,0x7fffffffffffffffULL,0x8000000000000000ULL,~Q{0},~Q{0}-1,0x123456789abcdef0ULL,0xfedcba9876543210ULL};
 // RAM only: canonical, cached/uncached aliases, and true uint32 address wrap.
 constexpr std::array<U,5> bases={0x500000,0x600000,0x80500000,0x20500000,0xfffffff0};
 unsigned cases=0;
 auto run=[&](U pc,U base,Q old,Q value){
  const U a=base+U{24},physical=a&0x1fffffff;require(physical<=ps2::kRamSize-8 && !(physical&7),"aligned RAM fixture");
  const Q saved=ps2::ld64(a);ps2::st64(a,old);
  auto before=initial_cpu();before.pc=pc;before.r[4].d[0]=base;before.r[5].d[0]=value;
  auto original=before;U e=gen::entries_0046[(pc-0x218000)/4];require(e!=0,"entry");gen::unit_0046(original,e,ps2::kMaxDepth);
  const Q expected_field=ps2::ld64(a),expected_result=original.r[2].d[0];
  auto envelope=before;envelope.pc=sentinel;envelope.budget-=pc==0x21a740?4:2;
  if(pc==0x21a6d0)envelope.r[2].d[0]=old;
  if(pc==0x21a740)envelope.r[2].d[0]=old+value;
  require(std::memcmp(&original,&envelope,sizeof original)==0,"original complete CPU mutation envelope/cost");
  ps2::st64(a,saved);require(std::memcmp(ps2::g_ram,baseline.data(),baseline.size())==0,"original entire RAM mutation envelope");
  ps2::st64(a,old);Memory mem;Q result=before.r[2].d[0];std::vector<Event> expected_events;
  if(pc==0x21a6d0){result=gt3::economy_recovery::FUN_0021a6d0(mem,base);expected_events={{false,a,0}};}
  else if(pc==0x21a740){gt3::economy_recovery::FUN_0021a740(mem,base,value);expected_events={{false,a,0},{true,a,expected_field}};}
  else{gt3::economy_recovery::FUN_0021a7d8(mem,base,value);expected_events={{true,a,expected_field}};}
  require(ps2::ld64(a)==expected_field,"native/original field differential");
  if(pc==0x21a6d0)require(result==expected_result,"getter return differential");
  require(mem.trace==expected_events,"native ordered load/store contract");
  ps2::st64(a,saved);require(std::memcmp(ps2::g_ram,baseline.data(),baseline.size())==0,"native entire RAM mutation envelope");++cases;
 };
 for(U pc:{0x21a6d0u,0x21a740u,0x21a7d8u}){
  for(U base:bases)for(Q old:edges)for(Q value:edges)run(pc,base,old,value);
  for(unsigned i=0;i<1000;++i){U base=0x500000+U(random_word()%1024)*8;Q old=random_word(),value=random_word();run(pc,base,old,value);}
 }
 unsigned chains=0;
 // Separate original/native images for setter -> add -> getter transitions.
 for(U base:bases)for(Q value:edges){
  U a=base+U{24};Q saved=ps2::ld64(a),step=random_word();ps2::st64(a,0);
  auto execute=[&](U pc,Q arg){auto c=initial_cpu();c.r[4].d[0]=base;c.r[5].d[0]=arg;c.pc=pc;gen::unit_0046(c,gen::entries_0046[(pc-0x218000)/4],ps2::kMaxDepth);require(c.pc==sentinel,"chain return");return c.r[2].d[0];};
  execute(0x21a7d8,value);Q o1=ps2::ld64(a);execute(0x21a740,step);Q o2=ps2::ld64(a);Q o3=execute(0x21a6d0,0);
  ps2::st64(a,0);Memory m;gt3::economy_recovery::FUN_0021a7d8(m,base,value);require(ps2::ld64(a)==o1,"chain setter");gt3::economy_recovery::FUN_0021a740(m,base,step);require(ps2::ld64(a)==o2,"chain add");require(gt3::economy_recovery::FUN_0021a6d0(m,base)==o3,"chain getter");
  ps2::st64(a,saved);require(std::memcmp(ps2::g_ram,baseline.data(),baseline.size())==0,"chain RAM envelope");++chains;
 }
 std::printf("PASS leaf differentials=%u chains=%u; original CPU envelope/cost, native outputs/load-store contract, whole32MiB RAM, uint32 address wrap, uint64 value wrap\n",cases,chains);
 std::puts("Scope: three field operations, no mocked callees; no proof of caller identity, legal credit range, save safety, or native whole-ABI replacement.");
}
