---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: orchestrator
ts: 2026-03-23T00:45:01Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:761dc6298e2515059ae913612bbb90bcea60121b05f48c335e5addc391b0f034
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:46Z
hash_method: body-sha256-v1
---

# New H2 entity: Inventry.ai LoopBack API at 182.30.152.122:3000 — /anonymous/login endpoint

API server for Inventry.ai (government inventory management system). Shodan title: "Rest APIs for Inventry.ai".
LoopBack v1.0.0 application. Server: http://182.30.152.122:3000. OpenAPI at /openapi.json.
Critical API paths: /anonymous/login, /admin/*, /agent-sessions/chat, /ai-agents, /ai-providers.
Schemas: Tour, SkuAttachment, AgentHistory, AgentSession — AI backend integrated.
/anonymous/login endpoint is a significant security concern if this serves government systems.
Source: bloomberg_shortlist_extract_RUN009.json (captured 2025-02-04).
Next: WHOIS/ASN for 182.30.152.122. Is this inside any government IP range?

---
*Source: REVIEW-INBOX · Agent: orchestrator · 2026-03-23*
