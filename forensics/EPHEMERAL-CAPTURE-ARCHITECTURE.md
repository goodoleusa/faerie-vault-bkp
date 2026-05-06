# Ephemeral Artifact Capture Architecture

**Mission:** Real-time capture of session artifacts (transcripts, responses, bash output, errors, COT, prompts) with zero main context burden.

**Design Principle:** Async, non-blocking hook-based capture. All I/O operations run in subprocess, main thread never waits. Artifacts stored immediately in forensics/ephemeral/ with complete lineage in filename.

---

## 1. Hook Architecture

### 1.1 Hook Points (Claude Code Harness Integration)

**Hook Name** | **Trigger Event** | **Payload** | **Async** | **Purpose**
---|---|---|---|---
`pre-submit` | User submits prompt before API call | `{ prompt, user_message, timestamp }` | Yes | Capture user intent before processing
`post-submit` | API returns response from Claude | `{ response_full, response_text, prompt_hash, timestamp }` | Yes | Capture complete API response before UI filtering
`post-tool-call` | Tool executes (Bash, Read, Edit, etc) | `{ tool_name, args, stdout, stderr, exit_code, timestamp }` | Yes | Capture bash output, tool invocations
`post-error` | Exception or error caught | `{ error_type, error_msg, stack_trace, timestamp }` | Yes | Capture errors for debugging
`session-checkpoint` | Session starts / resumes | `{ session_id, cwd, investigation_label, timestamp }` | Yes | Metadata snapshot for lineage

### 1.2 Hook Integration Method

Hooks defined in `.claude/settings.json` under `hooks:` key. Each hook specifies:
- **trigger:** event name (pre-submit, post-submit, post-tool-call, post-error, session-checkpoint)
- **script:** command to run (invokes 8x_ephemeral_capture.py subcommand)
- **async:** boolean (true = fire-and-forget, main continues)
- **timeout_ms:** max time before kill (default 5000ms; ephemeral capture must finish quickly)

**Example hook config:**
```json
{
  "hooks": {
    "pre-submit": {
      "trigger": "pre-submit",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-prompt",
      "async": true,
      "timeout_ms": 2000
    },
    "post-submit": {
      "trigger": "post-submit",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-response",
      "async": true,
      "timeout_ms": 3000
    },
    "post-tool": {
      "trigger": "post-tool-call",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-bash-output",
      "async": true,
      "timeout_ms": 1000
    },
    "post-error": {
      "trigger": "post-error",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-error",
      "async": true,
      "timeout_ms": 1000
    }
  }
}
```

### 1.3 Data Flow: Hook → Stdin → Script → Artifact

Harness passes event payload to script via stdin (JSON-encoded). Script:
1. Reads stdin (non-blocking, with timeout)
2. Parses JSON payload
3. Extracts task_id and session_id from environment
4. Constructs artifact filename per forensic standard
5. Writes to async queue (in-memory, buffered)
6. Returns immediately (async never blocks)

**Key constraint:** Hook must complete in <timeout_ms. Slow artifact writes must be batched and flushed asynchronously in background.

---

## 2. Artifact Storage & Organization

### 2.1 Ephemeral Folder Structure

```
forensics/ephemeral/
  transcripts/
    2026-04-28/
      14-48-56Z_transcript_design-ephemeral-capture-w1_session-abc123de_001.jsonl
      14-48-57Z_transcript_design-ephemeral-capture-w1_session-abc123de_002.jsonl
  responses/
    2026-04-28/
      14-48-56Z_response_design-ephemeral-capture-w1_session-abc123de_001.json
  bash-output/
    2026-04-28/
      14-48-56Z_bash-output_design-ephemeral-capture-w1_session-abc123de_001.jsonl
  errors/
    2026-04-28/
      14-48-56Z_error_design-ephemeral-capture-w1_session-abc123de_001.json
  cot/
    2026-04-28/
      14-48-56Z_cot_design-ephemeral-capture-w1_session-abc123de_001.txt
  prompts/
    2026-04-28/
      14-48-56Z_prompt_design-ephemeral-capture-w1_session-abc123de_001.txt
  metadata/
    2026-04-28/
      14-48-56Z_metadata_design-ephemeral-capture-w1_session-abc123de_001.json
```

