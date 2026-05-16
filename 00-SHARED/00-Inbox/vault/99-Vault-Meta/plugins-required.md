---
type: vault-meta
status: active
tags: [vault-meta, plugins, obsidian]
parent: "[[99-Vault-Meta/INDEX]]"
up: "[[INDEX]]"
created: 2026-04-25
updated: 2026-04-25
doc_hash: sha256:56d4699c88c41faf90eec69a23a7cb5c8fdf5dcb6146bd4eaa5ff060d76f16b6
hash_ts: 2026-04-25T01:10:54Z
hash_method: body-sha256-v1
---

> [up Parent](./INDEX.md) · [home Vault Index](../INDEX.md)

# Required Plugins — faerie2 Vault

This vault depends on the following Obsidian community plugins. Install all before using live dashboards, diagrams, or structured navigation.

**Templater is NOT used in this vault.** The templating path here is Blueprint + Nunjucks. Do not install Templater — its syntax conflicts with Blueprint templates.

---

## Plugin Inventory

### breadcrumbs

**Plugin ID:** `breadcrumbs`
**Author:** SkepticMystic
**Install:** Settings > Community Plugins > Browse > search "Breadcrumbs"

**Purpose in this vault:**
Hierarchical navigation via frontmatter fields `parent`, `up`, `child`. Every note in this vault includes at minimum `parent:` and `up:` frontmatter pointing to the note above it in the hierarchy. Breadcrumbs reads these to render a breadcrumb trail at the top of each note and an expandable tree view in the sidebar. The `> [up Parent] · [home Index]` lines in note headers are human-visible complements to the machine-readable frontmatter.

**Required frontmatter fields:**
- `up:` — immediate parent in hierarchy (e.g. `"[[00-SHARED/INDEX]]"`)
- `parent:` — same as `up:` (breadcrumbs reads both; redundancy is intentional for compatibility)
- `child:` — optional, list of child notes

---

### obsidian-excalidraw-plugin

**Plugin ID:** `obsidian-excalidraw-plugin`
**Author:** Zsolt Viczian
**Install:** Settings > Community Plugins > Browse > search "Excalidraw"

**Purpose in this vault:**
Diagrams for Hive narratives, architecture overviews, and dashboard visual elements. Excalidraw files live alongside their referencing notes as `.excalidraw.md` files (Obsidian-native format). Used in:
- `00-SHARED/Hive/` — architecture diagrams for f(0) and piston wave visualizations
- `00-SHARED/Dashboards/` — visual layout sketches embedded in dashboard notes

**Convention:** Embed diagrams with `![[diagram-name.excalidraw]]` syntax. Keep Excalidraw files in the same folder as the referencing note, or in a `diagrams/` subfolder when a note accumulates multiple drawings.

---

### juggl

**Plugin ID:** `juggl`
**Author:** Emile van Krieken
**Install:** Settings > Community Plugins > Browse > search "Juggl"

**Purpose in this vault:**
Advanced graph view for concept relationships. Where Obsidian's built-in graph shows all notes as undifferentiated dots, Juggl renders typed edges (parent/child/sibling) with configurable visual styles. Used to explore the stigmergy graph — how manifests, tasks, and agents connect across the forensics tree.

**Configuration notes:**
- Enable "Use Breadcrumbs relations" in Juggl settings to inherit the `up/parent/child` edge types already defined for Breadcrumbs
- Juggl local graph (workspace mode) is the primary use case — global graph with all 500+ notes is noise

---

### quickadd

**Plugin ID:** `quickadd`
**Author:** Christian Bager Bach Houmann
**Install:** Settings > Community Plugins > Browse > search "QuickAdd"

**Purpose in this vault:**
Rapid capture for droplets and working notes. QuickAdd macros provide hotkey-triggered note creation without navigating the vault file tree. Primary use cases:
- One-hotkey droplet creation: prompts for a title, inserts a timestamped entry into `00-SHARED/Droplets/LIVE-{date}.md`
- Quick task stub: prompts for task title + priority, appends to today's pollen file
- Quick capture to inbox: free-form note with auto-date frontmatter

**Setup:** QuickAdd choices are defined in Settings > QuickAdd. The vault ships a starter set of choices in `99-Vault-Meta/quickadd-choices.json` (import via QuickAdd settings if available, otherwise recreate manually).

---

### obsidian-linter

**Plugin ID:** `obsidian-linter`
**Author:** Victor Tao (platers)
**Install:** Settings > Community Plugins > Browse > search "Linter"

