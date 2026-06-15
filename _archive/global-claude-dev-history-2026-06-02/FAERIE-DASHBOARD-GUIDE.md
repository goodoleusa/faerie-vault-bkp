# Faerie Dashboard — Mission Control for CyberTemplate

**Dashboard-first experience:** Live queue, hypotheses, blockers, agents, decisions + auto-snapshot.

---

## **Quick Start**

### **Run the dashboard:**
```bash
python3 ~/.claude/hooks/state/faerie-dashboard-launcher.py
```

Or using the convenience command:
```bash
faerie-dashboard
```

### **Live watch mode** (refreshes every N seconds):
```bash
faerie-dashboard --watch 5
```
(Great for leaving on a second terminal while agents work)

---

## **What You See**

```
FAERIE — Mission Control Dashboard
═══════════════════════════════════════════

┌─ QUEUE VELOCITY
│  7 HIGH | 16 MED | 0 RUNNING | 33 DONE
│  Velocity: 30.0 tasks/hr | Burn rate: 0 agents = ~5 min to clear HIGH
└─

┌─ HYPOTHESIS SCORECARD
│  H1: Insider access          ██████░░░░ 0.68  ↑+0.13
│  H3: Coordinated exfil       ████████░░ 0.81  ↑+0.49 🔥 MAJOR SHIFT
│  (... H2, H4, H5)
└─

┌─ EVIDENCE TIER INVENTORY
│  TIER 1 (Smoking Gun)    8/15  (53%)  ✅ Floor met
│  TIER 2 (Strong Support) 4/50  (8%)   ⏳ Growing
│  (... TIER 3, 4)
└─

┌─ CRITICAL BLOCKERS (top 3)
│  1. ahmn.co identity: who owns current hostname on 172.93.110.120?
│  2. B2 backup verification for missing ProxMox video (URGENT)
│  3. anchored.host WHOIS + registrant
└─

┌─ AGENT ACTIVITY (next 3 tasks)
│  🔄 8-e7d4 — B2 backup verification for missing ProxMox video
│  🔄 7-e282 — ahmn.co WHOIS + MX
│  🔄 7-40bc — AS400495 BGP peer list
└─

┌─ DECISION ESCALATION (top flags)
│  1. 🔴 Source video missing from B2 backup (SHA-256: e82435...)
│  2. 🔴 ProxMox operator evaluated bulk-deleting VM records
└─

┌─ INSIGHTS SURFACED (things faerie noticed)
│  🔍 [NECTAR] fnd00006 userId gap resolved: a458... is transcription error
│  🔍 [NECTAR] Hypotheses: H1↑0.55, H3↑0.81, H5↑0.40
│  ⚠️ [REVIEW] EVIDENCE DESTRUCTION RISK: operator selected all 37 ProxmoxVM...
└─

💾 Auto-snapshot saved: dashboard-20260320-011754-faerie-turn4.json

NEXT: Run /run to launch next HIGH task, or /handoff to end sprint.
```

---

## **Snapshots & Comparison**

### **View all snapshots:**
```bash
faerie-dashboard --report
```

### **Compare last 2 snapshots:**
```bash
faerie-dashboard --compare
```

Output shows deltas:
```
DASHBOARD DELTA: 2026-03-20T01:17 → 2026-03-20T01:30
  baseline-t3 → after-agent-returns

┌─ QUEUE DELTA
│  HIGH queued:  7 → 4  (-3)
│  Completed:    33 → 36  (+3)
└─

┌─ HYPOTHESIS DELTA
│  H3:  0.32 → 0.81  ↑+0.49  🔥
│  H4:  0.61 → 0.82  ↑+0.21
└─
```

---

## **Your New Workflow**

Instead of chat back-and-forth:

**Turn 1: Orientation**
```bash
faerie-dashboard
# → See queue state, hypotheses, blockers, agents
# → Auto-snapshot captured ("faerie-turn1-orient")
```

**Turn 2-N: Execution**
```bash
/run
# Agent claims + executes task
# Outputs auto-committed to git
```

**Turn N+1: Review + Next**
```bash
faerie-dashboard
# → See updated state, new insights surfaced
# → Auto-snapshot captured ("faerie-turn5-post-agent-returns")
# → Decide: launch next batch or review findings
```

**Compare progression:**
```bash
faerie-dashboard --report
# See: baseline → turn1 → turn5 → current
# Understand: what worked? Where are we?
```

---

## **Integration with /faerie Skill**

Currently `/faerie` is the chat-heavy orchestrator. The dashboard launcher is a **complement** — use it for:
- **Status checks** before launching tasks
- **Review points** to see discoveries you missed
- **Sprint progress** visualization
- **Decision tracking** (which hypotheses are winning?)

You can run BOTH:
1. `faerie-dashboard` — see current state + auto-snapshot
2. `/faerie` — (if needed) for queue orchestration, launching agents, etc.

Or **replace `/faerie` calls with `faerie-dashboard`** for a cleaner dashboard-first workflow.

---

## **Advanced: Live Watch + Parallel Execution**

**Terminal 1 (Monitor):**
```bash
faerie-dashboard --watch 5
```
(Live dashboard updates every 5 seconds)

**Terminal 2 (Execute):**
```bash
/run
```
(Claims + runs HIGH tasks)

**Result:** As agents complete work, Terminal 1 shows real-time queue burndown + hypothesis movement.

---

## **Files**

- **Launcher:** `~/.claude/hooks/state/faerie-dashboard-launcher.py`
- **Dashboard renderer:** `~/.claude/hooks/state/mission_control_dashboard.py`
- **Comparison tool:** `~/.claude/hooks/state/dashboard-compare.py`
- **Snapshots:** `~/.claude/hooks/state/dashboard-snapshots/` (JSON, timestamped)
- **Convenience command:** `faerie-dashboard` (bash wrapper)

---

## **Next Steps**

1. **Try it:** `faerie-dashboard` or `faerie-dashboard --watch 5`
2. **Let agents finish** (ahmn.co WHOIS, BGP peer data still running)
3. **Compare snapshots** when they return: `faerie-dashboard --compare`
4. **Decide:** Launch next HIGH batch or review findings?
