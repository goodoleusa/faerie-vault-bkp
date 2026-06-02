---
title: "Retroactive Anchor Promotion — The Recovery Path"
type: architecture-narrative
created: 2026-06-02
canonical_tier: { agents: true, humans: true }
tags: [f0, gates, anchor-promote, recovery, coc, insight-regrounding, bypass, genetic-code]
mirror_of: "reckon/docs/152-RETROACTIVE-ANCHOR-PROMOTION-CANONICAL.md"
pairs_with: ["150-GATES-VS-INSIGHT-CANONICAL", "145-THE-CHARTER-SEAL-CANONICAL"]
---

# Retroactive Anchor Promotion — The Recovery Path

*Work that bypasses a gate is not lost — it is displaced. Retroactive anchor promotion
is the recovery path: it pulls displaced work back into the canonical, gated chain
after the fact, without pretending the bypass never happened. The gate still fires; the
COC still chains; the work earns its place through measurement, not through amnesia
about how it arrived.*

---

## Why bypasses happen

Gates are infrastructure, and infrastructure is never perfectly ahead of the work.
Three patterns recur:

**Ad-hoc hand-work.** An operator writes a critical CLAUDE.md entry or schema fix
directly — correctly and necessarily — during an emergency or an early sprint before the
gate existed. The work is good. It just arrived outside the chain.

**Pre-gate discovery.** A principle is observed and referenced by downstream agents
before `anchor_promote` was wired for it. The insight is real; its provenance is
informal.

**Branch-isolated work.** A worktree branch ships a correct mutation before the L2
merge cycle completes. The mutation lives on the branch, not yet hash-chained into the
canonical forensic record.

In all three cases: the work has merit but no gate receipt. Retroactive anchor
promotion closes that gap — and it closes it with a real gate run, not a rubber stamp.

---

## The four-step recovery sequence

```
propose ──▶ eval ──▶ promote-if-gated ──▶ COC
```

Each step maps to a subcommand in `scripts/anchor_promote.py`. None are skippable.

**Propose (`--propose <anchor_path>`).** The principle is extracted, a patch record is
written to `forensics/prompt-patches/{date}/{slug}.json` with `status: proposed`, and a
COC entry `anchor_patch_proposed` is appended. The patch is *not* applied yet. This is
the pre-registration step — declaring intent before acting. Proposing after applying
replicates the bypass in miniature.

**Eval (`--eval <patch_id>`).** The eval harness runs twice: once against the live
system (baseline), once with the patch applied in-place (patched). Dimension scores
A–G are captured for each run; the original is restored after the patched run. Both
score objects land in the patch record; status advances to `evaluated`. If the
instrument is missing, the step returns an error — a broken instrument produces no
verdict, and a missing verdict blocks promotion.

**Promote-if-gated (`--promote <patch_id>`).** The gate logic reads the dimension
deltas: quality and emergence must not regress; all other dimensions must not degrade
more than 5%. Pass: patch applied to the live `faerie.njk`; status advances to
`promoted`; COC entry `anchor_patch_promoted`. Fail: status advances to `rejected`;
COC entry `anchor_patch_rejected`. **The gate can say no.** Retroactive does not mean
automatic.

**COC chain (automatic at each step).** Every step appends to `forensics/coc.jsonl`:

```
anchor_patch_proposed → anchor_patch_evaluated → anchor_patch_promoted (or _rejected)
```

The bypass is visible in the chain — proposal timestamp predates promotion; both
postdate the anchor's creation. The COC does not erase the bypass. It documents the
recovery.

---

## Insight re-grounding (§7 of `150`)

`150` §7 establishes that gates decay and insight must periodically re-enter to
re-ground them:

```
insight DEFINES a gate  ──►  gate AUTOMATES promotion  ──►  insight AUDITS the gate
```

Retroactive anchor promotion is a concrete instance of this loop. The bypassed insight
was correct — that is why it survived long enough to be promoted retroactively. But no
gate had crystallized it into a measured criterion. The `propose → eval → promote`
sequence *makes the gate explicit* around an insight that was previously implicit.

After promotion, the principle lives in the live system prompt. Future mutations that
degrade it will be caught by the next eval cycle. The gate is now downstream of the
insight, as the loop requires.

Un-promoted insights are floating claims. They may guide agent behavior, but they are
not measured, not gated, not part of the fitness signal. Promotion is the act of
converting a claim into a measured criterion — and the difference between a principle
that guides behavior and one that merely decorates a charter is exactly that.

---

## Branch recovery (tie to `145`)

`145` §L2 describes the heartbeat mechanism: a worktree branch sends tamper-evident
handshakes to `forensics/heartbeats/{branch}.jsonl` on every Rekor anchor and
eventually returns for L2 automated merge. But L2 handles *structural* merge, not
*semantic* promotion.

They compose:

| Mechanism | What it handles |
|---|---|
| L2 heartbeat + merge | branch liveness + structural merge to main |
| `anchor_promote` | semantic content (anchors, principles) → live genetic code |

A branch that ships a new CLAUDE.md principle must do both: L2 returns the files to
main; the operator runs `anchor_promote --propose` on the principle to close the
semantic loop. The COC records both events — the L2 merge entry and
`anchor_patch_promoted` — giving complete lineage from branch creation to live system
prompt.

---

## When not to use it

Retroactive promotion is a recovery path for prior bypasses. If there was no bypass —
if the principle was never informally in the system before — it is just `anchor_promote`
operating normally, which is correct.

Do not use it to paper over bad work. The gate runs on real measurements. A principle
that genuinely degrades the system will be rejected. If a bypassed principle fails, the
options are: revise it until it passes, split it, or discard it. There is no
force-promote path. The gate is not bypassed retroactively.

---

## The operating rule

Bypassed work has merit. Bypassed gates don't.

Every principle that operates informally is a gate that hasn't been written yet. Write
the gate: `--propose`, `--eval`, `--promote`. If the gate says no, the principle was
wrong about what it measured. If the gate says yes, it has earned its place in the
genetic code — and the COC proves it did.

The bypass is not erased. The recovery is recorded. Both are in the chain.