**Purpose in this vault:**
Enforces frontmatter and heading conventions automatically on save. Configured to:
- Ensure every note has `created:` and `updated:` frontmatter (adds missing, updates `updated:` on every save)
- Normalize heading levels (H1 = document title only, H2+ for sections)
- Remove trailing whitespace and ensure single blank line before/after headings
- Enforce `tags:` as a YAML list (not inline string)

**Critical:** Linter does NOT add `doc_hash:` frontmatter — that is written by `stamp_doc_hash.py` and must not be overwritten by Linter. Configure Linter to skip `doc_hash` in Settings > Linter > Frontmatter > "Ignore frontmatter keys": `doc_hash, hash_ts, hash_method`.

---

### blueprint

**Plugin ID:** `blueprint`
**Author:** François Vaux (madx)
**Install:** Settings > Community Plugins > Browse > search "Blueprint"

**Purpose in this vault:**
Templating engine using Nunjucks syntax — the chosen templating path for new document scaffolds. Blueprint templates live in `.blueprint` files and are applied to notes via frontmatter (`blueprint: "template-name"`). When you run "Apply template" on a note, Blueprint renders the Nunjucks template and fills in the note's structure while preserving existing content in designated sections.

**Why Blueprint over Templater:**
Templater uses its own `<%` tag syntax that conflicts with other tools and is harder to read. Blueprint uses Nunjucks (`{{ variable }}`, `{% block %}`) — a well-documented, industry-standard templating language with a large reference ecosystem. Nunjucks templates are more readable, composable, and testable outside Obsidian.

**Do not install Templater.** Blueprint covers all scaffold use cases in this vault.

**Blueprint templates** live in `99-Vault-Meta/blueprints/`:
- `note.blueprint` — standard note with full frontmatter
- `dashboard.blueprint` — dashboard with Dataview block placeholders
- `agent-run.blueprint` — agent run record template

---

### dataview

**Plugin ID:** `dataview`
**Author:** Michael Brenan (blacksmithgu)
**Install:** Settings > Community Plugins > Browse > search "Dataview"

**Purpose in this vault:**
Live-querying frontmatter for dashboards. Dataview reads YAML frontmatter from all notes in the vault and makes it queryable via DQL (Dataview Query Language) and DataviewJS (JavaScript API). Used in:
- `00-SHARED/Dashboards/agent-eval-LIVE.md` — queries eval sidecar notes from `_manifest-index/`
- `00-SHARED/Dashboards/queue-state-LIVE.md` — queries queue sidecar notes
- `00-SHARED/Dashboards/phase-progress-LIVE.md` — queries phase notes
- `00-SHARED/Dashboards/stigmergy-state-LIVE.md` — queries manifest sidecars for chain health

**Required settings:**
- Enable JavaScript queries (Settings > Dataview > Enable JavaScript Queries): ON
- Inline queries: ON
- Automatic view refresh: ON (so dashboards re-render when sidecar files update)
- Inline field highlighting: optional

**Data source model:** Dataview queries vault markdown files — it cannot directly query JSON. Sidecar scripts (`9x_manifests_to_vault_index.py`, `9x_queue_to_vault_index.py`) convert JSON forensic data into vault markdown files with frontmatter. Dataview queries the sidecars. This is the intended pattern: sidecars bridge forensics (JSON) to vault (markdown).

---

## Install Checklist

1. Open Settings > Community Plugins
2. Disable "Safe mode" if not already done
3. Click "Browse"
4. For each plugin below, search by name, install, and enable:

| Plugin Name | Plugin ID | Status |
|---|---|---|
| Breadcrumbs | `breadcrumbs` | Required |
| Excalidraw | `obsidian-excalidraw-plugin` | Required |
| Juggl | `juggl` | Required |
| QuickAdd | `quickadd` | Required |
| Linter | `obsidian-linter` | Required |
| Blueprint | `blueprint` | Required |
| Dataview | `dataview` | Required |

**Do NOT install:** Templater (conflicts with Blueprint/Nunjucks syntax), Obsidian-Brain (superseded by Juggl for this vault's purposes).

---

## Post-Install Configuration

After installing all plugins:

1. **Linter:** Add `doc_hash, hash_ts, hash_method` to ignored frontmatter keys (prevents overwriting forensic hash stamps)
2. **Breadcrumbs:** Set "Default relation" to `up` in Breadcrumbs settings
3. **Dataview:** Enable JavaScript Queries and Automatic view refresh
4. **Juggl:** Enable "Use Breadcrumbs relations" for consistent edge types
5. **QuickAdd:** Import choices from `99-Vault-Meta/quickadd-choices.json` or create manually

---

*Generated by documentation-engineer | task-vault-FFFF-plugins-live-dashboards | 2026-04-25*
