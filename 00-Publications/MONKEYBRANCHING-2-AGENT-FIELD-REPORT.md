---
type: field-report
status: candid
session: 2026-05-19 (late session, post-POTEMKIN-v1)
title: "Monkeybranching with Two — Field Report on the 2-Agent Stigmergic Pattern"
audience: skeptical-engineer, future-self, anyone-evaluating-faerie
companion_to: POTEMKIN-FAERIE-FIELD-REPORT.md
---

# Monkeybranching with Two — Field Report

## What this doc is

Companion to `POTEMKIN-FAERIE-FIELD-REPORT.md` (the 5-agent ad-hoc swarm earlier this same session). This is the field report on the **2-agent stigmergic pattern** that ran in the same repo a few hours later, after the lessons from the 5-agent pass were absorbed.

The 5-agent pass produced real throughput (~25 themed indexes) but ate ~40% in dedupe + had one silent-corruption near-miss. This 2-agent pass tried the same pattern with two specific changes:

1. **Charter-first discipline.** Every mission file in `docs/_human-inbox/` was concrete enough that agents didn't have to *pick a theme* — they picked a mission, and the mission named the deliverable. The race vector that bit us last time (workers picking semantically-overlapping but differently-named themes) was structurally removed.
2. **Cap N at 2.** The earlier pass had 5 workers + a clusterer + a broadcaster in flight simultaneously. This pass capped at 2. Less throughput, but less collision surface and less burn rate when the user was watching cost.

This doc captures what happened, what was different from the 5-agent version, and what the data says about the right N for this kind of session.

---

## What landed (the deliverables)

**monkeybrancher-α** (a single agent run, ~12 min wall clock) shipped two missions cleanly:

1. **MESH-cybertemplate-into-faerie-OH-skill** — moved the cybertemplate data pipeline scripts into the faerie OH SDK skill family. Five new scripts in `.openhands/skills/data-ingest/scripts/`:
   - `build_timeline.py` — generic L1→L2 builder, env-var driven, COC-chained
   - `coc_tag_timeline_stages.py` — read-only stage tagger (TC-A)
   - `rename_data_stage_folders.py` — TC-B folder restructure (dry-run default)
   - `refine_timeline_master.py` — TC-C schema normalize + dedupe → L3 master
   - `snapshot_for_public.py` — TC-F publication snapshot with SHA256SUMS
   Plus a 3-line thin wrapper at `cybertemplate/scripts/build-timeline.py`. Plus two new MCP tools (`faerie_data_ingest` + `faerie_timeline_build`) registered in `deploy/mcp-server/server.py`. Plus a `mesh_skill` + `skill_run_summary` COC entry chain.

2. **RECOVER-3-MISSING-AUDITS** — reconstructed three audit artifacts that the earlier 5-agent pass had dropped silently to the SUBAGENT_FILE_PROTOCOL sandbox. Full live-walk verification (25,096 rawdata files counted, 992 data, 3,599 forensics; 43 clusters confirmed). Each marked `recovered_from: agent_report_in_session_transcript_2026-05-19`. Single hash-chained `audit_artifact_recovery` COC entry.

**monkeybrancher-β** (a single agent run, ~10 min wall clock) shipped the commit + push mission:

1. **COMMIT-2026-05-19-SESSION-WORK** — committed faerie2 main to `ec0f6fde` (2,009 files), committed cybertemplate to `3076c124` on the new `astro-consolidation-2026-05-19` branch (57 files), pushed both to origin. Hash-chained `session_commit` COC entry.

Two agents, three missions cleared, two repos pushed. Total wall clock: under 25 minutes elapsed between spawn and "all the work is on origin."

---

## What changed from the 5-agent pass

