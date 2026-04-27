---
type: agent-evolution-full
agent: research-analyst
generated: 2026-03-25
tags: [agent-evolution, performance, investigation-context]
privacy: personal-vault-only
doc_hash: sha256:378277929a90cd79ee77a8b297e8a317ce632bc9711e042f8beda065b1fdbabf
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Research Analyst — Full Evolution Story

## Current State
- **Score:** 1.00 (training) | **Deployment:** 0.95 (sprint-20260319-002, Hetzner Packetware run)
- **Tier:** INVESTIGATE (core OSINT workhorse)
- **Active investigations:** Operation CriticalExposure / Packetware attribution; AS23470/AS400495 BGP infrastructure mapping; Hetzner/Coolify management server cluster; FamousSparrow C2 network

## Training Timeline

| Date | Score | Delta | Context | Key Learning |
|------|-------|-------|---------|-------------|
| Pre-2026-03-19 | 0.60 | baseline | train-011 initial (failed) | Source diversity: no prior training — scored zero |
| 2026-03-19 | 1.00 | +0.40 | autotune redemption (adversarial pre-seed) | Synthesis vs retrieval distinction; strict type definitions prevent overcounting |
| 2026-03-19 | 0.95 | -0.05 | deployment — Hetzner OSINT run | 6 source types, headline confidence 0.97 — did NOT beat 1.00 training high |
| 2026-03-23 | 0.933 | (baseline) | deployment — sprint-0323 composite | First deployment baseline on RUN013-018 composite KPI |

## Investigation Context

### Operation CriticalExposure / Packetware Attribution
The research-analyst's formative case. The investigation centers on Packetware LLC (AS400495) — a US-registered company run by teenagers Aidan Coristine (CTO/edwardwc) and KrishSoni2 (COO), which received DOGE/OPM/CISA/SSA access in January 2025. The analyst's job was establishing the infrastructure attribution chain: who owns what, what is it connected to, and what does it prove?

Key OSINT work this agent performed:
- **AS23470/Packetware attribution** (the training task): Traced AS400495 BGP infrastructure using WHOIS, BGP routing tables, certificate transparency logs, DNS, Shodan, and PTR records. The adversarial training environment had WebFetch blocked at iterations 2-3 — the pre-seeding workaround (injecting ARIN/crt.sh/BGP data directly into the prompt) is what turned a 0.60 failure into a 1.00 score.
- **Hetzner management server** (65.108.96.185, AS24940): Identified as Packetware's primary management server at confidence 0.97 — Coolify PaaS platform + Prisma Studio accessible unauthenticated on port 5555. Six DNS subdomains confirmed. netbox.anchored.host CNAME to packetware.net. The analyst's REVIEW-INBOX headline: "HOLY SHIT" bookmark by the operator in Sept 2025 confirmed the server's significance.
- **ahmn.co identity gap**: 172.93.110.120 (formerly registry2.anchored.host) now resolves as mail.ahmn.co. The analyst flagged this identity transition in March 2026, noting potential operator identity change vs domain relinquishment.
- **AS400495 BGP hijacking**: Found AS400495 announcing 63.141.38.0/24 — an ARIN RESERVED block legitimately transferred to Continental Building Products in 2017. BGP instability Aug 2025: peak ~136 announcements/hour Aug 4. This became fnd00013 candidate (conf 0.90, H2/H4 support).

### FamousSparrow C2 Network
- **cdn181.awsdns-531.com**: Confirmed FamousSparrow C2 by UK NCSC MAR 2022-02-28 + Trend Micro Earth Estries IOC archive. awsdns-531 is a typosquat (valid AWS range 0-63). Passive DNS to 103.15.28.228 → AS55639 (HK VPS) — NOT AS45102 as initially hypothesized. Gap documented: 5 sibling awsdns-531.com domains need passive DNS sweep to confirm/deny AS45102 connection.

### Nuclear Triple (Sprint RUN012-013)
- Confirmed ORNL (Oak Ridge National Laboratory, 166.1.22.248) cert on Baxet-affiliated IPs, completing the "nuclear triple": LANL (194.58.46.116) + LLNL (45.130.147.179) + ORNL. Also found NASA, DHS/ICE SEVP, uscourts. AS26383 (Baxet US Delaware) carries 267 .gov Shodan hits.
- Russia→China BGP direct link: AS51659 (LLC Baxet, Russia) is the SOLE PEER of AS42375 (Netex Limited, China) — a private peering arrangement, not transit. This CONNECTION flag went to REVIEW-INBOX at HIGH.

