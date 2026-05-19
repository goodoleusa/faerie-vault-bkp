---
type: retention-policy
applies_to: "00-SHARED/Weekly/"
tags: [retention, crystallization]
---

# Retention — Weekly

**Tier:** mid (30d–90d).

- **Source:** condensed from `00-SHARED/Daily/{YYYY-MM-DD}/` after ~30 days
  of age via the planned `scripts/dev/vault/11-weekly-digest.py` (task #40).
- **Lifespan:** indefinite, but rolled into `00-SHARED/Monthly/` at ~90 days.
- **Forensic chain:** retired Daily entries get `superseded_by:` pointers
  back to `forensics/ephemeral/{date}/{task_id}/` — nothing deleted.
- **Read order:** start at Anchors → drill to Monthly → Weekly → Daily.
