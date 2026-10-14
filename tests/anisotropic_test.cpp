#include "gs/gpu/gpu.hpp"
#include <cstdio>
#include <cstdlib>
void require(bool ok, const char *what) { if (!ok) { std::fprintf(stderr,"FAIL: %s\n",what); std::exit(1); } }
int main() {
    using namespace ps2::gs;
    setenv("PS2_SCALE","9",1); setenv("PS2_SCALE_Y","3",1);
    require(gpu::init(gpu::Mode::primary),"GPU init");
    std::vector<std::uint32_t> vram((kMemorySize/4)*27), clut;
    for (unsigned k=0;k<27;++k) vram[k]=k*0x010305u;
    gpu::write_state(vram,(9u<<16)|3u,clut);
    std::vector<std::uint32_t> rgba; unsigned width=0,height=0;
    gpu::DisplaySource source{0,1,0,0,0,1,1,false};
    require(gpu::display(source,rgba,width,height),"display");
    require(width==9 && height==3 && rgba.size()==27,"independent dimensions");
    for (unsigned k=0;k<27;++k) require(rgba[k]==(0xff000000u|vram[k]),"independent x/y sample addressing");
    unsigned scale=0; gpu::read_state(vram,scale,clut);
    require(scale==((9u<<16)|3u) && vram.size()==(kMemorySize/4)*27,"anisotropic state round-trip");
    vram.assign((kMemorySize/4)*9,0);
    for(unsigned k=0;k<9;++k) vram[k]=k*0x010305u;
    gpu::write_state(vram,3,clut);
    require(gpu::display(source,rgba,width,height),"old isotropic state conversion");
    for(unsigned y=0;y<3;++y) for(unsigned x=0;x<9;++x)
        require(rgba[y*9+x]==(0xff000000u|vram[y*3+x/3]),"sample conversion preserves both axes");
    std::puts("Anisotropic GPU samples and state conversion PASS");
}
