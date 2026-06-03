# `_meta/` — One-place truth for the swarmy ecosystem

This folder is the **single source of truth** for the vocabulary, colors,
templates, and path conventions that every swarmy surface — the Obsidian
plugin, the `swarmy-*` CLI, the dashboards, the charter cap hook — reads
from. Edit one file here, reshape every surface.

## Files

| File | Purpose |
|---|---|
| `swarmy.config.json` | The config every reader consults. Status vocab, bearing colors, card templates, cluster-prefix aliases, max active charters, vault path conventions. |
| `charter-template.json` | Canonical charter shape. New charters start as a copy of this. Schema-locked to `cluster_prefix.length === 3`. |
| `manifest-template.json` | Canonical agent-manifest shape. Mirrors `scripts/0x_manifest_writer.py` output. |
| `cluster-prefixes.md` | The doctrine behind `cluster_prefix` — why exactly 3 items, slot conventions, examples. |

## `swarmy.config.json` key reference

### `schema_version` (string)
Bumped when a key's meaning changes incompatibly. Readers should
`config.get(key, default)` so additive changes never break old readers.

### `status_vocab` (array of strings)
Publish-flow status values, **in order**. Read by:
- `swarmy-inbox` (CLI) — bucket order in the inbox listing
- `swarmy-status-set` (CLI) — validation allowlist
- `canvas-recursive.ts` (plugin) — Excalidraw status palette keys
- PUBLISHING-DASHBOARD.md Dataview queries — *(known gap; hardcoded, see Limitations)*

Current vocab: `draft → reviewing → annotating → ready-to-publish → published → sealed`.

### `bearing_colors` (object)
The four compass bearings (N/S/E/W) with their semantic label, hex
color, and archetype mapping. Read by:
- Plugin canvas commit-topology surfaces
- Mission-graph dashboards
- Hive bearing-badge UI

| Bearing | Label | Archetype | Meaning |
|---|---|---|---|
| N | unblock | NAVIGATOR | reverse-dependency; free a blocked upstream task |
| S | ship | MAKER | forward-dependency; ship the next deliverable |
| E | parallel | BRIDGE | sister work in the same mission, same DAG level |
| W | baseline | DEEP_DIVER | return to genesis; re-seat assumptions |

### `card_templates` (array of strings)
Canvas + dashboard card kinds the UI knows how to render. Read by the
plugin's canvas surface and the chat-mvp HivePanel card chooser.

### `completion_kinds` (array of strings)
Valid values for `manifest.completion_choice.kind`. Read by
`scripts/0x_manifest_writer.py` to validate manifest authorship.

### `cluster_prefix_aliases` (object)
Synonym map for `cluster_prefix` terms (`{from: to}`). Used by charter
genesis + neighbor-search to treat `gui` and `ui` as the same scope.

### `max_active_charters` (integer)
Soft cap on `forensics/charters/active/*.json`. Enforced by
`.openhands/hooks/9x_hook-charter-cap.py` as a stderr warning (never
blocks writes). Defaults to 15 if the config is missing.

### `vault_paths` (object)
Where canonical vault content lives. Lets surfaces compute paths
without baking literal strings into code.

## Who reads `swarmy.config.json`

| Surface | Keys consumed |
|---|---|
| `deploy/scripts/install-swarmy-aliases.sh` → `swarmy-inbox` | `status_vocab` |
| `swarmy-hive-plugin/src/canvas-recursive.ts` | `status_vocab`, `bearing_colors` |
| `.openhands/hooks/9x_hook-charter-cap.py` | `max_active_charters` |
| `scripts/0x_charter_genesis.py` | `max_active_charters` (CLI override available) |

## Limitations (queued follow-ups)

- **PUBLISHING-DASHBOARD.md** uses literal Dataview queries that hardcode
  the status vocab. To fix without breaking Dataview, a small Templater
  script could regenerate the dashboard's status sections from
  `swarmy.config.json` on save. *(Tracked as follow-up; see project
  CLAUDE.md or the next charter genesis pass.)*
- **chat-mvp dashboards** (V0/V4) load these values at build time via
  their own constants. A `vite-plugin` could inject `swarmy.config.json`
  at build to close that gap.
- **NEVER edit the hardcoded fallbacks in code without also updating
  the config**, or readers will silently diverge.

## Forward compatibility

Every reader implements `config.get(key, default)`. You can add keys
freely; old readers ignore them. Renaming a key is a breaking change —
bump `schema_version` and update every reader in the same commit.

## How to extend

1. Add the new key (with a sensible default at every reader) to
   `swarmy.config.json`.
2. Document the key in the **Key reference** section above.
3. Add the consumer surface to the **Who reads** table.
4. If the change is incompatible, bump `schema_version`.
