// Original implementation of verified EE semantics, not a decompiler dump.
// Provenance and join contract: docs/site/docs/handbrake-v1.md.
#include "gt3_clean_handbrake.hpp"
#include "ps2/generated.hpp"
#include <limits>
namespace gt3::handbrake {
bool enabled=false;
Counts counts;
Result process(std::uint8_t flags,std::int16_t input,Bits previous,Calibration k) {
    namespace fp=ps2::fp;
    constexpr Bits one=0x3f800000, q12=0x39800000;
    Result r{};
    if(flags&0x10) {
        // 001E4C1C: signed conversion, exact 2^-12 scale; no saturation.
        r.v0=static_cast<std::uint32_t>(static_cast<std::int32_t>(input));
        r.f0=fp::cvt_s_w(r.v0);r.f1=0;r.f2=fp::mul(r.f0,q12);
        r.condition=fp::key(r.f2)==fp::key(0);
        r.at=q12;r.writes_at=true;r.cost=14;
        if(!r.condition) {
            // 001E4C44: zero alone bypasses floor; negative and >1 survive.
            r.at=one;r.f0=fp::sub(one,r.f2);r.f1=fp::mul(k.floor,r.f0);
            r.f2=fp::add(r.f2,r.f1);r.cost+=7;
        }
        r.value=r.f2;
    } else {
        // 001E4BC8: magnitude/sign ignored. The previous output IS history.
        const bool pressed=input!=0;
        r.v0=0x2d0000;r.f1=pressed?k.rise:k.fall;r.f2=pressed?one:0;
        r.f0=pressed?fp::add(previous,r.f1):fp::sub(previous,r.f1);
        r.condition=pressed?fp::key(one)<fp::key(r.f0):fp::key(r.f0)<fp::key(0);
        r.cost=pressed?15:16;
        r.writes_at=pressed;r.at=one;
        // 001E4BEC writes the unclamped value first, then an optional endpoint.
        r.value=r.condition?r.f2:r.f0;if(r.condition)r.cost+=2;
    }
    return r;
}
namespace {
std::uint64_t fingerprint(unsigned start,unsigned end) {
    std::uint64_t h=14695981039346656037ull;
    for(unsigned p=start;p<end;++p)h=(h^ps2::ld8(p))*1099511628211ull;
    return h;
}
}
bool profile_matches() {
    return fingerprint(0x1e4bb8,0x1e4c60)==0xcdb8e58e1936e8acull;
}
bool replace(ps2::Cpu &c,unsigned depth) {
    if(!enabled)return false;
    if(depth>=ps2::kMaxDepth)++counts.depth_boundary;
    const auto car=c.r[23].w[0],command=c.r[18].w[0];
    // Only one aligned high-RAM output word; no retained pointer/call/stack write.
    // Full-width identities exclude wraparound aliases. Calibration stays dynamic.
    // Depth limits generated CALL recursion, not this call-free interior seam.
    if(c.budget<std::numeric_limits<int>::min()+32 || car<0x500000 ||
       car>0x2000000-sizeof(CarPartial) || (car&3) || c.r[23].d[0]!=car ||
       c.r[16].d[0]!=car+0xf84 || c.r[18].d[0]!=command || (command&1) ||
       command<0x400000 || command>0x2000000-sizeof(CommandPartial) ||
       (command<car+sizeof(CarPartial) && car<command+sizeof(CommandPartial)) ||
       c.r[28].d[0]!=0x3579f0 || !profile_matches()) {
        ++counts.fallback;return false;
    }
    // Only digital release has a generated backward-branch preemption check
    // (001E4C14, after 14 instructions). Leave that scheduling path original.
    if(!(ps2::ld8(command)&16) && !ps2::ld16(command+14) && c.budget<14) {
        ++counts.fallback;return false;
    }
    const auto r=process(ps2::ld8(command),static_cast<std::int16_t>(ps2::ld16(command+14)),
                         ps2::ld32(car+0x13b4),
                         {ps2::ld32(0x2d4940),ps2::ld32(0x2d4944),ps2::ld32(0x352990)});
    c.r[2].sd[0]=static_cast<std::int32_t>(r.v0);
    if(r.writes_at)c.r[1].sd[0]=static_cast<std::int32_t>(r.at);
    c.f[0]=r.f0;c.f[1]=r.f1;c.f[2]=r.f2;
    c.fcr31=(c.fcr31&~ps2::kFpuCondition)|(r.condition?ps2::kFpuCondition:0);
    ps2::st32(car+0x13b4,r.value);c.budget-=r.cost;c.pc=0x1e4c60;
    ++counts.replaced;return true;
}
} // namespace gt3::handbrake
