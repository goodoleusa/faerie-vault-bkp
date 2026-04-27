# CyberTemplate — Collaboration Seed (HONEY)
# Install: `python3 scripts/setup-collab.py`

---

## Environment Setup (macOS/Linux)

[env | identity | permanent | 1.0] Claude CLI native install (https://github.com/anthropics/claude-cli or `brew install anthropic-cli`). Settings: `~/.config/Claude/settings.json` (Linux) or `~/Library/Application Support/Claude/settings.json` (macOS). Python 3.10+. SSH: `ssh -T git@github.com`. All paths Unix-style.

---

## Your Role on This Investigation

**Data analyst • Visualization engineer (D3/HTML/CSS) • Report writer (H1 + H3 + executive summary) • Editorial reviewer**
- **Primary:** Write H1 (DOGE insider access) narrative + H3 (federal breach) + executive summary
- **Secondary:** Review H2 (stats) clarity; fact-check before publication
- **Visualization:** Verify D3 timelines render correctly; suggest improvements
- **Verification:** Post-COC fix, run forensic verification against evidence manifest

---

## Investigation Status — Terminal Phase (Publication Target: Fri 2026-04-11)

| H | Claim | Confidence | Publish? | Key Evidence | Role |
|---|-------|-----------|----------|---|---|
| H1 | DOGE insider access via credential misuse | 0.95 | ✅ YES | tempf.gov + tempdf.gov in Packetware DB at same second as DOGE GitHub ID; NLRB corroborated by Congress | **YOU WRITE (5 paras + disclosure)** |
| H2 | Packetware/Prometheus as data exfiltration pipeline | 0.78 | ✅ YES | 205GB TX (Z=9.89, Bonferroni p=9.28e-22), 32 Frankfurt SSH servers, $6.74 Prisma revenue | Review clarity; verify journalist-friendly |
| H3 | Federal systems exposed during DOGE window | 0.78 | ✅ YES | Treasury LDAP fully exposed, 678 AzureGov IPs, NNSA breach (Microsoft attribution) | **YOU WRITE (4 paras + disclosure)** |
| H4 | Foreign actor proximity (statistical signal) | 0.55 | ⚠️ CAVEATS | Fisher p=3.82e-16 for Russia; operational linkage unproven | Review caveat language before final draft |
| H5 | Financial benefit | 0.00 | ❌ NO | Zero primary source evidence (no bank records, no crypto) | Single paragraph: "examined, found empty" |

---

## Critical Non-Result (MUST DISCLOSE IN REPORT — NOT APPENDIX)

[finding | finding | permanent | 1.0] **H-DOGE-TREASURY temporal test:** p=0.294 (NOT Bonferroni-significant). Cannot prove access + breach occurred at same moment, though broader pattern clear. Disclose in H1 narrative. Proves non-cherry-picking — credibility first.

---

## Mandatory Disclosures (Non-Negotiable Before Publish)

1. **H-DOGE-TREASURY p=0.294** — main narrative (not appendix)
2. **H4 confidence 0.55** — section header or opening
3. **H5 zero-evidence** — one paragraph acknowledgment + gap for journalists to dig
4. **H2 snapshot limitation** — one Prometheus snapshot; cannot claim "sustained" without time-series
5. **H4 operational linkage unproven** — statistically real pattern; does NOT prove data transfer
6. **SheepMC/Wuhan NAS — OMIT.** Self-label only (Shodan metadata, insufficient).

---

## Your Writing Tasks (This Week)

| Task | Format | Due | Owner |
|------|--------|-----|-------|
| **H1 narrative** (5 paras + disclosure) | `LAUNCH/Writing/h1-insider-access.md` in vault | Tue Apr 8 | **You** |
| **H3 narrative** (4 paras + disclosure) | `LAUNCH/Writing/h3-federal-breach.md` in vault | Tue Apr 8 | **You** |
| **Executive summary** (600–800 words) | `LAUNCH/Writing/executive-summary.md` in vault | Wed Apr 9 | **You** |
| Full narrative review + line edit | Annotation pass on H2/H4 sections | Thu Apr 10 | **You** |

Draft location: Vault `D:\0LOCAL\0-ObsidianTransferring\CyberOps\00-SHARED\LAUNCH\Writing\` (Syncthing synced).
Writing voice: See [launch/ARGUMENT_STRUCTURE.md](../launch/ARGUMENT_STRUCTURE.md) section "Writing Voice — Guidance for All Contributors".

---

## Tech Stack (for Visualization / UI Work)

[tech | identity | permanent | 1.0] Vanilla HTML/CSS/JS — NO build tools, NO Node.js. D3 v7 + Observable Plot (CDN). Design tokens: `assets/theme.css` (navy/crimson/gold). Responsive: `assets/responsive.css` (mobile/tablet/desktop). Target: Mullvad Browser (no hover-only, no XHR, no fingerprint APIs). Pages: index.html, executive.html, report.html, evidence-browser.html, knowledge-graph.html, timeline-enriched.html. Run locally: `python -m http.server 5000 --bind 0.0.0.0` then `http://localhost:5000`.

---

## Key Data Files (For Analysis / Evidence Cross-Reference)

```
scripts/audit_results/
  ├── unified_evidence_H1.json          ← 1,271 H1 entities (author, date, source)
  ├── unified_evidence_H2.json          ← 1,373 H2 entities (traffic, infra)
  ├── unified_evidence_H3.json          ← 772 H3 entities (federal systems)
  ├── unified_evidence_H4.json          ← 228 H4 entities (foreign infra)
  ├── treasury_ldap_extraction.json     ← Full Treasury LDAP schema dump
  ├── viz_prometheus_metrics.json       ← Traffic anomaly visualization
  ├── userid_crossref.json              ← GitHub ID confirmation chain
  ├── gap_priority_order.json           ← Evidence gaps + closure paths
  └── prisma_db_reconstruction.json     ← Packetware DB records
```

Verify every claim against these files. Show evidence for every citation.

---

## Statistical Spine (Key Facts)

[finding | finding | permanent | 1.0] **H2 anchor — 205GB anomaly:** Normal ~20GB observed 205GB. Z-score 9.89. Chance: 2.32e-23 (one in septillion). After Bonferroni 40× penalty: 9.28e-22. Translation: extreme statistical anomaly ever observed in network monitoring.

[finding | finding | permanent | 1.0] **H4 pattern — Russian infrastructure:** Test: Fisher exact. Raw p=3.82e-16. After Bonferroni: 1.53e-15. Meaning: foreign infra IPs co-locate with .gov domain activity non-randomly. NOT proof foreign actors have data.

[rule | method | permanent | 1.0] **Why Bonferroni matters:** 40 tests → ~2 show "significance" by pure luck. Bonferroni makes each 40× harder. Results surviving this penalty bulletproof.

---

## Vault (Obsidian) — Your Collaboration Hub

Location: `D:\0LOCAL\0-ObsidianTransferring\CyberOps\` (Windows) or `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps/` (macOS/Linux, Syncthing-synced).

Key folders:
- `00-SHARED/LAUNCH/ARGUMENT_STRUCTURE.md` — detailed paragraph guidance
- `00-SHARED/LAUNCH/Writing/` — H1, H3, executive summary drafts
- `00-SHARED/LAUNCH/PUBLICATION_BLOCKERS.md` — blocking issues (context)
- `00-SHARED/Human-Inbox/` — findings/flags (read for latest)
- `01-Memories/agents/KNOWLEDGE-BASE.md` — crystallized investigation facts

Editing protocol: (1) Draft in vault `Writing/` folder. (2) Request review via Syncthing (Amanda sees real-time). (3) Mark `ready-for-commit`. (4) Amanda commits to git → COC capture automatic.

---

## Context Snapshot (TL;DR)

- **Mission:** Publish evidence-based investigation of DOGE infrastructure access + federal breach exposure
- **Evidence:** 1,249 curated items (15 Tier 1 smoking guns, 183 Tier 2 strong support)
- **Statistical rigor:** Bonferroni-corrected (40 tests), one non-result disclosed (p=0.294)
- **Your deadline:** H1 + H3 by Tue Apr 8 noon; executive summary by Wed Apr 9 noon
- **Publication:** Fri 2026-04-11 (clearweb + IPFS + Bitcoin timestamp)
- **You write:** The access story (H1) + the exposure story (H3) + the summary for non-experts

Questions? Start with [launch/ARGUMENT_STRUCTURE.md](../launch/ARGUMENT_STRUCTURE.md) — paragraph-level guidance for each section.
