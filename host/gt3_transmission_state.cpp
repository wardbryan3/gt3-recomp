#include "gt3_transmission_state.hpp"
#include "ps2/fpu.hpp"
#include <limits>

namespace gt3::transmission_state {
namespace {
bool less(Bits a, Bits b) { return ps2::fp::key(a) < ps2::fp::key(b); }
bool less_equal(Bits a, Bits b) { return ps2::fp::key(a) <= ps2::fp::key(b); }
bool equal(Bits a, Bits b) { return ps2::fp::key(a) == ps2::fp::key(b); }
}
unsigned effective_policy(std::int8_t owner, std::uint8_t mode, std::uint8_t policy) {
    return owner == 1 || mode != 0 ? 0 : policy;
}
AdmissionResult admit(const Admission &a) {
    AdmissionResult r{a.state, a.candidate, Cause::unchanged, false};
    if (a.state == 1 && equal(a.candidate, 0)) {
        r.state = 0;
        r.cause = Cause::candidate_zero;
    } else if (a.state == 0 && !equal(a.candidate, 0)) {
        const bool moving_in_selected_direction =
            (less(a.positive_speed_threshold, a.speed) && a.selected != 0) ||
            (less(a.speed, a.negative_speed_threshold) && a.selected == 0);
        if (moving_in_selected_direction) {
            if (less(0x3e800000, a.effective_accelerator)) {
                r.state = 2;
                r.cause = Cause::accelerator_admission;
            }
        } else if (static_cast<int>(a.admission_rpm) < static_cast<int>(a.sampled_rpm)) {
            r.state = 2;
            r.cause = Cause::rpm_admission;
        } else {
            r.candidate = 0;
            r.cause = Cause::rpm_rejection;
        }
    }
    r.sample_rates = r.state == 2 || r.state == 3;
    return r;
}
Bits prepared_accelerator(std::uint8_t state, unsigned policy, Bits engine,
                          Bits target, Bits prior) {
    if (state != 3 || policy == 3 || policy == 6) return prior;
    return less(target, engine) ? 0 : 0x3f800000;
}
SelectionResult select(std::uint8_t state, std::uint8_t selected, std::uint64_t result) {
    SelectionResult r{state, selected, false, Cause::selection_rejected};
    if (result == std::numeric_limits<std::uint64_t>::max()) return r;
    r.commit = true;
    r.selected = static_cast<std::uint8_t>(result);
    if (state == 0) r.cause = Cause::selection_while_free;
    else if (result == 0 || selected == 0) {
        r.state = 2;
        r.cause = Cause::reverse_selection;
    } else {
        r.state = 3;
        r.cause = Cause::forward_selection;
    }
    return r;
}
SynchronizationResult synchronize(const Synchronization &a) {
    SynchronizationResult r{a.state, a.inhibition, a.engine, false, Cause::unchanged};
    if (a.state == 1) {
        r.engine = a.current_target;
        return r;
    }
    if (a.state != 2 && a.state != 3) return r;
    // This is an alternative to crossing, not an extra condition on it. A
    // non-exact-one candidate under policy 3/6 still takes ordinary crossing.
    if ((a.policy == 3 || a.policy == 6) && equal(a.candidate, 0x3f800000)) {
        r.state = 1;
        r.rewrite_axle_and_wheel_rates = true;
        r.cause = Cause::exact_one_policy;
        return r; // no write of 12, no ordinary crossing or subsequent abort
    }
    const bool crossed =
        (less_equal(a.saved_engine, a.saved_target) && less_equal(a.current_target, a.engine)) ||
        (less_equal(a.saved_target, a.saved_engine) && less_equal(a.engine, a.current_target));
    if (crossed) {
        r.state = 1;
        r.engine = a.current_target;
        r.inhibition = 12;
        r.cause = Cause::ordinary_crossing;
    } else if (a.state == 3 && less_equal(a.saved_target, a.idle_rate)) {
        r.state = 0;
        r.cause = Cause::low_target_abort;
    } else if (a.state == 2 && less(0x3f400000, a.brake) &&
               (less(a.engine, a.idle_plus_500_rate) ||
                (less(a.speed, a.low_speed_upper) && less(a.low_speed_lower, a.speed)))) {
        r.state = 0;
        r.cause = Cause::brake_abort;
    }
    return r;
}
Bits clamp_nonzero_engine(Bits engine, Bits upper) {
    if (less(engine, 0)) return 0; // original early branch, not std::clamp
    return less_equal(upper, engine) ? upper : engine;
}
Bits integrate_free_engine(Bits engine, Bits effort, Bits coefficient, Bits dt, Bits idle) {
    const Bits next = ps2::fp::add(engine, ps2::fp::mul(ps2::fp::mul(effort, coefficient), dt));
    return less(next, idle) ? idle : next;
}
DriveRoute drive_route(std::uint8_t state) {
    if (state == 0) return DriveRoute::bypass;
    if (state == 1) return DriveRoute::ordinary_effort;
    if (state == 3) return DriveRoute::calibrated_transfer;
    return DriveRoute::synchronization; // invalid bytes follow original "other" path
}
}
