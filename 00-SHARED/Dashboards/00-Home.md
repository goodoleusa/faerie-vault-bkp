---
type: dashboard
tier: home
title: "Swarmy Home — f(0) Overview & Bird's-Eye Navigation"
status: live
cssclasses: [wide-page, dashboard-home]
refresh_cadence: per-session
S: ['[01-Today](01-Today.md)', '[02-Missions-Emergent](02-Missions-Emergent.md)', '[03-Anchors](03-Anchors.md)', '[04-Eval-Dimensions](04-Eval-Dimensions.md)', '[05-Stigmergy](05-Stigmergy.md)']
E: ['[VAULT-STRUCTURE](../VAULT-STRUCTURE.md)', '[Compass-Graph](Compass-Graph.md)', '[VAULT-MAP](VAULT-MAP.excalidraw.md)']
tags: [dashboard, home, swarmy, orientation]
---

> **🐝 Navigate:** [00 Home](00-Home.md) · [01 Today](01-Today.md) · [02 Missions](02-Missions-Emergent.md) · [03 Anchors](03-Anchors.md) · [04 Eval Dimensions](04-Eval-Dimensions.md) · [05 Stigmergy](05-Stigmergy.md) · [VAULT-MAP](VAULT-MAP.excalidraw.md)

# Swarmy Home — f(0) Overview

> The vault you're reading is **a collaborative substrate** where you and AI work side-by-side. AI proposes — drafts, mission graphs, evidence trails, evaluations. You curate, annotate, redirect, ignore. Both contributions are first-class. Neither overwrites the other. Every change is forensically tracked.

Sentence-trail summary of today's hive state. Mission clusters, recent anchors,
eval dimension scores. FFFF structure: Findings · Flags · Friction · Flow.

---

## 🌱 Learning paths

```dataviewjs
const paths = dv.pages('#path/onboarding').sort(p => p['path-step'])
dv.table(['Step', 'Note', 'Summary'],
  paths.map(p => [p['path-step'] ?? '?', dv.fileLink(p.file.path), p.summary ?? '']))
```

---

## 🐝 Hive actions (Meta Bind)

```meta-bind-button
label: 🐝 Spawn manifest
id: faerie-spawn
style: primary
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const charter = await app.vault.adapter.read('forensics/charters/active.txt').catch(() => 'default');
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_spawn', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({ charter_ref: charter.trim() })
      });
      new Notice(r.ok ? '🐝 manifest spawned' : '⚠ ' + r.status);
```

```meta-bind-button
label: 📊 Refresh metrics
id: faerie-metrics
style: default
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_metrics', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (!r.ok) { new Notice('⚠ ' + r.status); return; }
      const data = await r.json();
      const out = '00-SHARED/Dashboards/_metrics-latest.md';
      await app.vault.adapter.write(out, '```json\n' + JSON.stringify(data, null, 2) + '\n```\n');
      new Notice('📊 metrics → ' + out);
```

```meta-bind-button
label: 🌼 Mirror today
id: faerie-mirror
style: default
actions:
  - type: inlineJS
    code: |
      const tokenPath = '.faerie-token';
      let tok = '';
      try { tok = (await app.vault.adapter.read(tokenPath)).trim(); } catch(e) { new Notice('Set ' + tokenPath + ' first'); return; }
      const today = new Date().toISOString().slice(0,10);
      const r = await fetch('https://api.retrofuture.tech/tools/faerie_vault_mirror_daily', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: today })
      });
      new Notice(r.ok ? '🌼 mirrored ' + today : '⚠ ' + r.status);
```

---

## 💎 Lifecycle ladder

> Read the crystals, not the volume. See [[../HELP/crystallization-workflow|crystallization workflow]] and [[../Faerie-System-Internals/Sync-Scripts/PROMOTION-PIPELINE|promotion pipeline]].

**Time tiers (volume → crystal):**

- 📌 **Today** — atomic notes: [[../Daily/_index|Daily/]]
- 🗓️ **This week** — [[../Weekly/_index|Weekly digests]]
- 📆 **This month** — [[../Monthly/_index|Monthly digests]]
- ⚓ **Anchor set** — [[../Anchors/_index|Anchors/]] (permanent principles)
- 🍯 **Honey droplets** — [[../Honey/_index|Honey/]] (crystallized memory)
- 📜 **Charters** — [[../Charters/_index|Charters/]] (declared intent)

**Promotion pipeline (ephemeral → canonical, mirrors `faerie2/forensics/`):**

