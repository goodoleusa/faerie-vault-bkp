---
type: home-landing
status: active
last_updated: 2026-05-22
purpose: vault-entry-point + full-nav for every dashboard
---

# 🏠 HOME — Swarmy Vault

> **Start every session here.** This page links every dashboard and
> tells you where to go next.

## 🧭 Inline nav (every dashboard, one click)

| | Dashboard | Purpose |
|---|---|---|
| 📰 | [[00-SHARED/PUBLISHING-DASHBOARD\|Publishing]] | Human-final-gate. Status buckets for everything in-flight. |
| 🔬 | [[00-SHARED/CybertemplatePUBLISH/README\|CybertemplatePUBLISH]] | Project-scoped publish workspace + imports staging |
| 🐝 | [[00-SHARED/Hive/Mission-Control\|Hive Mission-Control]] | Live mission graph (refreshed nightly via cron) |
| 📓 | [[00-SHARED/Daily\|Today's Daily Folder]] | New narratives land here (`swarmy-write` puts them) |
| 📊 | [[00-SHARED/Emerg Deep-Dives/Dev-Eval/index\|Dev-Eval index]] | Eval history (archive; live eval moved to V0 Tune tab) |
| 🎨 | [[_meta/README\|_meta config + templates]] | One-place config for visual language + ontology |
| 👋 | [[00-Welcome/01-quickstart\|Quickstart]] | First-time setup |

## ⚡ The 60-second orientation

Three folders cover 95% of the work:

- **`00-SHARED/`** — dashboards + Daily folder + CybertemplatePUBLISH. You'll live here.
- **`_meta/`** — the *one config* (`swarmy.config.json`) reshapes the system's visual language. Edit once → CLI + plugin + dashboards inherit.
- **`10-Charters/`** — active charters land here (mostly agent-written + signed; you read + occasionally curate).

The rest (`_legacy/`, `mission-graph/`, `ONBOARDING/`) is archive,
read-only mirror, or older onboarding — safe to skip on first pass.

**First action:** pin this tab + open the Publishing Dashboard in a
second tab (link above). Those two tabs are your home base.

---

## ⭐ Today's surfaces (pin these in your tab bar)

| Surface | Purpose | Open with |
|---|---|---|
| 📰 **[Publishing Dashboard](00-SHARED/PUBLISHING-DASHBOARD.md)** | Human-final-gate for everything in-flight. Status buckets (draft / reviewing / annotating / ready-to-publish / published) | Pin this — daily |
| 🔬 **[CybertemplatePUBLISH workspace](00-SHARED/CybertemplatePUBLISH/README.md)** | Project-scoped publish workspace for cybertemplate site. With imports-staging/ for CyberOps-UNIFIED roundup | Pin when working on cybertemplate |
| 📓 **[Today's Daily Folder](00-SHARED/Daily)** | Where new narratives land (`swarmy-write` puts them here) | Pin during active writing sessions |

---

## 🎨 Your visual language + ontology (one config, all surfaces)

Every status name, bearing color, card template, and cluster-prefix
alias used by the swarmy ecosystem flows from a single file:
**[`_meta/swarmy.config.json`](_meta/swarmy.config.json)**.

Edit that one file and you reshape every surface that consumes it —
the Obsidian Hive plugin's canvas palette, the `swarmy-inbox` CLI
buckets, and the soft cap on active charters all read from it at
runtime. New surfaces are wired through the same config (see the
follow-up list below for what isn't yet).

**What you can change there:**

- `status_vocab` — the publish flow ladder (default: `draft → reviewing → annotating → ready-to-publish → published → sealed`). Add a step, rename a step, or reorder.
- `bearing_colors` — N/S/E/W compass colors + archetype labels (Navigator / Maker / Bridge / Deep-Diver). Recolor the swarm.
- `card_templates` — canvas card kinds the UI can render (decker, parchment, bubble, door, spinner…).
- `cluster_prefix_aliases` — synonym map (`gui → ui`, `frontend → ui`). Stops merge-candidate analysis from missing kinship.
- `max_active_charters` — soft cap before the charter-cap hook warns you (default 15).
- `vault_paths` — where Daily / Publications / Charters / Shared live.

**Who reads it today:**

- `swarmy-hive-plugin` (Obsidian) — `canvas-recursive.ts` loads status + bearings at boot.
- `swarmy-inbox` CLI — loads the status vocabulary so buckets always match.
- `.openhands/hooks/9x_hook-charter-cap.py` — soft-warns when active charter count exceeds the cap.
- `scripts/0x_charter_genesis.py` — charter crystallization pass uses the same cap as default.

**Known gaps (queued follow-ups):**

- `PUBLISHING-DASHBOARD.md` Dataview queries still hardcode the status vocab — a small Templater script that regenerates the dashboard's status sections from the config would close this.
- The chat-mvp V0/V4 dashboards bake colors at build time — a `vite-plugin` injection of the config would unify them.

**Full key reference:** [`_meta/README.md`](_meta/README.md).

---

## 🧭 Full dashboard navigation

### Tier 1 — Daily (the focus surfaces)
- 📰 [Publishing Dashboard](00-SHARED/PUBLISHING-DASHBOARD.md) — **the daily**
- 📓 [Today's Daily Folder](00-SHARED/Daily) — narratives + synthesis logs

### Tier 2 — Project-scoped
- 🔬 [CybertemplatePUBLISH](00-SHARED/CybertemplatePUBLISH/README.md) — cybertemplate publish workspace
- 🐝 [Hive Mission-Control](00-SHARED/Hive/Mission-Control.md) — mission overview (stale — TODO: revive via nightly MCP cron)
- 📊 [Dev-Eval Index](00-SHARED/Emerg%20Deep-Dives/Dev-Eval/index.md) — eval history (mostly archive; eval surfaces moved to V0 Tune tab)

### Tier 3 — Weekly aggregate (queued — not yet built)
- 📅 Weekly Synthesis Dashboard *(coming — pulls past 7 days of daily + COC)*
- 📐 Cybertemplate Stage Dashboard *(coming — Tier-1/2/3 evidence counts + open promotions)*

### Archived dashboards (forensic reference, do not maintain)
- ~~[Emerg Deep-Dives Mission-Control](00-SHARED/Emerg%20Deep-Dives/Mission-Control.md)~~ — duplicate of Hive copy; delete or redirect
- [2026-04-28 Vault Ops Dashboard](_legacy/2026-04-28/00-DASHBOARD.md) — month-old forensic snapshot (shelved under `_legacy/`)
- [Vault Maintenance (archived 2026-04-30)](_legacy/2026-04-28/archive/10-vault-maintenance.md) — self-marked archived (shelved under `_legacy/`)

> Full audit + recommendations: [Dashboard Audit 2026-05-22](00-SHARED/Daily/2026-05-22/05-dashboard-audit.md)

---

## ✍️ The publish flow (read this once, then live in it)

```
swarmy-write <slug>            # creates today's note, status=draft
   ↓
swarmy-status-set <f> reviewing
   ↓
swarmy-status-set <f> annotating   # your voice goes on top
   ↓
swarmy-status-set <f> ready-to-publish
   ↓
swarmy-publish <file>          # sign + flip to published
   ↓
poll-deploy syncs to cybertemplate.retrofuture.tech (~5 min)
```

Check what's in each bucket with `swarmy-inbox`. Full alias suite
installed via `bash deploy/scripts/install-swarmy-aliases.sh` in the
faerie2 repo.

---

## 📚 Recent narratives (2026-05-22 — today)

- [01 — fast-evo skill reflection](00-SHARED/Daily/2026-05-22/01-fast-evo-skill-reflection.md)
- [02 — HONEY evolution narrative](00-SHARED/Daily/2026-05-22/02-honey-evolution-narrative.md)
- [03 — HONEY archeological dig](00-SHARED/Daily/2026-05-22/03-honey-archeological-dig.md) (1517 lines)
- [04 — HONEY v4 candidate ideas](00-SHARED/Daily/2026-05-22/04-honey-v4-candidate-ideas.md) (13 ideas)
- [05 — Dashboard audit](00-SHARED/Daily/2026-05-22/05-dashboard-audit.md)

---

## 🏗 Vault structure (quick map)

```
faerie-vault/
├── 00-HOME.md            ← you are here
├── _meta/                ← charter + manifest templates, cluster-prefixes
├── 00-Welcome/           ← quickstart, your-first-charter, microagents (NEW 2026-05-22)
├── 00-SHARED/            ← cross-project shared surface
│   ├── PUBLISHING-DASHBOARD.md   ← THE daily
│   ├── CybertemplatePUBLISH/     ← cybertemplate publish workspace
│   ├── Daily/                    ← dated narratives (NN-slug.md)
│   ├── Architecture/             ← architecture docs
│   ├── Hive/                     ← mission-control (revive target)
│   └── Emerg Deep-Dives/         ← eval + investigations
├── 10-Charters/          ← {active,closed,drafts}/ — charter authoring (NEW 2026-05-22)
├── 80-Publications/      ← published artifact sink (NEW 2026-05-22)
├── mission-graph/        ← stigmergic mission graph (read-only mirror)
├── ONBOARDING/           ← new-collaborator onboarding
└── _legacy/              ← shelved pre-2026-05-22 conventions (forensic; see _legacy/README.md)
```

> **`_legacy/` shelf** — Pre-2026-05-22 vault conventions
> (`2026-04-28/`, `2026-05-10/`, `00-SHARED/DAILYFOLDERS/`) have
> been moved under `_legacy/` to declutter the active vault root.
> They remain readable for forensic reference but are not active
> surfaces. See `_legacy/README.md` for the shelf manifest.

---

## 🔮 Where this is going

**The long-term canonical** for daily workflow is the
**[swarmy-hive-plugin](https://github.com/Persistech/swarmy-hive-plugin)**
(Obsidian plugin). It ships:

- Two-layer canvas (AI artifacts immutable + your annotations parallel)
- Commit-topology (sketch N/S/E/W bearings in Excalidraw → frontmatter)
- Steering layer (annotate live OR async-queue for next session)
- Plain-markdown forever (uninstall and notes still work)

The dashboards above + the `swarmy-*` CLI aliases are **interim**
until the plugin's daily workflow surfaces ship. When the plugin's
commit-topology + status-tag UI lands, the dashboards become
read-only reference and the CLI aliases stay as scripting helpers.

To install the plugin (in your vault):

```bash
git clone https://github.com/Persistech/swarmy-hive-plugin \
  $SWARMY_VAULT_PATH/.obsidian/plugins/hive
```

Then Obsidian → Settings → Community plugins → enable Hive.

---

## 🆕 First time here?

1. Pin **Publishing Dashboard** (00-SHARED/PUBLISHING-DASHBOARD.md) in your tab bar.
2. Install plugins (Longform, Dataview, Templater, Obsidian Git) — recommended set in the dashboard.
3. From the faerie2 repo on this machine, run:
   `bash deploy/scripts/install-swarmy-aliases.sh && source ~/.bashrc`
4. Try `swarmy-where` to see your paths + signer status.
5. Try `swarmy-write hello` to create your first note in today's daily folder.
6. Open the dashboard — your new note should appear in the **DRAFTS** bucket.

---

*Maintained at `00-HOME.md` (vault root). When you add a new
dashboard, add a link here in the appropriate tier. When you
deprecate a dashboard, move its link to the Archived section above.*
