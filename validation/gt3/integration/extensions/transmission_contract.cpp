// Independent controlled-original continuation contracts, NOT original ON parity.
#include "src/gt3/bindings/ps2/virtual-transmission/virtual_transmission.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
void register_generated_code();
namespace gen {void vt_contract_unit_0039(ps2::Cpu &,unsigned,unsigned);void vt_reference_unit_0039(ps2::Cpu &,unsigned,unsigned);}
namespace {unsigned action=0;bool override_selector=false;int requested=-1;unsigned seed=0x6d486e18,cases=0,whole=0;constexpr unsigned car=0x600000,sp=0x900000,gp=0x3579f0;
unsigned random_word(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
void require(bool x,const char *msg){if(!x){std::fprintf(stderr,"contract FAIL case%u action%u %s\n",cases,action,msg);std::exit(1);}}
ps2::Cpu fixture(){ps2::Cpu c{};for(unsigned j=0;j<sizeof c;++j)reinterpret_cast<unsigned char*>(&c)[j]=random_word();ps2::set32(c.r[4],car);ps2::set32(c.r[28],gp);ps2::set32(c.r[29],sp);ps2::set32(c.r[31],0x123456);c.budget=10000;c.pc=0x1e6d48;return c;}
void prefix(ps2::Cpu &c){using namespace ps2;set32(c.r[29],sp-48);st64(sp-48,c.r[16].d[0]);st64(sp-16,c.r[31].d[0]);set32(c.r[16],car+0xf84);st64(sp-32,c.r[17].d[0]);c.r[3].d[0]=ld8(car+0x13bb);c.budget-=8;set32(c.r[5],car+0x208);}
void compare(ps2::Cpu c,bool selection){using namespace ps2;
 const bool full=cases%64==0;std::vector<unsigned char> ram,expected;
 unsigned char object[0x1500],stack[160];std::memcpy(object,g_ram+car,sizeof object);std::memcpy(stack,g_ram+sp-128,sizeof stack);
 if(full){ram.assign(g_ram,g_ram+kRamSize);++whole;}
 auto ref=c;
 if(selection){set32(ref.r[29],sp-32);set32(ref.r[5],car+0x1304);st64(sp-32,ref.r[16].d[0]);st64(sp-16,ref.r[31].d[0]);ref.budget-=6;ps2::set32(ref.r[16],car+0xf84);ref.r[31].sd[0]=0x1e77f8;ref.r[2].sd[0]=requested;ref.pc=0x1e77f8;ref.budget-=2;gen::vt_reference_unit_0039(ref,154,0);}
 else if(action){prefix(ref);if(action==1)ref.f[1]=0;else set32(ref.r[2],2);gen::vt_reference_unit_0039(ref,action==1?1000:1001,0);}
 else gen::vt_reference_unit_0039(ref,123,0);
 unsigned char expected_object[0x1500],expected_stack[160];std::memcpy(expected_object,g_ram+car,sizeof object);std::memcpy(expected_stack,g_ram+sp-128,sizeof stack);if(full)expected.assign(g_ram,g_ram+kRamSize);
 if(full)std::memcpy(g_ram,ram.data(),ram.size());else{std::memcpy(g_ram+car,object,sizeof object);std::memcpy(g_ram+sp-128,stack,sizeof stack);}
 auto actual=c;gen::vt_contract_unit_0039(actual,selection?153:123,0);
 require(!std::memcmp(&ref,&actual,sizeof ref),"completeCPU/FCR/PC/SP/upper lanes/cost");require(!std::memcmp(expected_object,g_ram+car,sizeof object)&&!std::memcmp(expected_stack,g_ram+sp-128,sizeof stack),"object/stack");if(full)require(!std::memcmp(expected.data(),g_ram,expected.size()),"whole32MiB");
 if(action==1&&!selection)require(ld8(car+0x13bb)==0,"disengagement");if(action==2&&!selection)require(ld8(car+0x13bb)==2,"synchronization/preparation");++cases;
}
}
namespace gt3::extensions::vt {void admission_enter(ps2::Cpu &,unsigned){}unsigned admission_route(ps2::Cpu &,unsigned){return action;}bool selector(ps2::Cpu &c,unsigned){if(!override_selector)return false;c.r[2].sd[0]=requested;c.pc=c.r[31].w[0];c.budget-=2;return true;}}
int main(int argc,char **argv){using namespace ps2;if(argc!=2)return 2;register_generated_code();unsigned entry;require(load_elf(argv[1],entry),"ELF");g_options.on_probe=[](Cpu &,unsigned){};
 for(unsigned i=0;i<8192;++i){for(unsigned j=0;j<0x1500;j+=4)st32(car+j,random_word());for(unsigned j=0;j<128;j+=4)st32(sp-128+j,random_word());action=i%3;st8(car+0x13bb,action==2?0:i%4);st8(car+0x136d,0);st8(car+0x14b8,0);st8(car+0x13e5,1);st8(car+0x208,i%8);st8(car+0x13ba,i%7);compare(fixture(),false);}
 override_selector=true;action=0;
 for(unsigned i=0;i<4096;++i){st8(car+0x13bb,i%4);st8(car+0x13ba,(i/4)%7);requested=i%4?-1:int((i/4)%7);compare(fixture(),true);}
 require(cases==12288&&whole==192,"counts");std::printf("Original continuation contracts PASS:12288 completeCPU/FCR/ABI/cost/object+stack comparisons;192 whole32MiB;8192 admission OFF/free/start,4096 controlled selector-to-original commit. No whole-engine replacement or native proof.\n");}
