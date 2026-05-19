---
type: retention-policy
applies_to: "00-SHARED/Anchors/"
tags: [retention, crystallization, permanent]
---

# Retention — Anchors

**Tier: PERMANENT.**

- **Source:** principles that survived 1 year of continuous Monthly digests;
  promoted via `scripts/dev/vault/13-annual-anchor.py` (task #40).
- **Lifespan:** permanent. Anchors are the selvage — load-bearing principles
  the system rests on.
- **Retirement:** only via an explicit charter that proposes the new shape.
  The retired anchor stays in-place with `status: retired` and `superseded_by:`
  link; it is **never** deleted.
- **Question discipline:** challenge an anchor only via W-bearing (baseline
  re-seating) work.
