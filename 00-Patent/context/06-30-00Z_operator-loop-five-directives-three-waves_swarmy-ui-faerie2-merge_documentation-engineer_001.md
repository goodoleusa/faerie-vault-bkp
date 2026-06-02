# The Operator Loop: Five Mid-Flight Directives Across Three Waves

**Date:** 2026-05-26
**Session:** swarmy-ui-faerie2-backend-merge — single continuous session
**Scope:** 19 sub-agents sealed across 4 waves + 1 inline crash-recovery; operator interventions absorbed without re-spawn
**Companion:** [`docs/RECEIPTS.md`](../../../../0local/gitrepos/swarmy-ui/docs/RECEIPTS.md) (Wave 1 receipts, updated through Wave 4) — this doc is the *narrative* of the session, the receipts are the *numbers*
**Predecessor pub:** `2026-05-26-stigmergic-coordination-wave1-empirics/` — Wave 1 in isolation

---

## TL;DR

A single continuous session took the `swarmy-ui` repo from "front-end JSX only, no backend" to "self-contained Hive with a hash-chained COC ledger, three-mode signing infrastructure including sigstore-keyless OIDC, full mission-graph DAG, OpenHands chat substrate, and an OSINT-equipped Prober worker role." Nineteen sub-agents sealed across four waves. **Five operator directives landed mid-flight** — each one re-scoping work that was already in progress. None of them broke the wave model, because the stigmergic substrate doesn't require synchronous coordination.

The interesting story is not the parallelism (the prior pub covered that). It's that **the operator kept editing the plan while the swarm was running, and the swarm absorbed the edits as new graph nodes rather than as interrupts.** This is what human-in-the-loop with autonomous agents actually looks like when the loop is fast and the substrate is filesystem-anchored.

---

## What got built

The session arc — from front-end-only JSX to a self-validating forensic substrate:

| Layer | Wave | Phases | What landed |
|---|---|---|---|
| **Coordination substrate** | 1 | 0–5 | Charter, manifest writer + finalizer, path adapter, vocab adapter (one-way), charter aggregator (self-applying), swarm_ticker SSE live wire, Activity Feed UI |
| **Vocabulary + runtime + glossary reconcile** | 2 | 6–8d | Crystallize tightened, citation grammar widened, e2e smoketest harness, OH chat substrate + security perimeter, OH↔UI iframe bridge, finalizer ticker publish hook, /charters UI live API |
| **Forensic substrate + OSINT** | 3 | 9a–9e | Full COC chain (1d-1i + genesis + protect-paths), merkle tree, rekor + sigstore signing (sidecar mode + offline-by-default), full upstream mission_graph.py (1619 lines, in-place glossary rename), glossary canonicalization sweep (legacy adapter inverted), SpiderFoot skill + data-ingest OSINT scripts + NEW Prober agent card with scope fence |
| **Vocabulary correction + sigstore keyless** | 4 prelude | 10a–10b | queue→frontier sweep (79 hits classified across 3 buckets), VOCAB-DECISIONS.md ledger inaugurated, sigstore-keyless implementation (OIDC + Fulcio + ephemeral keys + rekor inclusion proof + fail-closed identity allowlist) |

**Test surface at session end:** 171 pytest cases green, 2 skipped, 0 regressions. Three signing modes coexisting under env dispatch. Hash-linked COC chain with verified entries. Live SSE backend with vocab-translated UI render. Self-applying charter aggregator running in-repo against this very charter.

**Everything additive to the existing beekeeping UI.** Zero existing screens modified; the new surfaces (`/charters`, `chat-tab`, `activity-feed`, `manifest-feed`) all landed as new routes / footer strips alongside the existing apiary / hive / honey / journal / skep / swarm screens. The product mental model (Pollen / Ambrosia / Cap / Crystallize, 9 named worker roles, hive/comb/cell) is preserved verbatim; the new operator-layer vocabulary (compass / archetypes / RAP-adjacent / merkle / sigstore) lives in the engine room and never surfaces to users.

---

## The five mid-flight directives

