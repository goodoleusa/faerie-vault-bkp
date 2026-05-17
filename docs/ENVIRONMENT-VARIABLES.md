---
type: reference
status: active
created: 2026-05-17
tags: [env, variables, setup, reference]
---

> [← START-HERE](START-HERE.md)

# Environment Variables — Complete Reference

**⚠️ CRITICAL: These must be set for faerie system to work properly.**

---

## Required Variables

| Variable | Required | Where to Set | Default |
|----------|----------|-------------|---------|
| `FAERIE_REPO` | Yes | `.envrc` or shell profile | `/mnt/d/0local/gitrepos/faerie2` |
| `FAERIE_VAULT` | Yes | `.envrc` or shell profile | `/workspace/project/faerie-vault` |

---

## `FAERIE_REPO`

**Path to faerie2 orchestration repo** — The agent orchestration system.

### Where to Find It

Typical mount paths:
- **Windows (WSL):** `/mnt/d/0local/gitrepos/faerie2`
- **Linux native:** `/home/{user}/gitrepos/faerie2` or `/opt/faerie2`
- **Mac:** `/Users/{user}/gitrepos/faerie2`

### Finding Your Path

```bash
# From any terminal in faerie2 repo:
pwd

# Or check git remotes:
cd ~/faerie2 && git remote -v

# Or look for daily folders:
ls ~/faerie2/daily/
```

### Setting It

**Option 1: .envrc (direnv - recommended)**
```bash
# In FAERIE_REPO root (the faerie2 repo, NOT this vault):
echo 'export FAERIE_REPO=/mnt/d/0local/gitrepos/faerie2' >> .envrc
```

**Option 2: Shell profile**
```bash
# In ~/.bashrc or ~/.zshrc:
export FAERIE_REPO=/mnt/d/0local/gitrepos/faerie2
```

**Option 3: One-time**
```bash
# For current session only:
export FAERIE_REPO=/mnt/d/0local/gitrepos/faerie2
```

### Verifying

```bash
# Should print your faerie2 path:
echo $FAERIE_REPO

# Should show daily folders:
ls $FAERIE_REPO/daily/
```

---

## `FAERIE_VAULT`

**Path to this vault (faerie-vault)** — The Obsidian vault.

### Where to Find It

- **This repo:** `/workspace/project/faerie-vault` (container default)
- **Local dev:** `/path/to/your/faerie-vault`

### Setting It

**Option 1: .envrc (for faerie2 sync)**
```bash
# In faerie2 repo root (NOT vault):
echo 'export FAERIE_VAULT=/workspace/project/faerie-vault' >> .envrc
```

**Option 2: Shell profile**
```bash
# In ~/.bashrc or ~/.zshrc:
export FAERIE_VAULT=/workspace/project/faerie-vault
```

### Verifying

```bash
echo $FAERIE_VAULT
ls $FAERIE_VAULT/.obsidian/
```

---

## Obsidian Dataview Integration

**Dataview reads `FAERIE_VAULT`** to find agent outputs in forensics.

### Required in Obsidian

1. **Dataview plugin enabled** (Essential stack)
2. **Environment variable set** before Obsidian launches

### How Dataview Uses It

```javascript
// Dataview reads from:
// $FAERIE_VAULT/faerie2/forensics/daily/
// $FAERIE_VAULT/faerie2/forensics/bundles/

// Example: Live agent reputation
dataview.table("agent", "score")
.from("faerie2/forensics/evals")
```

If `FAERIE_VAULT` is wrong:
- Dashboard queries return empty
- Live metrics don't update
- Intent routing fails

---

## Vault Sync Script

**Location:** `scripts/9x_obsidian_vault_sync.py`

### Environment Variables for Sync

```bash
# Full sync with external repo
FAERIE_REPO=/mnt/d/0local/gitrepos/faerie2 \
FAERIE_VAULT=/workspace/project/faerie-vault \
python3 scripts/9x_obsidian_vault_sync.py --all
```

### Sync Operations

| Flag | Function |
|------|----------|
| `--convert-json` | JSON evals → dataview markdown |
| `--scan` | Route docs to intent folders |
| `--sync-external` | Pull from faerie2 daily/forensics |
| `--validate-plugins` | Check 7 essential plugins |
| `--health` | Vault health report |

---

## Complete Setup Checklist

- [ ] `FAERIE_REPO` points to faerie2 repo (run: `echo $FAERIE_REPO`)
- [ ] `FAERIE_VAULT` points to this vault (run: `echo $FAERIE_VAULT`)
- [ ] Can list daily folders: `ls $FAERIE_REPO/daily/`
- [ ] Can list vault .obsidian: `ls $FAERIE_VAULT/.obsidian/`
- [ ] Obsidian launched with vars set
- [ ] Dataview queries working

---

## Common Issues

| Symptom | Fix |
|--------|-----|
| Dataview empty | Check `FAERIE_VAULT` is set |
| Sync finds nothing | Check `FAERIE_REPO` path |
| Plugin errors | Run `--validate-plugins` |
| Intent routing fails | Check intent folders exist |

---

*Updated: 2026-05-17*