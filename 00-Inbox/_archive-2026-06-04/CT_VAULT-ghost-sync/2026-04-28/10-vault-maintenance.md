# 🔨 Vault Maintenance — Anti-Creep & Crystallization

**Breadcrumb:** [[00-DASHBOARD]] > [[10-vault-maintenance]]

> **Mission:** Keep the vault crystalline, focused, current. Prevent folder bloat and documentation creep.

---

## 🚨 The Creep Problem

**Symptom:**
```
Today:   5 canonical docs → manageable, coherent
Week:   20 docs, 3 folders → still readable
Month: 100+ docs, 8 folders → "What should I read first?"
Year:  500+ docs, chaos → vault becomes a junkyard
```

**Root cause:** Every good idea becomes a new doc. No consolidation discipline. Vault grows outward instead of inward.

**Fix:** **Crystallization through consolidation.**

---

## 💎 The Crystallization Principle

Instead of:
```
Vault grows → more folders → more complexity → harder to find truth
```

Do:
```
Vault grows → consolidate → stronger crystal → easier to find truth
```

**Metric: Doc density per concept.**
- Bad: "10 docs about phases" scattered across the vault
- Good: "1 canonical phase section in codex" with wikilinks to related docs

---

## 🗑️ Consolidation Rules (Pre-Spawn & Post-Session)

### Rule 1: No Duplicate Topics
**Before creating a new doc:**
1. Search vault: `grep -r "investigation_label" CT_VAULT/2026-04-28/*.md | sort`
2. Check: does a doc with this topic already exist?
3. If YES → Edit existing doc (add wikilink, merge content)
4. If NO → Create new canonical doc only if it unblocks 2+ missions

**Enforcement:** PreToolUse hook on Write to `/CT_VAULT/` blocks duplicate investigation_labels.

### Rule 2: Merge Related Docs
**When creating doc N+1:**
1. Read docs N and N-1
2. Ask: Can these topics live in ONE doc?
3. If YES → Merge under section headings with wikilinks
4. If NO → Ensure wikilinks connect them strongly

**Example:**
```
❌ WRONG: Separate docs
  - "Phase Routing Rules"
  - "Compass Navigation"
  - "Bearing Semantics"

✅ RIGHT: One canonical doc with sections + wikilinks
  07-work-hierarchy-codex.md
    └─ Section 5: "Compass Bearing Semantics"
       └─ Wikilinks to [[06-investigation-id-governance]] for phase gates
```

### Rule 3: Archive Old Session Folders
**Weekly maintenance:**
1. Today's date: `2026-04-28/` (current, no archival)
2. Previous dates: `2026-04-27/`, `2026-04-26/` → Move to `Archive/` after 1 week
3. Keep in main view: Only the CURRENT day's canonical docs
4. Result: Vault surface shows only today's reality

**Structure:**
```
CT_VAULT/
├── 2026-04-28/                    (TODAY — visible, current)
│   ├── 00-DASHBOARD.md            (refresh daily)
│   ├── 07-work-hierarchy-codex.md (canonical)
│   ├── 06-investigation-id.md     (canonical)
│   └── ...
│
└── Archive/
    ├── 2026-04-27/                (Previous day, archived)
    ├── 2026-04-26/
    └── ...
```

### Rule 4: Dashboard = Home
**The 00-DASHBOARD.md is THE entry point.** It reflects current reality:
- Active investigations (with status)
- Open edges in mission graph
- System health snapshot
- What to read next (prioritized)

If someone says "what's the state of faerie?", the answer is: Read the dashboard.

---

## 🧹 Anti-Creep Enforcement (Hooks)

### Hook 1: PreToolUse on Write to `/CT_VAULT/`
```bash
# Check for duplicate investigation_labels
jq -r '.investigation_label' CT_VAULT/*/*.md 2>/dev/null | sort | uniq -d | while read label; do
  COUNT=$(grep -r "investigation_label.*$label" CT_VAULT/*/md | wc -l)
  if [ $COUNT -gt 1 ]; then
    echo "❌ Duplicate investigation_label '$label' found in $COUNT docs. Consolidate before writing."
    exit 1
  fi
done
```

