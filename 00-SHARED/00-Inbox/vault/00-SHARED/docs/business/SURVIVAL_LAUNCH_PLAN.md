---
type: business
status: active
created: 2026-04-21
tags: [business, launch, strategy]
up: README.md
prev: BUSINESS_PLAN.md
next: NOVELTY_TABLE.md
---

> [↑ Readme](README.md) · [← Business Plan](BUSINESS_PLAN.md) · [→ Novelty Table](NOVELTY_TABLE.md) · [⌂ Home](../../README.md)

# faerie — Zero-Budget Survival Launch Plan

> One dev. No money. Windows laptop. Strong idea. Need revenue now.
> This plan assumes $0 budget and prioritizes income in weeks, not months.

---

## The Hard Truth First

You already have the product. The `.claude/` folder + agents + skills we just
built IS faerie v0.1. It works on Claude API today.

The fastest path to revenue is not building more — it's finding 5 people who
will pay for what already exists and setting them up.

---

## Week 1–2: Get Paid for What Exists

### What You're Selling

A **working Claude CLI setup** that gives investigators, journalists, and researchers
a memory layer that doesn't forget between sessions. What they pay for:

1. **The config** — your `.claude/` folder, HONEY.md, rules, skills, agent cards
2. **The setup session** — 30-60 min live call to get them running
3. **Ongoing support** — they can Slack/Discord you questions for 30 days

Price: **$150-$300 one-time setup fee**. Recurring optional at $50/mo.

You can close your first sale **this week** if you reach the right people.

### Where to Find Buyers — Free Channels Only

**OSINT Twitter/X** (highest conversion for this product):
- Post a 5-tweet thread: "I built a memory system for Claude that never forgets your investigation context between sessions. Here's how it works:" → show a before/after SEED compression example
- Hashtags: #OSINT #InvestigativeJournalism #AItools #Claude
- Tag: @Bellingcat @OCCRP @ObservatoryIL @JakeBraun
- If 1 person DMs → $150 right there

**Reddit** (free, targeted):
- r/OSINT, r/InvestigativeJournalism, r/artificial, r/ClaudeAI
- Post: "I built a persistent memory layer for Claude investigations — here's how it works for cross-session forensic research"
- Mention the forensic reasoning log specifically — this is the hook for investigators

**LinkedIn** (professional, slower but higher WTP):
- Post the same thread format
- Tag investigative journalists, OSINT professionals, compliance investigators

**Discord servers** (free, immediate feedback):
- Bellingcat Discord
- OSINT Discord (invite-based, get invited via Twitter)
- r/OSINT Discord
- Offer free setup in exchange for feedback (barter phase)

### What to Say

Don't pitch the architecture. Say this:

> "If you use Claude for investigation work, you know the pain: every session starts
> from scratch. You re-explain the case, the entities, what you've already tried.
> I built a memory layer that fixes this. Your investigation context is always loaded.
> Dead ends are remembered so you don't retry them. Cross-session reasoning is preserved
> in a forensic log you can export. Setup takes 30 minutes. Happy to show you."

That's it. If they say "how much?" → $150 one-time, $50/mo ongoing.

---

## Week 2–4: Free Credits + Small Revenue

### Anthropic Developer Program
Apply NOW: https://www.anthropic.com/api
- Describe faerie as a memory middleware layer for the Claude API
- Request API credits for development
- This is legitimate — you're building a Claude-adjacent tool
- Credits remove your API cost concern for development

### GitHub + Open Source Positioning
1. Push the repo public (already on GitHub)
2. Write a good README that positions faerie as "the memory layer Anthropic doesn't ship"
3. Add a "sponsor this project" button (GitHub Sponsors — takes 2 minutes)
4. ProductHunt launch: free, can drive 100s of signups in one day

**Do NOT try to build a web app yet.** The repo IS the product for now.

### Barter for Testimonials
Find 3 OSINT researchers, offer free setup in exchange for:
- A written testimonial
- A tweet about their experience
- A 15-min recorded conversation (you use as social proof)

One good testimonial from a credible investigator is worth $5,000 in paid ads.

---

## Month 1–2: Build the Minimum Paid Product

You need one thing to charge monthly: **a way to deliver updates automatically**.

The simplest possible paid tier (no server, no code):
- Free: The GitHub repo (they set it up themselves)
- **$29/mo**: You maintain their `.claude/` folder — push updates, new agents, HONEY crystallization improvements — and they pull via git
- **$99/mo**: Same + monthly 30-min check-in call + priority support

