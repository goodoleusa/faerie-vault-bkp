---
tags:
  - lumo
  - techguide
date_created: 2026-03-10 01:23 pm
date_modified: 2026-03-10 01:39 pm
title: FIRE zimaboard openclaw setup lumo
share_link: https://share.note.sx/t27nuxnl#NUgXNv1qxCqZRVSVKQdIOnvEnN8IOa+x69O4czTeErw
share_updated: 2026-03-10T13:35:13-04:00
type: meta
doc_hash: sha256:44ee322d816af506043354b662a0c5f6d5dd94b01bfefa49c981b60104ed58c9
coc_ref: ~/.claude/memory/forensics/
hash_ts: 2026-03-29T16:10:26Z
hash_method: body-sha256-v1
---

## FIRE Zimaboard Openclaw Setup Lumo

This is a #lumo #techguide sophisticated architecture that blends local-first privacy, asynchronous collaboration, and distributed agent orchestration. You are essentially building a federated knowledge graph where the ZimaBoard acts as the "Stateless Memory & Coordination Layer" and the Workstation acts as the "Compute & Execution Layer."

Here is a design for your Zima-Obsidian-Agent Orchestration Setup, prioritizing security (air-gapped compute), data integrity, and seamless async collaboration.
## 1. High-Level Architecture

### The Vault (Single Source of Truth): Hosted on the ZimaBoard (6TB HDD). Contains agents/, skills/, memories/, projects/, and Raw Logs

### The Sync Engine: Syncthing (already running) Ensures the Vault is Mirrored to Your Local Obsidian Client and the Friend's Local Obsidian Client

### The Orchestrator (ZimaBoard): Runs OpenClaw

It manages the "state" of tasks, routes prompts to the vault, and triggers execution scripts. It has no inbound internet access (except your SSH).

### The Compute Node (Friend's Workstation): Runs Claude CLI (or Similar Local LLM runner) and the Heavy Lifting Agents

It pulls tasks from the Vault, executes them, and pushes results back. It has controlled egress (only to specific APIs or internal network).

### The Interface

Obsidian: For human reading, editing, and reviewing agent outputs.
ZimaOS Native Chat: Acts as the "Command Center" to trigger OpenClaw workflows or query the vault status.
## 2. Security & Network Topology
To protect the workstation while allowing agent interaction:

A. ZimaBoard (The Bastion)
Firewall (UFW/iptables):


INBOUND: Block ALL. Allow Port 22 (SSH) only from your specific IP. Allow Syncthing discovery ports (UDP/TCP 21027, 22000) only from the Workstation's IP.
OUTBOUND: Allow HTTPS (for OpenClaw to fetch tools/models if needed, or for Syncthing to talk to relay servers if direct connection fails).

Network Isolation: If possible, put the ZimaBoard and Workstation on a dedicated VLAN. 

The Workstation initiates connections to the ZimaBoard; the ZimaBoard never initiates connections to the Workstation.


### B. The Workstation (The Compute Engine)

Egress Control: Configure firewall rules to allow outbound traffic only to:

The ZimaBoard's IP (for pulling/pushing tasks via Syncthing or SSH).

Specific LLM API endpoints (if using cloud models) or localhost (if running local models).

DNS and NTP.

No Inbound: No ports open to the internet.

### C. The "Air Gap" Logic

The agents on the Workstation never receive direct commands from the internet. They only "wake up" when the ZimaBoard drops a new task file into the inbox/ folder (via Syncthing). The Workstation polls or watches this folder.

## 3. The Shared Obsidian Vault Structure
Design the vault to be "Agent-Readable" and "Human-Readable."

/Shared-Vault
├── .obsidian/              # Config (synced, but ignore plugin binaries if possible)
├── 00-Inbox/               # Drop zone for new tasks (Human or Agent created)
│   ├── task-2026-03-10-001.md
│   └── task-2026-03-10-002.md
├── 01-Memories/            # Long-term context, RAG index, world state
│   ├── user-preferences.md
│   ├── project-history.md
│   └── agent-logbook.md
├── 02-Skills/              # Reusable agent "functions" (Markdown specs or Python scripts)
│   ├── web_researcher.md   # Prompt template + tool definition
│   └── code_reviewer.py
├── 03-Agents/              # Active agent instances and state
│   ├── active_agents.json  # Who is working on what?
│   └── agent-logs/         # Raw stdout/stderr from agents
├── 04-Projects/            # The actual work output
│   └── project-alpha/
│       ├── plan.md
│       ├── artifacts/      # Generated code, images, reports
│       └── review.md       # Human feedback loop
└── 99-Archives/            # Completed tasks

Key Mechanism:

#### Task Creation: You drop a .md file in 00-Inbox.

#### Sync: Syncthing replicates it to the Workstation.

#### Execution: The Workstation's agent detects the new file, reads the 02-Skills for context, executes the task, and writes the result to 04-Projects.

