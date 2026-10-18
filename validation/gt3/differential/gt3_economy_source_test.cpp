// Public source regressions only: no ELF and no claim of independent oracle
// evidence. Original-function differentials are run by run_economy.py separately.
#include "gt3_garage.hpp"
#include "gt3_economy_catalog.hpp"
#include "gt3_economy_state.hpp"
#include "gt3_economy_checks.hpp"
#include "gt3_economy_transactions.hpp"
#include <cassert>
#include <cstring>
#include <utility>
#include <vector>
using U=std::uint32_t;using Q=std::uint64_t;
namespace model=gt3::economy_recovery;
struct Memory:model::garage_boundary,model::catalog_memory,model::post_debit_boundary,model::state_memory {
    std::vector<unsigned char> bytes=std::vector<unsigned char>(0x40000,0);
    std::vector<std::pair<U,U>> writes;
    struct Access {
        char kind;
        U address;
        U bits;
        bool operator==(const Access&) const = default;
    };
    std::vector<Access> accesses;
    std::uint16_t load16(U a)override{assert(a+2<=bytes.size());std::uint16_t x;std::memcpy(&x,bytes.data()+a,2);return x;}
    U load32(U a)override{assert(a+4<=bytes.size());U x;std::memcpy(&x,bytes.data()+a,4);accesses.push_back({'R',a,x});return x;}
    Q load64(U a)override{assert(a+8<=bytes.size());Q x;std::memcpy(&x,bytes.data()+a,8);return x;}
    void store32(U a,U x)override{assert(a+4<=bytes.size());std::memcpy(bytes.data()+a,&x,4);writes.emplace_back(a,x);accesses.push_back({'W',a,x});}
    void store64(U a,Q x)override{assert(a+8<=bytes.size());std::memcpy(bytes.data()+a,&x,8);}
    void put16(U a,std::uint16_t x){assert(a+2<=bytes.size());std::memcpy(bytes.data()+a,&x,2);}
    // Deliberately observable opaque boundary. This is not an implementation of
    // the original reset; composed differential fixtures execute that callee.
    void FUN_00237980(U a)override{writes.emplace_back(a,0xcafe);store32(a+0x218,0xdead);}
    U FUN_001dac48(U a)override{assert(a==0x2d2b00);return 0x7f800001;}
};
// Expected memory accesses come from the original FUN_00218fe0 body and
// FUN_0023c1b8, not just their final RAM values. In particular, +0x30 must be
// read before the incremented count is stored, for both signed branches.
void check_insertion_access_order(U field_30) {
    Memory m;
    constexpr U base=0x1000,record=base+0x138,list=base+0x1b6b8;
    m.store32(record+0x228,1); // Initialized detached record precondition.
    m.store32(base+0x30,field_30);
    m.accesses.clear();
    model::FUN_00218fe0(m,base,record);
    std::vector<Memory::Access> expected={
        {'R',base+0x2c,0}, {'W',record+0x22c,0},
        {'R',base+0x2c,0}, {'W',base+0x2c,1},
        {'R',list,0}, {'W',list+4,record}, {'W',list,record},
        {'R',base+0x38,0}, {'R',base+0x30,field_30},
        {'W',base+0x38,1}
    };
    if ((field_30 & 0x80000000u)==0)
        expected.push_back({'W',base+0x30,field_30+1u});
    assert(m.accesses==expected);
}
int main(){
    for (U field : {0xffffffffu,0x80000000u,0u,0x7fffffffu})
        check_insertion_access_order(field);
    Memory m;constexpr U base=0x1000,pool=base+0x138,list=base+0x1b6b8;
    for(U i=0;i<200;++i){assert(model::FUN_00218f88(m,base)==pool+i*560);m.store32(pool+i*560+0x228,1);}
    assert(model::FUN_00218f88(m,base)==0);
    constexpr U first=pool,second=pool+560,third=pool+1120;
    m.store32(list,0);m.store32(list+4,0);m.writes.clear();
    assert(model::FUN_0023c1b8(m,list,first)==list);
    assert((m.writes==std::vector<std::pair<U,U>>{{list+4,first},{list,first}}));
    m.writes.clear();model::FUN_0023c1b8(m,list,second);
    assert((m.writes==std::vector<std::pair<U,U>>{{first+4,second},{second,first},{list,second}}));
    model::FUN_0023c1b8(m,list,third);assert(model::FUN_0023c4a8(m,list,second)==1);
    m.writes.clear();model::FUN_0023c288(m,list,second);
    assert((m.writes==std::vector<std::pair<U,U>>{{first+4,third},{third,first},{second+4,0},{second,0}}));
    assert(m.load32(list)==third&&m.load32(list+4)==first);
    m.store32(second+0x228,1);m.store32(base+0x2c,0xffffffff);m.store32(base+0x30,0);m.store32(base+0x38,2);
    m.writes.clear();m.accesses.clear();model::FUN_00218fe0(m,base,second);
    assert((m.accesses==std::vector<Memory::Access>{
        {'R',base+0x2c,0xffffffff}, {'W',second+0x22c,0xffffffff},
        {'R',base+0x2c,0xffffffff}, {'W',base+0x2c,0},
        {'R',list,third}, {'W',third+4,second}, {'R',list,third},
        {'W',second,third}, {'W',list,second},
        {'R',base+0x38,2}, {'R',base+0x30,0},
        {'W',base+0x38,3}, {'W',base+0x30,1}
    }));
    assert(m.load32(base+0x2c)==0&&m.load32(second+0x22c)==0xffffffff);
    assert(m.load32(base+0x38)==3&&m.load32(base+0x30)==1);
    assert(m.writes.front()==std::make_pair(second+0x22c,0xffffffffu));
    assert(m.writes.back()==std::make_pair(base+0x30,1u));
    m.store64(second+16,0x123456789abcdef0ULL);m.writes.clear();model::FUN_0023af40(m,second);
    assert((m.writes==std::vector<std::pair<U,U>>{{second+16,0xcafe},{second+0x228,0xdead},{second+0x228,0},{second+0x22c,0xffffffff}}));
    assert(m.load64(second+16)==0x123456789abcdef0ULL);
    assert(model::FUN_00218f88(m,base)==second);
    constexpr U object=0x30000,handle=object+464,root=0x31000,table=0x32000,gp=0x3000+18968;
    m.store32(handle,root);m.store32(root+8,0);m.store32(root+12,0x80000000);
    m.store32(root+16+30*4,0x80000000|(table-root));m.put16(table+8,1);m.put16(table+10,264);
    m.store64(table+16,0x123456789abcdef0ULL);m.store64(object,0x123456789abcdef0ULL);m.store32(table+16+236,14660);
    assert(model::FUN_002315d8(m,handle,30,0)==0);
    m.store32(gp-18968,1);assert(model::FUN_00237bc0(m,object,gp)==14660);
    m.store32(gp-18968,0);assert(model::FUN_00237bc0(m,object,gp)==1466000);
    model::FUN_001d9f60(m,second+0x204);assert(m.load32(second+0x208)==0x7f800001);
    model::FUN_0021a7d8(m,base,~Q{0});model::FUN_0021a740(m,base,1);assert(model::FUN_0021a6d0(m,base)==0);
}
