# How Sync Works — Vault ↔ faerie2 Integration

## Three-Store Architecture

**faerie-vault** is part of a three-layer synchronization system:

1. **Git Canonical** — `faerie-vault/` (this repo)
   - Source of truth for vault structure
   - Investigation notes, findings, crystallized insights
   - Tracked in version control

2. **Forensics (Ephemeral)** — `faerie2/forensics/`
   - Agent outputs, manifests, session metrics
   - Real-time events from active orchestration
   - Not in vault; accessed via Dataview queries

3. **B2 WORM Backup** — Immutable cloud storage
   - Disaster recovery backup of forensics
   - Timestamp-locked, deletion-proof
   - Referenced for audit trail

**Flow:**
```
Agent writes to forensics/ → Vault Dataview queries live data → User reviews in Obsidian
                         ↓
                    B2 WORM backup (async)
                         ↓
                  Periodic snapshot → git commit → this repo
```

## Live Metrics via Dataview

**Example query** (`00-SHARED/Dashboards/Session-Metrics.md`):

```dataview
TABLE agent_type, reputation_score, task_count
FROM "faerie2/forensics/evals"
WHERE contains(file.path, "agent-reputation") AND file.mtime > now - dur(1 hour)
SORT file.mtime DESC
```

This automatically shows:
- Live agent reputation scores
- Current session piston state
- Task completion progress
- Time budget remaining

**Requirements:**
- Dataview plugin enabled in Obsidian
- `FAERIE_VAULT` env var set (Dataview uses it to find faerie2)
- `faerie2/forensics/evals/` contains recent JSON files

## Committing Vault Changes

**Normal workflow:**
1. Take notes in Obsidian (`00-SHARED/Inbox/`, `00-SHARED/Findings/`)
2. At investigation milestones, crystallize insights (move to `Droplets/`)
3. Commit to git: `cd ~/faerie-repos/faerie-vault && git commit -am "docs: investigation update"`

**Post-session snapshot:**
After a major faerie2 run, vault may contain new evidence or findings. Snapshot the vault:
```bash
cd ~/faerie-repos/faerie-vault
git add -A
git commit -m "snapshot: vault state post-RUN{N} — new findings in Evidence/"
git push origin main
```

## Sync Conflicts

**If vault and forensics diverge:**
- Vault = collaboration source (human decisions)
- Forensics = orchestration output (agent work)
- **Resolution:** Vault is authoritative; forensics are input. If conflict, vault wins (human review).

**If B2 backup and vault diverge:**
- Contact forensic recovery (6x_forensic_recovery.py) to validate
- B2 is immutable; vault takes precedence for ongoing work

## Isolation: Using Vault Without faerie2

Vault works standalone:
1. Clone only faerie-vault (skip faerie2)
2. Remove Dataview queries that reference forensics/ (optional; they'll show "no results")
3. Use vault as regular Obsidian note-taking system

## Integration: Using faerie2 Without Vault

faerie2 works standalone:
1. Clone only faerie2 (skip faerie-vault)
2. Agents output to forensics/ normally
3. No Obsidian integration; use Python/bash to query forensics

**To add vault later:**
```bash
cd ~/faerie-repos
git clone https://github.com/goodoleusa/faerie-vault.git faerie-vault
export FAERIE_VAULT=~/faerie-repos/faerie-vault
```

---

See faerie2 `INSTALL.md` for environment setup.
