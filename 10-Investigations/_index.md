---
type: index
tags: [meta, index]
doc_hash: sha256:e61027f8f8b89a452c2a5a3bbaea10250077a557a72b766034b556e575d9d0be
hash_ts: 2026-03-29T16:10:51Z
hash_method: body-sha256-v1
---

# 10-Investigations — Active Cases

Investigation case files tracking hypothesis-driven research. Each case uses [[Investigation-Case.blueprint]].

## Domains
- **Cults & High-Control Groups** — Organizational structure, recruitment, financial networks
- **Money Laundering** — Transaction chains, shell companies, crypto flows
- **Human Trafficking** — Networks, routes, front organizations
- **Shadow State Policy** — Renegade operations, off-book programs, policy contradictions
- **Cyber Infrastructure** — DOGE access, Treasury breaches, foreign actor connections

## Active Cases
```dataview
TABLE status, threat_level, hypothesis_focus, last_update
FROM "10-Investigations"
WHERE status = "active"
SORT threat_level ASC, last_update DESC
```

## By Domain
```dataview
TABLE length(rows) AS "Cases"
FROM "10-Investigations"
GROUP BY investigation_domain
```
