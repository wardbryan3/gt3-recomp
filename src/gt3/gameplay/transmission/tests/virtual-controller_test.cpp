#include "src/gt3/gameplay/transmission/virtual/controller.hpp"
#include <cstdio>
#include <cstdlib>
using namespace gt3::extensions::vt;
unsigned checks=0;
void check(bool b){++checks;if(!b){std::fprintf(stderr,"controller FAIL check%u\n",checks);std::exit(1);}}
int main(){
 for(unsigned m=1;m<=16;++m)for(unsigned s=0;s<4;++s)for(unsigned old=0;old<=m;++old)for(int gear=-1;gear<=int(m)+1;++gear)for(bool clutch:{false,true}){
  Controller c;auto d=c.step({s,old,m},{true,clutch,gear});check(d.gear>=-1&&d.gear<=int(m));
  if(clutch||gear==-1)check(d.route==Route::free);
  if(gear>int(m)){check(d.rejected);check(d.gear==int(old));}
  if(d.pending)check(d.route==Route::free);
  if(!clutch&&gear==int(old)&&s==0)check(d.route==Route::synchronize);
  if(!clutch&&gear==int(old)&&s>0)check(d.route==Route::original);
 }
 for(unsigned m:{1u,4u,5u,6u,8u,255u})for(unsigned gear:{0u,m,m+1}){Controller x;auto d=x.step({0,0,m},{true,true,int(gear)});check(d.rejected==(gear>m));check(d.gear>=0&&d.gear<=int(m));}
 Controller c;auto d=c.step({2,3,6},{true,true,4});check(d.route==Route::free&&d.pending&&d.gear==4);
 d=c.step({0,4,6},{true,false,4});check(d.route==Route::synchronize&&!d.pending);
 d=c.step({2,4,6},{true,false,4});check(d.route==Route::original);
 d=c.step({2,4,6},{true,false,5});check(d.rejected&&d.gear==4&&d.route==Route::original);
 d=c.step({3,4,6},{true,true,0});check(d.route==Route::free&&d.pending&&d.gear==0);
 d=c.step({0,0,6},{true,false,1});check(d.route==Route::free&&d.pending&&d.gear==1); // prior clutch permits atomic release+shift
 d=c.step({0,1,6},{true,false,1});check(d.route==Route::synchronize);
 d=c.step({1,1,6},{true,false,-1});check(d.route==Route::free&&d.gear==-1);
 d=c.step({0,1,6},{true,false,6});check(d.route==Route::free&&d.pending);
 d=c.step({0,6,6},{true,false,6});check(d.route==Route::synchronize);
 d=c.step({2,6,6},{false,false,1});check(d.lost&&d.gear==-1&&d.route==Route::free);
 for(unsigned i=0;i<10000;++i){d=c.step({i%4,6,6},{true,bool(i%2),int(i%8)-1});check(d.lost&&d.gear==-1&&!d.pending&&d.route==Route::free);}
 for(auto invalid: {Snapshot{4,1,6},Snapshot{0,7,6},Snapshot{0,0,0},Snapshot{0,0,256}}){bool threw=false;try{Controller x;x.step(invalid,{});}catch(const std::invalid_argument&){threw=true;}check(threw);}
 for(auto s:{"0:N","1:R","0:1","1:255"}){Input x;check(parse_input(s,x));}
 for(auto s:{"","2:N","1:0","1:256","1:-1","1:n","true:1","1:1x","1: 1","1:1:2"}){Input x;check(!parse_input(s,x));}
 std::uint64_t n=0;check(number("18446744073709551615",n));check(!number("18446744073709551616",n));check(!number("-1",n));
 std::printf("Virtual transmission public pure-policy PASS:%u checks; no original/native physics proof.\n",checks);
}
