// Standalone typed-source integration test; no guest update or state injection.
#include "extensions/gt3/native_bindings/virtual_transmission.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();void register_generated_vu();
int main(int argc,char **argv){
 if(argc!=5)return 2;using namespace ps2;using namespace gt3::extensions::vt;
 g_options.disc_path=argv[4];g_options.pal=false;register_generated_code();register_generated_vu();
 unsigned entry;if(!load_elf(argv[1],entry))return 2;boot(entry,{});if(!load_state(argv[2]))return 2;
 Config cfg;cfg.enabled=true;cfg.initial={true,false,int(ld8(0x1fbb7bc+0x13ba))};
 if(!std::strcmp(argv[3],"initial"))cfg.initial.connected=false;
 else if(!std::strcmp(argv[3],"event"))cfg.events.push_back({frame_count(),{false,false,cfg.initial.gear},false});
 else return 2;
 if(!configure(cfg,argv[2]))return 2;
 Cpu c{};set32(c.r[4],0x1fbb7bc);set32(c.r[28],0x3579f0);set32(c.r[29],0x49af20);set32(c.r[31],0x1e6ef8);c.budget=10000;
 auto before=c;std::vector<unsigned char> ram(g_ram,g_ram+kRamSize);admission_enter(c,3);
 if(admission_route(c,3)!=1||std::memcmp(&c,&before,sizeof c)||std::memcmp(g_ram,ram.data(),ram.size()))std::_Exit(99);
 std::printf("Typed disconnected %s -> free before guest execution; completeCPU/32MiB unchanged PASS\n",argv[3]);std::fflush(nullptr);
 // Intentionally no guest execution/selector: don't invoke whole-run finish checks.
 std::_Exit(0);
}
