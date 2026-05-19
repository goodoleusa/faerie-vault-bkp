# Environment Setup for faerie2 + Vault

When you join faerie2, your system needs to know where everything lives. This file explains the key environment variables.

## Critical Paths

### `CLAUDE_HOME`
- **What:** Where Claude Code stores faerie2's system (agents, hooks, memory)
- **Default:** `~/.claude`
- **Set by:** `install.sh` (automatic)
- **Example:** `export CLAUDE_HOME="$HOME/.claude"`

### `CT_VAULT`
- **What:** Your knowledge base (this Obsidian folder)
- **Default:** You choose during setup
- **Set by:** You (Step 3 of QUICKSTART)
- **Example:** `export CT_VAULT="$HOME/0-ObsidianTransferring/CyberOps-UNIFIED"`

### `FAERIE_REPO`
- **What:** Root of the faerie2 repository
- **Default:** Usually `~/faerie2` or wherever you cloned it
- **Set by:** `install.sh` (automatic)
- **Example:** `export FAERIE_REPO="$HOME/faerie2"`

### `FORENSICS_GLOBAL`
- **What:** Global forensics archive (for multi-project artifact chains)
- **Default:** `~/.forensics/global`
- **Set by:** `install.sh` (automatic)
- **Optional:** Most users don't need this

## How to Persist These

Add to `~/.bashrc` (or `~/.zshrc` for macOS Zsh):

```bash
# faerie2 environment
export CLAUDE_HOME="$HOME/.claude"
export CT_VAULT="$HOME/0-ObsidianTransferring/CyberOps-UNIFIED"
export FAERIE_REPO="$HOME/faerie2"
```

Then reload:
```bash
source ~/.bashrc
```

Verify:
```bash
echo $CT_VAULT
# Should print: /Users/you/0-ObsidianTransferring/CyberOps-UNIFIED
```

## Troubleshooting

**Q: `$CT_VAULT` is empty when I type `echo $CT_VAULT`**
- A: You haven't exported it. Add it to `~/.bashrc` and run `source ~/.bashrc`.

**Q: Paths look like `D:\` instead of `/mnt/d/`**
- A: You're in Windows CMD, not WSL. Open WSL by typing `wsl` first.

**Q: Faerie can't find my vault**
- A: Make sure `CT_VAULT` points to the folder where this file lives. Check: `ls $CT_VAULT/00-SHARED/ENVIRONMENT-SETUP.md`

## Next Steps

Once these are set:
1. Read the repo `QUICKSTART.md` for first-run steps
2. Type `claude` to start a Claude session
3. Type `/faerie` to launch the orchestrator
4. Type `/run` to claim your first task

**Questions?** See [../QUICKSTART.md](../QUICKSTART.md) in the vault or `$FAERIE_REPO/QUICKSTART.md` in the repo.