This is the part worth recording. Each row is a directive the operator issued **after** the relevant wave had already spawned. Each one would have been a re-plan in a synchronous orchestration model. In the stigmergic model, each one became a graph node that the next wave (or in two cases, the current wave's still-in-flight agents) consumed.

| # | Directive (paraphrased) | Issued during | Absorbed via | Cost to absorb |
|---|---|---|---|---|
| 1 | "Focus on OpenHands as base runtime; Claude Code/SDK is a brokered tool call, not the primary loop" | Wave 1 (5 of 6 agents in flight) | `swarm/2026-05-26/BUNDLE-AMENDMENT.md` + charter `operator_decisions_locked[]` patch | ~1,800 tokens; in-flight agents did not see it (too late); Wave 2 inherited cleanly via the amendment file |
| 2 | "Must import the full faerie2 COC system, merkle tree rollups, rekor API calls" — reverses Wave 1's explicit punt of sigstore to a future charter | Wave 2 sealing | Re-scoped Wave 3 bundle Phase 9a + 9b before spawn | ~2K tokens of bundle re-write |
| 3 | "Import the mission graph while preferring swarmy-ui glossary terms as canonical" — inverts the vocab adapter from egress-only to legacy-fallback | Wave 2 sealing | Wave 3 Phase 9c (full mission_graph import) + Phase 9d (glossary canonicalization sweep + adapter inversion) | Folded into Wave 3 bundle; BRIDGE-W3 did the adapter inversion + adopted the "is_legacy_payload" / "isLegacyPayload" companion functions |
| 4 | "Import the SpiderFoot skill and agent card; begin fleshing out a Prober agent equipped with great OSINT tooling" | Wave 3 about to spawn | Added Phase 9e as the 5th Wave 3 lane (was 4); created the Prober agent card from scratch (no faerie2 analog) with explicit scope fence | One added agent + ~3K tokens of bundle extension |
| 5 | "NO QUEUE i hate the term — it's a forensic mission graph not a queue" | Wave 3 sealing | Wave 4 prelude Phase 10a (queue→frontier sweep, 79 hits classified, aggregator envelope patched) + inaugurated `docs/VOCAB-DECISIONS.md` as a running operator-decision ledger | One dedicated DEEP-DIVER agent |

Plus two operator follow-ups that were **questions** rather than directives — "what gates anyone from signing anything?" → triggered a defense-in-depth analysis; "implement sigstore keyless" → Phase 10b, the OIDC-anchored signing mode with ephemeral keys and fail-closed identity allowlist.

---

## How stigmergy absorbed the edits without breaking the model

Four absorption mechanisms emerged across the session:

### 1. Mid-wave amendments via durable filesystem artifacts

Directive 1 (OH runtime) landed AFTER Wave 1 spawned. In a synchronous model, this would require killing the wave and re-spawning. Instead: a new file at `swarm/2026-05-26/BUNDLE-AMENDMENT.md` recorded the directive + per-agent guidance + Wave-2 action items, and the charter's `operator_decisions_locked[]` array was patched in place. In-flight agents (already deep in their work) didn't see the amendment — that's fine. Wave 2 inherited it cleanly because their bundle pointed at it. **The amendment is a graph node, not an interrupt.**

### 2. Architectural reversals between waves

Directive 2 reversed a charter `out_of_scope` decision (Wave 1 explicitly punted sigstore to a future charter). In the synchronous model this is a re-plan that re-litigates the charter. Stigmergic answer: charter file gets edited, future wave's bundle references the edit, the charter aggregator picks up the new shape on next run. No re-litigation; the operator decision is just a new fact in the graph.

The same charter went through three sigstore postures in one session:
- Wave 1: "sigstore is out of scope, future charter"
- Wave 3: "import full sigstore + rekor + merkle right now" — three lanes shipped (9a + 9b)
- Wave 4: "add sigstore keyless mode as defense-in-depth" — `SWARMY_SIGNING_MODE` dispatcher with three coexisting modes

Each reversal landed as new graph nodes; none broke any prior work. The Phase 9b signer (local-key + sidecar) still passes its smoketest; the Phase 10b dispatcher wraps it without modification.

### 3. Out-of-order seal arrival doesn't break dependency chains

Wave 3's most striking timing: **MAKER-A-W3 (Phase 9b sigstore signer) and BRIDGE-W3 (Phase 9d glossary canonicalization sweep) BOTH sealed BEFORE DEEP-DIVER-W3 (Phase 9a COC + merkle).** The 9b signer was supposed to anchor against the COC chain's tip hash — but the COC chain didn't exist yet when 9b sealed. The 9d sweep was supposed to clean up imported terms — but most of 9a's imports hadn't landed.

Both downstream agents **assumed forward**, emitted `discovered_work[]` entries flagging the seam, and trusted the blackboard to converge. When 9a finally sealed, the `chain_tip_hash()` API it exposed matched the API 9b had stubbed against. When 9d's sweep re-ran (or would re-run in a future wave), the additional 9a-imported terms would be caught by the same classification discipline.

This is the inverse of synchronous orchestration. There is no DAG-walker waiting for upstreams. Each agent operates on the snapshot of the blackboard at its claim moment + emits forward-looking notes for whatever lands after.

### 4. Crash recovery via blackboard preservation

Phase 9e (Prober + SpiderFoot) had its sub-agent transcript truncated mid-flight by an API socket error after ~29 tool calls. In a synchronous model: lose the work, re-spawn from zero. Stigmergic answer: the substantive work had already landed on the filesystem (agent card, two skill imports with provenance headers, data.jsx Prober entry fully populated). Main agent completed the remaining ~3 items inline (docs/PROBER-AGENT.md, smoketest script, manifest seal) rather than re-spawning. The 26-check smoketest then ran green.

The Wave 1 pub identified stigmergic *convergence* (two agents producing the same artifact independently with no collision). Phase 9e demonstrated the inverse: stigmergic *recovery* across a crash boundary. The blackboard was the source of truth, not the agent's memory. One agent + main produced a complete artifact across a transcript boundary because the substantive work was filesystem-anchored when the transcript truncated.

---

## The operator-loop pattern, named

Across 19 sealed agents and ~6 hours wall, the operator interacted with the swarm in this pattern:

```
1. Operator names a goal               → Main writes a bundle + charter
2. Main spawns N agents                → Wave fires; agents work parallel
3. Operator reads completion summaries → Notices something to add, change, or correct
4. Operator issues a directive          → Drops back into conversational
5. Main patches the bundle/charter      → Edits a durable filesystem artifact
                                          (existing in-flight agents continue
                                          to their seal; new agents inherit
                                          the edit at their next claim)
6. Next wave incorporates the edit      → As if it were always part of the plan
```

This is a **continuous-loop** model, not a request/response one. The operator doesn't wait for the swarm to finish to give the next directive. The swarm doesn't wait for the operator to confirm before sealing. Both run independently; the filesystem is the meeting point.

**The cost of an operator directive is the cost of editing one file.** Not a re-plan. Not a coordination meeting. Not a Gantt chart update. A directive is the same kind of object as an agent's `discovered_work[]` entry — both are forward-looking notes that the next claim will absorb.

Five of these directives across one session, zero re-spawns, zero rework.

---

## The numbers (session totals)

These are the harness's own numbers reported in task-notification events at seal time. Each agent corresponds to one manifest at `swarm/2026-05-26/manifests/` — open any of them to cross-check.

### Per-wave summary

| Wave | Agents sealed | Total tokens (sum) | Serial wall | Parallel wall | Speedup |
|---|---:|---:|---:|---:|---:|
| 1 (Phases 0-5) | 6 | 630,964 | ~49 min | ~14m 21s | 3.41× |
| 2 (Phases 6-8d) | 6 | ~886,400 | ~64 min | ~13m 53s | 4.61× |
| 3 (Phases 9a-9e) | 5 (1 inline-recovered) | ~750,000 | ~62 min | ~14m 51s (Phase 9a critical-path) | 4.18× |
| 4 prelude (10a-10b) | 2 | ~292,400 | ~23 min | ~13m 29s (Phase 10b critical-path) | 1.71× (only 2 agents — bounded by max) |
| **Total** | **19** | **~2,560,000 tokens** | **~3h 18m** *(serial)* | **~57 min** *(sum of parallel waves)* | **~3.5× sustained** |

### Test surface growth

| Wave | Pytest cases green | Smoketests | Notable proof |
|---|---:|---:|---|
| End of W1 | 42 | 2 | Vocab adapter end-to-end live SSE round-trip |
| End of W2 | 96 | 5 | E2E smoketest exit 0; OH chat substrate; aggregator self-apply |
| End of W3 | 147 | 7 | Hash-linked COC chain verified; full mission_graph imported; Prober equipped |
| End of W4 prelude | 171 | 8 | Three signing modes; sigstore keyless with fail-closed allowlist; queue→frontier swept |

### Rework and re-spawns

- Re-spawns: **0**
- Rework: **0** (zero agent reported a failure or asked for clarification)
- Charter edits: **3** (operator_decisions_locked appended, Phase 6/7/8/9/10 sequence accreted, scope reversed twice on sigstore)
- Inline crash-recoveries: **1** (Phase 9e Prober — sub-agent transcript truncated mid-flight; main completed inline)
- Stigmergic divergences surfaced + resolved: **3** (NAVIGATOR-W1 said `_charter_term_index_lib.py` was in archive/, MAKER-B-W1 found it missing — downstream truth won; MAKER-C-W2 found `agent_archetype` vs `archetype` field-name mismatch, fixed at egress with 5 lines; MAKER-A-W3 sealed before its COC dependency, stubbed forward)
- Discovered_work entries seeded (cumulative across all waves): **~55+**

### Coordination overhead ratio (across the session)

- Bundles (3 of them): ~10K tokens
- Mid-wave amendments: ~2K tokens
- Charter file + edits: ~10K tokens
- Vocab-decisions ledger: ~1K tokens
- Total shared state: ~23K tokens
- Total work: ~2.56M tokens
- **Coordination overhead: 0.90%** (down from Wave 1's 1.82%; the bundle cost continued to NOT scale with work volume — the load-bearing property held across 3.6× more work)

---

## What the session demonstrates beyond the prior Wave 1 pub

The Wave 1 pub made three claims about stigmergy:
1. The 3.41× parallelism speedup is real but bounded by the slowest agent
2. The 1.82% coordination overhead is the load-bearing number, not the speedup
3. Loose coupling absorbed mid-flight seam mismatches with minimum-invasive interventions

This session extended each:

**1. The speedup ratio stabilizes.** Across W1+W2+W3+W4-prelude, the sustained speedup is ~3.5×. The Wave 4 prelude's 1.71× pulls the average down because two agents = max bounded by one + sequential setup; W2's 4.61× was the high (less variance). The pattern is robust across wave compositions.

**2. The coordination overhead ratio dropped further.** 2.5% (5/6 W1) → 1.82% (6/6 W1) → 0.90% (session-cumulative). **The denominator grew 3.6× while the numerator stayed nearly flat.** This is the load-bearing property of stigmergy as a discipline. The bundle cost is paid once per wave; the work absorbs many wave's worth of value from the same shared state.

**3. The loose-coupling absorption pattern generalized to operator directives.** Wave 1 demonstrated it for inter-agent seams (vocab field-name mismatch absorbed at the egress gate). This session demonstrated it for operator directives (architectural reversals, vocabulary corrections, scope expansions) absorbed as new graph nodes rather than interrupts. **The same property — minimum-invasive intervention at the point of mismatch — works for human-issued edits, not just agent-discovered ones.**

---

## One conclusion, sharper than the numbers

> The operator does not need to wait for the swarm to finish before steering it. The swarm does not need to wait for the operator to confirm before sealing. Both run independently. The filesystem is the meeting point. The cost of a directive is the cost of editing one file.

The earlier pub's thesis was: *"The number that matters is not the speedup. It is the 1.82% coordination overhead. And the reason it matters is that it did not grow when the wave did."*

This session's extension: **The reason it does not grow is because the substrate is the same shape for operator edits as it is for agent emissions.** A directive is a `discovered_work[]` entry the human writes. A charter amendment is a manifest the human commits. A vocabulary correction is a sweep the human authorizes. There is no separate "human channel" vs "agent channel" — both flow through filesystem-anchored, hash-linkable, forensically-preserved artifacts.

That's why five operator directives across one session produced zero re-spawns. The swarm wasn't being interrupted; it was being **fed**.

---

## Reproducibility

All artifacts at versioned paths in `swarmy-ui:dev`:

- **All 28 sealed manifests** (19 agent seals + 9 in_progress claim records superseded by their seals): `swarm/2026-05-26/manifests/`
- **All ambrosia** (in-flight notes): `swarm/2026-05-26/ambrosia/{agent}-{wN}/`
- **Three wave bundles:** `swarm/bundles/2026-05-26_blackboard-bundle.md` (W1), `2026-05-26_wave2-bundle.md` (W2), `2026-05-26_wave3-bundle.md` (W3); Wave 4 prelude was specced inline per-agent
- **Mid-wave amendment:** `swarm/2026-05-26/BUNDLE-AMENDMENT.md`
- **Charter:** `forensics/charters/active/2026-05-26Z__charter__swarmy-ui-faerie2-backend-merge__goodoleusa.json`
- **Derived (aggregator-computed) charter:** `forensics/charters/active/2026-05-26Z__charter__swarmy-ui-faerie2-backend-merge__goodoleusa.derived.json`
- **Hash-linked COC chain:** `swarm/coc.jsonl`
- **VOCAB-DECISIONS.md ledger:** `docs/VOCAB-DECISIONS.md`
- **RECEIPTS:** `docs/RECEIPTS.md` + `docs/RECEIPTS.json` (machine-readable)
- **Pinned source SHA:** `e27389d74ec34931a6e4d9b0d31041511ade48cf` (faerie2) — `docs/MERGE-SOURCE.md`

To verify the session-end test surface:

```bash
python3 -m pytest server/tests/ -v
# Expected: 171 passed, 2 skipped

python3 server/scripts/4x_charter_aggregator.py --verbose \
  --charter-id swarmy-ui-faerie2-backend-merge
# Expected: rollup=uncapped, envelope={capped:0, uncapped:1, frontier:0}

python3 server/scripts/_smoketest_phase10b.py
# Expected: all 3 signing modes pass (disabled / local-key / keyless)

python3 server/scripts/9x_coc_verifier_via_chain.py  # or equivalent
# Expected: chain valid end-to-end
```

---

## Postscript: the role of the doc-engineer

This publication exists because the prior Wave 1 pub established that the *numbers* are reproducible by opening manifests. This pub is the *narrative* layer the numbers can't carry alone — what got built, what got reversed, what got named for the first time (the operator-loop pattern), what the session means beyond its own metrics.

The blackboard preserves the work. The receipts preserve the numbers. The vault publications preserve the meaning. Three layers; one mission graph.
