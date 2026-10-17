// Independent generated-original packet -> original consumers is the oracle.
// No original code/data embedded; explicit private ELF and generated archive.
#include "gt3_virtual_handbrake.hpp"
#include "gt3_virtual_handbrake_samples.hpp"
#include "gt3_clean_handbrake.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <bit>
#include <cstring>
#include <cstdlib>
#include <limits>
#include <vector>
void register_generated_code();
bool gt3_pedal_audit_stop=false;
namespace {
constexpr unsigned car=0x600000,race=0x700000,knots=0x710000;
void require(bool v,const char *why){if(!v){std::fprintf(stderr,"FAIL virtual handbrake oracle: %s\n",why);std::abort();}}
void f(unsigned a,float v){ps2::st32(a,std::bit_cast<unsigned>(v));}
void call(ps2::Cpu &cpu,unsigned pc,unsigned a0,unsigned a1,unsigned ret,unsigned sp){
 cpu.r[4].d[0]=a0;cpu.r[5].d[0]=a1;cpu.r[31].d[0]=ret;ps2::call(cpu,pc,0);
 require(cpu.pc==ret&&cpu.r[29].w[0]==sp,"original return/SP");
}
struct Observation {unsigned pc;ps2::Cpu cpu;std::array<unsigned char,16> command;unsigned processed,coupling;std::array<unsigned,4> brakes;};
}
int main(int argc,char **argv) {
 using namespace gt3::virtual_handbrake;
 require(argc>=2&&argc<=4,"explicit original ELF, optional exclusive original-result table, optional observed floor bits (hex)");
 FILE *table=argc>=3?std::fopen(argv[2],"wx"):nullptr;require(argc<3||table,"exclusive original-result table");
 register_generated_code();unsigned ep;
 require(ps2::load_elf(argv[1],ep)&&profile_matches(),"original profile");
 if(argc==4){unsigned floor=0;std::string_view text=argv[3];auto [end,error]=std::from_chars(text.data(),text.data()+text.size(),floor,16);require(error==std::errc{}&&end==text.data()+text.size(),"explicit floor bits");ps2::st32(0x352990,floor);}
 std::vector<unsigned char> initial(0x2000000),expected(0x2000000),injection(0x2000000);
 unsigned cases=0,comparisons=0,observations=0,rear_checks=0;
 for(const auto sample:virtual_handbrake_samples::all()) {
  const unsigned command=(cases&1)?0x49af40:0x49af50;
  std::memset(ps2::g_ram+car,0,0x1800);std::memset(ps2::g_ram+race,0,0xb800);std::memset(ps2::g_ram+0x49d060,0,32);
  std::memset(ps2::g_ram+command-256,0xa5,512);std::memset(ps2::g_ram+command,0,16);ps2::st64(command+48,0x1f3b6c);
  ps2::st32(car+4,race);f(car+0xec0,1.f/60);f(car+0x68,.5f);f(car+0x13ac,.5f);f(car+0x13b0,.5f);
  ps2::st32(car+0x13b4,std::array<unsigned,8>{0,0x3f000000,0x3f800000,0x80000000,0x7f800000,0x7fc12345,0xbf800000,1}[cases%8]);
  ps2::st8(car+0x13e5,cases%9);ps2::st8(car+0x20b,cases&1);ps2::st8(car+0x13bb,(cases>>1)&1);
  ps2::st16(car+0x14ba,(cases&8)?65535:0);ps2::st8(car+0x136f,4);ps2::st16(car+0x1d6,8000);ps2::st16(car+0x1414,4000);
  ps2::st8(command,1|(cases&0xee));ps2::st8(command+1,2+cases%3);ps2::st8(command+2,cases&1);ps2::st8(command+3,0x5a);
  ps2::st16(command+4,(cases%1025)-512);ps2::st16(command+8,(cases*17)&4095);ps2::st16(command+10,(cases*13)&4095);
  ps2::st16(command+12,cases&1);ps2::st16(command+14,0x5a5a^cases);
  for(unsigned i=0;i<3;++i){unsigned d=car+0x6c+i*0x3c,k=knots+i*16;ps2::st16(d,2);ps2::st32(d+4,k);ps2::st32(d+8,k+8);f(k,0);f(k+4,100);f(k+8,.5f);f(k+12,.5f);}
  f(car+0xe38,1.25f);f(car+0xe3c,2.5f);f(car+0xe40,3);ps2::st16(car+0x1d4,8000);f(car+0x13cc,100);f(car+0x2bc,1);f(car+0x1434,1);
  std::memcpy(initial.data(),ps2::g_ram,initial.size());ps2::Cpu original;std::vector<Observation> original_observations;
  for(unsigned phase=0;phase<3;++phase) {
   std::memcpy(ps2::g_ram,initial.data(),initial.size());ps2::Cpu cpu{};cpu.budget=1000000;
   cpu.r[28].d[0]=0x3579f0;cpu.r[29].d[0]=command+64;cpu.r[4].d[0]=car;
   Options options;options.enabled=true;options.value=sample.value;Experiment experiment(options);
   if(phase)experiment.probe(cpu,0x1e4d38,10);
   cpu.r[29].d[0]=command;cpu.r[16].d[0]=car+0xf84;cpu.r[17].d[0]=car;
   auto before=cpu;
   if(phase)experiment.probe(cpu,0x1e4d5c,10);
   else {ps2::st8(command,initial[command]|16);ps2::st16(command+14,sample.q);}
   require(!std::memcmp(&cpu,&before,sizeof cpu),"injector CPU/budget invariant");
   injection=initial;injection[command]|=16;injection[command+14]=sample.q&255;injection[command+15]=sample.q>>8;
   require(!std::memcmp(injection.data(),ps2::g_ram,injection.size()),"exact three command bytes only; no processed/direct car/input/neighbor writes");
   std::vector<Observation> observed;
   ps2::g_options.on_probe=[&](ps2::Cpu &c,unsigned pc){
    if(phase)experiment.probe(c,pc,10);
    if(pc==0x1e4bb8||pc==0x1e4c60||pc==0x1e4c74||pc==0x1e6fc8){
     Observation row{};row.pc=pc;row.cpu=c;row.cpu.pc=pc; // Explicit semantic probe PC, as in native trace; final CPU below is unnormalized.
     std::memcpy(row.command.data(),ps2::g_ram+command,16);row.processed=ps2::ld32(car+0x13b4);row.coupling=ps2::ld32(car+0x139c);
     for(unsigned i=0;i<4;++i)row.brakes[i]=ps2::ld32(car+0x1274+i*0x24);observed.push_back(row);
    }
   };
   gt3::handbrake::enabled=phase==2;
   call(cpu,0x1e4290,car+0xf84,command,0x1000000,command);
   call(cpu,0x1e4cb0,car,command,0x1e4dfc,command);
   require(ps2::ld16(command+14)==sample.q&&(ps2::ld8(command)&16),"actual original analog command");
   before=cpu;
   if(phase)experiment.probe(cpu,0x1e4e68,10);
   else {ps2::st8(command,initial[command]);ps2::st16(command+14,unsigned(initial[command+14])|(unsigned(initial[command+15])<<8));}
   require(!std::memcmp(&cpu,&before,sizeof cpu)&&!std::memcmp(initial.data()+command,ps2::g_ram+command,16),"restoration full command/CPU invariant");
   call(cpu,0x1e6ec8,car,0,0x1000000,command);
   for(unsigned i=0;i<4;++i){auto q=ps2::fp::mul(ps2::ld32(car+0x1074+i*0xa4),ps2::ld32(car+0xe38+(i>>1)*4));if(i>=2)q=ps2::fp::add(q,ps2::fp::mul(ps2::ld32(car+0x13b4),ps2::ld32(car+0xe40)));require(ps2::ld32(car+0x1274+i*0x24)==q,"original rear-only brake formula");++rear_checks;}
   call(cpu,0x1e7500,car,0,0x1000000,command);
   require(observed.size()==4,"every original semantic join/consumer observed");
   if(!phase){original=cpu;std::memcpy(expected.data(),ps2::g_ram,expected.size());original_observations=observed;
    if(table&&cases<=4096)require(std::fprintf(table,"{\"q\":%u,\"floor\":%u,\"processed\":%u}\n",sample.q,ps2::ld32(0x352990),ps2::ld32(car+0x13b4))>0,"original table write");
   }
   else {
    require(!std::memcmp(&original,&cpu,sizeof cpu)&&!std::memcmp(expected.data(),ps2::g_ram,expected.size()),"complete final CPU+32MiB original packet differential");
    for(unsigned i=0;i<observed.size();++i){const auto &a=observed[i],&b=original_observations[i];require(a.pc==b.pc&&!std::memcmp(&a.cpu,&b.cpu,sizeof a.cpu)&&a.command==b.command&&a.processed==b.processed&&a.coupling==b.coupling&&a.brakes==b.brakes,"command/processed/CPU/budget/coupling/rear original observations");++observations;}
    require(experiment.finished()&&experiment.counts.injected==1&&experiment.counts.restored==1&&experiment.counts.entries==1&&experiment.counts.joins==1&&experiment.counts.brakes==1&&experiment.counts.brake_joins==1&&experiment.counts.engines==1,"actual path/restore counts");++comparisons;
   }
  }
  ++cases;
 }
 require(gt3::handbrake::counts.replaced==cases&&!gt3::handbrake::counts.fallback,"actual unchanged Frozen substitutions");gt3::handbrake::enabled=false;
 unsigned rejected=0;
 for(unsigned scenario=0;scenario<10;++scenario) {
  const unsigned command=0x49af40;ps2::st8(car+0x136d,0);ps2::st8(car+0x14b8,0);ps2::st16(car+0x14ba,0);
  const auto opcode=ps2::ld8(0x210740);if(scenario==0)ps2::st8(0x210740,opcode^1);
  std::memcpy(initial.data(),ps2::g_ram,initial.size());Options options;options.enabled=true;Experiment experiment(options);
  ps2::Cpu cpu{};cpu.r[4].d[0]=car;cpu.r[29].d[0]=command+64;cpu.r[28].d[0]=0x3579f0;experiment.probe(cpu,0x1e4d38,0);
  cpu.r[29].d[0]=command;cpu.r[16].d[0]=car+0xf84;cpu.r[17].d[0]=car;
  if(scenario==1)cpu.r[29].d[0]+=16;if(scenario==2)cpu.r[17].d[0]+=4;if(scenario==3)cpu.r[16].d[0]+=4;
  if(scenario==4)cpu.r[29].d[0]=0xffffffff;if(scenario==5)cpu.r[28].d[0]+=4;
  if(scenario==6)cpu.r[17].d[0]|=1ull<<32;if(scenario==7)cpu.r[16].d[0]|=1ull<<32;if(scenario==8)cpu.r[29].d[0]|=1ull<<32;
  auto before=cpu;bool threw=false;try{experiment.probe(cpu,scenario==9?0x1e4d38:0x1e4d5c,0);}catch(const std::runtime_error &){threw=true;}
  require(threw&&!experiment.counts.injected&&!std::memcmp(&before,&cpu,sizeof cpu)&&!std::memcmp(initial.data(),ps2::g_ram,initial.size()),"unsupported activation mutation-free rejection");ps2::st8(0x210740,opcode);++rejected;
 }
 for(unsigned kind:{1u,2u,255u}) {
  ps2::st8(car+0x136d,kind);std::memcpy(initial.data(),ps2::g_ram,initial.size());Options options;options.enabled=true;Experiment experiment(options);
  ps2::Cpu cpu{};cpu.r[4].d[0]=car;cpu.r[29].d[0]=0x49af80;auto before=cpu;experiment.probe(cpu,0x1e4d38,0);experiment.probe(cpu,0x1e4d5c,0);experiment.probe(cpu,0x1e4e68,0);
  require(experiment.finished()&&!experiment.counts.injected&&!std::memcmp(&before,&cpu,sizeof cpu)&&!std::memcmp(initial.data(),ps2::g_ram,initial.size()),"nonmanual isolation");
 }
 for(double value:{-1.0,std::nextafter(0.0,-1.0),std::nextafter(1.0,2.0),2.0,std::numeric_limits<double>::infinity(),-std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()}) {
  std::memcpy(initial.data(),ps2::g_ram,initial.size());Options options;options.enabled=true;options.value=value;bool threw=false;
  try{Experiment experiment(options);}catch(const std::invalid_argument &){threw=true;}
  require(threw&&!std::memcmp(initial.data(),ps2::g_ram,initial.size()),"invalid host values reject before guest access, never clamp");
 }
 if(table)require(std::fclose(table)==0,"original table close");
 std::printf("Virtual handbrake original oracle PASS: cases=%u full-CPU+32MiB-comparisons=%u semantic-observations=%u rear-formula-checks=%u rejected-contexts=%u invalid-values=7; all4097 Q12 codes, all4096 binary64 half-tie neighbors,8192 rational random inputs; Frozen actual substitutions; original notification/manual/coupling/brake/engine\n",cases,comparisons,observations,rear_checks,rejected);
}
