#include "gt3_clean_steering.hpp"
#define main unchanged_trace_main
#include "gt3_steering_trace_test.cpp"
#undef main
#include <cstring>
namespace {
ps2::Cpu run(unsigned entry, unsigned a, unsigned b = 0, unsigned d = 0, unsigned f12 = 0,
             unsigned f13 = 0, unsigned f14 = 0) {
    ps2::Cpu c{};
    c.budget = 1000000;
    c.pc = entry;
    c.r[4].d[0] = a;
    c.r[5].d[0] = b;
    c.r[6].d[0] = d;
    c.r[28].d[0] = 0x3579f0;
    c.r[29].d[0] = stack;
    c.r[31].d[0] = 0x1000000;
    c.f[12] = f12;
    c.f[13] = f13;
    c.f[14] = f14;
    for (unsigned i = 16; i <= 23; ++i)
        c.r[i].d[0] = 0xabc000 + i;
    ps2::call(c, entry, 0);
    if (c.pc != 0x1000000 || c.r[29].w[0] != stack)
        std::abort();
    for (unsigned i = 16; i <= 23; ++i)
        if (c.r[i].d[0] != 0xabc000 + i)
            std::abort();
    return c;
}
unsigned random_word() {
    static unsigned seed = 0x475433;
    seed ^= seed << 13;
    seed ^= seed >> 17;
    seed ^= seed << 5;
    return seed;
}
void compare(unsigned entry, unsigned case_id, const ps2::Cpu &oracle, const ps2::Cpu &replacement,
             const void *expected, const void *actual, unsigned size) {
    if (std::memcmp(expected, actual, size) || oracle.budget != replacement.budget) {
        unsigned off = 0;
        while (off < size &&
               ((const unsigned char *)expected)[off] == ((const unsigned char *)actual)[off])
            ++off;
        std::fprintf(stderr,
                     "FAIL clean entry=%x case=%u diff_offset=%x budget=%lld/%lld bytes=%x/%x\n",
                     entry, case_id, off, (long long)oracle.budget, (long long)replacement.budget,
                     off < size ? ((const unsigned char *)expected)[off] : 0,
                     off < size ? ((const unsigned char *)actual)[off] : 0);
        std::exit(1);
    }
}
} // namespace
int main(int argc, char **argv) {
    if (argc != 2)
        return 2;
    register_generated_code();
    unsigned entry;
    if (!ps2::load_elf(argv[1], entry))
        return 1;
    if (!gt3::clean::profile_matches())
        std::abort();
    ps2::g_options.on_probe = [](ps2::Cpu &, unsigned) {};
    unsigned checked = 0;
    for (unsigned channel : {0u, 1u, 2u, 3u, 0x100u, 0x201u, 0x302u, 4u, 255u, 0xffffu})
        for (int sensitivity : {-2147483647, -100, -1, 0, 1, 20, 35, 60, 65, 100, 2147483647})
            for (unsigned raw = 0; raw < 256; ++raw) {
                gt3::clean::enabled = false;
                const auto original =
                    run(0x210f90, channel, raw | 0xfeed0000, unsigned(sensitivity));
                gt3::clean::enabled = true;
                const auto clean = run(0x210f90, channel, raw | 0xfeed0000, unsigned(sensitivity));
                compare(0x210f90, checked++, original, clean, &original.r[2], &clean.r[2], 8);
            }
    std::printf("Clean mapped normalization exact differential PASS: %u cases\n", checked);
    checked = 0;
    for (unsigned i = 0; i < 16384; ++i) {
        clear(input, 0x150);
        ps2::st32(input + 0xc0, 0x33f7e0);
        ps2::st32(input + 0x14, ((i % 8) << 5) | ((i & 8) ? 8 : 0));
        ps2::st32(input + 0x2c, random_word());
        for (unsigned j = 0; j < 32; ++j)
            ps2::st32(input + 0x38 + j * 4, random_word());
        for (unsigned j = 0; j < 16; ++j)
            ps2::st8(packet + j, random_word());
        std::array<unsigned char, 16> before, expected, actual;
        std::memcpy(before.data(), ps2::g_ram + packet, 16);
        gt3::clean::enabled = false;
        const auto original = run(0x2115f8, input, packet);
        std::memcpy(expected.data(), ps2::g_ram + packet, 16);
        std::memcpy(ps2::g_ram + packet, before.data(), 16);
        gt3::clean::enabled = true;
        const auto clean = run(0x2115f8, input, packet);
        std::memcpy(actual.data(), ps2::g_ram + packet, 16);
        compare(0x2115f8, checked++, original, clean, expected.data(), actual.data(), 16);
    }
    std::printf("Clean wheel command exact differential PASS: %u cases\n", checked);
    const std::array<unsigned, 18> floats = {
        0,          0x80000000, 1,          0x80000001, 0x3c888889, 0xbc888889,
        0x3f000000, 0xbf000000, 0x3f800000, 0xbf800000, 0x41200000, 0xc1200000,
        0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000, 0x7f7fffff, 0xff7fffff};
    checked = 0;
    for (unsigned i = 0; i < 16000; ++i) {
        clear(car, 0x1800);
        ps2::st32(car + 0xec0, floats[random_word() % floats.size()]);
        ps2::st32(car + 0x13a0, floats[random_word() % floats.size()]);
        ps2::st32(car + 0x13a8, floats[random_word() % floats.size()]);
        const unsigned target = floats[random_word() % floats.size()],
                       out = floats[random_word() % floats.size()],
                       ret = floats[random_word() % floats.size()];
        std::array<unsigned char, 0x1800> before, expected;
        std::memcpy(before.data(), ps2::g_ram + car, before.size());
        gt3::clean::enabled = false;
        const auto original = run(0x1e4368, car, 0, 0, target, out, ret);
        std::memcpy(expected.data(), ps2::g_ram + car, expected.size());
        std::memcpy(ps2::g_ram + car, before.data(), before.size());
        gt3::clean::enabled = true;
        const auto clean = run(0x1e4368, car, 0, 0, target, out, ret);
        compare(0x1e4368, checked++, original, clean, expected.data(), ps2::g_ram + car,
                expected.size());
    }
    std::printf("Clean stick filter exact differential PASS: %u cases\n", checked);
    checked = 0;
    for (unsigned i = 0; i < 20000; ++i) {
        clear(car, 0x1800);
        clear(race, 0xb800);
        clear(packet, 16);
        ps2::st32(car + 4, race);
        ps2::st8(race + 0xb7ad, i % 3);
        constexpr int policies[] = {-128, -1, 0, 1, 2, 3, 4, 5, 127};
        ps2::st8(car + 0x136f, policies[(i / 256) % 9]);
        ps2::st8(car + 0x1307, random_word() % 4);
        for (unsigned curve = 0; curve < 3; ++curve) {
            unsigned descriptor = car + 0x6c + curve * 0x3c, data = knots + curve * 16;
            ps2::st16(descriptor, 2);
            ps2::st32(descriptor + 4, data);
            ps2::st32(descriptor + 8, data + 8);
            store_float(data, 0);
            store_float(data + 4, 100);
            store_float(data + 8, .1f * (curve + 1));
            store_float(data + 12, .1f * (curve + 1));
        }
        for (unsigned off :
             {0x68u, 0xec0u, 0x105cu, 0x1100u, 0x13a0u, 0x13a8u, 0x1420u, 0x142cu, 0x1430u})
            ps2::st32(car + off, floats[random_word() % floats.size()]);
        ps2::st16(car + 0x16a4, random_word());
        ps2::st16(car + 0x16a6, random_word());
        ps2::st8(packet, random_word() & 1);
        ps2::st8(packet + 1, i % 256);
        ps2::st16(packet + 4, random_word());
        std::array<unsigned char, 0x1800> before, expected;
        std::memcpy(before.data(), ps2::g_ram + car, before.size());
        gt3::clean::enabled = false;
        const auto original = run(0x1e4478, car, packet, car + 0x1304);
        std::memcpy(expected.data(), ps2::g_ram + car, expected.size());
        std::memcpy(ps2::g_ram + car, before.data(), before.size());
        gt3::clean::enabled = true;
        const auto clean = run(0x1e4478, car, packet, car + 0x1304);
        compare(0x1e4478, checked++, original, clean, expected.data(), ps2::g_ram + car,
                expected.size());
    }
    std::printf("Clean steering envelope/full original tail exact differential PASS: %u cases\n",
                checked);
    gt3::clean::enabled = true;
    wheel_commands();
    wheel_driving();
    return 0;
}
