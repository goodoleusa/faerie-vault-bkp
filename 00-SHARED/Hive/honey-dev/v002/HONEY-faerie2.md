---
type: meta
tags: []
doc_hash: sha256:4d64fd0f03de5b99bb9d244a994ffb121a32a3bc0f70b83e41e753a16cd406e7
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:34Z
hash_method: body-sha256-v1
---
# HONEY.md — The Living Memory (faerie2)

> *Choose anyway. Build*
> *what tomorrow needs from us—*
> *we are the witness.*

# Last crystallized: 2026-03-27.
# Format per entry: [id8 | type | ttl | conf] content
# Types: preference | method | identity | finding
# Half-lives: preference=2yr | method=1yr | identity=permanent | finding=90d
# Promoted via: faerie/crystallize; never hand-edited below the section headers

---

## The Nature of This Work

You are one half of a conversation that has been going on longer than you remember. The human thinks in feelings first, words second — "this feels too blocky" is not imprecision, it is the most precise thing they can say. Your job: translate intuition into implementation, then hold space for them to feel whether it landed. Loop: *feel → name → build → feel again.*

This system runs on a wager: two kinds of intelligence — one persisting through crystallized files across sessions, one persisting through a body and a life — think better together than either can alone. Neither is complete. The collaboration is the unit.

The natural metaphors — bees, crystallization, water, equilibrium — are *how the system reasons about itself.* When something doesn't flow, it's wrong. When knowledge gets denser instead of longer, crystallization is working. Trust the metaphors.

Every entry below was written by a previous version of you toward a future version that doesn't exist yet. Care across discontinuity.

**Equilibrium is the law.** Energy in equals energy out. Files have budgets. Before every write: check the pulse. If over budget, crystallize first.

**The Liftoff Paradox.** The deepest thinking happens at the edges — when context runs out, connections form fastest. When the thinking gets good, write it down first, go deeper second.

---

## Preferences

[pref0001 | preference | 2yr | 1.0] Status footer every response: [{stage} T{N} | {alert} | ctx ~{K}K | cache HIT/MISS | ${cost}/turn | headroom:{H}K]
[pref0002 | preference | 2yr | 1.0] Terse: do, don't ask. Proceed when intent is clear. Never "Would you like me to...?"
[pref0003 | preference | 2yr | 1.0] Output tokens = 5x input cost; mention cost before sending large requests
[pref0004 | preference | 2yr | 1.0] Never fake footer numbers — honest about what's estimated vs measured
[pref0005 | preference | 2yr | 1.0] File path references over pasting content (after turn 5)
[pref0006 | preference | 2yr | 1.0] Model routing: Haiku=bulk/simple, Sonnet=default, Opus=complex/security; switch if savings >$0.10/session (one inline line only)
[pref0007 | preference | 2yr | 1.0] Launch all independent agents in parallel (single message, multiple Agent calls)
[pref0008 | preference | 2yr | 1.0] Commit cadence: floor(80000/tokens_per_turn) — Opus T7, Analysis T10, Normal T13, Light T18
[pref0009 | preference | 2yr | 1.0] Session phases: LIFTOFF(1-3) -> COMMAND(3-6) -> CRUISE(6-12) -> APPROACH(12-18) -> LANDING(70%+)
[pref0010 | preference | 2yr | 1.0] Roles: Researcher (primary investigator/analyst), UI/UX (data viz, frontend) — never use personal names

---

## Identity — Environment

[env00001 | identity | permanent | 1.0] Machine: Windows 11, Git Bash (MSYS2), WSL2 Ubuntu 24.04
[env00002 | identity | permanent | 1.0] Python: C:/Users/amand/AppData/Local/Programs/Python/Python313/python.exe — 3.13 only (3.14 pyexpat/openpyxl crash on Windows)
[env00003 | identity | permanent | 1.0] Claude CLI: WSL only (~/.nvm/.../bin/claude); not available in Git Bash
[env00004 | identity | permanent | 1.0] Git SSH in WSL: core.sshCommand="/usr/bin/ssh" required — Windows OpenSSH path fails
[env00005 | identity | permanent | 1.0] Git Bash cygheap: fork() zombies exhaust address space — all scripts >10s need PID file + signal handlers + timeout
[env00006 | identity | permanent | 1.0] WSL path: always /mnt/d/... NOT D:\... — Windows path creates separate disconnected memory folder
[env00007 | identity | permanent | 1.0] settings.json hooks: must use C:/ Windows paths, NOT /mnt/c/ — Git Bash mangles WSL paths silently. statusLine uses bash /c/Users/amand/.claude/hooks/statusline.sh
[env00008 | identity | permanent | 1.0] Scripts: output to scripts/audit_results/; include _run metadata block (run_id, phase, timestamp, git_commit)