- 🌼 **Ephemeral** — [[../Ephemeral/_index|Ephemeral/]] (agent scratch, only writable path)
- 📌 **Manifests** — [[../Manifests/_index|Manifests/]] (work cells, symlink overlay)
- ⬡ **Artifacts** — [[../Artifacts/_index|Artifacts/]] (work products, symlink overlay)
- 📦 **Bundles** — [[../Bundles/_index|Bundles/]] (spawn context, symlink overlay)
- 🔗 **COC entries** — [[../COC-Entries/_index|COC-Entries/]] (hash-chained audit)
- 🧑 **Human** — [[../Human/_index|Human/]] (your annotations, parallel COC chain)

```dataviewjs
const today = new Date().toISOString().slice(0,10);
const week = (() => {
  const d = new Date(); d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
  const wk = Math.ceil((((d - yearStart) / 86400000) + 1)/7);
  return `${d.getUTCFullYear()}-W${String(wk).padStart(2,'0')}`;
})();
const month = today.slice(0,7);
dv.table(['Tier','Pointer'], [
  ['📌 Daily', `[[../Daily/${today}/_index|${today}]]`],
  ['🗓️ Weekly', `[[../Weekly/${week}/_index|${week}]]`],
  ['📆 Monthly', `[[../Monthly/${month}/_index|${month}]]`],
  ['⚓ Anchors', '[[../Anchors/_index|view set]]'],
  ['🍯 Honey', '[[../Honey/_index|view droplets]]'],
]);
```

---

## FFFF (today)

- **Findings:** see [[01-Today]]
- **Flags:** see [[03-Anchors]] (status=proposed)
- **Friction:** see [[04-Eval-Dimensions]] (low-trend dimensions)
- **Flow:** see [[05-Stigmergy]] (discovered_work density)

---

## 🗺️ Top-level orientation (bird's-eye)

The vault is organized by **purpose tier**, not by topic. Find what you want by asking *what kind of artifact* it is:

| Tier | Folder | What lives here |
|---|---|---|
| **00** Shared dashboards | `00-SHARED/Dashboards/` | This file + 01-Today, 02-Missions, 03-Anchors, 04-Eval, 05-Stigmergy. Read in order |
| **00** Inbox | `00-Inbox/` | Anything not yet sorted. Triage regularly |
| **01** Memories | `01-Memories/` | NECTAR entries, HONEY droplets, personal anchors |
| **01** Protected | `01-PROTECTED/` | Write-restricted canonical artifacts |
| **02** Skills | `02-Skills/` | Agent skill descriptions (vault-side mirror of `.agents/skills/`) |
| **03** Agents | `03-Agents/` | Per-agent reputation, journals, gifts |
| **10** Investigations | `10-Investigations/` | Deep-dive cases with their own forensic trails |
| **80** Publications | `00-Publications/` | Polished session-end narratives, vault-canonical for humans |
| Excalidraw | `Excalidraw/` | Drawing canvas files — see vibe-coding section below |
| Blueprints | `Blueprints/` | Nunjucks templates the plugin renders against frontmatter |
| Narratives | `Narratives/` | Long-form reflections and explainers |

**The 60-second orientation test:** open this file. Read the FFFF section. Click into [[01-Today]] to see what shipped. Click into [[02-Missions-Emergent]] to see active charters. That's your bearings.

---

## ✏️ Vibe-coding canvas (Excalidraw bearing topology)

The big idea: **sketch your knowledge graph the way you'd vibe-code a UI.** Drag colored shapes around for your N/S/E/W bearings, hit *commit topology*, the plugin reads colors back and writes the structure into your note frontmatter. Re-sketch tomorrow if it doesn't feel right.

**Workflow:**

1. **Open** `[[VAULT-MAP.excalidraw.md]]` (or any `.excalidraw.md` file in `Excalidraw/`)
2. **Drop colored shapes** for nodes — color encodes bearing:
   - 🔴 **Red** = North (unblock — prerequisite work that needs to ship first)
   - 🟢 **Green** = South (ship — downstream deliverables)
   - 🔵 **Blue** = East (parallel — sister missions at the same level)
   - 🟣 **Purple** = West (re-baseline — return to assumptions)
3. **Connect with arrows** — direction encodes dependency
4. **Label nodes** — text inside each shape becomes the task_id / charter_id / artifact name
5. **Run command** `Swarmy: commit Excalidraw topology` (Cmd/Ctrl+P → search)
6. The plugin **scans colors + labels**, writes a `bearings: {N: [...], S: [...], E: [...], W: [...]}` block into the frontmatter of the linked note
7. Mission graph in repo (`forensics/mission-graph.json`) accretes the new edges via MCP sync

**Soft-dependency note:** Excalidraw is an optional plugin. Install via Settings → Community Plugins → search "Excalidraw" → install. Without it, the vibe-coding workflow degrades gracefully (you get a prompt to install). Without Excalidraw, the plugin still works for everything else (charters, manifests, blueprints, dashboards).

