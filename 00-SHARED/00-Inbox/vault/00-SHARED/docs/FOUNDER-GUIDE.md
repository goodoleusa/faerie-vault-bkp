---
type: guide
status: active
created: 2026-04-21
tags: [founder, eli5, getting-started, business]
up: README.md
next: COMMAND-GUIDE.md
---

> [↑ Readme](README.md) · [→ Command Guide](COMMAND-GUIDE.md) · [⌂ Home](../README.md)

# faerie2 — Founder's Plain-English Guide

**Written for:** You, Amanda. The person building this into a product.
**Level:** No code knowledge needed to understand this. Code knowledge needed to run it.
**Goal:** Know exactly what you built, why it matters, and what to do next.

---

## What Did We Just Build? (The Big Picture)

Imagine you hired 10 expert assistants — a researcher, a data analyst, a security auditor, a writer, a coder, and more. Every time they finish a job, they forget everything and start fresh. That's Claude without faerie.

**faerie** gives your team of AI assistants a shared memory, a task queue, and a self-improvement system. When the researcher learns something, the analyst can use it next session. When an assistant does a bad job, faerie notices and routes that type of work to a better assistant next time.

**What we built today** is the storage layer underneath all of that — a proper database service so that memory is fast, searchable, and survives the computer restarting.

---

## The Three Parts We Built (Memory Service)

### Part 1 — The Database (`models.py` + `schema.sql`)

Think of this as a filing cabinet with 11 drawers:

| Drawer | What goes in it | Lifetime |
|--------|----------------|----------|
| **HONEY** | Your AI's crystallized best practices — things it learned that work every time | Forever |
| **NECTAR** | Validated findings — "we confirmed this is true" | Forever (can never be deleted) |
| **POLLEN** | Work-in-progress notes from each session | 7 days, then auto-deleted |
| **DROPLETS** | Quick insights written in the moment | Forever |
| Sessions | Tracks every time you open Claude | Until session ends |
| Agent Cards | Each AI assistant's report card (scores, improvements) | Forever |
| Training Queue | AI assistants waiting to improve | Until redeemed |
| Forensics | Tamper-proof audit log of every action | Forever (immutable) |
| Review Queue | High-priority flags needing human attention | Until resolved |
| Agent Roster | Who was working on what, when | Forever |
| Memory Index | Search relevance scores (makes search fast) | 24 hours |

### Part 2 — The API (`main.py`)

Think of this as the front desk of the filing cabinet. Instead of reaching in yourself, you ask the front desk:

- "Give me the latest HONEY" → `GET /memory/honey`
- "Add this to NECTAR" → `POST /memory/nectar`
- "What pollen is active for this session?" → `GET /memory/pollen`
- "Search for anything about X" → `GET /memory/search`

**Why does this matter for your startup?** Because now *any* tool — your phone, a web dashboard, a different AI, a customer's system — can talk to faerie's memory. You're not locked into the command line.

### Part 3 — The Tests (`test_api.py`)

18 automated checks that run before you ship anything. They confirm:
- Every endpoint actually works
- Bad input gets rejected with a clear error (not a crash)
- The database is reachable
- Old commands still work after updates

---

## What Problem Does This Solve for Your Startup?

### The Problem You're Selling a Solution To

Every business using AI has the same frustration: **the AI forgets everything between sessions**. You explain your company's style, it forgets. You teach it your customer's situation, it forgets. You correct a mistake, it makes the same mistake tomorrow.

This costs companies money every day — in time spent re-explaining context, in mistakes from forgotten constraints, in junior employees who have to babysit AI output.

### What faerie Sells

**faerie is a memory and improvement layer for AI agents.** You sell it to:

1. **Businesses already using Claude or other LLMs** who are frustrated by the amnesia problem
2. **Teams running multi-step workflows** (research → writing → publishing, or intake → analysis → report)
3. **Organizations that need audit trails** (legal, finance, security — the forensics layer is designed for court-admissibility)

### The Three-Sentence Pitch