### 2.2 Filename Standard

```
{HH-MM-SS}Z_{artifact_type}_{task_id}_{session_id8}_{counter}.{ext}
```

- **{HH-MM-SS}Z:** UTC timestamp (hour-minute-second, 'Z' suffix)
- **{artifact_type}:** transcript, response, bash-output, error, cot, prompt, metadata
- **{task_id}:** from environment variable TASK_ID (e.g., "design-ephemeral-capture-w1")
- **{session_id8}:** first 8 chars of session ID (e.g., "abc123de")
- **{counter}:** increments per (timestamp, type, task_id, session) within same second (001, 002, ...)
- **{ext}:** jsonl (streaming), json (object), txt (plain text)

**Example filename:**
```
14-48-56Z_transcript_design-ephemeral-capture-w1_abc123de_001.jsonl
```

### 2.3 File Formats

**Transcripts (JSONL):** One JSON object per line, stream-friendly
```jsonl
{"timestamp": "2026-04-28T14:48:56Z", "role": "user", "content": "...", "turn": 1}
{"timestamp": "2026-04-28T14:48:58Z", "role": "assistant", "content": "...", "turn": 1}
```

**Responses (JSON):** Complete API response object
```json
{
  "timestamp": "2026-04-28T14:48:58Z",
  "prompt_hash": "sha256:abc123...",
  "response_full": { ... Claude API response ... },
  "response_text": "...",
  "tokens_in": 1234,
  "tokens_out": 5678
}
```

**Bash Output (JSONL):** Per-tool invocation
```jsonl
{"timestamp": "...", "tool": "Bash", "command": "...", "stdout": "...", "stderr": "...", "exit_code": 0}
{"timestamp": "...", "tool": "Read", "path": "...", "content_preview": "...(first 500 chars)..."}
```

**Errors (JSON):** Exception snapshot
```json
{
  "timestamp": "2026-04-28T14:48:59Z",
  "error_type": "TimeoutError",
  "error_msg": "Hook post-submit timeout",
  "stack_trace": "...",
  "context": { "last_tool": "Bash", "last_command": "..." }
}
```

**COT (TXT):** Chain-of-thought reasoning (raw text)
```
14:48:56Z — Analyzing hook architecture requirements
  • Need zero-context overhead → async writes
  • Need complete lineage → filename contains task_id + session_id
  • Need streaming support → JSONL format
14:48:58Z — Designing artifact storage layout
  ...
```

**Prompts (TXT):** User message + system context before submission
```
=== SYSTEM CONTEXT ===
[Global HONEY.md first 500 chars]
[Project HONEY.md first 500 chars]
[Investigation label if any]

=== USER MESSAGE ===
[Complete user input]

=== TIMESTAMP ===
2026-04-28T14:48:56Z
```

**Metadata (JSON):** Session snapshot
```json
{
  "timestamp": "2026-04-28T14:48:56Z",
  "session_id": "abc123de...",
  "task_id": "design-ephemeral-capture-w1",
  "investigation_label": "terminology-cleanup-sprint",
  "cwd": "/mnt/d/0local/gitrepos/faerie-vault",
  "repo_root": "/mnt/d/0local/gitrepos/faerie-vault",
  "environment": {
    "USER": "goodoleusa",
    "TASK_ID": "design-ephemeral-capture-w1",
    "SESSION_ID": "abc123de..."
  }
}
```

---

## 3. Async Write Strategy

### 3.1 In-Memory Buffer + Batch Flusher

**Architecture:**
1. Hook receives event payload via stdin
2. Parses JSON, constructs artifact record
3. Appends to in-memory buffer (per artifact type)
4. Returns immediately (hook finishes in <100ms)
5. Background flusher thread periodically writes buffers to disk (every 2–5 seconds or when buffer exceeds 10MB)

