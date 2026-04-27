---
type: agent-delivery
status: awaiting-human
created: 2026-03-30
updated: 2026-03-30
tags: [osint, evidence, agent-draft]
evidence_id: ""
source_file: scripts/audit_results/ahmn_co_research_RUN010.json
source_sha256: ""
local_path: /mnt/d/0local/gitrepos/cybertemplate/scripts/audit_results/ahmn_co_research_RUN010.json
git_commit: ""
source_type: agent-research
confidence_level: 0.00
source_quality: unverified
hypothesis_support: []
tier:
pipeline_run: RUN010
date_collected: 2026-03-30
date_analyzed: 2026-03-30
parent:
  - "[[00-SHARED/Agent-Outbox/criticalexposure]]"
sibling:
  -
child:
  -
memory_lane: inbox
promotion_state: capture
vault_path: 00-SHARED/Agent-Outbox/criticalexposure/ahmn_co_research_RUN010.md
faerie_session: ""
blueprint: "[[Evidence-Item.blueprint]]"
# --- chain (agent writes at creation — do not edit) ---
chain_id: "criticalexposure"
chain_seq: 0
prev_hash: ""
agent_hash: ""
agent_author: ""
agent_signed: ""
# --- researcher signature (optional — sign when reviewing) ---
sig: ""
sig_fp: ""
sig_ts: ""
sig_hw: false
# --- annotation commit (fill when done annotating) ---
ann_hash: ""
ann_ts: ""
doc_hash: sha256:f7481b752113aff9731fa08c295fbdcfa3ec1f2055cf6fb4797ae03a925b6a6d
hash_ts: 2026-03-30T01:29:05.881165+00:00
hash_method: body-sha256-v1
agent_type: data-engineer
---

# ahmn_co_research_RUN010

## Summary
<!-- One paragraph: what is this evidence, what does it show -->

## Provenance
| Field | Value |
|-------|-------|
| **Source File** | `scripts/audit_results/ahmn_co_research_RUN010.json` |
| **SHA-256** | `f7481b752113aff9731fa08c295fbdcfa3ec1f2055cf6fb4797ae03a925b6a6d` |
| **Collection Date** | 2026-03-30 |
| **Collector** | research-analyst |
| **Pipeline Run** | RUN010 |
| **Git Commit** | `pending` |

## Content
**Run ID:** RUN010
**Phase:** OSINT_RESEARCH
**Agent:** research-analyst
**Timestamp:** 2026-03-22T18:00:00Z

### Subject
- **Domain:** ahmn.co
- **Ip:** 172.93.110.120
- **Asn:** AS23470
- **Isp:** ReliableSite.Net

### Verdict
**Summary:** ahmn.co is operated by the same Packetware entity, not an unrelated new tenant. 172.93.110.120 has been decommissioned as a container registry and is now an SSH-only server on AS23470 (ReliableSite).
**Confidence:** 0.78
**Operator:** Packetware
**H2 Impact:** SUPPORTED — ahmn.co is Packetware-operated infrastructure, extending the infrastructure map
**H4 Impact:** NEUTRAL — confirms Packetware operator continuity; IP is US-based (ReliableSite, AS23470)

### Evidence (6 items)

**1. dns_verification_txt**
- Finding: anchored.host TXT: packetware-verification=ohtwzMJP9Agyqa17ZYJy6hu1JsVm5QionojE0wipVg0iE5MPcy
- Significance: Packetware-issued domain ownership proof on anchored.host

**2. dns_cname**
- Finding: anchored.host CNAME -> packetware.net
- Significance: Direct domain alias confirms same operator

**3. shared_ip**
- Finding: Both ahmn.co and anchored.host resolve to 65.108.96.185 (Hetzner Helsinki, AS24940)
- Significance: Same Cloudflare account controls both domains (identical NS pair: natasha/ruben.ns.cloudflare.com)

**4. internal_db**
- Finding: 172.93.110.120 in Packetware Prisma IPv4Address table: status=ASSIGNED, type=FIXED
- Significance: IP was actively managed as a fixed assignment in Packetware's internal database

**5. shodan_monitor**
- Finding: 172.93.110.120 March 2026: port 22 (SSH) only, 15 banner_update events (Mar 3-12 2026). No mail ports (25/465/587/993).
- Significance: Decommissioned container registry; mail.ahmn.co PTR is a hostname label only

**6. raindrop_bookmark**
- Finding: registry2.anchored.host on 172.93.110.120, ASN 23470 (ReliableSite) — separate from primary Packetware AS400495 block
- Significance: Packetware used ReliableSite dedicated server for container registry; main compute was AS400495 Frankfurt

## Analysis
<!-- What does this evidence mean in context? Hypothesis connection. -->

## Hypothesis Relevance
| Hypothesis | Supports/Contradicts | Strength | Notes |
|-----------|---------------------|----------|-------|
| H1 - Insider | | | |
| H2 - Pipeline | | | |
| H3 - Breach | | | |
| H4 - Handoff | | | |
| H5 - Payoff | | | |

## Open Questions
- [ ]

## For the human (async)
- [ ] Read and acknowledged
- [ ] Tier decision: (1 / 2 / 3 — add one line)
- [ ] Promote to 30-Evidence: (yes / needs more work / reject)

**Human notes (append-only below this line):**

## For the next agent run
- `status: awaiting-human` — do not spawn subagents until human acknowledges
- If promoting: change `type` → `evidence`, `status` → `reviewed`, `promotion_state` → `promoted`
- Apply `Evidence-Item.blueprint` in Obsidian after promotion to add review sections