This is a **managed config subscription**. No server. No cloud. No infrastructure costs.
Just a private GitHub repo they're a collaborator on, and you push improvements.

This can run on zero infrastructure costs indefinitely.

---

## Month 2–3: The Real Product Emerges

By month 2, you'll have:
- 5-15 paying users at $29-$99/mo = **$500-$1,500 MRR**
- Real usage data for what faerie does and doesn't do well
- A handful of testimonials and case studies
- Understanding of which pain points are universal vs niche

**Only then** do you start building the pieces that require code:
- Simple Python CLI wrapper (`pip install faerie-cli`)
- SEED generator script (queries HONEY, compiles <2K token brief)
- I/F ratio logger (hooks into Claude CLI post-turn hook)

These are 1-3 day projects each, not months. You already have the design.

---

## Month 3–6: SDK and Middleware Play

When you have ~20 paying users and $1,500+ MRR:
1. Apply to Y Combinator (next batch)
   - Your story: solo dev, investigative journalism use case, memory middleware for Claude API
   - They fund pre-revenue ideas; $1,500 MRR is "traction" to them
2. Apply to Anthropic Build (startup accelerator program if it exists)
3. Approach OCCRP, Bellingcat, First Draft about grant-funded journalist licenses
   (investigative journalism orgs get grants for tools — this is a real funding path)

---

## What to Build vs. What Not to Build Yet

### Build NOW (1-3 days each, no GPU, no server)

| Thing | Why | Time |
|-------|-----|------|
| `install.sh` — copy `.claude/` folder to new machine | Lowers setup friction | 2h |
| `seed_gen.py` — reads HONEY, generates <2K SEED | Core product value | 1 day |
| `if_logger.py` — post-turn hook, logs PAIN/SURPRISE to JSONL | I/F data collection | 4h |
| Public README with OSINT positioning | Discovery + conversion | Done |
| `GETTING_STARTED.md` for non-technical users | Enables self-service | Half day |

### Do NOT Build Yet

| Thing | Why not |
|-------|---------|
| Web UI | No users yet, no revenue, huge time sink |
| SaaS backend / server | $0 budget + no users = waste |
| Mobile app | Wrong audience |
| Vector database / embeddings | HONEY + crystallization replaces this |
| Training pipeline with GPU | Not needed — Claude API is your compute |
| Plugin/extension for other tools | Validate core first |

---

## Emergency Actions (This Week)

If you need money in days, not weeks:

1. **Post on Twitter/X today.** One thread. One real example of faerie preserving
   investigation context. Ask if anyone wants a setup session. Charge $100.

2. **DM 5 OSINT researchers directly.** "I built something for your workflow,
   would love to show you 30 minutes." Conversion rate on warm DMs is ~20%.
   5 DMs → 1 call → $100.

3. **Upwork/Toptal: "Claude API consultant"** — your faerie work IS a portfolio.
   AI consultants charge $50-150/hr. One small gig buys weeks of runway.

4. **Apply for Anthropic API credits** while you do the above.
   This removes the cost-of-goods problem entirely.

---

## The Honest Risk Assessment

**Biggest risk:** You spend the next 2 months building more architecture instead of
finding your first paying customer. The architecture is done. The product exists.
The bottleneck is now distribution, not development.

**Second biggest risk:** You target too broad an audience. The forensic investigator
beachhead is the right call — high pain, high WTP, tight community, word of mouth.
10 satisfied investigators is worth more than 1,000 casual Claude users.

**What you have that money can't buy:**
- A working system that actually solves a real problem
- Deep domain understanding (you ARE the target user)
- A repo with real architecture that signals credibility to technical buyers
- The ability to onboard someone in 30 minutes and have them see value immediately

That's a strong position. The gap between this and revenue is outreach, not more building.

---

## Revenue Timeline (Realistic)

| Week | Target | How |
|------|--------|-----|
| 1 | First $100 | Twitter thread + 1 setup session |
| 2–3 | $300–$500 | 3 setup sessions + 1-2 recurring |
| Month 2 | $500–$1,500 MRR | 5-15 recurring subscribers |
| Month 3 | $1,500–$3,000 MRR | First SDK customers + journalism grant inquiry |
| Month 6 | $5,000+ MRR | YC/Anthropic funding conversation becomes real |

The numbers aren't big — but $1,500/mo is survival. That's the only goal right now.
