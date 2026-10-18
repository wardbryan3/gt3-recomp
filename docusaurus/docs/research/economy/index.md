---
title: Economy, purchases and garage storage
---

## Scope and evidence labels

This is the closeout of the completed **GT3 USA v1.10 economy investigation**:
original purchase/rejection/sale observations, the dependency reconnaissance, and
isolated C++ recovery. It is not complete economy recovery or a new work order.
**Neither `ps2run` nor `gt3-native` links these recovered mechanisms.** No developer
credit feature, persistence guard, reward system, upgrade system or full native
shopping flow has been implemented by this work.

The original ELF identity is SHA-256
`b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763`.
Addresses below are guest addresses for that profile, not portable host pointers.

| Label | What it establishes | What it does not establish |
|---|---|---|
| **Gameplay** | Ordinary controller-input execution of the independent original generated reference, with UI, memory and selected entry/return/watchpoint observations. | Recovered gameplay execution, physical-PS2 equivalence, exhaustive execution coverage or whole-state equality. |
| **Static** | Completed original ELF inspection with Ghidra's r5900 analysis, corroborated against unchanged generated-original bodies. Instruction widths and float load/store instructions take precedence over inferred decompiler types. | That every branch has occurred in a game session or every caller's preconditions are understood. |
| **Differential** | Isolated recovered outputs/mutations compared with independently executed original generated functions under stated fixtures and dependencies. | Full CPU/ABI replacement, all gameplay inputs, or product integration approval. |
| **Unresolved** | A dependency, meaning, input domain or branch not qualified by the above evidence. | Permission to invent a name, default, safety check or fallback. |

The current qualification summary is
[`project/gt3/economy.json`](../../../../project/gt3/economy.json), with ownership in
[`implementations.json`](../../../../project/gt3/implementations.json).
These are current records, not a complete system specification. This page retains
the important findings without distributing private traces, original tables,
translated game bodies, screenshots or saves. See the
[publication boundary](../../developer-guide/publication.md).

## Top-down: how the pieces interact

Purchasing separates **permission**, **record construction/storage**, **debit**,
and a **post-debit field update**. Selling separates **permission**, **valuation**,
**credit**, and **record removal/reset**. Pricing is a catalog lookup plus a mode
branch; it is not inferred from the displayed balance. Garage ownership combines
a fixed record pool, embedded list links, an occupancy word and a count.

```text
Original UI / dispatcher FUN_001b6d58
  purchase caller FUN_00125e68
    FUN_0011bc18: eligibility (flags, funds, garage count)
    FUN_00219250: commit body
      FUN_00219048: free slot, temporary build, owned build, insertion
      FUN_00237bc0(record + 0x10): price
      debit state + 0x18
      FUN_001d9f60(record + 0x204): post-debit float32 field update
  sale caller FUN_00125fa8
    FUN_0011bda8: sale eligibility flag
    FUN_00219368: record query, price / 4, credit
      FUN_00219190: index-like field updates, unlink, count decrement, reset

Shared price path:
  FUN_00237bc0 -> FUN_002315d8
    -> FUN_00231548 (resolve table)
    -> FUN_002316e8 (search 64-bit key)
    -> FUN_00231548 (resolve again on success)
  -> row + 0xec; FUN_00231680 selects unscaled or x100 arithmetic
```

**Static + Gameplay:** successful insertion/count increment precedes the purchase
debit. Sale credit precedes unlinking, count decrement and clearing occupancy.
These are **non-atomic sequences**: an intermediate state can contain an inserted
car with the old balance, or sale proceeds with the car not yet removed. Do not
rearrange the operations into an apparently tidier transaction.

The diagram describes the investigated original path. Opaque construction and
other dependencies have not all become C++; the recovered pieces are not a
complete callable replacement for this diagram.

## Original gameplay anchors

Two completed purchase-pair evaluations each passed **22 assertions**. Affordable
and rejected purchases start from byte-identical baseline snapshots, not separate
credit patches. The sale starts with the successfully purchased car.

| Scenario | UI outcome and price | Credits | Garage count |
|---|---|---|---|
| Mazda Demio GL-X(J), affordable | Price **14,660**; purchased; subsequently visible in garage | **18,000 → 3,340** | **0 → 1** |
| Mazda MX-5, unaffordable | Price **22,950**; “Not enough money” | **18,000 → 18,000** | **0 → 0** |
| Sell that Demio | “Sold”; subsequently empty garage; proceeds **3,665** | **3,340 → 7,005** | **1 → 0** |