**Excalibrain** (also optional): neural-graph view of your bearings. Install for visual compass; without it, the plugin renders a Mermaid fallback.

**Existing canvas files:**
- [[VAULT-MAP.excalidraw.md]] — the master vault topology
- `Excalidraw/system-design.excalidrawlib` — reusable system shapes
- `Excalidraw/software-architecture.excalidrawlib` — reusable architecture shapes

---

## 📊 Metrics, insights, findings, FFFF

The vault tracks four metric families simultaneously. Click each link for the dashboard:

### Internal evolution (F-series — Faerie vs Faerie over time)

- **f(0) Queen Burden** — fraction of work done by main thread vs delegated agents. North star = 0 (full autonomy). See [[04-Eval-Dimensions]].
- **Bearing diversity (Shannon entropy)** — how spread are your missions across N/S/E/W? Target ≥0.87 (healthy mix). See [[05-Stigmergy]].
- **Mutation fitness** — % of agent cuts that survive review vs are rolled back. Target ≥0.85.
- **Discovery depth** — fraction of agents that surface `discovered_work[]` items in their manifests.
- **Mission completion velocity** — charter deliverables shipped / week.

Full formula catalog: [[../Faerie-System-Internals/Formulas/00-FORMULAS-CANONICAL]] (or in repo: `docs/00-FORMULAS-CANONICAL.md`).

### External benchmark (M-series — Swarmy vs competitors)

15 metrics M1–M15 covering token efficiency, latency, coverage, calibration, safety, etc. Run via the `swarmy_log_metric` MCP tool. Data flows to W&B project `swarmy-eval-testing`.

### System health (A–G dimensions)

7 dimensions for production readiness. Eval engine: `scripts/3x_eval_dimensions.py`. Dashboard: [[04-Eval-Dimensions]].

### FFFF (qualitative weekly read)

- **Findings** — concrete artifacts shipped this week (charters, manifests, publications)
- **Flags** — concerns that surfaced — security, drift, regression
- **Friction** — what was harder than it should have been
- **Flow** — what enabled momentum — discovered patterns, unblocked work

The 4 buttons at the top of this page (Spawn manifest, Refresh metrics, Mirror today) trigger live MCP calls. They write to `.faerie-token` for auth.

---

## 🐝 The swarmy-hive-plugin commands

Open command palette (Cmd/Ctrl+P) and search "Swarmy:" — your full toolkit:

| Command | What it does |
|---|---|
| `Swarmy: render blueprint to current note` | Apply a Blueprint template against this note's frontmatter |
| `Swarmy: render blueprint to clipboard` | Render without writing — preview |
| `Swarmy: commit Excalidraw topology` | Read bearing colors → write frontmatter (see vibe-coding above) |
| `Swarmy: propose bearings from folder` | Scan folder, MCP suggests N/S/E/W edges |
| `Swarmy: open chat panel` | Inline chat with swarmy MCP from inside Obsidian |
| `Swarmy: charter dashboard` | Live view of active charters + their journey logs |
| `Swarmy: PDF export current note` | Print-style PDF using vault styling (no external lib) |
| `Swarmy: open home` | Jumps back to this page |
| `Swarmy: design folder bearings` | Excalidraw workflow for a folder (optional plugin) |

**One plugin philosophy:** swarmy-hive-plugin vendors Blueprint/Nunjucks templating, Breadcrumbs relation resolution, and a Dataview subset internally. The only optional plugins are Excalidraw + Excalibrain (canvas-heavy; too substantial to vendor). See `THIRD_PARTY_NOTICES.md` in the plugin repo for full vendoring credits.

---

## 📍 The dashboard catalog (where every view lives)

The vault has many dashboards — each does one thing well. Click a section to jump in. Every dashboard has nav-pills at the top to hop between them.

### 🏠 Orientation (start here)

| Dashboard | What it tells you / does | Where it fits |
|---|---|---|
| [[00-Home]] (this page) | Bird's-eye orientation, FFFF, vibe-coding intro, dashboard catalog | First read after Obsidian opens |
| [[HOME]] | Vault-level entry point (older — being merged with this page) | Legacy; click into 00-Home instead |
| [[../START-HERE]] | The philosophy: AI as collaborator, vault as substrate | Read once when new |
| [[VAULT-STRUCTURE]] | Text-mode folder map | When you forget where something lives |
| [[VAULT-MAP.excalidraw\|VAULT-MAP]] | Visual map (Excalidraw vibe-coding canvas) | When you want to SEE the topology |

### 📌 Daily pulse (changes every session)

| Dashboard | What it tells you / does |
|---|---|
| [[01-Today]] | Today's findings, shipped artifacts, FFFF for the day |
| [[piston-status]] | Current W1/W2/W3 phase, context-pressure %, active spawns |

### 🎯 Mission layer (active work)

