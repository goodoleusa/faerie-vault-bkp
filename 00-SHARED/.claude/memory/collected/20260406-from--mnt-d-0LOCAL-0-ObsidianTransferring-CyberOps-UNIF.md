<!-- FORENSIC COLLECTION RECORD -->
<!-- source_path: /mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md -->
<!-- source_sha256: ffe331134cfa295acb9aceb8bf6aa3b784632d726920e8332cdbfe124beaa349 -->
<!-- source_size_bytes: 8921 -->
<!-- collected_at: 2026-04-06T07:00:39Z -->
<!-- collector: emergency_handoff.py -->
<!-- VERIFY: sha256sum /mnt/c/Users/amand/.claude/projects/-mnt-d-0LOCAL-0-ObsidianTransferring-CyberOps-UNIFIED/memory/MEMORY.md should match source_sha256 above -->
<!-- Content below is UNALTERED from source. -->

# CyberOps-UNIFIED Vault Memory

## First Principles (read before every action)

**Equilibrium**: Every output must balance an input. Context consumed crystallizes into knowledge. Budgets enforce this — never add to an over-budget file. If a file is over, crystallize first. The system is conservative: energy in = energy out.

**Flow**: Work flows like water — it doesn't pool. Scratch → NECTAR → HONEY. Agents produce → handoff collects → crystallize distills → faerie launches again. If something stops flowing, the system stagnates. Move things through, don't let them accumulate.

**Crystallization**: Not compression. Integration. The new fact is understood against everything already known. Duplicates merge. Contradictions resolve. Cross-references form. Each line carries more meaning. Shorter but deeper. This applies to EVERYTHING — manifests, memories, design docs, dashboards. If you're just appending, you're not crystallizing.

## Session 2026-03-27: Architecture Visualization + Memory Cleanup

### Done
- Rules crystallized (504→274 lines, under 300 budget) with human-readable vault versions
- 16 MermaidJS diagrams in System-Architecture.md (equilibrium color palette, mobile-friendly)
- 31 pseudosystem component notes with excalibrain metadata
- 18 design narrative docs collected with SHA256 IP provenance manifest + COC
- Session manifests consolidated (87+12 per-minute → 3 crystallized daily narratives)
- design-hash-track.py for lightweight edit tracking
- DataviewJS TOC→Mermaid template for design sessions

### Architecture Decisions
- `.claude/memory/` should be HONEY system only (HONEY + NECTAR + REVIEW-INBOX + scratch)
- forensics/, investigations/, training/ belong at their own `~/.claude/` level
- Session manifests: one crystallized daily .md, JSONs archived
- Two-tier docs: terse system files (tokens) + expanded vault versions (humans)
- Design IP: hash at creation, track edits via design-hash-track.py, COC in design-coc.jsonl

### Liftoff Paradox (crystallized 2026-03-27)
The best thinking happens at context edges — deepest depth, richest connections, most compaction risk. Discipline: **write the jewel before chasing the next one.** Chain-of-consciousness doc `13-CHAIN-OF-CONSCIOUSNESS-2026-03-27.md` was reconstructed after compaction loss — proof of the principle and its violation.

### Open Threads
1. Pseudosystem A/B parallel versions (prev vs next for comparison testing)
2. HONEY flow dashboard (central viz of all HONEY-tier files global→local)
3. `.claude/memory/` architecture refactor (move forensics/investigations/training out)
4. Investigation finish line dashboards (work-units-to-completion)
5. REVIEW-INBOX crystallization (427L, needs siphoning)
6. **Queue COC architecture** — done tasks are forensic evidence, never delete. COC-log all transitions, atomize outputs, enrich knowledge bases (NECTAR, AGENTS.md, agent cards, vault). See project_queue_coc.md.
7. Dashboard sweep (agent running — uncentralized dashboards/templates)
8. Manifest hook frequency fix (should fire once per session, not per tool call)

### Prior Session Work
- emergency_handoff.py (1.5 sec, circuit breaker pattern)
- /handoff and /faerie Step Zero protocol
- Three-layer separation, atomized briefs, deferred hashing

## Memory Index

