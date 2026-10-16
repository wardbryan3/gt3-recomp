// Newly written semantic recovery plus explicit outgoing EE ABI bookkeeping.
// Provenance/boundary: docs/site/docs/transmission-recovery-v1.md. No game tables.
#include "gt3_clean_transmission.hpp"
#include "ps2/generated.hpp"
#include <limits>
namespace gt3::transmission {
bool enabled=false;
Counts counts;
namespace {
std::uint64_t fingerprint(unsigned begin,unsigned end) {
    std::uint64_t h=14695981039346656037ull;
    for(unsigned p=begin;p<end;++p)h=(h^ps2::ld8(p))*1099511628211ull;
    return h;
}
bool overlap(unsigned a,unsigned n,unsigned b,unsigned m) { return a<b+m && b<a+n; }
struct Execution {
    ps2::Cpu &c;
    void word(unsigned r,unsigned value) { ps2::set32(c.r[r],value); }
    void signed_byte(unsigned r,unsigned address) {
        c.r[r].sd[0]=static_cast<std::int8_t>(ps2::ld8(address));
    }
    void cost(unsigned n) { c.budget-=n; }
    void no_change() { word(2,0xffffffffu); }
    void finish() {
        c.r[31].d[0]=ps2::ld64(c.r[29].w[0]);
        cost(3);word(29,c.r[29].w[0]+16);c.pc=c.r[31].w[0];
    }
};
// These scratch writes/costs preserve delay-slot, branch-likely and upper-lane
// effects. The decisions are selection/rearm, not engine engagement decisions.
void select(Execution &e,unsigned car,unsigned requests,unsigned depth) {
    auto &c=e.c;
    e.word(29,c.r[29].w[0]-16);
    e.word(6,car+0xf84);ps2::st64(c.r[29].w[0],c.r[31].d[0]);
    e.word(3,car+16);e.signed_byte(2,requests);e.cost(7);
    const unsigned selected=ps2::ld8(car+0x13ba);c.r[7].d[0]=selected;
    if(c.r[2].d[0]) {
        // Auxiliary request takes priority even while inhibition is nonzero.
        e.no_change();if(selected)c.r[2].d[0]=0;e.cost(3);e.finish();return;
    }
    e.cost(2);
    if(!selected) {
        c.f[1]=ps2::ld32(car+0x13ac);c.f[0]=0;
        const bool zero=ps2::fp::key(c.f[1])==ps2::fp::key(0);
        c.fcr31=(c.fcr31&~ps2::kFpuCondition)|(zero?ps2::kFpuCondition:0);e.cost(6);
        if(!zero) {
            // Preserve the original helper, including all EE FP/scratch/cost.
            e.cost(2);c.r[31].sd[0]=0x1e54a8;c.f[12]=ps2::ld32(car+0x140c);
            c.pc=0x1e4e80;++counts.original_speed_calls;ps2::dispatch(c,0,depth+1);
            // A yielded original callee must resume in generated code, not be
            // mistaken for a returned selection. Guard normally excludes this.
            if(c.pc!=0x1e54a8)return;
            e.word(3,1);if(!c.r[2].d[0])c.r[2].d[0]=1;
            e.cost(3);e.finish();return;
        }
    }
    c.r[2].d[0]=ps2::ld8(car+0x13be);
    const bool inhibited=c.r[2].d[0]!=0;
    e.word(2,c.r[2].w[0]-1);e.cost(2);
    if(inhibited) {
        c.r[3].d[0]=c.r[2].d[0]&255;
        ps2::st8(car+0x13be,c.r[2].w[0]);e.cost(3);
        if(!c.r[3].d[0]) {
            e.signed_byte(2,requests+1);const bool held=c.r[2].d[0]!=0;
            e.word(2,1);e.cost(3);
            if(held) {ps2::st8(car+0x13be,1);e.cost(2);}
        }
        e.no_change();e.cost(1);e.finish();return;
    }
    e.signed_byte(2,requests+1);const bool up=c.r[2].sd[0]>0;
    c.r[5].d[0]=ps2::ld8(requests+1);e.cost(3);
    if(up) {
        c.r[2].d[0]=ps2::ld8(car+0x20a);
        c.r[2].d[0]=selected<c.r[2].d[0];e.word(3,1);e.cost(4);
        if(c.r[2].d[0]) {
            e.word(2,selected+1);ps2::st8(car+0x13be,1);e.cost(3);e.finish();return;
        }
    }
    // Sign is tested from the raw byte's bit7, not from a host char type.
    e.word(2,c.r[5].w[0]<<24);const bool down=c.r[2].sd[0]<0;
    e.no_change();e.cost(3);
    if(down) {
        c.r[2].d[0]=selected<2;e.no_change();e.cost(3);
        if(selected>=2) {
            e.word(3,1);e.word(2,selected-1);ps2::st8(car+0x13be,1);e.cost(4);
        }
    }
    e.finish();
}
}
bool profile_matches() {
    return fingerprint(0x1e5458,0x1e553c)==0xdbf28532431c5391ull &&
           fingerprint(0x1e4e80,0x1e4f10)==0xd24c603536aba561ull;
}
bool replace_manual_selector(ps2::Cpu &c,unsigned depth) {
    if(!enabled)return false;
    const auto car=c.r[4].w[0],requests=c.r[5].w[0],sp=c.r[29].w[0];
    const bool addresses=car>=0x500000 && car<=0x2000000-sizeof(CarPartial) && !(car&3) &&
        requests>=0x400000 && requests<=0x2000000-2 && sp>=0x400010 && sp<=0x2000000 && !(sp&15) &&
        c.r[4].d[0]==car && c.r[5].d[0]==requests && c.r[29].d[0]==sp && c.r[28].d[0]==0x3579f0 &&
        !overlap(sp-16,16,car,sizeof(CarPartial)) && !overlap(sp-16,16,requests,2) &&
        !overlap(sp-16,16,0x100000,0x300000) &&
        (requests==car+0x1304 || !overlap(requests,2,car,sizeof(CarPartial))) &&
        !overlap(requests,2,0x100000,0x300000);
    if(!addresses || c.budget<std::numeric_limits<int>::min()+128 || !profile_matches()) {
        ++counts.fallback;return false;
    }
    const bool speed_path=!ps2::ld8(requests) && !ps2::ld8(car+0x13ba) &&
        ps2::fp::key(ps2::ld32(car+0x13ac))!=ps2::fp::key(0);
    if(speed_path && (depth>=ps2::kMaxDepth || c.budget<static_cast<int>(16*ps2::ld8(car+0x20a)+64))) {
        ++counts.fallback;return false;
    }
    Execution e{c};select(e,car,requests,depth);++counts.replaced;return true;
}
}
