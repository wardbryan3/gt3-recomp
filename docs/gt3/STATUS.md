# Status and evidence boundaries

## Private experiment observations (before the public-tree rebase)

- GT3 USA v1.10 menus/races and scoped projection/camera changes exercised.
- 20,480 actual translated-routine versus reference input cases passed.
- 9×3 GPU sample addressing and isotropic/anisotropic state conversion passed.
- Hardware regressions, camera comparisons and same-frame save/reload captures
  passed. Full-size compositor captures were identical across execution paths.
- Parallel execution produced approximately 60 requests/sec in three repeatable
  scenes; virtual presentation still had occasional 33 ms gaps.
- A user tested center-cropped 1920×1080 WebRTC delivery and reported about 60
  decoded FPS. That includes streaming and is not physical-scanout validation.
- The stream initially swapped RGBA/BGRA channels; that was an added streaming
  bug, not a GS renderer defect, and was corrected in the private stream.

No private frames, recordings, game binaries, generated units or snapshots are
included as public evidence artifacts.

## This clean source tree

Started from upstream a02cdd56a8ab5077724da2b5ff8ca683024d7cf4 and selectively
rebased source/tests. The newer upstream interrupt-latch implementation was kept;
state version is bumped for the additional i.Link state. Experiment measurements
are not automatically measurements of this newly rebased code.

Publication guard, script syntax and synthetic patch tests are preparation checks.
CI is configured for synthetic software-runtime regressions. Fresh-clone native
boot/discovery, local GPU tests, browser/GT4 regression coverage and portable build
coverage must be established before a release. No release binaries are provided.

## Known limits / follow-up

- Not complete game-source recovery; only a narrow readable control reference.
- Supported triple-profile fingerprint is specific to the tested USA revision.
- Overlay/replay issues and full game-mode coverage remain.
- i.Link initialization emulation does not implement network play.
- Native VU remains a detached worker; fully orderly joinable teardown is pending.
- Triple rendering, pacing and snapshot changes need broader upstream-style tests.
- SSE4.1 is optional, native x86-only, with no runtime dispatch.
- Physical scanout, hardware audio timing and all-adapter performance are unproven.

Priority upstream candidates remain SIF scratchpad reads and the final-thread
idle transition, each with a focused synthetic regression.
