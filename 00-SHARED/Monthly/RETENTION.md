---
type: retention-policy
applies_to: "00-SHARED/Monthly/"
tags: [retention, crystallization]
---

# Retention — Monthly

**Tier:** deep (90d–1y).

- **Source:** condensed from `00-SHARED/Weekly/{YYYY-Www}/` after ~90 days
  via the planned `scripts/dev/vault/12-monthly-digest.py` (task #40).
- **Lifespan:** indefinite. Principles that hold continuously for one full
  year are eligible for promotion to `00-SHARED/Anchors/`.
- **Forensic chain:** retired Weekly entries leave `superseded_by:` pointers;
  original ephemera remain queryable.
