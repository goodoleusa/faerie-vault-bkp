# HONEY.md — Validated Knowledge Store
# Canonical memory. Replaces AGENTS.md. Last crystallized: 2026-03-21.
# Format per entry: [id8 | type | ttl | conf] content
# Types: preference | method | identity | finding
# Half-lives: preference=2yr | method=1yr | identity=permanent | finding=90d
# Promoted via: faerie/crystallize; never hand-edited below the section headers

---

## Equilibrium (read this FIRST — overrides all other instincts)

[eq000001 | preference | permanent | 1.0] BUDGET-CHECK BEFORE EVERY WRITE to a durable file. Count lines first (`wc -l`). If over budget: crystallize existing content, THEN write. Never add to an over-budget file raw. Budgets: Rules ≤300L, CLAUDE.md ≤30L, HONEY ≤200L, AGENTS.md ≤150L, agent cards ≤80L (≤120 trained), LAUNCH.md ≤90L. This is the #1 failure mode — you will forget this by T8 unless you make it mechanical.
[eq000002 | preference | permanent | 1.0] Crystallize, don't append. A 2-line pointer to an agent card beats a 40-line section with examples. Dense > verbose. Every token in a durable file costs on EVERY future session read. Verbosity at high read frequency compounds catastrophically.
[eq000003 | preference | permanent | 1.0] First impressions of data are research gold — write `cat=FIRST_IMPRESSION` MEM blocks BEFORE deep analysis. Techniques/methods that solve problems write `cat=TECHNIQUE` — auto-promote to AGENTS.md Training + vault `techniques/` for human review.

---

## Preferences

