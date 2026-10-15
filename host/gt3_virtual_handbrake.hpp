#pragma once
// Virtual action input only. No physical-device calibration or vehicle behavior.
#include "ps2/cpu.hpp"
#include <array>
#include <charconv>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>
namespace gt3::virtual_handbrake {
// Finite binary64 [0,1] -> existing unsigned nonnegative Q12 halfword.
// The original analog floor is downstream: input .5 is Q2048, not force .5.
inline int command_for_value(double value) {
    if(!std::isfinite(value)||value<0||value>1)return -1;
    return int(std::lround(value*4096.0)); // exact power-of-two scale; half ties up
}
inline bool parse_value(std::string_view text,double &out) {
    if(text.empty())return false;
    bool dot=false,digit=false;
    for(char c:text) {
        if(c=='.'&&!dot&&digit){dot=true;digit=false;}
        else if(c>='0'&&c<='9')digit=true;
        else return false;
    }
    if(!digit)return false;
    double value=0;
    auto [end,error]=std::from_chars(text.data(),text.data()+text.size(),value,std::chars_format::fixed);
    if(error!=std::errc{}||end!=text.data()+text.size()||command_for_value(value)<0)return false;
    out=value;return true;
}
struct Event {std::uint64_t frame=0;double value=0;};
struct Options {bool enabled=false;double value=0;std::vector<Event> events;std::string trace_path;};
inline bool parse_event(std::string_view text,Event &out) {
    auto colon=text.find(':');if(colon==text.npos||colon==0)return false;
    for(char c:text.substr(0,colon))if(c<'0'||c>'9')return false;
    Event event;auto [end,error]=std::from_chars(text.data(),text.data()+colon,event.frame);
    if(error!=std::errc{}||end!=text.data()+colon||!parse_value(text.substr(colon+1),event.value))return false;
    out=event;return true;
}
inline void validate(const Options &options) {
    if(command_for_value(options.value)<0)throw std::invalid_argument("virtual handbrake outside [0,1]");
    if(!options.events.empty()&&!options.enabled)throw std::invalid_argument("scheduled handbrake requires explicit enable");
    for(std::size_t i=0;i<options.events.size();++i)
        if(command_for_value(options.events[i].value)<0||(i&&options.events[i-1].frame>=options.events[i].frame))
            throw std::invalid_argument("handbrake events must be valid and strictly increasing");
}
inline double at_frame(const Options &options,std::uint64_t frame) {
    double value=options.value;
    for(const auto &event:options.events){if(event.frame>frame)break;value=event.value;}
    return value;
}
bool profile_matches();
struct Counts {std::uint64_t injected=0,restored=0,entries=0,joins=0,brakes=0,brake_joins=0,engines=0,shifts=0;};
class Experiment {
public:
    explicit Experiment(Options options);
    ~Experiment();
    Experiment(const Experiment &)=delete;Experiment &operator=(const Experiment &)=delete;
    bool open_trace();
    void probe(ps2::Cpu &,unsigned pc,std::uint64_t frame);
    bool finished()const{return !active_&&!scoped_&&counts.injected==counts.restored;}
    Counts counts;
private:
    Options options_;FILE *trace_=nullptr;
    bool active_=false,eligible_=false,scoped_=false;
    unsigned car_=0,player_=0,owner_sp_=0,command_=0;
    std::array<unsigned char,16> saved_{},expected_{};
    double value_=0;
    void record(const char *stage,unsigned pc,std::uint64_t frame);
};
}