> "Every AI assistant you use starts from zero every time. faerie gives your AI team persistent memory, self-improvement, and a tamper-proof audit log. Your agents get better every sprint — and you can prove it."

---

## How You Run This (Step by Step)

You do not need to understand the code. You need to know which commands to type.

### Prerequisites (One-Time Setup)

**You need:**
- A computer running Linux, Mac, or Windows with WSL (you already have WSL)
- PostgreSQL installed (the database engine)
- Python 3.10 or newer
- Claude CLI installed

**Install dependencies once:**

```bash
# Navigate to the memory service folder
cd /mnt/d/0local/gitrepos/faerie2/memory_service

# Install Python packages
pip install -r requirements.txt

# Create the database (PostgreSQL must be running)
createdb faerie_memory

# Set up the database tables
# (Run this once — it creates all 11 drawers in the filing cabinet)
psql faerie_memory < schema.sql
```

### Starting the Service

Every time you want faerie's memory to be active:

```bash
# Start the memory service (keep this terminal open, or run in background)
cd /mnt/d/0local/gitrepos/faerie2/memory_service
uvicorn main:app --host 0.0.0.0 --port 8765

# You'll see: "Uvicorn running on http://0.0.0.0:8765"
# That means it's working.
```

**To verify it's running**, open a browser and go to: `http://localhost:8765/health`

You should see: `{"status": "ok", "ts": "2026-..."}`

### Running the Tests

Before trusting any code with real data, run the tests:

```bash
cd /mnt/d/0local/gitrepos/faerie2/memory_service

# Make sure service is running first, then:
pytest test_api.py -v
```

You want to see 18 green dots (passes). If you see red, something is misconfigured.

### Using It With faerie (Daily Use)

Once the service is running, faerie automatically uses it. When you type `/handoff` at the end of a Claude session, faerie:

1. Pushes all your session's observations (POLLEN) to the database
2. Promotes high-priority findings to NECTAR
3. Those findings are available next session when you type `/faerie`

**You don't touch the service directly** — faerie and your agents do.

---

## The Self-Improvement Loop (Your Competitive Moat)

This is the part that separates faerie from "Claude with a notepad."

```
Session 1: Agent does work → gets scored → score stored
Session 2: faerie reads scores → routes work to better agents
Session 3: agents improve → beat their previous scores → learn
Session 4: same tasks run 30% faster with fewer errors
...
Session N: measurable, provable improvement over baseline
```

**Why this matters for your pitch:** You can show a customer a graph. "On day 1, your AI team scored 0.65. On day 30, it scores 0.91. Here's the audit log proving it."

No competitor can show that. Most AI tools give you a black box. faerie gives you a grade report.

---

## What to Build Next (Startup Roadmap)

Here is the honest priority order for getting to revenue:

### Step 1 — Make It Run on Someone Else's Computer (2 weeks)

Right now faerie only runs on your machine. To sell it, it needs to install on a customer's machine in under 10 minutes.

**What to do:**
- Run `bash scripts/install.sh` and document every step that breaks
- Fix the breaks
- Test on a fresh machine (rent a $5/month VPS, try installing there)
- When a stranger can install it without help, you're ready to demo

### Step 2 — Build One Paying Use Case (4 weeks)

Don't sell "AI memory platform." Sell a specific outcome to a specific customer. Best candidates:

**Option A — Security/Compliance Teams**
The forensics layer (tamper-proof audit log, hash-chained records) is already built. Security teams pay real money for auditable AI workflows. Pitch: "Use AI for threat analysis with a court-admissible audit trail."

**Option B — Research Teams**
Academic or corporate researchers who run multi-day investigations. faerie's NECTAR + context bundles mean a researcher picks up exactly where they left off. Pitch: "Your AI research assistant that actually remembers."

**Option C — Content/Marketing Agencies**
Agencies running AI workflows for multiple clients. faerie can run separate agent teams per client with separate memories. Pitch: "AI that learns your client's voice and never forgets it."

### Step 3 — Show the Score (2 weeks)

