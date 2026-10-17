---
title: 0049AF40 pedal admission — read-only audit, stopped
---

:::note Historical source context

This page preserves findings/instructions from the pre-restructuring context
`aee79fba37937e4dc99dac4263589d005112c504` and its explicitly versioned predecessors.
Paths, Frozen labels and native validation-host results below are **historical**,
not current product integration approval. Use the [current workflow](workflow.md)
and [execution status](development/restructuring.md) for maintained commands and actual gates.

:::


## Current disposition

This is the immutable **earlier read-only stopped audit**, not the latest admission
decision. The separately authorized [closure](pedal-closure.md) now establishes
actual-context equivalence, ownership, displacement cause and guarded substitutions
for every observed representative context. Its source/authority version is separate;
this audit's original evidence, protected hashes and zero-replacement result remain
unchanged. No universal or physical-device claim follows.

## Historical decision

**Safe admission and actual-context clean equivalence are not fully established.
Stop; do not expand the guard.** The Frozen implementation/header, guard and
`pedal-validation.json` authority are unchanged. The stopped profile authority is
also unchanged. No runtime build, new gameplay run, input injection, relocated
command experiment or guard bypass was performed in this audit.

The important new finding is ownership: **0049AF40 and0049AF50 are observed
addresses of an activation-local stack command, not independently identified
global BSS command objects.** Earlier BSS wording, including the Frozen source
comment, is an unsupported ownership attribution. That comment is deliberately
not edited under this read-only authorization. Whether the underlying stack
reservation is BSS-backed is a separate, unresolved allocation question.

Authority: `decomp/gt3/pedal-admission-49af40.json`, separately linked by provenance.
The prior profile survey, whose [matrix is retained with closure](pedal-closure.md),
remains a stopped historical result;
this audit does not turn protective fallback into clean execution.

## Provenance, layout and lifetime

Original `001E4D38` reserves **64 bytes** on entry. Its first **16 bytes** hold the
command; saved low-64-bit `s0`, `s1` and `ra` slots start at frame+16,+32,+48.
Original producer `00210740` receives this frame-base pointer and first calls
`001F4330`, which clears **all16 bytes**, before filling existing input fields.
The wrapper may then pass the same pointer to an optional virtual command hook
when car+`136E` is zero. No new implementation of these producers was recovered.

The existing partial command view agrees with the consumed layout:

| Byte offset | Bounded meaning |
|---|---|
| +0 | Flags |
| +1 | Command mode |
| +2…+7 | Other command fields, not newly interpreted here |
| +8 | Unsigned accelerator halfword |
| +10 | Signed brake halfword |
| +12 | Unsigned auxiliary halfword |
| +14…+15 | Not newly interpreted |

For kind0, when car+`14B8` is zero or car+`14BA` is nonzero, the wrapper reaches
original `001E4CB0`, which reserves32 bytes and passes the same command plus
car+`1304` to `001E4478`. The latter's176-byte frame yields:

**command = pedal-region SP +208 (`0xD0`)**.

No allocator selects a new command object in this chain. Storage lifetime is the
owning `001E4D38` activation; its64-byte frame is released on return and reused
on later calls. This establishes storage lifetime, **not a global no-escape
proof**: all possible virtual-hook targets, retention and reentrancy were not
audited. The underlying thread/stack reservation and the complete upstream
reason for the16-byte position difference also remain unresolved.

## Callers and selection

Ghidra found a direct incoming reference at **001F3B64**, in containing function
**001F39D8**, returning to **001F3B6C**. Its relevant loop obtains a car through
`001F2B68` and calls `001E4D38`; the loop start depends on whether its second
parameter is zero and is bounded by the original car count. Do not assign a new
player/AI/mode meaning to that parameter. The wider simulation is not recovered.

Static incoming references to001F39D8 occur at0017C840 and001F14A4. Those address
projections are not a complete indirect caller inventory or proof of which outer
activation produced each observed SP. In particular, there is **no established
mode-specific global-buffer selector** between49AF40 and49AF50. The observed
absolute address follows the active call stack. The optional virtual command hook
remains an indirect selection point upstream of the pedal region.

The analyzed direct-xref result for0049AF40 was empty. That is consistent with a
stack-computed address, but is not proof of no other references or writers.

## Retained live evidence, reanalyzed read-only

The identity-verified prior survey contains4,199 original pedal entries across14
runs, including exploratory duplicates. All4,199 satisfy the same command/SP
relation and original join `v0`/`s1`, preserved SP and GP checks. **4,185 entries**
also have a preceding recorded wrapper entry, proving
`command = wrapper-entry SP -64` and return address001F3B6C. The first wrapper
entry in each run was not logged by the old host; the14 missing links are not
silently counted as observed. This is reanalysis of retained live execution,
**not a fresh capture**.

