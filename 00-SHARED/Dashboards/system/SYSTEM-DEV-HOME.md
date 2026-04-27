---
type: system-dashboard
stage: system
status: final
created: 2026-03-29
updated: 2026-03-29
tags: [system, faerie, dev, dashboard, home]
entry_point: true
---

> [!nav]
> **System Dev Home** · [[System-Architecture|Architecture]] · [[00-SHARED/Hive/_index|Hive →]] · [[00-SHARED/Queue/|Queue →]]

# Faerie System Dev Home

Single entry point for faerie system development. Eval scores, queue depth, tools, design docs, blueprints.

---

## 1 · Live Status

```dataviewjs
// ── Eval score (from eval-mirror.md, written by eval_harness.py) ──
const evalMirror = app.vault.getAbstractFileByPath(
  "00-SHARED/Dashboards/system/eval-mirror.md"
);
let evalScore = "⚠️ eval-mirror.md not found — run eval_harness.py";
let evalDimScores = null;
if (evalMirror) {
  const fm = app.metadataCache.getFileCache(evalMirror)?.frontmatter;
  if (fm) {
    evalScore = fm["composite_score"] != null
      ? `**${fm["composite_score"]} / 10** (updated ${fm["updated"] ?? "unknown"})`
      : "⚠️ composite_score not set in eval-mirror.md";
    evalDimScores = fm["dim_scores"] ?? null;
  }
}

// ── HONEY budget (from memory-status.md, written by membot) ──
const memStatus = app.vault.getAbstractFileByPath(
  "00-SHARED/Dashboards/system/memory-status.md"
);
let honeyLine = "⚠️ memory-status.md not found — run membot";
if (memStatus) {
  const fm = app.metadataCache.getFileCache(memStatus)?.frontmatter;
  if (fm) {
    const used = fm["honey_tokens"] ?? null;
    const max = 5000;
    if (used != null) {
      const pct = Math.round((used / max) * 100);
      const filled = Math.round(pct / 10);
      const bar = "█".repeat(filled) + "░".repeat(10 - filled);
      const flag = pct >= 90 ? " 🔴 CRYSTALLIZE" : pct >= 70 ? " 🟡 watch" : " 🟢";
      honeyLine = `\`${bar}\` ${used}/${max} tok (${pct}%)${flag}`;
    } else {
      honeyLine = "⚠️ honey_tokens not set in memory-status.md";
    }
  }
}

// ── Queue depth ──
const queueFolder = app.vault.getAbstractFileByPath("00-SHARED/Queue");
let queueDepth = "?";
if (queueFolder && queueFolder.children) {
  queueDepth = queueFolder.children.filter(f => f.extension === "md").length;
}

// ── Render pulse table ──
dv.header(3, "System Pulse");
dv.table(["Metric", "Value", "Source"],
  [
    ["Eval Score",   evalScore,   "`eval-mirror.md` ← eval_harness.py"],
    ["HONEY Budget", honeyLine,   "`memory-status.md` ← membot"],
    ["Queue Depth",  `${queueDepth} tasks → [[00-SHARED/Queue/|Open Queue]]`, "Queue/ folder count"],
  ]
);

