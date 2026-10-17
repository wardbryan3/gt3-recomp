// Game-free protocol consistency, NOT original-EE or live proof.
#include "gt3_virtual_handbrake.hpp"
#include "gt3_virtual_handbrake_samples.hpp"
#include <cassert>
#include <limits>
int main() {
 using namespace gt3::virtual_handbrake;
 const auto samples=virtual_handbrake_samples::all();
 for(auto sample:samples)assert(command_for_value(sample.value)==int(sample.q));
 for(double value:{-1.0,-.01,std::nextafter(0.0,-1.0),std::nextafter(1.0,2.0),1.01,std::numeric_limits<double>::max(),std::numeric_limits<double>::infinity(),-std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()}) {
  assert(command_for_value(value)==-1);Options options;options.enabled=true;options.value=value;bool threw=false;try{validate(options);}catch(const std::invalid_argument &){threw=true;}assert(threw);
 }
 for(auto text:{"0","1","0.5","0.25","0.0625","0.000244140625","0.1","0.9","000.5","00","1.000","0.000"}) {
  double value=-1;assert(parse_value(text,value)&&command_for_value(value)>=0);
 }
 for(auto text:{"","-0","-0.1","1.0000000000000002","nan","NaN","inf","-inf","1e-1",".5","0."," 0.5","0.5 ","0.5x","+0.5","0..5","2","99999999999999999999999999999999999999"}) {
  double value=.5;assert(!parse_value(text,value)&&value==.5);
 }
 Event event{99,.5};assert(parse_event("18446744073709551615:0.5",event)&&event.frame==std::numeric_limits<std::uint64_t>::max()&&event.value==.5);
 for(auto text:{"1","-1:0","1.0:0","18446744073709551616:0","1:-0.1","1:1.01","1:0:0",":0","1:inf"}) {
  auto before=event;assert(!parse_event(text,event)&&event.frame==before.frame&&event.value==before.value);
 }
 Options options;options.enabled=true;options.value=0;options.events={{10,.25},{20,.5},{30,1},{40,0}};validate(options);
 for(auto [frame,value]:std::vector<std::pair<std::uint64_t,double>>{{0,0},{9,0},{10,.25},{19,.25},{20,.5},{29,.5},{30,1},{39,1},{40,0},{std::numeric_limits<std::uint64_t>::max(),0}})assert(at_frame(options,frame)==value);
 for(unsigned kind=0;kind<4;++kind) {
  auto changed=options;if(kind==0)changed.events[1].frame=10;if(kind==1)changed.events[1].frame=9;if(kind==2)changed.events[1].value=1.01;if(kind==3)changed.enabled=false;
  bool threw=false;try{validate(changed);}catch(const std::invalid_argument &){threw=true;}assert(threw);
 }
 std::printf("Virtual handbrake source protocol PASS: %zu independent exact mappings; parser/range/finite/atomic-output/schedule tests; not original-game proof\n",samples.size());
}
