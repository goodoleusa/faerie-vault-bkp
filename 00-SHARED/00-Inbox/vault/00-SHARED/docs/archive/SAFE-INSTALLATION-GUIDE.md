# Safe Installation Guide — faerie2 Coexistence

**Document**: SAFE-INSTALLATION-GUIDE.md  
**Version**: 1.0  
**Created**: 2026-04-06  
**Purpose**: Installation manifest documenting safe merge scenarios for existing ~/.claude environments

---

## Overview

Many Claude CLI users already have their own `~/.claude/` with custom:
- Agent cards in `~/.claude/agents/`
- Personal commands in `~/.claude/commands/`
- Custom rules in `~/.claude/rules/`
- Settings in `~/.claude/settings.json`
- Memory in `~/.claude/memory/HONEY.md` and `~/.claude/memory/NECTAR.md`

**faerie2 must coexist gracefully** without destroying any of this.

This guide documents:
1. What faerie2 adds to `~/.claude/`
2. What faerie2 never touches
3. How to merge safely if you have existing content
4. How to roll back if something goes wrong

---

## What Was Updated

### 1. INSTALL.md — Main Installation Guide

**Location**: `/mnt/d/0local/gitrepos/faerie2/INSTALL.md`

**Added Section**: `## Step 2: Safe Installation`

This new section covers:
- **Fresh Installation** (no existing ~/.claude) — simple path
- **Existing ~/.claude Protection** (THE IMPORTANT ONE) — detailed merge scenarios

**New subsections**:
- Step 1: Back Up Your Existing ~/.claude
- Step 2: Audit What You Have
- Step 3: Choose Your Merge Strategy (3 options)
  - Option A: Safe Merge (recommended) — uses `cp -rn` to skip existing files
  - Option B: Selective Install — pick specific components
  - Option C: Full Override — replace everything (backup is safety net)
- Step 4: Integrate settings.json — manual merge (never copy wholesale)
- Step 5: Protect Your Memory — HONEY.md and NECTAR.md handling
- Step 6: Verify the Install — dashboard test
- Rollback Protocol — restore from backup if needed

**Also added**: Table showing what faerie2 adds vs. what it doesn't touch

### 2. scripts/install.sh — Enhanced Installer

**Location**: `/mnt/d/0local/gitrepos/faerie2/scripts/install.sh`

**New flags**:
- `--no-clobber` — Use `cp -n` to skip existing files (safe merge for custom ~/.claude)
- `--force` — Skip all confirmations, do full override immediately
- `--verify-settings` — Check settings.json validity after install

**Enhanced behavior**:
- Clearer messaging when using safe-merge mode
- Updated next-steps guidance pointing to INSTALL.md safe installation section
- Optional settings.json validation at install end

---

## Installation Scenarios

### Scenario A: Fresh Installation (no ~/.claude yet)

```bash
bash scripts/install.sh
```

Simple path. No conflicts possible. Installation completes in ~5 seconds.

### Scenario B: Existing ~/.claude with Custom Content (THE IMPORTANT ONE)

**Three merge strategies available:**

#### Option A: Safe Merge (RECOMMENDED)

```bash
# Step 1: Backup first (automatic, but you can do it manually too)
cp -r ~/.claude ~/.claude-backup-$(date +%Y%m%d-%H%M%S)

# Step 2: Install with --no-clobber flag
bash scripts/install.sh --no-clobber

# Result:
# - Your existing agent cards stay untouched
# - Your existing commands stay untouched
# - Your existing rules stay untouched
# - Only NEW faerie2 files are added
```

**Use when**: You have custom agents/commands/rules and want to keep them while adding faerie2.

#### Option B: Selective Install

```bash
# Manual approach: copy only what you want
cp -r /path/to/faerie2/.claude/skills/faerie ~/.claude/skills/
cp -r /path/to/faerie2/.claude/commands/faerie.md ~/.claude/commands/
cp -r /path/to/faerie2/.claude/rules/ ~/.claude/rules/
# Don't touch agents until you've reviewed them
```

**Use when**: You want only specific faerie2 components.

#### Option C: Full Override

```bash
# Backup first (essential safety net)
cp -r ~/.claude ~/.claude-backup-$(date +%Y%m%d-%H%M%S)

# Full replacement with faerie2
bash scripts/install.sh

# If problems occur:
rm -rf ~/.claude && mv ~/.claude-backup-* ~/.claude
```

**Use when**: Starting fresh with faerie2 as your entire system. Backup from Step 1 is your escape hatch.

---

## Critical: settings.json Merge Protocol

**DO NOT** copy faerie2's settings.json over yours wholesale.

Your `~/.claude/settings.json` contains:
- Trusted tools and permissions specific to your workflow
- Your custom hooks or configurations
- Features you may have already set up

**faerie2 adds hooks.** Merge manually:

