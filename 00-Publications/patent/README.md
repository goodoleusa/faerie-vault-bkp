# 📑 Business / Patent — Consolidated Drafts

> 2026-05-23 — promoted from `forensics/charters/expeditions/enterprise-patent-foundation/polished-deliverables/`. Original 11 agent-authored deliverables preserved verbatim at `_source/` (ancestor provenance, not deletion).

## What's here (3 consolidated drafts + PDFs for sharing)

| File | Purpose | Audience |
|---|---|---|
| **`PATENT-APPLICATION-DRAFT.md/.pdf`** | USPTO provisional spec + Claim 7 (zero-knowledge custody) + Vancouver-endnote bibliography | Patent attorney |
| **`SERVICE-LICENSE-AGREEMENT-DRAFT.md/.pdf`** | ELA + compliance recitals + BAA template + DPA template + retention-period reference | Commercial + privacy attorney |
| **`SUPPORTING-DOCS.md/.pdf`** | Open questions + Assignment Agreement template + marketing blurbs | Operator + attorney internal |

PDFs in `pdfs/` are styled at **14pt DejaVu Sans, 0.75in margins, with TOC + colorlinked references**. Mermaid diagrams in the patent spec render as embedded PNGs (via `mermaid.ink`). Generated 2026-05-23 from the markdown source.

## Folder structure

```
business/patent/
├── README.md                                   ← you are here
├── PATENT-APPLICATION-DRAFT.md                 ← consolidated (cites _source/)
├── SERVICE-LICENSE-AGREEMENT-DRAFT.md          ← consolidated (cites _source/)
├── SUPPORTING-DOCS.md                          ← consolidated (cites _source/)
├── pdfs/
│   ├── PATENT-APPLICATION-DRAFT.pdf            ← share with patent attorney
│   ├── SERVICE-LICENSE-AGREEMENT-DRAFT.pdf     ← share with commercial+privacy attorney
│   ├── SUPPORTING-DOCS.pdf                     ← operator + attorney internal
│   └── mermaid-*.png                           ← rendered diagram embeds (provenance preserved)
└── _source/                                    ← ANCESTOR ARCHIVE — DO NOT DELETE
    ├── PATENT-PROVISIONAL-SPECIFICATION.md     (487 LOC, technical core)
    ├── PATENT-CLAIM-7-ZERO-KNOWLEDGE.md        (zero-knowledge claim + dependents)
    ├── ELA-DRAFT.md                            (Enterprise License Agreement)
    ├── ELA-COMPLIANCE-ADDENDUM.md              (6 compliance recitals)
    ├── BAA-TEMPLATE.md                         (HIPAA BAA template)
    ├── DPA-TEMPLATE.md                         (GDPR DPA template + SCC)
    ├── ASSIGNMENT-AGREEMENT-DRAFT.md           (future patent assignment template)
    ├── BIBLIOGRAPHY-VERIFIED.md                (Vancouver bibliography)
    ├── OPEN-QUESTIONS.md                       (20 open questions)
    ├── RETENTION-PERIODS-VERIFIED.md           (jurisdiction-by-jurisdiction)
    └── BLURBS-BRAINSTORM.md                    (semantic-density blurbs catalog)
```

## Patent claim catalog (8 claims + 7d)

| # | Claim | Novelty |
|---|---|---|
| 1 | Memory orchestration hierarchy (HONEY ↔ NECTAR ↔ pollen ↔ forensics) with mechanical promotion gates | Eliminates stale-memory + context saturation via gates, not LLM judgment |
| 2 | Stigmergic agent coordination via filesystem manifests (w3w mission + compass bearings) | No orchestrator/router; N-agent coordination via filename grammar |
| 3 | Four-shields enforcement (🛡🧠⛓🪞 cheaper-earlier stack) | Biological-immune-system pattern applied to AI integrity |
| 4 | Shape-registry mechanical verdict classification | Deterministic + reproducible quality signals; no LLM-as-judge |
| 5 | Membench quality measurement substrate (probes ARE shapes) | Closed loop memory-arch ↔ quality probes; no human evaluation overhead |
| 6 | Overall novel combination (1-5) | Integrated AI orchestration ecosystem |
| **7** | **Zero-knowledge customer-key-custody for AI in regulated industries** | Vendor can't decrypt customer data even if compelled |
| **7d** | **Extension to SIGNING keys (NEW — operator-locked 2026-05-23)** | Vendor can't impersonate customer in the forensic record; ZERO vendor-side cryptographic surface |
| 8 | Four-bulkheads cyber defense (🏰🧹🩺🪞 perimeter/purification/detection/quarantine) | Forensically-sound AI; bulkhead logs form defensible chain of custody |

## Critical findings preserved (must read before attorney handoff)

1. **HIPAA Conduit Exception is CLOSED** per HHS FAQ 2076: encrypted-only CSP is still a Business Associate. BAA required.
2. **IRS 7-year general business records is IMPRECISE** — IRC § 6501(a) standard is 3 years; 7yr applies only to bad-debt/worthless-securities claims. The 7-year guidance is conventional, not statutory.
3. **Quebec Law 25 phrasing corrected** — official: "for the period necessary to achieve the purposes for which it was collected, or as required by law".
4. **LUMO bibliography hallucination** — `uspto.gov/patents/apply/patent-eligibility` does NOT exist. Canonical SME page is `uspto.gov/patents/laws/examination-policy/subject-matter-eligibility`; August 2025 memo PDF at `uspto.gov/sites/default/files/documents/memo-101-20250804.pdf`.
5. **Inventor structure**: 2 individual inventors, NOT a company entity. Company holds exclusive license; sublicenses to enterprise.
6. **Filing blockers** (operator answers required before USPTO filing): inventor names + addresses + citizenship; company entity formation; first enterprise customer info; jurisdiction strategy (US-only vs PCT); patent attorney engagement.

## Vault mirror

Same structure mirrored at `$VAULT/00-SHARED/Business/Patent/` for Obsidian-curated reading + human-edit promotion to canonical (via authorship signature — see `AGENTS.md` § "Authorship frontmatter — additive contributor list").

## PDF generation command (operator can re-run anytime)

```bash
cd business/patent
for base in PATENT-APPLICATION-DRAFT SERVICE-LICENSE-AGREEMENT-DRAFT SUPPORTING-DOCS; do
  # Pre-render mermaid diagrams via mermaid.ink (public service)
  python3 scripts/render-mermaid-to-png.py "${base}.md" --out-dir pdfs/
  # Then pandoc with the swarmy "business" preset
  pandoc "pdfs/${base}.preprocessed.md" \
    --pdf-engine=xelatex \
    --resource-path=pdfs \
    -V fontsize=14pt -V geometry:margin=0.75in \
    -V mainfont="DejaVu Sans" -V sansfont="DejaVu Sans" -V monofont="DejaVu Sans Mono" \
    -V documentclass=article -V colorlinks=true -V linkcolor=blue -V urlcolor=blue \
    --toc --toc-depth=2 \
    -o "pdfs/${base}.pdf"
done
```

Or via the swarmy-hive-plugin (when installed in vault): right-click the markdown → "Export to Hive PDF" → select preset "business" → done.

## Ancestor citation discipline

Every line of consolidated content has its ancestor in `_source/`. The consolidations cite ancestors at section breaks (e.g., `(continued from _source/PATENT-CLAIM-7-ZERO-KNOWLEDGE.md)`). When the operator (or attorney) edits a consolidated doc, they should also update the corresponding `_source/` file for traceability — OR (preferred) edit `_source/` and re-run the consolidation. The `_source/` files are the canonical authorial truth; the consolidations are the "shareable bundle" view.