Build a one-page dashboard that shows:
- Number of agents run this week
- Beat-last rate (% that improved vs last week)
- Top findings from NECTAR
- Training queue status

This is your sales tool. Show it to prospects. Show them their AI team getting smarter.

### Step 4 — Charge Money

Starting price point: **$200-500/month per team** (5-10 users). That's below budget-approval thresholds for most teams, above "side project" pricing that signals you're serious.

---

## The Files and What They Do

Here is every file in `memory_service/` explained in plain English:

| File | What it does | Do you touch it? |
|------|-------------|-----------------|
| `schema.sql` | Creates the database structure (run once at setup) | Run once, then never |
| `models.py` | Python description of each database table | Only if adding new tables |
| `main.py` | The API — the front desk for the filing cabinet | Only to add new endpoints |
| `requirements.txt` | List of Python packages needed | Run `pip install -r` then never |
| `test_api.py` | 18 automated checks — run before shipping anything | Run before every deploy |
| `memory_client.py` | Python SDK so agents can talk to the API | Agents use this automatically |
| `cli_bridge.py` | Command-line interface for the memory service | Used by `/handoff` skill |
| `3x_memory_sdk.py` | Enhanced SDK with fallback for when service is down | Agents use this automatically |
| `3x_fallback.py` | Local filesystem fallback when database is unavailable | Auto-used when DB is down |
| `migrations/` | Database version control (how to upgrade the schema) | Run when schema changes |

---

## Common Questions

**Q: What if the database crashes? Do I lose everything?**

No. The CLI bridge (`cli_bridge.py`) and SDK (`memory_client.py`) automatically fall back to local files when the database is unavailable. You don't lose work — it writes to `~/.claude/memory/` instead. When the database comes back up, you can sync the local files to the database.

**Q: How is this different from just writing notes in a text file?**

Three ways: (1) Search — you can search 10,000 findings in milliseconds; a text file search is slow and clunky. (2) Immutability — NECTAR entries cannot be edited or deleted, even by you; this is what makes the forensics defensible. (3) Structure — the database enforces categories, priorities, and relationships; a text file is just text.

**Q: Can I use this without the PostgreSQL database?**

Yes. The fallback layer stores everything in local markdown files, which is what faerie used before this service was built. The database adds speed and multi-user access; the local fallback keeps you working when it's unavailable.

**Q: How do I know if something is wrong?**

Run `python3 cli_bridge.py status` — it tells you if the service is ONLINE or OFFLINE. If offline, check that PostgreSQL is running and the service is started.

**Q: What does "court-admissible audit log" mean practically?**

Every action that touches forensic data (writes, promotes, deletes) gets a HMAC-SHA256 hash. Each hash includes the previous entry's hash, creating a chain. If anyone tampers with a record, the chain breaks and the tampering is mathematically detectable. This is the same principle used in blockchain, but simpler and more auditable. For a legal or compliance customer, this means AI-generated analysis can be traced, verified, and submitted as evidence.

---

## Your Most Important Next Action

**This week:** Get the service running locally, run the tests, and write down every step that confused you.

That confusion is your product documentation. Every place you got stuck is a place a customer will get stuck. Fix it before you demo.

**Next week:** Show one person outside your household a 10-minute demo. Watch where they're confused. Those are your UI/UX gaps.

**The month after:** Talk to 5 potential customers. Ask them: "What's the most expensive mistake your AI assistant makes repeatedly?" The answer shapes which use case you build first.

You built real infrastructure. The filing cabinet, the front desk, and the audit system are done. Now you need to put something in the cabinet that someone will pay to retrieve.

---

## Technical Reference (For When You Need to Dig In)

- **API docs:** `http://localhost:8765/docs` (auto-generated, interactive) — open this in a browser when the service is running
- **Database schema:** `memory_service/schema.sql` — the ground truth for what's stored
- **Full technical README:** `memory_service/README.md` — developer-level detail
- **System architecture:** `ARCHITECTURE.md` — how all pieces connect
- **Eval & learning system:** `docs/EVAL-AND-LEARNING.md` — how agents improve over time
