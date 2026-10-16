// Original-dependent standalone negative fixtures. NEVER native state injection.
#include "extensions/gt3/native_bindings/virtual_transmission.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <climits>
#include <string>
void register_generated_code();void register_generated_vu();
int main(int argc,char **argv){
 if(argc!=5)return 2;using namespace ps2;using namespace gt3::extensions::vt;
 g_options.disc_path=argv[4];g_options.pal=false;register_generated_code();register_generated_vu();
 unsigned entry;if(!load_elf(argv[1],entry))return 2;boot(entry,{});if(!load_state(argv[2]))return 2;
 Config cfg;cfg.enabled=true;if(!configure(cfg,argv[2]))return 2;
 Cpu c{};set32(c.r[4],0x1fbb7bc);set32(c.r[28],0x3579f0);set32(c.r[29],0x49af20);set32(c.r[31],0x1e6ef8);c.budget=10000;unsigned depth=3;std::string kind=argv[3];
 if(kind=="gp")c.r[28].d[0]=0;
 else if(kind=="stack")++c.r[29].d[0];
 else if(kind=="ra")c.r[31].d[0]=0;
 else if(kind=="upper-pointer")c.r[4].d[0]|=1ull<<32;
 else if(kind=="budget")c.budget=INT_MIN;
 else if(kind=="depth")depth=kMaxDepth;
 else if(kind=="code")g_ram[0x1e6d48]^=1;
 else if(kind=="calibration")g_ram[0x1fbb7bc+0x234]^=1;
 else if(kind=="state")st8(0x1fbb7bc+0x13bb,255);
 else if(kind=="gear")st8(0x1fbb7bc+0x13ba,7);
 else if(kind=="owner")st8(0x1fbb7bc+0x136d,1);
 else if(kind=="mode")st8(0x1fbb7bc+0x14b8,1);
 else if(kind=="policy")st8(0x1fbb7bc+0x13e5,0);
 else if(kind=="missing-player"){set32(c.r[4],0x600000);observe(c,0x1e5b98);std::fprintf(stderr,"UNSAFE CONTINUATION\n");return 99;}
 else if(kind!="duplicate")return 2;
 admission_enter(c,depth);if(kind=="duplicate")admission_enter(c,depth);
 std::fprintf(stderr,"UNSAFE CONTINUATION\n");return 99;
}
