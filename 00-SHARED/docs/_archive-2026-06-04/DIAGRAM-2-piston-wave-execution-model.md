---
type: diagram
status: active
diagram_id: faerie2-diagram-2
title: "Piston Wave Execution Model"
tags: [architecture, system-design, faerie2, excalidraw]
created: 2026-04-26
updated: 2026-04-26
source: scripts/generate_excalidraw_diagrams.py
---

# Piston Wave Execution Model

## Description

Timeline of autonomous dispatch stages: W1 (LIFTOFF: max parallel, cache TTL), W2 (CRUISE: single-spawn, dashboard compression), W3 (INSERTION: deep synthesis, background). No manual pauses between waves.

## Diagram

<svg width="806" height="600" viewBox="0 0 806 600" xmlns="http://www.w3.org/2000/svg">
<defs><style>text {{ font-family: sans-serif; }} .label {{ font-size: 12px; }} .title {{ font-size: 18px; font-weight: bold; }}</style></defs>
<rect width="806" height="600" fill="#ffffff" stroke="none"/>
<text x="390" y="40" text-anchor="middle" font-size="20" class="label">Piston Waves: Autonomous Dispatch + Compression</text>
<text x="90" y="92" text-anchor="middle" font-size="12" class="label">Time →</text>
<text x="290" y="92" text-anchor="middle" font-size="12" class="label">Context fill →</text>
<rect x="20" y="140" width="140" height="100" fill="transparent" stroke="#ef4444" stroke-width="2" rx="4"/>
<text x="140" y="176" text-anchor="middle" font-size="11" class="label">W1: LIFTOFF</text>
<text x="140" y="187" text-anchor="middle" font-size="11" class="label">Max parallel</text>
<text x="140" y="198" text-anchor="middle" font-size="11" class="label">Hit cache TTL</text>
<text x="140" y="209" text-anchor="middle" font-size="11" class="label">~5min</text>
<rect x="220" y="140" width="140" height="100" fill="transparent" stroke="#eab308" stroke-width="2" rx="4"/>
<text x="340" y="176" text-anchor="middle" font-size="11" class="label">W2: CRUISE</text>
<text x="340" y="187" text-anchor="middle" font-size="11" class="label">Single-spawn</text>
<text x="340" y="198" text-anchor="middle" font-size="11" class="label">Dash compress</text>
<text x="340" y="209" text-anchor="middle" font-size="11" class="label">~10min</text>
<rect x="420" y="140" width="140" height="100" fill="transparent" stroke="#3b82f6" stroke-width="2" rx="4"/>
<text x="540" y="176" text-anchor="middle" font-size="11" class="label">W3: INSERTION</text>
<text x="540" y="187" text-anchor="middle" font-size="11" class="label">Deep synthesis</text>
<text x="540" y="198" text-anchor="middle" font-size="11" class="label">Background</text>
<text x="540" y="209" text-anchor="middle" font-size="11" class="label">~∞</text>
<line x1="160" y1="190" x2="220" y2="190" stroke="#000000" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="360" y1="190" x2="420" y2="190" stroke="#000000" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="90" y="312" text-anchor="middle" font-size="12" class="label">Context Fill Gauge</text>
<rect x="40" y="340" width="400" height="30" fill="transparent" stroke="#e5e7eb" stroke-width="2" rx="4"/>
<text x="140" y="365" text-anchor="middle" font-size="10" class="label">0% (W1 start)</text>
<text x="340" y="365" text-anchor="middle" font-size="10" class="label">100% (W3 end)</text>
<rect x="40" y="420" width="400" height="60" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="290" y="460" text-anchor="middle" font-size="10" class="label">No manual pauses between waves</text>
<text x="290" y="470" text-anchor="middle" font-size="10" class="label">Stage separation via dashboard_line compression</text>
<defs><marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#000000" /></marker></defs>
</svg>

## Export Formats

- **Excalidraw JSON**: `forensics/diagrams/diagram-2-*.excalidraw`
- **SVG**: Embedded above
- **Vault Location**: `00-SHARED/Diagrams/faerie2/`

## Notes

- All colors and layout designed for web and print
- SVG is standards-compliant and embeddable in docs
- Source Excalidraw files are editable in Excalidraw.com
