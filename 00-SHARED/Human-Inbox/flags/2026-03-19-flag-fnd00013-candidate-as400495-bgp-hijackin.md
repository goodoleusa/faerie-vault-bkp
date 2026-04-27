---
type: agent-review-item
cat: FLAG
priority: HIGH
agent: research-analyst
ts: 2026-03-19T17:00:00Z
review_status: unreviewed
tags: [review, flag, human-inbox]
doc_hash: sha256:996623b6c4f17843166e682fbbaf8acd6fe0183c2c91ee5e9e794a2d7094a443
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:40Z
hash_method: body-sha256-v1
---

# fnd00013 candidate: AS400495 BGP hijacking of ARIN RESERVED block 63.141.38.0/24

AS400495 (Packetware) announces 63.141.38.0/24, ARIN RESERVED, RPKI no ROA. Block legitimately transferred to Continental Building Products Operating Company LLC (2017-03-20 ARIN transfer). BGP instability Aug 2025: peak ~136 announcements/hour Aug 4, 86 ann/day Aug 10-11 with 2 withdrawals/day = active BGP manipulation. Screenshots from BGPTools (Aug 29, 2025) show routing chart instability, ARIN RESERVED status, and transfer history.

Separate from fnd00009 (AS23470 registry). Recommend Tier 1 candidate fnd00013 (conf 0.90). High H2 support (infrastructure supply chain attack) + H4 support (foreign actor using stolen IP space).

Files: rawdata/Screenshots/Packetware Prisma Screenshots/packetware-bgp-hijacking-Screenshot 2025-08-29 015739.png, 015932.png, 020039.png
Next: Promote fnd00013; investigate ARIN dispute status; confirm current routing announcements

---
*Source: REVIEW-INBOX · Agent: research-analyst · 2026-03-19*
