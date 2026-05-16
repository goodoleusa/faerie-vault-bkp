# HONEY.md Versioning via the Vault

HONEY.md is always-loaded startup context. Changing it affects every future agent.
The vault gives you a safe way to snapshot, diff, and roll back before a crystallization
makes irreversible changes.

---

## The Three Operations

### 1. Snapshot before crystallizing (always do this)

```bash
# From any repo — takes 2 seconds
STAMP=$(date +%Y%m%d-%H%M)
cp ~/.claude/memory/HONEY.md \
   "/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps/00-SHARED/Hive/honey-snapshots/HONEY-${STAMP}.md"
echo "Snapshot: HONEY-${STAMP}.md"
```

The vault's `00-SHARED/Hive/honey-snapshots/` folder holds all your HONEY snapshots.
Syncthing propagates them to other devices automatically. Git doesn't track HONEY (it's in
`~/.claude/memory/`, outside any repo), so the vault is the version history.

---

### 2. Diff two versions

```bash
# What changed between last snapshot and now?
LATEST=$(ls -t /mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps/00-SHARED/Hive/honey-snapshots/ | head -1)
diff "/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps/00-SHARED/Hive/honey-snapshots/${LATEST}" \
     ~/.claude/memory/HONEY.md
```

Or compare any two snapshots:
```bash
diff HONEY-20260405-1430.md HONEY-20260406-0900.md
```

---

### 3. Rollback to a prior snapshot

```bash
# Check the snapshot you want to restore
cat "/mnt/d/0LOCAL/.../honey-snapshots/HONEY-20260405-1430.md" | head -20

# Restore it (backs up current first)
cp ~/.claude/memory/HONEY.md ~/.claude/memory/HONEY.md.bak
cp "/mnt/d/0LOCAL/.../honey-snapshots/HONEY-20260405-1430.md" \
   ~/.claude/memory/HONEY.md
echo "Rolled back. Backup at HONEY.md.bak"
```

---

## HONEY Versioning Protocol (Full)

```
Before crystallizing:
  1. Run snapshot command above
  2. Note the timestamp in your session notes
  3. Run /crystallize
  4. Check: wc -l ~/.claude/memory/HONEY.md (should be ≤200)
  5. Read the diff — does every change make sense?
  6. If not: rollback immediately, inspect what membot changed

After a good crystallization:
  1. Take another snapshot (now you have before + after)
  2. The "after" snapshot is your new stable baseline
```

---

## Collaborator HONEY Versioning

When your collaborator installs via `0a_setup_collab.py`, the investigation context
is clearly delimited with a header:

```
---
## CyberTemplate Investigation Context (from 0a_setup_collab.py)
```

To update their investigation context when findings change:
```bash
# 1. Snapshot their current HONEY first
cp ~/.claude/memory/HONEY.md ~/.claude/memory/HONEY-before-update.md

# 2. Remove old investigation section (everything after the delimiter)
# Find the line number of the delimiter:
grep -n "CyberTemplate Investigation Context" ~/.claude/memory/HONEY.md

# 3. Re-run 0a_setup_collab.py from the updated cybertemplate repo
cd /path/to/cybertemplate
python3 scripts/0a_setup_collab.py  # appends fresh context
```

---

## What HONEY.md Should and Shouldn't Contain

**Put in HONEY (crystallization candidates):**
- Methods that work across many sessions (process patterns, not case data)
- System rules you've confirmed improve agent performance
- Preferences validated by 3+ sessions
- Identity facts (machine config, repo paths, tool choices)

**Keep in NECTAR (not HONEY):**
- Investigation findings (H1=0.95, specific IPs, named individuals)
- Sprint summaries and open questions
- Anything session- or case-specific

**The gate that matters:** "Would this be useful to an agent working on a completely
different project?" If yes → HONEY candidate. If no → stays in NECTAR.

Investigation-specific facts that passed the crystallization gate incorrectly will
show up as noise in agents that have nothing to do with your investigation. Keep HONEY
universal; keep findings in NECTAR.

---

## Vault Snapshot Folder

```
00-SHARED/Hive/honey-snapshots/
  HONEY-20260329-1400.md   ← pre-sprint crystallization
  HONEY-20260401-0900.md   ← post-sprint
  HONEY-20260405-1430.md   ← pre-C4 crystallization
  HONEY-20260406-0900.md   ← post-C4 (175 lines, 87.5%)
```

Naming convention: `HONEY-YYYYMMDD-HHMM.md`. One snapshot before + after each `/crystallize`.

---

## One-liner for your session startup

```bash
alias honey-snap='cp ~/.claude/memory/HONEY.md "/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps/00-SHARED/Hive/honey-snapshots/HONEY-$(date +%Y%m%d-%H%M).md" && echo "HONEY snapshotted"'
```

Add to `~/.bashrc`. Run `honey-snap` before any `/crystallize`.
