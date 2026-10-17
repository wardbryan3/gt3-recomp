// Read-only validation of the existing host serialization ABI. This is not a
// save-state loader/writer or a format change. Include the authoritative host
// type rather than guessing a wire layout or copying a game structure.
#include "../../../runtime/src/kernel.cpp"
#include <cstddef>
#include <cstdio>
int main() {
    using ps2::kernel::Thread;
    static_assert(offsetof(Thread, wait_id) == 56);
    static_assert(offsetof(Thread, order) == 64);
    static_assert(offsetof(Thread, context) == 80);
    static_assert(sizeof(Thread) == 768);
    static_assert(sizeof(Thread::wait_id) == 4 && sizeof(Thread::order) == 8);
    std::puts("{\"thread_size\":768,\"padding\":[[60,64],[72,80]]}");
}
