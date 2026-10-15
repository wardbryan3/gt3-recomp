// Validation only. Read the authoritative host type; no format/runtime changes.
#include "../runtime/src/kernel.cpp"
#include <cstddef>
#include <cstdio>
int main() {
    using ps2::kernel::Thread;
    static_assert(sizeof(Thread)==768 && offsetof(Thread,id)==0);
    static_assert(offsetof(Thread,status)==4 && offsetof(Thread,stack)==20);
    static_assert(offsetof(Thread,stack_size)==24 && ps2::kernel::kRun==1);
    std::puts("{\"thread_size\":768,\"id\":0,\"status\":4,\"stack\":20,\"stack_size\":24,\"running\":1}");
}