### Hook 2: PostToolUse on Write to Canonical Doc
```bash
# Trigger: recount wikilinks, check for orphaned docs
python3 scripts/vault_health_audit.py --check-orphans --check-cycles
```

### Hook 3: Weekly Archival Job
```bash
# Move docs older than 7 days to Archive/
find CT_VAULT -maxdepth 1 -type d -mtime +7 -not -name "00-SHARED" -not -name "Archive" | while read dir; do
  mv "$dir" CT_VAULT/Archive/
  echo "📦 Archived $dir"
done
```

---

## 📋 Pre-Doc Creation Checklist

Before spawning to create ANY new vault doc, check:

- [ ] **Duplicate check:** Does a doc with this topic exist? (grep -r investigation_label)
- [ ] **Merge possibility:** Can this be merged into an existing section + wikilink?
- [ ] **Necessity:** Will this unblock 2+ missions or fix critical infrastructure gap?
- [ ] **Atomicity:** Is this topic large enough to deserve its own doc (≥500 words)?
- [ ] **Navigation:** Will readers find this from 00-DASHBOARD within 3 hops?
- [ ] **Wikilinks:** What existing docs does this reference (backwards + forwards)?
- [ ] **Concept tags:** What #tags does this introduce/consolidate?

**If any "NO":** Merge into existing doc instead. Do NOT create.

---

## 📊 Dashboard Refresh Protocol (Daily)

Every session, update 00-DASHBOARD.md to reflect current state:

```markdown
---
# 🧭 Dashboard of All Dashboards — 2026-04-28 [SESSION#]

> **Status:** [Current piston wave: W1/W2/W3]
> **Active Investigations:** [[investigation-1]], [[investigation-2]], [[investigation-3]]
> **Critical Blocker:** [If any]

## 📊 System Health Snapshot
| Metric | Status | Change |
|--------|--------|--------|
| Active Investigations | 3 | (was 2) |
| Canonical Docs | 9 | (was 8) |
| Consolidated Topics | 15 | (was 14) |
| Orphaned Docs | 0 | ✅ (was 1) |

## 🎯 What to Read First (Today)
1. [[07-work-hierarchy-codex]] — if new to system
2. [[06-investigation-id-governance]] — if need investigation status
3. [[09-vault-architecture]] — if maintaining vault

## 🔗 Wikilink Map (Today's Connections)
[Auto-generated from grep of wikilinks]

---
```

**Refresh rules:**
- ✅ Update every session
- ✅ Reflect current investigation status (from mission graph)
- ✅ Update "Critical Blocker" if any
- ✅ Auto-count canonical docs, orphans, topics
- ❌ Don't accumulate historical notes (archive them)

---

## 🧬 Consolidation Workflow

**When you notice doc N and doc N+1 have overlapping content:**

1. **Read both docs** — understand scope
2. **Identify overlap** — which sections are duplicate?
3. **Plan merge** — will they fit in one doc?
4. **Execute merge:**
   - Keep the MORE CANONICAL/FOUNDATIONAL doc
   - Merge content from other doc into sections
   - Add wikilinks at merge point
   - Delete the OTHER doc
5. **Update related docs** — any wikilinks pointing to deleted doc? → Redirect to new location
6. **Write to manifest** — log consolidation decision:
   ```json
   {
     "action": "consolidate",
     "docs_merged": ["old-doc-A", "old-doc-B"],
     "result": "merged-into-canonical-doc",
     "reason": "duplicate investigation_label coverage"
   }
   ```

**Example:**
```
Before:
  - 02-compass-navigation.md (detailed routing logic)
  - 02b-bearing-routing.md (specialized bearing rules)
  
After:
  - 02-compass-navigation.md (expanded with bearing section)
  - 02b-bearing-routing.md (DELETED, redirects to 02 section 5.2)
```

---

## 🧹 Monthly Audit (Anti-Creep Inspection)

**First of every month, run:**