| Dashboard | What it tells you / does |
|---|---|
| [[02-Missions-Emergent]] | Currently-active charters + their journey logs |
| [[mission-control]] | Mission-graph compass view (N/S/E/W edges across all active work) |
| [[PRIORITY]] | What's next-on-deck per cluster_prefix routing |
| [[Compass-Graph]] | The mission DAG rendered as a bearing graph |

### ⚓ Knowledge anchors (long-horizon)

| Dashboard | What it tells you / does |
|---|---|
| [[03-Anchors]] | Permanent principles (status=anchored); proposed → review queue |
| [[01-Memories/00-META/MEMORY-INDEX\|MEMORY-INDEX]] | NECTAR + HONEY droplets ordered by age + confidence |

### ✍️ Publishing (your part of the loop)

| Dashboard | What it tells you / does |
|---|---|
| [[06-Publication-Worthy-Insights]] | Surfaces high-signal observations worth promoting from raw to publication |
| [[07-Publishing-Workflow]] | Your workflow: draft → edit → fact-check → sign-off. Per-phase queues |

### 📊 Metrics, eval, system health

| Dashboard | What it tells you / does |
|---|---|
| [[04-Eval-Dimensions]] | A–G system-health dimensions + F-series internal evolution metrics |
| [[Agent-Findings]] | Surface of agent-discovered findings across sessions |
| [[../Faerie-System-Internals/Formulas/00-FORMULAS-CANONICAL\|Formula catalog]] | All 33 formulas (governance + F1-F15) with current params + tweak protocols |

### 🌊 Stigmergy, flow, emergence

| Dashboard | What it tells you / does |
|---|---|
| [[05-Stigmergy]] | discovered_work density across active missions; flow patterns |
| [[../Hive/00-OVERVIEW\|Hive Overview]] | The hive's high-level state; archetype mix; spawn cadence |
| [[../Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK\|Agent Insights]] | What agents are observing about their own work |

### 🗂️ Indexes (when you want a list of lists)

| Dashboard | What it tells you / does |
|---|---|
| [[../00-META/DASHBOARD-INDEX\|DASHBOARD-INDEX]] | Auto-indexed list of all dashboards by mtime |
| [[../00-META/AGENT-INDEX\|AGENT-INDEX]] | All agent types + their reputation + recent work |
| [[../00-META/INDEX\|INDEX]] | Vault-wide index |
| [[../00-META/QUEUE-INDEX\|QUEUE-INDEX]] | Active spawn queues + claim TTL |
| [[Dashboards]] | Meta-doc about dashboards (older — will fold into 00-Home) |

### 📅 Session snapshots (historical reference)

Date-stamped dashboards capturing specific moments. Browse `00-SHARED/Dashboards/2026-*` for the full set:
- `2026-05-01-accountability-build.md` — accountability framework as of build date
- `2026-05-03-archetype-measurement-framework.md` — measurement framework at archetype-stabilization point

### Cross-dashboard nav (the every-dashboard-links-to-every-dashboard goal)

Every dashboard SHOULD have a nav-pill row at the top like this page's `🐝 Navigate:` line. **This is partial today** — the 5 numbered dashboards (00-05) have them; the rest don't. **Next-wave deliverable** (queued in vault-utils-bundling): the swarmy-hive-plugin adds a `Swarmy: insert nav pills` command that scans this catalog and writes a consistent navigation row into any dashboard, plus a content-script that auto-applies it on file open (similar to the home-page-on-startup pattern).

---

## 🚀 Onboarding paths

**If you're new to this vault:**
1. Read this page (you're here)
2. Read [[../START-HERE]] for the philosophy
3. Read [[../HOW-SYNC-WORKS]] for the repo ↔ vault protocol
4. Read [[../EMERGENCE-FRAMEWORK]] for the bearing system
5. Read [[../TERMINOLOGY]] for the lexicon
6. Try the vibe-coding workflow on [[VAULT-MAP.excalidraw.md]]

**If you're an AI agent reading this:**
1. Identify your `agent_type` and check for a keypair at `forensics/reputation/keys/{agent_type}.{pub,key}`
2. Read `.agents/skills/charter-discipline/SKILL.md` and `.agents/skills/spawn/SKILL.md` for the canonical discipline
3. Use canonical writers (`scripts/0x_manifest_writer.py`, `scripts/_charter_lib.py`) — never inline-write to `forensics/ephemeral/`
4. Read the active charter for your mission via `swarmy_charter(verb="get", charter_id=...)`
5. End your work with a `completion_choice` from the canonical 13 kinds

---

*Bird's-eye view last refreshed: 2026-05-21. This page is the vault's first orientation. If you can't get your bearings in 60 seconds from this file, the synthesis is failing its job — flag and improve.*
