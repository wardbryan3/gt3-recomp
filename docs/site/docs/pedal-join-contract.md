---
title: Pedal v1 — resumed join contract audit
---

> **Current admission version:** the semantic join contract remains unchanged.
> The original absolute-pointer exception is superseded by the separately pinned
> [observed-context closure](pedal-closure.md): actual-entry whole CPU/RAM/cost
> proof and structural-frame admission cover all14 observed contexts /five classes.
> This earlier contract does not independently establish the newer guard.

Source base: `46a32c7` (the committed/pushed current-main native baseline). This
resumes the prior audit, not broad reconnaissance. Existing static citations and
boundary findings in [the stopped audit](pedal-recovery-v1.md) remain applicable.

The final [Pedal v1 report](pedal-v1.md) now records 131,072 exact original/clean
join cases, complete CPU/cost proof, wrapper/consumer and v3 live validation. The
initial audit below records what was established before the first implementation.

## Boundary and observations before implementation

Entry **001E48FC**, inclusive end **001E4BA7**, generated join **001E4BA8**.
Prefix/steering, shift/handbrake, `update_control_coupling_candidate` (001E4180),
wrapper and all simulation consumers stay generated. Original 001D92E0 remains a
called generated dependency; no math, coupling or adjacent recovery is authorized.

An independent ORIGINAL-only generated-EE audit has executed **32,768 cases** at
that exact interior entry. A disposable unit supplies a host-only test entry and
returns at the join; no original body or production dispatch entry is changed.
Tests initialize command/car/history/stack/register state, execute the original
instructions and verify the mutation/stability surface. New private output is
`local/pedal-v1-resume/audit/results.log`; initial measured cost is **48–139** EE
instructions, including original descriptor evaluation. This is not yet a clean
differential or live pedal proof.

Inputs: `s7` car; `s0=car+F84`; `s2` command; `s3` control-state pointer;
`v1=int8(car+136D)`; pinned `gp=3579F0`. Other incoming scratch/FPU values must
persist wherever the original does not overwrite them. The prefix owns the
176-byte frame and all saved register slots. The manual wrapper supplies
`s3=car+1304`; unsupported aliases/contexts must remain generated.

Direct memory writes are **car+13AC, car+13B0, control-state+0/+2** only. The command,
stack, descriptors and every neighboring car byte remain unchanged. The null
derivative argument at both descriptor call sites is part of this guarantee.
Effective accelerator +1428 and coupling candidate +139C are NOT bounded writes.

The original can clobber low 64-bit GPR lanes **r1–r8, s1 and ra**, FPRs **f0–f3
and f12**, plus the FCR31 condition bit. Upper GPR lanes and all other CPU state
remain stable. `v0=uint16(car+14BA)` and computed policy `s1` are required live
outputs. Preserve scratch effects as well, rather than relying on dead-register
exclusions: this avoids different saved thread contexts when the runtime yields.
FCR31's other bits (including existing invalid flags) remain untouched: no divide
occurs on the derivative-null response paths.

The fixture join checkpoint sets the semantic PC to 001E4BA8 for comparison.
Generated direct branches do not maintain an instruction-by-instruction `Cpu.pc`;
the last jump-table/helper dispatch PC is transport state, not an independent
alternate join. Normal generated continuation overwrites that transport state at
calls/unwinds. No guest instruction is charged for checkpoint observation.

## Cost and arithmetic obligations

Cost is path-dependent, not the linear span size. Decoder costs include flag
branches and halfword wrapping, policy jump-table dispatch, tie selection, history
and clamp paths. Zero analog accelerator with history differs from a fresh zero;
its `<=0` clamp differs from digital release's `<0` clamp. Digital rises bypass
mode-4 descriptor evaluation while history is active. Brake digital clamp and
nonclamp exits have different costs: the latter performs the outgoing suppression
load in a branch delay slot. Descriptor calls retain original EE arithmetic,
register/FPU effects and dynamic cost, with original return PCs 001E4AD4/001E4B9C.

There is no preemption edge within the bounded region or derivative-null leaf
helper. Low/negative budgets must still reach the join with exact consumption.
Depth-limited original helper side-exits cannot be invented into a successful
replacement: unsupported depth/budget/profile/address contexts must fall back
before any mutation. Full region/helper/policy-dispatch fingerprints are appropriate
runtime guards, in addition to the build's original ELF identity check.

Before Frozen evaluation the clean differential must compare **all CPU state**
(including scratch lanes/FCR31), complete car/command/stack/descriptor windows and
exact budget, then run the untouched generated suffix/wrapper and original
consumers independently. Audit case counts above must not be reported as clean
passes. Runtime integration remains explicit and validation-only; canonical
ps2run has no pedal gate.
