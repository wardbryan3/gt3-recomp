#pragma once
// Validation-only virtual command input. Not physical calibration or a DriverInput API.
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
namespace gt3::virtual_pedals {
struct Values { double throttle=0,brake=0; };
struct Event { std::uint64_t frame=0; Values values; };
struct Options { bool enabled=false; Values values; std::vector<Event> events; std::string trace_path; };
inline bool parse_value(std::string_view s,double &out) {
    if(s.empty())return false;
    bool dot=false,digit=false;
    for(char c:s) {
        if(c=='.'&&!dot&&digit){dot=true;digit=false;}
        else if(c>='0'&&c<='9')digit=true;
        else return false;
    }
    if(!digit)return false;
    double v=0;auto [end,error]=std::from_chars(s.data(),s.data()+s.size(),v,std::chars_format::fixed);
    if(error!=std::errc{}||end!=s.data()+s.size()||!std::isfinite(v)||v<0||v>1)return false;
    out=v;return true;
}
inline bool parse_values(std::string_view s,Values &out) {
    auto colon=s.find(':');if(colon==s.npos)return false;Values v;
    if(!parse_value(s.substr(0,colon),v.throttle)||!parse_value(s.substr(colon+1),v.brake))return false;
    out=v;return true;
}
inline bool parse_event(std::string_view s,Event &out) {
    auto colon=s.find(':');if(colon==s.npos||colon==0)return false;
    for(char c:s.substr(0,colon))if(c<'0'||c>'9')return false;
    Event e;auto [end,error]=std::from_chars(s.data(),s.data()+colon,e.frame);
    if(error!=std::errc{}||end!=s.data()+colon||!parse_values(s.substr(colon+1),e.values))return false;
    out=e;return true;
}
inline int command_for_value(double v) {
    if(!std::isfinite(v)||v<0||v>1)return -1;
    return int(std::lround(v*4096.0)); // Q12, positive half-ties round up
}
inline void validate(const Options &o) {
    auto valid=[](Values v){return command_for_value(v.throttle)>=0&&command_for_value(v.brake)>=0;};
    if(!valid(o.values))throw std::invalid_argument("virtual pedal values outside [0,1]");
    for(std::size_t i=0;i<o.events.size();++i)
        if(!valid(o.events[i].values)||(i&&o.events[i-1].frame>=o.events[i].frame))
            throw std::invalid_argument("virtual pedal events must be valid and strictly increasing");
}
inline Values at_frame(const Options &o,std::uint64_t frame) {
    Values v=o.values;
    for(const auto &e:o.events){if(e.frame>frame)break;v=e.values;}return v;
}
bool profile_matches();
struct Counts { std::uint64_t injected=0,restored=0,entries=0,joins=0,brakes=0,engines=0; };
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
    bool active_=false,scoped_=false,eligible_=false;
    unsigned car_=0,player_=0,owner_sp_=0,command_=0;
    std::array<unsigned char,16> saved_{},expected_{};Values values_;
    void record(const char *,unsigned,std::uint64_t);
};
}
