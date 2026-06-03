# CLAIM-NUMBERING-RECONCILED.md
# Patent Claim Number Map — Spec vs Evidence-Index
# Produced: 2026-06-02 | Authority: navigator scan (unblock-remaining)
# Status: READY FOR ATTORNEY REVIEW

---

## Problem Statement

Two documents use different claim numbering for the same inventions:

- **Source spec** (`business/patent/_source/PATENT-PROVISIONAL-SPECIFICATION.md`)
  has Claims 1–9, where Claims 7/8/9 were folded in 2026-06-02 from standalone files.

- **Evidence-index** (`docs/patent/_consolidated/CANONICAL-AND-MIRRORS.md §3`)
  lists 13 claims (evidence-index = EI) with a different numbering, e.g.:
  - EI-2 = "stigmergic blackboard, O(F) coordination"
  - EI-3 = "per-branch Merkle rollup + 2-parent acceptance"
  - EI-7 = "four-layer enforcement stack"

The mismatch arose because: the evidence-index was authored against an earlier
draft numbering (or an expanded 13-claim non-provisional plan), while the
provisional spec was consolidated at 6 independent claims + 3 folded-in claims.

---

## Reconciled Map

| Spec Claim | Spec Topic | EI Claim | EI Topic | Match verdict |
|---|---|---|---|---|
| Spec 1 | Memory tier hierarchy (pollen/NECTAR/GOLD) + mechanical promotion gates | EI-6 | hierarchical memory promotion gates | MATCH — same invention |
| Spec 2 | Stigmergic filesystem coordination (manifest-only, no message-passing) | EI-2 | stigmergic blackboard, O(F) coordination | MATCH — same invention |
| Spec 3 | Four-layer enforcement stack (structural/cognitive/reactive/recovery) | EI-7 | four-layer enforcement stack | MATCH — same invention |
| Spec 4 | Shape-registry mechanical verdict classification | EI-8 | shape-registry quality classification | MATCH — same invention |
| Spec 5 | Membench quality measurement substrate (eval probes as shapes) | EI-5 | Membench quality substrate (M1–M11) | MATCH — same invention |
| Spec 6 | Combination claim (1–5 integrated ecosystem) | EI-13* | promotion-staged folder convention + combination | PARTIAL — EI-13 covers staging convention; combination intent shared but EI has no dedicated combination row |
| Spec 7 | Zero-knowledge customer-key-custody architecture | (none in EI 1–13) | — | GAP — EI has no matching claim row |
| Spec 8 | Multi-party hash-rollup completion seal (Merkle + single authority counter-sig) | EI-3 + EI-4 | per-branch Merkle rollup; handshake anchors | PARTIAL — EI-3/4 covers the Merkle/anchor mechanics; Spec 8 is broader (completion seal + f(0) property) |
| Spec 9 | Public hash-chained stigmergic blackboard (cross-tenant, O(F)) | EI-1 + EI-2 | COC = mission-graph edges; stigmergic blackboard | PARTIAL — EI-1/2 covers underlying COC/blackboard; Spec 9 adds cross-tenant + transparency-log anchoring |

### EI Claims with No Direct Spec Claim Counterpart

| EI Claim | EI Topic | Status |
|---|---|---|
| EI-1 | forensic hash-chained COC = mission-graph edges | Covered by Spec 9 (blackboard) + Spec 2 (filesystem coordination); not a standalone spec claim |
| EI-4 | handshake anchors (branch heartbeats) | Covered by Spec 8c (zero-protocol branch integration); dependent, not standalone |
| EI-9 | lifecycle-judgment / free-choice agency split | NOT in current provisional spec — see gap note below |
| EI-10 | seven-lens refusal framework | NOT in current provisional spec — see gap note below |
| EI-11 | Decker dual-face ontology | NOT in current provisional spec — see gap note below |
| EI-12 | always-loaded skill convention | NOT in current provisional spec — see gap note below |
| EI-13 | promotion-staged folder convention | Partially covered by Spec 6 (combination) + Spec 8d (dual-regime storage gate) |

---

## Gap Summary

**4 EI claims (9, 10, 11, 12) have no corresponding spec claim text.**

These were likely planned for a non-provisional expansion. They appear in the
evidence-index with backing data paths:

- EI-9 (lifecycle/free-choice agency): `forensics/schemas/vocab/completion-choice.schema.json`
- EI-10 (seven-lens refusal): `docs/patent/_consolidated/cross-repo/faerie-vault/.../refusal-as-load-bearing-doctrine.md`
- EI-11 (Decker dual-face): `00-Publications/architecture/2026-05-25-decker-as-full-stack-atom.md`
- EI-12 (always-loaded skill): `.agents/skills/*/SKILL.md` (always_load: true)

**Action required (attorney + operator):**
- Decision: add EI-9 through EI-12 as Claims 10–13 in the provisional spec,
  OR document them as "reserved for non-provisional expansion."
- Spec 7 (zero-knowledge custody) has no EI row — add EI row pointing to
  `scripts/b2-admin/0b-b2-provision.py` as backing evidence.

---

## Canonical Source of Truth Going Forward

The provisional spec (`business/patent/_source/PATENT-PROVISIONAL-SPECIFICATION.md`)
is the filing document. The evidence-index (`docs/patent/_consolidated/CANONICAL-AND-MIRRORS.md`)
is the evidence-chain document. They serve different purposes and may have different
claim counts — that is acceptable provided this reconciliation map is kept current.

**Recommended practice:**
1. Add a `spec_claim` column to the EI table in CANONICAL-AND-MIRRORS.md §3.
2. For each EI row, note the corresponding spec claim number (or "reserved for non-provisional").
3. Re-sync after non-provisional claim drafting.

---

## Quick-Reference Lookup (both directions)

```
Spec 1  ←→  EI-6   (memory hierarchy)
Spec 2  ←→  EI-2   (stigmergic coordination)
Spec 3  ←→  EI-7   (four-layer enforcement)
Spec 4  ←→  EI-8   (shape registry)
Spec 5  ←→  EI-5   (Membench)
Spec 6  ←→  EI-13  (combination / staging; partial)
Spec 7  ←→  [none] (zero-knowledge custody; EI gap)
Spec 8  ←→  EI-3+4 (Merkle seal + branch anchors; partial)
Spec 9  ←→  EI-1+2 (COC blackboard; partial)
EI-1    ←→  Spec 9 (COC = mission-graph edges)
EI-4    ←→  Spec 8c (handshake/branch dependent)
EI-9    ←→  [none in spec] (lifecycle/free-choice; reserved)
EI-10   ←→  [none in spec] (seven-lens refusal; reserved)
EI-11   ←→  [none in spec] (Decker dual-face; reserved)
EI-12   ←→  [none in spec] (always-loaded skill; reserved)
```
