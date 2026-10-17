// Process-local validation clock input, NOT linked into ps2run or its runtime.
// The original CD/DVD clock reads host time(). Pin only that external input;
// monotonic scheduling/render clocks and all guest logic remain unchanged.
#include <cerrno>
#include <cstdlib>
#include <ctime>

extern "C" std::time_t time(std::time_t *destination) noexcept {
    const char *text = std::getenv("GT3_BASELINE_UTC_EPOCH");
    if (!text || !*text) std::_Exit(2);
    char *end = nullptr;
    errno = 0;
    const auto epoch = std::strtoll(text, &end, 10);
    if (errno || *end || epoch <= 0) std::_Exit(2);
    const auto value = static_cast<std::time_t>(epoch);
    if (destination) *destination = value;
    return value;
}
