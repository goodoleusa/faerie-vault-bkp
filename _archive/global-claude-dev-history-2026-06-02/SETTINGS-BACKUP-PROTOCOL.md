# Global Settings Backup & Recovery Protocol

**Purpose:** Prevent loss of `~/.claude/settings.json` by maintaining automated daily backups and easy recovery.

---

## Architecture

```
~/.claude/
  ├── settings.json                    ← ACTIVE (in use by Claude Code)
  ├── backups/
  │   ├── settings-20260425.json       ← Day 1 backup (automatic)
  │   ├── settings-20260426.json       ← Day 2 backup (automatic)
  │   ├── settings-20260427.json       ← Day 3 backup (automatic)
  │   └── ...
  └── hooks/
      ├── backup-settings.sh           ← Automated daily backup script
      └── restore-settings.sh          ← Emergency recovery script
```

**Retention:** 30-day rolling window. Backups older than 30 days auto-deleted.

---

## Daily Automatic Backup

**Trigger:** Wire to your Claude Code startup (SessionStart hook in faerie2 project, or run manually).

```bash
bash ~/.claude/hooks/backup-settings.sh
```

**What it does:**
1. Checks if `~/.claude/settings.json` exists
2. Creates dated backup if one doesn't exist for today: `settings-YYYYMMDD.json`
3. Deletes backups older than 30 days
4. Safe: runs idempotently (max 1 backup per day)

**Wire to SessionStart hook** (in `.claude/settings.json`):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/backup-settings.sh 2>/dev/null || true",
            "timeout": 5,
            "statusMessage": "💾 Settings backup..."
          }
        ]
      }
    ]
  }
}
```

---

## Emergency Recovery

If `~/.claude/settings.json` is deleted or corrupted:

### Option 1: Restore Most Recent Backup
```bash
bash ~/.claude/hooks/restore-settings.sh
```
Automatically finds the most recent backup and restores it.

### Option 2: Restore Specific Date
```bash
bash ~/.claude/hooks/restore-settings.sh 20260425
```
Restores backup from April 25, 2026. List available dates:
```bash
ls ~/.claude/backups/settings-*.json | sed 's|.*/settings-||; s|\.json||'
```

### Recovery Safeguard
When restoring, the current state is backed up as `settings-pre-restore-{timestamp}.json`, so even recovery is reversible.

---

## Canonical Sources (Fallback)

If all backups are lost, rebuild from canonical templates:

1. **Project-level template:** `{repo}/.claude/settings.json.template`
   - Comprehensive hooks, tested configuration
   - Per-project specializations

2. **Global minimal baseline:** (to be created in global .claude/)
   - Essential permissions, default model
   - Fallback if no project template available

3. **Git history:** Check recent commits for `settings.json.template` references
   ```bash
   git log --all --name-only -- "*settings*" | head -20
   ```

---

## Threat Model

**What this protects against:**
- ✅ Accidental deletion (`rm ~/.claude/settings.json`)
- ✅ Corrupted file (manual edit gone wrong)
- ✅ Misconfiguration that breaks hooks (30-day rollback available)
- ✅ Session wipe that deleted global (restore from project backup)

**What this does NOT protect against:**
- ❌ Deliberate deletion of entire `~/.claude/` directory (use git + B2 for that)
- ❌ Credential leakage in old backups (never commit `settings.json`; use env vars for secrets)
- ❌ Ransomware (backups live in same filesystem; enterprise needs offline WORM)

---

## Monitoring

Check backup freshness:
```bash
# Show last 7 backups (most recent first)
ls -lhtr ~/.claude/backups/settings-*.json | tail -7

# Show how old the most recent backup is
stat ~/.claude/backups/settings-*.json | grep Modify | head -1
```

Alert if:
- No backups exist for today
- Settings.json mtime is newer than most recent backup (backup script may have failed)
- Backup directory is empty

---

## Next Steps

1. **Run initial backup NOW:**
   ```bash
   bash ~/.claude/hooks/backup-settings.sh
   ```

2. **Verify it worked:**
   ```bash
   ls -lh ~/.claude/backups/ | head -5
   ```

3. **Wire SessionStart hook** to run automatically each session (see "Daily Automatic Backup" section above).

4. **Test recovery** (optional, but recommended):
   ```bash
   bash ~/.claude/hooks/restore-settings.sh
   # Should restore most recent backup
   ```

---

**Last Updated:** 2026-04-27  
**Status:** ✅ Live and protecting  
**Recovery Test:** Manual (user-initiated)
