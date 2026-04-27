---
cssclasses:
  - wide-page
  - dashboard-home
tags:
  - home
  - dashboard
  - f4
type: dashboard
parent:
  - "[[00-SHARED/Dashboards/_index|Dashboards]]"
child:
  - "[[Phase1-AgentSync|Phase 1]]"
  - "[[Phase2-Publication|Phase 2]]"
  - "[[Hypothesis-Tracker|Hypotheses]]"
  - "[[Annotation-Dash|Annotations]]"
status: Todo
doc_hash: sha256:c5d41d1d7ab50a84c4c657b5f98d08778b955858ebd75c9eeba752266e73e866
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> **You are here: HOME** · [[00-SHARED/Human-Inbox/_index|Check Inbox →]] · [[00-SHARED/Queue/_index|Plan Work →]] · [[00-SHARED/Droplets/_index|What Was Captured →]]
> [[00-SHARED/Dashboards/_index|All Dashboards]] · [[00-SHARED/Agent-Outbox/_index|Raw Agent Work]] · [[00-SHARED/Hive/_index|Hive]] · [[00-SHARED/00-SHARED|00-SHARED Hub]]

# criticalexposure.report

**Phase 1 — Investigation** &nbsp;·&nbsp; [[Phase1-AgentSync|Agent detail ↓]] &nbsp;·&nbsp; [[Phase2-Publication|Start writing →]] &nbsp;·&nbsp; [[Annotation-Dash|Annotate + court prep]]

---

> [!priority]+ PRIORITY — Researcher North Star
> *Edit this to set your current #1 focus. Agents read it at session start.*
> **Current:** Verify ORNL + LLNL certs on Baxet IPs before any nuclear-triple claims go public.
> *[[00-SHARED/PRIORITY|Edit →]]*

---

## FINDINGS — What's confirmed

> [!critical]- SG-1 · Jan 14 Inflection — all H · `0.95`
> Jan 14 2025 = Simultaneous change across 4 independent infrastructure categories. Shodan 8-year baseline: zero pre-Jan-14 matches. Statistical backing: Fisher p≈0, KS-test confirms fundamentally different populations before/after.
> → `stat_baxet_fisher_RUN008.json`

> [!critical]- SG-2 · Reflected TLS — H4 mechanism · `0.82`
> C2 at 8.219.207.49 uses socat to proxy Treasury PKI TLS from 164.95.89.25 (no SNI enforcement). Appears as legitimate Treasury HTTPS to passive scanners — without the private key. Staged rollout: Aeza Jan 15 → Baxet Feb 8 → Alibaba Feb 10.
> → `audit-log.md`

> [!critical]- SG-3 · DOGE Malware C2 — H2 · confirmed
> `chrome_proxy.exe` calls home to `SUCKMYCHOCOLATESALTYBALLS.DOGE.GOV`. Falcon Sandbox confirmed. SHA256: 92fcf735… Tag: `bigballs` — same tag as the "Packetware and Purge" document naming Luke Farritor.
> → `pdf_ingest_RUN007.json`

> [!critical]- SG-4 · Fisher OR=123.7 p=6.54e-101 — H4 · Tier 1
> 3 independent foreign IPs show .gov certs clustering post-DOGE EO. OR=123.7 (124× more likely than null). Negative control 83.149.30.186: zero .gov certs both periods. Pre-EO access: Jan 15-19 on Aeza — 5 days before formal authorization.
> → `statistical_analysis_baxet_RUN007.json`

> [!critical]- SG-5 · Luke Farritor DOE Access — H1 · named
> "Packetware and Purge" names Luke Farritor (23, ex-SpaceX intern) accessing DOE Feb 5 2025. Also names Brooke Rollins + Chris Wright. Document tagged `bigballs` — same operational context as malware binary.
> → `pdf_ingest_RUN007.json`

> [!critical]- SG-6 · Federal System Exposures — H3
> 7 IPs with RDP open in usgovvirginia Jan-Mar 2025. DOE PKI LDAP: anonymous bind. Fermilab VPN + LLNL GlobalProtect + NNSS password reset: plain HTTP. SATODS (US Air Force) exposed.
> → `pdf_ingest_RUN007.json`

**Hypothesis confidence (live):** see [[session-briefs/LATEST-brief|Latest Brief]] for current scores

[[Hypothesis-Tracker|Full hypothesis detail →]] · [[Annotation-Dash|Annotate evidence →]]

