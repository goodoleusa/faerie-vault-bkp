---
type: project-publish-folder
project: cybertemplate
created: 2026-05-22
purpose: human-final-gate workspace for cybertemplate site publishing
canonical_dashboard: ../PUBLISHING-DASHBOARD.md
---

# CybertemplatePUBLISH — the publish workspace

This is the dedicated workspace for taking cybertemplate investigation
work from AI-curated state → site-published narrative.

## Folder structure

```
CybertemplatePUBLISH/
├── README.md (this file)
├── drafts/              ← AI session outputs land here (status: draft)
├── reviewing/           ← Moved here when you start reading (status: reviewing)
├── annotating/          ← Your active annotation pass (status: annotating)
├── ready-to-publish/    ← One last gate before site sync (status: ready-to-publish)
├── published/           ← Done; signed; live on cybertemplate.retrofuture.tech
└── imports-staging/     ← Material being imported from CyberOps-UNIFIED for review
```

## The pipeline

```
cybertemplate (data tier 1-4) →
  AI session writes narrative into drafts/ →
  you move to reviewing/ →
  you annotate (your voice on top) →
  ready-to-publish/ →
  swarmy-publish <file> →
  published/ + signed →
  poll-deploy sync to cybertemplate.retrofuture.tech (~5 min)
```

## Roundup from CyberOps-UNIFIED

The companion vault `D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED`
has cybertemplate / critical-exposure content authored earlier. Items
to import for the final push live in `imports-staging/`. See
`imports-staging/_INVENTORY.md` for the candidate list.

## Workflow (CLI)

```bash
# What's in each bucket right now?
swarmy-inbox

# Open today's vault daily folder (not project-specific)
swarmy-vault-today

# Move a draft → reviewing
swarmy-status-set drafts/foo.md reviewing
mv drafts/foo.md reviewing/foo.md   # also move file (until automated)

# Publish (signs + flips to published + stages for site sync)
swarmy-publish ready-to-publish/foo.md
```

## What the CybertemplatePUBLISH dashboard surfaces (to be built)

A sister Dataview-driven dashboard `00-SHARED/CYBERTEMPLATE-STAGE-DASHBOARD.md`
(queued — see `Daily/2026-05-22/05-dashboard-audit.md`) will surface:

- Items in each stage with one-click status transitions
- Tier-1 evidence count from cybertemplate repo
- Open promotions from `cybertemplate/forensics/promotion_log.json`
- AI sessions touching cybertemplate (from `forensics/manifests/{today}`)
- "What's blocking publication" rollup

