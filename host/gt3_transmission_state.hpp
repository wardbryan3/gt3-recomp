#pragma once
#include <cstdint>

// Original USA v1.10 decision model, NOT a Cpu entry replacement. EE quantities
// are bits, not host floats. See transmission-state-v1.md for external boundaries.
namespace gt3::transmission_state {
using Bits = std::uint32_t;
enum class Cause {
    unchanged, candidate_zero, accelerator_admission, rpm_admission,
    rpm_rejection, ordinary_crossing, exact_one_policy, low_target_abort,
    brake_abort, selection_rejected, selection_while_free, reverse_selection,
    forward_selection
};
struct Admission {
    std::uint8_t state, selected;
    Bits candidate, speed, effective_accelerator;
    std::int16_t sampled_rpm;
    std::uint16_t admission_rpm;
    Bits positive_speed_threshold, negative_speed_threshold;
};
struct AdmissionResult {
    std::uint8_t state;
    Bits candidate;
    Cause cause;
    bool sample_rates; // when true: save engine and independently derived target
};
AdmissionResult admit(const Admission &);
// Ordinary state 3 preparation; policies 3/6 deliberately retain accelerator.
Bits prepared_accelerator(std::uint8_t state, unsigned effective_policy,
                          Bits saved_engine, Bits target, Bits prior);
unsigned effective_policy(std::int8_t owner, std::uint8_t control_mode,
                          std::uint8_t stored_policy);
struct SelectionResult {
    std::uint8_t state, selected;
    bool commit;
    Cause cause;
};
// The dispatcher result is the full low 64-bit EE register, not a narrowed byte.
SelectionResult select(std::uint8_t state, std::uint8_t selected,
                       std::uint64_t dispatcher_result);
struct Synchronization {
    std::uint8_t state, inhibition;
    unsigned policy;
    Bits candidate, saved_engine, saved_target, engine, current_target;
    Bits brake, speed, idle_rate, idle_plus_500_rate;
    Bits low_speed_upper, low_speed_lower;
};
struct SynchronizationResult {
    std::uint8_t state, inhibition;
    Bits engine;
    bool rewrite_axle_and_wheel_rates;
    Cause cause;
};
// Nonzero-state decision phase at 001E7590, before common rate clamp/RPM update.
// Special policy rate writes, common clamp, and free integration are separate.
SynchronizationResult synchronize(const Synchronization &);
Bits clamp_nonzero_engine(Bits engine, Bits upper_rate);
// State 0 rate integration at 001E755C, after original effort helper.
Bits integrate_free_engine(Bits engine, Bits effort, Bits coefficient,
                           Bits timestep, Bits idle_rate);
// Target derivation and engine effort are external original dependencies.
// This enum describes drive routing, not a newly implemented torque model.
enum class DriveRoute { bypass, ordinary_effort, synchronization, calibrated_transfer };
DriveRoute drive_route(std::uint8_t state);
}
