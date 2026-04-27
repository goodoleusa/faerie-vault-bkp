---
type: meta
tags: [meta, faerie, evaluation, memory, marketing]
updated: 2026-03-24
parent: []
child: []
sibling: []
memory_lane: nectar
promotion_state: raw
doc_hash: sha256:b1a0dadfc41fe39f2f1bc5dc51053d60288fb624847636094cbb5395b109e452
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:18Z
hash_method: body-sha256-v1
---

# Measuring faerie’s impact — the honest A/B

This doc is a **heuristic comparison**, not a controlled study. Use it to **design demos** and **talk honestly** about what file-backed memory and queues add on top of “native” assistant sessions.

---

## Sovereignty, optional managed memory, and what faerie is *for*

**Three layers** (see [[00-OVERVIEW]]  that govern user data sovereignty

**(1)** Obsidian **vault** = conceptual collaboration home and readable memory. 

**(2)** **COC repo** = original forensic masters and audit trail. 

**(3)** **Managed memory** (optional) = hosted processor for **slices you approve** — not a replacement for (2).

**Managed memory** is **optional**: it can **increase depth and quality** when enabled; serious work can stay **fully local** with the same promotion gates.

**Faerie’s value proposition** is **legibility, continuity, and interoperability**: promoted narrative (`NECTAR`), orientation (`HONEY`), flags (**REVIEW-INBOX**), **queue**, and **agent cards** survive sessions and compaction. That **crystallized intelligence** lets **individuals** work like they have a lab notebook and **teams** share one **vault layout** so partners can **swap investigation folders**, reuse conventions, and **join the same research network** without re-explaining the whole case — while **COC originals** stay in the **repo** you control.

---

## What “native” Claude remembers *without* faerie

- Whatever is in the **current conversation context** (subject to compaction and window limits).
- The auto-memory **`MEMORY.md` index** where enabled — typically **pointers**, not full retained narrative.
- **`CLAUDE.md` / project instructions** loaded at session start (size and behavior vary by product and settings).

---

## What faerie adds on top (this stack)

- **`HONEY.md`** — Dense seed read early in the run (often ~200 lines cap), orienting agents quickly with **human-validated** preferences, methods, and anchored findings.
- **`NECTAR.md`** — Append-only narrative of **promoted** findings across sessions; survives **compaction** because it lives on disk, not in the chat transcript.
- **`REVIEW-INBOX`** — Surfaces **HIGH** flags from agents across sessions (in this vault, under the human inbox / flags surface agents write to).
- **Sprint queue** — Work is **durable** across session boundaries; claim / complete semantics let runs resume without re-explaining the plan.
- **Agent cards** — Per–agent-type notes (e.g. under `~/.claude/agents/`) where **training scores** and **last-learned techniques** can accumulate run-over-run.

Paths may differ between **CyberTemplate / Claude Code home** and **this Obsidian vault**; the invariant is: **filesystem-backed state + human promotion gates**, not “more tokens in chat.”

**Vault note shape:** When agents write human-readable deliveries into **`00-SHARED/`**, use **`00-META/12-ASYNC-HUMAN-AGENT-BRIDGE`** — same YAML for async read/reply **and** optional **faerie** fields (`memory_lane`, `promotion_state`, `queue_task_id`, `bundle_ref`, …) so queues, NECTAR/HONEY routing, and bundles stay queryable in Obsidian.

---

## The comparison (expected deltas)

| Metric | Without faerie | With faerie |
|--------|----------------|-------------|
| Session startup (turns before productive work) | Often **3–5** turns re-establishing state | Often **1** turn once `HONEY` / brief is loaded |
| Finding survival across compaction | Easy to **lose** unless user pastes back | **NECTAR** (and linked notes) **preserve** promoted narrative |
| Agent improvement over time | Tends to **reset** toward baseline each session | Can **accumulate** in cards + promoted memory files |
| Queue continuity | **Manual** (user re-types the plan) | **Structural** (claim / complete) |
| Cross-session coherence | Depends on **user recap** | **Structural** (disk + inbox + queue) |

Numbers like “3–5 turns” are **order-of-magnitude guides** for demos, not guarantees.

---

## Demo protocol (marketing-friendly but reproducible)

1. **Pick one fixed task** — e.g. same investigation prompt, same deliverable shape (outline, entity table, timeline), written **before** either run.
2. **Match the product** — same model tier, same account, same project; avoid comparing Sonnet to Opus.
3. **Arm A — cold start** — new chat, **no** faerie read, **no** `HONEY` / `NECTAR` injection; only the same `CLAUDE.md` you would have in production (or explicitly **none** in both arms).
4. **Arm B — faerie loaded** — start session with `/faerie` (or equivalent) so **`HONEY` + inbox + queue state** are actually on disk and read in.
5. **Pre-register “productive”** — e.g. first message that includes a cited artifact, a structured table, or a testable hypothesis list (pick **one** rubric and stick to it).
6. **Count** — turns to first productive output; optionally score quality with a **blind** rater using a short checklist (completeness, citations, alignment to prompt).

**The faerie delta** = difference in turns + rubric score between arms. Report **N=1** honestly; repeat across a few tasks to show a pattern.

---

## Confounders to name out loud

- **User skill** at prompting and at editing `HONEY`/`NECTAR`.
- **CLAUDE.md size** and quality — a huge project doc shrinks the apparent faerie gap.
- **Task type** — retrieval-heavy tasks benefit less than long-horizon investigations with promotion discipline.
- **What you promote** — faerie cannot fix garbage-in; NECTAR quality follows **human promotion** quality.

---

## What we are *not* claiming

- Faerie is not a substitute for **human judgment**, **legal review**, or **OPSEC**.
- File-backed memory does not automatically mean **correct** — only **durable** and **inspectable**.

---

## Related vault docs

- [[00-OVERVIEW]] — principles, data sovereignty, HONEY vs case substance.
- [[03-AGENT-HANDOFF-EXPLAINER]] — handoff and vault as collaboration surface.
- [[00-SHARED/HOW-SYNC-WORKS]] — what syncs vs stays local.
