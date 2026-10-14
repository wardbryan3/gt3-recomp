// Source-only regression: synthetic data, not an original-game differential.
#include "gt3_controls.hpp"
#include "gt3_clean_steering.hpp"
#include "gt3_synthetic_wheel.hpp"
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <limits>
static void require(bool ok, const char *what) {
    if (!ok) { std::fprintf(stderr, "FAIL: %s\n", what); std::abort(); }
}
int main() {
    std::array<std::uint8_t, 256> curve{};
    for (unsigned i=0;i<256;++i) curve[i]=i; // synthetic identity; no original table
    unsigned cases=0;
    for (unsigned channel : {0u, 0x100u, 0x200u, 4u, 0x104u})
        for (unsigned raw=0;raw<256;++raw)
            for (unsigned sensitivity : {20u,35u,65u,100u,200u}) {
                gt3::clean::Cost cost;
                require(std::uint32_t(gt3::clean::normalize_mapped_channel(channel,raw,sensitivity,curve.data(),cost)) ==
                        gt3::normalize_mapped_input(channel,raw,sensitivity,curve), "reference positive-domain consistency");
                require(cost.instructions>0, "cost recorded"); ++cases;
            }
    gt3::clean::Cost cost;
    require(gt3::clean::normalize_mapped_channel(4,255,0,curve.data(),cost)==-1,"EE zero divisor result");
    bool threw=false;
    try { gt3::normalize_mapped_input(4,255,0,curve); } catch (const std::invalid_argument &) { threw=true; }
    require(threw,"standalone zero contract remains distinct");
    for (int q=-4096;q<=4096;++q) {
        const double value=double(q)/4096;
        const int axis=gt3::synthetic::axis_for_value(value);
        require(axis>=0 && axis<=1023,"axis range");
        gt3::clean::InputPartial input{}; input.type_bits=32;
        input.channels[0]=axis; input.channels[1]=input.channels[2]=255;
        gt3::clean::Command command{}; command.accelerator=123; command.brake=456;
        gt3::clean::Cost wheel_cost;
        gt3::clean::build_wheel_command(input,command,wheel_cost);
        require(command.steering==gt3::wheel_steering_command(axis),"wheel helper consistency");
        require(command.steering_mode==4 && (command.analog_flags&1),"wheel mode and presence");
        require(command.accelerator==123 && command.brake==456,"released command persistence");
        require(std::abs(double(command.steering)/4096-value)<=4.5/4096,"quantization bound");
    }
    double value=0; gt3::synthetic::Event event{};
    require(gt3::synthetic::parse_value("+0.5",value) && value==0.5,"value parser");
    for (const char *bad : {"", "nan", "inf", "1.01", "0.5junk"}) require(!gt3::synthetic::parse_value(bad,value),"invalid value rejected");
    require(gt3::synthetic::parse_event("4801:-0.5",event) && event.frame==4801 && event.value==-0.5,"event parser");
    require(!gt3::synthetic::parse_event("-1:0",event),"negative frame rejected");
    require(gt3::synthetic::axis_for_value(std::numeric_limits<double>::quiet_NaN())==-1,"nonfinite axis rejected");
    require(!gt3::clean::enabled,"clean runtime default remains disabled");
    std::printf("Source-only consistency PASS: %u normalizations, 8193 quantizations; NOT an original oracle/live test\n",cases);
}
