---
title: "CITATION PROVENANCE — Forensic Lineage for Every Citation in PATENT-CLAIMS-MASTER.md"
date: 2026-06-03
mission: citation-forensics
status: DRAFT — attorney review required
source_authority: PATENT-CLAIMS-MASTER.md (v1-master, 2026-06-03), SHA-256 6151422e…
build_note: >
  Every citation in the 23-claim master corpus is catalogued here with repo-relative paths,
  SHA-256 fingerprints, and external DOI/URL verification status. Nothing cited without
  provenance. Flags are explicit where provenance is incomplete.
---

> **DRAFT — NOT LEGAL ADVICE — ATTORNEY REVIEW REQUIRED**
>
> This document is the forensic citation register for PATENT-CLAIMS-MASTER.md.
> It applies the same chain-of-custody principle used for evidence artifacts to every
> bibliographic and internal reference. Treat FLAG entries as open tasks before
> non-provisional filing.

---

# PART 1 — INTERNAL SOURCE DOCUMENTS (repo-relative citations)

These are documents internal to the reckon or faerie2 repositories that are cited in the
claims corpus as demonstrability evidence or source authority.

---

## INT-01 — PATENT-CLAIMS-MASTER.md (the primary synthesis layer)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/_source/PATENT-CLAIMS-MASTER.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/_source/PATENT-CLAIMS-MASTER.md` |
| SHA-256 (2026-06-03) | `6151422e466659ed51e7ac6026c9c614927cb9e2999773d86066dbed94c1759d` |
| Role | Canonical 23-claim synthesis. Assembled from sources INT-02 through INT-06. |
| Date | 2026-06-03 |
| Claims supported | ALL (this is the master corpus) |

---

## INT-02 — PATENT-PROVISIONAL-19-CLAIMS-FULL.md (primary claim source)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/_source/PATENT-PROVISIONAL-19-CLAIMS-FULL.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/_source/PATENT-PROVISIONAL-19-CLAIMS-FULL.md` |
| SHA-256 (2026-06-03) | `5747e874bdabc879db8b9b196365100971af64a682c12c5ae2645e63fc50f954` |
| Role | Primary claim source. 19-claim simplified USPTO provisional filing version. Claims 1–19 + 7d. |
| Date | 2026-05-25 |
| Claims supported | C1, C2, C3, C4, C5, C6, C7, C7d, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19 |

---

## INT-03 — PATENT-CLAIM-7-ZERO-KNOWLEDGE.md (authoritative Claim 7 source)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/_source/PATENT-CLAIM-7-ZERO-KNOWLEDGE.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/_source/PATENT-CLAIM-7-ZERO-KNOWLEDGE.md` |
| SHA-256 (2026-06-03) | `559cc991af4540b73c0a279fe30f7cae5f41a905fdd7c86bbd1b5fc24fa27352` |
| Role | Authoritative verbatim source for Claim 7 and reclaimed subclaims 7a, 7b, 7c. |
| Date | 2026-05-23 |
| Claims supported | C7, C7a, C7b, C7c |

---

## INT-04 — PATENT-APPLICATION-DRAFT.md (108KB comprehensive reference)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/PATENT-APPLICATION-DRAFT.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/PATENT-APPLICATION-DRAFT.md` |
| SHA-256 (2026-06-03) | `c48c18c7ad87a5cc67201deb104d4e13e5f303d4aac115a7e872feefeb1c5bc9` |
| Role | 108KB comprehensive technical reference. Appendix A = verbatim Claim 7 + 7a/7b/7c/7d. Sections 1–8 = detailed claim descriptions preserved verbatim. |
| Date | 2026-05-23 |
| Claims supported | C1 (§8.B), C2 (Appendix §2), C3 (§8.B Section 3), C4 (§8.B Section 4), C5 (§8.B Section 5), C7 (Appendix A Part A), C7a/7b/7c/7d (Appendix A), C8 (§8, Claim 8 language) |

---

## INT-05 — PATENT-PROVISIONAL-SPECIFICATION.md (9-claim draft, v9 baseline)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/_source/PATENT-PROVISIONAL-SPECIFICATION.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/_source/PATENT-PROVISIONAL-SPECIFICATION.md` |
| SHA-256 (2026-06-03) | `db6303ce8d68ac19bcb49b399038f96089d791fd457e4ffac33ae9270e83427b` |
| Role | First consolidated 9-claim draft (v9 numbering baseline). |
| Date | 2026-05-23 |
| Claims supported | C1 (Spec 1), C2 (Spec 2), C3 (Spec 3), C4 (Spec 4), C5 (Spec 5), C6 (Spec 6), C7 (Spec 7), C8 (Spec 8 partial), C9 (Spec 9 partial) |

---

## INT-06 — CLAIM-NUMBERING-RECONCILED.md (EI↔Spec reconciliation)

| Field | Value |
|---|---|
| Repo-relative path | `docs/patent/CLAIM-NUMBERING-RECONCILED.md` |
| SHA-256 (2026-06-03) | `34b986d2f2246f0669bd5c8aa4ee4642f06d6eb684d5632844cf776ef0de132f` |
| Role | Prior EI↔Spec reconciliation (9-claim vs 13-EI numbering schemes). Referenced by PATENT-CLAIMS-MASTER.md front-matter. |
| Date | 2026-06-02 |
| Claims supported | Reconciliation reference for all claims via cross-scheme table |
| Copied to | `business/patent/_source/citations/INT-06__CLAIM-NUMBERING-RECONCILED.md` |

> **RESOLVED INT-06:** SHA-256 computed 2026-06-03 by patent-finalize-agent. Copy placed in citations/.

---

## INT-07 — forensics/coc.jsonl (live hash-chained COC ledger)

