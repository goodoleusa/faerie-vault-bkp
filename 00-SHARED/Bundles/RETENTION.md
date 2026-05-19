---
type: retention-policy
applies_to: "00-SHARED/Bundles/"
tags: [retention, bundles, canonical]
---

# Retention — Bundles

**Tier:** canonical (promotion-only, write-protected).

- **Source:** promoted from Ephemeral via `0f_promote-to-forensics.py`.
- **Lifespan:** matches Ephemeral; symlink overlay.
- **Use:** bundles are read by `/run`, spawn templates, and replay. They
  are the auditable record of what an agent was given at spawn time.
