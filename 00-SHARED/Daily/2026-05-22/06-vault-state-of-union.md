---
type: state-of-union
status: active
last_updated: 2026-05-22
author: agent-b
purpose: vault-wide audit + recommendations + integration plan
related: [00-HOME.md, 07-unified-vault-ux-flow.md]
---

# 🏛 Vault State of the Union — 2026-05-22

> A full audit of `/mnt/d/0local/faerie-vault/` written for two readers:
> (1) the operator (goodoleusa) deciding what to fold in next, and
> (2) the next agent walking in cold and needing the 60-second orientation.
>
> If you only read one section, read **§5 Recommendations**.

---

## 1. Current vault structure (tree summary)

```
faerie-vault/
├── 00-HOME.md                    ← landing page, last_updated 2026-05-22
├── 00-SHARED/                    ← the live working surface
│   ├── PUBLISHING-DASHBOARD.md   ← THE daily (human final gate)
│   ├── Architecture/             ← 2 files (ARCH-001, REGISTRY)
│   ├── CybertemplatePUBLISH/     ← 6 status buckets (drafts/reviewing/
│   │                               annotating/ready-to-publish/
│   │                               published/imports-staging); 5 of 6
│   │                               are empty — only imports-staging
│   │                               has _INVENTORY.md
│   ├── DAILYFOLDERS/             ← legacy date-folder convention
│   │   ├── agents/2026-05-04/    ← one test agent leftover
│   │   └── system/               ← empty
│   ├── Daily/                    ← the live narrative convention
│   │   ├── 2026-05-02/           ← prior session
│   │   └── 2026-05-22/           ← TODAY: 01-05 narratives + this file (06)
│   ├── Emerg Deep-Dives/         ← Dev-Eval archive (2026-05-01..04),
│   │                               MANIFEST.json, Mission-Control.md
│   └── Hive/Mission-Control.md   ← STALE (last touched 2026-05-03)
├── 2026-04-28/                   ← archive — old date-folder convention
├── 2026-05-10/                   ← (empty)
├── mission-graph/                ← read-only mirror of stigmergic graph
│                                   (26 .md files, ship-* + audit-* + equil-*)
└── ONBOARDING/2026-04-29-b2-setup ← single onboarding artifact
```

**Counts:** 100 .md files total; 58 at depth ≤2. `.obsidian/plugins/`
holds breadcrumbs, dataview, excalibrain, obsidian-style-settings,
quickadd (5 plugins, all enabled).

---

## 2. What's folded in vs not (swarmy-vault-template merge)

`/mnt/d/0local/gitrepos/swarmy-vault-template/` ships a clean
five-shelf opinionated layout that the operational vault has only
partially adopted:

| Template shelf | In operational vault? | Status |
|---|---|---|
| `_meta/` (charter-template.json, manifest-template.json, cluster-prefixes.md, schemas/, microagents/) | ❌ MISSING | **FOLD IN** — charters cannot validate without templates |
| `00-Welcome/` (01-quickstart, 02-your-first-charter, 03-the-six-microagents) | ❌ MISSING | **FOLD IN** — `00-HOME.md` references no quickstart for charters |
| `10-Charters/{active,closed,drafts}/` | ❌ MISSING | **FOLD IN** — charters currently live in `forensics/charters/` repo-side; vault has no surface |
| `20-Inspirations/` | ❌ MISSING | optional — vault has `Emerg Deep-Dives/` which overlaps |
| `30-Synthesis-Log/` | ❌ MISSING | optional — Daily/{date}/ serves this role today |
| `80-Publications/` (empty .gitkeep) | ❌ MISSING | **FOLD IN** — eventual sink for published artifacts |

This Cut folds in the four marked **FOLD IN** items, skips the two
optional shelves (operator can adopt later if Daily/ overflows).

---

## 3. CybertemplatePUBLISH inventory + CyberOps-UNIFIED roundup

**Today (2026-05-22):**

- `drafts/`, `reviewing/`, `annotating/`, `ready-to-publish/`,
  `published/` — all **EMPTY**. No work in flight in any bucket.
- `imports-staging/` — contains only `_INVENTORY.md` (operator's
  cyber-ops roundup queue).

**Status:** the publish pipeline is wired (00-HOME + dashboard +
`swarmy-*` CLI aliases) but the buckets are not yet seeded. The
CyberOps-UNIFIED roundup mentioned in the mandate is **still pending
in `imports-staging/`** — agents have not promoted any item out of
the inventory toward drafts/. This is a clear seed-the-pump task for
the next session.

---

## 4. Existing dashboards inventory + status

| Dashboard | Path | Last touched | Status |
|---|---|---|---|
| **HOME** | `00-HOME.md` | 2026-05-22 | LIVE — primary entry |
| **Publishing Dashboard** | `00-SHARED/PUBLISHING-DASHBOARD.md` | 2026-05-22 | LIVE — daily gate |
| **CybertemplatePUBLISH README** | `00-SHARED/CybertemplatePUBLISH/README.md` | recent | LIVE (per HOME tier-2) |
| **Hive Mission-Control** | `00-SHARED/Hive/Mission-Control.md` | 2026-05-03 | STALE — needs nightly MCP cron revive |
| **Dev-Eval Index** | `00-SHARED/Emerg Deep-Dives/Dev-Eval/index.md` | varies | MOSTLY ARCHIVE — eval moved to V0 Tune tab |
| **Emerg Deep-Dives MC** | `00-SHARED/Emerg Deep-Dives/Mission-Control.md` | 2026-05-15 | DUPLICATE of Hive MC — archive candidate |
| **Vault Ops Dashboard 2026-04-28** | `2026-04-28/00-DASHBOARD.md` | 2026-04-28 | ARCHIVED — forensic snapshot |
| **Vault Maintenance (archived 2026-04-30)** | `2026-04-28/archive/10-vault-maintenance.md` | 2026-04-30 | SELF-MARKED ARCHIVED |

