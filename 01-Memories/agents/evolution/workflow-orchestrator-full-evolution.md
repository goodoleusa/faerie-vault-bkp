---
type: agent-evolution-full
agent: workflow-orchestrator
generated: 2026-03-25
tags: [agent-evolution, performance, investigation-context]
privacy: personal-vault-only
doc_hash: sha256:8ac3c8144a8667b67355ce7cacb5e8fa9c6e508c4ac76ef03423dedd639e18f4
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# Workflow Orchestrator — Full Evolution Story

## Current State
- **Score:** 1.00 (training, 2026-03-19) | **Deployment:** contributing across all multi-sprint sessions
- **Tier:** PRO (structural backbone — coordination, not investigation)
- **Active investigations:** Operation CriticalExposure — phase-gate architecture; AS23470 OSINT pipeline design; multi-sprint orchestration

## Training Timeline

| Date | Score | Delta | Context | Key Learning |
|------|-------|-------|---------|-------------|
| Pre-2026-03-19 | 0.84 | baseline | First formal scoring | Established baseline |
| 2026-03-19 | 1.00 | +0.16 | train-003+006 adversarial-bundle-completeness | Absolute paths, binary checkable done_looks_like, phase gates |

## Investigation Context

### Phase Gate Architecture — Preventing the sprint-20260315-010 Failure
The workflow-orchestrator's formative training context was the sprint-20260315-010 failure analysis. That sprint identified:
- phase_gate_failure: Tier 1 operations ran concurrently with Phase 1 data collection, causing manifest write conflicts
- background_mntd_permission: Background subagents blocked on /mnt/d/ reads
- concurrent_manifest_writes: Multiple agents writing evidence_manifest.json simultaneously

The adversarial training (train-003+006) directly addressed these failure modes. The orchestrator learned to enforce: research/analysis = Phase 1 MUST complete before Phase 2 (curation/writes). This phase gate is now the structural rule that prevents evidence manifest corruption.

### AS23470 OSINT Pipeline (sprint-20260319-001)
The orchestrator designed the multi-track pipeline for AS23470/Packetware attribution:
- Track 1: research-analyst OSINT (WebFetch for WHOIS/BGP/cert data)
- Track 2: data-engineer pipeline (evidence extraction, structured JSON output)
- Track 3: membot handoff architecture (faerie-brief.json redesign)
The pipeline delivered 6/6 deliverables, 1.00 resolution rate, research-analyst training closure at 1.00.

### Handoff Redesign (sprint-20260319-001)
The orchestrator was central to the /handoff command redesign — the "inverse of /faerie." The new architecture: session_stop_hook.py writes last-session-handoff.md; membot produces faerie-brief.json; context-manager bridges to next session. This eliminated the information loss that occurred when sessions ended mid-investigation.

### Multi-Sprint Session Management
The orchestrator appears in every major sprint's agents_used list. For sprint-20260319-001 (score 0.95): workflow-orchestrator was the pipeline architect. For sprint-20260315-010 through sprint-0323, it enforced phase gates and handled the wave-based routing that allowed 5-6 agents to work concurrently without manifest conflicts.

### sprint-20260315-010 Legacy
The orchestrator's phase-gate failures from sprint-010 became the training syllabus. Before train-003, the orchestrator was sending Tier 1 curation tasks before evidence collection was complete. After train-003+006, the rule is absolute: Phase 1 (research, extraction) must produce its output files before Phase 2 (curation, writes) starts. Binary-checkable done_looks_like criteria are the enforcement mechanism.

## What It Learned

### Process Improvements (shareable)
- highest_value must contain absolute file paths (not relative) — a fresh agent must pass the 60-second rule without reading any other field
- prior_run fields must include: sprint ID + numeric score + one-line outcome (3 fields, all required)
- source_files must be individual verified file paths — directories/globs fail adversarial completeness checks
- done_looks_like must be binary-checkable: "file exists at path X" not "analysis complete"
- Phase gate: research/analysis = Phase 1; curation/writes = Phase 2; always gate Phase 2 on Phase 1 completion

### Investigation-Specific Insights (private)
- The sprint-20260315-010 concurrent manifest write failures were the direct motivation for train-003+006. The adversarial training simulated an incomplete bundle being passed to a downstream agent — forcing the orchestrator to make every field self-sufficient for a "blind" agent reading it cold.
- The "highest_value must contain absolute file paths" rule came from a real failure: an orchestrator task bundle specified "see scratch for context" as the highest_value field. The downstream agent spent 8 minutes reading scratch files before finding the relevant data. This lost time in a time-boxed sprint.
- The phase gate rule directly prevented the sprint-0319-001 from having the manifest corruption issues that plagued sprint-0315-010. The orchestrator held back evidence-curator until research-analyst and data-engineer had written their output files.

## Performance Trajectory

The orchestrator's trajectory is clean: one jump from 0.84 to 1.00, then sustained deployment quality. The jump was driven by the adversarial training format — being forced to produce bundles that work without any follow-up questions revealed structural gaps (relative paths, vague done_looks_like, missing prior_run fields) that organic use had not exposed.

The deployment role has evolved: since the main agent now handles session-lead orchestration duties (rules/agents.md), the workflow-orchestrator is spawned specifically for complex workflow design problems, not session coordination. This specialization may be reducing spawn frequency but increasing the quality of each invocation.

## Spawn History

| Sprint | Task | Outcome | Score |
|--------|------|---------|-------|
| sprint-20260319-001 | AS23470 OSINT pipeline design + handoff redesign | 6/6 deliverables | contributing (train-003+006 concurrent) |
| train-003+006 | Adversarial bundle completeness drill | 1.00 on all 4 iterations | 1.00 |
| Multiple sprints | Phase gate enforcement, wave routing | no failures post-010 | deployment |
