// Included only in the separately generated extended host, never canonical main.
#include "extensions/gt3/native_bindings/virtual_transmission.hpp"
namespace {
gt3::extensions::vt::Config gt3_ext_config;
bool gt3_ext_initial_seen=false;
[[noreturn]] void gt3_extension_invalid(const char *why){std::fprintf(stderr,"extension arguments: %s\n",why);std::exit(2);}
bool gt3_extension_arg(const std::string &a,int &i,int argc,char **argv){
 using namespace gt3::extensions::vt;
 auto value=[&]()->std::string_view{if(i+1>=argc)gt3_extension_invalid("missing value");return argv[++i];};
 if(a=="--virtual-transmission"){if(gt3_ext_config.enabled)gt3_extension_invalid("duplicate enable");gt3_ext_config.enabled=true;}
 else if(a=="--vt-initial"){if(gt3_ext_initial_seen)gt3_extension_invalid("duplicate initial sample");gt3_ext_initial_seen=true;if(!parse_input(value(),gt3_ext_config.initial))gt3_extension_invalid("expected clutch0|1:R|N|forward1..255");}
 else if(a=="--vt-at"){
  auto s=value();auto pos=s.find(':');Event e;
  if(pos==s.npos||!number(s.substr(0,pos),e.frame)||!parse_input(s.substr(pos+1),e.input))gt3_extension_invalid("expected frame:clutch:gear");gt3_ext_config.events.push_back(e);
 }
 else if(a=="--vt-disconnect"){Event e;e.disconnect=true;if(!number(value(),e.frame))gt3_extension_invalid("expected disconnect frame");gt3_ext_config.events.push_back(e);}
 else if(a=="--extensions-shadow"){if(gt3_ext_config.shadow)gt3_extension_invalid("duplicate shadow");gt3_ext_config.shadow=true;}
 else if(a=="--extensions-trace"){if(!gt3_ext_config.trace.empty())gt3_extension_invalid("duplicate trace");gt3_ext_config.trace=std::string(value());}
 else return false;
 return true;
}
bool gt3_extension_start(bool forbidden,const std::string &load_path){
 if(forbidden){std::fprintf(stderr,"extended runner rejects RAM patches/triple/axes; supported original execution only\n");return false;}
 if(gt3_ext_initial_seen&&!gt3_ext_config.enabled){std::fprintf(stderr,"initial sample requires startup activation\n");return false;}
 return gt3::extensions::vt::configure(std::move(gt3_ext_config),load_path);
}
}