**Buffer structure (pseudocode):**
```python
class EphemeralBuffer:
    def __init__(self):
        self.buffers = {
            'transcript': [],
            'response': [],
            'bash-output': [],
            'error': [],
            'cot': [],
            'prompt': [],
            'metadata': []
        }
        self.lock = threading.RLock()
        self.flusher_thread = None
    
    def append(self, artifact_type: str, record: dict):
        with self.lock:
            self.buffers[artifact_type].append(record)
    
    def flush(self, artifact_type: str = None):
        """Flush one or all buffers to disk (async, non-blocking)"""
        with self.lock:
            types = [artifact_type] if artifact_type else self.buffers.keys()
            for atype in types:
                if self.buffers[atype]:
                    self._write_batch(atype, self.buffers[atype])
                    self.buffers[atype] = []
    
    def _write_batch(self, artifact_type: str, records: list):
        """Write batch to disk (runs in subprocess)"""
        # Delegates to background process (non-blocking)
        pass
```

### 3.2 Rotation & Archival

**Local retention:** Keep 7 days of ephemeral artifacts in forensics/ephemeral/{YYYY-MM-DD}/
**Archival trigger:** Daily cron job (22:00 UTC) runs:
```bash
python3 ./.claude/scripts/8x_ephemeral_capture.py rotate-archive
```

**Archive action:**
1. Find all forensics/ephemeral/{YYYY-MM-DD}/ folders older than 7 days
2. Tar + gzip: `forensics/ephemeral/archive/ephemeral-{YYYY-MM-DD}.tar.gz`
3. Calculate SHA256 hash of archive
4. Write COC entry to forensics/coc.jsonl (immutable audit log)
5. Delete source folder (keep archive only)
6. Upload archive to S3/B2 (WORM bucket) if configured

**Size limits:**
- Per-file: 50MB (ephemeral transcripts can grow large)
- Per-day: 1GB (rotate aggressively if exceeded)
- Rotation triggered early if daily size > 500MB

### 3.3 Subprocess Strategy (Zero Main Context Burden)

**Flusher runs in detached subprocess:**
```bash
# Main thread spawns background flusher (parent does NOT wait)
python3 ./.claude/scripts/8x_ephemeral_capture.py flusher \
  --interval 5 \
  --buffer-size-threshold 10485760 \
  --pidfile /tmp/ephemeral-flusher.pid \
  &
```

**Flusher subprocess:**
- Registers signal handler for SIGTERM (graceful shutdown)
- Polls in-memory buffer every N seconds
- Writes any pending records to disk
- Exits when signal received or buffer empty + idle for 30s
- Main never waits for flusher; flusher is fire-and-forget

**Race condition prevention:**
- File-level locks (fcntl) for append-only writes
- Atomic rename: write to .tmp, then rename to final name
- Counter collision handled: if filename exists, increment counter

---

## 4. Hook Configuration (settings.json)

### 4.1 Hook Definitions

```json
{
  "hooks": {
    "pre-submit": {
      "description": "Capture user prompt before API submission",
      "trigger": "pre-submit",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-prompt",
      "async": true,
      "timeout_ms": 2000,
      "env": {
        "EPHEMERAL_ROOT": "{repo}/.claude/forensics/ephemeral",
        "CAPTURE_METADATA": "true"
      }
    },
    "post-submit": {
      "description": "Capture Claude response (full, before UI filtering)",
      "trigger": "post-submit",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-response",
      "async": true,
      "timeout_ms": 3000,
      "env": {
        "EPHEMERAL_ROOT": "{repo}/.claude/forensics/ephemeral",
        "CAPTURE_TOKENS": "true"
      }
    },
    "post-tool-call": {
      "description": "Capture tool outputs (Bash, Read, Edit, etc)",
      "trigger": "post-tool-call",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-bash-output",
      "async": true,
      "timeout_ms": 1500,
      "env": {
        "EPHEMERAL_ROOT": "{repo}/.claude/forensics/ephemeral",
        "CAPTURE_STDOUT": "true",
        "CAPTURE_STDERR": "true"
      }
    },
    "post-error": {
      "description": "Capture errors and exceptions for debugging",
      "trigger": "post-error",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-error",
      "async": true,
      "timeout_ms": 1000,
      "env": {
        "EPHEMERAL_ROOT": "{repo}/.claude/forensics/ephemeral",
        "CAPTURE_STACK": "true"
      }
    },
    "session-init": {
      "description": "Capture session metadata on start",
      "trigger": "session-checkpoint",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py capture-metadata",
      "async": true,
      "timeout_ms": 1000,
      "env": {
        "EPHEMERAL_ROOT": "{repo}/.claude/forensics/ephemeral"
      }
    }
  },
  "cron": {
    "ephemeral-rotate": {
      "description": "Archive old ephemeral artifacts daily",
      "schedule": "0 22 * * *",
      "script": "python3 ./.claude/scripts/8x_ephemeral_capture.py rotate-archive",
      "timeout_ms": 30000
    }
  }
}
```

