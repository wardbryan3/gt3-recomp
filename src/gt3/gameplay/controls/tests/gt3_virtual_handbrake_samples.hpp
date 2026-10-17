#pragma once
// Independent expected integer codes; no call to the implementation under test.
#include <cmath>
#include <cstdint>
#include <vector>
namespace virtual_handbrake_samples {
struct Sample {double value;unsigned q;};
inline std::vector<Sample> all() {
    std::vector<Sample> samples;
    for(unsigned q=0;q<=4096;++q)samples.push_back({q/4096.0,q});
    for(unsigned q=0;q<4096;++q) {
        const double tie=(2*q+1)/8192.0;
        samples.push_back({std::nextafter(tie,0.0),q});
        samples.push_back({tie,q+1});
        samples.push_back({std::nextafter(tie,1.0),q+1});
    }
    std::uint64_t seed=0x418ecafb2219ull;
    for(unsigned i=0;i<8192;++i) {
        seed=seed*6364136223846793005ull+1442695040888963407ull;
        const std::uint32_t n=seed>>32;
        samples.push_back({n/4294967296.0,unsigned((std::uint64_t(n)+524288)>>20)});
    }
    for(const auto sample:std::vector<Sample>{{.1,410},{.9,3686},{.01,41},{.99,4055},{1.0/3.0,1365},{std::nextafter(0.0,1.0),0},{std::nextafter(1.0,0.0),4096},{-0.0,0}})samples.push_back(sample);
    return samples;
}
}
