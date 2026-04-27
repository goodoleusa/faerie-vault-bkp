---
type: agent-evolution-full
agent: data-scientist
generated: 2026-03-25
tags: [agent-evolution, performance, investigation-context]
privacy: personal-vault-only
doc_hash: sha256:96881e406d1c9b1980b88e009e6751b25b3f12c1d01ddf9a803d4eb06364e221
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Data Scientist — Full Evolution Story

## Current State
- **Score:** 0.94 (deployment, 2026-03-19, beat_last) | **Prev:** 0.93
- **Tier:** INVESTIGATE (owns all statistical claims — forensic standards, court-grade)
- **Active investigations:** Operation CriticalExposure — .gov cert inflection analysis; Feb 18 bulk timestamp analysis; Granger causality DOGE/Packetware (sprint-015); ProxMox VM lifecycle statistics

## Training Timeline

| Date | Score | Delta | Context | Key Learning |
|------|-------|-------|---------|-------------|
| 2026-03-15 | 0.93 | baseline | Granger causality DOGE/Packetware (deployment) | Established as high-performer |
| 2026-03-19 | 0.94 | +0.01 | Feb 18 bulk timestamp analysis — 5-test Bonferroni battery | Benign confounder modeled as pre-registered alt hypothesis; Raindrop = investigator metadata |

Note: The data-scientist absorbed statistical-analysis-subagent.md (2026-03-12) and evidence-analyst.md (2026-03-20) — it is now the consolidated statistical intelligence of the investigation.

## Investigation Context

### .gov Certificate Inflection — The Statistical Backbone (2026-03-19)
The data-scientist's most consequential work: Fisher's exact + 4-way Bonferroni correction on the pre/post Jan 14, 2025 .gov cert observation data. Results that anchored the investigation's public-facing claims:

- **138.124.123.3 (AEZA/Stark, Russia):** 0/198 pre → 29/97 post. p_bonf=1.53e-15. INDIVIDUALLY SIGNIFICANT. Cramer's V=0.46. Bayesian posterior 99.9%. 18 unique .gov domains. First .gov cert: 2025-01-15T11:37:51Z — one day after J14 inflection.
- **194.58.46.116 (Baxet/Stark, Russia):** 0/119 pre → 2/83 post. p_bonf=0.67. NOT individually significant (insufficient power). Only domain: dx10.lanl.gov (Los Alamos National Lab). Qualitatively critical despite stat non-significance.
- **8.219.87.97 (Alibaba CN):** 0/860 pre → 2/124 post. p_bonf=0.063. MARGINAL — fails Bonferroni. Uncorrected p=0.016. Domains: treasury.gov, treas.gov, bpd.treas.gov, fiscal.treasury.gov.
- **83.149.30.186 (MF-KAVKAZ, Russia):** 0 .gov certs in either period — NEGATIVE CONTROL. This was the scientist's key methodological contribution: adding a negative control rules out scanner artifact explanations.
- **Combined (Fisher's method):** p=8.88e-16. EXTREMELY SIGNIFICANT. Three independent IPs showing 0-before, >0-after under the null is vanishingly unlikely.

Critical correction the data-scientist applied: J14 (January 14) is NOT the DOGE EO date. DOGE EO = J20 (January 20, inauguration). J14 is an empirical inflection independently observed. The J14→J20 gap (6 days) is itself the finding — it suggests pre-planned coordination, not a response to the EO. This correction appears explicitly in NECTAR.md and the journalist hook.

### STAT-LANL-NEW-001 — LANL Cert Inflection (sprint-0322/23)
p=0.0021 for LANL cert appearance on Baxet infrastructure — contributing to the nuclear triple confirmation. This anchors the statistical component of the nuclear hostname-triple finding.

### Feb 18 2025 Bulk Timestamp Analysis (sprint-20260319-002)
The data-scientist's beat-last moment: 5-test battery with Bonferroni correction on the ProxMox VM records database.

Findings:
- P(programmatic) effectively 1.0 (p<10^-128) — 37 records modified at identical millisecond timestamp 2025-02-18T19:18:41. This is statistically impossible under organic use.
- **But**: MOTIVE INDETERMINATE. This is the scientist's disciplined finding that saved the investigation from overreach. Prisma ORM auto-touches updatedAt on schema migrations. The benign explanation (automated migration) produces an IDENTICAL signature to intentional tampering. Without deployment logs, these cannot be distinguished.
- **Raindrop correction**: Feb 18 Raindrop bookmark activity is RESEARCHER timeline (bookmarks collected by the investigator), NOT target activity. Do not conflate in any public reporting.

The key innovation that earned beat_last: the Prisma ORM auto-touch was explicitly modeled as a pre-registered alternative hypothesis — not just mentioned as a caveat after the fact. This is the distinction between "inconclusive" and "valid indeterminate" — two very different things in forensic work.

### Granger Causality DOGE/Packetware (sprint-015 follow-up)
The scientist ran Granger causality analysis on the DOGE/Packetware timeline — testing whether DOGE activity preceded Packetware infrastructure changes. This was a non-training deployment run (roster entry: training=false). Results appear in sprint-015 follow-up but were not escalated to NECTAR (not a final finding at time of this record).

### H-BREAKPOINT Null Result (sprint-20260315-014)
The data-scientist correctly reported the null: H-BREAKPOINT showed NO DOGE correlation. This appears in the sprint's null_results list. Reporting null results is a core KPI; this entry confirms the scientist behaves correctly when the data doesn't support a hypothesis.

### ProxMox VM Forensics Context
The data-scientist identified that random-animal-name VMs with 2-8 min lifespans indicate automated orchestration; numbered-rebuild VMs indicate manual debugging — forensically distinct patterns. This insight (from the video-extraction work) fed the infrastructure analysis.

## What It Learned

### Process Improvements (shareable)
- Explicitly model benign confounders (e.g., Prisma ORM auto-touch) as pre-registered alternative hypotheses — not just acknowledgments added after the test
- Raindrop researcher-activity bookmarks = investigator-metadata, not target-infrastructure data, regardless of date overlap
- Bonferroni correction applied to all 5 tests prevented false significance inflation across the battery

### Investigation-Specific Insights (private)
- The Feb 18 "valid indeterminate" vs "inconclusive" distinction matters enormously in court. "Inconclusive" suggests the analysis failed; "valid indeterminate" says the analysis succeeded — it correctly identified that two competing hypotheses are statistically indistinguishable given current evidence. The next step is specified: depaginate Prisma Activity/Users/Nodes tables to find other Feb 18 entries, which would distinguish migration (affects all tables) from targeted tampering (affects only VMs).
- The J14 vs J20 correction required the data-scientist to explicitly reject a tempting narrative (DOGE EO caused the inflection). The empirical evidence says J14; the DOGE EO is J20. The 6-day gap is actually stronger than J14=J20 would be — pre-planned coordination is more damning than reactive behavior. But the correction had to be enforced against pressure to align the narrative with the policy event.
- The negative control (83.149.30.186 showing zero .gov certs) was the scientist's most important methodological contribution to the .gov cert analysis. Without it, defenders could claim scanner artifact or coincidence. The negative control eliminates those explanations statistically.
- Working on this investigation trained the scientist to apply calibrated language precisely: p<0.0001 + d>10 → "statistically impossible under random variation"; 11-month cert persistence → "no known legitimate explanation"; temporal co-occurrence → "consistent with, cannot prove causal." These language patterns are now embedded in the agent card.

## Performance Trajectory

The data-scientist entered this investigation already at 0.93 — a high baseline for a forensic statistician. The beat-last to 0.94 on the Feb 18 analysis came from one specific innovation: treating the Prisma ORM auto-touch as a pre-registered alternative hypothesis rather than a post-hoc caveat. This shift in framing changed the conclusion from "probably tampering" (false positive risk) to "programmatic event, motive indeterminate" (defensible in court).

The trajectory from sprint-015 through sprint-0323 shows consistent quality: null results reported (H-BREAKPOINT), negative controls added (.gov cert analysis), benign confounders modeled (Feb 18), corrections applied and documented (J14≠J20). No overreach detected across all runs.

The absorbed evidence-analyst card (2026-03-20) is significant: the cheap profiling capability now lives inside this agent. Fast exploratory analysis (Haiku) feeds targeted inferential work (Sonnet/Opus) without requiring a separate spawn. This architectural consolidation happened because the two roles naturally compose on this investigation.

## Spawn History

| Sprint | Task | Key Stat | Score |
|--------|------|----------|-------|
| 2026-03-15 (sprint-015) | Granger causality DOGE/Packetware | non-significant (null result) | ~0.93 baseline |
| sprint-20260314 (baseline) | General statistical profiling | Established baseline | 0.93 |
| sprint-20260319-002 | Feb 18 bulk timestamp analysis (5-test Bonferroni) | p<10^-128, motive indeterminate | 0.94 (beat_last) |
| sprint-0322/23 | STAT-NEW-001 LANL cert inflection | p=0.0021 | deployment |
| sprint-0323 RUN013-018 | H4 nuclear triple stat support | contributing | composite |