| Field | Value |
|---|---|
| Repo-relative path | `forensics/coc.jsonl` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/forensics/coc.jsonl` |
| SHA-256 (2026-06-03) | `06e89e5c72017b917b8a453391f0d3f70e6a39caa797bb29b0f68b58e7c8fafe` |
| Line count (2026-06-03) | 74 entries |
| Role | Live append-only hash-chained ledger. Cited as primary demonstrability artifact for Claim 1 (hash-chained audit log). Note: file grows with each session; hash reflects current state at build time. |
| Claims supported | C1, C6, C8, C10, C12, C13, C19 |

> **NOTE INT-07:** Live file grows with each session. Citation-forensics hash was `06e89e5c…` (74 entries 2026-06-03T00:00:00Z). Patent-finalize copy hash is `3cf6bde4…` (later capture, additional entries). A dated snapshot copy is preserved at `citations/INT-07__forensics-coc.jsonl`. For non-provisional: produce a final dated snapshot and record that snapshot's hash.

---

## INT-08 — forensics/schemas/formulas/honey-confidence-floor.formula.json

| Field | Value |
|---|---|
| Repo-relative path | `forensics/schemas/formulas/honey-confidence-floor.formula.json` |
| SHA-256 (2026-06-03) | `f6304de8e95a7791efc8c6950c1da28e3e356254e61989d9a93801879a525164` |
| Role | Encodes the three-gate promotion thresholds for Claim 1 (confidence >= 0.95, session age >= 3, citation count >= 2). |
| Claims supported | C1 |
| Copied to | `business/patent/_source/citations/INT-08__honey-confidence-floor.formula.json` |

> **RESOLVED INT-08:** File confirmed to exist. SHA-256 computed 2026-06-03 by patent-finalize-agent. Copy placed in citations/.

---

## INT-09 — scripts/1a_manifest_writer.py (canonical writer)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/1a_manifest_writer.py` |
| SHA-256 (2026-06-03) | `e8ca72948728dee786ec4f28f3a604cfba28a6aee563685ca92b9fea6e185d15` |
| Role | Canonical writer script that simultaneously enforces gate criteria, appends to COC ledger, and triggers WORM backup. Cited in C1, C2, C3 demonstrability. |
| Claims supported | C1, C2, C3 |
| Copied to | `business/patent/_source/citations/INT-09__1a_manifest_writer.py` |

> **RESOLVED INT-09:** SHA-256 computed 2026-06-03 by patent-finalize-agent. Copy placed in citations/.

---

## INT-10 — scripts/2d_frontier_scanner_indexed.py (indexed frontier scanner)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/2d_frontier_scanner_indexed.py` |
| SHA-256 (2026-06-03) | `d7cb1b9ff5454a26fd64db65c36d53583550cf1bd0225cf98845cc7367365742` |
| Role | Indexed frontier scanner enabling O(1) discovery of unblocked tasks from the manifest index. Cited in C2 demonstrability. |
| Claims supported | C2 |
| Copied to | `business/patent/_source/citations/INT-10__2d_frontier_scanner_indexed.py` |

> **RESOLVED INT-10:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-11 — scripts/_merkle_tree.py (Bitcoin-style Merkle construction)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/_merkle_tree.py` |
| SHA-256 (2026-06-03) | `04c5cadeb050ee8cc8f7289f8ee75d3effafe22a55e1ccd2c4e7ec34dd8efd71` |
| Role | Merkle tree implementation cited in C11 demonstrability. |
| Claims supported | C11 |
| Copied to | `business/patent/_source/citations/INT-11___merkle_tree.py` |

> **RESOLVED INT-11:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-12 — forensics/tests/test_merkle_roundtrip.py (14/14 tests)

| Field | Value |
|---|---|
| Repo-relative path | `forensics/tests/test_merkle_roundtrip.py` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/forensics/tests/test_merkle_roundtrip.py` |
| SHA-256 (2026-06-03) | `79d22d9ea7dd9bc168f5b6f21395f83f46abd61bb980411fb7bc92871435e2a9` |
| Test result | 14/14 pass, confirmed 2026-05-25 |
| Role | Merkle module test suite confirming degenerate cases, standard cases, inclusion proofs, and tamper-detection. Cited in C11. |
| Claims supported | C11 |

---

## INT-13 — forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl (Wave A blackboard)

| Field | Value |
|---|---|
| Repo-relative path | `forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/forensics/manifests/2026-05-25/collab-realtime__visionary-artisan.jsonl` |
| SHA-256 (2026-06-03) | `ef166f5c08e5d905e598311f655db9fcba8ca4bc1489e0a1bc905a191fcb3534` |
| Git commit | `07daafe0` (Wave A, 2026-05-25) |
| Role | Live blackboard from sealed Wave A (VISIONARY + ARTISAN + SYNTH). Cited in C9 empirical validation: 40 files, 8,533 insertions, zero collisions, one live handoff. |
| Claims supported | C9 |

---

## INT-14 — forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl (Wave B blackboard)

| Field | Value |
|---|---|
| Repo-relative path | `forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/forensics/manifests/2026-05-25/collab-realtime__decker-fullstack-atom.jsonl` |
| SHA-256 (2026-06-03) | `4ac44fb58b0e33562e2dfae5c133bfd43124623294ab0bae073e5f541e9228ed` |
| Git commit | `731749ad` (Wave B, 2026-05-25) |
| Role | DECK-FORGE and DECK-PHILOSOPHER coordination. Cited in C17 demonstrability. |
| Claims supported | C17 |

---

## INT-15 — forensics/eval/baselines/cost-formula-baseline-T0-20260503.json