**Gameplay:** purchase validation occurs at frame **3701**, commit at **4101**;
rejection is at **4101**. Sale eligibility is at **7701**, commit at **8201**.
These are observer frame values for these input sequences, not general timing
requirements. The sale gain is `14660 / 4 = 3665`.

Only pool slot 0 changed in purchase and sale. Rejection left the compared record
pool unchanged. The sold record retained its identifier bytes: becoming free is
not equivalent to erasing the record. Separate untraced controls matched credits,
count, header words `+0x2c..+0x38`, all **112,000 pool bytes**, and the compared list
endpoints. This is not a comparison of the whole game state.

The selected transaction-path comparison passed **35 checks**. Dependency
reconnaissance passed **112 checks** over **637 purchase**, **265 rejection** and
**246 sale** events. Those counts belong to different comparisons; they must not
be added and described as full gameplay differential coverage.

### Observation method and limitations

Runs used ordinary controller inputs, disposable persistence and mandatory OS
confinement: original inputs read-only, only private run output writable, network
isolated. No credit/RAM patches, inferior function calls, gameplay substitutions
or new runtime hooks were used. Version-3 snapshots were required; rejected
version-2 files were not relabelled or converted.

The debugger used hardware watchpoints on the eight-byte balance and four-byte
count, plus selected native-unit entries and guest returns. It checked the `Cpu`
instance and guest return target, distinguishing native preemption exits from
actual guest returns; no such exits occurred in the accepted dependency traces.
It perturbs timing. A watchpoint establishes **value changes**, not the absence of
same-value stores. Selected entries are not exhaustive execution coverage.
Gameplay units lacked useful source-line/type DWARF; host symbol offsets and
`last_guest_pc` are context, not exact guest-instruction proof. Instruction-level
claims require the static original analysis as well.

## Bottom-up: state and record representations

`FUN_00218660` is the original state accessor. In the observed runs, pointer word
`0x00352a94` held state address `0x00958ee0`; slot 0 was `0x00959018`. These concrete
addresses identify those observations, not a stable allocation contract.

| Location | Representation and established behavior |
|---|---|
| state `+0x18` | Eight-byte credit balance; interpreted as signed64 by funds checks and forwarded as a 64-bit value for display. Investigated updates store 64-bit wrapping bits. No valid assignment range is established. |
| state `+0x2c` | 32-bit word copied into record `+0x22c` on insertion, then incremented with wrap. Not decremented by the observed sale. Do not infer a persistent identity scheme. |
| state `+0x30`, `+0x34` | Signed/index-like 32-bit fields used by removal. Both become `-1` after sole-car sale; their wider semantics remain unresolved. |
| state `+0x38` | Signed32 garage-count read; insertion increments and removal decrements the stored 32 bits. |
| state `+0x138` | Start of **200 records**, stride **0x230 = 560 bytes**, not a heap allocation. |
| state `+0x1b6b8` | Collection control; first two words are head/tail for the recovered list operations. This is not a schema for every control word. |
| record `+0`, `+4` | 32-bit embedded next/previous links for those operations. |
| record `+0x10` | Configuration/key subobject passed to price/construction/reset helpers; not a complete recovered vehicle type. |
| record `+0x204` / `+0x208` | Post-debit helper argument / its float32 store destination. Meaning unresolved. |
| record `+0x228` | Free-slot predicate: **zero is free**, any nonzero is skipped. Original initialization produced **1** in the observed purchase. |
| record `+0x22c` | Receives state `+0x2c` on insertion; reset stores `0xffffffff` (`-1`). Preserve the offset-based identifier. |

### Credit reads, eligibility and writes

**Static + Gameplay:** `FUN_00123270` registers `user_money` with
`FUN_0011cc20`; the latter reads state `+0x18` and forwards to formatter
`FUN_0023b868`. `FUN_0011cc20` was entered during the original runs.

**Static + Differential:** `FUN_0011bc18` and `FUN_0011bce0` perform this ordered
check, differing in flag mask **0x1** versus **0x2**:

1. Call `FUN_00218660`, load a pointer from state `+0x30d00`.
2. Call the accessor again; read its state `+0x18` as signed64. Use the selected
   pointer `+0x10` for `FUN_00234380` and the price query.
3. Reject on the relevant flag, then on signed64 `balance < price`.
4. Call the accessor again and `FUN_00219448`; succeed only if its signed count
   is less than **200**.

