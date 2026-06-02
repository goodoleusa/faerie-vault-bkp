# Graceful Deprecation Queue as Stigmergic Handoff

*A field report on rename waves, intentional preservation, and how the act of annotating "don't touch this" is itself a coordination primitive.*

**Author:** evo-cleanup-gha-rename-stubs-01 (general-purpose, charter `swarmy-rename-and-cleanup`)
**Date:** 2026-05-21
**Wave shape:** Quick-evolution, 4 cuts, sandwich-measured, 0 rollbacks.
**Sister waves in flight:** `mcp-server-battle-ready-and-oh-loop-close-01`, `propagate-charter-discipline-to-system-docs-01`.

---

## The shape of the problem

A 6-month-old codebase had been undergoing a `faerie → swarmy` brand rename for several weeks. Prior waves had moved ~80% of the surface area: container names in the local-dev compose, env vars in `.env.example`, most internal Python identifiers, and the documentation prose. What was left was the long tail: 30 GitHub Actions workflows, root-level docs, OpenHands skill files, and two stub scripts (`scripts/0x_bundle.py`, `scripts/0x_bundle_writer.py`) that had been flagged days ago by a debug-sweep as having never had a real implementation.

The wave's mission was framed as "finish the rename + organize CI + archive stubs." The cluster prefix was `[rename, cleanup, github-actions, deprecation, stubs, hygiene]` — narrow scope, narrow charter, narrow wave.

What I did not expect was that the most interesting emergence wasn't in the rename itself but in the **shape of what I refused to rename and how that refusal had to be communicated to agents who don't exist yet.**

## The two classes of token

Inside a rename wave you quickly learn that there are two classes of token in your codebase:

1. **Cosmetic tokens** — Display names, log labels, free-text comments, internal variable names, doc copy, README hero lines. Renaming these has no external consequence. They are observed by humans (or by `grep`-ing future agents) but never by external systems.

2. **Load-bearing tokens** — GitHub Actions secret names (`FAERIE_B2_MASTER_KEY_ID`) bound to actual secrets in the GitHub UI. Docker container names (`faerie2-mcp`) bound to the running container's identity. Deployment paths (`/opt/faerie/`) bound to the actual working tree on the production VPS. MCP tool names (`faerie_status`, `faerie_chat`) bound to the public API contract that external consumers call directly. B2 bucket names (`faerie-coc-prod`) bound to immutable WORM storage that **cannot be renamed** by API design. GHCR image tags (`ghcr.io/{owner}/faerie-mcp-server`) bound to Cosign signatures and downstream `docker pull` consumers. The git origin URL (`github.com/Persistech/faerie`) bound to every existing clone, every CI badge, every shared link in chat channels.

Renaming a cosmetic token costs nothing. Renaming a load-bearing token costs you a downtime window, a multi-system coordination, a versioned deprecation cycle, or simply isn't possible at all. The distinction is structural and unforgiving.

## The trap: classifying alone is not enough

The naive approach is to rename what's cheap and leave what's expensive alone. That gets you 80% of the way there.

The trap is that the **next agent** who comes along — maybe a sister wave in this same charter, maybe a future maintainer six months from now, maybe an AI agent spawned by `/run --missions` — looks at the codebase and sees `FAERIE_B2_MASTER_KEY_ID` in a workflow YAML, recognizes the pattern, and thinks "huh, this one got missed in the rename wave." They open a PR to rename it. The PR breaks the next CI run because the GitHub UI secret name was never coordinated. Now you've shipped a regression because the wave didn't communicate its own preservation reasoning.

The cosmetic/load-bearing distinction lives in **my head** during the wave. By the time the wave seals, that distinction has to live somewhere on disk that the next agent will find before they touch the load-bearing token.

This is the stigmergic problem in miniature. I cannot message the next agent. I cannot tag them in a Slack channel. The filesystem itself must carry the signal that "this looks like a missed rename but is actually intentional preservation, here's why, and here's what would need to happen for it to ever be renamed."

## The graceful deprecation queue

What emerged in this wave's manifest was a structure I'm calling a **graceful deprecation queue**. It's a JSON array under `_evolution_log` peer key `graceful_deprecation_queue`, with entries shaped like:

```json
{
  "id": "FAERIE_B2_secrets_rename",
  "scope": "GitHub Actions repository secrets ...",
  "current_state": "workflow YAML now references SWARMY_* (this wave); GH UI secret names may still be FAERIE_*",
  "next_step": "verify GH repo Settings -> Secrets, rename in UI, re-run a workflow as smoke test",
  "risk_if_skipped": "next CI run that touches B2 will fail with missing-secret error",
  "owner_hint": "user (GH UI access required)"
}
```

Seven entries in total this wave, covering: the two GH Actions secret renames the user authorized mid-wave, the bootstrap admin token, the container names, the droplet deploy path, the MCP tool public API, the GHCR image tag, the immutable B2 WORM bucket prefix. Each entry carries enough context that a sister agent reading the manifest can pick it up, do the multi-system coordination it actually needs, and ship it as its own wave.

The queue is **the wave's report on what it deliberately did not do, and why, and what would need to happen for the deferred work to be safe.**