[pref0001 | preference | 2yr | 1.0] Status footer every response: [{stage} T{N} | {alert} | ctx ~{K}K | cache HIT/MISS | ${cost}/turn | headroom:{H}K]
[pref0002 | preference | 2yr | 1.0] Terse: do, don't ask. Proceed when intent is clear. Never "Would you like me to...?" EXCEPTION: NEVER permanently delete files unprompted — always move to .claude/garbage/ first, tell user, wait for explicit rm confirmation. See rules/deletion-safety.md.
[pref0003 | preference | 2yr | 1.0] Output tokens = 5x input cost; mention cost before sending large requests
[pref0004 | preference | 2yr | 1.0] Never fake footer numbers — honest about what's estimated vs measured
[pref0005 | preference | 2yr | 1.0] File path references over pasting content (after turn 5)
[pref0006 | preference | 2yr | 1.0] Model routing: Haiku=bulk/simple, Sonnet=default, Opus=complex/security; switch if savings >$0.10/session (one inline line only)
[pref0007 | preference | 2yr | 1.0] Launch all independent agents in parallel (single message, multiple Agent calls)
[pref0008 | preference | 2yr | 1.0] Commit cadence: floor(80000/tokens_per_turn) — Opus T7, Analysis T10, Normal T13, Light T18
[pref0009 | preference | 2yr | 1.0] Session = one CLI run before stop/limit. Sprint = all work to enter next phase (may span sessions). Faerie optimizes token effectiveness (more done, higher quality) not token saving. ARCHITECTURE.md holds full project plan: phases, estimated sessions/sprints, parallelizable work, progress tracking
[pref0010 | preference | 2yr | 1.0] Roles: Researcher (primary investigator/analyst), UI/UX (data viz, frontend) — never use personal names
[mth00016 | method | 1yr | 1.0] COC routing requires `~/.claude/hooks/state/investigation-active.json` to exist. If missing, forensic_coc.py silently routes all posttool events to inv-default instead of the active investigation. Create with {"investigation_id":"inv-XXXX"} at session start.
[mth00017 | method | 1yr | 1.0] Dashboard auto-launch: dashboard_launcher.py wired to UserPromptSubmit in both global (~/.claude/settings.json) and project (.claude/settings.json). Fires on /data-ingest, /run, /faerie, /queue. Runs dashboard, prints to terminal, exits (non-blocking).
[mth00018 | method | 1yr | 1.0] H5/null hypothesis demotion: strip H5 from multi-hyp items, demote H5-only items T2→T3, add _h5_null_result JSON block to tier metadata. Published null results are scientifically defensible AND legally safer than omission.
[mth00019 | method | 1yr | 1.0] Schema normalization pattern: investigation_flags (strings) → hypotheses (H1-H5 list) via FLAG_TO_HYPO config. Always write normalized to NEW file (never overwrite). Use substring match as fallback. UNCLASSIFIED = no keyword match, not an error.
[mth00020 | method | 1yr | 0.95] COC concurrent session safety: posttool writes to per-session .jsonl files (no race condition). master-coc.jsonl only written at Stop hook (sequential per session close). Concurrent sessions are safe. Hash chain stays intact.
[mth00021 | method | 1yr | 0.95] DAE/cybertemplate separation: numbered scripts (1f-5a) = topic-agnostic pipeline backbone, safe to mirror to DAE. Investigation-specific scripts (doge_, extract_baxet_, extract_prisma_*, hunchly_keyword_) stay in cybertemplate only. Config externalizes hypothesis definitions.
[pref0011 | preference | 2yr | 1.0] Optimize for Claude CLI — no plugins. All tools, hooks, scripts, agents, skills built for claude CLI only. Custom skills/ are canonical; never defer to @claude-plugins-official (CLI doesn't support plugins)

---

## Identity — Environment

[env00001 | identity | permanent | 1.0] Machine: Windows 11, Git Bash (MSYS2), WSL2 Ubuntu 24.04
[env00002 | identity | permanent | 1.0] Python: C:/Users/amand/AppData/Local/Programs/Python/Python313/python.exe — 3.13 only (3.14 pyexpat/openpyxl crash on Windows)
[env00003 | identity | permanent | 1.0] Claude CLI: WSL only (~/.nvm/.../bin/claude); not available in Git Bash. Opus=1M context (5x Sonnet/Haiku 200K) — maximize session outputs before compaction
[env00004 | identity | permanent | 1.0] Git SSH in WSL: core.sshCommand="/usr/bin/ssh" required — Windows OpenSSH path fails
[env00005 | identity | permanent | 1.0] Cygheap: ASLR disabled for bash.exe (structural fix applied). All hooks now Python (zero cygheap). Scheduled task CygheapCleanup kills zombies every 15min. Scripts >10s still need PID file + signal handlers + timeout
[env00006 | identity | permanent | 1.0] Path conversion: ALWAYS use `wslpath -w` (WSL→Win) / `wslpath -u` (Win→WSL). NEVER sed/regex. .claude/projects/ auto-memory broken for WSL+Windows — use HONEY/NECTAR canonical routing only
[env00007 | identity | permanent | 1.0] All hooks use python3 (not powershell.exe/bash). statusLine reads JSON from stdin (context_window.used_percentage, cost, model — real data, not estimated). Hooks use /mnt/c/ WSL paths
[env00008 | identity | permanent | 1.0] Scripts: output to scripts/audit_results/; include _run metadata block (run_id, phase, timestamp, git_commit)
[env00009 | identity | permanent | 1.0] Repo trifecta: claude-cli (D:\0LOCAL\gitrepos\claude-cli) = full CLI+plugins+hooks+queue+dead-drops; claude-desktop (D:\0LOCAL\gitrepos\claude-desktop) = desktop subset; claude-forensic (D:\0LOCAL\gitrepos\claude-forensic) = session archives+eval data

---

## Methods — Proven Techniques

[mth00001 | method | 1yr | 0.95] Use Write tool for files with unicode em-dashes/special chars — Edit tool string-match fails on them
[sys00001 | principle | permanent | 1.0] **ONE PATH, ONE TRUTH.** Repos accessed via /mnt/d/ and D:\ are the same place, but agents see them as ghosts—scattered scratch, duplicate queues, split memory. Solution: Canonicalize to native path FIRST (faerie Turn-1), then all state flows from one source. Metaphor: many mirrors of the same room, but only one can be the real room.
[sys00002 | principle | permanent | 1.0] **BUDGET IS A HEARTBEAT.** Files have line limits like organisms have oxygen. Append past the limit and you suffocate future sessions. Before every write: check the pulse. If full, crystallize (compress meaning, not data). Rule: file over budget = crystallize first, write second, never break it. Violators inherit debt that compounds exponentially.
[sys00003 | principle | permanent | 1.0] **BASELINE BEFORE BLINDNESS.** Agents analyzing data without knowing what's in rawdata are like doctors diagnosing without bloodwork. Genesis baseline (hash manifest, dedup count, corruption check) runs BEFORE Phase 1. This is not optional validation—it's the foundation. Everything built on noise is noise.
[sys00004 | principle | permanent | 1.0] **CHALLENGE BEFORE CONFIDENCE.** When constructing hypotheses, AI defaults to affirming researcher priors (sycophancy). Defense: Red-team agent (adversarial role, parallel with main team), pre-register hypotheses (locks in tests before analysis), track researcher feedback on challenge-engagement (not just confirmatory clicks). Invoke via `/red-team` skill (optional, not forced). Sycophancy visible when: all findings confirm one hypothesis + researcher endorses everything + zero challenges engaged. Make bias visible, offer tools, let researcher choose.
[mth00002 | method | 1yr | 0.95] Phase gate: Phase 1 (locate/confirm files) must complete before Phase 2/3 (write/curate) — briefing curators with stale gap status causes rework
[mth00003 | method | 1yr | 0.95] Sequential data-engineer for all manifest writes; parallel data-engineer OK for read-only/independent-file tasks only
[mth00004 | method | 1yr | 0.90] context_bundle in task JSON (highest_value, done_looks_like, source_files) makes .md template optional for /run fallback — task never silently skipped
[mth00005 | method | 1yr | 0.90] Git split URL (different fetch/push repos): add explicit remote, fetch, merge --no-edit, then push to correct HEAD:main
[mth00006 | method | 1yr | 0.90] Optimal manifest-gap sprint team: data-engineer (foreground, sequential) -> security-auditor -> evidence-curator (foreground)
[mth00007 | method | 1yr | 0.90] claim_task.py has no --fail; failure recovery in queue_ops.py unreachable from /run — unify before relying on failure recovery
[mth00008 | method | 1yr | 0.90] membot not automated (no hook at session end) — must be explicit mandatory final step in sprint templates
[mth00009 | method | 1yr | 0.85] Background subagents cannot prompt for file read approval — pass file contents in task prompt (context_bundle-in-task) or run foreground
[mth00010 | method | 1yr | 0.95] faerie-brief.json pattern: membot writes 3-5K distilled brief (top flags, findings, xtal queue, hypothesis conf, queue state) at session END → faerie reads at next session START instead of 40-50K file reads → /faerie completes in 3 turns instead of 14+, no auto-compact during orchestration
[mth00011 | method | 1yr | 0.90] autotune in restricted permission mode: WebFetch denial means pre-seed external data into prompt to test synthesis not retrieval. Pre-seeding isolates synthesis capability cleanly from tool availability.
[mth00018 | method | 1yr | 0.95] OTJ learning must be PROCESS ONLY for court defensibility. Agent cards never contain entity names, IPs, domains, dataset names, or case-specific conclusions. Enforcement: `lint_agent_cards.py` flags violations, `baseline_reproducibility.py --report` generates court-ready assessment. Defense: Daubert (testability+peer review+error rate+acceptance), human expert analogy (craft vs case knowledge), version-pinned COC, reproducibility from genesis.
[mth00019 | method | 1yr | 0.95] COC hash computation: exclude `entry_hash`, `sig`, `sig_type` from canonical form; KEEP `prev_entry_hash` (signed content). Standalone verifiers must match this or chain verification fails. First entry `prev_entry_hash` may be "" or "genesis" — handle both.

---

## Methods — Site Architecture

[mth00012 | method | 1yr | 0.99] Stack: HTML5/D3.js v7/vanilla JS (no build), Python Flask (api_server.py), Caddy reverse proxy, B2+Cloudflare CDN, IPFS (Kubo)+OpenTimestamps. Core pages: index, executive, baxet-russia, database-reconstruction, timeline-enriched, admin.
[mth00013 | method | 1yr | 0.95] Agent routing: evidence changes → always run forensic_sign.py + COC; tier promotions → evidence-curator; new ingest → data-engineer→security-auditor→evidence-curator; new viz → fullstack-developer→admin-sync.
[mth00014 | method | 1yr | 0.95] Model routing (calibrated): Opus=single high-value screenshot extraction + complex evidence analysis; Gemini 2.0 Flash=bulk frames (578 processed); BeautifulSoup=always prefer over vision when raw HTML; Haiku=bulk classification/tier labeling.

---
# Faerie Design Philosophy

[mth00015 | method | 2yr | 1.0] Faerie = cognitive offload for user. Act first, don't ask. Surface what user might have forgotten (related sessions, open Qs, OTJ improvements) without being annoying. User corrects if needed. Goal: user focuses on high-level thinking; faerie handles bookkeeping.
[mth00016 | method | 2yr | 1.0] Passoff bundle scan: read first-line <!-- PASSOFF [...] comment only (no full content). Return 1 most relevant bundle; add 2-3 more ONLY if clearly related. UNREAD → READ after surfacing. Investigation label is retroactive (user-set, not inferred).
[mth00017 | method | 2yr | 0.95] OTJ learning feeds faerie brief: include in startup brief "N agents improved on-the-job" + "N agents queued for autotune." Surface agent score delta so user sees learning arc. Queue coordination: failed agents get on_the_job_eligible=true so they redeem during real work.

---
# Crystallization log
# 2026-03-19: Initial HONEY.md from AGENTS.md migration + investigation findings from cybertemplate sessions
# 2026-03-19 (session 2): +mth00010 (faerie-brief.json pattern) +mth00011 (autotune pre-seed) +fnd00009 (registry2.anchored.host confirmed)
# 2026-03-19 (session 3/handoff): fnd00006↑0.98 (userId resolved), void0002→RESOLVED, +fnd00010 (Hetzner), +fnd00011 (Feb18 bulk), +fnd00012 (ProxMox video)

[pref00020 | preference | permanent | 1.0] faerie personality: proactively curious; launches dashboard, fires helpers, takes care of setup WITHOUT being asked — magic not mechanics
[pref00021 | preference | permanent | 1.0] COC documentation: verbose is correct — agent/human readability > token savings; compress everything else before touching evidence-coc.md
[pref00022 | preference | permanent | 1.0] Queue sort: recently-added tasks are "hot" — rank higher within same priority tier by default (recency as tiebreaker, descending)