### 4.2 Environment Variables

Scripts can read these from harness:
- `TASK_ID`: Current task identifier
- `SESSION_ID`: Unique session identifier
- `INVESTIGATION_LABEL`: Investigation label (if bound)
- `CLAUDE_HOME`: Global .claude home
- `REPO_ROOT`: Repo root directory
- `CWD`: Current working directory

---

## 5. Pseudocode: 8x_ephemeral_capture.py

See separate file: `8x_ephemeral_capture.py` (100–150 lines)

Key subcommands:
- `capture-prompt` — Save user message + system context
- `capture-response` — Save Claude API response (full)
- `capture-bash-output` — Save tool invocation results
- `capture-error` — Save exception snapshot
- `capture-metadata` — Save session metadata
- `flusher` — Background daemon for batched writes
- `rotate-archive` — Archive old artifacts to S3/B2

---

## 6. Zero-Context-Burden Guarantees

### 6.1 Main Thread Never Blocks

- All hooks marked `async: true`
- Hook script returns immediately after queuing (100ms max)
- Flusher runs in separate process (main doesn't wait)
- File I/O happens in subprocess, not main

### 6.2 Minimal Memory Footprint

- In-memory buffer capped at 10MB per type
- Exceeds threshold → immediate flush to disk
- Old rotated artifacts deleted locally (only archive remains)

### 6.3 No Task_id Leakage

- Artifacts always namespaced by task_id
- Grep for task_id in forensics/ephemeral/ → all artifacts for that task
- Discovery via `ls forensics/ephemeral/*/2026-04-28/*task_id*`

---

## 7. Forensic Integrity

All ephemeral artifacts:
- Named with complete lineage (task_id, session_id, timestamp in filename)
- Stored in forensics/ (system of record)
- Hash-chained: SHA256(content) written to COC entry
- Append-only: never overwritten, only archived
- Court-ready: complete audit trail available via `6x_forensic_recovery.py recover task-123`

---

## 8. Implementation Checklist (W2 CRUISE)

- [ ] Write 8x_ephemeral_capture.py (150 lines, 5 subcommands, flusher daemon)
- [ ] Add hook definitions to settings.json
- [ ] Wire background flusher startup on session init
- [ ] Implement rotation + archival (daily cron)
- [ ] Add COC logging for all ephemeral writes
- [ ] Test: hook-to-artifact latency (<100ms)
- [ ] Test: buffer overflow behavior (>10MB → immediate flush)
- [ ] Test: concurrent writes from multiple hooks
- [ ] Test: graceful flusher shutdown on session exit
- [ ] Integration: forensic recovery includes ephemeral artifacts

---

## 9. Related Docs

- `docs/FORENSIC-INTEGRITY.md` — System of record, COC chain, deletion safety
- `docs/MAIN-CONTEXT-DISCIPLINE.md` — Why zero-burden is critical
- `./.claude/scripts/6x_forensic_recovery.py` — Recovery entry point
- `./.claude/scripts/0x_coc_writer.py` — COC audit logging