#### Review: You see the new file in your Obsidian and review it.

## 4. Orchestration Logic: OpenClaw vs. Claude CLI

This is the "Best of Both Worlds" split.

### Role of OpenClaw (Running on ZimaBoard) The Manager: It does not think; it routes.

Function:
Scans 00-Inbox for new tasks.
Reads the task metadata (priority, required skill).
Updates 03-Agents/active_agents.json to claim the task.
Triggers a script (via SSH or local cron) on the Workstation to "Process Task X".
Monitors the 04-Projects folder for completion signals.

#### Why here? It keeps the orchestration logic lightweight and secure. It doesn't need GPU power.


### Role of Claude CLI / Local LLM (Running on Workstation) The Worker: It thinks and executes

Function:

Receives the "Task X" signal (via a simple shell script triggered by OpenClaw or a local file watcher).

Loads the context from 01-Memories and 02-Skills (RAG).

Executes the task (writes code, fetches data, generates text).

Writes the output to 04-Projects.

Updates the task status in the vault to "Done" or "Needs Review".

Integration Pattern: The "Handshake" Script

Create a simple Python/Bash script on the Workstation called agent_runner.sh:

Watches 00-Inbox (using inotifywait or polling).

When a new file appears:

Locks the file (to prevent race conditions).
Calls claude-cli --context "01-Memories" --skill "02-Skills/web_researcher.md" --task "00-Inbox/task.md".
Saves output to 04-Projects.
Moves task to 99-Archives or marks as "Review Needed".
## 5. Implementation Steps

### Step 1: ZimaBoard Hardening
Firewall: Set UFW to default deny incoming. Allow SSH (Port 22) from your IP only.
Syncthing: Configure the folder to only accept connections from the Workstation's device ID. Disable "Global Discovery" if possible, or restrict it.
### Install OpenClaw: Deploy OpenClaw via Docker. Configure it to watch the /vault/00-Inbox directory.

### Step 2: Workstation Setup
Mount Remote: Mount the ZimaBoard share (via SSHFS or Syncthing) locally.
Install Agents: Install claude-cli (or your preferred local LLM runner like Ollama + LangChain).

Security: Set up ufw to block all incoming. Allow outgoing only to ZimaBoard IP and necessary APIs.
Watcher Script: Create the agent_runner.sh script to bridge the file system changes to the LLM.

### Step 3: The "ZimaOS Native Chat" Integration

Scenario: You want to ask, "What is the status of Project Alpha?"

Action: You type in ZimaOS Chat.
Backend: The chat backend calls a local script on the ZimaBoard that:
Parses the 03-Agents/active_agents.json.

Reads the latest files in 04-Projects/Project-Alpha.

Returns a summary to the chat UI.

Advanced: You can type "Start Task: Research Quantum Computing" in ZimaOS Chat. This creates a file in 00-Inbox via the ZimaOS API, triggering the whole chain.


## Step 4: Async Collaboration Workflow

### You (User A): Create task-research-ai-trends.md in 00-Inbox on your laptop.

### Sync: Syncthing pushes this to ZimaBoard, then to Friend's Workstation.

### Orchestration: OpenClaw on ZimaBoard sees the file, logs "Task Assigned," and triggers the Workstation script.

### Execution: Friend's Workstation (running the agent) picks up the task, uses local LLM to research, writes research-summary.md in 04-Projects.

### Notification: The agent updates the task file with a "Status: Done" header.

### Review: You get a notification (or just open Obsidian later) and see the new file. You edit it, add comments, and move it to 99-Archives.

## 6. Critical Considerations

Conflict Resolution: Syncthing handles binary conflicts, but text conflicts in Obsidian can be messy.

Solution: Enforce a naming convention where agents create unique filenames (e.g., agent-output-UUID.md). Humans should only edit the "Review" or "Final" versions, not the raw agent output.

Latency: Since this is async, don't expect real-time chat. The "loop" is: Drop Task -> Wait (minutes/hours) -> Review Output.

Context Window Management: The 01-Memories folder can grow large.
Solution: Implement a "Summarizer Agent" that runs weekly to compress old logs into a single memory-summary-YYYY-MM.md file, keeping the active context window small.

Secrets: Never store API keys in the Obsidian vault. Use environment variables on the Workstation or a secrets manager (like pass or age) that the agent can read but isn't synced to the vault.

## 7. Why This Works
Security: The heavy compute (Workstation) is behind a firewall and only talks to the ZimaBoard. The ZimaBoard is the only point of entry, and it's locked down.

Collaboration: Obsidian provides a familiar, visual interface for both humans to see the "state" of the system.

Scalability: You can add more "Worker" nodes (other laptops) that just sync the vault and run the agent_runner.sh script. OpenClaw on the ZimaBoard can distribute tasks to any available worker.

