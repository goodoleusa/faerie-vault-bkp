
● Stigmergy in the wild: breadcrumb trail in predictable places.

  Agent doing websearch on domains. Hits rate limit. Session crashes. Agent never returns. But stigmergy left:

  The trail (in order of freshness):

  1. Stream file — the primary signal:
  tail -n 1 ~/.claude/memory/streams/{TASK_ID}.jsonl
  # {"timestamp": "2026-03-30T00:32:15Z", "type": "finding", "content": "Found 23 domains, next batch pending",
  "entry_hash": "a7c2..."}
  2. Last confirmed thought. Timestamp. Entry hash.
  3. COC chain break — shows exactly where it died:
  tail -n 3 ~/.claude/memory/forensics/forensic-coc.jsonl | jq '.entry_hash, .agent_id, .tool, .timestamp'
  # Shows: websearch tool call at 00:32:14Z, then silence
  # Agent 2 can resume from that entry_hash
  4. Scratch MEM blocks — unfinished reasoning:
  grep "<!-- MEM" {repo}/.claude/memory/scratch-{SID}.md | tail -3
  # Shows: incomplete analysis, working hypothesis, what was being attempted
  5. Task state — claim tracking:
  python3 ~/.claude/hooks/state/queue_ops.py status {TASK_ID}
  # claimed_by: {SESSION_ID} | claimed_at: 12 mins ago | still in-progress
  # If elapsed > 2x expected time → orphaned task
  6. Vault draft — partial work product:
  ls {vault}/00-SHARED/Agent-Outbox/data-engineer/ | grep -i domain
  # domain-search-DRAFT.md | status: in-progress
  # Next agent reads frontmatter, sees what's done, continues

  Recovery (new agent reading the trail):

  # Step 1: what was the intent?
  tail ~/.claude/memory/streams/{TASK_ID}.jsonl  # See: "23/50 domains found"

  # Step 2: where exactly did it stop?
  tail ~/.claude/memory/forensics/forensic-coc.jsonl | jq .entry_hash  # hash: a7c2...

  # Step 3: what's the working hypothesis?
  grep "cat=OBSERVATION\|cat=IDEA" {repo}/.claude/memory/scratch-{SID}.md  # Extract reasoning

  # Step 4: any partial results in vault?
  cat {vault}/00-SHARED/Agent-Outbox/data-engineer/domain-search-DRAFT.md  # Grab what was found

  # Step 5: claim and continue
  python3 ~/.claude/hooks/state/queue_ops.py claim --task {TASK_ID} --resume-from-entry a7c2...
  # Agent 2 now picks up: search domains 24-50, append to existing results

  The pheromone is the file itself.

  No heartbeat, no connection protocol, no "I'm alive" messages. Just: "My work speaks for itself. Here's the
  timestamp, the hash chain, the partial results. If I vanish, follow the breadcrumbs in order of freshness."

  This survives context crashes, network partitions, even the human closing their laptop. Any agent who reads those
  predictable paths can reconstruct intent + state + progress and continue without asking.

  That's stigmergy in the wild: the filesystem as distributed memory, hash-verified, ordered by timestamp, no central
  authority.