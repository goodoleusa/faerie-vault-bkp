---
type: index
status: active
created: 2026-04-21
tags: [forensics, index, coc]
up: README.md
prev: forensic-system-design.md
next: CANONICAL-WRITE-LOCATIONS.md
---

> [↑ Readme](README.md) · [← Forensic System Design](forensic-system-design.md) · [→ Canonical Write Locations](CANONICAL-WRITE-LOCATIONS.md) · [⌂ Home](../../README.md)

# Forensic System Index — Quick Navigation

**Date:** 2026-04-07  
**Purpose:** One-page reference to all forensic system documentation  
**Audience:** Everyone (agents, developers, legal teams)  

---

## Documents in This Collection

### 1. **Forensic System Design** (`forensic-system-design.md`)
   - **What it is:** The complete architecture and technical specification
   - **Sections:**
     - Three-store model (evidence, vault, cloud)
     - COC chain structure and entry types
     - Integration with faerie phases (genesis → export)
     - Investigation folder structure
     - Enforcement & verification procedures
     - Court admissibility checklist
   - **Read when:** You need deep technical understanding
   - **Length:** ~600 lines | ~12K tokens

### 2. **Forensic System Summary** (`forensic-system-summary.md`)
   - **What it is:** 1-page executive summary (this document's sibling)
   - **Sections:**
     - What it does (purpose and properties)
     - Core components table
     - Three-store model visual
     - Hash chain explanation
     - Forensic integrity properties
     - Use cases (before court, during discovery, after investigation)
     - Key rules (non-negotiable)
     - Implementation timeline
   - **Read when:** You need the 30-second overview
   - **Length:** ~250 lines | ~4K tokens

### 3. **Forensic Layers Visual** (`forensic-layers-visual.txt`)
   - **What it is:** ASCII diagrams and flow charts
   - **Sections:**
     - Layer architecture (1-6: evidence → cloud)
     - Information flow (start → export)
     - Read/write permissions matrix
     - Hash chain visual example
     - Court admissibility flow
   - **Read when:** You want to see the system at a glance
   - **Length:** ~300 lines | ~5K tokens

### 4. **Forensic Implementation Checklist** (`forensic-implementation-checklist.md`)
   - **What it is:** Step-by-step hands-on procedure
   - **Sections:**
     - Phase 0: Pre-flight setup
     - Phase 1: Genesis (baseline snapshot)
     - Phase 2: Ingest (add evidence)
     - Phase 3: Analysis (agents produce findings)
     - Phase 4: Validation (promote to NECTAR)
     - Phase 5: Crystallization (integrate knowledge)
     - Phase 6: Export (prepare for court)
     - Verification checklist
     - Troubleshooting
   - **Read when:** You're implementing COC for a new investigation
   - **Length:** ~500 lines | ~10K tokens

### 5. **Forensic Schema Reference** (`forensic-schema-reference.json`)
   - **What it is:** JSON schema definitions for all data types
   - **Sections:**
     - COC entry schemas (all 11 types)
     - Manifest file entry schema
     - Manifest schema (genesis, rawdata, evidence)
     - Reasoning entry schema
     - Examples for each type
   - **Read when:** You're building tools or validating data
   - **Length:** ~400 lines | ~8K tokens

### 6. **Canonical Write Locations** (`CANONICAL-WRITE-LOCATIONS.md`)
   - **What it is:** Routing guide for all file writes
   - **Sections:**
     - Core principle (one writer per file)
     - Canonical locations by type
     - Write routing decision tree
     - Anti-patterns and correct alternatives
     - Migration checklist
     - Subagent write restrictions
     - Verification checklist
   - **Read when:** You need to know where to write something
   - **Length:** ~350 lines | ~6K tokens

### 7. **This Document** (`FORENSIC-SYSTEM-INDEX.md`)
   - **What it is:** Navigation and quick reference
   - **Purpose:** Help you find the right document for your needs

---

## Quick Reference by Use Case

### I need to understand the entire system
1. Start: **Forensic System Summary** (5 min)
2. Then: **Forensic Layers Visual** (5 min)
3. Then: **Forensic System Design** (30 min)

### I'm implementing a new investigation
1. Start: **Forensic System Summary** (understand why)
2. Then: **Forensic Implementation Checklist** (follow steps)
3. Reference: **Forensic Schema Reference** (validate JSON)

### I'm building tools or validation scripts
1. Start: **Forensic Schema Reference** (data structures)
2. Reference: **Canonical Write Locations** (routing)
3. Reference: **Forensic System Design** section 6 (enforcement)

### I need to explain this to a lawyer or court
1. Use: **Forensic System Summary** + **Forensic Layers Visual** (visuals)
2. Deep dive: **Forensic System Design** section 8 (admissibility)
3. Checklist: **Forensic Implementation Checklist** sections "Verification" (proof)

### I'm debugging a COC issue
1. Reference: **Forensic Implementation Checklist** section "Troubleshooting"
2. Reference: **Canonical Write Locations** (routing verification)
3. Reference: **Forensic System Design** section 9 (recovery procedures)

---

## Key Concepts (Glossary)

| Term | Definition | Document |
|---|---|---|
| **COC** | Chain of Custody — immutable log of every forensic event | Forensic System Design, Summary |
| **Entry** | Single record in COC (type, actor, action, data, hashes) | Forensic Schema Reference |
| **Hash chain** | Each COC entry depends on previous (SHA256) — unbreakable | Layers Visual, Design |
| **Genesis** | Baseline snapshot of all raw evidence at time zero | Design, Implementation |
| **Ingest phase** | Period when new evidence is added; each phase creates manifest | Implementation |
| **Manifest** | Versioned inventory of files + hashes (genesis, rawdata, evidence) | Design, Schema |
| **NECTAR** | Validated findings (append-only narrative) | Summary, Canonical Write |
| **HONEY** | Crystallized facts (compressed, contextualized, durable) | Summary, Canonical Write |
| **Reasoning log** | Agent analysis steps (inputs → outputs); enables replayability | Design, Schema |
| **Export bundle** | Court-ready package (all COC + evidence + signed + B2 WORM) | Implementation, Design |
| **Vault** | Human-readable sync mirror (not canonical, Syncthing-distributed) | Layers Visual, Design |
| **WORM** | Write-Once-Read-Many cloud storage (B2, immutable, permanent) | Summary, Design |

---

## Navigation Map

```
YOU ARE HERE
    │
    ├─→ New investigation?
    │   └─→ "Forensic Implementation Checklist"
    │
    ├─→ Need overview?
    │   └─→ "Forensic System Summary" + "Forensic Layers Visual"
    │
    ├─→ Where should I write X?
    │   └─→ "Canonical Write Locations"
    │
    ├─→ Building tools?
    │   └─→ "Forensic Schema Reference"
    │
    ├─→ Technical deep dive?
    │   └─→ "Forensic System Design"
    │
    └─→ Explaining to a lawyer?
        └─→ "Forensic System Summary" (30 sec)
        └─→ "Forensic Layers Visual" (5 min)
        └─→ "Forensic System Design" section 8 (admissibility)
```

---

## Key Files to Know

### Canonical Locations

| Purpose | Location | Type | Immutable? |
|---------|----------|------|-----------|
| COC entries | `{repo}/forensics/coc.jsonl` | JSON-L | Append-only |
| Audit log | `{repo}/forensics/audit-log.md` | Markdown | Append-only |
| Manifests | `{repo}/forensics/manifests/` | JSON | Versioned (immutable) |
| Evidence export | `{repo}/forensics/exports/` | .tar.gz | Yes (signed + B2 WORM) |
| Validated findings | `~/.claude/memory/NECTAR.md` | Markdown | Append-only |
| Durable knowledge | `~/.claude/memory/HONEY.md` | Markdown | Crystallized (compressed) |
| Agent reasoning | `~/.claude/memory/investigations/{id}/reasoning.jsonl` | JSON-L | Append-only |

---

## Document Metadata

| Document | Lines | Tokens | Format | Status |
|---|---|---|---|---|
| forensic-system-design.md | 600 | 12K | Markdown | APPROVED |
| forensic-system-summary.md | 250 | 4K | Markdown | APPROVED |
| forensic-layers-visual.txt | 300 | 5K | ASCII art | APPROVED |
| forensic-implementation-checklist.md | 500 | 10K | Markdown + code | APPROVED |
| forensic-schema-reference.json | 400 | 8K | JSON schema | APPROVED |
| CANONICAL-WRITE-LOCATIONS.md | 350 | 6K | Markdown | APPROVED |
| FORENSIC-SYSTEM-INDEX.md | this file | ~3K | Markdown | APPROVED |

**Total:** ~2,750 lines | ~48K tokens (fits in HONEY crystallized form)

---

## Sync Locations

All documents exist in TWO places:

### Primary: Git (System of Record)
```
{repo}/docs/design/
├── forensic-system-design.md
├── forensic-system-summary.md
├── forensic-layers-visual.txt
├── forensic-implementation-checklist.md
├── forensic-schema-reference.json
├── CANONICAL-WRITE-LOCATIONS.md
└── FORENSIC-SYSTEM-INDEX.md
```

### Mirror: Vault (Human Visibility)
```
$CT_VAULT/00-SHARED/Design-Narratives/
├── forensic-system-design.md
├── forensic-system-summary.md
├── forensic-layers-visual.txt
├── forensic-implementation-checklist.md
├── forensic-schema-reference.json
├── CANONICAL-WRITE-LOCATIONS.md
└── FORENSIC-SYSTEM-INDEX.md
```

**Sync method:** Git commits automatically → vault sync via Syncthing (LAN, ~5 sec propagation)

---

## Version History

| Date | Changes | Author |
|---|---|---|
| 2026-04-07 | Initial creation: 7-doc collection | faerie2 core |
| TBD | Revisions based on first investigation | TBD |

---

## How to Use This as a Seed

When onboarding a new agent or person to the investigation:

1. **Give them this index** (2 min read)
2. **Direct to the summary** (5 min read)
3. **Show the layer visual** (5 min study)
4. **Point to implementation checklist** (reference during work)
5. **Link to schema reference** (tool builders only)

**Total onboarding: ~15 minutes for understanding**

---

## Questions?

- **"How do I set up COC for a new investigation?"**
  → See Forensic Implementation Checklist, Phase 0

- **"Where do I write X?"**
  → See Canonical Write Locations, Write Routing Decision Tree

- **"Why are we doing this?"**
  → See Forensic System Summary, section "What It Does" + "Use Cases"

- **"Can we use this evidence in court?"**
  → See Forensic System Design, section 8 "Court Admissibility Checklist"

- **"What if something breaks?"**
  → See Forensic Implementation Checklist, section "Troubleshooting"

---

**Document Status:** PUBLISHED | APPROVED  
**Last Updated:** 2026-04-07  
**Maintained by:** faerie2 core  
**Contact:** See project ARCHITECTURE.md