// ── Per-dimension scores if available ──
if (evalDimScores) {
  dv.header(4, "Dimension Breakdown");
  dv.table(["Dim", "Score"],
    Object.entries(evalDimScores).map(([k, v]) => [k, v])
  );
}
```

> Generate eval mirror: `python3 ~/.claude/scripts/eval_harness.py --report`
> Generate memory status: spawn membot or `python3 ~/.claude/scripts/debloat.py --scan`

---

## 2 · Eval Dimensions

| Dim | Name | Score | Target | Key Metric |
|-----|------|-------|--------|------------|
| A | Throughput | ? | 8 tasks/session | tasks/session |
| B | Memory | ? | HONEY hit ≥40% | honey_hit_rate |
| C | Resilience | ? | manifest_cov ≥90% | manifest_coverage |
| D | Quality | ? | depth ≥7.0 | finding_depth |
| E | Piston | ? | waves_pre ≥1 | waves_before_response |
| F | Model Routing | ? | haiku_w1 ≥80% | haiku_w1_rate |

> Update scores: `python3 ~/.claude/scripts/eval_harness.py --report`
> Model comparison: `python3 ~/.claude/scripts/model_compare.py --report`
> Live scores live in `~/.claude/hooks/state/system-eval.json` — mirrored to `eval-mirror.md` each run.

---

## 3 · Dev Tools Index

### Evaluation

| Script | Purpose | Command |
|--------|---------|---------|
| `eval_harness.py` | 6-dimension system eval, hash-chained; runs at every Stop | `python3 ~/.claude/scripts/eval_harness.py --report` |
| `model_compare.py` | Compare system-haiku vs vanilla-sonnet/opus (4 arms × 3 tasks) | `python3 ~/.claude/scripts/model_compare.py --report` |
| `session_metrics.py` | 7 KPI hash chain; runs at every Stop | `python3 ~/.claude/scripts/session_metrics.py` |

### Memory

| Script | Purpose | Command |
|--------|---------|---------|
| `stamp_doc_hash.py` | Batch SHA256-stamp all vault frontmatter | `python3 ~/.claude/scripts/stamp_doc_hash.py --vault ...` |
| `debloat.py` | Check all file token budgets against limits | `python3 ~/.claude/scripts/debloat.py --scan` |
| `crystallize.py` | Pressure-based HONEY crystallization (gauntlet-gated) | Use via `/crystallize` — not directly |

### Session

| Script | Purpose | Command |
|--------|---------|---------|
| `surfacing_scheduler.py piston` | Wave planning for current session | `python3 ~/.claude/scripts/surfacing_scheduler.py piston` |
| `surfacing_scheduler.py calibrate` | Self-calibration from session metrics | `python3 ~/.claude/scripts/surfacing_scheduler.py calibrate` |
| `emergency_handoff.py` | Emergency context roundup (circuit-breaker, 1.5 s) | `python3 ~/.claude/scripts/emergency_handoff.py` |

### Pipeline (data-analysis-engine)

| Script | Purpose | Command |
|--------|---------|---------|
| `lib/trail_reader.py` | Read pipeline run trail by run_id | `python3 lib/trail_reader.py {run_id} --list` |
| `lib/stage_wrapper.py` | `stage_run()` context manager for pipeline stages | Import in pipeline scripts |
| `scripts/2b-hash-guardian.py` | Hash verification for pipeline artifacts | `python3 scripts/2b-hash-guardian.py` |

---

## 4 · Design Narratives (Hive)

### Numbered Design Docs

| # | Doc | Description |
|---|-----|-------------|
| 00 | [[00-SHARED/Hive/00-DESIGN-NARRATIVE-2026-03-22\|00 · Design Narrative 2026-03-22]] | Original vault architecture session |
| 00 | [[00-SHARED/Hive/00-META\|00 · Meta]] | Hive meta index and routing |
| 00 | [[00-SHARED/Hive/00-OVERVIEW\|00 · Overview]] | System overview |
| 00 | [[00-SHARED/Hive/00-VAULT-STATUS\|00 · Vault Status]] | Current vault health snapshot |
| 01 | [[00-SHARED/Hive/01-ARCHITECTURE\|01 · Architecture]] | Core architecture decisions |
| 01 | [[00-SHARED/Hive/01-LEARNINS\|01 · Learnins]] | Early lessons log |
| 01 | [[00-SHARED/Hive/01-MEMORY-EDIT\|01 · Memory Edit]] | Memory edit protocol |
| 02 | [[00-SHARED/Hive/02-QUICKADD-SETUP\|02 · QuickAdd Setup]] | Obsidian QuickAdd configuration |
| 03 | [[00-SHARED/Hive/03-AGENT-HANDOFF-EXPLAINER\|03 · Agent Handoff Explainer]] | How agent handoff works end-to-end |
| 04 | [[00-SHARED/Hive/04-QUICKADD-GLOBAL-VARS-HANDOFF\|04 · QuickAdd Global Vars Handoff]] | Global variable handoff via QuickAdd |
| 05 | [[00-SHARED/Hive/05-AGENT-INSIGHTS-DASHBOARD-AND-SYNC-BACK\|05 · Agent Insights Dashboard]] | Insights dashboard and sync-back design |
| 06 | [[00-SHARED/Hive/06-TEST-TASK-WALKTHROUGH\|06 · Test Task Walkthrough]] | End-to-end task test walkthrough |
| 08 | [[00-SHARED/Hive/08-AGENT-ADAPTIVE-CONTEXT-AND-EVOLVING-PROMPT\|08 · Adaptive Context]] | Evolving prompt / adaptive context design |
| 09 | [[00-SHARED/Hive/09-HUMAN-PROMOTES-AI-EXECUTES\|09 · Human Promotes AI Executes]] | Two-stage finding promotion model |
| 10 | [[00-SHARED/Hive/10-TASK-LINEAGE-AND-HANDBACK\|10 · Task Lineage and Handback]] | Task lineage, COC handback design |
| 11 | [[00-SHARED/Hive/11-FAERIE-IMPACT-AB\|11 · Faerie Impact A/B]] | A/B impact measurement methodology |
| 12 | [[00-SHARED/Hive/12-ASYNC-HUMAN-AGENT-BRIDGE\|12 · Async Human-Agent Bridge]] | Async bridge design |
| 13 | [[00-SHARED/Hive/13-CHAIN-OF-CONSCIOUSNESS-2026-03-27\|13 · Chain of Consciousness]] | Liftoff paradox — reconstructed after compaction loss |
| 13 | [[00-SHARED/Hive/13-MEMORY-FLOW-ARCHITECTURE\|13 · Memory Flow Architecture]] | HONEY/NECTAR/scratch flow design |
| 14 | [[00-SHARED/Hive/14-BUDDHIST-PHILOSOPHY-AND-SYSTEM-DESIGN\|14 · Buddhist Philosophy + System Design]] | Impermanence, equilibrium, design philosophy |
| 14 | [[00-SHARED/Hive/14-SCRATCH-DUMP-PROCESSING-STATE\|14 · Scratch Dump Processing State]] | Scratch dump and processing state |
| 15 | [[00-SHARED/Hive/15-MODULAR-SECRET-SAUCE\|15 · Modular Secret Sauce]] | Modular arch — what ships vs stays private |
| 16 | [[00-SHARED/Hive/16-FAERIE-STARTUP-BLOAT-ARC\|16 · Faerie Startup Bloat Arc]] | How faerie went from 61K → 11K startup tokens |

### Named Design Docs

| Doc | Description |
|-----|-------------|
| [[00-SHARED/Hive/Trail-Protocol\|Trail Protocol]] | Stigmergy manifest system — pheromone trails for agents |
| [[00-SHARED/Hive/DAE-Scripts-Architecture\|DAE Scripts Architecture]] | Tier classification, free/paid boundary for pipeline |
| [[00-SHARED/Hive/Eval-Framework\|Eval Framework]] | defense_score, failure-to-gold, benchmark methodology |
| [[00-SHARED/Hive/PISTON-MODEL-DESIGN\|Piston Model]] | Wave architecture — fast/medium/deep agent rhythm |
| [[00-SHARED/Hive/System-Architecture\|System Architecture]] | Full system overview (16 MermaidJS diagrams) |
| [[00-SHARED/Hive/PIPELINE-DESIGN\|Pipeline Design]] | Data analysis engine pipeline architecture |
| [[00-SHARED/Hive/BRIEFGEN-DESIGN\|Briefgen Design]] | Brief generation system design |
| [[00-SHARED/Hive/VAULT-SCHEMA\|Vault Schema]] | Vault folder ownership and routing schema |

---

## 5 · Session Blueprints

> Quick-start templates for common dev activities. Red links = blueprint not yet built.

| Blueprint | Purpose |
|-----------|---------|
| [[00-SHARED/Dashboards/session-briefs/Session-Review\|Session-Review]] | Post-session retrospective — what worked, what didn't, queue updates |
| [[00-SHARED/Dashboards/session-briefs/Feature-Eval\|Feature-Eval]] | defense_score + failure-to-gold evaluation before/after a feature |
| [[00-SHARED/Dashboards/session-briefs/Feature-Proposal\|Feature-Proposal]] | Pre-build multi-benefit check — does this earn its place? |
| [[00-SHARED/Dashboards/session-briefs/Problem-Log\|Problem-Log]] | Capture a failure: what broke, why, retry context |
| [[00-SHARED/Dashboards/session-briefs/Design-Insight\|Design-Insight]] | Capture a design insight — timestamp, source, implications |
| [[00-SHARED/Dashboards/session-briefs/Crystallization-Candidate\|Crystallization-Candidate]] | HONEY gauntlet check — recurrence, impact, universality |

---

## 6 · Key State Files

| File | Purpose | Updated |
|------|---------|---------|
| `~/.claude/hooks/state/system-eval.json` | Eval composite score + 6-dim chain | Every session Stop |
| `~/.claude/hooks/state/faerie-brief.json` | Cold-start fuel — prior session context bundle | Every `/faerie` |
| `~/.claude/hooks/state/sprint-queue.json` | Task queue — claimed, queued, done states | Every `/run`, `/faerie` |
| `~/.claude/hooks/state/surfacing-calibration.json` | Wave timing self-calibration data | Every `surfacing_scheduler.py calibrate` |
| `~/.claude/hooks/state/model-compare-results.jsonl` | Model comparison history (hash-chained) | Every `model_compare.py` run |
| `~/.claude/memory/HONEY.md` | Crystallized prefs/methods — budget ≤5K tokens | Only via `/crystallize` (pressure-gated) |
| `~/.claude/memory/NECTAR.md` | Validated findings — unbounded, append-only | Every `/handoff` |

> Vault-side mirrors: `eval-mirror.md` and `memory-status.md` in this folder are written by scripts so Obsidian DataviewJS can read them without hitting CLI paths directly.

---

## 7 · Quick Commands

```bash
# ── Eval ──────────────────────────────────────────────
python3 ~/.claude/scripts/eval_harness.py --report
python3 ~/.claude/scripts/model_compare.py --report
python3 ~/.claude/scripts/session_metrics.py

# ── Memory health ─────────────────────────────────────
python3 ~/.claude/scripts/debloat.py --scan

# ── Queue inspection ──────────────────────────────────
cat ~/.claude/hooks/state/sprint-queue.json | python3 -m json.tool | head -40

# ── Piston / wave state ───────────────────────────────
python3 ~/.claude/scripts/surfacing_scheduler.py piston
python3 ~/.claude/scripts/surfacing_scheduler.py calibrate

# ── Emergency ─────────────────────────────────────────
python3 ~/.claude/scripts/emergency_handoff.py
```

---

*Written by fullstack-developer agent 2026-03-29. Humans annotate via `SYSTEM-DEV-HOME.ann.md` sibling — do not edit this file directly.*
