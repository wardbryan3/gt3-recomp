// Readable decision recovery with explicit EE ABI accounting. No game tables.
#include "gt3_clean_transmission_admission.hpp"
#include "ps2/generated.hpp"
#include <limits>
namespace gt3::transmission_admission {
bool enabled=false;
Counts counts;
namespace {
std::uint64_t fingerprint(unsigned p,unsigned n) {
    std::uint64_t h=14695981039346656037ull;
    for(unsigned i=0;i<n;++i)h=(h^ps2::ld8(p+i))*1099511628211ull;
    return h;
}
struct Execution {
    ps2::Cpu &c;
    void word(unsigned r,unsigned v) {ps2::set32(c.r[r],v);}
    void cost(unsigned n) {c.budget-=n;}
    bool compare(unsigned a,unsigned b,bool eq=false) {
        const bool t=eq ? ps2::fp::key(a)==ps2::fp::key(b) : ps2::fp::key(a)<ps2::fp::key(b);
        ps2::fpu_compare(c,t);return t;
    }
};
void run(Execution &e,unsigned car,unsigned depth) {
    using namespace ps2;
    auto &c=e.c;
    e.word(29,c.r[29].w[0]-48);
    st64(c.r[29].w[0],c.r[16].d[0]);st64(c.r[29].w[0]+32,c.r[31].d[0]);
    e.word(16,car+0xf84);st64(c.r[29].w[0]+16,c.r[17].d[0]);
    c.r[3].d[0]=ld8(car+0x13bb);e.cost(8);e.word(5,car+0x208);
    const unsigned initial=c.r[3].w[0];
    if(initial==0) {
        c.f[1]=ld32(car+0x139c);c.f[0]=0;
        const bool absent=e.compare(c.f[1],0,true);e.cost(6);
        if(!absent) {
            c.f[1]=ld32(car+0x140c);c.f[0]=ld32(c.r[28].w[0]-30060);
            bool negative_route=false;
            bool directional=e.compare(c.f[0],c.f[1]);e.cost(5);
            if(directional) {c.r[2].d[0]=ld8(car+0x13ba);e.cost(3);directional=c.r[2].d[0]!=0;}
            if(!directional) {
                c.f[0]=ld32(c.r[28].w[0]-30056);
                const bool negative=e.compare(c.f[1],c.f[0]);e.cost(5);
                if(negative) {c.r[2].d[0]=ld8(car+0x13ba);e.cost(3);directional=c.r[2].d[0]==0;negative_route=directional;}
            }
            if(directional) {
                c.f[1]=ld32(car+0x1428);
                // Reverse negative-speed route has one extra standalone load.
                if(negative_route)e.cost(1);
                c.r[1].sd[0]=0x3e800000;c.f[0]=c.r[1].w[0];
                const bool admit=e.compare(c.f[0],c.f[1]);e.cost(6);e.word(2,2);
                if(admit) {st8(car+0x13bb,2);e.cost(2);}
            } else {
                c.r[2].d[0]=ld16(car+0x234);
                c.r[3].sd[0]=static_cast<std::int16_t>(ld16(car+0x1414));
                const bool admit=c.r[2].sd[0]<c.r[3].sd[0];c.r[2].d[0]=admit;e.cost(4);e.word(2,2);
                if(admit) {st8(car+0x13bb,2);e.cost(2);}
                else {st32(car+0x139c,0);e.cost(2);}
            }
            c.r[2].d[0]=ld8(car+0x13bb);e.cost(1);
        } else c.r[2].d[0]=ld8(car+0x13bb);
    } else {
        e.word(2,1);e.cost(3);
        if(initial==1) {
            c.f[1]=ld32(car+0x139c);c.f[0]=0;
            const bool absent=e.compare(c.f[1],0,true);e.cost(5);
            if(absent)st8(car+0x13bb,0); // taken branch-likely delay write
            c.r[2].d[0]=ld8(car+0x13bb);e.cost(1);
        } else {c.r[2].d[0]=ld8(car+0x13bb);e.cost(2);}
    }
    e.word(2,c.r[2].w[0]-2);const bool sample=c.r[2].d[0]<2;c.r[2].d[0]=sample;e.cost(4);e.word(2,1);
    if(sample) {
        c.r[3].sd[0]=static_cast<std::int8_t>(ld8(car+0x136d));e.cost(3);c.r[17].d[0]=0;
        if(c.r[3].d[0]!=c.r[2].d[0]) {
            c.r[2].d[0]=ld8(car+0x14b8);e.cost(3);
            if(!c.r[2].d[0])c.r[17].d[0]=ld8(car+0x13e5);
        }
        c.f[0]=ld32(car+0x13cc);e.cost(3);c.r[31].sd[0]=0x1e6e64;
        st32(car+0x1310,c.f[0]);c.pc=0x1e6ca8;dispatch(c,0,depth+1);
        if(c.pc!=0x1e6e64)return;
        c.f[1]=c.f[0];e.word(3,3);e.cost(4);st32(car+0x1314,c.f[1]);
        if(c.r[17].d[0]!=c.r[3].d[0]) {
            e.word(2,6);e.cost(3);
            if(c.r[17].d[0]==c.r[2].d[0]) {
                c.r[31].d[0]=ld64(c.r[29].w[0]+32);
                c.r[17].d[0]=ld64(c.r[29].w[0]+16);e.cost(1);
                c.r[16].d[0]=ld64(c.r[29].w[0]);e.cost(3);e.word(29,c.r[29].w[0]+48);c.pc=c.r[31].w[0];return;
            }
            c.r[2].d[0]=ld8(car+0x13bb);e.cost(3);
            if(c.r[2].d[0]==c.r[3].d[0]) {
                c.f[0]=ld32(car+0x1310);const bool below=e.compare(c.f[1],c.f[0]);e.cost(4);
                if(below) {st32(car+0x1428,0);e.cost(2);}
                else {c.r[1].sd[0]=0x3f800000;c.f[0]=c.r[1].w[0];st32(car+0x1428,c.f[0]);e.cost(3);}
            }
            c.r[17].d[0]=ld64(c.r[29].w[0]+16); // original early restore; common below reads same bytes
            if(ld8(car+0x13bb)==3 && fp::key(c.f[1])>=fp::key(ld32(car+0x1310))) {
                c.r[31].d[0]=ld64(c.r[29].w[0]+32);e.cost(2);
            } else {
                // Non-state3 and below-target paths branch directly to final s0 restore.
                c.r[31].d[0]=ld64(c.r[29].w[0]+32);
            }
            c.r[16].d[0]=ld64(c.r[29].w[0]);e.cost(3);e.word(29,c.r[29].w[0]+48);c.pc=c.r[31].w[0];return;
        }
    }
    c.r[31].d[0]=ld64(c.r[29].w[0]+32);e.cost(1);
    c.r[17].d[0]=ld64(c.r[29].w[0]+16);e.cost(1);
    c.r[16].d[0]=ld64(c.r[29].w[0]);e.cost(3);e.word(29,c.r[29].w[0]+48);c.pc=c.r[31].w[0];
}
}
bool profile_matches() {
    return fingerprint(0x1e6c28,0x2a0)==0x9a457d45da5ffc7cull &&
           fingerprint(0x33c7d0,32)==0x8c800352395cb4d1ull;
}
bool replace(ps2::Cpu &c,unsigned depth) {
    if(!enabled)return false;
    const unsigned car=c.r[4].w[0],sp=c.r[29].w[0];
    const bool valid=car>=0x500000 && car<=0x2000000-0x1500 && !(car&3) &&
        sp>=0x400060 && sp<=0x2000000 && !(sp&15) &&
        c.r[4].d[0]==car && c.r[29].d[0]==sp && c.r[28].d[0]==0x3579f0 &&
        (sp<=car || car+0x1500<=sp-96) && depth<ps2::kMaxDepth-3 &&
        c.budget>=std::numeric_limits<int>::min()+256 && profile_matches();
    if(!valid) {++counts.fallback;return false;}
    Execution e{c};run(e,car,depth);++counts.replaced;return true;
}
}