```bash
#!/bin/bash
# Vault health audit

echo "=== VAULT HEALTH AUDIT ==="

# 1. Count docs
COUNT=$(find CT_VAULT/2026-04-28 -name "*.md" | wc -l)
echo "Canonical docs: $COUNT"

# 2. Find orphans (docs with no wikilinks TO them)
echo "Orphaned docs (no backlinks):"
for doc in CT_VAULT/2026-04-28/*.md; do
  BACKLINKS=$(grep -r "$(basename $doc .md | sed 's/-/ /g')" CT_VAULT/2026-04-28/*.md | grep -v "^$doc:" | wc -l)
  if [ $BACKLINKS -eq 0 ]; then
    echo "  - $doc"
  fi
done

# 3. Find cycles (A→B→A)
echo "Cyclic wikilinks:"
python3 scripts/vault_graph_checker.py --find-cycles

# 4. Check tag consistency
echo "Tag usage:"
grep -rh "^**Tags:**" CT_VAULT/2026-04-28/*.md | sort | uniq -c | sort -rn

# 5. Count wikilinks per doc
echo "Wikilink density:"
for doc in CT_VAULT/2026-04-28/*.md; do
  LINKS=$(grep -o "\[\[.*\]\]" "$doc" | wc -l)
  echo "  - $(basename $doc): $LINKS links"
done
```

**Fix any issues found:**
- Orphans → Integrate via wikilink from related doc
- Cycles → Resolve by clarifying dependency direction
- Tag inconsistency → Standardize across docs
- Low backlinks → Merge doc into parent

---

## 📦 Archival Strategy (Folder Hygiene)

**Keep main view clean by archiving old sessions:**

```
# Schedule: Weekly
# Job: Move session folders older than 7 days to Archive/

CT_VAULT/
├── 2026-04-28/              ✅ Keep (today)
├── 2026-04-27/              ⏳ Archive after 7 days
├── 2026-04-26/              📦 Archived
└── Archive/
    ├── 2026-04-26/
    ├── 2026-04-25/
    └── ...
```

**Archive does NOT delete. It preserves historical docs for deep-dive but hides them from main view.**

---

## 🎯 Vault Metrics (Health Dashboard)

Track these metrics monthly to detect creep:

| Metric | Target | Alarm |
|--------|--------|-------|
| **Docs in current session folder** | ≤20 | >30 |
| **Avg wikilinks per doc** | 3-5 | <1 or >8 |
| **Orphaned docs** | 0 | >2 |
| **Concept tag reuse** | 1 tag = 2-3 docs | Tags only in 1 doc |
| **Backlink coverage** | 90%+ docs linked | <50% |
| **Doc readability** | Reachable in ≤3 hops | >5 hops |

---

## 🚀 Consolidation Roadmap

| Phase | Milestone | Frequency |
|---|---|---|
| **Phase 1: Prevent** | Duplicate check hook + pre-creation checklist | Every spawn |
| **Phase 2: Merge** | Consolidate related docs when overlap detected | Weekly |
| **Phase 3: Archive** | Move old session folders to Archive/ | Weekly |
| **Phase 4: Audit** | Monthly health check + tag standardization | Monthly |
| **Phase 5: Evict** | Delete docs with 0 backlinks (after merge attempt) | Monthly |

---

## 💡 The Crystallization Goal

**Desired outcome:**
- Main view (today's folder): **5-15 canonical docs** (enough to understand system, not overwhelming)
- All related concepts **in one place** with wikilink connections
- Old sessions **archived but searchable** (preserved, hidden)
- Dashboard **reflects current reality** (updated daily, not a museum)
- New agent **reads docs in 30 min** (not a semester-long course)

---

## 🔗 References

- [[00-DASHBOARD]] — Current state reflection
- [[08-documentation-governance]] — Document cascade rules
- [[09-vault-architecture]] — Braiding pattern
- `CT_VAULT/Archive/` — Historical docs (preserved, searchable)

---

**Last Updated:** 2026-04-28 15:00 UTC  
**Status:** MAINTENANCE PROTOCOL — Prevents vault creep, maintains crystalline pressure  
**Related:** [[09-vault-architecture]], [[08-documentation-governance]], [[00-DASHBOARD]]
