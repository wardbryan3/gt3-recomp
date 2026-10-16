// Newly written bounded search with explicit outgoing EE ABI bookkeeping.
// See docs/site/docs/transmission-speed-v1.md. No original tables/instructions.
#include "gt3_clean_transmission_speed.hpp"
#include "ps2/generated.hpp"
#include <limits>
namespace gt3::transmission_speed {
bool enabled=false;
Counts counts;
namespace {
void word(ps2::Cpu &c,unsigned reg,unsigned value) { ps2::set32(c.r[reg],value); }
void finish(ps2::Cpu &c,std::uint64_t index) {
    c.budget-=2;c.r[2].d[0]=index;c.pc=c.r[31].w[0];
}
void search(ps2::Cpu &c,unsigned object) {
    c.f[0]=0;
    const bool negative=ps2::fp::key(c.f[12])<ps2::fp::key(0);
    ps2::fpu_compare(c,negative);word(c,3,object+0x208);c.budget-=5;
    if(negative) {finish(c,0);return;}
    const unsigned maximum=ps2::ld8(object+0x20a);
    c.r[7].d[0]=maximum;word(c,5,1);c.r[2].d[0]=1<maximum;
    // This pointer advance is a delay-slot effect even for maximum0/1.
    word(c,4,object+0x264);c.budget-=5;
    if(maximum<=1) {finish(c,maximum);return;}
    c.r[6].d[0]=ps2::ld16(object+0x236);
    word(c,3,c.r[6].w[0]-500u);
    c.f[2]=ps2::ld32(c.r[28].w[0]-0x75e4);c.budget-=4;
    for(unsigned trial=1;trial<maximum;++trial) {
        c.f[0]=ps2::fp::cvt_s_w(c.r[3].w[0]);
        word(c,2,c.r[4].w[0]+4*trial);
        c.f[1]=ps2::ld32(c.r[2].w[0]);
        c.f[0]=ps2::fp::mul(c.f[0],c.f[2]);
        ps2::fpu_div(c,0,c.f[0],c.f[1]); // preserves sticky invalid/divide flags
        const bool below=ps2::fp::key(c.f[12])<ps2::fp::key(c.f[0]);
        ps2::fpu_compare(c,below);c.budget-=12;
        if(below) {finish(c,c.r[5].d[0]);return;}
        word(c,5,trial+1);c.r[2].d[0]=(trial+1)<maximum;c.budget-=4;
        // Admission guarantees nonnegative budget at BOTH original backward
        // polls, including the early-match jump. No scheduler call is elided
        // in any admitted context; unsupported entries execute original code.
    }
    finish(c,c.r[7].d[0]);
}
}
bool profile_matches() {
    std::uint64_t h=14695981039346656037ull;
    for(unsigned a=0x1e4e80;a<0x1e4f10;++a)h=(h^ps2::ld8(a))*1099511628211ull;
    return h==0xd24c603536aba561ull;
}
bool replace(ps2::Cpu &c) {
    if(!enabled)return false;
    const unsigned object=c.r[4].w[0];
    if(c.r[4].d[0]!=object || object<0x500000 || object>0x2000000-sizeof(ObjectReadSpan) ||
       (object&3) || c.r[28].d[0]!=0x3579f0 ||
       c.budget<std::numeric_limits<int>::min()+32 || !profile_matches()) {
        ++counts.fallback;return false;
    }
    const unsigned maximum=ps2::ld8(object+0x20a);
    const bool looping=ps2::fp::key(c.f[12])>=0 && maximum>1;
    if(looping && c.budget<static_cast<int>(16*maximum+16)) {++counts.fallback;return false;}
    search(c,object);++counts.replaced;return true;
}
}
