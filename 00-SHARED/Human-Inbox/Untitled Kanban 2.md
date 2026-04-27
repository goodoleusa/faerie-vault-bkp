---
status: In Progress
kanban-plugin: board
doc_hash: sha256:8003254e1575de0226ce5a42be1975264e92b07ea5ff484b66361ea87e37545f
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---


## HIGH

- [ ] Expand /faerie Turn-1 roundup: read manifest, REVIEW-INBOX, gates, active plan #faerie `task-20260325-235934-d743`
- [ ] Create memory_gate.py + memory-lite.md — FAERIE_TIER runtime detection #faerie `task-20260326-wire-008`
- [ ] HONEY contamination cleanup: remove fnd00013/14/15 case data from global HONEY.md #cybertemplate `task-20260328-020716-648b`
- [ ] Wire vault_annotation_sync.py into /faerie Turn-1 or UserPromptSubmit hook #faerie `task-20260328-031340-4700`
- [ ] Correct wrong NECTAR entry: C:/ paths rule from March 18 #faerie `task-20260328-033750-3164`
- [ ] HONEY restructure: move env/system entries to rules/, make HONEY artistic/shareable #faerie `task-20260328-145630-c411`
- [ ] Build /collab-export: HONEY-based collaboration handoff protocol #faerie `task-20260328-145632-0202`
- [ ] Vault-editable queue: write sprint-queue to 00-SHARED in human-editable format #faerie `task-20260328-145709-5f58`
- [ ] Streaming handoff: write faerie-brief.json on PreCompact trigger #faerie `task-20260328-152655-4c9a`
- [ ] memory_bridge vault mirror: write BRIDGE-{date}.md to Droplets/ #faerie `task-20260328-152655-3ddd`

## MED

- [ ] [COC-GAP2] hash_guardian sweep of scripts/audit_results/ post-RUN006b files #criticalexposure `task-20260323-014253-a161`
- [ ] Port scan 20.141.83.185:25,443,587 — confirm Mail-in-a-Box still running #criticalexposure `task-20260323-140250-2cea`
- [ ] yszfa.cn live DNS: dig + VirusTotal historical DNS #criticalexposure `task-20260323-140257-b985`
- [ ] Research 'fashfed-serverless' codename from Monk AI voice-ai codebase #criticalexposure `task-20260323-140417-6094`
- [ ] Code review: map all scripts/hooks/commands/skills, verify no overlap #faerie `task-20260325-235934-2025`
- [ ] Mermaid diagrams: provenance chain, three-store architecture, annotation flow #data-analysis-engine `task-20260325-235934-cccd`
- [ ] Transition CLI-GIT to faerie2 as canonical dev repo #faerie `task-20260325-235934-6855`
- [ ] Create /metrics command + metrics_renderer.py #faerie `task-20260326-wire-007`
- [ ] AGENTS.md crystallization: 164/150 lines, over budget #cybertemplate `task-20260328-020725-7db3`
- [ ] Vault frontmatter normalization: push to 95%+ coverage #cybertemplate `task-20260328-020725-2e73`
- [ ] Template consolidation: create central index for 3 template locations #cybertemplate `task-20260328-020725-1e1c`
- [ ] DAE vault self-contained template sync #cybertemplate `task-20260328-020725-f6e0`
- [ ] Write onboarding doc for new investigators joining mid-investigation `task-20260328-150348-839f`
- [ ] Mirror HONEY restructure to data-analysis-engine, faerie2, global claude #faerie `task-20260328-152655-6f55`
- [ ] REVIEW-INBOX siphoning: 89 HIGH flags need triage #faerie `task-20260328-152656-9b73`

## LOW

- [ ] Continuous self-improvement: audit TRAINING bullet quality, compress AGENTS.md `sprint-20260315-018`
- [ ] faerie2 .claude/ legacy cleanup: remove hardcoded-path copies #faerie `task-20260328-031342-05b2`

## DONE

- [x] Built memory_bridge.py — programmatic routing from Claude auto-memory
- [x] Built scratch_collector.py — periodic auto-save with PreCompact hooks
- [x] Built queue_vault_sync.py — bidirectional sprint queue sync
- [x] HONEY restructure — moved env entries to rules/environment.md
- [x] Reconnected statusline hook
- [x] Created 13-MEMORY-FLOW-ARCHITECTURE.md narrative doc
- [x] Created 14-SCRATCH-DUMP-PROCESSING-STATE.md narrative doc
- [x] Renamed condensation/ to Droplets/ system-wide
- [x] Updated WRITE-ROUTING.md with ownership model
- [x] Captured product vision (free/trial/paid tiers)
- [x] Captured adversarial crystallization + multi-mind forging design

> [!chain]- Chain: #8 · agent-lint · 2026-03-28T15:59Z
> chain: `criticalexposure` · prev: `sha256:c4d987ad4…` · this: `sha256:ea139e512…`
> Verify: `python3 ~/.claude/scripts/note_sign.py verify <this-file>`



%% kanban:settings
```
{"kanban-plugin":"board","show-checkboxes":true}
```
%%