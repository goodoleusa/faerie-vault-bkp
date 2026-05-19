---
type: retention-policy
applies_to: "00-SHARED/Ephemeral/"
tags: [retention, ephemeral, promotion-pipeline]
---

# Retention — Ephemeral

**Tier:** scratch (write-free, promotion-source).

- **Source:** agent writes during execution. Mirrors
  `faerie2/forensics/ephemeral/{date}/{task_id}/`.
- **Lifespan:** indefinite. Originals remain here forever; canonical
  Manifests/Artifacts/Bundles dirs are symlink overlays pointing back.
- **Promotion:** `scripts/0f_promote-to-forensics.py` on PostToolUse[Write],
  STOP, and SESSION_END.
- **Daily/ vs Ephemeral/:** `Daily/{date}/` is the *human-readable* mirror
  (full NSEW frontmatter, canvas). `Ephemeral/{date}/` is the *forensic*
  mirror (raw artifact payloads, by task_id).
