# 📚 Documentation Governance — Single Source of Truth + Cascade

**Breadcrumb:** [[00-DASHBOARD]] > [[08-documentation-governance]]

> **Principle:** One canonical vault doc sources all downstream work. Repo docs are sanitized summaries. Droplets are ephemeral insights. No proliferation.

---

## 🗂️ The Documentation Cascade

```
┌─────────────────────────────────────────────────────────────┐
│ 🍯 CANONICAL VAULT DOC (Deepest, Fullest Context)          │
│ Location: /mnt/d/0LOCAL/CT_VAULT/{date}/{canonical-topic}  │
│ Scope: Complete technical specification, design, examples   │
│ Audience: Agents (for discovery), operators (for detail)    │
│ Example: 07-work-hierarchy-codex.md (full hierarchy+rules)  │
│ Permissions: Edit only when major revisions needed          │
│ Format: Markdown with wikilinks, breadcrumbs, tables        │
│ Synchronization: Identical copy in faerie-vault             │
│ Source of truth: YES (canonical)                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    Render (sanitize)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 📄 REPO DOC (External-Facing Summary)                       │
│ Location: {repo}/docs/ or {repo}/ARCHITECTURE.md            │
│ Scope: Key concepts only, no exhaustive detail, user-ready  │
│ Audience: External stakeholders, GitHub readers             │
│ Example: faerie2/docs/MISSION-GRAPH-OVERVIEW.md             │
│ Permissions: Regenerate from vault when vault changes       │
│ Format: Markdown, simpler narrative flow                    │
│ Synchronization: Generated (derived artifact)               │
│ Source of truth: NO (always regenerated from vault)         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    Update (feedback)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 💧 DROPLETS (Ephemeral Insights)                            │
│ Location: /mnt/d/0LOCAL/CT_VAULT/00-SHARED/Droplets/       │
│ Scope: AHA moments, inspiration, pre-reasoning              │
│ Audience: Session-to-session memory preservation            │
│ Example: "Investigation clustering prevents queue amnesia"  │
│ Permissions: Write freely, no review needed                 │
│ Format: Bullet points, raw observations                     │
│ Synchronization: Not required (ephemeral)                   │
│ Source of truth: NO (inspirational only)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Canonical Vault Documents (System of Record)

These are THE authoritative documents. All other docs derive from these. Do not create variations.

| Canonical Doc | Topic | Last Updated | Lock Status |
|---|---|---|---|
| `07-work-hierarchy-codex.md` | Terminology, hierarchy, anti-creep | 2026-04-28 | ✅ Canonical |
| `06-investigation-id-governance.md` | Investigation lifecycle, validation | 2026-04-28 | ✅ Canonical |
| `05-mcp-server-architecture.md` | MCP server design, latency SLA | (next) | ✅ Planned |
| `04-forensic-governance.md` | Write permissions, COC, signing | (next) | ✅ Planned |
| `03-settings-sync-strategy.md` | Global/project settings balance | (next) | ✅ Planned |
| `02-compass-navigation.md` | Compass DAG, phase gates, routing | (next) | ✅ Planned |
| `01-f0-orchestration.md` | Context burden, piston waves, f(0) | (next) | ✅ Planned |

**Key rule:** Each canonical doc has:
- **One topic only** (no bundling unrelated topics)
- **Breadcrumb navigation** (shows hierarchy and relation to other docs)
- **Wikilinks** to related canonical docs and droplets
- **Version timestamp** (tracks when last canonicalized)
- **Lock status** (✅ = canonical, updates only on major revisions)

---

## 📄 Derived Repo Docs (External-Facing)

These are REGENERATED from canonical vault docs. They are sanitized, condensed, user-friendly summaries. **Do NOT edit these directly.** Always edit the canonical vault doc, then regenerate.

**Regeneration workflow:**

```
1. Agent finds vault doc needs external exposure
2. Reads canonical vault doc (full context)
3. Extracts: title + summary + key points + links
4. Removes: internal details, COC notes, system dynamics
5. Writes to {repo}/docs/{topic}-summary.md
6. Links back to vault for deeper reading
```

**Example derivations:**

| Canonical | Repo Doc | Sanitize Notes |
|---|---|---|
| `07-work-hierarchy-codex.md` | `faerie2/docs/WORK-HIERARCHY.md` | Remove system-dynamics details; keep hierarchy |
| `06-investigation-id-governance.md` | `faerie2/docs/INVESTIGATIONS.md` | Remove validation registry internals; highlight status flow |
| `05-mcp-server-architecture.md` | `faerie2/docs/MCP-SERVER.md` | Remove deployment scripts; keep architecture |

**Repo doc properties:**
- Location: `/docs/` subfolder of main repo (not `.claude/`)
- Naming: `{TOPIC}-{summary-suffix}.md` (e.g., WORK-HIERARCHY, INVESTIGATIONS)
- Format: Simple markdown, no wikilinks (links use full URLs for GitHub)
- Freshness: Regenerated whenever canonical vault doc changes
- Audience: External users, CI/CD docs, onboarding materials
- Source of truth: NOT canonical (always references vault for deep-dive)

---

## 💧 Droplets (Ephemeral Insights)

These are FREE-FORM, UNREVIEWED observations that survive session compaction. They are NOT authoritative and do NOT replace canonical docs.

**Droplet properties:**
- **Location:** `$CT_VAULT/00-SHARED/Droplets/YYYY-MM-DD-HHMMSS_insight.md`
- **Timestamp:** Automatic (captures when insight was recorded)
- **Format:** Raw bullet points, narrative, AHA moments
- **Review:** None required; write freely
- **Lifecycle:** Persist across sessions (preserved in droplets file)
- **Use case:** "Investigation clustering prevents queue amnesia" → later becomes section in codex
- **Authority:** Inspirational only; no system reliance on droplet content

**When to write a droplet:**
- ✅ You discover a pattern that's NOT yet in the codex
- ✅ You catch yourself thinking "this would be good to remember"
- ✅ You notice a drift risk that should be flagged later
- ✅ You have an AHA about the system's design
- ❌ Do NOT write droplets to replace canonical docs
- ❌ Do NOT use droplets as instruction material (use canonical docs)

**Droplet graduation:**
If a droplet becomes widely useful or prevents repeated drift, it graduates:
1. **Captured in session:** Agents write droplets freely
2. **Compaction survival:** Droplets included in preserved memory
3. **Pattern recognition:** Main notices droplet appearing in 2+ sessions
4. **Canonicalization:** Droplet content merged into appropriate canonical doc
5. **Vault integration:** Canonical doc updated, droplet archived

---

## 🚫 Anti-Proliferation Rules (Enforcement)

**Problem:** Agents create "helpful" docs → 20 docs exist → no one knows which is canonical → drift.

**Solution: System-enforced discipline.**

| Violation | Detection | Consequence |
|-----------|-----------|-------------|
| **Repo doc created without canonical source** | PreToolUse hook checks: does vault canonical exist? | Block write; remind agent to create vault doc first |
| **Canonical doc edited for minor fixes** | PostToolUse hook: version bump required | Require timestamp update + changelog entry |
| **Droplet content referenced as truth** | Code review: grep for "Droplet says..." | Flag as opinion, not authority |
| **Duplicate canonical docs** | Prescan: grep for investigation_label duplication | Reject spawn; consolidate into single doc |
| **Repo doc out of sync with vault** | Daily audit: hash-compare vault ↔ repo summaries | Flag for regeneration |

**Enforcement hooks:**
- `PreToolUse` on `Write` to `/docs/`: Verify canonical source exists
- `PostToolUse` on `Write` to vault canonical: Trigger repo doc regeneration
- `Prescan`: Check for duplicate investigation_labels before spawn

---

## 📚 Canonical Vault Reading Order (Onboarding)

When joining the system, agents read canonical docs in this order:

1. **[START HERE] Work Hierarchy Codex** (`07-work-hierarchy-codex.md`)
   - What is mission/phase/task/artifact?
   - What are subject matter vs. system dynamics tasks?
   - How to avoid mission creep

2. **Investigation ID Governance** (`06-investigation-id-governance.md`)
   - How investigations earn status
   - When to spawn vs. continue existing mission
   - Cross-repo discovery protocol

3. **Compass Navigation Protocol** (CLAUDE.md mth00101)
   - How to read mission graph
   - How to follow compass bearings
   - How to route follow-up work

4. **f(0) Orchestration** (CLAUDE.md core concepts)
   - Context burden and piston waves
   - Why main overhead must stay near zero

5. **[INFRASTRUCTURE] MCP Server Architecture** (if deploying)
   - How to host MCP server
   - Latency SLA and caching
   - Client calling patterns

---

## 🔄 Canonical Doc Update Protocol

**When:** Vault doc becomes stale or new pattern emerges

**Steps:**
1. Identify canonical doc that needs update
2. Draft changes in a droplet first (test the idea)
3. If droplet proves useful in 2+ sessions, proceed
4. Edit canonical doc:
   - Update version timestamp (YYYY-MM-DD HH:MM UTC)
   - Add changelog entry (what changed, why)
   - Re-sync identical copy to both vaults
5. Trigger repo doc regeneration
6. Post summary of change to session handoff (NECTAR)

**Example changelog entry:**
```
**Version:** 2026-04-28 14:22 UTC (added subject-matter vs. system-dynamics distinction)
  - Reason: Discovered agents were treating infrastructure work as domain missions
  - Added: Section 3.2 "Two Task Classes"
  - Related droplet: "Investigation clustering prevents queue amnesia"