1. Open your existing `~/.claude/settings.json`
2. Find the `"hooks"` section (or create it if absent)
3. Add these entries:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/forensic_coc.py stop",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read|Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/forensic_coc.py posttool",
            "timeout": 3
          }
        ]
      }
    ]
  }
}
```

4. **Merge**, don't replace — append these entries to your existing hooks arrays

---

## Memory Protection

faerie2 uses `~/.claude/memory/HONEY.md` and `~/.claude/memory/NECTAR.md`.

**What happens**:
- If these files don't exist: faerie2's setup creates them safely
- If they exist with your content: faerie2 **appends** investigation context rather than overwriting

**Your action**:
- Your existing memory is preserved
- Review appended content (it's clearly delimited)
- Remove investigation seed later if not needed

---

## What Faerie2 Adds vs. What It Doesn't Touch

| Component | faerie2 adds | Your existing content |
|-----------|-------------|----------------------|
| `~/.claude/agents/` | 20+ specialized agent cards | Kept (with --no-clobber) |
| `~/.claude/commands/` | /faerie /handoff /crystallize /run /queue | Kept |
| `~/.claude/rules/` | 4 canonical rule files | Kept (unless using full override) |
| `~/.claude/skills/` | faerie, run, memory, data-ingest, stat, etc | Kept |
| `~/.claude/hooks/` | forensic_coc.py, session hooks, state infrastructure | Kept |
| **`~/.claude/settings.json`** | **NOT TOUCHED** — manual merge only | Always yours |
| **`~/.claude/memory/HONEY.md`** | **NOT TOUCHED** — append only | Always yours |
| **`~/.claude/memory/NECTAR.md`** | **NOT TOUCHED** — append only | Always yours |

---

## Rollback Protocol

If something goes wrong or you change your mind:

```bash
# Full rollback to pre-faerie2 state (5 seconds)
rm -rf ~/.claude
mv ~/.claude-backup-YYYYMMDD-HHMMSS ~/.claude

# You're back to exactly where you started — no data loss
```

The backup from Step 1 is your escape hatch. Keep the backup directory name somewhere safe.

---

## Verification Checklist

After installation, verify everything works:

```bash
# 1. Claude CLI working
claude --version

# 2. faerie2 files copied
ls ~/.claude/{agents,commands,rules,skills,hooks}

# 3. settings.json is valid JSON
python3 -m json.tool ~/.claude/settings.json > /dev/null && echo "✓ valid"

# 4. Hooks exist
ls ~/.claude/hooks/forensic_coc.py

# 5. Dashboard works
cd /any/project
claude
/faerie
```

If you see a dashboard with no errors: **installation successful.**

---

## Timeline

| Activity | Time |
|----------|------|
| Backup existing ~/.claude | 2 seconds |
| Safe merge (--no-clobber) | 5 seconds |
| Full copy | 3 seconds |
| Settings.json manual merge | 2 minutes (one-time) |
| Verification | 30 seconds |
| **Total** | **~10 minutes first time** |
| **Upgrade (with --no-clobber)** | **~5 minutes** |

---

## Enhanced scripts/install.sh Features

The installer now supports these flags:

```bash
# Fresh install (traditional)
bash scripts/install.sh

# Dry-run: show what would be copied
bash scripts/install.sh --dry-run

# Safe merge: skip existing files
bash scripts/install.sh --no-clobber

# Full override with auto-backup
bash scripts/install.sh --force

# Verify settings.json validity after install
bash scripts/install.sh --verify-settings

# Combine flags
bash scripts/install.sh --no-clobber --verify-settings --dry-run
```

---

## Reference

**Main files updated**:
- `/mnt/d/0local/gitrepos/faerie2/INSTALL.md` — Added "Safe Installation" section (§ Step 2)
- `/mnt/d/0local/gitrepos/faerie2/scripts/install.sh` — Added --no-clobber, --force, --verify-settings flags
- `/mnt/d/0local/gitrepos/faerie2/docs/SAFE-INSTALLATION-GUIDE.md` — This document

**Related documentation**:
- `/mnt/d/0local/gitrepos/faerie2/README.md` — System overview
- `/mnt/d/0local/gitrepos/faerie2/docs/CHEATSHEET.md` — Daily commands
- `/mnt/d/0local/gitrepos/faerie2/docs/FAERIE-HUMAN-GUIDE.md` — How to use faerie2

---

## Key Principles

1. **Backup First**: Always create a timestamped backup before any install
2. **Merge, Don't Replace**: Use `--no-clobber` or selective copy when you have custom content
3. **Manual settings.json**: Never copy settings.json wholesale — merge hooks section only
4. **Memory Protected**: HONEY.md and NECTAR.md are append-only; your content is safe
5. **Escape Hatch**: Rollback is simple and fast (5 seconds to restore)

---

## FAQ

**Q: I have custom agent cards. Will faerie2 overwrite them?**  
A: Not if you use `--no-clobber` or selective install. Standard install does full copy, so back up first.

**Q: What if my settings.json gets corrupted?**  
A: It won't — the installer doesn't touch settings.json. You manually merge hooks (2-minute task).

**Q: Can I upgrade faerie2 later with --no-clobber?**  
A: Yes. Each upgrade with `--no-clobber` only adds new files, preserving your customizations.

**Q: How do I know if the install worked?**  
A: Run `claude` then `/faerie`. If you see a dashboard with no errors, you're good.

**Q: What's the fastest way to install if I'm starting fresh?**  
A: `bash scripts/install.sh` — ~8 seconds + 2 minutes to wire hooks.json.

**Q: I messed something up. How do I recover?**  
A: `rm -rf ~/.claude && mv ~/.claude-backup-* ~/.claude` — you're back in 5 seconds.

---

## Contact / Support

If you hit issues:
1. Check INSTALL.md (you may have missed a step)
2. Review README.md for architecture context
3. See docs/CHEATSHEET.md for common commands and patterns
4. Check the rules in `.claude/rules/` (they document how faerie2 works)

Good luck! Once `/faerie` shows a dashboard with no errors, you're ready to work.
