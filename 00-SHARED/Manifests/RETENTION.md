---
type: retention-policy
applies_to: "00-SHARED/Manifests/"
tags: [retention, manifests, canonical]
---

# Retention — Manifests

**Tier:** canonical (promotion-only, write-protected).

- **Source:** promoted from `00-SHARED/Ephemeral/{date}/{task_id}/` via
  `0f_promote-to-forensics.py`. Pure symlink overlay.
- **Lifespan:** matches Ephemeral original. Hash-chained in `coc.jsonl`.
- **Mutation:** none. To modify, write a new manifest with
  `superseded_by:` link; the old one stays.
