---
type: documentation
status: active
title: "faerie2 Architecture Diagrams"
tags: [architecture, system-design, faerie2, diagrams, excalidraw]
created: 2026-04-26
updated: 2026-04-26
---

# faerie2 Architecture Diagrams

Professional Excalidraw diagrams documenting the f(0) agent orchestration platform. All diagrams are available as:
- **SVG** (embedded in .md files, web/print compatible)
- **Excalidraw JSON** (editable in Excalidraw.com)
- **Markdown with frontmatter** (vault-ready)

---

## Diagram 1: f(0) Architecture Overview

**File**: `forensics/diagrams/diagram-1-f0-architecture.excalidraw`

**Description**: Comprehensive view of the f(0) system flow:
- Main context dispatches tasks
- Bundle pre-computation reduces per-spawn cost from 10,000 to 50 tokens (99.5% reduction)
- 3,700+ agents spawned across project lifetime
- Forensic immutability layer captures all artifacts

**Key Metrics**:
- Input token cost: **99.5% reduction** (10K → 50)
- Stigmergic return: **80-char dashboard_line** (compressed manifest)
- Piston waves: **W1/W2/W3 autonomous** (no manual pauses)

**Use case**: Investor decks, architecture reviews, context efficiency proof.

---

## Diagram 2: Piston Wave Execution Model

**File**: `forensics/diagrams/diagram-2-piston-waves.excalidraw`

**Description**: Temporal breakdown of the three-wave execution model:

| Wave | Name | Duration | Context Fill | Key Behavior |
|------|------|----------|---------------|--------------|
| W1 | LIFTOFF | ~5 min | 0% | Max parallel spawns, hit 5-min cache TTL |
| W2 | CRUISE | ~10 min | 25-50% | Single-spawn, dashboard compression |
| W3 | INSERTION | ~∞ | 100% | Deep synthesis, background agents, async results |

**Autonomous Dispatch**: No manual pauses between stages. Stage separation driven by `dashboard_line` compression and token pressure signals (altimeter).

**Use case**: Understanding orchestration flow, explaining why context fill doesn't block execution.

---

## Diagram 3: Forensic Immutability (3-Store Architecture)

**File**: `forensics/diagrams/diagram-3-forensic-immutability.excalidraw`

**Description**: Three-store chain ensuring artifact immutability and auditability:

**Store 1: {repo}/forensics/ (Canonical)**
- System of record: git-tracked, immutable append-only
- HMAC-SHA256 chaining per COC entry
- COC.jsonl contains forensic proof-in-place
- Deletion-proof at database layer

**Store 2: Vault/Obsidian (Derivative)**
- Human-readable styling and cross-linking
- Hash-tracked: before/after snapshots
- Linked to forensics/ via hash chain
- Edit metadata captured in COC

**Store 3: S3/B2 WORM (Immutable Backup)**
- Write-once, read-many (zero deletion)
- Cryptographic proof of integrity
- External custody (immune to repo accidents)
- Compliance-ready (legal discovery proof)

**Hash Chain Protocol**:
```
Agent writes artifact → hash_tracker snapshots (before) → 
  forensics/ entry + HMAC → vault mutation hook captures hash → 
  COC entry links all three → S3/B2 WORM ingests snapshot
```

**Use case**: Compliance audits, explaining forensic integrity to legal/stakeholders.

---

## Diagram 4: Stigmergic Queue (Mission-Based Coordination)

**File**: `forensics/diagrams/diagram-4-stigmergic-queue.excalidraw`

**Description**: Filesystem-only coordination without SendMessage or central message bus:

**Flow**:
1. Agent 1 completes task, writes manifest to `forensics/manifests/{ts}_{type}_{task_id}_{agent}_{sid8}.json`
2. Manifest includes field: `next_task_queued = { task_id: cost-reduction-input-delta, investigation_label: mission-cost-instrumentation }`
3. Agent 2 (or spawned follow-up) discovers predecessor via: `grep -r "_{task_id}_" forensics/manifests/`
4. Agent 2 reads manifest, injects findings into next task without context cost

**Key Advantage**: Zero coordination overhead. Filesystem IS the message queue. Follow-up discovery happens at negligible cost via grep + jq.

**Example Mission**: 
```
mission-cost-instrumentation-20260425/
  ├─ task-1: cost-reduction-analysis (Agent 1)
  ├─ task-2: input-delta-deep-dive (Agent 2, discovered via task_id)
  └─ task-3: synthesize-findings (Agent 3, discovered via task_id)
```

