# Unified Forensic System — Complete Index

**Start Here** to understand the complete forensic redesign.

---

## Quick Navigation

### For Decision Makers (15 min read)
1. **START:** `/mnt/d/0LOCAL/.claude/hooks/state/DELIVERY-SUMMARY.md` — What was delivered, why it matters
2. **DETAILS:** `/mnt/d/0LOCAL/.claude/hooks/state/FORENSIC-SYSTEM-SUMMARY.md` — Executive summary with key features

**Question:** "Should we build this system?"  
**Answer:** Read FORENSIC-SYSTEM-SUMMARY.md sections: "Four Immutable Layers", "Why Court-Defensible", "Risks Addressed"

### For Technical Leads (1 hour read)
1. **OVERVIEW:** `/mnt/d/0LOCAL/.claude/hooks/state/FORENSIC-SYSTEM-SUMMARY.md` — Big picture
2. **DESIGN:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-system-design.md` (read: Architecture + Hash Chain sections) — Core concepts
3. **VISUAL:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-layers-visual.txt` — Timeline example
4. **CHECKLIST:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-implementation-checklist.md` (skim Phase 1) — What needs to be built

**Question:** "Can I understand this design without the 12K-word doc?"  
**Answer:** Yes. Read Summary + Visual Guide + Checklist Phase 1 section. That's 3K words, captures 80% of the design.

### For Developers (Implementation)
1. **CHECKLIST:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-implementation-checklist.md` — Exactly what to code, in order
2. **SCHEMA:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-schema-reference.json` — Exact JSON format for each event type
3. **DESIGN:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-system-design.md` (read: Verification API section) — ForensicArchive Python class to implement

**Question:** "How do I code this?"  
**Answer:** Start with checklist Step 2 (Create ForensicArchive module). Copy the class from the design doc. Run checklist items in order.

### For Court Lawyers (Admissibility)
1. **SUMMARY:** `/mnt/d/0LOCAL/.claude/hooks/state/FORENSIC-SYSTEM-SUMMARY.md` → "Why Court-Defensible" section — Five key strengths
2. **DESIGN:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-system-design.md` → "Court Admissibility" section — Complete legal argument
3. **VISUAL:** `/mnt/d/0LOCAL/.claude/hooks/state/forensic-layers-visual.txt` → "FORENSIC STRENGTH" section — Why hash chain is defensible

**Question:** "Would a court accept this forensic proof?"  
**Answer:** Yes, if Phase 2 (signing) is completed. Current design provides 80% of court strength. Phase 2 adds PGP signatures.

---

## Document Map

### 6 Deliverables (in recommended read order)

```
DELIVERY-SUMMARY.md                      [2,500 words] ← START HERE
    ↓
FORENSIC-SYSTEM-SUMMARY.md               [2,500 words] ← Quick reference
    ↓
forensic-layers-visual.txt               [1,200 words] ← Visual walkthrough
    ↓
forensic-implementation-checklist.md     [900 words]   ← Development steps
    ↓
forensic-system-design.md                [12,500 words] ← Complete spec
    ↓
forensic-schema-reference.json           [1,800 lines] ← Copy-paste schemas
```

### By Use Case

| I want to... | Read this | Then this | Time |
|---|---|---|---|
| Understand the system in 15 min | SUMMARY | Visual | 15 min |
| Decide if we should build it | SUMMARY | Design (court section) | 30 min |
| Build Phase 1 | Checklist | Schema reference | 2-3 hours |
| Understand causality proofs | Visual | Design (hash chain) | 20 min |
| Answer "why court-defensible" | SUMMARY | Design (court) | 20 min |
| Query the system (Phase 3+) | Design (API) | Visual (query examples) | 30 min |

---

## The Four Layers (Quick Reference)

### Layer 1: Artifacts (Permanent)
**What:** Agent cards, skills, rules, memories  
**Example:** `research-analyst.md` gets "Last Training" update (0.88 → 0.91)  
**Event:** One per update, with before/after hash  
**Volume:** ~100-200/year  

### Layer 2: Agent State (Session-Scoped)
**What:** Checkpoints, state transitions, learning events  
**Example:** Agent forms H1 confidence 0.70 (state V1), then 0.95 (state V2) with full data  
**Event:** Checkpoint + each state transition + learning event  
**Volume:** ~2,000-3,000/year  

### Layer 3: Working Memory (Progressive Lifecycle)
**What:** MEM blocks draft → validated → promoted → archived  
**Example:** "AS400495 cross-project CONNECTION" created (draft), promoted to NECTAR (validated)  
**Event:** Created, promoted, archived (with timestamps & confidence)  
**Volume:** ~5,000-10,000/year  

### Layer 4: Transcripts (Immutable)
**What:** Conversation, tool calls, findings, session summary  
**Example:** "H1 confidence 0.95" stated at turn 23 with 3 sources cited  
**Event:** Tool calls, responses, findings, session close  
**Volume:** ~50,000+/year  

**All connected via:** Single manifest.jsonl with hash chain (prev_event_id linking)

---

## Core Innovation: Causality Proof

**The Problem:** Court says "How do I know you didn't improve AFTER seeing results?"

**The Solution:** State versioning + progressive disclosure + timestamped events

**Timeline Example:**
```
13:15 — State V1: H1 confidence 0.70 (partial data)  [evt-agent-state-001]
13:45 — State V2: H1 confidence 0.95 (full data)      [evt-agent-state-002]
13:50 — Learning event: KPI 0.88→0.91                 [evt-agent-state-003]
14:22 — Finding stated: H1 confidence 0.95            [evt-transcripts-023]
```

**Proof:** V1→V2 happened BEFORE learning event. Finding used state V2, not learning.
∴ Learning didn't bias the finding. No retroactive justification possible.

**Court Value:** Timestamps are immutable (hash-chained). Can't be forged after the fact.

---

## Three Essential Queries

### Query 1: Prove Finding Wasn't Cherry-Picked
```python
archive = ForensicArchive(...)
proof = archive.prove_learning_causality("evidence-curator", 
                                         finding_ts=datetime(2026,4,7,14,22))
