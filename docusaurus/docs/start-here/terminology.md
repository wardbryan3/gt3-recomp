---
title: Terminology and claims
---

| Term | Meaning in this project |
|---|---|
| **Original** | Behavior executed by the independent original reference. |
| **Recovered** | Readable implementation verified against original behavior within a stated boundary. |
| **Modernized** | Separately approved native implementation preserving the approved behavior without its old execution mechanism. |
| **Enhanced** | Intentional change beyond original behavior, explicitly activated and tested both OFF and ON. “Extended” is also used in historical records. |
| Oracle | Independent original reference that supplies expected behavior, not the implementation being tested. |
| Differential test | Original and candidate execute equivalent inputs; observable differences are checked. |
| ABI | Application binary interface: register, stack, argument and return conventions visible across a code boundary. |
| EE / VU | PS2 Emotion Engine CPU / Vector Units. Native generated code still represents their execution. |
| Fixture | Controlled inputs and initial state for a test; synthetic fixture values are not measured stock-car calibration. |
| Partial layout | Only evidenced fields are named; opaque padding denotes unknown storage, not a reconstructed whole class. |
| Instruction budget | Runtime guest instruction accounting; exact equality is not a host-performance benchmark. |
| Shadow | Comparison on copies of the actual entry state; not itself an actual gameplay replacement. |
| Fallback | Original execution after candidate rejection; parity during fallback is not successful substitution. |
| Frozen | Historical label for an exact bounded evaluated source/context; not current product integration approval. |
| Proof / approval | Evidence supports a claim; only the owner can authorize its specified integration. They are separate records. |

Index **0 is Reverse**, not Neutral, in the recovered transmission slice. Selector
return **−1 means no accepted selection**. A coupling candidate is not a physical
clutch axis. These distinctions matter throughout the [worked example](../developer-guide/worked-example-mt-selector/index.md).