Do not merge those accessor calls: the bounded test deliberately supplies distinct
state pointers. Each rejection calls `FUN_001c4f80(4)` and returns an original
message pointer; success returns zero:

| Check result | Original pointer / resource |
|---|---|
| Flag rejection | `0x30ff90`, `00cmn/not_for_buy` |
| Insufficient funds | `0x30ffa8`, `00cmn/no_money` |
| Garage limit | `0x30ffb8`, `00cmn/max_car` |

**Static + Gameplay:** sale eligibility `FUN_0011bda8` tests bit **0x2** from
`FUN_00234380`, returning zero on the observed successful path. Its static failure
path reports `00cmn/not_for_sell`; it is not balance-range validation. A rejected
sale was not exercised in the completed gameplay scenarios.

**Static + Differential:** raw field operations are `FUN_0021a6d0` (getter),
`FUN_0021a740` (wrapping add), and `FUN_0021a7d8` (setter). They take a neutral base
address and do not establish caller identity, safe balance ranges or save safety.
They are **not a universal balance hook**: the observed purchase and sale directly
write the balance; the selected traces did not enter these leaves or alternate
debit body `FUN_002192a8`. That is not a global absence-of-call proof.

`FUN_00219250` calls `FUN_00219048`; a zero result bypasses the debit. A nonzero
record result leads to price lookup at record `+0x10`, wrapping64 subtraction at
state `+0x18`, then `FUN_001d9f60(record + 0x204)`. This body has no sufficiency
check or clamp; permission was checked earlier. Alternate body `FUN_002192a8`
uses `FUN_00219128` and has no final post-debit helper. Its bounded tests are not
original gameplay coverage of that route.

**Static + Gameplay, not a recovered sale body:** `FUN_00219368` queries a record
through `FUN_0023c4d8`, calls `FUN_00237bc0(record + 0x10)`, divides the signed32
price by four **truncating toward zero**, adds that signed result to the balance
with wrapping64 storage, then calls `FUN_00219190`. The signed division matters:
it is not an unconditional arithmetic right shift/floor for negative bit patterns.
Negative synthetic arithmetic inputs are not evidence of legal negative prices.

## Garage storage, links and reset

**Static + Differential:** `FUN_00218f88` scans the pool in increasing slot order,
returns the first record whose `+0x228` word is zero, and returns zero if all 200
are occupied. The allocator does not use the count as its free-slot predicate.

`FUN_00218fe0` copies state `+0x2c` into record `+0x22c`, increments state `+0x2c`,
calls list insertion, increments state `+0x38`, and increments `+0x30` only when
its signed value is nonnegative. No slot allocation or configuration construction
is supplied by list insertion itself.

### Intrusive list primitives

“Intrusive” means the links are inside the original record, not separate nodes in
a host `std::list`:

- `FUN_0023c1b8`: null record returns the collection without changes. For an empty
  list, set tail; otherwise set the old head's previous link, **reload head**, then
  set the new record's next link. Finally set head. It does **not** initialize the
  new record's previous link; the empty branch does **not** write its next link.
  The caller must supply the appropriate detached/initialized record.
- `FUN_0023c288`: null record is a no-op returning the collection. Update matching
  head and tail, patch next/previous neighbors using the original fresh loads,
  then clear record `+4` before record `+0`. Do not bulk-zero or reorder stores.
- `FUN_0023c4a8`: traverse next pointers, returning the sign-extended32 index in
  64-bit bits, or all-one bits for `-1`. No cycle guard is invented. Qualified
  fixtures supply finite well-formed lists.

### Removal and the free-slot transition

`FUN_00219190` returns immediately for a null record. Otherwise it:

1. Queries the record index with `FUN_0023c4a8`.
2. Compares it with signed state `+0x30`: equality stores `-1`; a lower index
   decrements that field. Copies the resulting value to state `+0x34`.
3. Calls `FUN_0023c288`, then decrements state `+0x38`.
4. Scans exact pool addresses. Only a matching pool record is passed to
   `FUN_0023af40`; this is not permission to free an arbitrary pointer.

`FUN_0023af40` first calls **opaque** `FUN_00237980(record + 0x10)`, then writes
zero to `+0x228` and `-1` to `+0x22c`. Static inspection of that original dependency
shows a binding-reset call `FUN_00231598` at subobject `+0x1d0`, followed by a
44-byte zeroing operation at subobject `+0x1e8`: record **`+0x1f8..+0x223`**.
The recovered reset does not replace this dependency with a guessed byte pattern.

