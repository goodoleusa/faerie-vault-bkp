---
type: dashboard
tier: workflow
title: "Publishing Workflow — Draft → Sign-Off"
status: live
cssclasses: [wide-page, dashboard-workflow]
refresh_cadence: per-publication
S: ['[[06-Publication-Worthy-Insights]]']
N: ['[[00-Home]]']
E: ['[[02-Missions-Emergent]]', '[[03-Anchors]]']
tags: [dashboard, publishing, workflow, signoff, swarmy]
---

> **🐝 Navigate:** [[00-Home]] · [[01-Today]] · [[02-Missions-Emergent]] · [[03-Anchors]] · [[04-Eval-Dimensions]] · [[05-Stigmergy]] · [[06-Publication-Worthy-Insights|6 Insights]] · **[[07-Publishing-Workflow|7 Publishing]]**

# Publishing Workflow

Your part of publishing — writing, editing, fact-checking, signing off. The
swarm produces drafts; you do the journalism. This dashboard tracks each
publication through its lifecycle and surfaces what needs your hand right now.

---

## 🎯 The pipeline (4 phases per publication)

```
DRAFT  ────►  EDIT  ────►  FACT-CHECK  ────►  SIGN-OFF
[claim]      [shape]       [verify]            [seal]
```

1. **DRAFT** — exists somewhere (agent wrote it, or you sketched, or imported). Lives in `inspiration/` (repo) or `00-Publications/_drafts/` (vault).
2. **EDIT** — language tightened, structure reviewed, claims clarified. Status moves to `editing`.
3. **FACT-CHECK** — every citation verified against forensic record (COC entry hashes, manifest sha256s, file paths). Status moves to `fact-checked`.
4. **SIGN-OFF** — signed via `9x_agent_sign.py` (or `swarmy_sign_artifact` MCP tool) with your author keypair. Status moves to `published`.

Each phase has its own working table below. Click into a publication's link to do the next step.

---

## 📝 Drafts (need your attention)

Publications without `status: published` or `status: editing`:

```dataview
TABLE
  default(title, file.name) AS "Title",
  default(status, "draft") AS "Status",
  default(file.mtime, "—") AS "Last Touched"
FROM "00-Publications"
WHERE !contains(status, "published") AND !contains(status, "editing")
SORT file.mtime DESC
LIMIT 15
```

**Triage actions:**
- Looks good as-is → move to **Editing** (set frontmatter `status: editing`)
- Needs deep rework → keep in `draft` + add `needs_rework: <reason>` to frontmatter
- Not publication-worthy → move to `inspiration/_archive/`
- Already published elsewhere → set `status: published` + add `external_link`

---

## ✂️ In editing (your active queue)

Publications in active editing:

```dataview
TABLE
  default(title, file.name) AS "Title",
  default(editor, "—") AS "Editor",
  default(edit_started, "—") AS "Started"
FROM "00-Publications"
WHERE status = "editing"
SORT default(edit_started, file.mtime) DESC
```

**Per-publication editing checklist:**
- [ ] Title sells the read in <8 words
- [ ] First paragraph passes the cold-reader orientation test (60s comprehension)
- [ ] Every claim has a citation (file:line, sha256, command output, OR explicit "my interpretation")
- [ ] Prose flows; no bullet-list-as-synthesis sections
- [ ] Companion publications linked in frontmatter `companions: [...]`
- [ ] Charter lineage declared (`charter_lineage: <charter_id> → <observation>`)
- [ ] Length is right (the user, not a word count, decides)

---

## 🔍 Fact-checking (verification phase)

Publications claiming forensic-grade truth need every citation verified:

```dataview
TABLE
  default(title, file.name) AS "Title",
  default(fact_check_status, "pending") AS "Check Status",
  default(claims_verified, 0) AS "Verified",
  default(claims_total, "?") AS "Total"
FROM "00-Publications"
WHERE status = "fact-checking"
```