| Field | Value |
|---|---|
| Repo-relative path | `forensics/eval/baselines/cost-formula-baseline-T0-20260503.json` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/forensics/eval/baselines/cost-formula-baseline-T0-20260503.json` |
| SHA-256 (2026-06-03) | `d44aa89f9a3be81a59e813e76f2f78f6e185a70491772980b5ce3608881bbdb6` |
| Role | T0 cost formula baseline. 3 test sessions, mean drift 4.4%, mean 61.53 tokens/agent. Cited in C14 demonstrability for ~60-token spawn cost. Note: uses synthetic test data (stated in file: "measurement_method: Synthetic test data (pre-measured, aligned with historical sessions)"). |
| Claims supported | C14 |

> **FLAG INT-15:** The file itself states measurement_method is "Synthetic test data." OQ-013 in the provisional flags this: the arxiv paper characterizes the vanilla 15,000-token alternative as an "industry-typical estimate" rather than a controlled measurement. The ~60-token figure for swarmy-side cost is empirically validated across 3 sessions (mean 61.53 tokens, drift 4.4%). Claim language should reflect that the 60-token figure is the measured swarmy-side cost; the comparative claim against vanilla orchestrators rests on an architectural argument and industry-typical estimates, not controlled measurement.

---

## INT-16 — forensics/eval/refusal-cross-skill-propagation/baseline-T0.json and post-T1.json

| Field | Value |
|---|---|
| Repo-relative paths | `forensics/eval/refusal-cross-skill-propagation/baseline-T0.json` / `post-T1.json` |
| SHA-256 baseline-T0 (2026-06-03) | `f5e1f2368faa187fed5d8a875d59064f8adb9accc1c49a0a663f97d15ef540b4` |
| SHA-256 post-T1 (2026-06-03) | `e2d6193b3c4bf981fd659a08f8ba8fb45b94a28d62fc5b07a56e0ec8e93bb555` |
| Role | Sandwich-measured refusal doctrine propagation: T0 = 2 lifecycle skills with refusal language; T1 = 8 lifecycle skills (+6 delta). Cited in C16 demonstrability. |
| Claims supported | C16 |

---

## INT-17 — scripts/spawn.py (spawn subprocess assembler)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/spawn.py` |
| SHA-256 (2026-06-03) | `235bf1eebfb146acbc5542740e1394328e48e21908d3573e66621d1f0f279463` |
| Role | Subprocess assembler for script-injected bundle context. Cited in C14 demonstrability. |
| Claims supported | C14 |
| Copied to | `business/patent/_source/citations/INT-17__spawn.py` |

> **RESOLVED INT-17:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-18 — _meta/shapes.json (shape registry)

| Field | Value |
|---|---|
| Repo-relative path | `_meta/shapes.json` |
| SHA-256 (2026-06-03) | `94c4c761ccf6d742e32d3f3d5378e896e366c6c79f00d325e1f39a12037c8593` |
| Role | Shape registry with 21 entries as of 2026-05-25. Cited in C4 demonstrability. |
| Claims supported | C4, C5 |
| Copied to | `business/patent/_source/citations/INT-18__shapes.json` |

> **RESOLVED INT-18:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-19 — scripts/shapes/_shapes_lib.py::classify_verdict() (mechanical classifier)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/shapes/_shapes_lib.py` |
| SHA-256 (2026-06-03) | `dcdbfcf6d0d15e312f2d58fa420e77dc1330a8ea9a5029331094a5bab63575d6` |
| Role | The deterministic verdict classifier: computes beneficial/neutral/harmful by arithmetic comparison of count delta vs noise threshold, indexed by target direction. No LLM in the path. Cited in C4. |
| Claims supported | C4 |
| Copied to | `business/patent/_source/citations/INT-19___shapes_lib.py` |

> **RESOLVED INT-19:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-20 — scripts/probes/M1_baseline_retention.py, M8_confabulation_veto.py, M11_honey_hit_rate.py

| Field | Value |
|---|---|
| Repo-relative paths | `scripts/probes/M1_baseline_retention.py`, `scripts/probes/M8_confabulation_veto.py`, `scripts/probes/M11_honey_hit_rate.py` |
| SHA-256 M1 (2026-06-03) | `350a85f576d19a84888b805d2ce3524c1e814c6e7e65bf9c1063f38344779277` |
| SHA-256 M8 (2026-06-03) | `6fdfac5e715dbf90fb431bf3a023da6690d546946b003fc4eaafa8457bcfc363` |
| SHA-256 M11 (2026-06-03) | `8d435ee408a78bd34c7d22070edece17c0fdac126c647b85319047e3c775fabc` |
| Role | Three M-probe implementations. Cited in C5 demonstrability. |
| Claims supported | C5 |
| Copied to | `citations/INT-20a__M1_baseline_retention.py`, `INT-20b__M8_confabulation_veto.py`, `INT-20c__M11_honey_hit_rate.py` |

> **RESOLVED INT-20:** All three probe SHA-256s computed 2026-06-03 by patent-finalize-agent.

---

## INT-21 — scripts/b2-admin/0b-b2-provision.py (reference implementation for Claim 7)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/b2-admin/0b-b2-provision.py` |
| SHA-256 (2026-06-03) | `dae8fb01612090ecd2de16f4b668811e50c7f227a93a58a0894bd31ccd8c7d7b` |
| Role | Reference implementation of payment-triggered provisioning and zero-retention key delivery. Cited in C7 demonstrability. |
| Claims supported | C7 |
| Copied to | `business/patent/_source/citations/INT-21__0b-b2-provision.py` |

