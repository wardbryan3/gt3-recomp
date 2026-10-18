// Independent, unmodified generated-original execution versus memory-native
// recovery. No original code patches or hooks. Synthetic fixtures are readable,
// aligned fixed pools and finite, well-formed intrusive lists, not saved games.
// Original ABI stack bytes are outside the recovered API; compare ALL other RAM.
#include "gt3_garage.hpp"
#include "ps2/generated.hpp"
#include "ps2/system.hpp"
#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <numeric>
#include <vector>

void register_generated_code();
namespace {
using U=std::uint32_t; using Q=std::uint64_t;
namespace model=gt3::economy_recovery;
constexpr U base=0x500000, pool=base+0x138, list=base+0x1b6b8;
constexpr U sp=0x1f00000, sentinel=0xdeadbee0, gp=0x3579f0;
unsigned cases=0, seed=0x218f88, resets=0;
void require(bool ok,const char* message) { if(!ok){std::fprintf(stderr,"FAIL garage case=%u %s\n",cases,message);std::exit(1);} }
U random_word(){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
U slot(U i){return pool+i*560;}
struct Event {U argument; bool after; std::vector<unsigned char> region; bool operator==(const Event&)const=default;};
std::vector<Event> events;
void capture(U arg,bool after){events.push_back({arg,after,{ps2::g_ram+base,ps2::g_ram+base+0x1b6c8}});}
Q original(U pc,U a0,U a1=0,bool observe=false,U stack=sp) {
    ps2::Cpu c{};
    for(U i=0;i<32;++i){c.r[i].d[0]=0xabc0000000000000ULL+i;c.r[i].d[1]=0xdef0000000000000ULL+i;}
    ps2::set32(c.r[0],0); ps2::set32(c.r[4],a0);ps2::set32(c.r[5],a1);
    ps2::set32(c.r[28],gp);ps2::set32(c.r[29],stack);ps2::set32(c.r[31],sentinel);
    c.pc=pc;c.budget=1000000;
    std::array<Q,8> saved{};for(U i=0;i<8;++i)saved[i]=c.r[16+i].d[0];
    U return_pc=0, reset_arg=0; unsigned steps=0;
    while(c.pc!=sentinel){
        require(++steps<10000,"original termination");
        if(observe && return_pc && c.pc==return_pc){capture(reset_arg,true);return_pc=0;}
        if(observe && c.pc==0x237980){reset_arg=c.r[4].w[0];capture(reset_arg,false);return_pc=c.r[31].w[0];}
        ps2::dispatch(c,c.pc,ps2::kMaxDepth);
    }
    require(c.r[29].w[0]==stack,"original SP restored");
    for(U i=0;i<8;++i)require(c.r[16+i].d[0]==saved[i],"original callee-saved GPR");
    return c.r[2].d[0];
}
struct Memory:model::garage_boundary {
    U load32(U a)override{return ps2::ld32(a);}
    void store32(U a,U v)override{ps2::st32(a,v);}
    void FUN_00237980(U a)override{
        capture(a,false);
        // Preserve this unrecovered operation by running the untouched callee.
        original(0x237980,a,0,false,sp-128);
        capture(a,true);++resets;
    }
};
std::vector<unsigned char> baseline, before, expected;
void fixture(const std::vector<U>& indices,int current=-1) {
    std::memcpy(ps2::g_ram,baseline.data(),baseline.size());
    for(U offset=0;offset<0x1b6c8;offset+=4)ps2::st32(base+offset,random_word());
    for(U i=0;i<200;++i){ps2::st32(slot(i),0);ps2::st32(slot(i)+4,0);ps2::st32(slot(i)+0x228,0);}
    for(U j=0;j<indices.size();++j){
        U p=slot(indices[j]);ps2::st32(p,j+1<indices.size()?slot(indices[j+1]):0);
        ps2::st32(p+4,j?slot(indices[j-1]):0);ps2::st32(p+0x228,j%2?0xffffffffu:1u);
    }
    ps2::st32(list,indices.empty()?0:slot(indices.front()));
    ps2::st32(list+4,indices.empty()?0:slot(indices.back()));
    ps2::st32(base+0x30,U(current));ps2::st32(base+0x34,U(current));
    ps2::st32(base+0x38,U(indices.size()));
}
void normalize_stack(std::vector<unsigned char>& image){
    // Reserved 512-byte ABI workspace covers the original reset/remove chain
    // and the separately executed opaque reset. No gameplay region is masked.
    std::memcpy(image.data()+sp-512,before.data()+sp-512,512);
}
Q compare(U pc,U a0,U a1,const std::function<Q(Memory&)>& recovered,bool compare_return=false) {
    before.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    events.clear();const Q result=original(pc,a0,a1,true);const auto original_events=events;
    expected.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);normalize_stack(expected);
    std::memcpy(ps2::g_ram,before.data(),before.size());events.clear();Memory memory;
    const Q clean=recovered(memory);
    if(compare_return)require(clean==result,"logical return bits");
    require(events==original_events,"opaque reset arguments, order and before/after region");
    std::memcpy(ps2::g_ram+sp-512,before.data()+sp-512,512);
    require(std::memcmp(ps2::g_ram,expected.data(),expected.size())==0,"complete nonstack RAM");
    ++cases;return clean;
}
std::vector<U> prefix(U n){std::vector<U> v(n);std::iota(v.begin(),v.end(),0);return v;}
}
int main(int argc,char**argv){
    require(argc==2,"ELF argument");register_generated_code();U entry;
    require(ps2::load_elf(argv[1],entry),"original ELF load");
    baseline.assign(ps2::g_ram,ps2::g_ram+ps2::kRamSize);
    // Every free-slot position and exhaustion, with well-formed matching lists.
    for(U free=0;free<=200;++free){
        fixture(prefix(free));
        auto result=compare(0x218f88,base,0,[&](Memory&m){return model::FUN_00218f88(m,base);},true);
        require(result==(free==200?0:slot(free)),"first-free position/full");
    }
    for(U k=0;k<64;++k){std::vector<U> ids;for(U i=0;i<200;++i)if(random_word()%3)ids.push_back(i);fixture(ids);
        compare(0x218f88,base,0,[&](Memory&m){return model::FUN_00218f88(m,base);},true);}
    const unsigned pool_cases=cases;
    for(U count:{0u,1u,2u,9u,199u})for(int current:{-1,0,5}){
        if(current>=int(count))continue;
        fixture(prefix(count),current);U node=slot(count);ps2::st32(node+0x228,1);
        // Parent insertion expects a nonnull, initialized detached record.
        compare(0x218fe0,base,node,[&](Memory&m){model::FUN_00218fe0(m,base,node);return 0;});
        require(ps2::ld32(base+0x38)==count+1,"insertion count");
        fixture(prefix(count),current);
        compare(0x23c1b8,list,node,[&](Memory&m){return Q(model::FUN_0023c1b8(m,list,node));},true);
    }
    for(U count:{0u,1u,2u,5u,200u}){
        fixture(prefix(count));compare(0x23c1b8,list,0,[&](Memory&m){return Q(model::FUN_0023c1b8(m,list,0));},true);
        fixture(prefix(count));compare(0x23c288,list,0,[&](Memory&m){return Q(model::FUN_0023c288(m,list,0));},true);
        fixture(prefix(count));compare(0x219190,base,0,[&](Memory&m){model::FUN_00219190(m,base,0);return 0;});
        for(U position=0;position<count;++position){
            if(count==200 && position!=0 && position!=99 && position!=199)continue;
            fixture(prefix(count));U node=slot(position);
            compare(0x23c4a8,list,node,[&](Memory&m){return model::FUN_0023c4a8(m,list,node);},true);
            fixture(prefix(count));compare(0x23c288,list,node,[&](Memory&m){return Q(model::FUN_0023c288(m,list,node));},true);
            for(int selected:{-1,0,int(count/2),int(count-1)}){
                fixture(prefix(count),selected);
                compare(0x219190,base,node,[&](Memory&m){model::FUN_00219190(m,base,node);return 0;});
                require(ps2::ld32(base+0x38)==count-1 && ps2::ld32(node+0x228)==0,"count and freed slot");
            }
        }
        fixture(prefix(count));compare(0x23c4a8,list,0x700000,[&](Memory&m){return model::FUN_0023c4a8(m,list,0x700000);},true);
    }
    for(U index:{0u,99u,199u}){
        fixture(prefix(200));U node=slot(index);
        compare(0x23af40,node,0,[&](Memory&m){model::FUN_0023af40(m,node);return 0;});
        // Full-pool removal then free selection and reinsertion. The explicit
        // occupancy store is a fixture's initialized-record precondition, NOT a
        // replacement for original configuration construction or a purchase.
        fixture(prefix(200));
        compare(0x219190,base,node,[&](Memory&m){model::FUN_00219190(m,base,node);return 0;});
        Q chosen=compare(0x218f88,base,0,[&](Memory&m){return model::FUN_00218f88(m,base);},true);
        require(chosen==node,"freed slot reselected");ps2::st32(node+0x228,1);
        compare(0x218fe0,base,node,[&](Memory&m){model::FUN_00218fe0(m,base,node);return 0;});
    }
    std::printf("PASS garage differentials=%u pool=%u original-reset-compositions=%u; complete nonstack 32MiB and ordered reset checkpoints\n",cases,pool_cases,resets);
    std::puts("Scope: memory-native projections, not full Cpu/stack/cost equivalence; FUN_00237980 remains original. Synthetic instruction-contract fixtures, not gameplay or integration proof.");
}