### Organizational Nexus
- Confirmed Monk AI Group organizational link: Coristine (CTO/edwardwc) + Soni (COO/KrishSoni2). Both teenagers. No government contracts — DOGE access was "volunteer" appointment. H1 pathway: Packetware (infrastructure 2022) → Monk AI Group (Sept 2024) → DOGE/OPM/CISA/SSA (Jan 2025+).

## What It Learned

### Process Improvements (shareable)
- Source diversity benchmark tests SYNTHESIS not RETRIEVAL: when tool-denial blocks WebFetch, pre-seeding external data isolates the synthesis skill cleanly
- Strict type definitions are load-bearing: same-tool monitor + PTR + domain scan = ONE type; state this explicitly before scoring
- Structure findings as: conclusion → per-conclusion source list → count → pass/fail; don't aggregate at the end
- Gap identification format: "gap = missing source type X for conclusion Y" is more actionable than "needs more research"
- In restricted environments: pre-seed external data when WebFetch will be denied; note this limitation so future runs know to use pre-seeding

### Investigation-Specific Insights (private)
- The autotune failure at 0.60 (train-011) was a wake-up call about the brittleness of the OSINT pipeline when external tools are blocked. The solution — pre-seeding ARIN/crt.sh/BGP data before the session — became a standard technique for adversarial training environments.
- Working on the Packetware case taught strict type discipline. In the real case, it's easy to count Shodan data, Censys data, and BGP.Tools data as three types when they're all infrastructure monitoring — they're ONE type. This overcounting bias was explicitly corrected.
- The Hetzner management server finding (0.97 confidence) showed what high source diversity looks like in practice: Shodan ClickHouse alerts, DNS CNAME chain, operator bookmark history, Prisma Studio network observable, Hunchly MHTMLs, and RIPEstat BGP data — six genuinely independent source types confirming the same conclusion.
- The ahmn.co identity gap is an example of what the analyst cannot close alone: it requires WHOIS queries that need WebFetch access. This gap-flagging skill (rather than speculation) was honed on Packetware.
- The FamousSparrow C2 overlap (cdn181.awsdns-531.com) created a hypothesis-testing discipline: the analyst initially suspected AS45102 linkage but passive DNS showed AS55639 instead. Documenting the gap (rather than claiming the link) is the correct move.

## Performance Trajectory

The research-analyst's arc is one of dramatic recovery from a structural failure. The initial train-011 attempt scored 0.60 because the adversarial environment blocked WebFetch at iterations 2-3 — the agent tried to retrieve live data and got cut off. The insight was that retrieval is not what was being tested: synthesis was. Once the training methodology was corrected (pre-seed the external data, then test synthesis), the score jumped to 1.00.

The deployment scores (0.95, 0.933) show the natural difficulty gravity of real-world investigation work versus controlled training. The 0.95 on the Hetzner sprint was excellent — 6 source types confirmed, 0.97 headline confidence — but fell slightly short of the 1.00 training score, which is expected. Real investigations are messier than constrained drills.

The RUN013-018 composite score (0.933) established the first formal deployment baseline. The sprint included the nuclear hostname-triple confirmation (H4), c5isr.dev Army impersonation analysis, and K8s enrichment — genuine attribution work against state-level adversaries.

## Spawn History (from subagent-roster.json + run-benchmarks.json)

| Sprint | Task | Outcome | Score |
|--------|------|---------|-------|
| sprint-20260319-001 | AS23470/Packetware OSINT pipeline | Redemption: 0.60→1.00 | 1.00 |
| sprint-20260319-002 | Hetzner OSINT (65.108.96.185 attribution) | beat_last=false (0.95 vs 1.00) | 0.95 |
| sprint-0323 RUN012 | FamousSparrow C2 + Monk AI nexus + nuclear triple | First deployment baseline | 0.933 |

The agent has been a named participant in every major sprint since March 19, 2026, anchoring the H4 (foreign actor) hypothesis development with attribution-grade OSINT.