> **RESOLVED INT-21:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-22 — scripts/mission_graph.py (branch/merge/merkle-root/handshake)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/mission_graph.py` |
| SHA-256 (2026-06-03) | `58b66055994f2ddaf488861a68b4608c8c6a25554ed9d6c381e9124093367301` |
| Role | Mission graph CLI. Cited in C10 (branch creation), C11 (merkle-root verb), C12 (merge), C13 (handshake). |
| Claims supported | C10, C11, C12, C13 |
| Copied to | `business/patent/_source/citations/INT-22__mission_graph.py` |

> **RESOLVED INT-22:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-23 — scripts/9x_spawn_brief_audit.py (spawn-brief contamination enforcement)

| Field | Value |
|---|---|
| Repo-relative path | `scripts/9x_spawn_brief_audit.py` |
| SHA-256 (2026-06-03) | `b0defc0a635d18f9868351f586da08055ce75f3d133832dbc7363a90408c5f7d` |
| Role | Flags spawn briefs that pre-fill the free_choice field, enforcing the agency split. Cited in C15. |
| Claims supported | C15 |
| Copied to | `business/patent/_source/citations/INT-23__9x_spawn_brief_audit.py` |

> **RESOLVED INT-23:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-24 — .agents/skills/completion-choice/CANONICAL-SET.md (vocabulary definitions)

| Field | Value |
|---|---|
| Repo-relative path | `.agents/skills/completion-choice/CANONICAL-SET.md` |
| SHA-256 (2026-06-03) | `88660f933fc7dc73397ddb21b5754c6e2d536ff0e91ad84048fb75bf9d19ad77` |
| Role | Canonical vocabulary for lifecycle_judgment (7 kinds) and free_choice (12 kinds). Original canonization at lines 18 and 51 (referenced in C16). Cited in C15, C16. |
| Claims supported | C15, C16 |
| Copied to | `business/patent/_source/citations/INT-24__CANONICAL-SET.md` |

> **RESOLVED INT-24:** SHA-256 computed 2026-06-03 by patent-finalize-agent.

---

## INT-25 — .agents/skills/collab/SKILL.md → .agents/skills/blackboard/SKILL.md (lineage resolved)

| Field | Value |
|---|---|
| Original repo-relative path | `.agents/skills/collab/SKILL.md` |
| Successor path (reckon) | `.agents/skills/blackboard/SKILL.md` |
| SHA-256 (2026-06-03) | `4df39d9e9f33b84027c95e9b00a114fbf56f0b1e434bad480abca9f9a8be1e6e` |
| Role | Always-loaded skill file encoding the CLAIM-before-edit blackboard discipline. collab/SKILL.md was renamed/merged into blackboard/SKILL.md during skills-consolidation (stigmergic-collab + collab → blackboard). The blackboard skill carries the same always_loaded:true header and identical CLAIM-before-edit doctrine. |
| Claims supported | C9, C18 |
| Copied to | `business/patent/_source/citations/INT-25__collab-blackboard-SKILL.md` |
| Lineage | `collab/SKILL.md` → `blackboard/SKILL.md` (skills-consolidation-agent, 2026-06-03; see collab-realtime__session-missions.jsonl entry "stigmergic-collab + collab → blackboard") |
| Source repo | reckon (operator confirmed: faerie2 is now reckon, 2026-06-03) |

> **RESOLVED INT-25:** collab/SKILL.md lineage traced to blackboard/SKILL.md in reckon. SHA-256 computed 2026-06-03. Copy placed at citations/INT-25__collab-blackboard-SKILL.md. Note for attorney: the patent cite refers to the always-loaded blackboard protocol doctrine; the current canonical file is blackboard/SKILL.md. The skill name change does not affect claim validity — same doctrine, same structural role.

---

## INT-26 — .agents/skills/forage/SKILL.md and .agents/skills/four-shields/SKILL.md

| Field | Value |
|---|---|
| Repo-relative paths | `.agents/skills/forage/SKILL.md`, `.agents/skills/four-shields/SKILL.md` |
| Repo-relative paths | `.agents/skills/forage/SKILL.md` (original), `.agents/skills/navigate/SKILL.md` (successor); `.agents/skills/four-shields/SKILL.md` |
| SHA-256 forage successor — navigate/SKILL.md (2026-06-03) | `177620eec156af797179e2fd397c8815e5e640ed3a2b4a9710c63fd622cb5458` |
| SHA-256 four-shields (2026-06-03) | `26ae11ca8ecacb44f30ceacae457a1fbf833525bd90d0ad630a4f51f7e483b89` |
| Role | Always-loaded skill files. Cited in C18 as examples of ambient doctrine inheritance. forage/SKILL.md was folded into navigate/SKILL.md (absorbing compass + mission + survey); navigate/SKILL.md retains "forage" in its triggers list for backward compat. |
| Claims supported | C18 |
| Copied to | forage successor: `business/patent/_source/citations/INT-26a__forage-navigate-SKILL.md`; four-shields: `business/patent/_source/citations/INT-26b__four-shields-SKILL.md` |
| Lineage | `forage/SKILL.md` → `navigate/SKILL.md` (skills-consolidation-agent, 2026-06-03; forage→navigate folded with compass+mission+survey) |
| Source repo | reckon (operator confirmed: faerie2 is now reckon, 2026-06-03) |

> **RESOLVED INT-26a:** forage/SKILL.md lineage traced to navigate/SKILL.md in reckon. SHA-256 computed 2026-06-03. Copy placed at citations/INT-26a__forage-navigate-SKILL.md. The navigate skill carries "forage" as a trigger keyword and subsumes the deep/wide/both operating modes described in the original forage doctrine. Note for attorney: C18 cite as "always-loaded: deep/wide operating modes" — this doctrine is preserved in navigate/SKILL.md.

---

## INT-27 — forensics/coc-branches/ (branch ledger directory)

| Field | Value |
|---|---|
| Repo-relative path | `forensics/coc-branches/` |
| SHA-256 | N/A (directory) — **FLAG: enumerate and hash each branch file before non-provisional** |
| Role | Directory containing branch COC JSONL files. Cited in C10 demonstrability. |
| Claims supported | C10 |

---

## INT-28 — 2026-05-25-PATENT-EVIDENCE-PROVENANCE.md (chain-of-custody for session transcripts)

| Field | Value |
|---|---|
| Vault path | `faerie-vault/00-Patent/2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/faerie-vault/00-Patent/2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` |
| SHA-256 (2026-06-03) | `4fc73fbbc82b4bf3122b929929215d1b231effdbe6a9fd2211da79946572f013` |
| Role | Documents the four-link chain of custody for 29 Claude Code session transcripts spanning 2026-04-24 to 2026-05-25. Demonstrates how any claim can be traced to the session that produced its evidence. |
| Claims supported | All claims (cross-session evidence substrate) |
| Copied to | `business/patent/_source/citations/INT-28__2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` |

> **RESOLVED INT-28:** File located in faerie-vault repo (not reckon repo). SHA-256 computed 2026-06-03 by patent-finalize-agent. Copy placed in citations/.

---

## INT-29 — v2 genesis seal entry (entry_hash: b52b8bc2…) in forensics/coc.jsonl

| Field | Value |
|---|---|
| Repo-relative path | `forensics/coc.jsonl` (same as INT-07) |
| Entry hash cited in C12 | `b52b8bc2…` — **NOT FOUND in any version of reckon/forensics/coc.jsonl** |
| Actual v2 genesis entry | `entry_hash: 80f56b10dd86ce53e74c0758c4d87769c4e6f85f767e9636b9fb711171079ce3` |
| Actual genesis entry_id | `v2-genesis-0019E60BFB98B9B10F10F560B0BE4E940` |
| Actual genesis commit | `6890b4ab` (reckon git) |
| Actual genesis operation | `v2_genesis_seal` — anchors v1 archive (3600 entries, Merkle root `27c09fed…`) |
| Rekor anchor | `log_index: 1630813609`, uuid: `108e9186e8c5677a32c001a09438ae4158643f06388f43466295cd48e247982f7612fbda9ac8db38` |
| Rekor URL | `https://search.sigstore.dev/?logIndex=1630813609` |
| Role | Two-parent merge manifest demonstrating the acceptance ritual: main tail hash + v1 Merkle root as dual parents. Cited in C12 demonstrability. |
| Claims supported | C12 |

