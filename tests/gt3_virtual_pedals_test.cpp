// Public, game-free parser/scheduling/mapping tests, not an original-game oracle.
#include "gt3_virtual_pedals.hpp"
#include <cstdlib>
#include <limits>
using namespace gt3::virtual_pedals;
void require(bool ok){if(!ok)std::abort();}
int main(){
 double v=99;
 for(auto s:{"0","1","0.5","00.125","0.0001"})require(parse_value(s,v));
 for(auto s:{"","nan","inf","-0","-1","+0.5"," 0","0 ",".5","0.","0.1.2","1.0001","0x1","1e-3","1:0"}){v=99;require(!parse_value(s,v)&&v==99);}
 Values pair;require(parse_values("0.25:0.5",pair)&&pair.throttle==.25&&pair.brake==.5);
 for(auto s:{"0","0:",":0","0:0:0","0:nan"})require(!parse_values(s,pair));
 Event e;require(parse_event("18446744073709551615:1:0",e)&&e.frame==UINT64_MAX);
 for(auto s:{"-1:0:0","+1:0:0","1:0","1::0","18446744073709551616:0:0","1:2:0"})require(!parse_event(s,e));
 for(unsigned n=0;n<=8192;++n){double x=n/8192.0;require(command_for_value(x)==int((n+1)/2));require(std::abs(command_for_value(x)/4096.0-x)<=1./8192);}
 require(command_for_value(std::numeric_limits<double>::quiet_NaN())==-1&&command_for_value(1.01)==-1);
 Options o;o.values={.25,.75};o.events={{0,{0,0}},{20,{1,0}},{30,{0,1}},{40,{0,0}}};validate(o);
 for(auto f:{0u,19u,20u,29u,30u,39u,40u,100u}){
  auto x=at_frame(o,f);require(x.throttle==((f>=20&&f<30)?1:0)&&x.brake==((f>=30&&f<40)?1:0));
 }
 for(unsigned scenario=0;scenario<4;++scenario){Options bad=o;
  if(scenario==0)bad.values.brake=2;
  if(scenario==1)bad.events[2].frame=20;
  if(scenario==2)bad.events[2].frame=19;
  if(scenario==3)bad.events[0].values.throttle=std::numeric_limits<double>::infinity();
  bool threw=false;try{validate(bad);}catch(const std::invalid_argument &){threw=true;}require(threw);
 }
 std::puts("Virtual pedal source-only PASS: 8193 exact quantizations; strict parser/ranges/order/duplicate/overflow/scheduling");
}