This setup effectively turns your ZimaBoard into a secure, distributed task queue and your Obsidian vault into a living, breathing knowledge base that agents can read from and write to, all while keeping your powerful workstation isolated from the public internet.


## why not to use git

Thought about this
The user is asking about alternatives to Syncthing for syncing Obsidian vaults, specifically mentioning Git-based solutions like Obsidian Git, Flowershow, Quartz, and other "digital garden" style publishing tools. They want to know if these would be cleaner or better than Syncthing for their use case.

This is a technical question about Obsidian sync solutions. I should provide a balanced comparison of the options they mentioned, along with considerations for their specific architecture (ZimaBoard + Workstation setup with agents).

Let me think about what I know:

Obsidian Git - Uses Git for version control and sync. Good for version history, but requires Git knowledge and can be slower for large files.

Flowershow - A digital garden publishing tool that can sync with Obsidian. More focused on publishing than syncing.

Quartz - Similar to Flowershow, a static site generator for Obsidian vaults. Again, more about publishing than real-time sync.

Syncthing - Peer-to-peer file sync, no central server needed, works well for continuous sync.

For their specific use case (shared vault with agents writing files, async collaboration, security considerations), I should analyze:

Conflict resolution
Version history
Performance with large files (they have 6TB storage)
Security implications
Ease of use for both humans and agents
Whether publishing features matter for their use case
I don't need to use web search for this - this is well-established technical information about these tools that I can discuss from general knowledge. However, I could search for any recent updates or changes to these tools if needed.

Let me provide a thoughtful comparison without needing to search, as this is general technical knowledge about these tools.

Great question. For your specific architecture (ZimaBoard + Workstation + Agents), the choice depends on whether you prioritize version history, conflict resolution, or simplicity. Here's a breakdown:

Git-Based Solutions (Obsidian Git, Quartz, Flowershow)
Feature	Pros	Cons
Version History	Excellent. Every change is committed. Easy rollback.	Can become bloated with agent-generated noise.
Conflict Resolution	Git handles merges, but Obsidian files often conflict on simultaneous edits.	Requires manual conflict resolution for binary or complex markdown.
Publishing	Quartz/Flowershow turn vaults into static sites automatically.	Extra complexity if publishing isn't your primary goal.
Security	SSH keys for remote repos. Fine-grained access control.	Git credentials need careful management across devices.
Performance	Slower for large files. Git operations add latency.	Not ideal for 6TB with frequent agent writes.
Verdict: Git is excellent for human-authored content where version history matters. But for agent-generated outputs, the commit noise can become overwhelming.

Syncthing (Your Current Choice)
Feature	Pros	Cons
Real-Time Sync	Near-instant. No commit overhead.	No built-in version history (though you can enable file versioning).
Conflict Handling	Creates .sync-conflict files automatically.	Requires manual cleanup of conflicts.
Performance	Handles large files and directories efficiently.	Initial sync can be slow for 6TB.
Security	End-to-end encrypted. No central server.	Trust model relies on device authentication.
Agent-Friendly	Simple file watching. No Git hooks needed.	No atomic operations for multi-file writes.
Verdict: Syncthing is cleaner for your agent workflow. Agents can write files without worrying about Git staging, committing, or merge conflicts.

Hybrid Recommendation for Your Setup
Given your architecture (ZimaBoard as orchestrator, Workstation as compute, Obsidian as interface), I'd recommend:

Primary: Syncthing
Use it for the live vault that agents read/write to.
Enable file versioning in Syncthing settings (keeps deleted/modified file versions for recovery).
Configure ignore patterns to exclude agent temp files (*.tmp, __pycache__/, etc.).
Secondary: Git for Archival
Run a separate Git repository on the ZimaBoard for 99-Archives/.
Once a week, a script can snapshot completed projects into Git for long-term version history.
This gives you the best of both worlds: fast sync for active work, versioned history for completed work.
Publishing (Optional)
Quartz or Flowershow can run as a separate container on ZimaBoard.
Point them at a read-only copy of the vault (not the live sync folder).
This way, publishing doesn't interfere with agent operations.
Security Considerations
Solution	Internet Exposure	Credential Risk
Syncthing	None (P2P only)	Device IDs only
Git (GitHub/GitLab)	Yes (remote repo)	SSH keys/tokens
Obsidian Sync (Official)	Yes (Proton servers)	Account credentials
For your security goals (blocking incoming connections, protecting the workstation), Syncthing wins. It requires no external credentials and no inbound ports beyond the initial handshake.

Final Recommendation
Stick with Syncthing for your core vault. It's simpler, faster, and more compatible with agent workflows. Add Git only if you need formal version history for archival purposes.

If you want to explore Quartz/Flowershow for publishing, run them as separate containers that pull from a snapshot of the vault, not the live sync folder. This keeps your orchestration clean and prevents publishing processes from interfering with agent operations.