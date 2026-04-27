# Data Analysis Engine — Collaborator Seed (HONEY)

Crystallized context for macOS/Linux collaborators. Install via: `python3 scripts/setup-collab.py`

---

## What DAE Is (2 lines)

**Data Analysis Engine** — forensic evidence pipeline. Ingest raw data (XLSX, CSV, PDF, JSON, MHTML, images) → apply statistical rigor + chain of custody → produce tiered evidence for publication. Topic-agnostic: swap `docs/Index.md`, `docs/Glossary.md`, `docs/gaps.md` for any investigation domain.

---

## Quick Start — Two Paths

| Path | When | Command |
|------|------|---------|
| **Standalone** | Debug, batch, scripted | `python scripts/0a-coc-genesis-ledger.py --run-id RUN-NNN` → `lib/trail_reader.py --resume` |
| **Faerie** | Full investigation, multi-session | `claude` → `/data-ingest` (spawns agent team) |

Both read the same manifests — switch anytime. See `docs/STANDALONE-VS-FAERIE.md` for details.

---

## Pipeline (7 Stages)

| Stage | Purpose | Key output |
|-------|---------|-----------|
| **0a** | Genesis + COC baseline | `genesis_manifest.json` (immutable proof) |
| **2a–2f** | Ingest raw data → JSON with hashes | `evidence_manifest.json` + `rawdata_manifest.json` |
| **3a–3d** | Deduplicate, normalize, 4-tier winnow | `tier1_smoking_gun.json` (≤15 items, 3-source) |
| **4a–4b** | PGP-sign manifests, run-level COC | `SIGNED-*.asc`, `run-manifest.json` |
| **5a** | Deploy to clearweb + IPFS + Bitcoin | Site files, IPFS CID, `.ots` proofs |
| **6a** | Archive to B2 WORM or git | Archive manifest |

**Trail protocol:** Every stage writes a manifest. `lib/trail_reader.py RUN-NNN` shows what's done, what's pending, exact next command. No human relay needed.

---

## Run Status

- **RUN-001 through RUN-008:** Complete, published to IPFS
- **RUN-009+:** Pending
- **Check anytime:** `python lib/trail_reader.py RUN-001`

---

## Active Data Gaps (High Priority)

| Gap | Hypothesis | Status |
|-----|-----------|--------|
| **H2 — Prometheus** | Exfiltration pipeline (network flows) | Not yet extracted |
| **H3 — SATODS Bloomberg** | Federal systems (Treasury, NNSA, Air Force) | TLS cert DB pending |
| **H4 — Treasury + USPTO TLS** | Foreign actor proximity (cert rotation) | PDF extraction pending |

---

## Non-Negotiable Rules

- **Append-only:** Never overwrite `evidence_manifest.json`, `genesis_manifest.json`, `hash_manifest*.json` — version-named outputs only
- **Hash before/after:** Every pipeline write requires SHA-256 before + after + FSL entry
- **FSL entries:** Forensic Script Log entry in `audit-log.md` BEFORE any write
- **Tier 1 cap:** Max 15 smoking gun items per run (requires 3-source corroboration)
- **Git commits:** Commit after each stage completes

---

## Critical Issue: F-1 (Hash Verification Mismatch)

**Severity:** BLOCKER — COC verification disabled until fix deployed

**What:** Hash computation differs between producer (stages 2–3) and verifier (`verify_coc.py`). False failures when verifying RUN-001 to RUN-008.

**Workaround:** Manual spot-check of 10 tier 1 files sufficient for publication while F-1 open.

**Fix target:** After RUN-009 baseline.

---

## Key Scripts & Commands

| Script | Purpose |
|--------|---------|
| `lib/trail_reader.py RUN-NNN` | Status + next stage + bash snippet |
| `lib/trail_reader.py RUN-NNN --resume` | Pipe to bash; auto-advance pipeline |
| `scripts/2b-hash-guardian.py` | Compute SHA-256 for all files |
| `scripts/gemini_extract_tables.py` | Vision extraction (Gemini 2.0 Flash) |
| `scripts/verify_coc.py` | COC verification (DO NOT run on RUN-001 to RUN-008 yet) |
| `scripts/coc.py` | COC utilities + export |
| `/data-ingest` (faerie skill) | Spawns agent team for full pipeline |

---

## Evidence Tiers (Publication Model)

- **Tier 1:** Smoking gun — direct proof, 3+ sources, court-admissible, SHA-256 anchored (≤15 items)
- **Tier 2:** Strong support — 2+ sources, clear hypothesis connection
- **Tier 3:** Contextual — background, timeline, infrastructure (cannot stand alone)
- **Tier 4:** Raw catalog — complete inventory, unverified, archive purposes

All tiers output as JSON with full provenance (source file, extraction method, hash chain).

---

## Environment (macOS/Linux)

- No WSL complications — all paths are native Unix
- Python 3.10+ (3.13 recommended for openpyxl compatibility)
- All scripts use `REPO_ROOT`-relative paths
- Settings: `~/.config/Claude/settings.json` (Linux) or `~/Library/Application Support/Claude/settings.json` (macOS)

---

## Customization Points (For New Investigation)

Edit these to adapt DAE for your domain:

- `docs/Index.md` — hypothesis definitions (H1–H5, what's relevant)
- `docs/Glossary.md` — terminology + keywords for your domain
- `docs/gaps.md` — gap analysis + collection priorities

Then run `python scripts/0a-coc-genesis-ledger.py --run-id RUN-001` to begin.

---

## Documentation Map

- **ARCHITECTURE.md** — full seven-stage blueprint + coordination protocol
- **README.md** — quick start + philosophy
- **docs/STANDALONE-VS-FAERIE.md** — when to use each mode (5 scenarios)
- **docs/GUIDE.md** — step-by-step walkthrough
- **.claude/LAUNCH.md** — entry map + skills registry

---

## Memory Flow (Cross-Session)

Standalone: You manage state via manifests (read `lib/trail_reader.py` at session start).

Faerie: Automatic — session 1 findings → scratch → NECTAR.md → session 2 HONEY seed.

**HONEY.md is read at every faerie session start.** Keep it ≤200 lines — this file is it.
