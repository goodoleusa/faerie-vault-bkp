---
type: meta
tags: [business, faerie]
sibling:
  - "[[Cursor Faerie Money]]"
  - "[[../Hive/17-BUSINESS-PLAN-HIVE-DESIGN|17-BUSINESS-PLAN-HIVE-DESIGN]]"
  - "[[../Agent-Outbox/batch-api-business-plan|batch-api-business-plan]]"
doc_hash: sha256:343976a573bc8d4eb88da18e55f25b95ffc8556ab5abf2a721a136474fd41f64
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:35Z
hash_method: body-sha256-v1
---
This is a strategic product question about how to make an open source tool go viral while protecting the "secret sauce" (faerie's orchestration and memory system). Let me think through this carefully.

sibling:: [[Cursor Faerie Money]]
::child

- [ ] The user wants to:

1. Make DAE go viral as an open source tool
2. Give users "the magic" of faerie without exposing the full system
3. Create a "taste without the secret sauce"

This is a classic freemium/open-core product design question. Let me think about what faerie actually provides and what parts could be open vs proprietary (or at least not easily replicated).

**What faerie adds that's hard to replicate:**

- HONEY.md crystallization (memory that accumulates over time)
    
- Investigation state tracking with hypotheses and confidence scoring
    
- Cross-session continuity through append-only findings
    
- COC forensic provenance tracking
    
- The full 3-tier queue system (global → investigation → repo)
    
- Agent training and improvement loops
    

**What DAE can ship open source that gives a taste:**

- The 10-agent pipeline (this is the magic visible to users)
- REVIEW-INBOX mechanism (findings surface to humans)
- Basic COC/hashing
- Session scratch notes
- Simple queue

**The "secret sauce" protection strategy options:**

**Option A: Ship the pipeline, not the memory**

- DAE ships the full agent orchestration that users see and love, but without the persistent learning layer that makes faerie continuously improve
- Users get excellent single-session results but can't compound knowledge across runs
- Faerie users get the advantage of every session building on previous discoveries

**Option B: Ship a "faerie lite" that calls home**

- Open source DAE includes an optional connection to a faerie server that holds the memory and crystallization logic
- Users can self-host or use the hosted version, making it a context-as-a-service model

**Option C: Make faerie an optional enhancement**

- DAE works standalone with good results, but when FAERIE_HOME is configured, it reads from the persistent memory files for dramatically better performance
- The open source skeleton is available, but the accumulated knowledge stays private, creating that viral hook of continuous improvement

**Option D: The "BYOF" (Bring Your Own Faerie) model**

- DAE ships as the standard with minimal memory, but users can point to any faerie backend via environment variable
- Publish a community edition alongside it, with a premium managed service handling the memory layer

**What would make it go viral:**

1. **Immediate wow moment**: First run produces something impressive that would normally take hours of manual work
2. **Compound value**: Results improve over time, but only if users install faerie to unlock this
3. **Shareable artifacts**: The findings and tier summaries are compelling enough that people want to share them
4. **"How did it know that?"**: Cross-session memory pulling up something relevant from weeks prior

The real split is between what's open and what's proprietary — the pipeline execution and orchestration are public, but the memory format and crystallization algorithm stay private. Or maybe everything goes open source, but the magic lives in the accumulated knowledge within the memory files.

The deepest realization is that the actual moat isn't the code itself — it's the accumulated memory. Open sourcing everything still works because users need months of running it to build up the knowledge that makes it truly powerful. It's like git: completely open source, but the value is in the history you've built.

The recommended path forward is shipping DAE as fully open source... The real differentiator isn't any single feature—it's how memory and orchestration compound over repeated use, building investigation knowledge that gets richer each session. I can showcase the immediate single-run impact (the pipeline delivering results that would take days manually) without revealing the long-term accumulation magic that only emerges from sustained use.

3 agents running. On your question — this is a good product design problem.

---

**The core insight: the secret sauce isn't the code — it's the memory.**

You can open source everything and still have a moat, because:

- HONEY.md after 3 months of investigation work is irreplaceable
- The crystallization that built it required hundreds of sessions
- A new user gets the code but starts with an empty memory

This is like git — fully open, but the value is in the history only you have.

---

**The "taste without sauce" architecture:**

```
DAE (open source, full pipeline)
  └── runs beautifully on session 1
  └── writes to REVIEW-INBOX, scratch — standard, open
  └── has FAERIE_HOME hook (env var, optional)
        └── if set → reads HONEY.md, NECTAR.md, injects context bundle
        └── if not set → runs clean, no memory, still impressive
```

**Session 1 (no faerie):** "How did it find all that in 3 minutes?" **Session 10 (with faerie):** "How did it know to connect this to something from last month?"

---

**What to ship open:**

- Full 10-agent pipeline
- REVIEW-INBOX mechanism
- COC/hash integrity
- Queue system
- The faerie hook (reads from FAERIE_HOME if set)
- A starter `HONEY.md` template with generic investigation patterns

**What stays private by nature:**

- Your accumulated HONEY.md (2+ years of investigation knowledge)
- Your NECTAR.md findings chain
- Your agent training history (scores, redemptions)

---

**The viral hook:**

> "Your investigation runs on a 10-agent pipeline. Connect it to memory and it gets smarter every time."

First-run magic = pipeline. Retained-user magic = compound memory. The upgrade path is effort (setting up faerie), not a paywall. That's good open source dynamics.

---

**For the faerie/data-ingest coexistence in your own setup:**

The cleanest model is making faerie a **pre/post wrapper**, not embedded logic:

```
/faerie → reads memory → injects context_bundle → queues data-ingest task
           ↓
/data-ingest → runs pipeline with that bundle → writes findings
           ↓
faerie (session end, via membot) → promotes findings → updates hypothesis scores
```

No overlap. `/data-ingest` never reads HONEY/NECTAR directly — faerie feeds it the relevant excerpts as a bundle. This also makes the open source version clean: the pipeline just accepts a context bundle (JSON), regardless of where it came from.

---

**For the FAE vs. DAE experiment:** That would be genuinely interesting data — same raw data, same agents, with and without faerie. Hypothesis: pipeline precision stays similar, but recall (finding connections) and depth (correct hypothesis attribution) should be significantly better with faerie. Worth running once DAE is cleaned up.

3 agents are still running. I'll report when they return.

[⚡ T11 | 3 agents running | ctx ~128K | HIT ✓ | $0.05/turn | headroom: ~65K]

Task 2 (pipeline_ip_crossref.json) completed. Both IPs already existed but were enriched. Let me mark it complete and wait for the other 2 agents.

Bash Mark K8s IP crossref task complete

IN

cd "D:/0LOCAL/gitrepos/cybertemplate" && C:/Users/amand/AppData/Local/Programs/Python/Python313/python.exe "C:/Users/amand/.claude/skills/run/claim_task.py" --complete task-20260323-140407-e027 2>/dev/null

OUT

{"status": "ok", "task_id": "task-20260323-140407-e027", "action": "completed"}

**Task 2 done** — K8s IPs were already in the crossref from a prior run, now enriched with full Hetzner/AS24940 metadata + `federal_data_exposure` flag. Clean outcome.

Still waiting on:

- `ada43302e63851187` — cdn181.awsdns-531.com passive DNS (FamousSparrow C2)
- `ae3d222261ffc51b5` — ORNL cert on 166.1.22.248 (nuclear triple)

[⚡ T12 | 2 agents running | ctx ~130K | HIT ✓ | $0.03/turn | headroom: ~60K]

i do want to make money though. what would be magic and easily persuade users to upgrade? im using this to get out of poverty, so whats the minimal infra i would need to try to maintain user trust about memory? i want to show i respect privacy which is important for trusting your crystallized intel with another provider on top of the model provider. cld i sell the fact that its only crystallized insights about the process to make agents more effective over time, not any PII or sensitive info about their data? how cld i provide a hosted or managed service using like my zimaboard2 and some personal hard drives to maintain custody? cld i make customers' memory auditable and fully COC'd and exportable any time, ie iron clad data sovereignty? cld i deliver this and put in the TOS that my company also collects insights about PROCESS for future agent builds but retains no company-specific PII or IP and prove it with transparency audits that dont cost me money

This is a serious business/product strategy question from someone who's trying to get out of poverty. Let me think through this carefully and give genuinely useful advice.

The user wants to:

1. Make money from DAE/faerie
    
2. Build user trust through privacy-respecting memory management
    
3. Sell a hosted/managed service
    
4. Run it on personal hardware (ZimaBoard2 + personal hard drives)
    
5. Sell the "crystallized process insights" not PII/sensitive data
    
6. Make memory auditable, COC'd, exportable (data sovereignty)
    
7. Include in TOS: company collects process insights for agent improvement, retains NO company PII/IP
    
8. Prove it with free or cheap transparency audits
    

The real value here is that users accumulate valuable memory artifacts (HONEY.md, NECTAR.md) through their investigations, and a managed service solves the persistence, sync, and backup problem they'd otherwise face. What I'm actually selling is memory persistence plus the ability to enhance their starting point with curated templates, while gradually improving the agents themselves through anonymized process insights.

The privacy model hinges on a critical distinction: agent cards contain only process knowledge (safe to share like "use Bonferroni correction" or "Git Bash needs HOMEDRIVE+HOMEPATH"), while case data stays sensitive and private. I can honestly collect anonymized process insights about how agents improve over time and which techniques work best, but I never touch the actual investigation data.

For the infrastructure, I'm thinking a ZimaBoard2 with personal storage (NVMe + HDD backup), Tailscale or Cloudflare Tunnel for secure access, and a simple FastAPI server syncing memory through git repos and Restic backups. The trust mechanism relies on chain-of-custody hashing for every memory write, so there's cryptographic proof of what was accessed and when.

On the TOS side, the real differentiation is being explicit about what you _don't_ collect—case data stays encrypted end-to-end on the user's machine, you only see anonymized process insights for improvement, and users get full export and deletion rights including the audit trail itself. The proof angle is open-sourcing the sync layer so people can verify the encryption claims without needing to trust marketing.

For revenue, I'm thinking a free tier for local-only use, then Pro at $10-20/month for managed sync and backup, and Team tier at $50-100/month for shared investigation memory across multiple agents. The real bottleneck isn't building this—it's getting those first 10 users to trust you enough to pay, then keeping the sync service stable.

The moments that actually drive upgrades are when agents recall connections from months back, when you see visible performance improvements from learning, when memory persists across devices, and when users can export everything instantly and verify the full audit trail. For trust, I need E2E encryption where users hold the keys, an open source sync server, and the ability to export everything at any time—those are the non-negotiables.

The real competitive advantage is proving I can't access their data even if I wanted to. Client-side encryption with user-controlled keys shifts the pitch from "we store your memory" to "we back up your memory safely," which is a fundamentally different value prop.

This is a real product with genuine monetization potential. Let me be direct about what actually works.

---

**The core monetization insight:**

HONEY.md already has the separation built in — by design, agent cards and HONEY contain **process knowledge only** (techniques, methods, agent behaviors), never case data. This isn't a compromise — it's the legal COC requirement you already enforce. It's also your privacy story.

You're selling: **"Your agents get smarter over time. We only ever see HOW they improve, never WHAT they investigated."**

That's true, verifiable, and genuinely rare.

---

**What makes users upgrade (the magic moments):**

|Moment|What triggers it|When it happens|
|---|---|---|
|Cross-session recall|Agent surfaces connection from 3 months ago|~session 5-10|
|Visible agent improvement|"Agent beat its last score — here's what changed"|After first OTJ redemption|
|Machine migration|Memory survived a laptop swap|First hardware change|
|"How did it know?"|HONEY injected context the user forgot they had|Any session after crystallization|

The hardest one to fake and easiest to wow: **cross-session recall on something the user forgot.** That's the hook.

---

**Minimal honest infrastructure (ZimaBoard2 model):**

```
User machine (client)
  └── HONEY.md + NECTAR.md encrypted with USER-HELD key
  └── faerie sync daemon encrypts before upload
  └── hash chain (COC) signed locally before upload

ZimaBoard2 (your server, at home or a $5/mo VPS)
  └── Receives: encrypted blobs + hash manifests
  └── Stores: ciphertext only — you literally cannot read their content
  └── Syncs: Restic backup to Backblaze B2 (~$0.006/GB/mo)
  └── Serves: fast sync + retrieval API

git per user
  └── Private repo per user (your Gitea instance on ZimaBoard)
  └── Every HONEY.md write is a commit — full version history
  └── User can clone at any time — full export = git clone
```

Total cost to run: ~$15/mo (Backblaze B2 + a domain + ~5W power draw from ZimaBoard).

---

**The privacy architecture that's actually auditable:**

```python
# Client-side, before any upload:
key = derive_key(user_passphrase)  # never leaves user machine
ciphertext = encrypt(HONEY_md_content, key)
manifest_entry = {
    "sha256": sha256(HONEY_md_content),  # hash of plaintext
    "encrypted_sha256": sha256(ciphertext),  # hash of what we store
    "ts": timestamp,
    "sig": hmac(entry, user_key)
}
upload(ciphertext, manifest_entry)
```

What this proves: you store only ciphertext. User holds the key. The COC chain is signed with their key. You can never retroactively claim you had access because the HMAC requires their key to verify.

---

**The "process insights" collection (your honest data flywheel):**

When an agent improves (OTJ redemption), the training-log.jsonl entry already separates:

- **What improved**: "source diversity benchmark" (process — safe to collect)
- **On what task**: the investigation context (private — stays local)

You collect only the `path_to_success` field, not the task itself. One line in the code. Verifiable in open source.

**TOS that's actually defensible:**

> We collect: anonymized agent technique improvements (what method worked better, not what was investigated). We never see: your HONEY.md contents, NECTAR.md findings, any case data. Client-side encryption means we cannot. You own: full export (git clone) + full deletion + COC audit trail at any time. Transparency: sync server is open source. Verify we can't read your data.

The "prove it without money" part: **open source the sync server.** Security researchers will audit it for free if it's interesting. The hash chain provides mathematical proof without requiring auditors.

---

**Revenue structure that works at your scale:**

|Tier|Price|What they get|
|---|---|---|
|Local free|$0|Pipeline runs locally, no sync|
|Memory sync|$8/mo|Encrypted sync + backup + export|
|Teams|$35/mo|Shared investigation memory, 3 users|

You need ~25 paying users at $8 to cover a month of food. ~100 to be stable. That's achievable from a niche (security researchers, investigative journalists, complex analysts) before you need to think about scale.

---

**The one thing that kills this:** uptime. Paid users expect sync to work. Before charging money, run it for yourself for 3 months, prove the ZimaBoard doesn't fail. Then charge. The trust investment is worth more than early revenue.

The big picture: you have working code, a real use case, and a privacy story that isn't theater. Most AI tool companies don't have that combination.