---
type: diagram
status: active
diagram_id: faerie2-diagram-4
title: "Stigmergic Queue (Mission-Based Coordination)"
tags: [architecture, system-design, faerie2, excalidraw]
created: 2026-04-26
updated: 2026-04-26
source: scripts/generate_excalidraw_diagrams.py
---

# Stigmergic Queue (Mission-Based Coordination)

## Description

Filesystem-only coordination via investigation_label. Agent 1 writes manifest with next_task_queued. Agent 2 discovers via `grep -r "_{task_id}_" forensics/manifests/`. No SendMessage; paths form the coordination backbone.

## Diagram

<svg width="815" height="600" viewBox="0 0 815 600" xmlns="http://www.w3.org/2000/svg">
<defs><style>text {{ font-family: sans-serif; }} .label {{ font-size: 12px; }} .title {{ font-size: 18px; font-weight: bold; }}</style></defs>
<rect width="815" height="600" fill="#ffffff" stroke="none"/>
<text x="420" y="40" text-anchor="middle" font-size="20" class="label">Stigmergy-First: Filesystem Coordination</text>
<text x="70" y="91" text-anchor="middle" font-size="11" class="label">LEGEND</text>
<rect x="20" y="105" width="15" height="15" fill="transparent" stroke="#f97316" stroke-width="2" rx="4"/>
<text x="95" y="116" text-anchor="middle" font-size="9" class="label">Initial Task</text>
<rect x="170" y="105" width="15" height="15" fill="transparent" stroke="#3b82f6" stroke-width="2" rx="4"/>
<text x="245" y="116" text-anchor="middle" font-size="9" class="label">Queue Path</text>
<rect x="320" y="105" width="15" height="15" fill="transparent" stroke="#10b981" stroke-width="2" rx="4"/>
<text x="395" y="116" text-anchor="middle" font-size="9" class="label">Follow-up Agent</text>
<rect x="20" y="170" width="130" height="70" fill="transparent" stroke="#f97316" stroke-width="2" rx="4"/>
<text x="135" y="215" text-anchor="middle" font-size="10" class="label">Agent 1</text>
<text x="135" y="225" text-anchor="middle" font-size="10" class="label">Writes manifest</text>
<text x="135" y="235" text-anchor="middle" font-size="10" class="label">investigation_label</text>
<line x1="150" y1="205" x2="210" y2="205" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="210" y="170" width="130" height="70" fill="transparent" stroke="#3b82f6" stroke-width="2" rx="4"/>
<text x="325" y="199" text-anchor="middle" font-size="9" class="label">next_task_queued</text>
<text x="325" y="208" text-anchor="middle" font-size="9" class="label">field in manifest</text>
<text x="325" y="217" text-anchor="middle" font-size="9" class="label">(same label)</text>
<line x1="340" y1="205" x2="400" y2="205" stroke="#10b981" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="400" y="170" width="130" height="70" fill="transparent" stroke="#10b981" stroke-width="2" rx="4"/>
<text x="515" y="215" text-anchor="middle" font-size="10" class="label">Agent 2</text>
<text x="515" y="225" text-anchor="middle" font-size="10" class="label">Reads path</text>
<text x="515" y="235" text-anchor="middle" font-size="10" class="label">Auto-discovers</text>
<text x="70" y="301" text-anchor="middle" font-size="11" class="label">FILESYSTEM COORDINATION (NO SENDMESSAGE)</text>
<rect x="20" y="320" width="500" height="100" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="320" y="344" text-anchor="middle" font-size="9" class="label">Path Pattern: forensics/manifests/{ts}_{type}_{task_id}_{agent}_{sid8}.json</text>
<text x="80" y="369" text-anchor="middle" font-size="9" class="label">Agent 1 writes: 20260425_manifest_cost-reduction-analysis_faerie-main_a1b2c3d4.json</text>
<text x="80" y="387" text-anchor="middle" font-size="9" class="label">Agent 1 sets: next_task_queued = { task_id: cost-reduction-input-delta, label: mission-cost }</text>
<text x="80" y="405" text-anchor="middle" font-size="9" class="label">Agent 2 discovers: grep -r "_{task_id}_" forensics/manifests/ (zero context cost)</text>
<rect x="20" y="450" width="500" height="50" fill="transparent" stroke="#fef3c7" stroke-width="2" rx="4"/>
<text x="320" y="485" text-anchor="middle" font-size="10" class="label">No SendMessage needed. Agents coordinate via predictable filesystem paths.</text>
<defs><marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#000000" /></marker></defs>
</svg>

## Export Formats

- **Excalidraw JSON**: `forensics/diagrams/diagram-4-*.excalidraw`
- **SVG**: Embedded above
- **Vault Location**: `00-SHARED/Diagrams/faerie2/`

## Notes

- All colors and layout designed for web and print
- SVG is standards-compliant and embeddable in docs
- Source Excalidraw files are editable in Excalidraw.com
