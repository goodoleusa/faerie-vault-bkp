# Pseudosystem Architecture (0dotclaude)

This folder (`0dotclaude/`) is the **pseudosystem layer** for faerie-vault. It holds system infrastructure (formulas, scripts, hooks) that drive agent behavior and mission formation, without cluttering the vault's main content.

**Why "0dotclaude" instead of ".claude"?** Obsidian treats dot-prefixed folders as hidden. Using `0dotclaude` makes the system infrastructure visible in the graph while keeping it conceptually separate from project data.

---

## Folder Structure

```
faerie-vault/
├── 0dotclaude/                          ← PSEUDOSYSTEM (this folder)
│   ├── faerie2-formulas.json            ← Mutable parameters (wave gates, quality thresholds, etc.)
│   ├── CONTEXT-GATING-OPERATIONAL.md    ← mth00106: Context % → auto wave selection
│   ├── BUNDLE-EMISSION-PRESSURE.md      ← mth00107: Remaining context > 30% → emit bundles
│   ├── GLOSSARY-UNIFIED.md              ← Visual language (🚀 LIFTOFF, ⚡ CRUISE, etc.)
│   ├── scripts/
│   │   └── 0x_spawn.py                  ← Spawn orchestrator (fixed: executes agents)
│   └── hooks/
│       └── 0x_bundle_emission_pressure.sh ← Presend: injects bundle-emit instructions
│
├── forensics/                           ← VAULT EVIDENCE (mission outcomes)
│   ├── manifests/2026-04-28/            ← Agent routing signals (where did work go?)
│   ├── artifacts/2026-04-28/            ← Work products (reports, analysis, measurements)
│   ├── bundles/2026-04-28/              ← Task context (what was the mission?)
│   └── coc-entries/                     ← Chain of custody (audit trail)
│
├── 00-SHARED/                           ← VAULT CONTENT (discoveries, insights)
│   └── Droplets/                        ← Cross-session inspiration (AHA moments)
│
├── 01-Memories/                         ← Session memory & learning
├── 01-PROTECTED/                        ← Sensitive case data
├── 02-Skills/                           ← Skill definitions & protocols
└── ...
```

---

## Conceptual Model: Faerie System Layers

```
User (you)
    ↓
Global HONEY/NECTAR (/mnt/d/0LOCAL/.claude/)
    ↓
faerie2/.claude/ (SYSTEM GOLDEN SOURCE)
    ├─ CLAUDE-CORE.md (1.5K, f(0) principles)
    ├─ faerie2-formulas.json (source of truth)
    ├─ SPAWNING-DISCIPLINE.md (mth00090)
    ├─ MUTATION-CYCLE-GUIDE.md (mth00087)
    └─ scripts/ (0x_spawn.py, 0x_mission_graph.py, etc.)
    ↓
faerie-vault/0dotclaude/ (THIS FOLDER - PROJECT PSEUDOSYSTEM)
    ├─ faerie2-formulas.json (copy, for local mutation testing)
    ├─ CONTEXT-GATING-OPERATIONAL.md (mth00106)
    ├─ BUNDLE-EMISSION-PRESSURE.md (mth00107)
    └─ scripts/ (0x_spawn.py synced from upstream)
    ↓
faerie-vault/forensics/ (MISSION OUTCOMES)
    ├─ manifests/ (agent routing decisions)
    ├─ artifacts/ (work products)
    └─ bundles/ (task context for future agents)
    ↓
faerie-vault/00-SHARED/Droplets/ (LONG-TERM INSIGHTS)
    └─ Crystallized insights survive session compaction
```

---

## Mission Graph Navigation

**How agents find work:**

1. Agent spawned with `investigation_label="treasury-cert-origins"`
2. Agent reads: `forensics/manifests/{YYYY-MM-DD}/` files
3. Manifests have `compass_edge` (N/S/E/W bearing) + `next_task_queued`
4. Agent follows bearing → discovers work autonomously (no SendMessage)
5. Agent writes manifest → signals next agent what to do next
6. Mission grows emergently via investigation_label clustering

**Graph query:**
```bash
# Find all manifests for a mission
grep -r "investigation_label.*treasury-cert-origins" forensics/manifests/

# See mission topology (which agents did what)
grep -r "compass_edge" forensics/manifests/ | grep "treasury-cert"

# Discover unfinished work
grep -r "discovered_work" forensics/manifests/ | grep -v "\[\]"
```

---

## Integration Points

### `/spawn` (0x_spawn.py)
- **Reads:** `faerie2-formulas.json` (wave thresholds)
- **Reads:** `~/.claude/altimeter.json` (context %)
- **Logic:** auto-determines W1/W2/W3 based on context fill
- **Outputs:** agents spawned, manifests written

### Bundle Emission Pressure (0x_bundle_emission_pressure.sh)
- **Trigger:** Presend hook (before agent spawn)
- **Reads:** `faerie2-formulas.json` (BUNDLE_EMISSION_CONTEXT_THRESHOLD)
- **Injects:** bundle-emission opportunity into agent prompt if remaining context > 30%

### Formulas (faerie2-formulas.json)
- **Mutation target:** WAVE_*_SPAWN_MAX_CONTEXT_PCT, BUNDLE_EMISSION_CONTEXT_THRESHOLD, quality gates
- **Protocol:** Measure baseline → Mutate → Measure post → Accept/Revert
- **Real measurements (2026-04-28):**
  - NECTAR: 1,204 tokens (theory 2-3K) → **40-60% cheaper**
  - HONEY: 200 tokens (theory 1,500) → **7.5x cheaper**

---

## Why This Matters (Equilibrium = f(0))

Traditional orchestration: Main context = high (planning, synthesis, routing) → Limited agents in flight → Bottleneck

Stigmergic orchestration (faerie2): Local rules (formulas) + filesystem coordination (manifests) → Zero main burden → Unlimited agents in flight

**This folder enables that:** Formulas are readable, mutable, measurable. Agents follow them autonomously. Main observes, doesn't orchestrate.

---

## See Also

- `faerie2-formulas.json` — All mutable parameters (wave thresholds, quality gates, reputation weights)
- `CONTEXT-GATING-OPERATIONAL.md` (mth00106) — How context % drives wave selection
- `BUNDLE-EMISSION-PRESSURE.md` (mth00107) — How remaining context drives bundle emission
- `MUTATION-CYCLE-GUIDE.md` (mth00087, in faerie2) — Framework for safe formula mutations
- `SPAWNING-DISCIPLINE.md` (mth00090, in faerie2) — Agent autonomy + stigmergy