- [feedback_fast_handoff.md](feedback_fast_handoff.md) — /handoff delegates to membot, not read files in low-context parent
- [feedback_handoff_is_workday_end.md](feedback_handoff_is_workday_end.md) — /handoff = end of workday, not just session
- [feedback_rounds_not_percentage.md](feedback_rounds_not_percentage.md) — Context budget = synthesis rounds, not raw %
- [feedback_honey_dev_mode.md](feedback_honey_dev_mode.md) — HONEY versions are folders with all 4 levels
- [feedback_honey_living_document.md](feedback_honey_living_document.md) — HONEY deepens through crystallization
- [feedback_websearch_claude_docs.md](feedback_websearch_claude_docs.md) — Always websearch Claude CLI docs
- [feedback_surfacing_timing.md](feedback_surfacing_timing.md) — Time agent launches so returns cluster in productive windows
- [feedback_evergreen_vs_chain.md](feedback_evergreen_vs_chain.md) — Classify jobs: evergreen (anytime) vs chain (sequential deps)
- [feedback_self_correcting_algorithm.md](feedback_self_correcting_algorithm.md) — Algorithm self-corrects from metrics via closed loop
- [project_queue_coc.md](project_queue_coc.md) — Done tasks are forensic evidence, never delete
- [project_faerie2_standalone.md](project_faerie2_standalone.md) — faerie2 standalone system at /mnt/d/0LOCAL/gitrepos/faerie2/
- [project_three_inbox_architecture.md](project_three_inbox_architecture.md) — Three inboxes: REVIEW-INBOX → Human-Inbox/ → 00-Inbox/
- [project_session_metrics_v3.md](project_session_metrics_v3.md) — 7 hash-chained KPIs in session_metrics.py v3
- [feedback_memory_permission.md](feedback_memory_permission.md) — Memory writes have standing permission, never ask
- [feedback_benchmark_calibration.md](feedback_benchmark_calibration.md) — New benchmarks need 3-5 runs to calibrate; 1.0 on first run = benchmark too easy
- [project_03agents_blind_zone.md](project_03agents_blind_zone.md) — 03-Agents/ is agent-blind; annotations must route back to 00-SHARED/Dashboards/
- [project_honey_shareable_vision.md](project_honey_shareable_vision.md) — HONEY should be artistic/shareable; technical jargon moves to rules/
- [project_product_vision_tiers.md](project_product_vision_tiers.md) — Free/trial/paid tiers, data sovereignty, accidental inventions
- [project_crystallization_multi_mind.md](project_crystallization_multi_mind.md) — Crystallization = multi-mind forging (agents + human + training + time)
- [feedback_honey_sacred.md](feedback_honey_sacred.md) — HONEY is sacred; entries earn place through time-tested validity
- [feedback_narrative_numbering.md](feedback_narrative_numbering.md) — Design narratives use sequence numbers (13-, 14-) not dates
- [feedback_ann_copy_files.md](feedback_ann_copy_files.md) — Human annotations written to .ann copy files, not inline
- [project_streaming_provenance.md](project_streaming_provenance.md) — Streaming agent outputs + vault provenance chain (stream → doc_hash → ann_hash)
- [project_honey_export_design.md](project_honey_export_design.md) — Two faces of HONEY: internal (gauntlet) vs export (collaboration brief for sharing)
- [feedback_handoff_membot_first.md](feedback_handoff_membot_first.md) — Membot spawns FIRST in /handoff; 3 steps not 9
- [feedback_context_economy.md](feedback_context_economy.md) — Context is investment economy (multipliers, debt, reserve), not line-count accounting
- [project_queue_clustering_design.md](project_queue_clustering_design.md) — Queue clustering, dynamic /run loop, /faerie natural language args, dashboard as main interface
- [project_piston_model.md](project_piston_model.md) — Fast/medium/deep agent piston rhythm for queue throughput
- [project_product_vision.md](project_product_vision.md) — Platform product: opus-quality on sonnet/haiku, overnight batch synthesis
- [feedback_read_before_write.md](feedback_read_before_write.md) — Read-before-write is platform constraint; use offset+limit to minimize re-read cost
- [feedback_dev_mode_budgets.md](feedback_dev_mode_budgets.md) — Crystallization is for memory files, not command files being iterated
- [feedback_modular_secret_sauce.md](feedback_modular_secret_sauce.md) — Modular architecture: remove proprietary modules before sharing repo for interviews
- [project_windows_wsl_moat.md](project_windows_wsl_moat.md) — Claude Desktop broken on Windows+WSL; faerie bridges 72% of desktop market
- [feedback_seamless_autocompact.md](feedback_seamless_autocompact.md) — Auto-compact invisible; never require /faerie mid-session; only speak on actual news
- [feedback_citation_style.md](feedback_citation_style.md) — Vancouver style, arXiv URLs, fact-checked links, numbered in-text refs
- [feedback_agent_dispatch.md](feedback_agent_dispatch.md) — Specialist before general-purpose; claude-code-guide for CLI meta-questions; cards at ~/.claude/agents/
- [feedback_no_compress_crystallize.md](feedback_no_compress_crystallize.md) — Never "compress" during crystallization; integration = denser+richer, never lossy
- [project_product_model_routing.md](project_product_model_routing.md) — W1=Haiku/W2=Sonnet/W3=Sonnet-high-effort; Opus never default; profit = cheap models performing like expensive
- [feedback_crystallization_choice.md](feedback_crystallization_choice.md) — Crystallization is human choice; never queue it; budget = price signal not alarm; evolutionary forces govern timing
- [project_overnight_batch.md](project_overnight_batch.md) — Batch API for overnight W3 synthesis; 50% cost; system improves while user sleeps; morning faerie reads results