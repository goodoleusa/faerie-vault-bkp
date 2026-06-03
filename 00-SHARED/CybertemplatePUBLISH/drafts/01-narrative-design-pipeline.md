---
date: 2026-05-22
author: goodoleusa
related_mission: cybertemplate-publish
status: draft
imported_from: CyberOps-UNIFIED/NARRATIVE-DESIGN.md
---

# CT_VAULT Narrative Design — Investigation Publishing Pipeline

**Vault root:** `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/`
**Purpose:** Centralized evidence collection, narrative synthesis, and publication staging for the CyberTemplate investigation (H1-H5 hypothesis framework)

---

## Finding Flow Pipeline

```
Agent work (pollen-{SESSION_ID}.md)
    ↓
Memory promotion (memory-keeper → NECTAR.md)
    ↓
Crystallization (faerie → HONEY.md + vault droplets)
    ↓
Narrative synthesis (report-writer → VAULT/00-SHARED/Human-Inbox/findings/)
    ↓
Editorial review (EDITORIAL_REVIEW_CHECKLIST.md)
    ↓
Publication bundle (ipfs-publisher → IPFS + Bitcoin timestamp)
```

## Vault Zones (Authority Model)

| Zone | Purpose | Writer | Reader |
|------|---------|--------|--------|
| **00-SHARED/Agent-Outbox/** | Agent work products (drafts, bundles, analysis) | Agents | Humans (review) |
| **00-SHARED/Droplets/** | Real-time insights (immediately captured, before auto-compact) | Agents | Humans (scan for breakthroughs) |
| **00-SHARED/Human-Inbox/findings/** | Findings awaiting editorial review | Agents (via memory-keeper) | Humans (editorial gate) |
| **00-SHARED/Human-Inbox/flags/** | HIGH-priority alerts requiring immediate action | Agents | Humans (response queue) |
| **00-SHARED/Dashboards/** | Investigation state snapshots, timeline views | Agents/faerie | Humans (operational awareness) |
| **01-Memories/agents/** | Agent training, card copies, roster updates | Agents + membot | Agents (at eval phase only) |
| **01-Memories/human/** | Investigator notes, synthesis, decision rationale | Humans | Agents (context only, NECTAR-level) |
| **01-Memories/shared/** | Validated facts, HONEY candidates, crystallized knowledge | Humans (promotion) | All (reference) |
| **30-Evidence/** | FINAL PUBLICATION — approved narratives, evidence bundles, court-ready artifacts | Humans only | All (read-only archive) |

## Narrative Tiers

### Tier 1: Draft (Agent-Outbox)
```
00-SHARED/Agent-Outbox/narrative-H1-draft-20260407.md
Status: draft
Agent: documentation-engineer | data-scientist
Confidence: working
Audience: internal (agent + human review)
```

### Tier 2: Editorial Review (Human-Inbox/findings)
```
00-SHARED/Human-Inbox/findings/2026-04-07-H1-insider-access.md
Status: awaiting review
Editorial gate: EDITORIAL_REVIEW_CHECKLIST.md
Confidence: 0.95 (internal)
Audience: human editorial team
Constraints: citation discipline, Bonferroni correction disclosure, anti-assertion protocol
```

### Tier 3: Approved (30-Evidence)
```
30-Evidence/narratives/H1-insider-access-2026-04-11.md
Status: approved for publication
Editorial sign-off: checklist complete, spot-checks passed
Confidence: 0.95 (public)
Audience: external (court-ready, publication bundle)
Metadata: CID (IPFS), Bitcoin timestamp, sha256 hash chain
```

## Finding Promotion Protocol

### Step 1: Agent Deposits to Outbox
Agent writes draft finding to `00-SHARED/Agent-Outbox/finding-{id}-{date}.md`:
```markdown
---
type: finding
agent: evidence-curator
confidence: 0.78
tier: Tier 2
hypothesis: H3
status: draft
blueprint: [[Blueprints/Finding-Item.blueprint]]
---

# Federal Systems Exposed During DOGE Window

[Draft narrative with inline citations]
```

### Step 2: Memory-Keeper Promotes to Human-Inbox
At `/handoff` (faerie cycle end), memory-keeper reads pollen blocks tagged `cat=HEADLINE | FINDING`:
- Appends to `00-SHARED/Human-Inbox/findings/{date}-{slug}.md`
- Links back to agent-outbox draft
- Marks promotion in forensic log

### Step 3: Human Editorial Review
Investigator opens `00-SHARED/Human-Inbox/findings/` folder, reviews against:
- EDITORIAL_REVIEW_CHECKLIST.md (citation discipline, non-results disclosure, gates)
- Evidence manifests (file paths, sha256 verification)
- Prior narratives (consistency, no contradictions)

**Decision gates:**
- APPROVED → promote to 30-Evidence
- REVISE → comment in vault, return to agent via queue
- BLOCKED → move to 00-SHARED/Human-Inbox/blocked/ with reason

### Step 4: Publish to 30-Evidence
Human moves approved finding to `30-Evidence/narratives/H{N}-{topic}-{date}.md`:
- Generate sha256(content)
- Create COC entry (who approved, when, hash)
- Metadata: publication timestamp, IPFS CID (once published)
- Lock: read-only (agents never write here)

### Step 5: IPFS + Bitcoin Stamp
ipfs-publisher agent:
- Reads 30-Evidence/narratives/
- Generates IPFS bundle (CID)
- Creates Bitcoin OpenTimestamp proof
- Updates guardian_registry.json with CID + timestamp
- Commits to repo (publication record)

## Evidence Linking

All findings must cite evidence sources using standardized format:

```markdown
[Claim statement] (per `scripts/audit_results/evidence_file.json` entity_id ENTITY-001,
Tier 1, confidence 0.95, sha256: abc123...def789)
```

**Evidence backlink in vault:**
```markdown
00-SHARED/Agent-Outbox/evidence-trace-ENTITY-001.md
---
entity_id: ENTITY-001
file_source: scripts/audit_results/unified_evidence_H1.json
row: 1042
confidence: 0.95
tier: Tier 1
findings_citing_this: [finding-001, finding-042, finding-089]
```

This creates bidirectional traceability — finding → evidence, evidence → findings using it.

## Investigation State Snapshots

Every 6 hours (faerie cycle), create operational snapshot:

```
00-SHARED/Dashboards/investigation-state-{date-time}.md
---
type: dashboard
ts: 2026-04-07T12:30:00Z
---

## Hypothesis Status
| H | Claim | Confidence | Evidence Count | Tier 1 Count | Publication Status |
|---|-------|-----------|-----------------|--------------|-------------------|
| H1 | DOGE insider | 0.95 | 47 claims | 12 | APPROVED |
| H3 | Fed systems | 0.78 | 52 claims | 8 | APPROVED WITH CAVEAT |

## Evidence Summary
- Total entities indexed: 1,271 (H1) + 772 (H3)
- Tier 1 confirmed: 127
- Findings drafted: 15
- Findings approved: 4
- Findings published: 2

## Critical Path
- H1 publication: ready (citations complete)
- H3 publication: ready (c5isr.dev caveat documented)
- Blockers: none
```

## Blueprint Integration

Each agent deposit uses Blueprints for structured data:

**Finding-Item.blueprint:**
```
Entity: Finding
Fields:
  - claim (string, required)
  - evidence_ids (array of strings, required)
  - confidence (0.0-1.0, required)
  - tier (Tier 1/2/3, required)
  - sources (array of file paths)
  - contradiction_check (boolean)
  - editorial_status (draft | review | approved | blocked)
```

**Evidence-Trace.blueprint:**
```
Entity: Evidence
Fields:
  - entity_id (string, required)
  - source_file (path)
  - row_or_line (number)
  - tier (1/2/3)
  - confidence (0.0-1.0)
  - findings_citing (array of finding IDs)
  - coc_entry (hash reference)
```

## Publication Bundle (Final)

When ready to publish (Fri Apr 11):

```
30-Evidence/
├── narratives/
│   ├── H1-insider-access-2026-04-11.md (approved, CID: Qm..., timestamp: 123456789)
│   ├── H3-federal-exposure-2026-04-11.md (approved, CID: Qm..., timestamp: 123456789)
│   └── evidence-manifest-2026-04-11.json
├── evidence/
│   ├── unified_evidence_H1-snapshot-2026-04-11.json (758 items, hash-verified)
│   ├── unified_evidence_H3-snapshot-2026-04-11.json (412 items, hash-verified)
│   └── editorial-checklist-2026-04-11.json
└── coc/
    ├── publication-coc-2026-04-11.jsonl (chain of custody record)
    └── bitcoin-timestamp.txt (OpenTimestamps proof)

guardian_registry.json updated:
{
  "H1_cid": "Qm...",
  "H1_timestamp": 123456789,
  "H1_bitcoin_tx": "...",
  "H3_cid": "Qm...",
  "H3_timestamp": 123456789,
  "H3_bitcoin_tx": "..."
}
```

## Vault Conventions

1. **Timestamped headings** in all human-editable files (so merge conflicts are obvious)
2. **Bidirectional linking** (finding → evidence, evidence ← findings)
3. **Blueprint compliance** (every evidence item and finding uses correct blueprint)
4. **COC entries** for all promotions (who, when, hash before/after)
5. **Status fields** always up-to-date (draft → review → approved → published)
6. **No deletion** — only status transitions (publish, archive, blocked-with-reason)

---

**Adopted:** 2026-04-07
**Investigators:** CyberTemplate team
**Publication target:** Fri Apr 11 2026, noon UTC
**Repository:** goodoleusa/cybertemplate (master branch), IPFS mirror, Bitcoin-stamped