```

---

## 📋 Documentation Checklist (Pre-Spawn)

Before spawning agents to work on docs:

- [ ] Is this a canonical vault doc (system of record)?
- [ ] Does it belong with existing canonical docs or is it NEW?
- [ ] Have I checked for duplicates (grep investigation_label)?
- [ ] Is this a subject-matter mission or sys-documentation task?
- [ ] If subject-matter: does it need a separate repo doc summary?
- [ ] Are all wikilinks using vault doc titles (both vaults)?
- [ ] Does it have breadcrumb navigation?
- [ ] Will agents find this via standard onboarding order?

---

## 🎯 Current Canonical Docs (Audit)

**Status:** 07 and 06 completed. 05, 04, 03, 02, 01 planned as system-dynamics work.

```
Canonical Status:
├─ ✅ 07-work-hierarchy-codex.md (LOCKED)
├─ ✅ 06-investigation-id-governance.md (LOCKED)
├─ 🔄 05-mcp-server-architecture.md (IN PROGRESS)
├─ 🔄 04-forensic-governance.md (IN PROGRESS)
├─ 🔄 03-settings-sync-strategy.md (IN PROGRESS)
├─ 🔄 02-compass-navigation.md (REFERENCED from CLAUDE.md)
└─ 🔄 01-f0-orchestration.md (REFERENCED from CLAUDE.md)

Repo Doc Status:
├─ ✅ faerie2/docs/WORK-HIERARCHY.md (derived from 07)
├─ ✅ faerie2/docs/INVESTIGATIONS.md (derived from 06)
├─ ⏳ faerie2/docs/MCP-SERVER.md (waiting for 05)
└─ ⏳ faerie2/docs/ARCHITECTURE-OVERVIEW.md (landing page)

Droplets Status:
├─ 💧 "Investigation clustering prevents queue amnesia" (2026-04-25)
├─ 💧 "Phase gates are orthogonal to phases" (2026-04-26)
└─ 💧 (more as session progresses)
```

---

## 🔗 References

- [[07-work-hierarchy-codex]] — Master codex (START HERE)
- [[06-investigation-id-governance]] — Investigation lifecycle
- CLAUDE.md mth00101 — Compass Navigation Protocol
- CLAUDE.md (core) — f(0), piston waves, bundle emission

---

**Last Updated:** 2026-04-28 14:30 UTC  
**Status:** SYSTEM GOVERNANCE — All agents must follow this cascade  
**Related:** [[00-DASHBOARD]], [[07-work-hierarchy-codex]]
