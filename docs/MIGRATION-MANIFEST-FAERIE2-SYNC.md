# 🚀 LIFTOFF — Migration to faerie2/.claude (System Golden Source)

**Status:** W1 discovery + bearing mapping  
**Investigation Label:** infrastructure-consolidation-2026-04-28

---

## 🧭 Navigation Bearings (N/S/E/W)

**North (⛓️ Blocked by):** Determine which docs are system vs. project-scoped  
**South (🔓 Proceeds):** Migrate system docs to faerie2/.claude/, lock them  
**East (➡️ Parallel):** Audit global .claude/ settings (remove redundancy)  
**West (⬅️ Retreat):** Keep faerie-vault/.claude/ minimal (project HONEY only)

---

## 📋 What Moves Where

### ✅ MIGRATE TO faerie2/.claude/ (System Infrastructure)

These are **universal principles, not project-specific**:

```
faerie2/.claude/
├── CLAUDE-CORE.md
│   └── 5 f(0) principles + governance rule (1.5K tokens, ALWAYS load)
├── SPAWNING-DISCIPLINE.md (mth00090)
│   └── Agent autonomy + stigmergy (read on-demand)
├── MUTATION-CYCLE-GUIDE.md (mth00087)
│   └── How to test formula changes safely
├── faerie2-formulas.json
│   └── All mutable + immutable parameters
├── THEORY-VS-PRACTICE.md
│   └── Formula calibration dashboard
├── scripts/
│   ├── 0x_spawn_template.py (emit-bundle support)
│   ├── 0x_mission_graph.py (compass navigation)
│   ├── 0x_coc_writer.py (forensic signing)
│   └── 0x_prescan_cache.py (staleness checking)
└── hooks/
    ├── statusline.sh (live metrics push)
    └── presend-context-gate.sh (wave enforcement)
```

### ✅ STAYS IN faerie-vault/.claude/ (Project-Scoped)

Only project-specific facts:

```
faerie-vault/.claude/
├── HONEY.md
│   └── Project facts (certs, IPs, vendors—NOT universal)
└── (no CLAUDE.md copy, no system scripts)
```

### ✅ STAYS IN /mnt/d/0LOCAL/.claude/ (Global)

Universal across ALL projects:

```
~/.claude/
├── HONEY.md (universal facts, e.g., "faerie2 = f(0) orchestration")
├── NECTAR.md (recent HIGH findings, cross-project)
├── settings.json (clean, no redundancy)
└── (NO copies of SPAWNING-DISCIPLINE, MUTATION-CYCLE-GUIDE, etc.)
```

---

## 🚀 W1 LIFTOFF — Discovery Tasks (Parallel)

| Task | Bearing | Agent | Goal |
|------|---------|-------|------|
| Audit-System-Docs | S | evidence-curator | List all docs in .claude/scripts/, identify which are system vs project |
| Audit-Global-Settings | S | security-auditor | Check ~/.claude/settings.json for faerie2-specific paths that should be in faerie2/.claude/ |
| Audit-Symlinks | S | stigmergy-scout | Verify CLAUDE.md symlink path (currently → faerie2, should be locked there) |
| Map-Bundle-Locations | S | data-analyst | Where are 0x_spawn_template.py, hooks, formulas? Which repo do they belong in? |

**Goal:** Identify what moves, what stays, what's redundant.  
**Output:** forensics/artifacts/2026-04-28/AUDIT-SYSTEM-DOCS-TOPOLOGY.json

---

## ⚡ W2 CRUISE — Execution (Sequential)

| Task | Bearing | Agent | Goal |
|------|---------|-------|------|
| Migrate-System-Docs | S | documentation-engineer | Move SPAWNING-DISCIPLINE, MUTATION-CYCLE, etc. to faerie2/.claude/ with git commit |
| Migrate-Scripts | S | python-pro | Move 0x_*.py scripts to faerie2/.claude/scripts/ (or create symlinks if needed) |
| Update-Symlinks | S | fullstack-developer | CLAUDE.md symlink should point to faerie2/.claude/CLAUDE-CORE.md (or composite) |
| Clean-Settings | S | security-auditor | Remove faerie2-specific paths from ~/.claude/settings.json (they're in faerie2/.claude/settings.json now) |
| Lock-Faerie2-CLAUDE | S | code-reviewer | Commit faerie2/.claude/ to git, ensure immutable against future changes from faerie-vault/ |

**Goal:** Consolidate system docs in one place, remove redundancy.  
**Output:** Git commits tagged `migration-system-consolidation-2026-04-28`

---

## 🛸 W3 INSERTION — Background (Async)

| Task | Bearing | Agent |
|------|---------|-------|
| Wire-Context-Gates | S | ai-engineer |
| Implement-Token-Ledger | S | mlops-engineer |
| Update-Glossary-Refs | S | documentation-engineer |

---

## 📊 Compass Bearing Summary

**Current state (N edge — blocked):**
- ❌ System docs scattered (faerie2 repo, .claude/ folder, faerie-vault docs/)
- ❌ Scripts don't know which repo is their home
- ❌ Symlinks fragile (point across repos)
- ❌ Redundancy: settings.json, HONEY.md, CLAUDE.md in multiple places

**Target state (S edge — proceed):**
- ✅ faerie2/.claude/ = system golden source (principles + scripts + formulas)
- ✅ faerie-vault/.claude/ = project HONEY only (no system docs)
- ✅ ~/.claude/ = global HONEY + NECTAR + settings (clean, validated)
- ✅ Git locks system files; faerie-vault docs are project-scoped

**Next bearing (post-migration):**
- 🧭 Context gates wired into /spawn (reads faerie2/.claude/faerie2-formulas.json)
- 🧭 Token ledger hooks operational (logs real measurements)
- 🧭 /metrics dashboard live (shows theory vs practice)

---

## 🎯 Success Criteria

- [ ] Zero redundant docs (no CLAUDE.md in multiple repos)
- [ ] Scripts know their home (faerie2/.claude/scripts/ is canonical)
- [ ] Settings consolidated (one ~/.claude/settings.json, no duplication)
- [ ] Glossary used (W1/W2/W3, N/S/E/W, no "phases")
- [ ] Git locked (faerie2/.claude/* committed, immutable)
- [ ] Next agent can spawn with real token measurements

---

## Next Mission Node

**Compass edge:** S (Proceed)  
**Next task:** W2 CRUISE — Begin migrations (documentation-engineer leads)  
**Blocker:** None (N edge clear)  
**Discovery:** Token ledger implementation can run parallel (W3 INSERTION)