Full audit lives at `00-SHARED/Daily/2026-05-22/05-dashboard-audit.md`.

---

## 5. Obsidian plugin posture

`.obsidian/plugins/` enabled set (5):

- **breadcrumbs** — graph relations (up/down/same/prev)
- **dataview** — query/render frontmatter blocks
- **excalibrain** — visual brain map (graph-of-notes)
- **obsidian-style-settings** — theme/CSS tunables
- **quickadd** — macro-driven inserts

**Missing (recommended set per 00-HOME):** Longform, Templater,
Obsidian Git. These are mentioned as the "recommended set" in HOME
but not installed in the operational vault.

**Critical gap:** the canonical `swarmy-hive-plugin` (Persistech repo
at `/mnt/d/0local/gitrepos/swarmy-hive-plugin/`) is **NOT installed**
in the vault. HOME documents the install command:

```bash
git clone https://github.com/Persistech/swarmy-hive-plugin \
  $SWARMY_VAULT_PATH/.obsidian/plugins/hive
```

…but no `.obsidian/plugins/hive/` directory exists. The plugin ships
the two-layer canvas, commit-topology, chat-panel, charter-dashboard,
mcp-bridge — all the surfaces 00-HOME calls "the long-term canonical."
This is the single highest-leverage missing piece. **See Cut 3 for
the docker-side install plan.**

---

## 6. Open structural debt

1. **Legacy date-folder convention** (`2026-04-28/`, `2026-05-10/`,
   `00-SHARED/DAILYFOLDERS/`) sits parallel to the canonical
   `00-SHARED/Daily/{YYYY-MM-DD}/`. Either deprecate-with-redirect
   or archive into a single `_legacy/` shelf.

2. **Charter surface absent in vault** — charters live in
   `faerie2/forensics/charters/{active,closed,drafts}/`. Vault has
   no `10-Charters/` mirror. Folded in by Cut 2.

3. **CybertemplatePUBLISH buckets empty** — pipeline runs cold.
   `imports-staging/_INVENTORY.md` is the seed; an agent should
   promote items into `drafts/` to wake the dashboard up.

4. **Hive Mission-Control stale 18 days** — nightly MCP cron not
   wired. Adjacent mission, not in this cut's scope.

5. **`swarmy-hive-plugin` not installed inside the docker vault
   container.** Highest-leverage missing piece. Folded in by Cut 3.

6. **`.obsidian/community-plugins.json` missing** — the file Obsidian
   uses to mark community plugins enabled. The plugin folders exist
   but Obsidian may treat them as unregistered. Re-enable on first
   container open via Settings → Community Plugins → toggle each.

---

## 7. Recommendations (prioritized)

1. **Fold in the four template shelves** (`_meta/`, `00-Welcome/`,
   `10-Charters/{active,closed,drafts}/`, `80-Publications/`) — done
   by Cut 2 of this session.
2. **Install `swarmy-hive-plugin` inside the `swarmy-vault` docker
   container** — done by Cut 3, documented for one-time install.
3. **Wire vault into Hive dashboard via preview-pane (option B)** —
   done by Cut 4. iframe option rejected because vault-dev sits
   behind basic_auth (would need credential forwarding) and KasmVNC
   ships X-Frame-Options that block embedding.
4. **Seed CybertemplatePUBLISH** by promoting one inventory item
   from `imports-staging/` to `drafts/`. *(Adjacent mission — left
   as a discovered_work for the next agent.)*
5. **Archive legacy date-folder shelves** into `_legacy/`.
   *(Adjacent mission — left as a discovered_work for the next agent.)*
6. **Revive Hive Mission-Control** via nightly MCP cron writing the
   mission graph in markdown.
   *(Adjacent mission — left as a discovered_work for the next agent.)*

---

## 8. Where we were / are / are headed (60-second orientation)

- **Were:** vault was a flat working surface for narratives + a stale
  Hive dashboard; charters lived only in `forensics/` repo-side;
  plugin existed in a sibling repo but was not installed; Obsidian
  ran in docker but was not visible in the Hive web UI.
- **Are:** four template shelves folded in (Cut 2); plugin install
  path verified inside docker (Cut 3); Hive dashboard now has a
  vault preview pane (Cut 4); plugin gained light canvas elements
  (Cut 5); unified UX flow documented (Cut 6).
- **Headed:** operator opens swarmy.retrofuture.tech → sees vault
  pane inside Hive → clicks "Open Obsidian" → Obsidian opens with
  swarmy-hive-plugin already loaded → bliss. The remaining work is
  filling `10-Charters/active/` with real charters and seeding
  CybertemplatePUBLISH drafts.

---

*Companion docs:*
- `07-unified-vault-ux-flow.md` — end-to-end bliss flow
- `05-dashboard-audit.md` — dashboard inventory audit
- `forensics/ephemeral/2026-05-22/vault-state-of-union/manifest.json` — agent-b manifest
