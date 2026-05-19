---
type: retention-policy
applies_to: "00-SHARED/Artifacts/"
tags: [retention, artifacts, canonical]
---

# Retention — Artifacts

**Tier:** canonical (promotion-only, write-protected).

- **Source:** promoted from Ephemeral via `0f_promote-to-forensics.py`.
- **Lifespan:** matches Ephemeral originals; symlink overlay.
- **Mutation:** none. Crystallization may write `superseded_by:` links
  onto the original payload in Ephemeral, but never edits Artifacts.
