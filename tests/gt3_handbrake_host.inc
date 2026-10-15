// Validation-only CLI; no synthetic handbrake source or command mutation.
namespace {
FILE *handbrake_trace=nullptr;
unsigned handbrake_car=0,handbrake_command=0;
}
void handbrake_probe(ps2::Cpu &c,unsigned pc,std::uint64_t frame) {
    if(pc==0x1e4bb8){handbrake_car=c.r[23].w[0];handbrake_command=c.r[18].w[0];}
    if(!handbrake_trace||!handbrake_car)return;
    if(pc!=0x1e4bb8&&pc!=0x1e4c60&&pc!=0x1e4c74&&pc!=0x1e6ec8&&
       pc!=0x1e6fc8&&pc!=0x1e5e1c&&pc!=0x1e5eac&&pc!=0x1e7500&&
       pc!=0x1e3a90&&pc!=0x1e3aac&&pc!=0x1e3ab8)return;
    if((pc==0x1e6ec8||pc==0x1e7500)&&c.r[4].w[0]!=handbrake_car)return;
    if(pc==0x1e6fc8&&c.r[17].w[0]!=handbrake_car+0xf84)return;
    if((pc==0x1e3a90||pc==0x1e3aac||pc==0x1e3ab8)&&c.r[17].w[0]!=handbrake_car)return;
    if((pc==0x1e5e1c||pc==0x1e5eac)&&c.r[16].w[0]!=handbrake_car+0xf84)return;
    std::fprintf(handbrake_trace,"{\"frame\":%llu,\"pc\":%u,\"car\":%u,\"command\":%u,",
        (unsigned long long)frame,pc,handbrake_car,handbrake_command);
    trace_cpu(handbrake_trace,c,pc);
    std::fprintf(handbrake_trace,",\"flags\":%u,\"input\":%d,\"processed\":%u,\"coupling_candidate\":%u,\"wheel_brake\":[",
        ps2::ld8(handbrake_command),static_cast<short>(ps2::ld16(handbrake_command+14)),
        ps2::ld32(handbrake_car+0x13b4),ps2::ld32(handbrake_car+0x139c));
    for(unsigned i=0;i<4;++i)std::fprintf(handbrake_trace,"%s%u",i?",":"",ps2::ld32(handbrake_car+0x1274+i*0x24));
    std::fprintf(handbrake_trace,"]}\n");
}
int main(int argc,char **argv) {
    bool enabled=false;std::string trace;std::vector<char *> forwarded{argv[0]};
    for(int i=1;i<argc;++i){std::string a=argv[i];
        if(a=="--gt3-clean-handbrake") {
#if GT3_HANDBRAKE_VALIDATION_GATES
            enabled=true;
#else
            std::fprintf(stderr,"Handbrake build gate is OFF\n");return 2;
#endif
        } else if(a=="--gt3-handbrake-trace"&&i+1<argc)trace=argv[++i];
        else forwarded.push_back(argv[i]);
    }
    forwarded.push_back(nullptr);
    if(!trace.empty()){handbrake_trace=std::fopen(trace.c_str(),"wx");if(!handbrake_trace)return 1;}
    gt3::handbrake::enabled=enabled;
    int result=pedal_validation_host_main(int(forwarded.size())-1,forwarded.data());
    if(handbrake_trace)std::fclose(handbrake_trace);
    const auto n=gt3::handbrake::counts;
    std::fprintf(stderr,"[gt3-handbrake] replaced=%llu fallback=%llu depth_boundary=%llu\n",
        (unsigned long long)n.replaced,(unsigned long long)n.fallback,(unsigned long long)n.depth_boundary);
    if((enabled||!trace.empty())&&!handbrake_car)return 1;
    return result;
}
