---
type: retention-policy
applies_to: "00-SHARED/COC-Entries/"
tags: [retention, coc, canonical, permanent]
---

# Retention — COC entries

**Tier: PERMANENT (immutable, append-only, hash-chained).**

- **Source:** written by `0a_coc-core.append_coc_entry()` via the
  promotion hook (`0f_promote-to-forensics.py`).
- **Lifespan:** permanent. Mirrors `faerie2/forensics/coc.jsonl` — the
  hash-chained spine of the entire system.
- **Mutation:** impossible by design. Every entry carries
  `prev_entry_hash`; any tampering breaks the chain and is detected by
  `coc-verify`.
- **Backup:** B2 WORM bucket on every write.
