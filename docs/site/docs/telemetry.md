> **Evidence context:** historical private experiment. Current main preserves source and findings; clean steering/synthetic runtime installation is not yet revalidated or enabled here.

---
title: Telemetry and race-state candidates
---

| Guest field / routine | Candidate meaning | Confidence / evidence boundary |
|---|---|---|
| car+13A0; +FF0+i*A4 | Steering and per-wheel angles | High; static, differential and bounded running-game observations |
| car+13AC/+13B0/+1428 | Processed accelerator/brake and effective accelerator | High static / 22 constructed original-code fixtures, not a live pedal telemetry contract |
| car+13CC | Engine angular-rate candidate | Static integration and fixture; physical units/sign/range need verification |
| car+1414; `001E6D00` | Display engine speed candidate | Static rate×60/constant and idle-floor conversion; stored signed16, may wrap |
| car+140C | Steering-envelope speed input candidate | Live envelope changes at speed; units/frame not certified |
| car+F84 and following vector | Position-like candidate | Static motion/post-update consumers; axes, world frame and units not recovered |
| car+13BA/+13BB | Ratio index / driveline state candidates | Different fields; do not conflate with displayed gear |
| `001ED000(race,index)` | Reads car-slot word at race+E388+index*4 | Static getter; count/ownership and player association need proof |
| `001F2B18` | Countdown-like race field +B7AE and callback | Static only, no lap/finish interpretation |

Live pointers in the known snapshot (car01FBB7BC, input01FAC260) are observations, **not stable API addresses**. Find objects through proven ownership paths and guards in any future telemetry design.

`001E7D90/001E8008` are vehicle motion candidates; `001EB218` orchestrates many post-update routines, including geometry/state/output work. None is a complete recovered telemetry boundary. `RaceLapTime` at003279B0, `RaceLapDisplay` at0032F190 and `LapCountLabel` at00330F18 are retained typed-string seeds; UI names do not establish the lap counter or timer. Trace writers and event lifecycle before exposing lap/finish state.

Future read-only telemetry contract must specify units, coordinate frame, sampling phase and atomicity, object lifetime/player selection, episode/tick identity, valid flags, race-state transitions, signed/wrapping fields and replay validation. Correlate observations with visible gameplay and independent original memory, not convenient names. No exporter, new probe, action API or live lap/finish experiment was implemented tonight.
