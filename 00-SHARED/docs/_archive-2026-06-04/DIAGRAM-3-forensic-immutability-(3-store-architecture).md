---
type: diagram
status: active
diagram_id: faerie2-diagram-3
title: "Forensic Immutability (3-Store Architecture)"
tags: [architecture, system-design, faerie2, excalidraw]
created: 2026-04-26
updated: 2026-04-26
source: scripts/generate_excalidraw_diagrams.py
---

# Forensic Immutability (3-Store Architecture)

## Description

Three-store COC chain: {repo}/forensics/ (canonical, git-tracked) ← hash-chain → Vault (Obsidian, derivative) ← hash-tracker → S3/B2 WORM (immutable backup). HMAC-SHA256 chaining, deletion-proof at DB layer.

## Diagram

<svg width="1035" height="600" viewBox="0 0 1035 600" xmlns="http://www.w3.org/2000/svg">
<defs><style>text {{ font-family: sans-serif; }} .label {{ font-size: 12px; }} .title {{ font-size: 18px; font-weight: bold; }}</style></defs>
<rect width="1035" height="600" fill="#ffffff" stroke="none"/>
<text x="420" y="40" text-anchor="middle" font-size="20" class="label">Forensic Immutability: Three-Store COC Chain</text>
<rect x="20" y="100" width="140" height="100" fill="transparent" stroke="#10b981" stroke-width="2" rx="4"/>
<text x="140" y="155" text-anchor="middle" font-size="10" class="label">{repo}/forensics/</text>
<text x="140" y="165" text-anchor="middle" font-size="10" class="label">Canonical System</text>
<text x="140" y="175" text-anchor="middle" font-size="10" class="label">Git-tracked</text>
<line x1="160" y1="150" x2="220" y2="150" stroke="#059669" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="240" y="144" text-anchor="middle" font-size="9" class="label">Hash-chained</text>
<rect x="220" y="100" width="140" height="100" fill="transparent" stroke="#8b5cf6" stroke-width="2" rx="4"/>
<text x="340" y="155" text-anchor="middle" font-size="10" class="label">Vault</text>
<text x="340" y="165" text-anchor="middle" font-size="10" class="label">(Obsidian)</text>
<text x="340" y="175" text-anchor="middle" font-size="10" class="label">Derivative styling</text>
<line x1="360" y1="150" x2="420" y2="150" stroke="#7c3aed" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="440" y="144" text-anchor="middle" font-size="9" class="label">Hash-tracked</text>
<rect x="420" y="100" width="140" height="100" fill="transparent" stroke="#dc2626" stroke-width="2" rx="4"/>
<text x="540" y="155" text-anchor="middle" font-size="10" class="label">S3/B2 WORM</text>
<text x="540" y="165" text-anchor="middle" font-size="10" class="label">Immutable Backup</text>
<text x="540" y="175" text-anchor="middle" font-size="10" class="label">Immune to deletion</text>
<text x="70" y="252" text-anchor="middle" font-size="12" class="label">FORENSIC CHAIN DETAILS</text>
<rect x="20" y="270" width="180" height="120" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="160" y="295" text-anchor="middle" font-size="10" class="label">Canonical (repo)</text>
<text x="80" y="314" text-anchor="middle" font-size="9" class="label">• HMAC-SHA256 chaining</text>
<text x="80" y="323" text-anchor="middle" font-size="9" class="label">• COC entries immutable</text>
<text x="80" y="332" text-anchor="middle" font-size="9" class="label">• Git history preserved</text>
<text x="80" y="341" text-anchor="middle" font-size="9" class="label">• Append-only by design</text>
<rect x="250" y="270" width="180" height="120" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="390" y="295" text-anchor="middle" font-size="10" class="label">Hash-tracked (vault)</text>
<text x="310" y="314" text-anchor="middle" font-size="9" class="label">• Before/after snapshots</text>
<text x="310" y="323" text-anchor="middle" font-size="9" class="label">• Linked to forensics</text>
<text x="310" y="332" text-anchor="middle" font-size="9" class="label">• Edit-proof metadata</text>
<text x="310" y="341" text-anchor="middle" font-size="9" class="label">• Evidence-grounded</text>
<rect x="480" y="270" width="180" height="120" fill="transparent" stroke="#f3f4f6" stroke-width="2" rx="4"/>
<text x="620" y="295" text-anchor="middle" font-size="10" class="label">WORM-backed (S3/B2)</text>
<text x="540" y="314" text-anchor="middle" font-size="9" class="label">• Zero deletion</text>
<text x="540" y="323" text-anchor="middle" font-size="9" class="label">• Cryptographic proof</text>
<text x="540" y="332" text-anchor="middle" font-size="9" class="label">• External custody</text>
<text x="540" y="341" text-anchor="middle" font-size="9" class="label">• Compliance-ready</text>
<defs><marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#000000" /></marker></defs>
</svg>

## Export Formats

- **Excalidraw JSON**: `forensics/diagrams/diagram-3-*.excalidraw`
- **SVG**: Embedded above
- **Vault Location**: `00-SHARED/Diagrams/faerie2/`

## Notes

- All colors and layout designed for web and print
- SVG is standards-compliant and embeddable in docs
- Source Excalidraw files are editable in Excalidraw.com
