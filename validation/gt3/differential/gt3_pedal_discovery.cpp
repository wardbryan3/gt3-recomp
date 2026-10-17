// Discovery fixture only: ORIGINAL generated calls, no replacement and no new input API.
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <array>
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#ifdef GT3_PEDAL_DIFFERENTIAL
#include "gt3_clean_pedals.hpp"
#include <vector>
#endif
void register_generated_code();
namespace {
constexpr unsigned car=0x600000,input=0x501000,command=0x502000,race=0x700000,knots=0x710000;
void f(unsigned a,float v) { ps2::st32(a,std::bit_cast<unsigned>(v)); }
float get(unsigned a) { return std::bit_cast<float>(ps2::ld32(a)); }
void call(unsigned entry,unsigned a,unsigned b=0) {
    ps2::Cpu c{};c.pc=entry;c.budget=1000000;c.r[4].d[0]=a;c.r[5].d[0]=b;
    c.r[28].d[0]=0x3579f0;c.r[29].d[0]=0x800000;c.r[31].d[0]=0x1000000;
#ifdef GT3_PEDAL_DIFFERENTIAL
    const auto before=c;
    const std::vector<unsigned char> initial(ps2::g_ram,ps2::g_ram+0x2000000);
    gt3::pedals::enabled=false;
#endif
    ps2::call(c,entry,0);
#ifdef GT3_PEDAL_DIFFERENTIAL
    const auto expected=c;
    const std::vector<unsigned char> expected_ram(ps2::g_ram,ps2::g_ram+0x2000000);
    std::memcpy(ps2::g_ram,initial.data(),initial.size());c=before;gt3::pedals::enabled=true;
    ps2::call(c,entry,0);
    if(std::memcmp(&c,&expected,sizeof c)||std::memcmp(ps2::g_ram,expected_ram.data(),expected_ram.size())) {
        std::fprintf(stderr,"Whole original wrapper/consumer differential failed at %08x\n",entry);std::abort();
    }
    gt3::pedals::enabled=false;
#endif
    if(c.pc!=0x1000000 || c.r[29].w[0]!=0x800000)std::abort();
}
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;register_generated_code();unsigned entry;
    if(!ps2::load_elf(argv[1],entry))return 1;
    ps2::g_options.on_probe=[](ps2::Cpu &,unsigned){};
    unsigned cases=0;
    for(unsigned bank : {0u,16u}) for(unsigned raw : {0u,47u,48u,52u,53u,100u,174u,175u,179u,180u,255u}) {
        std::memset(ps2::g_ram+car,0,0x1800);std::memset(ps2::g_ram+input,0,0x150);
        std::memset(ps2::g_ram+race,0,0xb800);
        ps2::st32(input+0xc0,0x33f7e0);ps2::st32(input+0x14,0x20|(bank?8:0));
        ps2::st32(input+0x38+bank*4,512);ps2::st32(input+0x3c+bank*4,raw);ps2::st32(input+0x40+bank*4,raw);
        call(0x1f4330,command);call(0x2115f8,input,command);
        ps2::st32(car+4,race);f(car+0xec0,1.f/60);f(car+0x68,.5f);
        for(unsigned i=0;i<3;++i) {
            unsigned d=car+0x6c+i*0x3c,k=knots+i*16;
            ps2::st16(d,2);ps2::st32(d+4,k);ps2::st32(d+8,k+8);
            f(k,0);f(k+4,100);f(k+8,.5f);f(k+12,.5f);
        }
        // Identity response descriptors for an isolated synthetic state, NOT live calibration.
        std::memset(ps2::g_ram+0x49d060,0,32);
        call(0x1e4cb0,car,command);
        if(ps2::ld32(car+0x1428)!=ps2::ld32(car+0x13ac))std::abort();
        const unsigned brake=ps2::ld32(car+0x13b0);
        for(unsigned i=0;i<4;++i)if(ps2::ld32(car+0x1074+i*0xa4)!=brake)std::abort();
        f(car+0xe38,1);f(car+0xe3c,1);f(car+0xe40,1);
        call(0x1e6ec8,car);
        for(unsigned i=0;i<4;++i)if(ps2::ld32(car+0x1274+i*0x24)!=brake)std::abort();
        // Neutral/free-engine branch: processed throttle -> original engine torque -> speed update.
        ps2::st16(car+0x1d4,8000); // rev-limit configuration; zero would cut all torque
        f(car+0x13cc,100);f(car+0x2bc,1);f(car+0x1434,1);f(car+0x1438,0);
        call(0x1e7500,car);
        const unsigned expected=ps2::fp::add(std::bit_cast<unsigned>(100.f),ps2::fp::mul(ps2::ld32(car+0x1428),ps2::ld32(car+0xec0)));
        if(ps2::ld32(car+0x13cc)!=expected) { std::fprintf(stderr,"engine mismatch raw=%u actual=%08x expected=%08x\n",raw,ps2::ld32(car+0x13cc),expected); std::abort(); }
        std::printf("{\"bank\":%u,\"raw\":%u,\"q_accelerator\":%d,\"q_brake\":%d,\"flags\":%u,\"throttle\":%.9g,\"brake\":%.9g,\"effective_throttle\":%.9g,\"wheel_brake\":%.9g,\"engine_rate\":%.9g}\n",bank,raw,(int)(short)ps2::ld16(command+8),(int)(short)ps2::ld16(command+10),ps2::ld8(command),get(car+0x13ac),get(car+0x13b0),get(car+0x1428),get(car+0x1274),get(car+0x13cc));
        ++cases;
    }
    std::fprintf(stderr,"Original generated pedal discovery PASS: %u fixtures; no live pedal claim\n",cases);
#ifdef GT3_PEDAL_DIFFERENTIAL
    if(gt3::pedals::counts.replaced!=cases)std::abort();
    std::fprintf(stderr,"Clean pedal whole-wrapper/original-consumer PASS: %u fixtures, complete CPU and 32MiB RAM\n",cases);
#endif
}