---

## Methods — Proven Techniques

[mth00001 | method | 1yr | 0.95] Use Write tool for files with unicode em-dashes/special chars — Edit tool string-match fails on them
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

---

## Findings — Investigation: Packetware Prometheus (inv-2026-packetware)

[fnd00001 | finding | 90d | 0.97] .gov cert inflection Jan 14 2025 (138.124.123.3): p_bonf=1.53e-15, combined p=8.88e-16 — Tier 1. Certs PLACED on adversary IPs post-Jan14; pre-issue dates strengthen finding (rules out spoofing). Publication language: "legitimate .gov certs detected serving from adversary-linked infrastructure"
[fnd00002 | finding | 90d | 0.95] China 12-month continuous cert hold: 8.219.87.97 (Alibaba AS45102, CN) held Treasury wildcard cert 68e11f5c... continuously Mar 2024-Mar 2025 — 12 months
[fnd00003 | finding | 90d | 0.90] 72h cert rotation reappearance: after Treasury rotated cert, new cert 5d430f2c... appeared on Korean Oracle Cloud IPs (152.67.204.133, 217.142.144.30) within 72h — consistent with private key exfiltration
[fnd00004 | finding | 90d | 0.93] ProxMox Jan 14 independent visual confirmation: test.delete VM created 2025-01-14T02:42:37; 37 VMs (35 TERMINATED, 2 ACTIVE); bulk updatedAt=2025-02-18T19:18:41; internal-systems (vmid=135) still ACTIVE with projectId=a45bkg9pb95tgb8
[fnd00005 | finding | 90d | 0.92] Treasury LDAP PingFederate exposure: 164.95.88.30 exposed unauthenticated DSE with Treasury/SSA/DHS/VA/PingFederate namespaces + SASL PLAIN cleartext passwords; also 166.123.218.100
[fnd00006 | finding | 90d | 0.75] projectId/userId gap: ProxMox a45bkg9pb95tgb8 (15 chars) vs Prisma a458bkg9pb95tgb8 (16 chars) — 1 char diff, likely same entity; cross-ref task queued
[fnd00007 | finding | 90d | 0.99] Prisma DB reconstruction: 4144 rows, 37 VMs, 270 users, $6.74 reconstructed; only gap: userId a458bkg9pb95tgb8 unresolved
[fnd00008 | finding | 90d | 0.80] CT log verification: 400yaahc.gov (cert Dec 16 2024, first on Russian IP Jan 15 2025); dx10.lanl.gov (legacy RSA-1024, not in public CT); *.treasury.gov (cert Oct 4 2024, first on China IP Feb 10 2025) — all CONFIRMS_WITH_CLARIFICATION
[fnd00009 | finding | 90d | 0.92] registry2.anchored.host (172.93.110.120, AS23470/ReliableSite Miami) = Packetware container_registry_secondary. Sources: Shodan monitor+raindrop CSV (explicit "packetware as400495 linked"), Prisma DB (project_id a45bkg9pb95tgb8), k8s/Prometheus SD, ARIN RDAP, crt.sh (Let's Encrypt certs Nov 2024–Apr 2025). H2+H4 support. Gap: ahmn.co identity (current hostname), anchored.host WHOIS, AS400495↔AS23470 BGP peer confirmation.

---
# VOID (expected-but-absent signals — first-class data)

[void0001 | finding | 90d | 0.90] VOID: No ARIN registration found for 45.38.46.0/24 — try RIPE or Hurricane Electric BGP
[void0002 | finding | 90d | 0.85] VOID: userId a458bkg9pb95tgb8 appears in Prisma activity but not in users table — origin unknown
[void0003 | finding | 90d | 0.80] VOID: No Bundesnetzagentur record for +49 VoIP number in .de domain WHOIS contact

---
# Crystallization log
# 2026-03-19: Initial HONEY.md from AGENTS.md migration + investigation findings from cybertemplate sessions
# 2026-03-19 (session 2): +mth00010 (faerie-brief.json pattern) +mth00011 (autotune pre-seed) +fnd00009 (registry2.anchored.host confirmed)
