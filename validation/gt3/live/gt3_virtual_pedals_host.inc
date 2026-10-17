// Appended only to a disposable copy of the existing validation host.
namespace {
gt3::virtual_pedals::Experiment *virtual_experiment=nullptr;
bool virtual_error=false;
}
void gt3_virtual_probe(ps2::Cpu &c,unsigned pc,std::uint64_t frame) {
    if(!virtual_experiment||virtual_error)return;
    try {virtual_experiment->probe(c,pc,frame);}
    catch(const std::exception &e){virtual_error=true;std::fprintf(stderr,"[gt3-virtual-pedals] FAIL: %s\n",e.what());ps2::halt("virtual pedal validation failed");}
}
int main(int argc,char **argv) {
    using namespace gt3::virtual_pedals;
    Options options;bool seen=false,seen_trace=false;std::vector<char *> args{argv[0]};
    try {
        for(int i=1;i<argc;++i){
            const std::string arg=argv[i];
            auto next=[&](){if(i+1>=argc)throw std::invalid_argument("missing virtual pedal argument");return std::string_view(argv[++i]);};
            if(arg=="--gt3-virtual-pedals"){
#if GT3_VIRTUAL_PEDAL_GATE
                if(seen||!parse_values(next(),options.values))throw std::invalid_argument("expected one THROTTLE:BRAKE pair in [0,1]");
                seen=true;options.enabled=true;
#else
                throw std::invalid_argument("Virtual pedal validation build gate is OFF");
#endif
            } else if(arg=="--gt3-virtual-pedals-at"){
                Event e;if(!parse_event(next(),e))throw std::invalid_argument("expected FRAME:THROTTLE:BRAKE");options.events.push_back(e);
            } else if(arg=="--gt3-virtual-pedals-trace"){
                auto path=next();if(seen_trace||path.empty()||path.starts_with("--"))throw std::invalid_argument("invalid/duplicate virtual pedal trace");
                seen_trace=true;options.trace_path=path;
            } else if(arg.starts_with("--gt3-virtual"))throw std::invalid_argument("unknown virtual pedal option");
            else args.push_back(argv[i]);
        }
        if(!options.events.empty()&&!options.enabled)throw std::invalid_argument("scheduled virtual pedals require explicit enable");
        validate(options);
        Experiment experiment(options);if(!experiment.open_trace()){std::perror("virtual pedal exclusive trace");return 2;}
        virtual_experiment=&experiment;args.push_back(nullptr);
        const int result=pedal_validation_host_main(int(args.size())-1,args.data());
        virtual_experiment=nullptr;
        const auto &c=experiment.counts;
        std::fprintf(stderr,"[gt3-virtual-pedals] injected=%llu restored=%llu entries=%llu joins=%llu brakes=%llu engines=%llu\n",
            (unsigned long long)c.injected,(unsigned long long)c.restored,(unsigned long long)c.entries,(unsigned long long)c.joins,(unsigned long long)c.brakes,(unsigned long long)c.engines);
        if(virtual_error||!experiment.finished()||(options.enabled&&(!c.injected||c.injected!=c.entries||c.entries!=c.joins)))return 1;
        return result;
    } catch(const std::exception &e){std::fprintf(stderr,"Virtual pedals: %s\n",e.what());return 2;}
}