---

## FLAGS — Pending your review

```dataview
TABLE WITHOUT ID
  file.link AS "Item",
  cat AS "Cat",
  priority AS "Pri",
  agent AS "Agent",
  dateformat(date(ts), "MM-dd") AS "Date"
FROM "00-SHARED/Human-Inbox/findings" OR "00-SHARED/Human-Inbox/flags"
WHERE review_status = "unreviewed"
SORT choice(priority = "HIGH", 0, choice(priority = "MED", 1, 2)) ASC, ts DESC
LIMIT 25
```

*Open any item → apply Blueprint → fill → Ctrl+Alt+C to commit with ann_hash*

[[00-SHARED/Human-Inbox/_index|All pending items →]] · [[Annotation-Dash|Annotation dashboard →]]

---

## FRICTION — Gaps & blockers

> [!gap] 4 gaps · none blocking publish, all blocking Tier 1 claims
> - [ ] **LLNL cert** — 45.130.147.179 Shodan archive (nuclear triple incomplete)
> - [ ] **AS45102 link** — cdn181 sibling domains passive DNS unchecked
> - [ ] **BlurbStudio.cr** — WHOIS unknown (Costa Rica TLD, manually generated cert)
> - [ ] **userId a458bkg9pb95tgb8** — Levenshtein=1 from known DOGE account, unresolved

> [!critical]+ 3 decisions waiting
> **ORNL nuclear triple** — Baxet IP has `icons.ornl.gov` hostname, but TLS cert is `CN=BlurbStudio.cr` (self-signed, NOT ornl.gov). Revise framing before publish? Or hold for LLNL verification?
>
> **FamousSparrow C2** — cdn181.awsdns-531.com confirmed (UK NCSC + Trend Micro). 5 sibling domains unchecked. Promote now or wait for sibling sweep?
>
> **Federal K8s overseas** — Two K8s API servers (5.161.91.219, 5.161.241.43) on Hetzner DE confirmed. Accept or send to red-team?

[[Pipeline-Gates|Gate status →]] · [[Chain-of-Custody|COC →]]

---

## FLOW — Pipeline & sprint

> [!agent]+ Latest Session
> *What happened last session, across all repos.*

![[session-manifests/LATEST-manifest]]

> [!agent]+ Sprint Queue
> *Run `/run` in Claude Code to consume next task.*

![[session-briefs/LATEST-brief]]

[[Session-Manifests|All manifests →]] · [[Phase1-AgentSync|Full agent view →]]

---

## Narrative Waves

| Wave | Chapter | Status |
|------|---------|--------|
| [[00-SHARED/MEMROUND/criticalexposure/WAVE-01-The-Emergence\|WAVE-01]] | The Jan 14 Inflection | 📝 Draft |
| [[00-SHARED/MEMROUND/criticalexposure/WAVE-02-The-Infrastructure\|WAVE-02]] | The Infrastructure | 📝 Draft |
| [[00-SHARED/MEMROUND/criticalexposure/WAVE-03-The-Foreign-Fingerprints\|WAVE-03]] | Foreign Fingerprints | 📝 Draft |
| [[00-SHARED/MEMROUND/criticalexposure/WAVE-04-The-Malware\|WAVE-04]] | DOGE Malware | 📝 Draft |
| Wave 05 | Statistical Evidence | ⬜ Queued |
| Wave 06 | Personnel | ⬜ Queued |

*All waves Final → shift to [[Phase2-Publication]]*

---

## Your Space

> [!note]- Your Annotations — private, agents never write here
> *What you believe and why. Connections you see. Things that feel wrong. The story in your own words.*

> [!note]- Court Prep — private
> - [ ] Jan 14 inflection — why not a collection artifact
> - [ ] Reflected TLS — how a C2 appears as Treasury HTTPS
> - [ ] OR=123.7 — what the null hypothesis predicts
> - [ ] Staging sequence — Aeza → Baxet → Alibaba
> - [ ] Luke Farritor — who, what access, why it matters
> - [ ] Negative control on 83.149.30.186 — what it proves

---

*FINDINGS · FLAGS · FRICTION · FLOW — [[Phase1-AgentSync|Agent view]] · [[Phase2-Publication|Publication]] · [[Hypothesis-Tracker|Hypotheses]] · [[Annotation-Dash|Annotations]]*