| Context | Command | Pedal SP | Observed original region cost |
|---|---|---|---|
| Single Race pad, including AT/MT cars | 0049AF50 | 0049AE80 | 63–72 |
| Time Trial / Free Run / B-1 | 0049AF40 | 0049AE70 | 63–72 |
| Existing synthetic steering compatibility cases | 0049AF50 | 0049AE80 | 123–132 |

Costs are exact budget differences between original entry/join observations and
lie inside the prior Frozen audit's48–152 range. Similar observed cost is **not**
a replacement differential at49AF40; coverage is only the recorded input paths.
Mode4 compatibility evidence is not native/physical pedal evidence.

The two addresses cannot simply be exchanged in one activation:

- With command at**49AF40**, **49AF50** is the owning wrapper's saved-`s0` slot.
- With command at**49AF50**, **49AF40** is the nested `001E4CB0` saved-`ra` slot.

Thus they share a logical layout **at different stack positions**, not an alias
that can be substituted while leaving the rest of an activation unchanged.
Bounds/disjointness and ownership must be established together, not inferred
from proximity, alignment or a matching calibration fingerprint.

## Differential result and limits

The retained original Time Trial run and its unchanged-guard run were compared
now: **299 entries,0 replacements,299 fallbacks**, exact defined CPU/budget traces,
pedal/profile observations, unchanged steering traces, complete guest dump and
all**three captures**. Only the already documented stale transport-PC observation
field is excluded from semantic CPU equality. No tolerance or assertion changed.
This establishes bounded **fallback equivalence**, not clean-body equivalence.

The guard's low-address rule excludes49AF40 and exempts only49AF50. That is a
sufficient reason to reject this context. Translation depth and all intermediate
fingerprints were not newly instrumented per entry, so this is not a newly proven
sole-rejection-cause claim. No enabled actual49AF40 clean-body differential or
live substitution exists under the unchanged guard. Relocating data to an allowed
address, comparing two generated executions, or observing exact fallback would
not fill that gap.

Static layout, common region/callers, matching observed selectors and original
ABI/cost support **candidate semantic applicability**. They do not fully establish
safe admission across other stack activations, indirect hooks or unvisited paths.
No new all-mode, invalid/edge-profile, long-session or hardware claim is made.

## Evidence and stop conditions

Original ELF SHA-256 is the established USA v1.10 profile
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
Ghidra12.1.4/r5900 static records are retained in a new private snapshot; the owned
analysis session was closed. Key records:

- Wrapper/lifetime: `ev_7a7a249ad0f3291deb0946a19d09b88008249c10d942c4bf564c68c2343b6858`.
- Common parent: `ev_cd75c411d387fc80dcd6cd69ec492ff126e1fca5323b75502da4d7ae62a893a2`
  (selector001F3B64 resolved to001F39D8, not a new function).
- Producer: `ev_d8eb9a12c74539978d50bbaf9f564ada5a33ab691e1f45e6f70ebddda1775618`.
- Clear16-byte layout: `ev_a97feea50bee968e6d4d240004c3c3679505a7e68e3c07d17550caa5053aa6b3`.
- Manual wrapper: `ev_6b282703c7b457fdbc13c8de5d4a8557cfa46439cdffb362f9336b42c4b0fe37`.

Instruction-level frame accounting was cross-checked against pinned original
translations. Ordinary-shell ELF32 parsing finds49AF40 outside the file-backed
load segment; that does not establish the backing stack/BSS allocation. Raw
translations, pseudocode, traces and captures remain private and unchanged.

The new `scripts/audit_gt3_pedal_admission.py` only decodes/reduces retained files;
it does not execute gameplay, write guest state or call the replacement. Four
new private artifact hashes pin its analysis, static snapshot, protection baseline
and ELF-layout metadata; the strict check also verifies the prior501-file survey
and unchanged baseline/Frozen proof.

```bash
just verify-pedal-admission /absolute/path/to/this/repository
```

Final unchanged `just check`, `just test`, `just docs-build`, strict admission
verification (including prior survey/Frozen/baseline proof), historical private
verification and the four protected source/authority hash checks passed. No fresh
full game-dependent native regression suite or enabled-admission live run was
performed; unchanged source-only checks and retained proof are not those claims.

**Stop without a guard proposal or expansion.** A future separately authorized
proposal would need actual-context complete CPU/scratch/ABI, full command/stack/
neighbor mutation and exact path-cost differentials against the independent
original; dynamic frame/thread ownership and non-alias evidence including indirect
hook/reentrancy boundaries; and enabled/disabled/trace-only native-v3 live proof
with actual substitution counters and unchanged regressions. No bypass or relocated
surrogate should be represented as proof of this exact admission. These are
unmet evidence obligations, not permission to implement or execute the next cycle.