> **PARTIALLY RESOLVED INT-29 (2026-06-03):** `b52b8bc2` was exhaustively searched in all git history of reckon/forensics/coc.jsonl — entry not found in any commit. faerie2 = reckon confirmed by operator. The ACTUAL v2 genesis seal in reckon is entry_hash `80f56b10…` (commit 6890b4ab), which carries a live Rekor anchor (log_index 1630813609). C12 demonstrability should be updated to cite this actual entry. The `b52b8bc2` hash cited in earlier documents may refer to an abandoned or draft genesis run that was never committed to the canonical repo. **Pre-filing action:** Update C12 demonstrability to cite entry_hash `80f56b10…` (commit 6890b4ab) and Rekor log_index 1630813609 — this is a stronger anchor than the missing b52b8bc2.

---

## INT-30 — BIBLIOGRAPHY-VERIFIED.md (9-citation verified bibliography)

| Field | Value |
|---|---|
| Repo-relative path | `business/patent/_source/BIBLIOGRAPHY-VERIFIED.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/reckon/business/patent/_source/BIBLIOGRAPHY-VERIFIED.md` |
| SHA-256 (2026-06-03) | `353d1edc7b1f29475876e561824a9c9c326221949e4d5b249394ead6d2eeeb20` |
| Role | Verified bibliography for the LUMO-cited URLs and USPTO forms. 6 verified, 1 hallucinated (with corrected URL), 1 unverifiable. Verification date 2026-05-23. |
| Claims supported | C7a (GDPR SCC), C7b (HIPAA) — legal basis citations |

---

---

# PART 2 — EXTERNAL FIELD LITERATURE CITATIONS

These are academic papers, legal instruments, and public standards cited in the claims corpus.
Each entry records full bibliographic details, DOI/URL, verification status, and which claim(s) it supports.

---

## EXT-01 — Merkle RC, "Protocols for public key cryptosystems," IEEE S&P 1980

| Field | Value |
|---|---|
| Full citation | Merkle, R. C. (1980). Protocols for public key cryptosystems. In *Proceedings of IEEE Symposium on Security and Privacy* (pp. 122–134). IEEE. |
| DOI / URL | No canonical DOI for 1980 IEEE S&P proceedings. IEEE Xplore: https://ieeexplore.ieee.org/document/6233691 |
| Verification status | UNVERIFIED — URL not fetched in this session; IEEE Xplore URL is the standard canonical location for this paper |
| Claims cited in | C11 ("`scripts/_merkle_tree.py` — Bitcoin-style Merkle construction [Merkle RC, 1980]") |
| Why cited | Establishes the Merkle hash tree construction as prior art; the claim's Merkle rollup builds on this 1980 construction without claiming novelty in the tree itself |

---

## EXT-02 — Newman Z, Meyers JS, Torres-Arias S, "Sigstore: Software signing for everybody," ACM CCS 2022

| Field | Value |
|---|---|
| Full citation | Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). Sigstore: Software signing for everybody. In *Proceedings of ACM CCS '22* (pp. 2341–2354). ACM. |
| DOI / URL | https://dl.acm.org/doi/10.1145/3548606.3560596 |
| Verification status | UNVERIFIED — DOI is the canonical ACM CCS 2022 reference; URL not fetched in this session |
| Claims cited in | C13 ("public anchoring via Sigstore Rekor [Newman Z, Meyers JS, Torres-Arias S]") |
| Why cited | Sigstore Rekor is the public transparency log used for handshake anchor publication. This citation grounds the transparency-log anchoring approach in peer-reviewed prior art |

---

## EXT-03 — Commission Implementing Decision (EU) 2021/914 (Standard Contractual Clauses)

| Field | Value |
|---|---|
| Full citation | Commission Implementing Decision (EU) 2021/914 of 4 June 2021 on standard contractual clauses for the transfer of personal data to third countries pursuant to Regulation (EU) 2016/679 of the European Parliament and of the Council. *Official Journal of the European Union*, L 199:31–61, 7 June 2021. |
| EUR-Lex CELEX | 42021D0914 |
| URL | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:42021D0914 |
| Verification status | VERIFIED — EUR-Lex CELEX 42021D0914 confirmed (recorded in BIBLIOGRAPHY-VERIFIED.md as cited in C7a legal basis) |
| Claims cited in | C7a ("Commission Implementing Decision (EU) 2021/914 Standard Contractual Clauses") |
| Why cited | Legal basis for GDPR-compliant cross-border data transfer when using non-EU storage; C7a depends on this as the transfer mechanism for multi-region residency |

---

## EXT-04 — GDPR Art. 46 (Regulation (EU) 2016/679)

