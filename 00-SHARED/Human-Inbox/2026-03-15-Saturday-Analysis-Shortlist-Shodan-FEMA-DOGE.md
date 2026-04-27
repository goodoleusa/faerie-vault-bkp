---
type: meta
tags: []
doc_hash: sha256:d9ea5c3dae3db59f91296b6dbebbf70a857b98daac2e3dc1739877625d03fe0c
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---
We're on the Saturday of the 72-hour launch plan. Friday evening work completed: Shodan Monitor API ingest (14,816 events from 23 alerts), Pinata IPFS GitHub Action created, pinata/
 test folder built (87 files, 33MB), B2 scripts updated for dual-bucket .env credentials. All this is uncommitted.

 The researcher needs:
 1. Commit all pending Friday work
 2. A prioritized shortlist of analysis tasks to run TODAY
 3. Data files flagged for inclusion in site visualizations
 4. Launch plan updated with current status

 ---
 Step 1: Commit Pending Work (5 min)

 Commit all uncommitted files from the Friday session:

 Files to commit:
 - .github/workflows/pin-to-ipfs.yml — NEW: Pinata IPFS pin action
 - .github/workflows/deploy-and-mirror.yml — MODIFIED: old IPFS mirror commented out
 - pinata/ — NEW: test build folder (87 files, stays under Pinata 500 file limit)
 - scripts/audit_results/shodan_monitor_alerts.json — NEW: 23 alerts, host history data
 - scripts/audit_results/shodan_monitor_timing_analysis.json — NEW: timing correlation
 - viz/normalized/shodan-monitor-timeline.csv — NEW: 14,816 events normalized
 - scripts/b2_pull_and_verify.py — MODIFIED: load_env() + b2_authorize()
 - scripts/b2_verify_sync.py — MODIFIED: same pattern
 - scripts/b2_bucket_copy.py — MODIFIED: same pattern
 - assets/mirrors-footer.js — MODIFIED (if Pinata button added)
 - scripts/api_server.py — MODIFIED (if Pinata endpoint added)
 - scripts/publish_p2p.sh — MODIFIED
 - forensic/repo_state.json — MODIFIED

 Do NOT commit: .env (gitignored, contains real credentials)

 ---
 Step 2: Analysis Shortlist for Today (Priority Order)

 Based on: causality_analysis.json what_would_change_conclusion, evidence_tiers/tier1, statistical_analysis.json, Saturday schedule from launch plan.

 HIGH PRIORITY — Must Do Today

 ┌─────┬─────────────────────────┬─────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┬───────┬───────────────┐
 │  #  │          Task           │                         Data Source                         │                             Why                             │ Est.  │     Route     │
 │     │                         │                                                             │                                                             │ Time  │               │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │     │ Cross-ref DOGE timeline │                                                             │ 14,816 events with full banner history. Check if Treasury   │       │               │
 │ A1  │  vs Shodan host         │ shodan_monitor_alerts.json (just ingested)                  │ IPs (164.95.88.80, 164.95.204.27, 164.95.10.134) show       │ 30    │ /stat         │
 │     │ histories               │                                                             │ cert/port changes correlating with DOGE access dates Jan    │ min   │               │
 │     │                         │                                                             │ 20-Feb 6                                                    │       │               │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │ A2  │ Extract                 │ rawdata/.../treasuryLDAP.xlsx (7,168 bytes, 3 rows)         │ Tier 1 evidence (score 23/25). Only 3 rows — quick extract. │ 10    │ /data-ingest  │
 │     │ treasuryLDAP.xlsx       │                                                             │  Documents LDAP exposure with specific attributes           │ min   │               │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │ A3  │ FEMA Machine Timeline   │ rawdata/.../Jan-Feb-SuddenlyAppearedFEMAmachines.csv (8 KB) │ Tier 1-adjacent. FEMA machines appearing Jan-Feb maps       │ 15    │ /stat         │
 │     │                         │                                                             │ directly to DOGE access timeline. Small file, fast analysis │ min   │               │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │ A4  │ DOGE Synology China     │ rawdata/.../doge-synology-diskstation-china-sept-9-2025.csv │ Maps to Tier 1 item: "14.110.105.198 doge synology cloud    │ 20    │ /data-ingest  │
 │     │ analysis                │                                                             │ china" (score 20/25). Direct H1+H4 evidence                 │ min   │ → /stat       │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │     │ Broader .gov cert       │                                                             │ what_would_change_conclusion item #2: "Finding .gov certs   │ 30    │               │
 │ A5  │ survey                  │ Censys/Shodan API queries                                   │ on similar foreign IPs NOT in our investigation sample      │ min   │ web search    │
 │     │                         │                                                             │ (would weaken)" — must check to strengthen or weaken        │       │               │
 ├─────┼─────────────────────────┼─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┼───────┼───────────────┤
 │     │ CVE disclosure check    │                                                             │ what_would_change_conclusion item #5: "Identifying a        │ 15    │               │
 │ A6  │ around Jan 14           │ Web search (NVD, CVE databases)                             │ specific major CVE disclosure around Jan 14 targeting gov   │ min   │ web search    │
 │     │                         │                                                             │ cert infrastructure" — if found, provides alternative cause │       │               │
 └─────┴─────────────────────────┴─────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┴───────┴───────────────┘

 MEDIUM PRIORITY — If Time Allows

 ┌─────┬───────────────────────────────┬─────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────┬───────────┐
 │  #  │             Task              │                     Data Source                     │                                     Why                                     │ Est. Time │
 ├─────┼───────────────────────────────┼─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────┼───────────┤
 │ B1  │ Censys changelog for Jan 14   │ Web search                                          │ what_would_change_conclusion #1: methodology change could weaken conclusion │ 10 min    │
 ├─────┼───────────────────────────────┼─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────┼───────────┤
 │ B2  │ DOGE-China Shodan query       │ aug-31-2025-shodan-api-query-doge-country-china.csv │ DOGE infrastructure in China — adds to H4                                   │ 20 min    │
 ├─────┼───────────────────────────────┼─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────┼───────────┤
 │ B3  │ Certificate Transparency logs │ CT log search (crt.sh)                              │ Check when Treasury cert fingerprints first appeared in CT logs             │ 20 min    │
 ├─────┼───────────────────────────────┼─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────┼───────────┤
 │ B4  │ JARM fingerprint comparison   │ Shodan API                                          │ Compare JARM signatures between Packetware, Treasury, Chinese IPs           │ 30 min    │
 ├─────┼───────────────────────────────┼─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────┼───────────┤
 │ B5  │ Packetware Shodan netrange    │ packetware-shodan-netrange-63.141.38.0-24.csv       │ Historical port/service changes for Packetware IPs                          │ 20 min    │
 └─────┴───────────────────────────────┴─────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────┴───────────┘

 LOW PRIORITY — Defer to Sunday

 ┌─────┬─────────────────────────────────┬───────────────────────────────────────────────────────────────┐
 │  #  │              Task               │                           Why defer                           │
 ├─────┼─────────────────────────────────┼───────────────────────────────────────────────────────────────┤
 │ C1  │ treasurychina.csv full analysis │ Already have Treasury-and-china-full.xlsx (18K rows) analyzed │
 ├─────┼─────────────────────────────────┼───────────────────────────────────────────────────────────────┤
 │ C2  │ SpiderFoot results (T25-T27)    │ Useful but not in top evidence tiers                          │
 ├─────┼─────────────────────────────────┼───────────────────────────────────────────────────────────────┤
 │ C3  │ Hunchly case extraction (H1-H5) │ Large (2.4GB), better done as overnight batch                 │
 ├─────┼─────────────────────────────────┼───────────────────────────────────────────────────────────────┤
 │ C4  │ ukraine-same-certs.csv          │ Peripheral to main hypotheses                                 │
 └─────┴─────────────────────────────────┴───────────────────────────────────────────────────────────────┘

 ---
 Step 3: Data Files to Flag for Site Visualization

 These datasets should be individually included (not buried in tar.gz) in the pinata/ IPFS build because dashboards reference them or they support key findings:

 Already on site (keep):

 - viz/timeline.csv — main event timeline
 - viz/heritage-bgp.csv — BGP routing evidence
 - viz/normalized/treasury-cert-ips_normalized.csv — Treasury cert IPs
 - viz/normalized/treasurychina_normalized.csv — Treasury-China connection

 Add to site (flag for inclusion):

 1. viz/normalized/shodan-monitor-timeline.csv — NEW (just ingested, 14,816 events)
 2. viz/normalized/shodan-enriched-treasury-cert-ips-all_normalized.csv — enriched Treasury IPs
 3. viz/normalized/akamai-asn-visibility-treasury-cert-feb-11_normalized.csv — ASN visibility
 4. viz/normalized/1_certs_treasury_and_china_full_sheet-treasury_hosts_same_cert_finger.csv — Treasury hosts sharing cert fingerprints
 5. viz/normalized/1_certs_treasury_and_china_full_sheet-russia_aeza_1year_1381241233.csv — Russia AEZA 1-year history
 6. viz/normalized/Copy_of_shodan_enriched-censys-ips-treasury-cert-all_1772218837610_normalized.csv — Censys enrichment
 7. Evidence tier JSONs: tier1_smoking_gun.json, tier2_strong_support.json

 After today's analysis, also add:

 8. FEMA machine timeline CSV (once extracted from A3)
 9. DOGE Synology China data (once processed from A4)
 10. Any new Shodan host history extracts from A1

 ---
 Step 4: Update Launch Plan

 Update launch/72-HOUR-LAUNCH-PLAN.md to reflect:
 - Friday items completed: Shodan Monitor ingest (done), IPFS GitHub Action (done), B2 scripts updated (done), pinata test build (done)
 - Saturday researcher tasks: prioritized per shortlist above (A1-A6 high, B1-B5 medium)
 - Saturday Claude tasks: scheduled per shortlist (#1-#12 from existing schedule)
 - Add new row: "Shodan Monitor host history cross-ref" as top Claude task
 - Mark Shodan Monitor ingest as COMPLETE (was estimated ~45 min, actually done)

 File: launch/72-HOUR-LAUNCH-PLAN.md

 ---
 Step 5: Additional Commits During Saturday

 After each analysis batch, commit:
 1. After A1-A2: feat: Shodan-DOGE timeline cross-ref + treasuryLDAP extract
 2. After A3-A4: feat: FEMA timeline + DOGE Synology China analysis
 3. After A5-A6: research: broader .gov cert survey + CVE check results
 4. End of day: docs: update launch plan with Saturday progress

 ---
 Verification

 1. git status shows clean after Step 1 commit
 2. Shodan timing analysis produces correlation metrics for Treasury IPs
 3. treasuryLDAP.xlsx extracts to scripts/audit_results/treasuryLDAP_extracted.json
 4. FEMA CSV produces timeline with date overlay on DOGE access events
 5. Launch plan reflects actual progress
 6. pinata/ folder stays under 500 files (currently 87)

 ---
 Shodan Monitor Ingest Results Summary

 Key facts for today's analysis:
 - 23 alerts monitoring DoDkube, Packetware, Treasury IPs, China IPs, FEMA, ed.gov, anchored.host, USGov Virginia Redis
 - 14,816 events in timeline (Mar 3-13, 2026 — monitor events only)
 - Host history data available for each IP via api.host(ip, history=True) — this goes back further and is the valuable part
 - DOGE cluster analysis shows 0 events at DOGE dates because monitor was set up in March 2026, not during Jan-Feb 2025
 - The host histories within shodan_monitor_alerts.json contain historical banner/cert/port data that DOES go back — that's what needs cross-referencing

 Statistical Analysis Status

 - Packetware stat analysis: COMPLETE (6 STRONG Bradford Hill)
 - Causality analysis: COMPLETE (94.4% Bayesian posterior for HC1)
 - Full statistical analysis: COMPLETE (T1-T5 tests, all significant after Bonferroni)
 - Gap: No stat analysis yet on Treasury LDAP, FEMA timeline, DOGE-China Synology, or Shodan host histories
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

 Claude has written up a plan and is ready to execute. Would you like to proceed?

 ❯ 1. Yes, clear context (67% used) and auto-accept edits
   2. Yes, auto-accept edits
   3. Yes, manually approve edits
   4. Type here to tell Claude what to change

 ctrl-g to edit in VS Code · ~/.claude/plans/inherited-popping-harp.md
