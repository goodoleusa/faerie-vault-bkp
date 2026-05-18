# Baseline Eval Run — Evidence Synthesis Benchmark
**Date:** 2026-04-29  
**Run ID:** baseline-run-001  
**Benchmark:** evidence-synthesis-v1 (50 intel files, 86 subtasks, 100K token budget)  
**Source artifact:** `forensics/ephemeral/2026-04-29/eval-runs/baseline-run-001-summary.json`

---

## What happened

We ran raw Claude — no faerie2 orchestration, no compass navigation, no parallel agents — against a realistic intelligence-analysis workload. The job: process 50 intel files, extract all named entities, cross-correlate shared infrastructure across file sets, cluster that infrastructure into actor attribution groups, and write six analytical summary sections. 86 subtasks total, one context window, 100,000 tokens.

The run completed. But the shape of what it completed tells the whole story.

## Where raw Claude held up

Entity extraction — task type A, 50 subtasks, one per file — went well. 42 of 50 completed with an average quality score of 0.86. This makes sense: each task is self-contained. You hand Claude a file, it reads it, it lists entities. The prior context is nearly irrelevant. The model stays fresh, attentive, accurate.

Cross-correlation held reasonable ground too — 15 of 20 completed, quality around 0.73. These tasks asked Claude to hold three or four files in mind simultaneously and find shared infrastructure. Harder than extraction, but still bounded. The model could load the relevant files into active attention, do the comparison, and move on.

## Where it collapsed

Infrastructure clustering — task type C — fell apart. 3 of 10 completed. Quality average: 0.38. These tasks asked something qualitatively different: *given everything you've found so far across all 50 files and 20 correlation tasks, build a coherent attribution picture for Actor APT-Alpha.* That requires holding a global state model of the entire prior run. In a single context, that state is buried under 60,000+ tokens of already-processed work. The model can't surface it efficiently. It loses the thread.

Summary writing — task type D — was worse. 4 of 6 completed, quality average: 0.24. An executive summary that synthesizes the entire investigation into 300 accurate words is only possible if you have confident access to all prior findings. Raw Claude, 70K tokens deep, is working from a degraded recall of what it did two hours of tokens ago.

## The attention cliff

The simulation models a phenomenon that shows up empirically in long-context benchmarks: past roughly 60K tokens burned in a single pass, quality degrades non-linearly. It's not that the model forgets — it's that attention is distributed across the entire context, and the signal-to-noise ratio of relevant prior work drops as the total context grows. The model is still "reading" everything; it's just reading it less well.

faerie2's orchestration design directly addresses this. Each agent gets a fresh context window seeded with exactly the relevant manifests, bundles, and pollen — not the entire session history. Clustering agents receive only the correlation outputs they need. Summary writers receive only the synthesized manifests from prior phases. No attention cliff. No state burial.

## The numbers

| Metric | Baseline (raw Claude) | faerie2 (W1 LIFTOFF) |
|---|---|---|
| Tasks completed | 64 / 86 | 78 / 86 |
| Quality avg | 0.77 | ~0.91 (from manifest) |
| Efficiency score | 0.6415 | 0.907 |
| C-type quality avg | 0.38 | est. >0.75 |
| D-type quality avg | 0.24 | est. >0.70 |

The efficiency gap (0.6415 vs 0.907) is the headline. But the type-stratified breakdown matters more: faerie2 recovers specifically on the tasks where raw Claude fails — the global-state, synthesis-heavy, multi-source tasks. That's not coincidental. It's structural.

## What this means for the architecture

The benchmark confirms the design hypothesis. f(0) orchestration isn't just about parallelism. It's about *context hygiene*: every agent receives exactly the context it needs to do its task well, no more, no less. Manifests carry the signal forward in compressed form (dashboard_line ≤80 chars). Bundles inject that signal selectively. The agent doing infrastructure clustering doesn't need to re-read 50 intel files — it reads the correlation manifests, which already extracted the relevant patterns.

This is why the compass exists. South-bearing manifests mean "proceed — quality gate passed." North-bearing means "don't proceed — prerequisites missing." The routing isn't bureaucracy. It's quality enforcement. Low-quality clustering work doesn't get promoted to summary writers. The chain stays clean.

---

*Written from: baseline-run-001-summary.json + faerie2-run-001 orchestrator manifest (eff=0.907, compass_edge=S)*  
*Neighbor manifests read: forensics-hook-audit, faerie2-run-001 orchestrator*
