// Isolated validation ONLY: original execution remains oracle; shadow body runs
// against the exact entry CPU and 32 MiB RAM, then all original state is restored.
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include "ps2/state.hpp"
#include "gt3_clean_pedals.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
namespace ps2::kernel { void state(ps2::state::Stream &); }
extern void gt3_pedal_closure_body(ps2::Cpu &,unsigned);
bool gt3_pedal_closure_busy=false;
namespace {
FILE *out=nullptr;bool opened=false,active=false,hook=false;
unsigned owner_sp=0,owner_car=0;ps2::Cpu before;
std::vector<unsigned char> entry_ram(0x2000000),original_ram(0x2000000);
void check(bool ok,const char *why){if(!ok){std::fprintf(stderr,"CLOSURE FAIL: %s\n",why);std::abort();}}
unsigned word(const unsigned char *p){unsigned w;std::memcpy(&w,p,4);return w;}
}
void gt3_pedal_closure_probe(ps2::Cpu &c,unsigned pc,unsigned depth) {
 if(gt3_pedal_closure_busy)return;
 if(!opened){opened=true;if(const char *p=std::getenv("GT3_PEDAL_CLOSURE_TRACE")){out=std::fopen(p,"wx");check(out,"exclusive trace");}}
 if(!out)return;
 const auto sp=c.r[29].w[0];
 if(pc==0x1e4d38){check(!active,"reentrant owner");active=true;owner_sp=sp;owner_car=c.r[4].w[0];}
 if(pc==0x1e4d88){check(active&&!hook,"nested virtual hook");hook=true;
  std::fprintf(out,"{\"stage\":\"hook\",\"target\":%u,\"owner_sp\":%u}\n",c.r[2].w[0],owner_sp);}
 if(pc==0x1e4d90){check(hook,"hook return");hook=false;}
 if(pc==0x1e48fc){
  check(active&&!hook&&owner_car==c.r[23].w[0],"owner/hook lifetime");
  const unsigned cmd=c.r[18].w[0];check(cmd==owner_sp-64&&cmd==sp+208,"activation shape");
  check(ps2::ld64(sp+128)==0x1e4cc8&&ps2::ld64(cmd-16)==0x1e4dfc&&ps2::ld64(cmd+48)==0x1f3b6c,"return chain");
  ps2::state::Writer kernel;ps2::kernel::state(kernel);check(kernel.out.size()>12,"kernel state");
  const unsigned count=word(kernel.out.data()+8);unsigned owners=0,tid=0,base=0,size=0;
  for(unsigned i=0;i<count;++i){const auto *t=kernel.out.data()+12+i*772+4;
   check(t+768<=kernel.out.data()+kernel.out.size(),"kernel Thread serialization bounds");
   const unsigned low=word(t+20),length=word(t+24);
   if(sp>=low&&owner_sp<=low+length&&word(t+4)==1){++owners;tid=word(t);base=low;size=length;}}
  check(owners==1,"unique running stack owner");
  std::fprintf(out,"{\"stage\":\"entry\",\"frame\":%llu,\"command\":%u,\"sp\":%u,\"owner_sp\":%u,\"thread\":%u,\"stack_base\":%u,\"stack_size\":%u,\"parent_ra\":%u,\"depth\":%u}\n",(unsigned long long)ps2::frame_count(),cmd,sp,owner_sp,tid,base,size,ps2::ld32(cmd+240),depth);
  before=c;std::memcpy(entry_ram.data(),ps2::g_ram,entry_ram.size());
 }
 if(pc==0x1e4ba8){
  const auto original=c;std::memcpy(original_ram.data(),ps2::g_ram,original_ram.size());
  std::memcpy(ps2::g_ram,entry_ram.data(),entry_ram.size());auto clean=before;
  auto callback=std::move(ps2::g_options.on_probe);const auto counts=gt3::pedals::counts;
  gt3_pedal_closure_busy=true;gt3_pedal_closure_body(clean,depth);gt3_pedal_closure_busy=false;
  gt3::pedals::counts=counts;ps2::g_options.on_probe=std::move(callback);
  auto expected=original;expected.pc=0x1e4ba8;
  check(!std::memcmp(&clean,&expected,sizeof clean),"complete actual-entry CPU/budget differential");
  check(!std::memcmp(ps2::g_ram,original_ram.data(),original_ram.size()),"complete actual-entry 32MiB differential");
  const auto car=before.r[23].w[0];
  for(unsigned offset:{0x1304u,0x1306u,0x13acu,0x13adu,0x13aeu,0x13afu,0x13b0u,0x13b1u,0x13b2u,0x13b3u})entry_ram[car+offset]=original_ram[car+offset];
  check(!std::memcmp(entry_ram.data(),original_ram.data(),entry_ram.size()),"bounded mutation surface");
  std::memcpy(ps2::g_ram,original_ram.data(),original_ram.size());
  std::fprintf(out,"{\"stage\":\"join\",\"cost\":%d,\"exact\":true}\n",before.budget-c.budget);
 }
 if(pc==0x1e4e68){check(active&&!hook,"owner return lifetime");check(sp==owner_sp-64,"owner unwind");active=false;}
 check(!std::ferror(out),"trace write");std::fflush(out);
}
