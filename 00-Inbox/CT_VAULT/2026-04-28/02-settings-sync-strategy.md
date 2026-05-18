---
task_id: vault-enhancement-02-settings-sync
investigation_label: vault-enhancement-2026-04-28
status: in_progress
created: 2026-04-28
---

# Settings Sync Strategy — Keeping ~/.claude/ in Balance

**Breadcrumb:** [[00-DASHBOARD]] > [[02-settings-sync-strategy]] > [[01-forensic-governance]]

> Keep global ~/.claude/ (HONEY.md, NECTAR.md, agent cards) synchronized with faerie2 project state while respecting both local developer preferences and mission-critical settings.

---

## Navigation Table

| Document | Direction | Purpose |
|----------|-----------|---------|
| [[00-DASHBOARD]] | ← Previous | System status hub |
| [[01-forensic-governance]] | ← Related | COC integrity model |
| [[03-mcp-server-architecture]] | → Next | MCP server design |

---

## The Sync Problem

**Three layers of settings:**
1. **Global ~/.claude/** — User preferences, agent cards, cryptographic keys (persists across all projects)
2. **Project ./claude/** — faerie2-specific hooks, scripts, configurations (repo-scoped)
3. **Runtime state** — NECTAR.md, pollen MEM blocks (ephemeral but critical to preserve)

**The challenge:** Changes in any layer can break the others if not synchronized properly.

**Example failure modes:**
- Agent card updated in ~/.claude/ but old version cached in faerie2 repo → agent spawns with stale behavior
- Hook configuration updated in ./claude/ but global HONEY.md references old principles → manifest truthfulness drops
- NECTAR refreshed during session but not persisted to ~/.claude/ → session-scoped learning lost on restart

---

## Sync Architecture: Three Zones

### Zone 1: Global HONEY.md (~/.claude/HONEY.md)
**Owner:** User (manual edits), Agents (append-only pollen compaction)  
**Content:** Universal facts, procedures, design principles (immutable reference layer)  
**Change frequency:** Low (major updates only; monthly review cycle)  
**Sync mechanism:** Manual + scheduled backup

```
Source: ~/.claude/HONEY.md
Backup target: faerie2/docs/HONEY-BASELINE.md (read-only reference)
Conflict resolution: User edits win; repo docs are secondary references only
```

**When to sync HONEY.md:**
- Monthly: Review for new design principles from NECTAR summaries
- After major reframe: New agent behavior patterns emerge
- Quarterly: Deep audit of universal facts (purge obsolete entries)

### Zone 2: Project ./claude/ (faerie2-scoped)
**Owner:** Repo maintainers + agents (within forensic constraints)  
**Content:** f(0) hooks, scripts, 0x utilities, mission graph  
**Change frequency:** Medium (weekly or per-sprint)  
**Sync mechanism:** Git commits + hook enforcement

```
Source: faerie2/./claude/
Boundary: Agents write to forensics/ ONLY, not ./claude/
Enforcement: 8x_state_write_coc_enforcer.py (PreToolUse hook)
```

**Read-only in ./claude/:**
- hooks/*.py (scripts, not agent-modified)
- scripts/*.py (utilities, not agent-modified)
- agents/*.md (agent cards, version-controlled)

**Write-allowed in faerie2:**
- forensics/ (agent outcomes, manifests, bundles)
- .claude/memory/pollen-{SID}.md (in-session pollen)

### Zone 3: Agent Cards (~/.claude/agents/*.md)
**Owner:** Agents (discovery + reputation), User (final review)  
**Content:** Routing metadata, behavioral templates, reputation scores  
**Change frequency:** High (agent discovery happens live)  
**Sync mechanism:** Automatic via 5x_agent_card_sync.py

```
Source: ./claude/agents/*.md (project cards)
Target: ~/.claude/agents/*.md (global cards)
Conflict: Project cards take priority (more recent, mission-specific)
Direction: Unidirectional (project → global) ONLY
Frequency: Post-session (automatic)
```

**Card fields that sync:**
- Metadata: domain_mastery, belief_index, routing_weight
- Behavioral annotations: recent_successes, recovery_notes
- Cross-training: related_domains, upstream_blockers

---

## Sync Procedures: When and How

### Procedure 1: Daily Pollen Compaction → NECTAR (Every Session End)

**Trigger:** Agent completes session + writes manifest  
**Action:**
1. Read pollen MEM blocks from `.claude/memory/pollen-{SID}.md`
2. Identify HIGH-severity entries (new principles, major discoveries)
3. Append to `~/.claude/NECTAR.md` with timestamp + investigation_label
4. Compress pollen: move older entries to archive

**Script:**
```bash
python3 scripts/2x_settings_sync.py --mode pollen-to-nectar --session-id $SID
```

**Output:** NECTAR.md grows; pollen archive created

### Procedure 2: Weekly Agent Card Sync (Every Friday)

**Trigger:** Cron job + manual trigger  
**Action:**
1. Read all agent cards from `./claude/agents/*.md`
2. Compare reputation scores with `~/.claude/agents/*.md`
3. For each card: if project version is newer, update global version
4. Log sync result to `forensics/coc-entries/`

**Script:**
```bash
python3 scripts/2x_settings_sync.py --mode agent-cards --interval weekly
```

**What gets updated:**
- belief_index (if agent improved honesty)
- domain_mastery (cross-training achievements)
- routing_weight (trustworthiness composite score)

**What stays unchanged:**
- Agent name / description (user-curated)
- Cryptographic keys (never sync, security)

### Procedure 3: Monthly HONEY.md Audit (Manual, First of Month)

**Trigger:** Calendar reminder  
**Action:**
1. Read tail-30 of `~/.claude/NECTAR.md` (this month's discoveries)
2. Review for new universal facts (applicable across all projects)
3. If found: add to `~/.claude/HONEY.md` with citation + timestamp
4. Commit + push

**Script (guidance only; manual review required):**
```bash
# Show this month's HIGH entries
grep "severity: HIGH" ~/.claude/NECTAR.md | tail -30

# Review for universal applicability
# If applicable: manually add to ~/.claude/HONEY.md with ref marker [mth-xxxxx]
# Example: "Agent discovery discipline leads to 22% reduction in speculative spawns [mth00100-discovery-protocol]"

# Commit
cd ~/.claude && git add HONEY.md && git commit -m "HONEY.md: Add [mth-xxxxx] findings from $(date +%Y-%m)"
```

### Procedure 4: Sprint Boundary Hook Sync (Every 2 Weeks)

**Trigger:** Sprint start (project planning)  
**Action:**
1. Read `./claude/hooks/*.py` (all PreToolUse, PostToolUse, SubagentStop definitions)
2. Compare with `~/.claude/hooks/` (global hook registry)
3. If project hooks are newer, stage update
4. Alert user: "New hook signatures detected. Review and approve?"

**Script:**
```bash
python3 scripts/2x_settings_sync.py --mode hooks --interval sprint
```

**Critical review points:**
- Hook matchers (are they still correct for this project?)
- Enforcement level (should new rules apply to other projects?)
- Side effects (does this hook conflict with existing global hooks?)

---

## Conflict Resolution Strategy

**Hierarchy (highest to lowest priority):**
1. **User consent** — If user says "don't sync", don't sync
2. **Recency** — Newer version wins (except for HONEY.md, which is immutable)
3. **Mission specificity** — Project settings override global settings
4. **Integrity first** — If sync would break COC chain, abort and alert

**Example resolution:**

| Scenario | Global | Project | Resolution |
|----------|--------|---------|------------|
| Agent reputation scores | belief_index: 0.75 | belief_index: 0.82 | Use 0.82 (newer, project-scoped) |
| Hook configuration | Old matcher (v1) | New matcher (v2) | Use v2 if project is primary owner; alert if v2 is breaking change |
| HONEY.md principle | Established (immutable) | Proposed change | REJECT change; propose as NECTAR entry instead |
| Agent card domain | "code-review" (global) | "code-review, mcp-deployment" (project) | Merge: add project domains to global card |

---

## Troubleshooting Common Issues

### Issue: "Agent card out of sync; manifest belief_index doesn't match card"

**Diagnosis:**
```bash
# Check if project agent card is newer than global
stat /mnt/d/0local/gitrepos/faerie-vault/.claude/agents/python-pro.md
stat ~/.claude/agents/python-pro.md
```

**Fix:**
```bash
# Force sync from project to global
python3 scripts/2x_settings_sync.py --mode agent-cards --force
```

### Issue: "NECTAR.md has grown to >10MB; performance degrading"

**Diagnosis:** NECTAR compaction missed or disabled

**Fix:**
```bash
# Archive old entries (>3 months ago) to NECTAR-ARCHIVE.md
python3 scripts/2x_settings_sync.py --mode nectar-archive --older-than 90d

# Verify size after archive
wc -l ~/.claude/NECTAR.md ~/.claude/NECTAR-ARCHIVE.md
```

### Issue: "Pollen never compacted; session knowledge lost"

**Diagnosis:** No automatio hook firing at session end

**Fix:**
1. Verify PostSubagentStop hook is configured in Anthropic settings
2. Check if 5x_agent_card_sync.py is executable
3. Run manually: `python3 scripts/2x_settings_sync.py --mode pollen-to-nectar --session-id {SID}`

### Issue: "Sync script blocked by permission error"

**Diagnosis:** ~/.claude/ not writable by current user

**Fix:**
```bash
# Check permissions
ls -la ~/.claude/

# Fix if needed (assumes user owns ~/.claude/)
chmod u+w ~/.claude/NECTAR.md
chmod u+w ~/.claude/agents/

# Retry sync
python3 scripts/2x_settings_sync.py --mode pollen-to-nectar
```

---

## Hook Integration Points

**These hooks wire settings sync into the normal agent lifecycle:**

### PreToolUse Hook: Validate Settings Before Spawn
```
Match: Agent() spawn
Action: Check if ~/.claude/ matches ./claude/ versions
Output: If mismatch, warn user + offer to sync before spawn
```

### PostToolUse Hook: Capture New Settings
```
Match: Write to ./claude/hooks or ./claude/agents
Action: Trigger weekly sync check (defer to batch)
Output: Log to forensics/coc-entries/
```

### PostSubagentStop Hook: Compact Pollen
```
Match: Subagent completes (TaskNotification received)
Action: Read pollen MEM blocks, identify HIGH entries
Output: Append to NECTAR, create pollen archive
```

**See [[01-forensic-governance]] for COC enforcement details.**

---

## Best Practices

1. **Never edit ~/.claude/ manually during a session** — Use scripts to sync instead. Manual edits can create orphaned entries.

2. **Review NECTAR monthly** — Compaction is automatic, but understanding what learned is critical for system improvement.

3. **Commit HONEY.md changes separately** — `git commit -m "HONEY.md: Add [mth-xxxxx]..."` makes changes traceable to discovery process.

4. **Test hook changes in project first** — Update ./claude/hooks, verify locally, THEN promote to ~/.claude/ via sync.

5. **Archive NECTAR quarterly** — Keep active NECTAR <5MB for fast reads. Archive >3mo old entries.

---

**Related:** [[01-forensic-governance]] (COC chain integrity), [[03-mcp-server-architecture]] (how settings affect server behavior)  
**Ref:** faerie design principle: "Artifacts-in-forensics"; settings are artifacts too  
**Status:** Ready for implementation
