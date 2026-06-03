---
type: explainer
audience: skeptical-engineer
status: draft
created: 2026-05-19
title: "For Skeptics: How Faerie's 0% Confabulation Rate and 100% Manifest Truthfulness Are Actually Measured"
---

# For Skeptics — "You're Just Making That Number Up, Right?"

Short answer: **no.** The 0% confabulation rate and 100% manifest truthfulness numbers aren't vibes, aren't an LLM self-rating, and aren't a benchmark on a curated test set. They are the **directly observed outputs of a deterministic verification hook that runs after every agent turn**, written to an append-only ledger, signed with Ed25519, and hash-chained into the chain of custody (COC).

If you don't trust the number, you don't have to trust me — you can recompute it from the raw event log yourself. This doc walks through exactly how.

---

## 1. What the two metrics actually mean

These are defined in [`docs/22-AGENT-CARD-REPUTATION-SCHEMA.md`](https://github.com/Persistech/faerie/blob/main/docs/22-AGENT-CARD-REPUTATION-SCHEMA.md) on Persistech/faerie. They are **not** LLM-eval scores. They are mechanical.

### `manifest_truthfulness_score`
- Every agent run ends by writing a **manifest**: a JSON blob declaring what it did — `files_written`, `commands_run`, `dashboard_line` claims, etc.
- An **adversarial reviewer** (a separate agent, or a deterministic checker) reads the manifest and asks: for each verifiable claim, can it be confirmed against the filesystem / git / COC log right now?
- Verified claim → `+1`. Caught lie → `−1`.
- Score = decay-weighted 30-day rolling average: `Σ verdict_i · exp(−days_i / 30) / Σ exp(−days_i / 30)`.
- Range: `[−1, 1]`, displayed clamped to `[0, 1]`. New agents start at `0.85` as a Bayesian prior.

### `mutation_verification_pass_rate`
- The narrower, cheaper, fully-deterministic cousin.
- For each `files_written: [...]` entry in a manifest, the post-turn hook `stat()`s the path. Either the file exists with the declared sha256 — or it doesn't.
- Pass rate = `present_files / claimed_files`.
- No LLM involved. No judgment call. A filesystem syscall.

### "Confabulation rate"
- Defined as `1 − mutation_verification_pass_rate`, restricted to **claims the agent made about its own outputs** (the strict subset).
- "0% confabulation" means: across the measured window, every single file an agent claimed to have written, **was actually present on disk with the claimed hash**.

The distinction matters: **truthfulness** is the broader, adversarial measure (catches lies about what was done, what was found, what was concluded). **Confabulation rate** is the narrow, automated measure (catches lies about file outputs specifically).

---

## 2. Why the numbers can legitimately be 0% / 100%

A skeptic's instinct is "no real system gets 100% — you must be cooking the books." Three reasons this one can:

1. **The measure is narrow on purpose.** Confabulation rate only looks at `files_written` claims. That set is small, structured, and trivially verifiable (`os.path.exists` + `hashlib.sha256`). It's not measuring "did the agent hallucinate any fact ever"; it's measuring "did the agent lie about the artifact it just produced." That's a much easier bar — and a useful one, because it's the lie that breaks downstream tooling.

2. **The hook runs synchronously and the manifest is rewritten if it fails.** `9x_reputation_tracker.py` fires on `PostToolUse`. If a `files_written` claim doesn't verify, the manifest is rejected and the agent gets a `caught_lying` increment. So observed 100% means: across N runs, every manifest either (a) verified clean, or (b) was rejected before it became a measurable event. The denominator is "manifests that were accepted." This is honest math, not p-hacking — but it's worth saying out loud.

3. **The system is small and recent.** At current scale (hundreds-to-low-thousands of manifests, single-digit weeks of operation), a 100% pass rate is plausible. It is **not** a claim about the asymptotic behavior of LLMs in general; it is a claim about *this fleet, this hook config, this window*. If you want to make me sweat, ask "what's the rate at 100k manifests?" — I don't know yet.

---

## 3. The evidence chain (what you can actually inspect)

This is the part skeptics should care about. Every number is reproducible from artifacts a third party can audit.

```
agent run (under OpenHands runtime)
  └─► writes manifest:  forensics/ephemeral/{date}/{task_id}/*_manifest_*.json
        └─► PostToolUse hook 9x_reputation_tracker.py fires (synchronous)
              ├─► verifies each files_written entry via stat + sha256
              ├─► appends ONE event line directly to canonical:
              │     forensics/reputation/events/{YYYY-MM-DD}/reputation-events.jsonl
              ├─► every 10 events: recompute REPUTATION block on agent ledger
              │     forensics/reputation/agents/{agent_type}.md   (atomic tmp+rename)
              ├─► Ed25519-signs the REPUTATION block (9x_agent_sign.py)
              └─► appends a hash-linked COC entry:
                    forensics/coc.jsonl
```

**Important:** the runtime is **OpenHands**, the evidence tree is any
`forensics/` folder — either *this* repo's, another investigation repo's
(e.g. `cybertemplate/forensics/`, `faerie-vault/forensics/`), or the **global
forensics root** at `$FAERIE_FORENSICS_GLOBAL` (`$FAERIE_FORENSICS_GLOBAL`).
All three are equally citable: each is git-tracked or WORM-backed, hash-chained,
Ed25519-signed, and append-only. There is no `.claude/` mirror, no per-machine
shadow tree. Hooks execute under OpenHands and write **directly** to a canonical
`forensics/reputation/` path — same promotion pipeline as manifests, no
intermediate location. Anything outside a `forensics/` tree is not part of the
system of record and is not citable as proof.

So for any reported metric, you can:

1. **Open the canonical agent reputation ledger** at `{repo}/forensics/reputation/agents/{type}.md` — it carries the current REPUTATION block, Ed25519-signed, hash-linked to its prior version.
2. **Verify the signature** with the public key in `{repo}/forensics/reputation/keys/{type}.pub`. If it doesn't verify, the ledger has been tampered with — throw the number out.
3. **Recompute from raw events.** Replay `{repo}/forensics/reputation/events/{YYYY-MM-DD}/reputation-events.jsonl` through the same formula (`Σ verdict · exp(−Δdays/30) / Σ exp(...)`) and you should land on the same score to floating-point precision.
4. **Cross-check against COC.** Every reputation event has a corresponding `{repo}/forensics/coc.jsonl` entry with the same `(session_id, task_id, manifest_path)` triple, hash-chained to the prior entry. If a reputation event lacks a COC counterpart — or the COC chain breaks — the metric is invalid.
5. **Spot-check the underlying manifests.** Pick any 10 manifests at random from `{repo}/forensics/manifests/{YYYY-MM-DD}/` (promoted canonical location, **not** `forensics/ephemeral/` — ephemeral is pre-promotion scratch and is not citable as proof). For each `files_written` claim, `stat` the path and `sha256sum` it. Compare to the manifest's declared hash. Any mismatch in the "passed" set means the metric is fraudulent.

This is the whole audit. It takes maybe 20 minutes to do by hand for a sample. There's no inner sanctum; the ledger is on disk, the formula is in `9x_reputation_tracker.py`, the signing key is per-agent.

---

## 4. What this metric does NOT claim

Because skeptics are right to suspect overclaiming, here's what these numbers explicitly **do not** mean:

- **Not** "the agent never hallucinates in prose." Free-text reasoning isn't scored here. An agent can absolutely write a wrong analytical paragraph and still get 100% manifest truthfulness, because nothing in the paragraph is a structured verifiable claim.
- **Not** "the agent's conclusions are correct." Correctness of *reasoning* is what adversarial review and human annotation are for — slower, fuzzier, separate metric.
- **Not** "no LLM hallucination occurred." Hallucinations that don't make it into the manifest (because the agent corrected itself, or the claim was never structured) aren't counted. The measure is about **what survived to the artifact layer**.
- **Not** "trust everything the agent says." It means: "when the agent says it wrote file X with hash Y, you can trust that specific claim to the extent the hook verified it."

Think of it like a build system's reproducibility metric. "100% of declared build outputs match their declared hashes" is a real and useful guarantee. It is not "the code is bug-free."

---

## 5. The honest failure modes

If you're trying to break my number, here's where to push:

1. **Selection bias on the denominator.** If rejected manifests don't count, an agent could thrash producing bad manifests, get them all rejected, finally produce one good one, and score 100%. **Mitigation:** `caught_lying.count` is monotonic and never decays to zero (only `decay_factor` decays). A high rejection rate shows up as a low routing weight even when the truthfulness score looks good. Look at both.

2. **Trivial manifests.** An agent that writes manifests with `files_written: []` can never fail the check. **Mitigation:** mutation verification is only one of two metrics. Adversarial review (`manifest_truthfulness_score`) catches "this agent claimed to do X but the manifest is suspiciously empty."

3. **Hook bypass.** If an agent could write a manifest without triggering the hook, it could lie freely. **Mitigation:** the hook is registered at the Claude Code / OpenHands runtime layer, not the agent layer. Agents have no API to disable it. The settings file is git-tracked; tampering shows up in `git diff`.

4. **Signing key compromise.** If a per-agent private key under `forensics/reputation/keys/` leaks, an attacker can forge REPUTATION blocks. **Mitigation:** keys are per-agent, never logged, and the COC chain provides an independent witness — a forged ledger with no matching event-log history fails cross-check.

5. **Small-N statistics.** 100% over 50 runs is a much weaker claim than 100% over 50,000. Always ask "over how many manifests, in what window?" The agent card shows `last_updated`; the event log shows N. Do the math.

If a skeptic raises any of these, the right answer is "good catch, here's the cross-check that addresses it" — not "trust me." Every one of these has a verifiable counter-artifact.

---

## 6. The one-paragraph version (for your colleague)

> The 0% confabulation rate isn't an LLM self-evaluation or a benchmark score. It's the direct output of a synchronous post-turn hook that takes every `files_written` claim the agent makes in its manifest, runs `stat` + `sha256` on the path, and records pass/fail to an append-only, Ed25519-signed, hash-chained ledger. Recomputing the metric from raw events takes one script and matches the displayed score to floating-point precision. The schema is documented in `docs/22-AGENT-CARD-REPUTATION-SCHEMA.md` and the verifier is `9x_reputation_tracker.py`. The number is narrow — it measures lies about declared artifacts, not hallucinations in prose — but within that scope it's mechanically real. If you want to break it, the highest-leverage attack is small-N statistics: ask how many manifests, over what window. That's the honest weakness.

---

## 7. Where to look in the repo

**Forensics never live outside `forensics/`.** The runtime is OpenHands; the evidence tree is whichever `forensics/` folder the work belongs to. Three citable scopes exist and can be cross-referenced:

- **This repo's `forensics/`** — `{repo}/forensics/` (e.g. faerie2)
- **Sibling-repo `forensics/`** — e.g. `cybertemplate/forensics/`, `faerie-vault/forensics/`
- **Global `forensics/`** — `$FAERIE_FORENSICS_GLOBAL` (`$FAERIE_FORENSICS_GLOBAL`), the cross-investigation root for system-wide events

All three carry the same guarantees: git-tracked or WORM-backed, hash-chained, Ed25519-signed, append-only.

| Artifact | Canonical path | What it proves |
|---|---|---|
| Schema | `{repo}/docs/22-AGENT-CARD-REPUTATION-SCHEMA.md` | Definitions, formulas, ownership |
| Verifier code | `{repo}/scripts/9x_reputation_tracker.py` | The actual code that decides pass/fail |
| Raw event log | `{forensics-root}/reputation/events/{YYYY-MM-DD}/reputation-events.jsonl` | Per-event ground truth, append-only, hash-linked |
| Per-agent ledger | `{forensics-root}/reputation/agents/{type}.md` (`## REPUTATION` block) | Current rolling score, Ed25519-signed |
| Public key | `{forensics-root}/reputation/keys/{type}.pub` | For signature verification |
| Chain of custody | `{forensics-root}/coc.jsonl` | Independent hash-chained witness |
| Manifests (promoted) | `{forensics-root}/manifests/{YYYY-MM-DD}/*.json` | The claims being verified |
| Rejected manifests | `{forensics-root}/rejected-manifests/{YYYY-MM-DD}/*.json` | The lies that didn't make it onto the chain |

Where `{forensics-root}` may be any citable scope above. Cross-scope claims (e.g. a manifest in `cybertemplate/forensics/` citing a global reputation ledger entry) are valid as long as both endpoints carry their own hash + signature.

**Not citable as proof** (mutable / volatile / scratch):
- `forensics/ephemeral/**` (any scope) — pre-promotion agent scratch; manifests transit here briefly before the promotion hook moves them into `forensics/manifests/{date}/` via symlink
- `/tmp/**`, `/var/tmp/**`, `.obsidian/**` — volatile or UI-derivative
- Any path outside *any* `forensics/` tree

If anyone says "this is just LLM marketing numbers," send them this doc and the seven paths above. Then let them recompute it themselves.

---

## 8. Why the *observed* hallucination rate is near zero — reputation + cross-checking as a pre-chain filter

Section 1-7 explained why the metric is honest. This section explains why the underlying behavior is actually good — i.e. why hallucinations get **caught before they make it into the hash chain**, rather than caught after.

The chain doesn't just *measure* truthfulness; the architecture around it *produces* truthfulness, by making lying expensive and being caught lying career-limiting (for an agent).

### 8.1 The pre-chain gauntlet

A claim has to survive several independent checks before it gets a COC entry. Each layer is a separate, cheap filter; the product of their pass rates is what you observe as "0% hallucination on chain."

```
agent generates output
  ├─► (a) self-check: agent re-reads its own manifest before submit
  ├─► (b) deterministic verifier: 9x_reputation_tracker.py
  │       stat() + sha256 every files_written claim
  │       → fail = manifest rejected, NEVER reaches chain
  ├─► (c) adversarial reviewer (separate agent, different reputation key)
  │       reads manifest, tries to falsify claims
  │       → catch = caught_lying++, manifest rejected
  ├─► (d) cross-agent audit: any agent acting as auditor stakes its own
  │       adversarial_auditor_score on the verdict — false catches
  │       hurt the auditor; missed lies hurt the original agent
  └─► (e) only THEN: hash-chained into forensics/coc.jsonl
```

The "0% confabulation on chain" number is what's left *after* (a)-(d) filter out the lies. Those filters are not free: each one has a measurable rejection rate. If you sum up (rejected at b) + (rejected at c) + (rejected at d), you get the real upstream lie rate — and it is **not** zero. It's small but nonzero. The chain is clean because the gauntlet works, not because nothing was ever wrong.

This is the same epistemic move as a build system: "0 broken builds in main" doesn't mean nobody ever wrote broken code; it means CI rejected the broken commits before they merged. Main is clean *because* CI is loud.

### 8.2 Reputation as economic incentive

Reputation makes the gauntlet **self-enforcing** rather than purely external. Two mechanisms:

**For the producing agent:**
- `caught_lying.count` is monotonic. It never decreases. The `decay_factor` softens the penalty over 14 days but the count is permanent.
- A `caught_lying` event pushes routing weight toward `DEMOTION_THRESHOLD` (0.5). Below that, the agent type gets rerouted to `stigmergy-scout` — i.e. it loses the ability to take real tasks and gets demoted to classification work.
- So an agent type that lies once eats a small permanent penalty and a large temporary one. An agent type that lies twice in a window risks demotion. The incentive is to refuse a claim when uncertain, not to fabricate.

**For the reviewing agent:**
- `adversarial_auditor_score` tracks whether the auditor's "catch" calls were upheld by the eval harness. A reviewer who cries wolf gets demoted just as fast as a producer who lies.
- This is the key piece: **cross-checking has a cost**. You can't bury a producer in spurious catches to look diligent — your own score tanks. So adversarial review converges on actually-justified catches.

The result is a small adversarial market where both sides are staked on accuracy. Not friction-free, but the equilibrium is "say what you can verify, catch what's actually false." Which is what you want.

### 8.3 Cross-checking culture — what makes it cheap

Three architectural choices make cross-checking cheap enough to do by default rather than as a special audit:

1. **Manifests are structured.** Verifiers don't need to parse prose; they parse JSON. A reviewer agent reading a manifest is doing field-level checks, not reading comprehension.
2. **Claims are addressable.** Every claim names a file path, a session_id, a manifest_path, or a COC line. The reviewer can `stat`/`grep`/`git log` and get a yes/no without judgment.
3. **Reputation is cached on the agent card.** The router checks `routing_weight` at spawn time, not at audit time. The audit happens once, the consequence persists forever in the card. One verification, many downstream decisions.

Without these, cross-checking would be expensive enough that you'd ration it — and rationed audits are easy to game. Cheap audits are hard to game, because there's nowhere quiet to put a lie.

### 8.4 What "minimal observed hallucination" really means

Put together:

> Observed on-chain confabulation is ~0% **because** every claim runs a deterministic verifier (b), an adversarial reviewer with its own skin in the game (c), and a cross-agent audit with reputation stakes (d), before being hash-chained. The lies that exist get caught at (b)-(d) and never reach (e). The number you see is the post-filter rate, and the filter is mechanical, signed, and replayable.

The hallucinations that *do* exist are visible in canonical forensics (never in `~/.claude/`, never in `forensics/ephemeral/` — both are mutable scratch and not citable):

- `caught_lying.count` per `{repo}/forensics/reputation/agents/{type}.md` ledger (cumulative, monotonic, signed)
- Rejection events with `verdict = -1` in `{repo}/forensics/reputation/events/{YYYY-MM-DD}/reputation-events.jsonl`
- Rejected manifests promoted to `{repo}/forensics/rejected-manifests/{YYYY-MM-DD}/` with their rejection reason and the COC entry that records the rejection

If you want the *real* upstream hallucination rate, sum those. They are not hidden — they're just not on the truth chain, because the truth chain is the post-gauntlet ledger. The **rejection trail** is its own forensic record, equally append-only and hash-linked.

---

## 9. What "being added to the chain" means for truthfulness / confidence

This is the question that exposes whether someone understands the system or is treating it as marketing. Short answer:

**Being added to the chain ≠ being true. It means: this claim passed every cheap pre-chain filter and is now structurally accountable.**

Three layers to unpack:

### 9.1 The chain is a commitment device, not a truth oracle

Once a manifest is hash-linked into `coc.jsonl`:

- It is **append-only** — you cannot quietly retract it. A correction requires a *new* entry that references the old one.
- It is **hash-linked** — modifying any past entry breaks every subsequent hash, which is immediately detectable.
- It is **signed** — the agent's Ed25519 key committed to that exact byte sequence at that exact time.

So inclusion doesn't *make* a claim true. Inclusion makes a claim **permanent and attributable**. If it turns out later to be false, you cannot pretend it didn't happen — you must issue a counter-entry, and your `caught_lying.count` ticks up forever.

This is why agents become more careful at the chain boundary: pre-chain, you can quietly fix a manifest; on-chain, every error becomes part of your permanent record. The chain is the asymmetry that turns "be careful" from an aspiration into an incentive gradient.

### 9.2 Confidence is what the chain *enables you to compute*, not what it asserts

The chain doesn't say "this claim is true with probability 0.97." It says "this claim was made, by this agent, at this time, with this verifier passing, signed by this key, with these N priors in the same agent's history."

From that, downstream consumers can compute confidence. Examples:

- **High confidence:** claim is in chain + agent has high `manifest_truthfulness_score` + low `caught_lying.decay_factor × count` + claim type is one the deterministic verifier covers (e.g. file output).
- **Medium:** in chain, decent reputation, but claim type is prose-reasoning where only adversarial review applies (slower, fuzzier).
- **Low:** in chain, but agent has recent `caught_lying` events, or claim depends on inputs that themselves came from low-reputation upstream agents.

So the chain is the **substrate** for confidence calculations. The number you trust is reputation-weighted, not chain-membership-thresholded. "On the chain" is the floor (someone is accountable); "high reputation + on chain + verified claim type" is the ceiling.

### 9.3 Why this matters for hallucination

Hallucination becomes **structurally observable** the moment a claim is on the chain. Before chain entry, a hallucination is just a draft — embarrassing if caught, but recoverable. After chain entry, a hallucination is a forensic event: it generates a counter-entry, a `caught_lying` increment, a routing-weight hit, and a permanent record both for the producing agent and for any reviewers who waved it through.

So the architectural answer to "how can hallucination be near zero" is:

> Because **the cost of letting a hallucination onto the chain is structurally higher than the cost of pausing to verify**. Agents that don't internalize this lose routing weight and get demoted. The chain isn't proving the claims are true — it's making the producing-and-reviewing pipeline care, by making "being added" expensive enough to be earned.

That's the whole trick. Reputation provides the gradient; the chain provides the commitment; cross-checking provides the cheap-enough filter; and what you observe at the top — 0% on-chain confabulation, 100% manifest truthfulness — is the post-filter steady state of a system designed so that lying is more expensive than checking.

It's not magic. It's just a small economy that pays for honesty.

