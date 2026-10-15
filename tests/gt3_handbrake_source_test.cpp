// Synthetic public consistency only: NOT an original-game oracle or live proof.
#include "gt3_clean_handbrake.hpp"
#include "ps2/generated.hpp"
#include <cstdio>
#include <cstdlib>
namespace {
void require(bool b){if(!b)std::abort();}
}
int main(){
 using namespace gt3::handbrake;
 constexpr Calibration stock{0x3f800000,0x3f800000,0x3dcccccd};
 require(!enabled);
 require(process(16,0,0x7fc00000,stock).value==0);
 require(process(16,4096,0,stock).value==0x3f800000);
 require(process(0,-1,0,stock).value==0x3f800000);
 require(process(0,0,0x3f800000,stock).value==0);
 constexpr Calibration varied{0x3e800000,0x3e000000,0x3dcccccd};
 require(process(0,1,0xbf000000,varied).value==0xbe800000); // press does not clamp low
 require(process(0,0,0x40000000,varied).value==0x3ff00000); // release does not clamp high
 for(unsigned raw=0;raw<65536;++raw){
    const auto q=static_cast<std::int16_t>(raw);
    auto analog=process(16,q,0x7fc00000,stock);
    auto x=ps2::fp::mul(ps2::fp::cvt_s_w(static_cast<unsigned>(static_cast<int>(q))),0x39800000);
    const auto expected=q?ps2::fp::add(x,ps2::fp::mul(stock.floor,ps2::fp::sub(0x3f800000,x))):x;
    require(analog.value==expected && analog.cost==(q?21u:14u));
    require(process(0,q,0,stock).value==(q?0x3f800000u:0u));
 }
 std::puts("Handbrake public synthetic consistency PASS: all 65536 signed inputs; NOT original oracle/live proof");
}
