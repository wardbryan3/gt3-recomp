// Original generated table/price/float execution versus recovered mechanisms.
// Fixtures establish readable aligned, nonempty sorted tables and initialized
// handles. Numeric mode/price/float bit tests are instruction contracts, NOT a
// claim that every fixture is a legal gameplay configuration.
#include "gt3_economy_catalog.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <algorithm>
#include <array>
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <vector>
void register_generated_code();
namespace {
using U=std::uint32_t;using Q=std::uint64_t;namespace model=gt3::economy_recovery;
constexpr U object=0x600100,handle=object+464,root=0x800000,table=0x810000;
constexpr U gp=0x3579f0,sp=0x1f00000,sentinel=0xdeadbee0;
unsigned cases=0,seed=0x2315d8;
void require(bool ok,const char* msg){if(!ok){std::fprintf(stderr,"FAIL catalog case=%u %s\n",cases,msg);std::exit(1);}}
U random_word(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
struct Event{U arg;bool after;std::array<U,12> words;bool operator==(const Event&)const=default;};
std::vector<Event> events;
void capture(U arg,bool after){Event e{arg,after,{}};for(U i=0;i<3;++i)e.words[i]=ps2::ld32(object+i*4);for(U i=0;i<9;++i)e.words[i+3]=ps2::ld32(0x2d2b00+i*4);events.push_back(e);}
struct Result{Q v0;U f0;};
Result original(U pc,U a0,Q a1=0,Q a2=0,bool observe=false,U stack=sp){
 ps2::Cpu c{};for(U i=0;i<32;++i)c.r[i].d[0]=0xabc0000000000000ULL+i;
 ps2::set32(c.r[0],0);ps2::set32(c.r[4],a0);ps2::set64(c.r[5],a1);ps2::set64(c.r[6],a2);
 ps2::set32(c.r[28],gp);ps2::set32(c.r[29],stack);ps2::set32(c.r[31],sentinel);c.pc=pc;c.budget=1000000;
 std::array<Q,8> saved{};for(U i=0;i<8;++i)saved[i]=c.r[16+i].d[0];
 U ret=0,arg=0;unsigned steps=0;
 while(c.pc!=sentinel){require(++steps<10000,"original termination");
  if(observe&&ret&&c.pc==ret){capture(arg,true);ret=0;}
  if(observe&&c.pc==0x1dac48){arg=c.r[4].w[0];capture(arg,false);ret=c.r[31].w[0];}
  ps2::dispatch(c,c.pc,ps2::kMaxDepth);
 }
 require(c.r[29].w[0]==stack,"original SP");for(U i=0;i<8;++i)require(c.r[16+i].d[0]==saved[i],"original callee saved");
 return {c.r[2].d[0],c.f[0]};
}
struct Memory:model::catalog_memory,model::post_debit_boundary{
 std::uint16_t load16(U a)override{return ps2::ld16(a);}
 U load32(U a)override{return ps2::ld32(a);}
 Q load64(U a)override{return ps2::ld64(a);}
 void store32(U a,U v)override{ps2::st32(a,v);}
 U FUN_001dac48(U a)override{capture(a,false);auto r=original(0x1dac48,a,0,0,false,sp-128);capture(a,true);return r.f0;}
};
std::vector<unsigned char> baseline,before,expected;
void compare(U pc,U a0,Q a1,Q a2,const std::function<Q(Memory&)>& clean,bool returns=true){
 before.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);events.clear();auto result=original(pc,a0,a1,a2,true);auto original_events=events;
 expected.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);std::memcpy(expected.data()+sp-512,before.data()+sp-512,512);
 std::memcpy(ps2::g_ram,before.data(),before.size());events.clear();Memory m;Q got=clean(m);
 if(returns)require(got==result.v0,"logical return bits");
 require(events==original_events,"original float dependency checkpoints/order");
 std::memcpy(ps2::g_ram+sp-512,before.data()+sp-512,512);
 require(std::memcmp(ps2::g_ram,expected.data(),expected.size())==0,"complete nonstack RAM");++cases;
}
std::vector<Q> fixture(U count,U stride=264,U offset=0,U mask=0x80000000){
 std::memcpy(ps2::g_ram,baseline.data(),baseline.size());
 ps2::st32(handle,root);ps2::st32(root+8,offset);ps2::st32(root+12,mask);
 ps2::st32(root+16+30*4,(table-root-offset)|mask);
 ps2::st16(table+8,count);ps2::st16(table+10,stride);
 std::vector<Q> keys;for(U i=0;i<count;++i)keys.push_back((Q(random_word())<<32)|random_word());
 if(count>2){keys[0]=0;keys[1]=~Q{0};keys[2]=Q{1}<<63;}
 std::sort(keys.begin(),keys.end());require(std::adjacent_find(keys.begin(),keys.end())==keys.end(),"unique fixture keys");
 for(U i=0;i<count;++i)ps2::st64(table+16+stride*i,keys[i]);
 return keys;
}
}
int main(int argc,char**argv){require(argc==2,"ELF argument");register_generated_code();U entry;require(ps2::load_elf(argv[1],entry),"ELF load");baseline.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
 for(U count:{1u,2u,3u,7u,16u,31u,244u})for(U stride:{8u,16u,264u})for(U offset:{0u,128u}){
  auto keys=fixture(count,stride,offset);
  compare(0x231548,handle,30,0,[&](Memory&m){return model::FUN_00231548(m,handle,30);});
  for(U i=0;i<count;++i){if(count>31&&i!=0&&i!=count/2&&i!=count-1)continue;Q key=keys[i];
   compare(0x2316e8,table,key,0,[&](Memory&m){return model::FUN_002316e8(m,table,key);});
   compare(0x2315d8,handle,30,key,[&](Memory&m){return model::FUN_002315d8(m,handle,30,key);});
  }
  for(unsigned k=0;k<3;++k){Q absent=(Q(random_word())<<32)|random_word();require(!std::binary_search(keys.begin(),keys.end(),absent),"absent fixture key");
   compare(0x2316e8,table,absent,0,[&](Memory&m){return model::FUN_002316e8(m,table,absent);});
   compare(0x2315d8,handle,30,absent,[&](Memory&m){return model::FUN_002315d8(m,handle,30,absent);});
  }
 }
 const unsigned lookups=cases;
 constexpr std::array<U,12> prices={0,1,99,14660,22950,0x7fffffff,0x80000000,0xffffffff,0x40000001,0x10000000,0xff000001,0xdeadbeef};
 for(U bits:prices)for(U mode:{0u,1u,2u,0xffffffffu,0x80000000u}){
  auto keys=fixture(3);Q key=keys[1];ps2::st64(object,key);ps2::st32(table+16+264+236,bits);ps2::st32(gp-18968,mode);
  compare(0x231680,handle,0,0,[&](Memory&m){return model::FUN_00231680(m,gp);});
  compare(0x237bc0,object,0,0,[&](Memory&m){return std::bit_cast<Q>(model::FUN_00237bc0(m,object,gp));});
 }
 const unsigned pricing=cases-lookups;
 constexpr std::array<U,14> float_bits={0,0x80000000,1,0x80000001,0x3f800000,0xbf800000,0x7f800000,0xff800000,0x7fc00001,0x7f800001,0xffc00001,0xc8927c00,0x7fffffff,0xffffffff};
 for(U pc:{0x1d9ce8u,0x1d9f60u})for(U bits:float_bits){
  std::memcpy(ps2::g_ram,baseline.data(),baseline.size());ps2::st8(0x2d294c,1);ps2::st32(0x2d2b00,bits);
  for(U i=0;i<12;i+=4)ps2::st32(object+i,random_word());
  compare(pc,object,0,0,[&](Memory&m){if(pc==0x1d9ce8)model::FUN_001d9ce8(m,object);else model::FUN_001d9f60(m,object);return 0;},false);
  require(ps2::ld32(object+4)==bits,"float32 bits forwarded, including NaN payload/sign");
 }
 for(U pc:{0x1d9ce8u,0x1d9f60u}){
  std::memcpy(ps2::g_ram,baseline.data(),baseline.size());ps2::st8(0x2d294c,0);
  compare(pc,object,0,0,[&](Memory&m){if(pc==0x1d9ce8)model::FUN_001d9ce8(m,object);else model::FUN_001d9f60(m,object);return 0;},false);
 }
 std::printf("PASS catalog differentials=%u lookup=%u pricing/mode=%u float-forwarding=%u; complete nonstack 32MiB, original float callee retained\n",cases,lookups,pricing,cases-lookups-pricing);
 std::puts("Scope: nonempty sorted synthetic tables; no corrupt/empty-table or missing-row price precondition qualification; not full Cpu/stack/cost or gameplay integration proof.");
}
