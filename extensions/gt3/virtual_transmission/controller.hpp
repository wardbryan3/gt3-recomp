#pragma once
// Deliberate extension policy, NOT a recovered original transmission model.
#include <charconv>
#include <cstdint>
#include <stdexcept>
#include <string_view>
namespace gt3::extensions::vt {
constexpr int neutral=-1;
struct Input {bool connected=true;bool clutch=true;int gear=neutral;};
struct Snapshot {unsigned state,selected,maximum;};
enum class Route:unsigned {original=0,free=1,synchronize=2};
struct Decision {Route route=Route::original;int gear=neutral;bool pending=false,lost=false,rejected=false;};
class Controller {
 bool attached_=false,lost_=false,prior_clutch_=false;int accepted_=neutral;
public:
 Decision step(Snapshot,Input);
};
inline bool number(std::string_view s,std::uint64_t &n){
 if(s.empty())return false;for(char c:s)if(c<'0'||c>'9')return false;
 auto [p,e]=std::from_chars(s.data(),s.data()+s.size(),n);return e==std::errc{}&&p==s.data()+s.size();
}
inline bool parse_input(std::string_view s,Input &out){
 if(s.size()<3||s[1]!=':'||(s[0]!='0'&&s[0]!='1'))return false;
 Input x;x.clutch=s[0]=='1';auto g=s.substr(2);std::uint64_t n=0;
 if(g=="N")x.gear=neutral;else if(g=="R")x.gear=0;
 else {if(!number(g,n)||n==0||n>255)return false;x.gear=int(n);}
 out=x;return true;
}
}
