#include "hw.hpp"
#include "kernel.hpp"
#include "ps2/system.hpp"
#include "ps2/generated.hpp"
#include "iop/hw.hpp"
#include "iop/iop.hpp"
#include "iop/sif.hpp"
#include "ps2/memory.hpp"
#include <cstdio>
#include <cstdlib>

void require(bool ok, const char *message) {
    if (!ok) { std::fprintf(stderr, "FAIL: %s\n", message); std::exit(1); }
}
int main() {
    using namespace ps2;
    hw::reset();
    hw::intc_set_mask(2, true);
    hw::intc_raise(2);
    require(hw::intc_pending() == 4, "vblank interrupt pending");
    hw::intc_ack(2);
    require(hw::intc_pending() == 0, "delivered interrupt is not repeatedly dispatched");
    require((hw::read32(0x1000F000) & 4) != 0, "hardware status remains visible to polling after HLE delivery");
    hw::write32(0x1000F000, 4);
    require((hw::read32(0x1000F000) & 4) == 0, "guest clears interrupt status by writing one");
    hw::intc_raise(2);
    require(hw::intc_pending() == 4, "next vblank is deliverable");
    iop::hw::reset();
    iop::hw::write(0x1F808410, 2, 4);
    require((iop::hw::read(0x1F808410, 4) & 8) != 0, "i.Link serial clock ready");
    iop::hw::write(0x1F808414, 0x400004A5, 4);
    require((iop::hw::read(0x1F808414, 4) & 0x40000000) == 0, "PHY write completes");
    iop::hw::write(0x1F808424, 0x40000000, 4);
    iop::hw::set_interrupt_mask(24, true);
    iop::hw::write(0x1F808414, 0x84000000, 4);
    require((iop::hw::read(0x1F808414, 4) & 0x8000FFFF) == 0x04A5, "PHY read returns register and completes");
    require(iop::hw::next_pending_interrupt() == 24, "PHY read delivers enabled i.Link interrupt");
    iop::hw::write(0x1F808420, 0x40000000, 4);
    require(iop::hw::read(0x1F808420, 4) == 0, "i.Link status is write-one-to-clear");
    // Deliberately conflicting descriptors at RAM and scratchpad addresses.
    // Reading scratchpad as a RAM alias would copy the wrong payload.
    st32(0x70001000, 0x2000);
    st32(0x70001004, 0x180000);
    st32(0x70001008, 16);
    st32(0x7000100C, 0);
    st32(0x1000, 0x2100);
    st32(0x1004, 0x180000);
    st32(0x1008, 16);
    st32(0x100C, 0);
    for (unsigned i = 0; i < 16; ++i) {
        st8(0x2000 + i, static_cast<unsigned char>(0xA0 + i));
        st8(0x2100 + i, 0x55);
    }
    sif::set_dma(0x70001000, 1);
    for (unsigned i = 0; i < 16; ++i)
        require(iop::read8(0x180000 + i) == 0xA0 + i, "SIF descriptor is read from EE scratchpad, not a RAM alias");
    kernel::reset();
    kernel::start_main_thread(0x100000, 0, 0, 0);
    g_cpu.pc = 0x100004;
    g_cpu.r[3].w[0] = 0x24; // ExitDeleteThread: remove the only runnable thread.
    kernel::handle_syscall(g_cpu, 0x100000);
    require(kernel::current_thread() == 0, "last thread was deleted");
    require((g_cpu.pc & ~kUnwind) == kIdle, "deleting the last runnable thread enters idle, not deleted guest code");
    std::puts("GT3 hardware regressions PASS");
}
