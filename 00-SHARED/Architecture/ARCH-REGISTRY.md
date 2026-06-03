---
type: registry
title: Architecture Documentation Registry
created: 2026-05-04
updated: 2026-05-04T143000Z
parent: ../Architecture.md
doc_hash: "sha256:auto"
---

> [↑ Architecture](../Architecture.md) · [⌂ Home](../../HOME.md)

# Architecture Documentation Registry

**Last updated:** 2026-05-04T143000Z  
**Total documents:** 3 active | 0 archived | 0 pending review

---

## Active Documents

| ID | Title | Status | Created | Version | Next Review | Confidence |
|----|-------|--------|---------|---------|-------------|------------|
| **ARCH-001** | Stigmergic Spawn Protocol | **ACTIVE** | 2026-05-04 | 1.0 | 2026-06-04 | 0.88 |
| **ARCH-002** | Swarmy OH Lifecycle × Hooks — Strategic Boundary Matrix | **ACTIVE** | 2026-05-23 | 1.0 | 2026-06-23 | 0.85 |
| **ARCH-003** | Four-Bulkheads — Defense-in-Depth Cyber Stack for Forensic AI Systems | **ACTIVE** | 2026-05-23 | 1.0 | 2026-06-23 | 0.82 |

---

## Document Statuses

### ARCH-003: Four-Bulkheads — Defense-in-Depth Cyber Stack for Forensic AI Systems

**Path:** `00-SHARED/Architecture/ARCH-003-FOUR-BULKHEADS-CYBER-DEFENSE.md`

**Status:** ACTIVE

**Version:** 1.0 (released 2026-05-23)

**Confidence:** 0.82 (architectural design + citation framework; external URL verification pending via enterprise-patent-foundation polished-deliverables agent)

**Scope:**
- The cyber defense-in-depth stack protecting the forensic chain from adversarial input
- Sister doctrine to ARCH-002 (lifecycle × hooks) and to `four-shields` skill (discipline enforcement)
- 4-layer stack: 🏰 PERIMETER → 🧹 PURIFICATION → 🩺 DETECTION → 🪞 QUARANTINE
- Supports the reproducibility + court-discovery readiness claims of the forensic-coc-v2 architecture
- Captured as Patent Claim 8 in the `enterprise-patent-foundation` expedition

**Dependencies:**
- `forensics/coc.jsonl` + `forensics/schemas/shape/` (the chain + schemas that the bulkheads defend)
- `.agents/skills/four-bulkheads/SKILL.md` (knowledge skill mirroring this doctrine)
- `.agents/skills/script-quarantine/SKILL.md` (Bulkhead 4 partial implementation)
- `scripts/quarantine/` (Bulkhead 4 storage)
- `[FORENSIC-COC-V2-MERKLE-ROLLUP-REKOR]` (the chain being defended)
- `[STIGMERGY-FOR-AGENT-TEAMS]` (the coordination substrate)
- `[FOR-SKEPTICS-zero-confabulation]` (forensic-integrity measurement)

**Last Validation:** 2026-05-23 (doctrine + citation framework; implementation in tactical follow-up charters)

**Next Review:** 2026-06-23 (30-day confidence gate)

**Citation:** Use as `[ARCH-003]` in inline references or frontmatter citations

**External-URL verification:** PENDING via `enterprise-patent-foundation/polished-deliverables` agent's URL-check pass (24 external sources marked ⚠️ until verified).

---

### ARCH-002: Swarmy OH Lifecycle × Hooks — Strategic Boundary Matrix

**Path:** `00-SHARED/Architecture/ARCH-002-LIFECYCLE-HOOKS-MATRIX.md`

**Status:** ACTIVE

**Version:** 1.0 (released 2026-05-23)

**Confidence:** 0.85 (derived from precious-faerie-salvage 5-lane analysis + matrix v2 in `scripts/_recovery/2026-05-23-precious-faerie/SCRIPTS-FEATURE-MATRIX.md`)

**Scope:**
- Boundary × hook × shield matrix for the swarmy-on-OH runtime
- Mapping of 10 retired stubs in top-level `hooks/` to their canonical 4-shields role
- Lean keeper list: 11 hooks total (3 🛡 + 3 ⛓ + 5 🪞; 🧠 served by skills)
- The cheaper-earlier law + how to add a new hook (lifecycle-first design)

**Dependencies:**
- `.agents/skills/four-shields/SKILL.md` — the 4-layer enforcement pattern
- `forensics/charters/active/2026-05-23Z__charter__swarmy-oh-runtime-bootstrap__goodoleusa.json`
- `scripts/_recovery/2026-05-23-precious-faerie/` — salvage source for cannibalization patterns

**Last Validation:** 2026-05-23 (matrix v2 in matrix doc, sister-lane B confirmed substrate green)

**Next Review:** 2026-06-23 (30-day confidence gate)

**Citation:** Use as `[ARCH-002]` in inline references or frontmatter citations

**Verbatim mirror:** `deploy/README.md` § "ARCH-002 — Lifecycle × Hooks Matrix" (swarmy repo)

---