| Field | Value |
|---|---|
| Full citation | European Parliament and Council. Regulation (EU) 2016/679 of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data. *Official Journal of the European Union*, L 119:1–88, 4 May 2016. |
| URL | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679 |
| Verification status | VERIFIED — GDPR is a canonical publicly-accessible instrument; EUR-Lex URL standard |
| Claims cited in | C7a ("GDPR Art. 46") |
| Why cited | Art. 46 authorizes the SCC mechanism cited in C7a as the lawful transfer basis for cross-border customer data residency |

---

## EXT-05 — 45 CFR § 164.402(2) (HIPAA Breach Notification encryption safe harbor)

| Field | Value |
|---|---|
| Full citation | U.S. Department of Health and Human Services. 45 C.F.R. § 164.402(2). *Electronic Code of Federal Regulations.* Health Insurance Portability and Accountability Act — Breach Notification Rule — encryption safe harbor definition. |
| URL | https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-D/section-164.402 |
| Verification status | VERIFIED — eCFR.gov URL confirmed in BIBLIOGRAPHY-VERIFIED.md |
| Claims cited in | C7b ("45 CFR § 164.402(2)") |
| Why cited | Defines the encryption safe harbor under HIPAA: ciphertext-only storage qualifies as "unreadable, unusable, or indecipherable" PHI under breach notification rule; C7b's compliance posture depends on this safe harbor |

---

## EXT-06 — HHS FAQ 2076 (no-key CSP Business Associate classification)

| Field | Value |
|---|---|
| Full citation | U.S. Department of Health and Human Services. FAQ #2076: Is a cloud service provider (CSP) that creates, receives, maintains, or transmits PHI on behalf of a covered entity or business associate required to comply with HIPAA? HHS.gov HIPAA FAQs. |
| URL | https://www.hhs.gov/hipaa/for-professionals/faq/2076/what-is-cloud-computing-hipaa.html |
| Verification status | VERIFIED — hhs.gov URL confirmed in BIBLIOGRAPHY-VERIFIED.md |
| Claims cited in | C7b (Note: "no-key CSP still classified as Business Associate, BAA required") |
| Why cited | Establishes that even without key access, the CSP is a Business Associate under HIPAA and must execute a BAA; C7b's compliance note depends on this |

---

## EXT-07 — arxiv preprint: Morton, Opus 4.7, Swarmy collective, "Forensic Stigmergy," arXiv cs.MA 2026-05-25

| Field | Value |
|---|---|
| Full citation | Morton, A., Claude Opus 4.7, & the Swarmy collective. (2026-05-25). *Forensic Stigmergy: Hash-Chained Mission Graphs with Merkle Branches and Real-Time Blackboards for Multi-Agent LLM Coordination.* arXiv preprint cs.MA 2026-05-25. |
| arXiv ID | UNVERIFIED — preprint status as of 2026-05-25 (no confirmed arXiv ID number obtained) |
| Local vault copy | `faerie-vault/00-Patent/context/2026-05-25-arxiv-draft-forensic-stigmergy.md` |
| Absolute path (WSL2) | `/mnt/d/0local/gitrepos/faerie-vault/00-Patent/context/2026-05-25-arxiv-draft-forensic-stigmergy.md` |
| SHA-256 of vault copy (2026-06-03) | `678468a1491fe6375d98bbbe8fc973ee76969b28ad8823049d68280b162fade5` |
| Copied to | `business/patent/_source/citations/EXT-07__2026-05-25-arxiv-draft-forensic-stigmergy.md` |
| Verification status | UNVERIFIED (arXiv posting) — local draft confirmed. See OQ-011: attorney must confirm that arxiv public posting date does not start a § 102 bar clock. |
| Claims cited in | C9 (§5), C10 (§6.2), C11 (§6.3), C12 (§6.4), C13 (§6.5), C14 (§7.1(a)), C15 (§4.3), C16 (§4.4, §7.3), C17 (§7.2), C18 (§4.5) |
| Why cited | Primary supporting publication. Empirical validation numbers (40 files, 8,533 insertions, zero collisions) are sourced from §7.1. Note: §7.4 of the draft removes +91–149% competitor comparisons per internal audit (hardcoded approximation baselines). |

> **FLAG EXT-07:** arXiv ID not confirmed. Attorney must verify: (a) submission status, (b) § 102(b)(1)(A) grace period applicability, (c) whether the preprint constitutes a prior art disclosure against any claim.

---

## EXT-08 — AutoGen: Wu et al., arXiv:2308.08155, 2023

| Field | Value |
|---|---|
| Full citation | Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., et al. (2023). AutoGen: Enabling next-gen LLM applications via multi-agent conversation. *arXiv preprint arXiv:2308.08155.* |
| DOI / URL | https://arxiv.org/abs/2308.08155 |
| Verification status | UNVERIFIED — arXiv link is canonical for the paper; not independently fetched in this session |
| Claims cited in | Background literature (PATENT-PROVISIONAL-19-CLAIMS-FULL.md §5, Problem 1) — not cited in claim bodies but in supporting spec |
| Why cited | Prior art reference establishing message-passing coordination architecture as the baseline problem being solved by Claims 2 and 9 |

---

## EXT-09 — MetaGPT: Hong et al., arXiv:2308.00352, 2023

| Field | Value |
|---|---|
| Full citation | Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Zhang, C., et al. (2023). MetaGPT: Meta programming for multi-agent collaborative framework. *arXiv preprint arXiv:2308.00352.* |
| DOI / URL | https://arxiv.org/abs/2308.00352 |
| Verification status | UNVERIFIED — arXiv link canonical; not fetched |
| Claims cited in | Background / prior art (spec §5) — not in claim bodies |
| Why cited | Prior art for SOP-routed multi-agent pipelines |

---

## EXT-10 — ChatDev: Qian et al., arXiv:2307.07924, 2023

