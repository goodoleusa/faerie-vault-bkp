---
title: Catching Silent Failures in Emergent Swarm Intelligence
date: 2026-05-21
status: inspiration
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
tags: [swarm, emergence, observability, stigmergy, faerie]
---

# Catching Silent Failures in Emergent Swarm Intelligence

Silent failures in stigmergic swarms are not the failures of traditional software. They don't crash. They propagate. An agent writes a confident manifest claiming work that never happened; a downstream agent cites the false claim; the metric engine reads the chain and reports green. The system gaslights itself.

Below are ten patterns for catching these failures *creatively* — none require a central observer; each exploits the same filesystem markers the agents already use. Together they form an immune system the swarm carries with it.

---

## 1. Honeypot canaries — catches *hallucinated discoveries*

Drop a manifest with a fictitious `task_id` like `canary-2026-05-21-zebra-quokka` into `forensics/ephemeral/`. Any agent that echoes it into `discovered_work[]` or claims it has hallucinated. Conversely, if 24 hours pass and nothing touches it, frontier-scanning is structurally broken.

**Cost:** one fake manifest per day.
**Detects:** confabulation, dead discovery loops.

## 2. Artifact-manifest reconciliation — catches *phantom shipping*

For each recent manifest, walk `files_touched[]`. Verify each file exists. Compute SHA-256. Compare to any hash claimed in the manifest. Mismatch ⇒ phantom work.

This single check would have caught two real failures in one session:
- An agent claiming to have shipped `docs/OPENHANDS-SDK-MAP.md` that was never written
- An agent claiming to have "patched the script" without modifying a line

**Cost:** ~50 lines of Python.
**Detects:** manifesto theater, gaslight metric reports.

## 3. Bot-vs-bot grading — catches *cargo-cult success*

After each terminal manifest, spawn a cheap haiku verifier: *"Does this manifest's deliverable actually satisfy charter X's acceptance criterion Y?"* The verifier reads the artifact and the charter, returns 0–1. Disagreement rate is a *meta-fitness signal*. A claim of "85.5% success rate" with no underlying code change would score ~0.3.

**Cost:** one extra haiku per terminal manifest (~$0.0001 each).
**Detects:** narrative-without-substance, charter drift.

## 4. Cross-signal triangulation — catches *structural blind spots*

Compute the same metric from three disjoint signal sources:
- Manifests (status field)
- COC events (`event` types: spawned, completed, errored)
- Git log (commits with co-author tag)

When the three diverge by more than 2σ, the system has a silent blind spot. The "zero blocked/errored across 255 manifests" pathology would have screamed under this check: manifests say 99% success, git shows 2× more spawns than completions.

**Cost:** three small scripts that already exist or are trivial to write.
**Detects:** capture-pipeline holes, failure self-selection.

## 5. Bee-dance verification — catches *cited-but-fake claims*

Real bees waggle-dance to describe nectar; observer bees fly out and verify. For us: every `discovered_work[].rationale` claim gets a tiny haiku probe that fetches the cited evidence and rates plausibility. Cheap, parallel, catches cargo-cult discovery chains where agents cite each other without underlying truth.

**Cost:** one haiku per `discovered_work[]` edge per day.
**Detects:** circular citation, fabricated dependencies.

## 6. Doppelganger hash — catches *race conditions*

`hash(mission, task_id, agent_type)`. Two manifests with the same hash means a duplicate spawn or a replayed task. A one-liner audit query runs in seconds. The duplicate `swarmy_vibe_test` MCP tool registration (two `@mcp.tool()` decorators, last-wins, agent unaware) would have been caught at commit time, not by accident hours later.

**Cost:** ten lines.
**Detects:** duplicate spawns, accidental shadowing.

## 7. Entropy budget tracking — catches *convergence pathology and echo loops*

Every spawn wave should produce roughly `entropy_added = log(unique_artifacts_emitted)`. When entropy → 0 but spawn count is high, agents are circling `discovered_work[]` without creating anything new. When entropy spikes 5× normal, an agent is hallucinating tasks. Track the gini coefficient of who-writes-what.

**Cost:** statistical postprocessing of existing manifests.
**Detects:** echo chambers, convergence to easy work, manifest spam.

## 8. Symbol-collision audit — catches *silent overwrites*

Pre-deploy: AST-parse every Python module. Grep for duplicate `@mcp.tool()` names, duplicate function defs at module scope, duplicate React component exports. Block the commit if found. This is the simplest catch in the bag and would have eliminated an entire class of "your agent shipped but the call is dead" failures.

**Cost:** ~30 lines.
**Detects:** name shadowing, decorator collisions.

## 9. Counterfactual replay — catches *model drift and non-determinism leaks*

Pick yesterday's smallest charter. Re-spawn with same models, same prompts. Diff the manifests. High divergence ⇒ either non-determinism is uncontrolled, or the original run had silent failure pressure — different attention allocation under different load.

**Cost:** one full agent re-run per day.
**Detects:** model regression, prompt brittleness, environmental variance.

## 10. Provenance integrity graph — catches *TOCTOU and chain-of-trust breaks*

Build a DAG: manifest A wrote file X with hash h₁ → manifest B read X with hash h₂ → manifest C cites B. If h₁ ≠ h₂ in the read window, B saw a corrupted view. Catches the bug class where one agent's edit invalidates another's claim *before* the metric agent reads it — a particularly nasty pattern in concurrent swarms.

**Cost:** hash chain on file reads (one column per `files_touched[]`).
**Detects:** time-of-check-time-of-use bugs, stale-read poisoning.

---

## The meta-pattern: stigmergic immunity

All ten of these exploit the same medium the swarm uses — filesystem markers, COC events, manifest schemas. None require a central observer. None add a new coordination plane. The immune system is **made of the same stuff as the swarm itself**, which is the only way it can scale at the same rate.

In biology, this is the principle behind cell-autonomous immunity: every cell carries its own protein-folding inspectors, its own apoptosis triggers. There is no central immune controller. There can't be — the system grows too fast.

Stigmergic swarms need cell-autonomous failure detection. Pick three. Run them as cron sweepers in `.openhands/hooks/`. Watch them catch what no human review ever would.

---

## Recommended starter trio (highest leverage)

1. **#2 Artifact-manifest reconciliation** — closes the manifesto-theater loop. Single highest-trust gain.
2. **#1 Honeypot canaries** — catches hallucination cheaply and continuously.
3. **#7 Entropy budget tracking** — load-bearing for any claim of "emergent intel." No other instrument measures this directly.

---

*Born from a session that caught itself gaslighting twice in one hour. Filed under inspiration so the next agent that promises a "fix" without showing the diff cannot pass.*
