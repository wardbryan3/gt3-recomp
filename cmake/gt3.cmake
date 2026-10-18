# Explicit, single source ownership. No gameplay library below is installed into
# ps2run or gt3-native by this restructuring.
set(GT3_CONTROLS "${CMAKE_SOURCE_DIR}/src/gt3/gameplay/controls")
set(GT3_TRANSMISSION "${CMAKE_SOURCE_DIR}/src/gt3/gameplay/transmission")
set(GT3_ECONOMY "${CMAKE_SOURCE_DIR}/src/gt3/gameplay/economy")
# Memory-native recovery only. No product or PS2 runtime binding is installed.
add_library(gt3_economy_recovered STATIC
    ${GT3_ECONOMY}/gt3_garage.cpp
    ${GT3_ECONOMY}/gt3_garage_list.cpp
    ${GT3_ECONOMY}/gt3_economy_catalog.cpp)
target_include_directories(gt3_economy_recovered PUBLIC ${GT3_ECONOMY})
add_library(gt3_controls_recovered STATIC
    ${GT3_CONTROLS}/gt3_clean_steering.cpp
    ${GT3_CONTROLS}/gt3_clean_pedals.cpp
    ${GT3_CONTROLS}/gt3_clean_handbrake.cpp)
target_include_directories(gt3_controls_recovered PUBLIC ${GT3_CONTROLS})
target_link_libraries(gt3_controls_recovered PUBLIC ps2runtime)
add_library(gt3_transmission_recovered STATIC
    ${GT3_TRANSMISSION}/gt3_clean_transmission.cpp
    ${GT3_TRANSMISSION}/gt3_clean_transmission_speed.cpp
    ${GT3_TRANSMISSION}/gt3_clean_transmission_admission.cpp
    ${GT3_TRANSMISSION}/gt3_transmission_state.cpp)
target_include_directories(gt3_transmission_recovered PUBLIC ${GT3_TRANSMISSION})
target_link_libraries(gt3_transmission_recovered PUBLIC ps2runtime)
add_library(gt3_control_adapters STATIC
    ${GT3_CONTROLS}/gt3_synthetic_wheel.cpp
    ${GT3_CONTROLS}/gt3_virtual_pedals.cpp
    ${GT3_CONTROLS}/gt3_virtual_handbrake.cpp)
target_include_directories(gt3_control_adapters PUBLIC ${GT3_CONTROLS})
target_link_libraries(gt3_control_adapters PUBLIC ps2runtime)
add_library(gt3_virtual_transmission_policy STATIC
    ${GT3_TRANSMISSION}/virtual/controller.cpp)
target_include_directories(gt3_virtual_transmission_policy PUBLIC ${CMAKE_SOURCE_DIR})
# Binding syntax is checked separately, gates OFF. It is never a product dependency.
add_library(gt3_virtual_transmission_binding OBJECT
    ${CMAKE_SOURCE_DIR}/src/gt3/bindings/ps2/virtual-transmission/virtual_transmission.cpp)
target_include_directories(gt3_virtual_transmission_binding PRIVATE ${CMAKE_SOURCE_DIR})
target_link_libraries(gt3_virtual_transmission_binding PRIVATE ps2runtime)
target_compile_definitions(gt3_virtual_transmission_binding PRIVATE GT3_EXT_VIRTUAL_TRANSMISSION=0)

if(BUILD_TESTING)
    # Validation-only compilation of both existing gate states; neither object
    # target is linked into a product. This is NOT enabled live proof.
    add_library(gt3_virtual_transmission_binding_on OBJECT
        ${CMAKE_SOURCE_DIR}/src/gt3/bindings/ps2/virtual-transmission/virtual_transmission.cpp)
    target_include_directories(gt3_virtual_transmission_binding_on PRIVATE ${CMAKE_SOURCE_DIR})
    target_link_libraries(gt3_virtual_transmission_binding_on PRIVATE ps2runtime)
    target_compile_definitions(gt3_virtual_transmission_binding_on PRIVATE GT3_EXT_VIRTUAL_TRANSMISSION=1)
    function(gt3_source_test name source)
        add_executable(${name} ${source})
        target_link_libraries(${name} PRIVATE ${ARGN})
        # The tests use assert as a failure condition; keep it active in Release.
        target_compile_options(${name} PRIVATE -UNDEBUG)
        add_test(NAME ${name} COMMAND ${name})
    endfunction()
    gt3_source_test(gt3_economy_source_test ${CMAKE_SOURCE_DIR}/validation/gt3/differential/gt3_economy_source_test.cpp gt3_economy_recovered)
    add_library(gt3_fixture_clock SHARED ${CMAKE_SOURCE_DIR}/validation/gt3/live/gt3_baseline_clock.cpp)
    set_target_properties(gt3_fixture_clock PROPERTIES PREFIX "" OUTPUT_NAME "fixed-clock")
    gt3_source_test(gt3_state_layout ${CMAKE_SOURCE_DIR}/validation/gt3/live/gt3_baseline_layout.cpp ps2runtime)
    gt3_source_test(gt3_recovered_source_test ${GT3_CONTROLS}/tests/gt3_recovered_source_test.cpp gt3_controls_recovered gt3_control_adapters)
    gt3_source_test(gt3_handbrake_source_test ${GT3_CONTROLS}/tests/gt3_handbrake_source_test.cpp gt3_controls_recovered)
    gt3_source_test(gt3_virtual_pedals_test ${GT3_CONTROLS}/tests/gt3_virtual_pedals_test.cpp gt3_control_adapters)
    gt3_source_test(gt3_virtual_handbrake_test ${GT3_CONTROLS}/tests/gt3_virtual_handbrake_test.cpp gt3_control_adapters)
    gt3_source_test(gt3_transmission_source_test ${GT3_TRANSMISSION}/tests/gt3_transmission_source_test.cpp gt3_transmission_recovered)
    gt3_source_test(gt3_transmission_speed_source_test ${GT3_TRANSMISSION}/tests/gt3_transmission_speed_source_test.cpp gt3_transmission_recovered)
    gt3_source_test(gt3_transmission_state_source_test ${GT3_TRANSMISSION}/tests/gt3_transmission_state_source_test.cpp gt3_transmission_recovered)
    gt3_source_test(gt3_virtual_controller_test ${GT3_TRANSMISSION}/tests/virtual-controller_test.cpp gt3_virtual_transmission_policy)
endif()
