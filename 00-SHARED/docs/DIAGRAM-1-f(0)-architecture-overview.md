---
type: diagram
status: active
diagram_id: faerie2-diagram-1
title: "f(0) Architecture Overview"
tags: [architecture, system-design, faerie2, excalidraw]
created: 2026-04-26
updated: 2026-04-26
source: scripts/generate_excalidraw_diagrams.py
---

# f(0) Architecture Overview

## Description

Shows main context dispatch → bundle pre-computation → 3,700+ agent spawns → forensic immutability. Highlights 99.5% cost reduction (10K → 50 tokens), stigmergic 80-char returns, and piston wave autonomy.

## Diagram

<svg width="952" height="600" viewBox="0 0 952 600" xmlns="http://www.w3.org/2000/svg">
<defs><style>text {{ font-family: sans-serif; }} .label {{ font-size: 12px; }} .title {{ font-size: 18px; font-weight: bold; }}</style></defs>
<rect width="952" height="600" fill="#ffffff" stroke="none"/>
<text x="420" y="40" text-anchor="middle" font-size="20" class="label">f(0): Agent Orchestration with Forensic Immutability</text>
<rect x="20" y="80" width="150" height="80" fill="transparent" stroke="#3b82f6" stroke-width="2" rx="4"/>
<text x="147" y="127" text-anchor="middle" font-size="12" class="label">Main Context</text>
<text x="147" y="139" text-anchor="middle" font-size="12" class="label">(Dispatch)</text>
<line x1="170" y1="120" x2="250" y2="120" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="250" y="80" width="150" height="80" fill="transparent" stroke="#10b981" stroke-width="2" rx="4"/>
<text x="375" y="127" text-anchor="middle" font-size="12" class="label">Bundle</text>
<text x="375" y="139" text-anchor="middle" font-size="12" class="label">Pre-computation</text>
<line x1="400" y1="120" x2="480" y2="120" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="480" y="80" width="150" height="80" fill="transparent" stroke="#f97316" stroke-width="2" rx="4"/>
<text x="605" y="127" text-anchor="middle" font-size="12" class="label">3,700+ Spawns</text>
<text x="605" y="139" text-anchor="middle" font-size="12" class="label">(50 tokens ea)</text>
<line x1="630" y1="120" x2="710" y2="120" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="710" y="80" width="150" height="80" fill="transparent" stroke="#8b5cf6" stroke-width="2" rx="4"/>
<text x="835" y="127" text-anchor="middle" font-size="12" class="label">Forensic</text>
<text x="835" y="139" text-anchor="middle" font-size="12" class="label">Immutability</text>
<text x="70" y="234" text-anchor="middle" font-size="14" class="label">COST REDUCTION</text>
<rect x="20" y="250" width="180" height="60" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="160" y="286" text-anchor="middle" font-size="11" class="label">Input tokens: 99.5%↓</text>
<text x="160" y="297" text-anchor="middle" font-size="11" class="label">Per-spawn: 10K → 50</text>
<rect x="250" y="250" width="180" height="60" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="390" y="286" text-anchor="middle" font-size="11" class="label">Stigmergic Return</text>
<text x="390" y="297" text-anchor="middle" font-size="11" class="label">80-char dashboard_line</text>
<rect x="480" y="250" width="180" height="60" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="620" y="286" text-anchor="middle" font-size="11" class="label">Piston Waves</text>
<text x="620" y="297" text-anchor="middle" font-size="11" class="label">W1/W2/W3 autonomy</text>
<defs><marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#000000" /></marker></defs>
</svg>

## Export Formats

- **Excalidraw JSON**: `forensics/diagrams/diagram-1-*.excalidraw`
- **SVG**: Embedded above
- **Vault Location**: `00-SHARED/Diagrams/faerie2/`

## Notes

- All colors and layout designed for web and print
- SVG is standards-compliant and embeddable in docs
- Source Excalidraw files are editable in Excalidraw.com