**Verification ritual:**
1. Open the publication's `inspiration/` mirror (in repo)
2. For each numerical claim (e.g., "13 keypairs", "82 MCP tools", "1898 char rationale"):
   - Run the cited command verbatim
   - Confirm the number matches
   - Update if drifted (or add `as_of: <date>` qualifier)
3. For each cited path (e.g., `forensics/charters/active/X.json`):
   - Verify the file exists at that path
   - Verify it has the claimed content (use `sha256sum` if claim is hash-anchored)
4. For each cited agent quote (e.g., the goodbye rationale):
   - Locate the manifest sha256
   - Read the `completion_choice.rationale` field
   - Confirm verbatim
5. When all green: `status: fact-checked` + `claims_verified == claims_total`

---

## ✅ Sign-off (your final commitment)

Publications ready for signature:

```dataview
TABLE
  default(title, file.name) AS "Title",
  default(signed_by, "UNSIGNED") AS "Signed By",
  default(signed_at, "—") AS "Signed At"
FROM "00-Publications"
WHERE status = "fact-checked" OR contains(signed_by, "ed25519")
```

**Sign-off process:**

```bash
# Via canonical CLI:
python3 /mnt/d/0local/gitrepos/faerie2/scripts/9x_agent_sign.py sign \
  <your-author-keypair> \
  /mnt/d/0LOCAL/gitrepos/faerie-vault/00-Publications/<file>.md

# OR via MCP tool (from inside the swarmy-hive-plugin chat panel):
swarmy_sign_artifact(artifact_path="00-Publications/<file>.md", agent_type="goodoleusa")
```

After sign-off:
- `signed_by: "ed25519:..."` in frontmatter
- `signed_at: <ISO timestamp>`
- `status: published`
- COC entry appended automatically
- Repo `inspiration/` mirror updated with the signed version

---

## 🌐 External publishing (optional)

After local sign-off, you may want external distribution:

| Channel | How |
|---|---|
| GitHub Pages | Push `00-Publications/` to a `gh-pages` branch |
| Substack / blog | Copy-paste md → platform's editor; preserve frontmatter as separate metadata |
| Sigstore Rekor (public attestation) | `cosign sign-blob` the file; record the Rekor UUID in frontmatter `rekor_uuid` |
| IPFS (immutable URL) | `ipfs add` the file; pin to a service; record CID in frontmatter `ipfs_cid` |
| Arweave (permanent) | Use ardrive CLI; record TXID in frontmatter `arweave_txid` |

`storage_tier` field in the publication's frontmatter declares which channels apply. The meta-schema (`forensics/schemas/shape/canonical-doc.meta.schema.json`) enumerates valid storage_tier values.

---

## 📊 Today's publishing throughput (2026-05-21 example)

| Phase | Count |
|---|---|
| Drafts shipped | 10 (all 10 of today's publications start here) |
| In editing | 0 (most went directly to fact-checked because they're session-eval pieces) |
| Fact-checked | 1 (session-metrics — every number citable) |
| Signed | 0 (signing requires your author keypair — needs provision via `9x_init_reputation.py goodoleusa`) |
| Published externally | 0 (next-wave decision) |

**Next action for you (the user):**
1. Provision your author keypair: `python3 scripts/9x_init_reputation.py goodoleusa`
2. Pick 1-2 publications you most want signed today
3. Run sign-off CLI or use MCP tool
4. Update `status: published` in frontmatter

---

## 🤝 Co-authorship and AI attribution

Every publication's `authors:` field lists humans + AI. The convention:

```yaml
authors: [goodoleusa, JescaLyn, claude-opus-4-7]
```

Names are not equal — you're the editor of last resort. AI contributions are
attributed honestly, neither erased nor inflated. If a publication was largely
agent-authored (like graceful-deprecation-queue), the `authors:` reflects that
and there's an `agent_authored: true` flag in frontmatter.

---

*Your part of the loop. AI drafts; you edit; both sign; the record is anchored. Without your final sign-off, nothing in 00-Publications counts as published — it's all in some draft state. The signing IS the publishing.*
