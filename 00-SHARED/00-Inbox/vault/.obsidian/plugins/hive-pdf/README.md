# Hive PDF Export — Obsidian Plugin

Export the active note to a Hive-styled PDF with smart-sized Mermaid diagrams.
Insert ready-made Excalidraw templates. Surface all diagram/template commands from one launchpad.

No inference at runtime. Deterministic pipeline: mmdc → aspect-sizer → pandoc/xelatex.

## Changelog

### v1.2.0
- **INSERT-GRAPH FIX**: templates converted from raw `.excalidraw` JSON to `.excalidraw.md` (Markdown-wrapper format required by modern obsidian-excalidraw-plugin). Legacy raw files preserved in `templates/legacy/`.
- **PDF QUALITY**: `excalidrawScale` default bumped 2 → 3. Very-tall figures (ar < 0.45) clamped to `height=6.0in,keepaspectratio` to prevent page spillover.
- **HIVE LAUNCHPAD**: new command `Hive: Open launchpad` — one keystroke to surface all hive / quickadd / excalidraw / templater commands.
- **EXCALIDRAW TOOLKIT**: new command `Hive Excalidraw Toolkit` — 5 curated power-user actions.

### v1.1.0
- Excalidraw embed pipeline, Insert diagram command, settings.

### v1.0.0
- Initial release: mmdc + pandoc/xelatex PDF export.

---

## Requirements

- Windows 11 + WSL2 (Ubuntu or similar)
- Inside WSL: `pandoc`, `xelatex` (via `texlive-xetex`), `mmdc` (mermaid-cli), `python3`, chromium
- The following files must exist at their expected paths:
  - `/mnt/d/0LOCAL/.claude/scripts/9x_pdf_aspect_sizer.py`
  - `/mnt/d/0LOCAL/.claude/scripts/pdf-template.tex`
  - `/mnt/d/0LOCAL/.cache/puppeteer/chrome/linux-147.0.7727.56/chrome-linux64/chrome`
- For Excalidraw features: `obsidian-excalidraw-plugin` installed and enabled

## Install

1. Open Obsidian Settings → Community plugins
2. Turn off Safe mode (if prompted)
3. The plugin is already in your vault's `.obsidian/plugins/hive-pdf/` folder
4. Click "Reload plugins" or restart Obsidian
5. Find "Hive PDF Export" in the Installed plugins list and enable it

## Usage

### Export to PDF

1. Open any Markdown note
2. Open the Command Palette (`Ctrl+P`)
3. Run: **Export to Hive PDF (smart-sized diagrams)**

The plugin will:
- Extract all ` ```mermaid ``` ` blocks to `.pdf-build/diagrams/`
- Render each diagram with `mmdc` (neutral theme, black text, scale 2)
- Export any `![[*.excalidraw]]` embeds to PNG at scale 3 (v1.2.0+)
- Run `9x_pdf_aspect_sizer.py` to map each PNG aspect ratio to a pandoc image size
- Run `pandoc --pdf-engine=xelatex` with the Hive template
- Write the PDF next to your note (default)
- Open it in your default viewer (configurable)

Build logs are written to `<note-folder>/.pdf-build/build-YYYYMMDD-HHMM.log`.

### Insert Diagram

1. Open a Markdown note where you want to insert a diagram
2. Run: **Insert Hive diagram from template**
3. Pick from 6 templates: Architecture, Process Flow, Timeline, Decision Tree, Component Diagram, Data Pipeline
4. The plugin copies the chosen template to `assets/<note-basename>-HHMMSS.excalidraw.md` and inserts `![[assets/<name>.excalidraw]]` at your cursor

The inserted file opens directly in Excalidraw for editing.

**Troubleshooting .excalidraw.md format:**
Modern versions of `obsidian-excalidraw-plugin` (v1.9+) require diagrams to be stored as `.excalidraw.md` files — a Markdown file with `excalidraw-plugin: parsed` frontmatter and a fenced ` ```json ``` ` block containing the elements. Raw `.excalidraw` JSON files will silently fail to render. The v1.2.0 templates use the correct format. If you have old templates in `templates/legacy/`, do not use them directly.

### Hive Launchpad

Run: **Hive: Open launchpad (diagram / template / PDF actions)**

Opens a fuzzy-search modal over all installed Obsidian commands whose id or name contains:
`hive`, `quickadd`, `excalidraw`, or `templater`

This is your single-keystroke entry point to all diagram, template, and PDF actions across plugins.

### Excalidraw Toolkit

Run: **Hive Excalidraw Toolkit**

Opens a suggest modal with 5 curated power-user actions:

| Action | What it does |
|--------|-------------|
| (a) Auto-arrange as flowchart | Top-down grid layout, 20px snap, equal spacing |
| (b) Beautify | Apply Hive palette: nodes #FFB627/#FF8C42, arrows #293241, Excalifont 20px |
| (c) Add numbered step stickies | Badge each selected element with a sequential number |
| (d) Convert to Mermaid | Export selection as `flowchart TD` → clipboard |
| (e) Insert legend block | Auto-generate color legend bottom-right from element fills |

All actions guard against missing Excalidraw plugin and show a Notice on any error.

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Output directory | (same as note) | Where to write the PDF |
| Filename pattern | `{basename}-{timestamp}.pdf` | `{basename}` = note name, `{timestamp}` = YYYYMMDD-HHMM |
| mmdc render scale | 2 | Higher = sharper. Recommended: 2–3 |
| Excalidraw PNG export scale | 3 | Render scale for Excalidraw → PNG. Default: 3 (v1.2.0+) |
| Include Excalidraw embeds | on | Export `![[*.excalidraw]]` to PNG in PDF |
| Open PDF after build | on | Auto-open in default viewer |
| Overwrite existing | off | If off, appends timestamp to avoid collision |
| WSL distro name | (auto) | Leave blank to use your default WSL distro |

## Troubleshooting

**"wsl.exe not found"** — Ensure you are running Obsidian on Windows with WSL2 installed.

**mmdc fails** — Check that chromium path is correct in the plugin source and that mmdc is on your WSL PATH (`which mmdc` in WSL).

**pandoc fails** — Ensure `xelatex` is installed: `sudo apt install texlive-xetex texlive-fonts-recommended`.

**PDF locked** — If a PDF is already open in a reader, the plugin auto-timestamps the output name.

**Excalidraw toolkit "not loaded"** — Install and enable `obsidian-excalidraw-plugin` from Community plugins.

**Full error** — Check `<note-folder>/.pdf-build/build-*.log` for complete stderr.

## Pipeline (internals)

```
note.md
  ↓ resolve ![[*.excalidraw]] → export PNG via ExcalidrawAutomate (scale 3)
  ↓ extract ```mermaid blocks
diagrams/diagram_NNN.mmd
  ↓ mmdc -t neutral -s 2 (black text, Hive palette)
diagrams/diagram_NNN.png
  ↓ 9x_pdf_aspect_sizer.py (aspect-ratio → pandoc size directive)
.pdf-build/note.ready.md
  ↓ pandoc --pdf-engine=xelatex --template=pdf-template.tex
note-TIMESTAMP.pdf
```

Sizing map (v1.2.0):
- ar >= 4.0 → `\begin{landscape}` full-width rotated page (requires `lscape` in template)
- ar >= 2.5 → width=95%
- ar >= 1.3 → width=80%
- ar >= 0.8 → width=55%
- ar >= 0.45 → height=5.5in
- ar < 0.45 → height=6.0in,keepaspectratio (clamped from 6.5in to prevent spillover)