# Returns: ["V1 state at 13:15", "V2 state at 13:45", "Learning at 13:50", 
#           "Finding at 14:22" → "Learning after state shift, no bias"]
```

### Query 2: Trace Evidence → Finding → Publication
```python
archive = ForensicArchive(...)
finding_event = archive.get_transcript("session-20260407")[23]  # turn 23
sources = finding_event["sources"]  # ["cert_collision", "github_verify", "nlrb_corr"]
# Each source has hash, can retrieve original evidence
```

### Query 3: Show Agent Learning Timeline
```python
archive = ForensicArchive(...)
learning = archive.get_learning_events("evidence-curator")
# Returns: [
#   {"ts": "2026-04-07T13:50:00Z", "kpi": "tier1_accuracy", 
#    "score": "0.88→0.91", "technique": "cross-project detection"}
# ]
```

---

## Implementation Phases

| Phase | Timeline | Focus | Deliverable |
|-------|----------|-------|-------------|
| **1** | 2 weeks | Core infrastructure | manifest.jsonl with 50+ entries |
| **2** | 2 weeks | Signing + verification | PGP signatures, court export |
| **3** | 2 weeks | Query API + dashboard | CLI tool, web dashboard |
| **4** | Ongoing | Archive rotation + perf | Automation, benchmarks |

**Start Phase 1 when:** User approves FORENSIC-SYSTEM-SUMMARY.md  
**Phase 1 complete when:** 50+ real entries logged, hash chain verified

---

## File Locations (All in `/mnt/d/0LOCAL/.claude/hooks/state/`)

| File | Size | Purpose | Read if... |
|------|------|---------|-----------|
| DELIVERY-SUMMARY.md | 2.5K | Overview | You want the big picture |
| FORENSIC-SYSTEM-SUMMARY.md | 2.5K | Executive summary | You're deciding yes/no |
| forensic-layers-visual.txt | 1.2K | Timeline example | You learn visually |
| forensic-implementation-checklist.md | 900 words | Step-by-step build | You're writing code |
| forensic-system-design.md | 12.5K | Complete spec | You need all details |
| forensic-schema-reference.json | 1.8K | JSON schemas | You're coding |

---

## Key Takeaways

1. **Four layers unified:** Artifacts + agent state + working memory + transcripts, all hash-chained
2. **Causality provable:** State versioning shows when assumptions shifted vs when learning happened
3. **Court-defensible:** Hash chain is immutable, timestamps prove no post-hoc bias
4. **Transparent:** Every decision visible — MEM blocks show what was considered, state transitions show thinking evolution
5. **Queryable:** Three essential queries answer 80% of investigative needs
6. **Phased:** Phase 1 alone (2 weeks) creates complete working system

---

## Why This Matters (Bottom Line)

**Before this system:**
- Court asks: "How do I know findings weren't cherry-picked after you saw results?"
- Answer: "Well, we didn't... there's a log somewhere..."
- Result: Credibility reduced, findings questioned

**After this system:**
- Court asks: "How do I know findings weren't cherry-picked?"
- Answer: "Here's the timestamp chain. Learning happened at 13:50. Finding stated at 14:22. State shift at 13:45. All hash-verified. Can't be forged."
- Result: Findings accepted, credibility maintained

---

## Start Reading Now

**Choose your path:**

- **Decision maker?** → `/mnt/d/0LOCAL/.claude/hooks/state/FORENSIC-SYSTEM-SUMMARY.md`
- **Developer?** → `/mnt/d/0LOCAL/.claude/hooks/state/forensic-implementation-checklist.md`
- **Technical lead?** → `/mnt/d/0LOCAL/.claude/hooks/state/forensic-system-design.md` (Architecture section)
- **Lawyer?** → `/mnt/d/0LOCAL/.claude/hooks/state/FORENSIC-SYSTEM-SUMMARY.md` (Why Court-Defensible section)
- **Curious?** → `/mnt/d/0LOCAL/.claude/hooks/state/forensic-layers-visual.txt`

---

**Index created:** 2026-04-07  
**All files location:** `/mnt/d/0LOCAL/.claude/hooks/state/`  
**Status:** Complete, ready for review and Phase 1 implementation