| Dimension | 5-agent pass | 2-agent pass |
|---|---|---|
| Pre-spawn artifacts | None (workers picked themes from prose prompts) | Six concrete `.mission` files with named deliverables in `_human-inbox/` |
| Theme races | Yes — worker-1 + worker-2 both claimed MEMORY-AND-CRYSTALLIZATION via different string slugs | None — missions have unique slugs; the queue grants atomically |
| Coordination overhead | Workers had to read prior workers' `.claim` files and infer what was uncovered | Workers just `ls _human-inbox/*.mission` and pick |
| Output overlap | ~40% (25 indexes, ~10 effectively duplicate) | ~0% (3 distinct missions, no overlap) |
| Silent corruption near-miss | Yes (Worker-1 vs Worker-2 attribution mismatch on the MEMORY index) | None (each mission writes to disjoint paths) |
| Cost (rough) | ~$3-5 across 6 agents | ~$1.50-2 across 2 agents |
| User intervention rate | High (operator had to redirect, fix collisions, clarify naming) | Low (operator declared scope via mission text once; agents executed) |
| Per-agent depth | Shallow — each worker did 1 theme | Deep — α did two full missions including MCP-tool registration |

**The key invariant:** with charter-first declarations + atomic claim files, parallelism stops trading throughput for cleanup. The 2-agent pass produced fewer artifacts but a higher fraction of them were ship-ready.

---

## Honest observations from running it

**The mission queue is the strongest abstraction.** Both agents read `_human-inbox/*.mission`, picked unclaimed ones, marked them `.done` on completion. The queue is git-trackable, human-droppable, agent-claimable. It survives session boundaries. It made cross-agent coordination invisible. The same `docs/_human-inbox/` will be readable by any future session and immediately tell that session what's queued.

**Charter clarity is the secret ingredient.** The mission files I wrote were paragraph-length with acceptance rituals, anti-goals, and `See also` cross-links. Agents didn't have to interpret intent; they had to execute a written contract. The 5-agent pass tried to compress intent into the spawn prompt and the result was theme drift. Charters externalize the contract into a file the agent reads, the human reads, and a future audit reads — all from the same source.

**The 2-agent cap was the right call given budget anxiety.** The user named cost as a concern. Two agents at higher per-agent depth + zero overlap produces less raw output than five at lower depth + 40% overlap, but the *clean* output rate is comparable. If budget hadn't been a concern, three agents might have been the sweet spot (one more agent could have done the COPY-CRYSTALLIZED-SCRIPTS-TO-FAERIE-OH mission concurrently). Five was too many for this scope.

**Stigmergy scales down beautifully.** The 5-agent version had string-name collision on similar themes. The 2-agent version had zero collisions because the mission filenames were unique by construction. The atomic-create lock on `{mission}.claim` worked exactly as designed; α and β each picked different files in the same milliseconds and never stepped on each other.

**The user can pivot mid-session without disrupting in-flight agents.** Mid-pass, the user said "FOLLOW JESS'S COMMITS" / "I'M DATA NOT UI." That reversed the orchestrator's planned next action (the Astro port). It did NOT affect α or β, who were already mid-mission on MESH and COMMIT. Agents that read their mission file at spawn time aren't disturbed by user pivots after spawn. That decoupling is exactly the property that makes the pattern survive a real session where directives change every five minutes.

**The dropped artifacts from the earlier pass were recoverable in this pass.** Three audit files lost to the SUBAGENT_FILE_PROTOCOL sandbox got fully reconstructed by α from the conversation transcript + live-walking the filesystem. The 5-agent pass produced the *substance*; the 2-agent pass produced the *durable artifact*. The two passes together cover what a single pass at either size would not have.

**The mesh landed cleanly.** This is the most architecturally significant thing: cybertemplate's data pipeline is no longer cybertemplate-specific. The five scripts live at `faerie2/.openhands/skills/data-ingest/scripts/`, they're env-var driven, they're invocable via MCP, and cybertemplate's working tree has a 3-line shim that points at them. Any future investigation using the same skill family inherits the work. That's the difference between a one-off bash pipeline and an OH-SDK-native skill.

---

## What was harder than expected