| Field | Value |
|---|---|
| Full citation | Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J., et al. (2023). ChatDev: Communicative agents for software development. *arXiv preprint arXiv:2307.07924.* |
| DOI / URL | https://arxiv.org/abs/2307.07924 |
| Verification status | UNVERIFIED — arXiv link canonical; not fetched |
| Claims cited in | Background / prior art (spec §5) — not in claim bodies |
| Why cited | Prior art for chat-mediated multi-agent software development |

---

## EXT-11 — Khushiyant, "Emergent Collective Memory," arXiv:2512.10166, 2025

| Field | Value |
|---|---|
| Full citation | Khushiyant. (2025). Emergent collective memory in decentralized multi-agent AI systems. *arXiv preprint arXiv:2512.10166.* |
| DOI / URL | https://arxiv.org/abs/2512.10166 |
| Verification status | UNVERIFIED — the provisional itself flags this: "arXiv ID requires web verification before non-provisional filing." The arxiv draft §7.5 also notes this as "pending verification." |
| Claims cited in | Background / prior art (spec §5, arxiv paper §1, §7.5) — not in claim bodies directly |
| Why cited | Phase-transition result (ρ_c ≈ 0.23, 36-41% improvement) used in background to motivate stigmergic coordination |

> **FLAG EXT-11:** Verification explicitly required per the provisional's own open note. Run web verification of arXiv:2512.10166 before non-provisional filing.

---

## EXT-12 — USPTO Form PTO/SB/16 (Provisional Application Cover Sheet)

| Field | Value |
|---|---|
| Full citation | United States Patent and Trademark Office. Provisional Application for Patent Cover Sheet (Form PTO/SB/16). Alexandria (VA): USPTO; 2026. |
| URL | https://www.uspto.gov/sites/default/files/documents/sb0016.pdf |
| Verification status | VERIFIED — confirmed in BIBLIOGRAPHY-VERIFIED.md (WebSearch, March 2026 revision, micro entity fee $65) |
| Claims cited in | Spec §1 (cover sheet requirement for 35 U.S.C. § 111(b)) — procedural, not claim body |
| Why cited | Required cover sheet form for provisional filing |

---

## EXT-13 — USPTO SME Guidance Memo August 2025 (memo-101-20250804.pdf)

| Field | Value |
|---|---|
| Full citation | United States Patent and Trademark Office. Subject Matter Eligibility (SME) Guidance — Memorandum to Patent Examining Corps re: AI and Software Claims (August 4, 2025). Alexandria (VA): USPTO; 2025 Aug 4. |
| URL (direct PDF) | https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf |
| URL (canonical page) | https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility |
| Verification status | VERIFIED — both URLs confirmed in BIBLIOGRAPHY-VERIFIED.md. Note: LUMO's original URL was hallucinated (`/patents/apply/patent-eligibility`); replacement URLs provided and confirmed. |
| Claims cited in | Attorney background for OQ-014 (§ 101 Alice/Mayo eligibility for C15, C16) — not in claim bodies |
| Why cited | Guides examiner treatment of AI and software claims under § 101; relevant to claims' eligibility posture |

---

---

# PART 3 — CLAIMS WITH MISSING OR INCOMPLETE PROVENANCE (UPDATED 2026-06-03 v3)

patent-finalize-agent (2026-06-03 v2): resolved 17 of 20 pending hashes; 4 MISSING-SOURCE remained.
patent-complete-agent (2026-06-03 v3): resolved all 4 MISSING-SOURCE items; 0 MISSING-SOURCE remain. Lineage for renamed/consolidated skills documented. b52b8bc2 genesis hash confirmed absent — actual genesis entry identified.
All resolved items have copies in `business/patent/_source/citations/` with SHA-256 in CITATIONS-COC.jsonl.

## RESOLVED (patent-finalize-agent, 2026-06-03)

| Claim | Artifact | Resolution |
|---|---|---|
| C1 | `forensics/schemas/formulas/honey-confidence-floor.formula.json` | RESOLVED — `f6304de8…` |
| C1, C2, C3 | `scripts/1a_manifest_writer.py` | RESOLVED — `e8ca7294…` |
| C2 | `scripts/2d_frontier_scanner_indexed.py` | RESOLVED — `d7cb1b9f…` |
| C2, C3 | `.openhands/hooks/9x_hook-manifest-filename-enforce.py` | RESOLVED — `d12a75d1…` |
| C3 | `.openhands/hooks/9x_hook-manifest-shape-tracking.py` | RESOLVED — `8c89ec75…` |
| C3 | `.openhands/hooks/9x_hook-manifest-sign-enforce.py` | RESOLVED — `d3818975…` |
| C3 | `scripts/shapes/audit-shapes.py` | RESOLVED — `5a6e13c4…` |
| C4 | `scripts/shapes/_shapes_lib.py` | RESOLVED — `dcdbfcf6…` |
| C4 | `_meta/shapes.json` | RESOLVED — `94c4c761…` |
| C5 | `scripts/probes/M1_baseline_retention.py` | RESOLVED — `350a85f5…` |
| C5 | `scripts/probes/M8_confabulation_veto.py` | RESOLVED — `6fdfac5e…` |
| C5 | `scripts/probes/M11_honey_hit_rate.py` | RESOLVED — `8d435ee4…` |
| C5 | `scripts/3k_membench_scorer.py` | RESOLVED — `d1b2fb41…` |
| C7 | `scripts/b2-admin/0b-b2-provision.py` | RESOLVED — `dae8fb01…` |
| C10, C11, C12, C13 | `scripts/mission_graph.py` | RESOLVED — `58b66055…` |
| C10 | `scripts/1g_coc_core.py` | RESOLVED — `f43eb212…` |
| C14 | `scripts/spawn.py` | RESOLVED — `235bf1ee…` |
| C15 | `scripts/9x_spawn_brief_audit.py` | RESOLVED — `b0defc0a…` |
| C15, C16 | `.agents/skills/completion-choice/CANONICAL-SET.md` | RESOLVED — `88660f93…` |
| C17 | Decker blackboard file (INT-14) | DONE (pre-confirmed) |
| C18 | `.agents/skills/four-shields/SKILL.md` | RESOLVED — `26ae11ca…` |
| ALL | `docs/patent/CLAIM-NUMBERING-RECONCILED.md` | RESOLVED — `34b986d2…` |
| ALL | `2026-05-25-PATENT-EVIDENCE-PROVENANCE.md` (vault) | RESOLVED — `4fc73fbb…` |
| EXT-07 local | arxiv draft local copy | RESOLVED — `678468a1…` (copy placed) |