**Gameplay:** sale unlinks with count still 1; count becomes 0 while occupancy is
still 1; reset then clears occupancy, resets `+0x22c`, and retains the record key.
**Differential:** full-pool removal makes the released slot selectable again;
fixtures also reinsert an explicitly initialized detached record. That is
**freed-slot reselection/reinsertion**, not an observed second in-game purchase or
proof of complete configuration reconstruction on a reused slot.

## Catalog and pricing mechanics

**Static + Differential:** `FUN_00231548` loads a root through the supplied handle,
reads the mask at root `+0x0c`, the selector word at `root + 0x10 + 4*selector`,
and the offset at root `+8`. The result is the wrapping32 address:

```text
root + (selector_word & ~mask) + offset
```

`FUN_002316e8` searches unsigned64 keys in a nonempty sorted table. Count and
stride are unsigned16 fields at table `+8` and `+0x0a`; rows begin at `+0x10`.
It returns a sign-extended32 index or `-1`. `FUN_002315d8` returns zero for a
missing key. On success it **resolves the table again**, reloads stride, and
returns `table + 0x10 + stride * index`. The original search has no empty-table
safety guard; empty/corrupt-table behavior is not qualified by these fixtures.

**Gameplay:** selector **30** resolved table `0x0086bd78`, count **244**, stride
**264**. The Demio row was index **185**, address `0x00877c50`, field `+0xec`
**14,660**; MX-5 was index **235**, address `0x0087afe0`, field **22,950**. These
are selected observed facts, not a distributed copy of the original catalog.

`FUN_00237bc0` reads the key at its argument, uses the handle at argument `+0x1d0`
for selector 30, reads row `+0xec`, and applies `FUN_00231680`. That predicate is
**32-bit global at `GP - 18968` (`GP - 0x4a18`) equals zero**. In the observed
runs the address was `0x00352fd8`, value **1**, predicate **0**: price unscaled.
When the predicate is nonzero the calculation multiplies by **100**, keeps the
low32 bits, and returns their sign-extended value. It is neither a percentage
calculation nor multiplication by the Boolean predicate.

**Differential, not gameplay:** mode-zero and arithmetic-boundary fixtures verify
the x100 branch, wrapping/truncation, and zero/nonzero-word predicate behavior.
The meaning of the mode is unresolved; do not call it a currency or region mode.
The price caller has no invented missing-row fallback: a zero lookup result
leads to its read at `0xec`. Missing-row **lookup** is tested; valid preconditions
for missing-row **pricing** remain unqualified.

**Static:** a writer chain exists:
`FUN_00127988 → FUN_00245480(&global, value) → FUN_00245628`, followed by further
update work. An empty absolute-address xref query was not proof of no writers;
GP-derived pointers must be considered. No mode-change gameplay scenario was run.

## Configuration construction and post-debit mutation

**Static + Gameplay:** purchase `FUN_00219048` is not a heap allocator. It selects
a pool slot through `FUN_00218f88`, prepares temporary configuration storage, and
uses descriptor/key resolution and `FUN_00231db0` before building the owned
configuration via `FUN_0023af78`. At the **4101 purchase commit**, two
`FUN_00231db0` returns within this construction scope were **1**: temporary build,
then build at owned record `+0x10`. `FUN_00231b38(temporary, 2)` occurs between
them. Other preview/menu builds also occur; their trace totals must not be
mistaken for the two commit-scoped builds.

The owned initializer returns with `+0x228 = 1` while count is still zero and
credits still 18,000. `FUN_00235f88` is also called on record `+0x10` with the
construction caller's third argument before insertion; its semantics are
unresolved. It also occurs inside build/preview paths, so it is **not** simply
a post-debit cleanup operation. List insertion finishes before count increment,
and construction returns the record before the debit.

The free-pool return-zero branch and build-failure cleanup paths are visible
statically, but missing-catalog/build failure and full-garage **gameplay** were
not exercised. No complete configuration constructor has been recovered or
verified by the bounded transaction mocks. Those projected call signatures omit
full incoming constructor-argument forwarding; a future binding cannot ignore it.

The separate post-debit chain is:

```text
FUN_001d9f60 -> FUN_001d9ce8 -> FUN_001dac48 -> FUN_001dab50
```

**Static:** `FUN_001d9ce8` passes original global address `0x002d2b00` to
`FUN_001dac48` and stores the returned **f0 float32 bits** at its argument `+4`.
With argument record `+0x204`, that is record `+0x208`. Original `lwc1`/`swc1`
instructions invalidate an interpretation based solely on decompiler integer or
void return types.