1. **The astro-consolidation branch had to be flat-named.** `git refs/heads/dev` exists as a non-directory ref, so `dev/astro-consolidation-2026-05-19` couldn't be created (namespace collision). The branch ended up as `astro-consolidation-2026-05-19`. Cosmetic but worth recording — anyone trying to recreate the slash-prefixed naming convention will hit the same wall.

2. **The Astro build kept failing on bare `<script src="assets/...">` tags from Jess's legacy HTML.** Each port attempt hit it. The fix is `is:inline` or assets-mirror-to-public, both of which are mechanical but require knowing the trick. This isn't a stigmergy problem; it's an Astro-meets-legacy-HTML problem. Documented in the build-failure forensic doc.

3. **`forensics/` discipline took three corrections to settle.** First I wrote audit artifacts at `forensics/` root. User correction: belongs in canonical locations. I moved them to `forensics/artifacts/2026-05-19/` (type-first). User correction again: canonical is **date-first** with type-subdir. Moved them to `forensics/2026-05-19/artifacts/`. User correction once more: BOTH views — `forensics/2026-05-19/artifacts/` (date-first canonical) plus `forensics/artifacts/2026-05-19/` (type-aggregate symlinks). Three iterations on layout because the orchestrator (me) didn't read the existing ORGANIZATION.md carefully enough. The agents downstream had to follow whatever layout was current at their spawn time, which luckily was consistent within each agent's run.

4. **Audit-agent-C waited on a Monitor instead of writing the inbound-link map.** Hit a UX edge in the agent runtime — it tried to monitor for an event and didn't realize that wasn't going to terminate. Its output substrate (the inbound-link map) had to be recovered from the main session afterward by direct grep. Not a stigmergy failure; an agent-runtime failure that we'd want a watchdog for.

---

## What I'd carry into the next session

1. **Cap N at 2-3** for cost-sensitive sessions. Charter-first eliminates the throughput penalty.
2. **Mission files are the persistent contract.** Drop them eagerly. Future sessions inherit them. The queue is the API between sessions.
3. **Snapshot before consolidate.** TC-PRE pattern (snapshot every retired thing to `_archive/{date}-pre-consolidation/` with SHA256SUMS + COC entry) is what makes "comprehensive not reductive" enforceable instead of aspirational.
4. **Don't try to fold mid-session user pivots into in-flight agents.** Let them finish. Reflect the pivot in the next mission's text.
5. **Mesh shipped data pipelines into the OH skill family** is the architectural unlock. The cybertemplate → faerie-skill mesh is the model for every future investigation: data work doesn't live in a single repo; it lives in the skill that any repo can invoke.

---

## What the user paid for vs what they got

Approx $1.50-$2.00 in inference (rough; depends on Anthropic billing). What landed:

- 5 production-ready data-pipeline scripts in faerie's OH skill
- 2 new MCP tools surfacing the pipeline to chat / dashboard / coworker workflows
- 3 forensic audit artifacts recovered
- 1 large `session_commit` push across two repos
- Hash-chained COC trail with `mesh_skill`, `skill_run_summary`, `audit_artifact_recovery`, `session_commit` entries
- An updated `forensics/ORGANIZATION.md` with the dual-view (date-first + type-aggregate) layout
- A `CONFIG-MAP.md` orientation doc
- The `MONKEYBRANCHING-2-AGENT-FIELD-REPORT.md` (this doc)

Per-agent throughput was lower than the 5-agent pass; per-dollar artifact quality was higher.

---

## The pattern in one sentence

> Charter-first + atomic claim files + cap N at 2-3 + the mission queue as the persistent API between sessions = stigmergic coordination that doesn't trade throughput for cleanup.

---

*This report is a companion to `POTEMKIN-FAERIE-FIELD-REPORT.md` (5-agent ad-hoc version) and `ORCHESTRATOR-OBSERVATIONS.md` (first-person orchestrator notes from the 5-agent pass). The three together form the field-evidence package for "stigmergic coordination of Claude agents on real engineering work" at three different N values.*
