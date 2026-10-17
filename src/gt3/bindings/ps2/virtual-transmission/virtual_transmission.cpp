#include "virtual_transmission.hpp"
#include "profile.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <limits>
#include <memory>
namespace gen {void unit_0039(ps2::Cpu &,unsigned,unsigned);void vt_reference_unit_0039(ps2::Cpu &,unsigned,unsigned);}
#ifndef GT3_EXT_VIRTUAL_TRANSMISSION
#define GT3_EXT_VIRTUAL_TRANSMISSION 0
#endif
namespace gt3::extensions::vt {
namespace {
using namespace ps2;
constexpr unsigned player=0x1fbb7bc,gp=0x3579f0;
Config options;FILE *trace=nullptr;bool shadowing=false;
std::uint64_t entries=0,shadows=0,free_routes=0,starts=0,ordinary=0,selectors=0,commits=0,rejections=0,last_frame=0,selector_frame=0;
Decision decision;Input sample;unsigned prior_selected=0;std::size_t cursor=0;bool transport_lost=false;
#if GT3_EXT_VIRTUAL_TRANSMISSION
std::unique_ptr<Controller> controller;
#endif
[[noreturn]] void fail(const char *why){std::fprintf(stderr,"[virtual-transmission] FAIL-CLOSED before further execution: %s\n",why);std::fflush(nullptr);std::_Exit(1);}
std::uint64_t hash(const unsigned char *p,std::size_t n,std::uint64_t h=0xcbf29ce484222325ull){for(std::size_t i=0;i<n;++i)h=(h^p[i])*0x100000001b3ull;return h;}
bool startup(const std::string &path){std::ifstream f(path,std::ios::binary);if(!f)return false;std::uint64_t h=0xcbf29ce484222325ull;char b[65536];while(f.read(b,sizeof b)||f.gcount())h=hash(reinterpret_cast<unsigned char*>(b),f.gcount(),h);if(!f.eof())return false;for(auto expected:startup_hashes)if(h==expected)return true;return false;}
bool profile(){
 for(auto x:code_profile)if(hash(g_ram+x.at,x.size)!=x.hash)return false;
 std::uint64_t h=0xcbf29ce484222325ull;for(auto x:calibration_spans)h=hash(g_ram+player+x.at,x.size,h);
 return h==calibration_hash&&ld8(player+0x136d)==0&&ld8(player+0x14b8)==0&&ld8(player+0x13e5)==1;
}
void context(const Cpu &c,unsigned depth,bool select){
 if(!profile()||c.r[4].d[0]!=player||c.r[28].d[0]!=gp||depth!=3||
    c.r[29].d[0]!=(select?0x49af40u:0x49af20u)||c.r[31].d[0]!=(select?0x1e77f8u:0x1e6ef8u)||
    c.budget<std::numeric_limits<int>::min()+4096||ld8(player+0x13bb)>3||ld8(player+0x13ba)>ld8(player+0x20a))fail("unsupported original profile/caller/frame/state/budget");
}
void controlled_reference(Cpu &c,unsigned depth){
 if(decision.route==Route::original){gen::vt_reference_unit_0039(c,123,depth);return;}
 // Independent original-prefix reconstruction; public contract test checks all CPU.
 const unsigned car=c.r[4].w[0];set32(c.r[29],c.r[29].w[0]-48);st64(c.r[29].w[0],c.r[16].d[0]);st64(c.r[29].w[0]+32,c.r[31].d[0]);set32(c.r[16],car+0xf84);st64(c.r[29].w[0]+16,c.r[17].d[0]);c.r[3].d[0]=ld8(car+0x13bb);c.budget-=8;set32(c.r[5],car+0x208);
 if(decision.route==Route::free)c.f[1]=0;else set32(c.r[2],2);
 gen::vt_reference_unit_0039(c,decision.route==Route::free?1000:1001,depth);
}
}
bool configure(Config config,const std::string &load_path){
 if(config.shadow&&!config.enabled){std::fprintf(stderr,"shadow requires explicit extension activation\n");return false;}
 if(!config.enabled&&!config.events.empty()){std::fprintf(stderr,"extension inputs require startup activation\n");return false;}
 if(config.enabled){
#if GT3_EXT_VIRTUAL_TRANSMISSION
  const char *one=std::getenv("PS2_ONE_THREAD");
  if(!one||std::strcmp(one,"1")){std::fprintf(stderr,"virtual transmission v1 requires PS2_ONE_THREAD=1\n");return false;}
  if(!startup(load_path)){std::fprintf(stderr,"virtual transmission requires a supported original MT native-v3 startup fixture\n");return false;}
  controller=std::make_unique<Controller>();
#else
  std::fprintf(stderr,"virtual transmission not included in this extended build\n");return false;
#endif
 }
 for(std::size_t j=1;j<config.events.size();++j)if(config.events[j-1].frame>=config.events[j].frame){std::fprintf(stderr,"extension events must be strictly increasing\n");return false;}
 options=std::move(config);sample=options.initial;transport_lost=!sample.connected;
 if(!options.trace.empty()){trace=std::fopen(options.trace.c_str(),"wx");if(!trace){std::fprintf(stderr,"new extension trace path required\n");return false;}}
 if(options.enabled||trace)std::atexit(finish);
 return true;
}
void admission_enter(Cpu &c,unsigned depth){
#if GT3_EXT_VIRTUAL_TRANSMISSION
 if(shadowing||!options.enabled||c.r[4].w[0]!=player)return;
 context(c,depth,false);auto frame=frame_count();if(entries&&frame!=last_frame+1)fail("unsupported reload/reset/duplicate or discontinuous owner updates");
 if(entries&&!decision.pending&&ld8(player+0x13ba)!=prior_selected)fail("unexpected ratio writer outside extension commit");
 while(cursor<options.events.size()&&options.events[cursor].frame<=frame){auto e=options.events[cursor++];if(e.disconnect||!e.input.connected)transport_lost=true;else sample=e.input;}
 sample.connected=!transport_lost;prior_selected=ld8(player+0x13ba);
 decision=controller->step({ld8(player+0x13bb),prior_selected,ld8(player+0x20a)},sample);
 last_frame=frame;++entries;rejections+=decision.rejected;
 if(decision.route==Route::free)++free_routes;else if(decision.route==Route::synchronize)++starts;else ++ordinary;
 if(options.shadow){
  const std::vector<unsigned char> before(g_ram,g_ram+kRamSize);auto ref=c;shadowing=true;controlled_reference(ref,depth);const std::vector<unsigned char> expected(g_ram,g_ram+kRamSize);std::memcpy(g_ram,before.data(),before.size());auto actual=c;gen::unit_0039(actual,123,depth);
  if(std::memcmp(&ref,&actual,sizeof c)||std::memcmp(g_ram,expected.data(),expected.size()))fail("controlled-original real-entry completeCPU/cost/32MiB shadow");
  std::memcpy(g_ram,before.data(),before.size());shadowing=false;++shadows;
 }
#else
 (void)c;(void)depth;
#endif
}
unsigned admission_route(Cpu &c,unsigned depth){
#if GT3_EXT_VIRTUAL_TRANSMISSION
 if(options.enabled&&c.r[4].w[0]==player){(void)depth;return unsigned(decision.route);}
#endif
 (void)c;(void)depth;return 0;
}
bool selector(Cpu &c,unsigned depth){
#if GT3_EXT_VIRTUAL_TRANSMISSION
 if(!options.enabled||c.r[4].w[0]!=player)return false;
 context(c,depth,true);if(last_frame!=frame_count()||selector_frame==last_frame||c.r[5].d[0]!=player+0x1304||c.r[16].d[0]!=player+0xf84)fail("selector owner/order/argument contract");
 if(decision.pending&&(decision.gear<0||unsigned(decision.gear)>ld8(player+0x20a)||ld8(player+0x13bb)!=0))fail("ratio commit must be valid and disengaged");
 c.r[2].sd[0]=decision.pending?decision.gear:-1;c.pc=c.r[31].w[0];c.budget-=2;selector_frame=last_frame;++selectors;return true;
#else
 (void)c;(void)depth;return false;
#endif
}
void observe(Cpu &c,unsigned pc){
 if(shadowing||(!options.enabled&&!trace))return;
 unsigned car=0;
 switch(pc){
 case 0x1e6d48:case 0x1e6ec8:case 0x1e5b98:case 0x1e7500:case 0x1e77e0:car=c.r[4].w[0];break;
 case 0x1e5d54:car=c.r[18].w[0];break;
 case 0x1e7590:car=c.r[17].w[0];break;
 case 0x1e77f8:case 0x1e783c:car=c.r[16].w[0]-0xf84;break;
 case 0x6d480000:car=c.r[16].w[0];break;
 }
 // Qualified player must precede every vehicle drive in this supported update order.
 // A lost/moved/reset owner must stop simulation, never leave an active feature inert.
 if(options.enabled&&pc==0x1e5b98&&last_frame!=frame_count())fail("player authority missing before vehicle drive");
 if(car!=player)return;
 if(options.enabled&&pc==0x1e5b98&&decision.route==Route::free&&ld8(car+0x13bb)!=0)fail("disengagement must precede drive");
 if(options.enabled&&pc==0x1e7500&&decision.route==Route::free&&(ld8(car+0x13bb)!=0||(ld32(car+0x1478)&0x7fffffff)))fail("held clutch/Neutral/loss must have zero engine-directed term");
 if(options.enabled&&pc==0x1e783c){
  if(selector_frame!=last_frame)fail("missing selector authority");
  if(decision.pending){if(ld8(car+0x13bb)!=0||ld8(car+0x13ba)!=unsigned(decision.gear))fail("original ratio-only commit result");++commits;}
  else if(ld8(car+0x13ba)!=prior_selected)fail("conflicting original selection");
 }
 if(!trace)return;
 std::fprintf(trace,"{\"frame\":%llu,\"pc\":%u,\"state\":%u,\"selected\":%u,\"maximum\":%u,\"candidate\":%u,\"engine\":%u,\"saved_engine\":%u,\"target\":%u,\"speed\":%u,\"accelerator\":%u,\"brake\":%u,\"rpm\":%u,\"inhibition\":%u,\"term\":%u,\"rear\":%u,\"relative\":%u,\"route\":%u,\"gear\":%d,\"clutch\":%u,\"lost\":%u,\"rejected\":%u,\"cpu\":\"",
 (unsigned long long)frame_count(),pc,ld8(car+0x13bb),ld8(car+0x13ba),ld8(car+0x20a),ld32(car+0x139c),ld32(car+0x13cc),ld32(car+0x1310),ld32(car+0x1314),ld32(car+0x140c),ld32(car+0x1428),ld32(car+0x13b0),ld16(car+0x1414),ld8(car+0x13be),ld32(car+0x1478),ld32(car+0x130c),ld8(car+0x1305),options.enabled?unsigned(decision.route):0,options.enabled?decision.gear:-1,unsigned(sample.clutch),unsigned(decision.lost),unsigned(decision.rejected));
 auto p=reinterpret_cast<const unsigned char*>(&c);for(unsigned j=0;j<sizeof c;++j)std::fprintf(trace,"%02x",p[j]);std::fprintf(trace,"\"}\n");
}
void finish(){
 std::fprintf(stderr,"VT entries=%llu shadows=%llu free=%llu starts=%llu ordinary=%llu selectors=%llu commits=%llu rejected=%llu lost=%u\n",(unsigned long long)entries,(unsigned long long)shadows,(unsigned long long)free_routes,(unsigned long long)starts,(unsigned long long)ordinary,(unsigned long long)selectors,(unsigned long long)commits,(unsigned long long)rejections,unsigned(decision.lost));
 if(options.enabled&&(!entries||entries!=selectors||(options.shadow&&shadows!=entries)))fail("missing entry/selector/shadow coverage");
 if(trace&&std::fclose(trace))fail("trace close");trace=nullptr;
}
}
