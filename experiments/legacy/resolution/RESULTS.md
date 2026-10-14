> Historical experiment record. Not current-main validation; referenced artifacts remain private and services may no longer be running.

# GT3: 5760 × 1080 native rendering experiment

October 13, 2026. The resolution work is isolated at `$GT3_LEGACY_ROOT/resolution`. The previously validated build and its launcher remain preserved. No production service, desktop mode, streaming configuration, system package, ISO, or existing save was changed.

## Actual result

The native renderer produces **5760 × 1080 captures with a wider camera view**, rather than stretching the original 4:3 view. At the default setting it rasterizes **5760 × 1344** internally using separate **9× horizontal / 3× vertical samples**, then reduces the vertical dimension to 1080. A matching original-camera capture has a 1440 × 1080 viewport centered within the same output dimensions; the widened capture uses the full width and reveals additional track geometry.

A fresh boot progressed through proportional menus, selected a car, and reached a race. Super Speedway, Trial Mountain, and Midfield Raceway also reached racing through independent scene checks. Bumper, chase, look-behind, and an automatic replay angle were captured at the target output size. These are short scene checks, not comprehensive coverage of all cameras, tracks, effects, or a repeat of the previous 30-minute stability run.

## Presentation limit

The renderer and captures reach the target resolution. **Full-size desktop presentation is not yet verified.** A real native Wayland window requested 5760 × 1080, but the existing compositor supplied **1129 × 577**. The application presented through WebGPU and completed its window test. No display or streaming service was reconfigured to bypass that limit. A desktop session supporting the target dimensions is still needed for full-size triple-screen presentation. Monitor angles, bezel compensation, and separate per-monitor projections were not implemented.

## Camera and controls

The tested native game cycles between its forward bumper view and external chase view with **R1**. **L1**, held, looks behind. The forward view has no visible cockpit interior. It is the closest tested view to an in-car preference; no new cockpit assets were created.

Keyboard: **W** switches camera; **Q** looks behind; **Z** accelerates; **A** brakes; arrows steer; Enter pauses/starts. SDL controller right and left shoulder buttons map to R1 and L1 respectively. Physical controller operation remains untested. Trigger bindings retain the upstream L2/R2 mapping; they were not remapped to throttle/brake in this work.

Selective control decompilation started with EE routine **0x00210F90**, now expressed as `gt3::normalize_mapped_input` with readable channel, raw-value, sensitivity, and response-curve names. It handles table-based axis response, positive/negative axis halves, pressure sensitivity, and saturation. A differential harness invoked the actual generated game routine and compared **20,480 cases** covering every raw byte value, two synthetic response curves, ten channel encodings, and four sensitivities. All matched. The helper is a verified reference implementation; the live game still uses its original translated control routine. Action bindings, steering smoothing, dead zones, camera state, shifting, and physics integration have not all been decompiled.

## Implementation and provenance

Upstream base: `snuri00/ps2-web-recomp`, commit **b6482fb4b3e89657917b664f829f20307e1899c1**. The source patch includes the earlier GT3 boot/runtime fixes, scheduled analog test inputs, and the new resolution work.

