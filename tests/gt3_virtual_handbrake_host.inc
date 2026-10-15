// Appended only to the disposable, identity-checked handbrake validation host.
namespace {
gt3::virtual_handbrake::Experiment *virtual_handbrake_experiment=nullptr;
bool virtual_handbrake_error=false;
}
void virtual_handbrake_probe(ps2::Cpu &cpu,unsigned pc,std::uint64_t frame) {
    if(!virtual_handbrake_experiment||virtual_handbrake_error)return;
    try {virtual_handbrake_experiment->probe(cpu,pc,frame);}
    catch(const std::exception &e){virtual_handbrake_error=true;std::fprintf(stderr,"[gt3-virtual-handbrake] FAIL: %s\n",e.what());ps2::halt("virtual handbrake validation failed");}
}
int main(int argc,char **argv) {
    using namespace gt3::virtual_handbrake;
    Options options;bool seen=false,seen_trace=false;std::vector<char *> args{argv[0]};
    try {
        for(int i=1;i<argc;++i) {
            const std::string arg=argv[i];
            auto next=[&](){if(i+1>=argc)throw std::invalid_argument("missing virtual handbrake argument");return std::string_view(argv[++i]);};
            if(arg=="--gt3-virtual-handbrake") {
#if GT3_VIRTUAL_HANDBRAKE_GATE
                if(seen||!parse_value(next(),options.value))throw std::invalid_argument("expected one handbrake value in [0,1]");
                seen=true;options.enabled=true;
#else
                throw std::invalid_argument("Virtual handbrake build gate is OFF");
#endif
            } else if(arg=="--gt3-virtual-handbrake-at") {
                Event event;if(!parse_event(next(),event))throw std::invalid_argument("expected FRAME:VALUE");options.events.push_back(event);
            } else if(arg=="--gt3-virtual-handbrake-trace") {
                auto path=next();if(seen_trace||path.empty()||path.starts_with("--"))throw std::invalid_argument("invalid/duplicate virtual handbrake trace");
                seen_trace=true;options.trace_path=path;
            } else if(arg.starts_with("--gt3-virtual-handbrake"))throw std::invalid_argument("unknown virtual handbrake option");
            else args.push_back(argv[i]);
        }
        validate(options);
        Experiment experiment(options);if(!experiment.open_trace()){std::perror("virtual handbrake exclusive trace");return 2;}
        virtual_handbrake_experiment=&experiment;args.push_back(nullptr);
        const int result=handbrake_validation_host_main(int(args.size())-1,args.data());
        virtual_handbrake_experiment=nullptr;const auto &c=experiment.counts;
        std::fprintf(stderr,"[gt3-virtual-handbrake] injected=%llu restored=%llu entries=%llu joins=%llu brakes=%llu brake_joins=%llu engines=%llu shifts=%llu\n",
            (unsigned long long)c.injected,(unsigned long long)c.restored,(unsigned long long)c.entries,(unsigned long long)c.joins,
            (unsigned long long)c.brakes,(unsigned long long)c.brake_joins,(unsigned long long)c.engines,(unsigned long long)c.shifts);
        if(virtual_handbrake_error||!experiment.finished()||(options.enabled&&(!c.injected||c.injected!=c.entries||c.entries!=c.joins)))return 1;
        return result;
    } catch(const std::exception &e){std::fprintf(stderr,"Virtual handbrake: %s\n",e.what());return 2;}
}