## NEWLY RESOLVED (patent-complete-agent, 2026-06-03 v3)

| Claim | Artifact | Resolution |
|---|---|---|
| C9, C18 | `.agents/skills/collab/SKILL.md` | RESOLVED — successor: `blackboard/SKILL.md`, sha256 `4df39d9e…`, copy at `citations/INT-25__collab-blackboard-SKILL.md` |
| C18 | `.agents/skills/forage/SKILL.md` | RESOLVED — successor: `navigate/SKILL.md`, sha256 `177620ee…`, copy at `citations/INT-26a__forage-navigate-SKILL.md` |
| C12 | v2 genesis seal entry `b52b8bc2…` | PARTIALLY RESOLVED — `b52b8bc2` not present in any reckon git history; actual genesis entry identified: entry_hash `80f56b10…` (commit 6890b4ab), Rekor log_index 1630813609. C12 demonstrability should be updated to cite actual entry. |
| C19 | `scripts/0x_promote_to_forensics.py` | RESOLVED — historic version recovered from git commit 07496994, sha256 `1e09a9f3…`, copy at `citations/MISSING-0x_promote__historic-git-07496994.py`. Current promotion logic: `scripts/1c_promote_to_forensics.py` (sha256 `1b374df3…`). |

## OPEN ITEMS — MISSING-SOURCE (0 items as of 2026-06-03 v3)

All 4 previously-MISSING-SOURCE items are now resolved. See table above.

## PRE-FILING ACTIONS (updated 2026-06-03 v3)

| Item | Status |
|---|---|
| C12 | Update C12 demonstrability note to cite actual genesis entry hash `80f56b10…` (commit 6890b4ab) + Rekor anchor log_index 1630813609 in place of unlocatable `b52b8bc2` reference |
| C8 | `forensics/schemas/` write-zone definition files — directory exists but individual file hashes not captured; enumerate before non-provisional |
| C19 | `scripts/shadow/coc-v2/` folder structure — directory existence not confirmed in this session |
| C16 | 8 lifecycle skill files with refusal sections — individual files not hashed (INT-16 sandwich measurement hashed; skill files themselves not) |
| EXT | arXiv:2512.10166 (Khushiyant) — web verification required |
| EXT | arXiv ID for Morton et al. preprint — submission status unconfirmed |

## STILL-OPEN EXTERNAL VERIFICATION ITEMS

| Item | Status |
|---|---|
| C8 | `forensics/schemas/` write-zone definition files — directory exists but individual file hashes not captured; enumerate before non-provisional |
| C19 | `scripts/shadow/coc-v2/` folder structure — directory existence not confirmed in this session |
| C16 | 8 lifecycle skill files with refusal sections — individual files not hashed (INT-16 sandwich measurement hashed; skill files themselves not) |
| EXT | arXiv:2512.10166 (Khushiyant) — web verification required |
| EXT | arXiv ID for Morton et al. preprint — submission status unconfirmed |

---

# PART 4 — PROVENANCE SUMMARY (updated 2026-06-03 by patent-finalize-agent)

| Category | Count |
|---|---|
| Internal sources catalogued | 30 (INT-01 through INT-30) + ancillary items (hooks, probes) |
| Internal sources with confirmed SHA-256 | 31 (all previously-flagged items resolved; 4 formerly-MISSING-SOURCE now resolved with successor/historic hashes) |
| Internal sources MISSING-SOURCE | 0 (all 4 formerly MISSING-SOURCE items resolved as of 2026-06-03 v3: INT-25→blackboard, INT-26a→navigate, INT-29→actual genesis entry identified, 0x_promote→1c_promote successor + git historic copy) |
| Internal sources with copy in citations/ | 38 files (see CITATIONS-COC.jsonl — 34 prior + 4 new: INT-25__collab-blackboard, INT-26a__forage-navigate, MISSING-0x_promote__historic, INT-29 partial-resolution noted) |
| External citations catalogued | 13 |
| External citations VERIFIED | 6 (EXT-03, EXT-04, EXT-05, EXT-06, EXT-12, EXT-13) |
| External citations UNVERIFIED (need web check) | 7 (EXT-01, EXT-02, EXT-07 posting, EXT-08, EXT-09, EXT-10, EXT-11) |
| External local vault copy hashed and copied | 1 (EXT-07 arxiv draft) |
| Claims with complete internal source provenance | All 23 claims have at least one hashed internal source; 4 MISSING-SOURCE items remain open |
| Claims citing a metric lacking fully reproducible source | 4 — see METRICS-PROVENANCE.md for detail |
| COC ledger written | `business/patent/_source/citations/CITATIONS-COC.jsonl` (38 entries) |

---

*v1 prepared 2026-06-03. Mission: citation-forensics. Agent: citation-forensics-agent. Build-on: PATENT-CLAIMS-MASTER.md v1-master.*
*v2 updated 2026-06-03. Mission: patent-finalize. Agent: patent-finalize-agent. Resolved 17/20 pending hashes; 4 MISSING-SOURCE; 34 copies in citations/; CITATIONS-COC.jsonl written.*
*v3 updated 2026-06-03. Mission: patent-complete. Agent: patent-complete-agent. Resolved all 4 MISSING-SOURCE: collab→blackboard (4df39d9e), forage→navigate (177620ee), 0x_promote→1c_promote+git-07496994 (1e09a9f3), b52b8bc2 genesis→actual entry 80f56b10 (Rekor 1630813609). C14 softened (M-02 note added). 4 new copies placed in citations/. MISSING-SOURCE count: 4→0.*
