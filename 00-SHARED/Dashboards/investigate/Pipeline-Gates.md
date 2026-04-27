---
cssclasses: [wide-page]
type: dashboard
stage: investigate
status: active
created: 2026-03-25
tags: [dashboard, pipeline, gates, scientific-rigor]
parent:
  - "[[HOME]]"
sibling:
  - "[[Phase1-AgentSync]]"
  - "[[Hypothesis-Tracker]]"
  - "[[Data-Ingest-Pipeline]]"
doc_hash: sha256:b29c36260486c6165b15cb4664372478f9985fd71ccbacf7e69b308bd1955376
hash_ts: 2026-03-29T16:10:00Z
hash_method: body-sha256-v1
---

> [!nav]
> [[HOME|← HOME]] · [[Phase1-AgentSync|← Command Center]] · [[Hypothesis-Tracker|← Hypotheses]] · **Pipeline Gates** · [[Data-Ingest-Pipeline|Pipeline →]]

# Pipeline Gates

> Human checkpoints in the `/data-ingest` progressive disclosure pipeline.
> Gates prevent runaway inference and enable course correction without coaching.

---

## Gate Status

| Gate | Phase Transition | Purpose | Status |
|------|-----------------|---------|--------|
| **1** | SEED (15%) -> DEEPEN (50%) | Review first impressions. Seal private hypotheses. Correct factual errors. | `pending` |
| **2** | DEEPEN -> EXTEND (75%) | Hypothesis evolution check. Flag incorrect factual premises. | `pending` |
| **3** | EXTEND -> FULL (100%) | Convergence review. Add raw data if needed. Request red-team. | `pending` |
| **4** | FULL -> PUBLISH | Unseal hypotheses. Compare agent vs human. Final review. | `pending` |

> Update this table from: `python3 scripts/gate_pass.py status`

---

## Hypothesis Pre-Registration

| Aspect | Status |
|--------|--------|
| **Agent hypotheses** | `scripts/audit_results/hypothesis_registry.json` (committed) |
| **Human hypotheses** | Sealed (hash committed, content local until GATE 4) |
| **Seal status** | `python3 scripts/hypothesis_seal.py status` |

### The Sealed Envelope Protocol

1. After SEED run: you see agent's first impressions in the vault
2. You write your own hypotheses privately (`human_hypotheses_sealed.json`)
3. `hypothesis_seal.py seal` — commits SHA-256 hash, NOT the content
4. Analysis proceeds through DEEPEN -> EXTEND -> FULL
5. At GATE 4: `hypothesis_seal.py reveal` — commits the content, verifies hash match
6. **Court value:** Git timestamp of seal PRECEDES full analysis. Hash proves no tampering.

---

## Corrections Log

Human corrections at gates are constrained to prevent coaching:

| Allowed | Not Allowed |
|---------|-------------|
| Factual corrections ("that IP is a CDN") | Steering conclusions ("look for evidence of X") |
| Scope clarifications ("data covers 2024 only") | Changing hypotheses after seeing results |
| Data quality flags ("these rows are duplicates") | Excluding contradicting data |
| Stop/redirect ("known false positive") | Adding case data to agent training |

Corrections are validated by `gate_pass.py` schema — coaching language is rejected.

> View corrections: `python3 scripts/gate_pass.py status`

---

## How Gates Integrate

```
/data-ingest (SEED run)
  └─ Agents write FIRST_IMPRESSION blocks
  └─ vault_narrative_sync.py syncs to vault
  └─ GATE 1 ← human reviews in Obsidian
       ├─ Correct factual errors: gate_pass.py correct 1
       ├─ Seal hypotheses: hypothesis_seal.py seal
       └─ Approve: gate_pass.py pass 1

/data-ingest (DEEPEN run)
  └─ Agents read GATE 1 corrections as data input
  └─ Hypothesis evolution documented
  └─ GATE 2 ← human reviews changes
       └─ Approve: gate_pass.py pass 2

... (EXTEND, FULL)

/data-ingest (PUBLISH)
  └─ GATE 4: hypothesis_seal.py reveal
  └─ Agent vs Human hypothesis comparison generated
  └─ Agreement = independent convergence (strong validation)
  └─ Disagreement = documented (valuable finding)
```

---

*← [[HOME]] . [[Session-Manifests]] . [[session-briefs/LATEST-brief|Latest Brief]]*