### ARCH-001: Stigmergic Spawn Protocol — F(0) Preservation & Emergence Design

**Path:** `00-SHARED/Architecture/ARCH-001-STIGMERGIC-SPAWN-PROTOCOL.md`

**Status:** ACTIVE (locked for production use)

**Version:** 1.0 (released 2026-05-04)

**Confidence:** 0.88 (validated via 4 N-edge agent completions + manifest testing)

**Scope:** 
- F(0) burden reduction mechanism (main context overhead ≤100 tokens)
- Lean prompt architecture (1,882 chars per agent via path references)
- Stigmergic coordination protocol (mission field routing + compass bearings)
- In-flight discovery mechanism (agents scan 7-day manifest index, claim work)
- Emergence metrics validation (100% discovery rate, bearing balance, mission field coverage)

**Dependencies:** 
- Charter scope constraint enforcement
- Manifest-index-{date}.jsonl (7-day work history)
- HONEY.md (cached global principles)
- Agent card reputation system

**Last Validation:** 2026-05-04 (4/4 agents tested, 0 failures)

**Next Review:** 2026-06-04 (30-day confidence gate)

**Citation:** Use as `[ARCH-001]` in inline references or frontmatter citations

---

## Crystallization Lifecycle

Documents follow this lifecycle:

```
DRAFT
  ├─ Author active development
  ├─ Reviews: 0/2 (peer + metrics)
  └─ Gate: Passes peer review
      ↓
ACTIVE
  ├─ Locked for production reference
  ├─ Used in agent bundles + spawn templates
  ├─ Cited in frontmatter of dependent docs
  └─ Monitoring: Monthly confidence gate (≥0.75 required)
      ├─ ✓ Passes → remains ACTIVE
      └─ ✗ Fails → escalates to REVIEW
          ↓
ARCHIVED
  ├─ Superseded by newer version or intentionally deprecated
  ├─ Kept for historical reference only
  ├─ Version link points to successor
  └─ Frozen: no further updates
```

**Promotion Rules:**

- **DRAFT → ACTIVE:** 
  - Peer review approval (≥1 reviewer)
  - Metric validation (≥2 sessions with ≥0.85 confidence)
  - Change log entry in forensics/doc-crystallization-log.jsonl
  - Frontmatter updated: `status: active`, `promoted_ts: ISO8601`

- **ACTIVE → ARCHIVED:**
  - New version released OR intentional deprecation
  - Successor documented in `superseded_by` field
  - Change log entry with rationale
  - Frontmatter updated: `status: archived`, `archived_ts: ISO8601`, `successor: ARCH-XXX`

**Monitoring:** Monthly confidence audits run `9x_arch_doc_validator.py` to recompute confidence scores based on usage metrics + citation density + downstream impact.

---

## Creating New Architecture Documents

**Numbering scheme:** `ARCH-NNN-{TITLE}.md` where NNN = zero-padded sequence (001, 002, 003, ...).

**Frontmatter template:**

```yaml
---
type: system-architecture
title: {Document Title}
created: {YYYY-MM-DD}
updated: {ISO8601}
status: draft|active|archived
version: 1.0
promotion_date: null  # filled on ACTIVE promotion
next_review: {YYYY-MM-DD}  # 30 days from promoted_ts
confidence: 0.00  # initially unset; computed after metric validation
tags: [architecture, ...]
parent: ../Architecture.md
doc_hash: "sha256:auto"
coc_ref: "forensics/doc-crystallization-log.jsonl"
metric_sources: [
  "~/.claude/hooks/state/system-eval.json",
  "forensics/performance-gauges.json",
  "forensics/manifests/{YYYY-MM-DD}/"
]
superseded_by: null  # ARCH-NNN if superseded
---
```

**Validation checklist before submitting for ACTIVE promotion:**

- [ ] Document is self-contained (can be read standalone)
- [ ] Diagrams present for complex flows (Mermaid preferred)
- [ ] Real eval metrics cited inline (not placeholders)
- [ ] Frontmatter `metric_sources` links to actual files in forensics/
- [ ] COC entry created in forensics/doc-crystallization-log.jsonl
- [ ] Peer review approval recorded
- [ ] Confidence score computed (formula: Σ(session_passes) / Σ(total_sessions) for sessions where doc was actively cited)

---

## Backward Compatibility

Old documents (pre-ARCH-001) not yet numbered:

- `docs/12-ARCHITECTURE.md` (project repo) — mirrors ARCH-001 narrative but will be updated as new ARCH-* docs ship
- `~/.claude/CLAUDE.md` — operational rules (not numbered; persistent reference)

Once ARCH-002 ships, will update `docs/00-NAVIGATION.md` to route to ARCH-* registry.

---

## References

- **Crystallization mechanism:** `forensics/doc-crystallization-log.jsonl` (immutable COC log)
- **Confidence validator:** `scripts/9x_arch_doc_validator.py` (monthly gate)
- **Metric bridge:** `canonical-emergence-metrics.md` (faerie-vault/00-SHARED/Hive/)
- **Citation index:** `forensics/arch-citation-index.jsonl` (tracks which agents/docs cite each ARCH-*)
