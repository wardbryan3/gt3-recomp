---
title: Supported original profile and state formats
---

Original profile: **USA PBPX-95503 v1.10**.

| Input | SHA-256 |
|---|---|
| Original extracted ELF | `b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763` |
| Retained comparison ISO | `0946bb943a766d0afe057fbff5aa96132b16a797f3e3edc985a3b6d2f3afee0e` |

Hashes identify supported original inputs, not distribution rights. Bring your own
legally obtained ISO; do not publish input/output game content. Other revisions,
regions, device configurations and discovery coverage need separate qualification.

Current native snapshots use **PS2STATE version 3**. Original retained version-2
states must not be imported by changing a header. A snapshot is runtime continuation
state; a memory card is separate persistent save data. Use fresh disposable output
paths/cards, never overwrite a user's save or a retained fixture.

The [historical native-v3 baseline](../research/checkpoints/native-v3-baseline.md)
records a normal-boot fixture, process-local external UTC input and compiled host
Thread-padding observations. Its unresolved 22-versus-23 byte-count discrepancy
remains unresolved; this reference does not choose a count or broaden any comparison
exception. Ordinary driving continuations and explicitly declared fixture recaptures
have different qualified comparison rules in the [validation guide](../developer-guide/validation.md).
