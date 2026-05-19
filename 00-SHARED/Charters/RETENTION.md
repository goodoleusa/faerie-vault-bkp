---
type: retention-policy
applies_to: "00-SHARED/Charters/"
tags: [retention, charters, permanent]
---

# Retention — Charters

**Tier: PERMANENT.**

- **Source:** mirrored from `faerie2/forensics/charters/{YYYY-MM-DD}/{charter_id}.md`
  (the system of record).
- **Lifespan:** permanent. Charters are first-class declared intent and the
  cornerstone every manifest references.
- **Retirement:** by flipping `status:` to `retired` (and adding
  `superseded_by:` if applicable). Never delete a charter — the COC chain
  depends on charter_ref resolvability.