The camera/HUD address leads and triple-width constants come from [Silentwarior112's GT3 PBPX-95503 patch](https://github.com/Silentwarior112/PCSX2-patches/blob/main/Gran%20Turismo%203/USA%20PBPX-95503/8AA991B0.pnach). This experiment adapts that profile for static recompilation rather than running PCSX2. Each expected instruction/data word was verified against this extracted core before applying changes.

- `scripts/gt3_triple.py` refuses any core ELF whose SHA-256 differs from **b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763**. It writes a separate patched ELF and manifest; the input ELF and ISO are unchanged.
- Camera instructions are patched **before** recompilation. Writing an instruction to guest RAM alone would not change its already translated native counterpart.
- The source profile and `triple-manifest.json` give semantic names to projection, mirror, text, canvas, and visibility adjustments. These are analyst-assigned names, not recovered original symbols. License-screen roles remain candidates awaiting scene validation.
- A supported recompiler probe at **0x0017E888** marks race/replay rendering and selects 16:3 presentation. Other scenes default to 4:3. The GT3 display flag at **0x002F424C** enables its widescreen HUD behavior. The scene override expires when that render path stops being called.
- Internal x/y sample counts are independent throughout rasterization, display readback, copying, and GPU state conversion. Existing isotropic snapshots can be converted; new anisotropic snapshots use a packed x/y scale marker and require this updated runtime.

## Measurements

All numbers below are short, unpaced, single-thread scene samples. They are not full-track averages or a promise of sustained frame rate. Timing excludes the final capture itself.

| Sample | Internal scale | ms/frame | Equivalent fps |
|---|---:|---:|---:|
| Super Speedway, throttle held | 9×3 | 31.26 | 32.0 |
| Same Super Speedway scene | 6×3 | 28.16 | 35.5 |
| Same Super Speedway scene | 3×3 | 25.56 | 39.1 |
| Fresh-boot Super Speedway scene | 9×3 | 32.21 | 31.0 |
| Trial Mountain, short continuation | 9×3 | 15.63 | 64.0 |
| Midfield, car against a barrier | 9×3 | 8.09 | 123.6 |

The Midfield view is unusually restricted and is not representative of normal driving. Reducing horizontal detail helps only modestly in the matched Super Speedway sample; further profiling is needed to identify the remaining cost. A 9×9 probe worked but spent unnecessary work on 4032 vertical pixels. The 9×3 path avoids that cost while keeping 5760 horizontal samples. Lower horizontal scales retain the output dimensions and camera view but upscale fewer horizontal samples.

## Validation

- Native build and isolated rebuild script: passed.
- Source patch application dry run against the clean upstream source: passed.
- `git diff --check`: passed.
- Actual GPU sample-addressing test at 9×3: passed.
- GPU sample-state round-trip and isotropic-to-anisotropic conversion: passed.
- Actual game snapshot at 9×3 saved and reloaded: passed.
- Control-normalization differential test: **20,480 cases passed**.
- Earlier hardware/runtime regressions against the new runtime: passed.
- Native Wayland presentation: passed at the compositor's smaller drawable size.

## Launch and rebuild

From the Mac:

```bash
ssh gpu-01 $GT3_LEGACY_ROOT/resolution/play-gt3-triple.sh
```

The launcher defaults to maximum horizontal detail. Append `--render-scale 6` or `--render-scale 3` for lower-cost detail settings; vertical scale remains 3. The output request stays 5760 × 1080. It starts with no memory card unless an experiment-only `--memcard` path is supplied.

To rebuild on gpu-01:

```bash
$GT3_LEGACY_ROOT/resolution/rebuild-triple.sh
$GT3_LEGACY_ROOT/resolution/repo/tests/run_resolution_tests.sh
```

The rebuild script builds its own native translation tools, verifies and patches the extracted core, regenerates EE code and recorded VU code, and builds the native executable. It reuses the experiment's previously recorded entry points/VU programs and isolated toolchain. It does not perform a new full disc extraction or exploration pass and does not build browser/Emscripten targets.

## Remaining work

- Move the position indicator from the far left into the center screen.
- Correct stretched pause/confirmation lettering and validate more overlay/menu transitions.
- Check camera projection, visibility, shadows, effects, and mirrors across more scenes. Replay captures revealed overlapping billboard/geometry artifacts that still need diagnosis. The original low-resolution textures remain; higher rasterization resolution cannot add texture detail absent from the game.
- Profile expensive scenes and improve frame times.
- Validate a 5760 × 1080 desktop/streaming session without disrupting production services.
- Continue selective controls decompilation using differential tests before changing live behavior.

The first widened countdown capture retained stale imagery; later captures after the transition cleared it. No claim is made that every rendering defect is fixed.

## Saved evidence

- `super-speedway.png`, `trial-mountain.png`, `midfield.png`: actual target-size native captures.
- `baseline-9x3.png`: original 4:3 camera within target-size output.
- `bumper-view.png`, `chase-view.png`, `l1-view.png`: camera choices.
- `title.png`: proportional menu presentation.
- `pause.png`, `exit-confirm.png`, `return-menu.png`: remaining overlay issues and replay rendering. The attempted return-menu sequence stayed in replay; a complete return to selection menus is not claimed.
- `gt3-resolution.patch`: source-only patch, with no game assets or generated game code.
- `triple-manifest.json`: verified addresses, expected words, replacements, and semantic names.
- `performance.json` and `adaptive-*.log`: measurements and frame dimensions.
- `final-tests.log`, `window.log`, `rebuild.log`: regression, drawable-size, and build evidence.