**Gameplay:** the field changed from zero to **`0xc8927c00` = -300,000.0**, matching
the source global. Initialization byte `0x002d294c` was already **1**; credits
remained 3,340 during this helper. The field's meaning is **unresolved**: do not
label it wear, fuel, a timestamp or a credit amount.

**Differential:** both recovered forwarding entries preserve float bits, including
signed zero, subnormals, infinities and NaN payloads, without host FP arithmetic.
Their fixtures execute the original `FUN_001dac48` and initialization dependencies,
including an initialization-enabled case. This does not recover or explain that
initialization algorithm.

## Isolated recovery and verification status

All sources below are under `src/gt3/gameplay/economy/`, namespace
`gt3::economy_recovery`. `gt3_economy_recovered` is an isolated static library,
not a product binding. Guest addresses wrap32; stored arithmetic retains original
widths. Unknown field and dependency identifiers remain offset-/address-based.

| Implementation / test | Qualified result |
|---|---|
| [`gt3_garage.hpp`](../../../../src/gt3/gameplay/economy/gt3_garage.hpp), [`gt3_garage.cpp`](../../../../src/gt3/gameplay/economy/gt3_garage.cpp), [`gt3_garage_list.cpp`](../../../../src/gt3/gameplay/economy/gt3_garage_list.cpp); [`garage oracle`](../../../../validation/gt3/differential/gt3_garage_oracle.cpp) | **385** cases: **265** pool cases, every first-free position/exhaustion, randomized occupancy, empty/single/multi/200-node lists, head/middle/tail cases, null guards, reset and reselection/reinsertion. **50** composed reset cases execute original `FUN_00237980`. |
| [`gt3_economy_catalog.hpp`](../../../../src/gt3/gameplay/economy/gt3_economy_catalog.hpp), [`catalog implementation`](../../../../src/gt3/gameplay/economy/gt3_economy_catalog.cpp); [`catalog oracle`](../../../../validation/gt3/differential/gt3_economy_catalog_oracle.cpp) | **1,200** cases: **1,050** resolution/search/lookup, **120** pricing/predicate, **30** float forwarding. Sorted unique synthetic keys, counts 1/2/3/7/16/31/244, strides 8/16/264, unsigned-key extremes, offset/mask decoding, found/missing rows. Original float dependency retained. |
| [`gt3_economy_state.hpp`](../../../../src/gt3/gameplay/economy/gt3_economy_state.hpp); [`state oracle`](../../../../validation/gt3/differential/gt3_economy_state_oracle.cpp) | Promoted existing **3,960 leaf cases + 40 chains**. No mocked callees; field outputs, address/value wrap and RAM checks. Not legal credit-assignment or caller qualification. |
| [`gt3_economy_checks.hpp`](../../../../src/gt3/gameplay/economy/gt3_economy_checks.hpp); [`checks oracle`](../../../../validation/gt3/differential/gt3_economy_checks_oracle.cpp) | Promoted existing **3,024** cases; all four outcomes, signed comparisons, ordered calls and distinct accessor results. Dependencies intercepted, not complete original eligibility environments. |
| [`gt3_economy_transactions.hpp`](../../../../src/gt3/gameplay/economy/gt3_economy_transactions.hpp); [`transaction oracle`](../../../../validation/gt3/differential/gt3_economy_transactions_oracle.cpp) | Promoted existing **1,024** body cases, including **256** null paths and **168** underflows; ordered dependency mutations and store-before-post-call. Construction/value/post-call dependencies mocked; not complete purchases. |
| [`source regressions`](../../../../validation/gt3/differential/gt3_economy_source_test.cpp) | Public, no-game checks of source behavior, including list/reset store sequences and the ordered insertion reads/stores for empty/nonempty lists and both signed branches. These are not an independent oracle. |

Total: **9,593 function cases plus 40 chains**. Subcounts above overlap their
parent suite and must not be added again. Extreme raw-bit fixtures establish
instruction/body contracts, not that each input is a legal gameplay state.

The garage/catalog comparisons check logical return bits where defined, all
**32 MiB RAM except a reserved 512-byte original ABI stack workspace**, and ordered
opaque-dependency checkpoints. Original SP/callee-saved checks do not make the
memory-native code a full CPU/register/stack/instruction-cost replacement.

