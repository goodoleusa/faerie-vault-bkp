# Plugin Install Checklist — faerie-vault

**Generated:** 2026-05-19  
**Scope:** Plugins the faerie system expects but that may not yet be installed. Install via Obsidian → Settings → Community plugins → Browse.

---

## Currently installed in `faerie-vault`

| Plugin                       | Status      |
|------------------------------|-------------|
| dataview                     | installed   |
| quickadd                     | installed   |
| blueprint                    | installed   |
| breadcrumbs                  | installed   |
| obsidian-excalidraw-plugin   | installed   |
| juggl                        | installed   |
| obsidian-linter              | installed   |

## Needed in `faerie-vault` (install manually)

| Plugin                         | Why                                                          |
|--------------------------------|--------------------------------------------------------------|
| **Meta Bind** (`obsidian-meta-bind-plugin`) | Interactive frontmatter widgets in dashboards (N/S/E/W toggles, status pickers). |
| **Homepage** (`obsidian-homepage`)          | Auto-open dashboard at vault load — wires `00-Investigation-Home.md` as entry. |
| **Style Settings** (`obsidian-style-settings`) | Required by faerie CSS snippets for theme tuning.       |
| **Extended Graph** (`extended-graph`)       | Renders N/S/E/W edges with directional color/weight in the graph view. |
| **Excalibrain** (`excalibrain`)             | Alternative neighborhood view honoring the breadcrumbs hierarchy. |
| **BRAT** (`obsidian42-brat`)                | Required if you want bleeding-edge plugin tracks.            |

## Currently installed in `CyberOps-UNIFIED`

Full list (already adequately stocked):

dataview, quickadd, obsidian-homepage, file-title-updater, obsidian-excalidraw-plugin, excalibrain, obsidian-linter, blueprint, share-note, obsidian-style-settings, breadcrumbs, mermaid-tools, copilot, table-editor-obsidian, obsidian-kanban, automatic-table-of-contents, obsidian-meta-bind-plugin, obsidian-daily-named-folder, graph-banner, juggl, obsidian-chartsview-plugin, extended-graph

## Templater — DO NOT INSTALL

The faerie system deliberately avoids Templater (templating happens upstream via the hive frame, not in-vault). Verified absent from both vaults as of 2026-05-19.

If Templater is found present in any vault later, remove via Settings → Community plugins → toggle off → Uninstall. Do not delete its `data.json` manually — use Obsidian's UI.

## Install procedure

1. Open Obsidian for the relevant vault.
2. Settings → Community plugins → Browse.
3. Search exact plugin ID from the table.
4. Install → Enable.
5. After install, re-open the vault; faerie hooks will pick up the new `data.json` on next session.

## After-install sanity check

- Run `python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('.obsidian/plugins/*/data.json')]"` from vault root.
- Confirm Breadcrumbs side panel shows N/S/E/W tabs (matrix view).
- Confirm Linter respects `forensics/` ignore (open any forensics note, run Lint — should be no-op).
