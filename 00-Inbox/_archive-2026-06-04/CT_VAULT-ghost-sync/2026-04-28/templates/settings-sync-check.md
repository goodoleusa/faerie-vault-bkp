---
task_id: settings-sync-check-{{DATE}}
investigation_label: vault-enhancement-2026-04-28
status: in_progress
created: {{DATE}}
report_type: settings_sync_audit
---

# Settings Sync Verification — {{SYNC_TARGET}}

**Date:** {{DATE}}  
**Operator:** {{OPERATOR_NAME}}  
**Sync Scope:** ~/.claude/ → faerie-vault/.claude/ (and vice versa)

---

## Sync Targets

| Layer | File | Source | Target |
|-------|------|--------|--------|
| **HONEY** | HONEY.md | ~/.claude/HONEY.md | faerie-vault/.claude/HONEY.md |
| **NECTAR** | NECTAR.md | ~/.claude/NECTAR.md | N/A (project-scoped) |
| **Agents** | agents/*.md | ~/.claude/agents/ | faerie-vault/.claude/agents/ |
| **Hooks** | hooks/*.py | ~/.claude/hooks/ | faerie-vault/.claude/hooks/ |

---

## Source Files (Global)

### ~/.claude/HONEY.md

**Size:** ___ KB  
**Last Modified:** {{TIMESTAMP}}  
**Content Check:**
- [ ] Contains >5 principles (design constants)
- [ ] Has recent discovery cites (mth-xxxxx references)
- [ ] No agent-specific tactics (those go in agents/*.md)

**Checksum:** `sha256sum ~/.claude/HONEY.md`
```
{{HASH}}
```

### ~/.claude/NECTAR.md (Last 50 Lines)

**Size:** ___ KB  
**Last Modified:** {{TIMESTAMP}}  
**Recent HIGH Entries:** ___ (count)

**Last Entry:**
```
[Show tail -1 of NECTAR.md]
```

### ~/.claude/agents/ (All Cards)

**Count:** ___ agent cards

| Agent | Size | Modified | Status |
|-------|------|----------|--------|
| agent-1.md | ___ KB | {{DATE}} | ✅ / ⚠️ |
| agent-2.md | ___ KB | {{DATE}} | ✅ / ⚠️ |
| agent-3.md | ___ KB | {{DATE}} | ✅ / ⚠️ |

---

## Target Files (Project)

### faerie-vault/.claude/HONEY.md

**Size:** ___ KB  
**Last Modified:** {{TIMESTAMP}}  
**Match Global?** ✅ / ⚠️ / ❌

**Diff (if any):**
```bash
diff ~/.claude/HONEY.md faerie-vault/.claude/HONEY.md
# Show differences
```

### faerie-vault/.claude/agents/ (All Cards)

**Count:** ___ agent cards

**Missing in Project:** 
- [ ] (None) — All agents present ✅
- [ ] agent-X.md (old variant, safe to delete)
- [ ] agent-Y.md (missing, needs sync)

**Sync Status:**
```
✅ = Present + matching
⚠️ = Present but outdated (needs update)
❌ = Missing (needs sync from global)
```

---

## Diff Summary

### HONEY.md Comparison

```bash
diff ~/.claude/HONEY.md faerie-vault/.claude/HONEY.md | head -50
```

**Result:**
- [ ] **Identical** — No sync needed
- [ ] **Minor differences** — Global has recent additions, pull to project
- [ ] **Significant differences** — Conflicting edits, requires manual review

**Action:** 
- If identical: ✅ No action
- If minor: `cp ~/.claude/HONEY.md faerie-vault/.claude/HONEY.md`
- If significant: (Manual review required)

### Agent Cards Comparison

| Agent | Global | Project | Status | Action |
|-------|--------|---------|--------|--------|
| agent-1 | v1.2 | v1.2 | ✅ Match | None |
| agent-2 | v1.3 | v1.2 | ⚠️ Global newer | Pull global |
| agent-3 | v1.1 | v1.1 | ✅ Match | None |

**Total Cards:** ___ (Global), ___ (Project)  
**Out of Sync:** ___ cards

---

## Issues Found

### Issue 1 (if any)

**Location:** [which file/layer]  
**Symptom:** [what's wrong]  
**Severity:** 🟢 Minor / 🟡 Medium / 🔴 Critical  
**Root Cause:** (Why did this happen?)

**Resolution:**
```bash
# Steps to fix
step 1
step 2
```

**Verification:** (How to confirm it's fixed?)

### Issue 2 (if any)

[Repeat structure]

---

## Action Log

| Timestamp | Action | File | Result |
|-----------|--------|------|--------|
| {{TIME}} | Pulled HONEY.md | ~/.claude/HONEY.md → faerie-vault/ | ✅ Success |
| {{TIME}} | Checked agents/ | agent-cards sync | ✅ All synced |
| {{TIME}} | [Your action] | [file] | ✅ / ⚠️ / ❌ |

---

## Verification Steps

### Step 1: Verify Global ↔ Project Sync

```bash
# Check if files are identical
for file in ~/.claude/HONEY.md faerie-vault/.claude/HONEY.md; do
  echo "=== $file ===" 
  sha256sum "$file"
done

# They should have the SAME checksum
# If different: pull from global
cp ~/.claude/HONEY.md faerie-vault/.claude/HONEY.md
```

### Step 2: Verify Agent Cards Sync

```bash
# Count agents in both locations
echo "Global agents: $(ls ~/.claude/agents/*.md | wc -l)"
echo "Project agents: $(ls faerie-vault/.claude/agents/*.md | wc -l)"

# They should be equal

# Compare each card
for agent in ~/.claude/agents/*.md; do
  agent_name=$(basename "$agent")
  diff "$agent" "faerie-vault/.claude/agents/$agent_name" && echo "$agent_name: ✅ MATCH" || echo "$agent_name: ⚠️ DIFFERS"
done
```

### Step 3: Verify Hook Configuration

```bash
# Check if hooks are consistent
diff ~/.claude/hooks/ faerie-vault/.claude/hooks/ -r

# Result should be minimal or empty
```

### Step 4: Verify No Stale NECTAR

```bash
# Check NECTAR size (should be <5MB for performance)
du -h ~/.claude/NECTAR.md

# If >5MB, archive old entries
python3 scripts/2x_settings_sync.py --mode nectar-archive --older-than 90d
```

---

## Sign-Off

| Check | Status | Notes |
|-------|--------|-------|
| **Global HONEY.md synced** | ✅ / ⚠️ / ❌ | [notes] |
| **Project HONEY.md matches** | ✅ / ⚠️ / ❌ | [notes] |
| **All agent cards synced** | ✅ / ⚠️ / ❌ | Count: ___ |
| **Hook configs consistent** | ✅ / ⚠️ / ❌ | [notes] |
| **No critical issues found** | ✅ / ⚠️ | [if issues: link to Issue # above] |

**Overall Sync Status:** ✅ **CLEAN** / ⚠️ **MINOR ISSUES** / ❌ **CRITICAL ISSUES**

**Operator Signature:** {{OPERATOR}} — {{TIMESTAMP}}

---

## Example: Real Settings Sync Check

---

### Example: 2026-04-28 Sync Audit

**Date:** 2026-04-28  
**Operator:** documentation-engineer

#### Source Files

**~/.claude/HONEY.md**
- Size: 4.2 KB
- Last Modified: 2026-04-25 (3 days old)
- Checksum: `abc123def456...`

**~/.claude/NECTAR.md**
- Size: 8.7 KB (recent session notes)
- Recent HIGH entries: 3 (vault-enhancement-related)

**~/.claude/agents/**
- Count: 8 agent cards
- All up-to-date (modified within last 7 days)

#### Target Files

**faerie-vault/.claude/HONEY.md**
- Size: 4.2 KB
- Checksum: `abc123def456...`
- **Match?** ✅ Identical

**faerie-vault/.claude/agents/**
- Count: 8 agent cards
- Status: All match global versions ✅

#### Diff Summary

```
HONEY.md: IDENTICAL ✅
Agents: All 8 cards match ✅
Hooks: Consistent ✅
```

#### Issues Found

**None!** All systems are in sync.

#### Sign-Off

| Check | Status |
|-------|--------|
| Global HONEY.md synced | ✅ |
| Project HONEY.md matches | ✅ |
| All agent cards synced | ✅ |
| Hook configs consistent | ✅ |
| No critical issues | ✅ |

**Overall Status:** ✅ **CLEAN**

---

**When filing:** Save to CT_VAULT/2026-04-28/ with filename: `{{HH-MM-SS}}_settings-sync-check_{{SCOPE}}.md`
