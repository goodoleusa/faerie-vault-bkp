---
type: review-inbox-siphon
date: 2026-03-29
agent: membot
session: siphon-2026-03-29
priority: HIGH
status: needs-human-review
---

# REVIEW-INBOX Siphon — 2026-03-29

REVIEW-INBOX was 908 lines (3.6x over target). This siphon reduced it to ≤50 lines.

**Counts:** 35 investigation findings + 7 system findings → NECTAR | 12 faerie/system items → KEEP in inbox | ~850 lines archived/deduplicated

---

## Items Requiring Human Decision

### 1. H1 Confidence Conflict — NEEDS TRIAGE
**DECISION NEEDED:** H1 confidence conflict between two sources.
- HONEY.md shows H1=0.95
- NECTAR sprint summary (RUN-008) shows H1=0.55
- membot wrote H1=0.55 into faerie-brief.json as "correct post-NECTAR value"
- Clarify: which is current? Was the 0.95 pre-NECTAR baseline never updated?
Source: membot DECISION 2026-03-22T23:58Z, session task-20260319-184813-3bfd

### 2. GitHub PAT Exposed in mcp.json — CRITICAL SECURITY
**ACTION REQUIRED:** GitHub personal access token exposed in plaintext in `mcp.json` (faerie2 repo).
- Rotate the token immediately
- Ensure mcp.json is in .gitignore or credential-stripped before any public push
Source: workflow-orchestrator phase1 audit 2026-03-28

### 3. Source Video File Status — CONFLICTING REPORTS
**DECISION NEEDED:** Two conflicting flags about the Packetware ProxMox source video:
- `2026-03-19-flag-source-video-file-missing-from-local-raw.md` says MISSING
- `2026-03-22-flag-proxmox-source-video-confirmed-not-missing.md` says CONFIRMED
- Which is current? If confirmed, what path is the canonical copy?
SHA-256: e82435523a..., 22.4MB, local file confirmed per security-auditor 2026-03-22.

### 4. Report.html Cert Language — Pre-Publication Edit
**ACTION REQUIRED:** `report.html` cert analysis section needs language update before release.
Current: "certificates appeared on..."
Required: "legitimate US gov certs detected serving from adversary-linked foreign infrastructure after Jan 14 2025"
This strengthens the finding (pre-Jan-14 issuance rules out forgery). H-TEMPORAL caveat framing already correct (lines 420, 438). Human legal review of H-TEMPORAL framing previously flagged.
Source: `2026-03-22-flag-report-html-cert-analysis-language-needs.md`

### 5. T1 Evidence SHA256 Verification — Publication Blocker
**ACTION REQUIRED:** T1 has 18 items, 0 sha256-verified. Publication blocked until hashes confirmed.
Run `hash_guardian` on all 18 Tier 1 items before any disclosure.
Source: `2026-03-22-flag-t1-evidence-18-items-0-sha256-verified-p.md`

### 6. GSA FICAM Let's Encrypt Cert — Policy Question
**QUESTION:** gsa.gov + fedidcard.gov + fpisc.gov using Let's Encrypt (not US Gov Root CA1/2 or DigiCert Federal). Is this a known GSA policy decision for citizen-facing domains, or is it part of the finding? Research-analyst flagged this as human-judgment call.
Source: `scratch task-20260319-030201-8e6a`, flag `2026-03-22-flag-bc76377-gsa-fingerprint-alibaba-verifica.md`

### 7. Monk AI Group — 6 Critical Lookups Still Blocked
**BLOCKED:** 6 critical live lookups for Monk AI Group remain blocked (WebFetch/WebSearch).
Items pending: government contract mapping, LinkedIn extraction, RegisteredAgent details, funding, personnel cross-ref with other DOGE actors.
Source: `2026-03-23-gap-monk-ai-group-6-critical-live-lookups-re.md`

### 8. AS400495 Full Dataset Not In Pipeline
**ACTION NEEDED:** `packetware-current-400495-all.xlsx` — full AS400495 Shodan dataset NOT yet in normalized pipeline.
Source: `scratch-mine007-1774030104.md`, agent: data-engineer

### 9. awsdns-531.com Sibling Subdomains
**GAP OPEN:** awsdns-531.com sibling subdomains not checked — potential AS45102 link unresolved.
Source: `scratch-task71be.md`, agent: research-analyst

### 10. COC Chain Break Entries 742-746
**ACTION REQUIRED:** master-coc.jsonl entries 742-746 require manual review (hash chain break).
Source: `2026-03-22-flag-coc-chain-break-entries-742-746-requires.md`, agent: security-auditor

### 11. Claude Memory Comparison Report — Human Review Before Publishing
**REVIEW NEEDED:** Research complete. Key numbers: 330 KB crystallized / 581.6 MB transcripts (0.055% ratio). Platform waste: Mac ~85%, WSL/Windows ~99.7%, investigative ~95-99%.
Needs: web-verification of post-Aug 2025 Claude changes before any public use.
Full report: `/mnt/d/0LOCAL/0-ObsidianTransferring/CyberOps-UNIFIED/00-SHARED/Agent-Outbox/research-claude-memory-comparison.md`

### 12. Faerie System Flags — Routing + Score Feedback Loop Open
**IMPROVEMENT NEEDED (non-urgent):** Three related system gaps from phase1 audit (2026-03-18):
- Agent routing 100% hard-coded; scores never influence dispatch (run-benchmarks.json scores not read by routing)
- Zero tasks in sprint-queue.json have `next_on_failure` populated → failures silently stagnate
- Training queue has 5 agents since 2026-03-15 — none consumed
Proposal: score-gated routing rule; `next_on_failure` template in task creation; /run warns when field absent on HIGH tasks.
Source: workflow-orchestrator, error-coordinator, performance-eval — phase1 audit 2026-03-18

---

## Archived (Investigation items already routed to vault Human-Inbox)

All `<!-- ROUTED: [[...]] -->` entries (lines 1-22 of original REVIEW-INBOX): 11 items dated 2026-03-19 through 2026-03-23. Already routed to vault on respective dates — no action needed.

## Archived (Duplicate auto-collected entries from data-analysis-engine + faerie2 scratch)

Lines 650-908 of original: auto-collected copies of cybertemplate scratch entries. All substantive content identical to primary cybertemplate entries already captured in NECTAR above. Archived to prevent duplication. No findings lost.

## Archived (Session operational entries)

Session separator headers, ROUTED comments, membot operational OBSERVATION blocks about faerie-brief.json rebuild mechanics — operational only, no investigation value. Not promoted.

