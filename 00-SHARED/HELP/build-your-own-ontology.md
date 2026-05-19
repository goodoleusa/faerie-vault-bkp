# Build your own ontology

The Faerie hive plugin is built on four compass bearings: **N, S, E, W**.
Those four are universal. They are the *topology* of any directed-acyclic
work graph — prereq, deliverable, sibling, baseline. Every ontology in the
world that orders work or knowledge collapses into those four roles.

The **labels** are yours. "N" doesn't have to mean "unblock predecessor."
It can mean "cited source," "blocker," "hypothesis," "parent note," or
"waiting-for." Pick the vocabulary your domain already speaks.

## How it works

1. The plugin ships with 6 preset ontologies in `presets/`:
   - `faerie.yaml` — the canonical hive-mind framing (unblock / ship / parallel / baseline)
   - `gtd.yaml` — Getting Things Done (waiting-for / next-action / project / someday)
   - `zettelkasten.yaml` — atomic note linking (parent / child / sibling / structure)
   - `osint-investigation.yaml` — hypothesis / evidence / related-entity / counter-theory
   - `software-project.yaml` — blocker / shipped / parallel / design-decision
   - `academic-paper.yaml` — citation / claim / related-work / counter-argument

2. The active ontology lives at `vault/.hive/ontology.yaml`. It overrides
   the plugin defaults. **Internal data is unchanged**: frontmatter still
   uses `up:`, `down:`, `same:`, COC entries still log bearing=`N|S|E|W`,
   the MCP server still routes by `N/S/E/W`. Only the **display** surface
   (label text, glyph, color) reflects your ontology.

3. Switch with the command palette: **Faerie: switch ontology preset**.

## Example: GTD walkthrough

Say you live in David Allen's *Getting Things Done* world. You don't think
about "unblocking predecessors" — you think about contexts and next
actions. Switch to the GTD preset and the plugin re-skins:

| Bearing | Faerie default        | GTD label          | What it means in your workflow |
|---------|-----------------------|--------------------|---------------------------------|
| N       | unblock predecessor   | Waiting-for        | Blocked on someone else / external input |
| S       | conclude downstream   | Next action        | The next concrete physical action |
| E       | parallel sister       | Parallel project   | Active sister project at the same horizon |
| W       | return to baseline    | Someday/maybe      | Incubating — review during weekly review |

The bearing picker modal, the inline breadcrumb pills, the Excalidraw
compass overlay, the ExcaliBrain hierarchy — every UI surface now reads
"Waiting-for / Next action / Parallel project / Someday-maybe" while the
underlying graph stays N/S/E/W. Your data stays portable; agents and the
MCP server keep speaking the canonical bearing vocabulary.

## Roll your own

Drop a YAML in `presets/` (or directly into `.hive/ontology.yaml`):

```yaml
name: "my-ontology"
bearings:
  N: {label: "Upstream",   color: "#C73E1D", glyph: "⬆", role: "what came before"}
  S: {label: "Downstream", color: "#2E8540", glyph: "⬇", role: "what comes next"}
  E: {label: "Side track", color: "#FF8E3C", glyph: "➡", role: "parallel work"}
  W: {label: "Baseline",   color: "#FFB300", glyph: "⬅", role: "anchor / return point"}
callouts:
  - {id: "fact", icon: "check-circle", color_uses_bearing: S}
blueprint_pack: "my-pack"
```

Then run **Faerie: ontology doctor** to validate, and **Faerie: switch
ontology preset** to activate.

## Why four

Because every directed work graph has exactly four bearings relative to
any node: what came before (N), what comes after (S), what runs alongside
(E), and what anchors the whole thing (W). More bearings = arbitrary;
fewer = lossy. Four is the minimum complete set. The structure is fixed;
the words on top are yours.