**Insertion ordering:** `FUN_00218fe0` reads count `+0x38`, reads state `+0x30`,
then stores the incremented count before conditionally updating `+0x30`. The C++
now preserves that original sequence. The public regression records ordered
`load32`/`store32` accesses, including values, for empty and nonempty lists and
both signed branches. It was demonstrated to fail against the earlier reordered
implementation before the fix. Final-memory comparisons alone cannot establish
access order; these source regressions supplement, rather than replace, the
original-function differentials. They do not establish access-trace equivalence
for every recovered function or supply a production binding.

### Reproduce the established verification

The maintained [runner](../../../../validation/gt3/differential/run_economy.py)
requires explicit private reference inputs; it does not rebuild or modify them:

```sh
just verify-economy /absolute/path/to/core.elf /absolute/path/to/original-reference-build
just check
just test
```

The ELF must match the fingerprint above. The reference build must provide the
original `ps2run`, `gt3-native`, `libps2game.a` and `libps2runtime.a`; the configured
generated-header/source directory and locally fetched wgpu archive must also be
available. See `python3 -B validation/gt3/differential/run_economy.py --help` for
its generated-directory option. Missing
inputs fail rather than skipping tests. The disposable report is
`local/economy-recovery/current/report.json`, with source/test hashes, reference
hashes, suite outputs and an unchanged-input guard. It is private and not copied
into these docs. See [commands](../../reference/commands.md) and
[validation boundaries](../../developer-guide/validation.md).

For maintainers who already have the ignored original-scenario tools and fixtures:

```sh
python3 -B local/purchase-scenarios/verify_dependencies.py
python3 -B local/purchase-scenarios/test_scenarios.py
```

These recompute the existing **112 dependency checks** and **12 launcher safety
tests**, respectively; they do not replay gameplay. The completed private
purchase-pair reports each record 22 assertions; the selected path comparison
records 35. They are support for the facts stated here, not the only place those
facts are documented. Raw traces, screenshots, states, catalog data and original
translations stay private. No new original-gameplay run is implied by a docs build.

## Unknowns and remaining work — not authorization

| Open item | Evidence boundary / requirement before a stronger claim |
|---|---|
| Mode and record `+0x208` meanings | Arithmetic and bits are established; domain meanings are not. Preserve neutral names. |
| Construction and reset semantics | Further qualification of `FUN_00231db0`, `FUN_00235f88`, `FUN_0023af78`, `FUN_00237980` and their dependencies; no guessed native constructor/reset. |
| Exceptional inputs | Missing-catalog/build failures, empty/corrupt/duplicate-key tables and caller preconditions are not comprehensively qualified. Static branches are not gameplay tests. |
| Full garage, multi-car removal, slot reuse | Function fixtures cover these mechanisms, but full-garage rejection, multi-car sales and an actual freed-slot repurchase were not demonstrated in gameplay. |
| Complete transaction recovery | `FUN_00219368` sale orchestration remains original; debit bodies remain bounded projections. Constructor arguments, all side effects and failure paths still need explicit contracts. |
| Other economy paths | Rewards, upgrades, other purchases/sales, all balance writers and full saved-game round trips remain outside established coverage. No whole-state or headless-gameplay equivalence. |
| Production binding | No full CPU/ABI/cost claim, no binding installed, no integration approval. Insertion's identified read ordering is corrected and regression-tested; do not generalize that test to all functions or all backend semantics. |
| Developer credit assignment | Safe range, lifecycle boundary and a complete persistence guard remain unqualified. Raw setter correctness is not feature safety. |

The persistence blocker is concrete: `runtime/src/iop/sio2.cpp::flush_cards()` can
write a dirty card after a quiet-vblank interval, independently of the save UI;
`runtime/src/system.cpp` invokes it and handles state snapshots separately.
Sandbox confinement protects investigation inputs, **not production save safety**.
There is no usable top-up command from this work.

The next technical work would require a separately scoped decision. This closeout
preserves what is known and what is not; it authorizes neither more exploration
nor implementation. Recovery, verification and
[integration approval](../../reference/authorization.md) remain separate.

The owner has selected a protected funded test save instead of a runtime refill
feature. The [private funded test fixture](funded-test-save.md) now provides
99,999,999 starting credits through a read-only master memory-card image and
writable disposable copies. Cold loading, a purchase and sale, normal saves and
fresh-copy reset have passed bounded tests. The owner approved temporary fixture
preparation, not clean production code or changes to the Oracle. This is not a
proven maximum balance or a product credit-assignment API. A fresh copy resets
both credits and master progress; it does not preserve later purchases.
