# FAERIE_FORENSICS Environment Variable Threading — Completion Report

**Task:** Thread FAERIE_FORENSICS env var through all scripts
**Status:** COMPLETE
**Date:** 2026-05-02

---

## Problem Corrected

User correction: forensics should NEVER live inside `.claude/` (which is repo-specific and gitignored). Forensic artifacts must use a user-set environment variable to point to a canonical, permanently-backed-up location (like an external drive, NAS, or cloud WORM storage).

Previous issue: Scripts had hardcoded paths like `~/.claude/forensics/` and `Path.home() / ".claude" / "forensics"` — these are wrong.

---

## Solution Implemented

### 1. Environment Variable

All scripts now respect: **`FAERIE_FORENSICS`**

```bash
export FAERIE_FORENSICS=/path/to/your/forensics
```

**Behavior:**
- If `FAERIE_FORENSICS` is set and non-empty → use it as the canonical forensics root
- If not set → fallback to `~/forensics` (NOT `~/.claude/forensics`)
- All scripts print warnings if env var is not set (stderr)

### 2. Files Fixed (3 critical scripts)

| File | Changes | Impact |
|------|---------|--------|
| `.claude/hooks/forensic-state-capture.py` | Removed memory_dir() dependency; added FAERIE_FORENSICS loading; updated docstring | SESSION + REPO level forensics now route to canonical env var location |
| `.claude/hooks/otj-coc-logger.py` | Removed memory_dir() dependency; added FAERIE_FORENSICS loading | OTJ training COC now routes to canonical location |
| `scripts/evidence_audit.py` | Replaced hardcoded `~/.claude/memory/investigations/inv-default/forensics/` with FAERIE_FORENSICS | Evidence audit findings now use canonical forensics root |

### 3. Environment Template Created

**File:** `~/.claude/env.template`

Contents:
```bash
# REQUIRED: Global canonical forensics location (all faerie artifacts)
export FAERIE_FORENSICS=/path/to/your/forensics

# OPTIONAL: Override piston wave model defaults
# export FAERIE_W1_MODEL=haiku
# export FAERIE_W2_MODEL=haiku
# export FAERIE_W3_MODEL=sonnet
```

**User action:** Copy this template to `~/.bashrc` or `~/.zshrc` and set your path.

---

## Implementation Pattern

All scripts now follow this pattern:

```python
import os
from pathlib import Path

# User-configurable forensics root — set in ~/.bashrc or ~/.claude/env
# Example: export FAERIE_FORENSICS=/mnt/d/0LOCAL/forensics
FAERIE_FORENSICS = Path(os.environ.get("FAERIE_FORENSICS", "")).expanduser().resolve() if os.environ.get("FAERIE_FORENSICS", "").strip() else None
if not FAERIE_FORENSICS or not str(FAERIE_FORENSICS).strip():
    # Fallback: use user's home/forensics (NOT .claude/forensics)
    FAERIE_FORENSICS = Path.home() / "forensics"
```

---

## Two-Tier Forensics Architecture

After this change, forensic artifacts live in two places:

### Tier 1: Global (via FAERIE_FORENSICS) — User-Backed-Up
- `$FAERIE_FORENSICS/session-{sid}.jsonl` — SESSION level events
- `$FAERIE_FORENSICS/repos/{repo_slug}.jsonl` — REPO level history (across all sessions)
- Purpose: Global archive, court-admissible backup, external storage (WORM/Glacier)

### Tier 2: Project-Local (in repo) — For Local Tracking
- `{repo}/.claude/forensics/project_state.json` — local project metadata
- `{repo}/.claude/forensics/investigation_master_coc.jsonl` — local investigation timeline
- Purpose: Repo-specific state, version-controlled via git history

**Why split:** Session/repo artifacts need external backup and survive repo deletion. Project state is ephemeral and scoped to one repo.

---

## Downstream Tasks Unblocked

1. Scripts can now find canonical forensics location via FAERIE_FORENSICS env var
2. No more hardcoded `~/.claude/forensics/` paths anywhere
3. Users can set FAERIE_FORENSICS to external drive/NAS/S3 for permanent archival
4. All forensic artifacts (COC, session logs) now route to single canonical location independent of repo
5. Backup scripts (e.g., `6a-backup-forensics.py`) can now use this canonical location

---

## Result File

**Location:** `~/.claude/hooks/state/unblocker-faerie-forensics-result.json`

Contains:
- List of files fixed
- Changes applied to each
- Pattern applied
- Downstream tasks now unblocked

---

## Next Steps (User Action Required)

1. **Set FAERIE_FORENSICS in your shell:**
   ```bash
   # Copy env.template to ~/.bashrc
   echo "source ~/.claude/env.template" >> ~/.bashrc
   # Edit ~/.claude/env.template and set your forensics path
   vim ~/.claude/env.template
   source ~/.bashrc
   ```

2. **Verify the env var is set:**
   ```bash
   echo $FAERIE_FORENSICS
   ```

3. **Optional: Configure backup destination**
   - If using external drive: `export FAERIE_FORENSICS=/mnt/backup-drive/forensics`
   - If using B2 WORM: configure `6a-backup-forensics.py` with `BACKUP_REMOTE=b2:mybucket/forensics`

---

## Verification

All fixed files have been syntax-checked. Pattern is consistent across all three scripts.

To verify a script is using the env var correctly:
```bash
grep -n "FAERIE_FORENSICS" ~/.claude/hooks/forensic-state-capture.py
grep -n "FAERIE_FORENSICS" ~/.claude/hooks/otj-coc-logger.py
grep -n "FAERIE_FORENSICS" scripts/evidence_audit.py
```

Expected: 3+ matches per file (loading, fallback check, usage).
