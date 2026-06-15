---
type: diagram
status: active
diagram_id: faerie2-diagram-5
title: "Memory System ROI: Observation → Crystallization"
tags: [architecture, system-design, faerie2, excalidraw]
created: 2026-04-26
updated: 2026-04-26
source: scripts/generate_excalidraw_diagrams.py
---

# Memory System ROI: Observation → Crystallization

## Description

Circular flow: Observation (agent work) → Pollen MEM (session-local) → NECTAR (HIGH @ handoff) → Droplets (vault, live) → HONEY (universal, gauntlet). Quality gates at Tier 1-4. Measured ROI: 2.85× efficiency ratio. Circular: better memory → better work → better observations.

## Diagram

<svg width="1455" height="600" viewBox="0 0 1455 600" xmlns="http://www.w3.org/2000/svg">
<defs><style>text {{ font-family: sans-serif; }} .label {{ font-size: 12px; }} .title {{ font-size: 18px; font-weight: bold; }}</style></defs>
<rect width="1455" height="600" fill="#ffffff" stroke="none"/>
<text x="420" y="40" text-anchor="middle" font-size="20" class="label">Memory System ROI: Observation → Crystallization</text>
<rect x="20" y="120" width="110" height="80" fill="transparent" stroke="#10b981" stroke-width="2" rx="4"/>
<text x="125" y="170" text-anchor="middle" font-size="10" class="label">Observation</text>
<text x="125" y="180" text-anchor="middle" font-size="10" class="label">(Agent work)</text>
<line x1="130" y1="160" x2="190" y2="160" stroke="#10b981" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="190" y="120" width="110" height="80" fill="transparent" stroke="#3b82f6" stroke-width="2" rx="4"/>
<text x="295" y="159" text-anchor="middle" font-size="9" class="label">Pollen MEM</text>
<text x="295" y="168" text-anchor="middle" font-size="9" class="label">Session-local</text>
<text x="295" y="177" text-anchor="middle" font-size="9" class="label">(pollen-{SID})</text>
<line x1="300" y1="160" x2="360" y2="160" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="360" y="120" width="110" height="80" fill="transparent" stroke="#f97316" stroke-width="2" rx="4"/>
<text x="465" y="159" text-anchor="middle" font-size="9" class="label">NECTAR</text>
<text x="465" y="168" text-anchor="middle" font-size="9" class="label">HIGH entries</text>
<text x="465" y="177" text-anchor="middle" font-size="9" class="label">@ /handoff</text>
<line x1="470" y1="160" x2="530" y2="160" stroke="#f97316" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="530" y="120" width="110" height="80" fill="transparent" stroke="#8b5cf6" stroke-width="2" rx="4"/>
<text x="635" y="159" text-anchor="middle" font-size="9" class="label">Droplets</text>
<text x="635" y="168" text-anchor="middle" font-size="9" class="label">(Vault, live)</text>
<text x="635" y="177" text-anchor="middle" font-size="9" class="label">Published</text>
<line x1="640" y1="160" x2="700" y2="160" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrowhead)"/>
<rect x="700" y="120" width="110" height="80" fill="transparent" stroke="#dc2626" stroke-width="2" rx="4"/>
<text x="805" y="159" text-anchor="middle" font-size="9" class="label">HONEY</text>
<text x="805" y="168" text-anchor="middle" font-size="9" class="label">Universal</text>
<text x="805" y="177" text-anchor="middle" font-size="9" class="label">Gauntlet</text>
<line x1="755" y1="200" x2="755" y2="250" stroke="#dc2626" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="755" y1="250" x2="75" y2="250" stroke="#dc2626" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="75" y1="250" x2="75" y2="200" stroke="#dc2626" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="420" y="270" text-anchor="middle" font-size="10" class="label">↻ Circular: Better memory → Better future work → Better observations</text>
<text x="70" y="331" text-anchor="middle" font-size="11" class="label">TIER & QUALITY GATES</text>
<rect x="20" y="350" width="200" height="90" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="170" y="375" text-anchor="middle" font-size="10" class="label">Tier 1-2: Session-scoped</text>
<text x="80" y="394" text-anchor="middle" font-size="9" class="label">• Pollen MEM blocks</text>
<text x="80" y="403" text-anchor="middle" font-size="9" class="label">• Session FOONotes</text>
<text x="80" y="412" text-anchor="middle" font-size="9" class="label">• Raw observations</text>
<rect x="270" y="350" width="200" height="90" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="420" y="375" text-anchor="middle" font-size="10" class="label">Tier 3: Evidence-grounded</text>
<text x="330" y="394" text-anchor="middle" font-size="9" class="label">• NECTAR promotion</text>
<text x="330" y="403" text-anchor="middle" font-size="9" class="label">• Artifact hash-linked</text>
<text x="330" y="412" text-anchor="middle" font-size="9" class="label">• Forensic audit trail</text>
<rect x="520" y="350" width="200" height="90" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="670" y="375" text-anchor="middle" font-size="10" class="label">Tier 4: Universal (HONEY)</text>
<text x="580" y="394" text-anchor="middle" font-size="9" class="label">• Cross-project patterns</text>
<text x="580" y="403" text-anchor="middle" font-size="9" class="label">• Gauntlet certification</text>
<text x="580" y="412" text-anchor="middle" font-size="9" class="label">• ROI validated: 2.85×</text>
<defs><marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#000000" /></marker></defs>
</svg>

## Export Formats

- **Excalidraw JSON**: `forensics/diagrams/diagram-5-*.excalidraw`
- **SVG**: Embedded above
- **Vault Location**: `00-SHARED/Diagrams/faerie2/`

## Notes

- All colors and layout designed for web and print
- SVG is standards-compliant and embeddable in docs
- Source Excalidraw files are editable in Excalidraw.com