**Use case**: Explaining how agents self-organize without a message bus.

---

## Diagram 5: Memory System ROI (Observation → Crystallization)

**File**: `forensics/diagrams/diagram-5-memory-roi.excalidraw`

**Description**: Circular lifecycle of memory tiers, from raw observation to universal crystallization:

**Stages**:

1. **Observation** (Agent work)
   - Raw findings, bug discoveries, pattern recognition
   - Specific to current session/task

2. **Pollen MEM** (Session-scoped)
   - Tier 1-2: Memory blocks in `{repo}/.claude/memory/pollen-{SID}.md`
   - Lightweight FOONotes, session observations
   - Not yet curated

3. **NECTAR** (Evidence-grounded)
   - Tier 3: Promoted HIGH entries at /handoff
   - Artifact hash-linked
   - Forensic audit trail present
   - Promotes from session → multi-session

4. **Droplets** (Vault, live-updated)
   - Published to `$CT_VAULT/00-SHARED/Droplets/`
   - Human-readable with evidence links
   - Cross-project accessible
   - Real-time updates possible

5. **HONEY** (Universal, gauntlet)
   - Tier 4: Cross-project patterns
   - Gauntlet certification passed
   - Long-lived, highly-curated
   - Examples: agent routing heuristics, common bugs, best practices

**Quality Gates & ROI**:
- **Tier 1-2** (Pollen): Zero curation overhead, session-local
- **Tier 3** (NECTAR): Light filtering, hash-proof required
- **Tier 4** (HONEY): Full audit, cross-validation, 2.85× measured ROI

**Circular Flow**: Better memory → Better future work → Better observations → Improved memory

**Measured Impact**: 2.85× efficiency ratio across 3,700+ spawns (baseline: T+1 with forensic proof)

**Use case**: Justifying memory infrastructure investment, explaining how agents get smarter over time.

---

## Export & Deployment Locations

### Repository
- Source Excalidraw: `/mnt/d/0local/gitrepos/faerie2/forensics/diagrams/diagram-*.excalidraw`
- Documentation: `/mnt/d/0local/gitrepos/faerie2/docs/DIAGRAM-*.md`
- This index: `/mnt/d/0local/gitrepos/faerie2/docs/ARCHITECTURE-DIAGRAMS.md`

### Vault (Obsidian)
- `/mnt/d/0LOCAL/ObsidianVault/00-SHARED/Diagrams/faerie2/Diagram-*.md`
- All files include SVG embeds + frontmatter for easy cross-referencing

### Editing

To edit any diagram:
1. Download the `.excalidraw` file from `forensics/diagrams/`
2. Open in [Excalidraw.com](https://excalidraw.com) or Excalidraw desktop app
3. Make changes
4. Export as SVG + Excalidraw JSON
5. Re-run `scripts/excalidraw_to_svg.py` to regenerate .md files

---

## Design Decisions

### Color Palette
- **Blue** (#3b82f6): Main context, flows, core processes
- **Green** (#10b981): Observational, foundational, healthy
- **Orange** (#f97316): Agents, active work, energy
- **Purple** (#8b5cf6): Forensics, memory systems, crystallization
- **Red** (#dc2626): Critical infrastructure (WORM, HONEY), high-stakes
- **Gray** (#f3f4f6): Detail boxes, annotations

### Typography
- **Titles**: 20px, sans-serif bold
- **Section headers**: 12px, sans-serif bold
- **Labels**: 10-11px, sans-serif
- **Monospace** (file paths): 9px, source code pro

### Layout
- **Mobile-first**, but diagrams are desktop-optimized (>800px wide)
- **Whitespace**: Generous (20px padding on all sides)
- **Grouping**: Related elements clustered with same color family
- **Arrows**: Directional flow always left-to-right or top-to-bottom

---

## Integration with Other Documentation

- **ARCHITECTURE-MODEL-ROUTING.md**: Cross-referenced from Diagram 4 (stigmergic queue)
- **ARCHITECTURE_QUEUE_CLAIMING.md**: Cross-referenced from Diagram 2 (piston waves)
- **SPAWN-BOILERPLATE.md**: Cross-referenced from Diagram 1 (bundle pre-computation)
- **FORENSIC-INTEGRITY.md**: Cross-referenced from Diagram 3 (3-store architecture)
- **PHILOSOPHY.md**: Cross-referenced from Diagram 5 (memory ROI circular logic)

---

**Generated**: 2026-04-26  
**Agent**: frontend-design (SVG export) + excalidraw-generator (JSON)  
**Status**: Active · Ready for investor/documentation use