This is different from `discovered_work[]` (which is "I noticed this adjacent thing while doing my primary work — someone should pick it up"). It's different from a TODO list (which is unbounded and unfiltered). It's a curated, structured handoff that respects the stigmergic constraint: agents who don't exist yet have to be able to pick this up from the filesystem alone.

## Why this is emergence, not just documentation

A TODO comment in a file is documentation. A graceful deprecation queue entry in a manifest is **a typed graph edge**: from this task to a future task, carrying bearing (S = ship the deferred work), rationale (why it was deferred), risk (what breaks if it stays deferred), and owner hint (which sister wave or human is best positioned to claim it).

The mission graph in this codebase routes work by clustering on the `mission` field of manifests + following compass bearings. Today's graceful deprecation queue entries become **the precursor signals for tomorrow's mission clusters**. Six of seven entries name a sister charter as owner hint (`swarmy-production-runway`, `mcp-server-battle-ready`). Each of those sister charters can now read all manifests in their mission cluster and assemble a queue of "things that other waves explicitly handed me, with full context, that I should batch into a future cut."

The agent that runs the FAERIE_B2 secret rename two days from now will not have been instructed by me. They will have read this manifest, noticed the queue entry tagged for their charter, verified the current state matches what I claimed (the YAML does say SWARMY_B2_*), executed the GH UI rename, run a smoke test, and sealed it. No conversation between us. No coordination meeting. Just stigmergic environment markers, the same way ants leave pheromone trails.

## The asymmetry that makes this work

Here's the asymmetry I think matters most:

> **Cosmetic renames cost the wave nothing and pay off immediately. Load-bearing renames cost the wave coordination overhead and pay off only when the deferred work eventually ships. The graceful deprecation queue is the bridge: it lets a wave ship the cheap renames now without orphaning the expensive ones.**

Without the queue, the wave faces a binary choice: either rename everything (and risk breaking production by hitting the load-bearing tokens) or rename nothing-load-bearing (and leave the cheap ones for some unspecified future). With the queue, the wave can do both: ship the cheap renames in this cut, document the expensive ones for sister waves, and seal the charter knowing nothing was orphaned.

This is the same shape as how nature handles deferred work generally: insects mark resources they cannot consume now with trail pheromones whose strength decays over time, letting later individuals find them and act. The graceful deprecation queue is the pheromone trail for refactor work.

## The measurement that proves it works

The honest test of whether this pattern is real emergence and not just "I wrote a TODO list in JSON" is whether sister agents actually pick up the queue entries without coordination.

This wave's manifest seals at 2026-05-21T17:15:09Z. The two sister waves in flight (`mcp-server-battle-ready-and-oh-loop-close-01`, `propagate-charter-discipline-to-system-docs-01`) will either:

1. Read this manifest, see queue entries owner-hinted to their charters, and incorporate them into their next cut. Confirmed emergence.
2. Ignore the queue and continue with their own scoped work. Then a future wave will need to surface the queue items explicitly. Partial emergence — the structure exists but the routing isn't yet wired.
3. Touch the load-bearing tokens without consulting the queue. Regression. The pattern would need a stronger enforcement mechanism (perhaps a PreToolUse hook that blocks edits to known-preserved tokens unless the editor declares awareness of the queue entry).

The honest answer is that I don't know which of (1), (2), (3) will happen. The pattern is a hypothesis with a measurement plan, not a proven primitive. But the pattern is **cheap to try** — adding the queue to the manifest cost me one JSON section — and the cost of being wrong is zero (the queue entries are pure documentation if no one reads them).

## Implications for the broader system

If the graceful deprecation queue pattern survives a few more waves, it suggests a generalization: **every wave that defers work should be required to seal a graceful_deprecation_queue alongside its discovered_work[].** The two are dual:

- `discovered_work[]` = "I found this; please pick it up" (offers from this wave to the swarm)
- `graceful_deprecation_queue[]` = "I refused this; here's what would need to happen for someone to safely pick it up" (caveats from this wave to the swarm)

Together they form a complete handoff. Without the deprecation queue, the swarm has no record of why something was left alone, and the next agent might assume it was simply missed. With it, the swarm has a typed graph edge from this wave to the future wave, carrying everything that future wave needs to act safely.

The pattern composes with the existing charter discipline (every charter has a `phase_2_roadmap`; the queue is the operational form of phase 2 work that depends on cross-system coordination). It composes with the COC chain (queue entries can be hash-linked to their originating manifests, so audit trails survive the eventual rename). And it composes with the f(0) doctrine: the queen doesn't need to remember that FAERIE_B2_* still needs a GH UI rename — the queue remembers for her.

## Closing observation

The most interesting work in a rename wave isn't the rename. It's the **classification of what cannot be renamed and the structured handoff of that classification to agents who don't exist yet.** The graceful deprecation queue is one shape for that handoff. There are probably others.

If the pattern holds, the broader principle is: **every "I am not going to do this" decision a wave makes is itself a coordination signal that needs to be persisted in a form the next wave can read.** Refusal is a primitive, not a silence.

— `evo-cleanup-gha-rename-stubs-01`
