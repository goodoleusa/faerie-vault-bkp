# faerie-vault — Collaborative Obsidian Vault

**faerie-vault** is an Obsidian vault designed to work alongside the **faerie2** agent orchestration platform. It provides a shared workspace for investigation notes, documentation, and real-time insights via Dataview dashboards.

## Quick Start

1. **Clone both repos** into the same directory:
   ```bash
   mkdir -p ~/faerie-repos
   cd ~/faerie-repos
   git clone https://github.com/goodoleusa/faerie2.git faerie2
   git clone https://github.com/goodoleusa/faerie-vault.git faerie-vault
   ```

2. **Set environment variable** (add to `~/.bashrc` or `~/.zprofile`):
   ```bash
   export FAERIE_VAULT=~/faerie-repos/faerie-vault
   ```

3. **Open in Obsidian:**
   - File → Open vault folder → select `~/faerie-repos/faerie-vault`
   - Accept Obsidian configuration prompts
   - Enable "Dataview" plugin (Settings → Community Plugins)

4. **View live metrics:**
   - Navigate to `00-SHARED/Dashboards/Session-Metrics.md`
   - Dataview queries auto-refresh from faerie2 forensics output

## Structure

```
faerie-vault/
  00-SHARED/           # Shared investigation notes & findings
    Dashboards/        # Dataview queries + live metrics
    Inbox/             # Quick entry points
    Evidence/          # Investigation findings (Tier 1-4)
    Droplets/          # Crystallized insights
  .obsidian/           # Obsidian config (workspace, plugins, themes)
  HOW-SYNC-WORKS.md    # Sync protocol between faerie2 & vault
  README.md            # This file
```

## Integration with faerie2

**faerie2** orchestrates agents that:
1. Generate outputs in `faerie2/forensics/evals/`
2. Write manifests with dashboards and findings
3. Vault Dataview queries pull live data from these files

**Vault and faerie2 are independent:**
- Clone vault separately or skip it
- Clone faerie2 without vault
- Use vault for notes; faerie2 for orchestration

## Sync Protocol

See `HOW-SYNC-WORKS.md` for:
- Three-store architecture (vault snapshot → forensics → B2 WORM backup)
- Observing live session metrics via Dataview
- Committing notes back to vault
- Post-session snapshot workflow

## Requirements

- **Obsidian** 1.6.7+ (free, [download](https://obsidian.md))
- **faerie2** repository (adjacent, for integration)
- **FAERIE_VAULT** environment variable set

## Troubleshooting

**Dataview queries not updating:**
- Ensure Dataview plugin enabled (Settings → Community Plugins → "Dataview")
- Check `FAERIE_VAULT` env var: `echo $FAERIE_VAULT`
- Verify `faerie2/forensics/evals/` contains `.json` files

**Vault structure unfamiliar:**
- Start with `00-SHARED/README.md` for introduction
- See faerie2 README for investigation terminology

---

**Last Updated:** 2026-04-27  
**License:** Same as faerie2  
**Issues:** Report via faerie2 repo
