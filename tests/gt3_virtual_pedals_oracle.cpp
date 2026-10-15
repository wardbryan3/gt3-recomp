// Private-original fixture oracle. No original instructions/data are embedded.
#include "gt3_virtual_pedals.hpp"
#include "gt3_clean_pedals.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <bit>
#include <cstring>
#include <cstdlib>
#include <vector>
void register_generated_code();
namespace {
constexpr unsigned car=0x600000,race=0x700000,knots=0x710000;
void require(bool v,const char *s){if(!v){std::fprintf(stderr,"FAIL virtual pedal oracle: %s\n",s);std::abort();}}
void f(unsigned a,float v){ps2::st32(a,std::bit_cast<unsigned>(v));}
void call(ps2::Cpu &c,unsigned pc,unsigned a0,unsigned a1,unsigned ret,unsigned sp){
 c.r[4].d[0]=a0;c.r[5].d[0]=a1;c.r[31].d[0]=ret;ps2::call(c,pc,0);require(c.pc==ret&&c.r[29].w[0]==sp,"original return/SP");
}
}
int main(int argc,char **argv){
 using namespace gt3::virtual_pedals;
 require(argc==2,"explicit original ELF");register_generated_code();unsigned ep;require(ps2::load_elf(argv[1],ep)&&profile_matches(),"exact original profile");
 std::vector<unsigned char> initial(0x2000000),expected(0x2000000),injection(0x2000000);unsigned cases=0,comparisons=0;
 for(unsigned group=0;group<3;++group)for(unsigned n=0;n<=4096;++n){
  const unsigned command=(n&1)?0x49af40:0x49af50;
  const unsigned tq=group==1?0:n,bq=group==0?0:group==1?n:4096-n;
  std::memset(ps2::g_ram+car,0,0x1800);std::memset(ps2::g_ram+race,0,0xb800);std::memset(ps2::g_ram+0x49d060,0,32);
  std::memset(ps2::g_ram+command-256,0xa5,512);std::memset(ps2::g_ram+command,0,16);ps2::st64(command+48,0x1f3b6c);
  ps2::st32(car+4,race);f(car+0xec0,1.f/60);f(car+0x68,.5f);f(car+0x13ac,.5f);f(car+0x13b0,.5f);
  ps2::st8(car+0x1306,n%3);ps2::st8(car+0x13e5,n%3);ps2::st8(car+0x136f,4);
  ps2::st8(command,1|(n&6));ps2::st8(command+1,2+n%3);ps2::st16(command+4,(n%1025)-512);
  ps2::st16(command+8,(n*17)&65535);ps2::st16(command+10,0x5a5a^n);
  for(unsigned i=0;i<3;++i){unsigned d=car+0x6c+i*0x3c,k=knots+i*16;ps2::st16(d,2);ps2::st32(d+4,k);ps2::st32(d+8,k+8);f(k,0);f(k+4,100);f(k+8,.5f);f(k+12,.5f);}
  f(car+0xe38,1);f(car+0xe3c,1);f(car+0xe40,1);ps2::st16(car+0x1d4,8000);f(car+0x13cc,100);f(car+0x2bc,1);f(car+0x1434,1);
  std::memcpy(initial.data(),ps2::g_ram,initial.size());ps2::Cpu original;
  for(unsigned phase=0;phase<3;++phase){
   std::memcpy(ps2::g_ram,initial.data(),initial.size());ps2::Cpu c{};c.budget=1000000;c.r[28].d[0]=0x3579f0;c.r[29].d[0]=command+64;c.r[4].d[0]=car;
   Options o;o.enabled=true;o.values={tq/4096.0,bq/4096.0};Experiment e(o);
   if(phase)e.probe(c,0x1e4d38,10);
   c.r[29].d[0]=command;c.r[16].d[0]=car+0xf84;c.r[17].d[0]=car;
   const auto before=c;
   if(phase)e.probe(c,0x1e4d5c,10);
   else {ps2::st8(command,initial[command]|6);ps2::st16(command+8,tq);ps2::st16(command+10,bq);}
   require(!std::memcmp(&c,&before,sizeof c),"injection never mutates CPU/budget");
   injection=initial;injection[command]|=6;injection[command+8]=tq&255;injection[command+9]=tq>>8;injection[command+10]=bq&255;injection[command+11]=bq>>8;
   require(!std::memcmp(injection.data(),ps2::g_ram,injection.size()),"only five command bytes changed, all car/input/steering/neighbor bytes unchanged");
   ps2::g_options.on_probe=[&](ps2::Cpu &cpu,unsigned pc){if(phase)e.probe(cpu,pc,10);};
   gt3::pedals::enabled=phase==2;
   call(c,0x1e4290,car+0xf84,command,0x1000000,command);
   call(c,0x1e4cb0,car,command,0x1e4dfc,command);
   if(phase)e.probe(c,0x1e4e68,10);
   else {ps2::st8(command,initial[command]);ps2::st16(command+8,unsigned(initial[command+8])|(unsigned(initial[command+9])<<8));ps2::st16(command+10,unsigned(initial[command+10])|(unsigned(initial[command+11])<<8));}
   call(c,0x1e6ec8,car,0,0x1000000,command);call(c,0x1e7500,car,0,0x1000000,command);
   if(!phase){original=c;std::memcpy(expected.data(),ps2::g_ram,expected.size());}
   else {
    require(!std::memcmp(&original,&c,sizeof c)&&!std::memcmp(expected.data(),ps2::g_ram,expected.size()),"complete generated-oracle CPU/32MiB differential");
    require(e.finished()&&e.counts.injected==1&&e.counts.restored==1&&e.counts.entries==1&&e.counts.joins==1&&e.counts.brakes==1&&e.counts.engines==1,"exact scope/path/restore counts");++comparisons;
   }
  }
  gt3::pedals::enabled=false;++cases;
 }
 require(gt3::pedals::counts.replaced==cases&&gt3::pedals::counts.fallback==0,"actual Frozen substitutions");
 // Ineligible owners and idle/default observers are mutation-free.
 for(unsigned kind:{1u,2u,255u}){
  ps2::st8(car+0x136d,kind);std::memcpy(initial.data(),ps2::g_ram,initial.size());Options o;o.enabled=true;o.values={1,1};Experiment e(o);
  ps2::Cpu c{};c.r[4].d[0]=car;c.r[29].d[0]=0x49af80;auto before=c;e.probe(c,0x1e4d38,0);e.probe(c,0x1e4d5c,0);e.probe(c,0x1e4e68,0);
  require(e.finished()&&!e.counts.injected&&!std::memcmp(&before,&c,sizeof c)&&!std::memcmp(initial.data(),ps2::g_ram,initial.size()),"nonmanual context isolation");
 }
 // Reject unsupported mode/auxiliary/profile/frame before any guest write.
 unsigned rejected=0;
 for(unsigned scenario=0;scenario<8;++scenario){
  constexpr unsigned command=0x49af40;
  ps2::st8(car+0x136d,0);ps2::st8(car+0x14b8,0);ps2::st16(car+0x14ba,0);
  std::memset(ps2::g_ram+command,0,16);ps2::st8(command+1,scenario==0?1:2);
  if(scenario==1)ps2::st16(command+12,1);
  const auto opcode=ps2::ld8(0x210740);if(scenario==2)ps2::st8(0x210740,opcode^1);
  std::memcpy(initial.data(),ps2::g_ram,initial.size());Options o;o.enabled=true;Experiment e(o);
  ps2::Cpu c{};c.r[4].d[0]=car;c.r[29].d[0]=command+64;e.probe(c,0x1e4d38,0);
  c.r[29].d[0]=command;c.r[16].d[0]=car+0xf84;c.r[17].d[0]=car;
  if(scenario==3)c.r[29].d[0]+=16;
  if(scenario==4)c.r[17].d[0]+=4;
  if(scenario==5)c.r[16].d[0]+=4;
  if(scenario==6)c.r[29].d[0]=0xffffffff;
  auto before=c;bool threw=false;try{e.probe(c,scenario==7?0x1e4d38:0x1e4d5c,0);}catch(const std::runtime_error &){threw=true;}
  require(threw&&!e.counts.injected&&!std::memcmp(&before,&c,sizeof c)&&!std::memcmp(initial.data(),ps2::g_ram,initial.size()),"unsupported context rejection is mutation-free");
  ps2::st8(0x210740,opcode);++rejected;
 }
 require(rejected==8,"all negative scopes");
 std::printf("Virtual pedal generated oracle PASS: %u cases / %u complete CPU+32MiB comparisons; all Q12 codes; actual Frozen substitutions; command-only writes/restoration; 8 mutation-free rejections; original notification/wrapper/brake/engine\n",cases,comparisons);
}
