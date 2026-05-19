---
type: retention-policy
applies_to: "00-SHARED/Honey/"
tags: [retention, crystallization, honey]
---

# Retention — Honey

**Tier:** crystallized (canonical-on-write).

- **Source:** written by `scripts/dev/vault/10-crystallize.py` (task #39) when
  sibling manifests at the same address prefix get merged. Mirrors
  `faerie2/forensics/honey/{date}/{slug}.md`.
- **Lifespan:** indefinite. Each droplet is canonical from the moment it
  lands here — no further refinement.
- **Forensic chain:** the surviving manifest stays in `forensics/artifacts/`;
  merged siblings live in `forensics/ephemeral/` with `superseded_by:` pointers
  back to the droplet.
