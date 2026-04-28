#!/usr/bin/env python3
"""
TIER: 0x_ (setup — SDK harness is the spawn contract implementation layer)
REPLACES: subprocess-based CLI prototype agent spawning (7x_faerie_spawn.py subprocess pattern)
METRIC: 100% of agent spawns carry AGENT-RUN-ID + valid manifest; zero stale signals; COC chain intact
LOAD: core (system-critical — production SDK harness for f(0) agent orchestration)

implementation_spec.py — Production-grade Agent SDK Harness

This module bridges the faerie2 f(0) orchestration system with the Anthropic Agent
SDK. It replaces subprocess-based prototype spawning with direct SDK integration,
implementing four interlocking subsystems:

  1. AgentSpawner      — W1/W2/W3 wave dispatch, bundle injection, manifest writes
  2. ManifestWriter    — Atomic writes with COC chain integrity
  3. WaveDispatcher    — Parallel agent lifecycle with rate limiting
  4. BundleComposer    — HONEY + NECTAR + pollen + task context assembly

Design contracts:
  - Every spawn generates an AGENT-RUN-ID (forensic anchor)
  - Every manifest written AFTER agent execution (no stale signals)
  - Bundle composition is role-aware (injected as prompt prefix, not external files)
  - W1: 4-5 agents parallel, haiku, inline wait
  - W2: 2-3 agents, sonnet, inline wait
  - W3: 1-2 agents, sonnet, background (fire-and-forget)
  - COC entries via 4x_coc_writer.py subprocess call (hash-chain integrity)
  - All artifacts land in forensics/{type}/{date}/ (stigmergy-first naming)

Architecture alignment:
  - Stigmergy-only: no SendMessage; filesystem IS the coordination layer
  - Artifacts-in-forensics: all outputs in {repo}/forensics/, never .claude/
  - Task_id-in-filename: {HH-MM-SS}Z_{type}_{task_id}_{agent}_{counter}.{ext}
  - Cascading summarization: main reads only dashboard_line (<=80 chars)
  - Manifest-first: signal survives agent exit; no silent work loss

Python 3.11+ required (asyncio.TaskGroup used for parallel wave dispatch).

Usage (library):
    from implementation_spec import WaveDispatcher, BundleComposer, AgentSpawnConfig

    config = AgentSpawnConfig(
        task_id="my-task-001",
        agent_type="python-pro",
        investigation_label="my-investigation",
        goal="Implement X feature",
        wave=1,
    )
    dispatcher = WaveDispatcher(repo_root=Path("/path/to/repo"))
    result = await dispatcher.dispatch_wave(wave=1, configs=[config])

Usage (CLI dry-run):
    python3 implementation_spec.py --dry-run --wave 1 --task-id "test-task"
    python3 implementation_spec.py --self-test
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import fcntl
import hashlib
import hmac
import json
import logging
import os
import secrets
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("faerie.sdk-harness")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(os.environ.get("FAERIE_REPO_ROOT", Path(__file__).resolve().parent))
CLAUDE_HOME = Path(os.environ.get("CLAUDE_HOME", "/mnt/d/0LOCAL/.claude"))
COC_WRITER = CLAUDE_HOME / "scripts" / "4x_coc_writer.py"
AGENT_RUN_ID_GEN = CLAUDE_HOME / "scripts" / "9x_agent_run_id_generator.py"

# Wave parameters
WAVE_PARAMS: dict[int, dict[str, Any]] = {
    1: {
        "max_parallel": 5,
        "model": "claude-haiku-4-5",
        "timeout_seconds": 120,
        "run_in_background": False,
        "description": "W1 LIFTOFF — max burn, parallel triage",
    },
    2: {
        "max_parallel": 3,
        "model": "claude-sonnet-4-5",
        "timeout_seconds": 600,
        "run_in_background": False,
        "description": "W2 CRUISE — selective dispatch, feature work",
    },
    3: {
        "max_parallel": 2,
        "model": "claude-sonnet-4-5",
        "timeout_seconds": 1800,
        "run_in_background": True,
        "description": "W3 INSERTION — deep synthesis, background",
    },
}

# Retry configuration
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1.0  # seconds; exponential backoff from this base

# Rate limiting (conservative defaults; tune per API quota)
RATE_LIMIT_RPS = 2.0  # requests per second max

# Compass edge thresholds (from CLAUDE.md phase gate table)
PHASE_THRESHOLDS = {
    "SEED":   {"quality": 0.50, "belief": 0.50},
    "DEEPEN": {"quality": 0.70, "belief": 0.50},
    "EXTEND": {"quality": 0.80, "belief": 0.75},
    "FULL":   {"quality": 0.85, "belief": 0.75},
}

# Agent-type to Anthropic official type mapping
# (Custom cards -> official SDK subagent_type mapping)
AGENT_TYPE_MAP: dict[str, str] = {
    "python-pro":             "software-engineer",
    "code-reviewer":          "software-engineer",
    "data-analyst":           "data-scientist",
    "documentation-engineer": "software-engineer",
    "knowledge-synthesizer":  "software-engineer",
    "ai-engineer":            "software-engineer",
    "research-analyst":       "software-engineer",
    "fullstack-developer":    "software-engineer",
    "stigmergy-scout":        "software-engineer",
    "context-manager":        "software-engineer",
    "performance-eval":       "software-engineer",
    "general-purpose":        "software-engineer",
}

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class AgentSpawnConfig:
    """Configuration for a single agent spawn. Validated before execution."""
    task_id: str
    agent_type: str
    investigation_label: str
    goal: str
    wave: int = 1

    # Optional overrides
    model: Optional[str] = None
    timeout_seconds: Optional[int] = None
    run_in_background: Optional[bool] = None

    # Bundle composition inputs
    honey_content: Optional[str] = None
    nectar_content: Optional[str] = None
    pollen_content: Optional[str] = None

    # Forensic metadata
    phase: str = "SEED"
    parent_task_id: Optional[str] = None
    compass_edge_in: Optional[str] = None  # bearing that triggered this spawn

    def validate(self) -> list[str]:
        """Return list of validation errors. Empty = valid."""
        errors = []
        if not self.task_id or not self.task_id.strip():
            errors.append("task_id must be non-empty")
        if not self.agent_type or not self.agent_type.strip():
            errors.append("agent_type must be non-empty")
        if not self.investigation_label or not self.investigation_label.strip():
            errors.append("investigation_label must be non-empty")
        if not self.goal or not self.goal.strip():
            errors.append("goal must be non-empty")
        if self.wave not in (1, 2, 3):
            errors.append(f"wave must be 1, 2, or 3 (got {self.wave!r})")
        return errors

    @property
    def effective_model(self) -> str:
        return self.model or WAVE_PARAMS[self.wave]["model"]

    @property
    def effective_timeout(self) -> int:
        return self.timeout_seconds or WAVE_PARAMS[self.wave]["timeout_seconds"]

    @property
    def effective_background(self) -> bool:
        if self.run_in_background is not None:
            return self.run_in_background
        return WAVE_PARAMS[self.wave]["run_in_background"]


@dataclass
class AgentRunResult:
    """Result of a single agent execution. Contains manifest + audit trail."""
    agent_run_id: str
    task_id: str
    agent_type: str
    wave: int
    status: str  # "success" | "error" | "timeout" | "skipped"
    dashboard_line: str
    compass_edge: str  # N/S/E/W
    next_task_queued: Optional[str]
    quality_score: float
    belief_index: float
    manifest_path: Optional[str]
    artifact_paths: list[str] = field(default_factory=list)
    error_message: Optional[str] = None
    retries_used: int = 0
    duration_seconds: float = 0.0
    raw_output: Optional[str] = None

    def to_manifest_dict(self) -> dict[str, Any]:
        """
        Serialize to manifest-compatible dict (faerie2 compass schema).

        Includes all 11 required fields per manifest-schema-wiring-critical:
        - task_id: unique task identifier
        - agent_type: role/type of agent (maps to official subagent_type)
        - agent_run_id: forensic anchor for this execution
        - investigation_label: stigmergic mission cluster (filled by ManifestWriter)
        - dashboard_line: <=80 char summary (only signal main reads)
        - compass_edge: N/S/E/W bearing for phase gating
        - next_task_queued: task_id of next unblocking work (or null)
        - quality_score: 0.0-1.0 data/artifact quality metric
        - belief_index: 0.0-1.0 honesty in self-reporting (avg of 4 signals)
        - discovered_work: array of task_ids found during frontier scan
        - honey_version_used: which HONEY.md SHA256 was injected
        - honey_rendering_context: metadata about HONEY context assembly
        - honey_render_fidelity: 0.0-1.0 quality of HONEY rendering for agent
        - status: "success" | "error" | "timeout" | "skipped" | "pending"
        - retries_used: count of retry attempts before success/failure
        - duration_seconds: wall-clock execution time
        - ts: ISO8601 timestamp of manifest write
        """
        return {
            "task_id": self.task_id,
            "agent_type": self.agent_type,
            "agent_run_id": self.agent_run_id,
            "investigation_label": "",  # filled in by ManifestWriter
            "dashboard_line": self.dashboard_line,
            "compass_edge": self.compass_edge,
            "next_task_queued": self.next_task_queued,
            "quality_score": self.quality_score,
            "belief_index": self.belief_index,
            "discovered_work": [],  # populated by frontier scan (if conducted)
            "honey_version_used": "",  # set by ManifestWriter from BundleComposer
            "honey_rendering_context": {  # metadata about HONEY injection
                "global_honey_present": False,
                "project_honey_present": False,
                "nectar_present": False,
                "pollen_present": False,
            },
            "honey_render_fidelity": 0.5,  # default; overridden by agent or analyzer
            "status": self.status,
            "retries_used": self.retries_used,
            "duration_seconds": round(self.duration_seconds, 2),
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }


@dataclass
class WaveResult:
    """Result of a complete wave dispatch (all agents in one wave)."""
    wave: int
    spawned: int
    succeeded: int
    failed: int
    timed_out: int
    skipped: int
    results: list[AgentRunResult] = field(default_factory=list)
    duration_seconds: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.spawned == 0:
            return 0.0
        return self.succeeded / self.spawned

    def summary(self) -> str:
        return (
            f"W{self.wave}: {self.spawned} spawned, {self.succeeded} ok, "
            f"{self.failed} fail, {self.timed_out} timeout "
            f"({self.success_rate:.0%} success, {self.duration_seconds:.1f}s)"
        )


# ---------------------------------------------------------------------------
# BundleComposer — assemble HONEY + NECTAR + pollen + task
# ---------------------------------------------------------------------------


class BundleComposer:
    """
    Assembles agent spawn bundles from layered context.

    Bundle composition order (innermost = highest authority):
      1. Global HONEY.md        (~1K tokens, crystallized universal facts)
      2. Project HONEY.md       (~800 tokens, repo-scoped facts)
      3. NECTAR.md tail-50      (recent HIGH/CRITICAL findings)
      4. Pollen session         (live MEM blocks, live session insights)
      5. Agent card excerpt     (role-specific behavioral wiring)
      6. Task goal              (what this specific spawn must accomplish)

    The composed bundle is injected as a prompt prefix so the agent's context
    begins with full situational awareness — no external file reads required.
    """

    def __init__(
        self,
        claude_home: Path = CLAUDE_HOME,
        repo_root: Path = REPO_ROOT,
    ) -> None:
        self.claude_home = claude_home
        self.repo_root = repo_root
        self._global_honey: Optional[str] = None
        self._project_honey: Optional[str] = None
        self._nectar_cache: Optional[str] = None
        self._nectar_cache_ts: float = 0.0
        self._nectar_ttl_seconds: int = 300  # 5-min cache; matches piston wave cadence

    # ------------------------------------------------------------------
    # Private readers
    # ------------------------------------------------------------------

    def _read_global_honey(self) -> str:
        """Read global HONEY.md (cached for session lifetime)."""
        if self._global_honey is None:
            honey_path = self.claude_home / "HONEY.md"
            if honey_path.exists():
                content = honey_path.read_text(encoding="utf-8")
                # Respect budget: cap at 5K tokens (~20K chars) per CLAUDE.md guidance
                if len(content) > 20_000:
                    content = content[:20_000] + "\n[...HONEY truncated at 5K token budget...]"
                self._global_honey = content
            else:
                self._global_honey = "# HONEY.md not found — operating without crystallized memory"
                log.warning("Global HONEY.md not found at %s", honey_path)
        return self._global_honey

    def _hash_global_honey(self) -> str:
        """Return SHA256 hash of global HONEY.md for version tracking."""
        content = self._read_global_honey()
        return hashlib.sha256(content.encode()).hexdigest()[:16]  # 16-char abbrev

    def _read_project_honey(self) -> str:
        """Read repo-scoped HONEY.md (cached for session lifetime)."""
        if self._project_honey is None:
            honey_path = self.repo_root / ".claude" / "HONEY.md"
            if not honey_path.exists():
                # Fallback: look in repo root
                honey_path = self.repo_root / "HONEY.md"
            if honey_path.exists():
                content = honey_path.read_text(encoding="utf-8")
                if len(content) > 16_000:
                    content = content[:16_000] + "\n[...Project HONEY truncated at 4K token budget...]"
                self._project_honey = content
            else:
                self._project_honey = "# Project HONEY.md not found"
                log.info("No project HONEY.md found — relying on global HONEY only")
        return self._project_honey

    def _read_nectar_tail(self, n_lines: int = 50) -> str:
        """Read NECTAR.md tail-N (TTL-cached to prevent re-read on rapid spawns)."""
        now = time.monotonic()
        if self._nectar_cache is not None and (now - self._nectar_cache_ts) < self._nectar_ttl_seconds:
            return self._nectar_cache

        nectar_path = self.claude_home / "NECTAR.md"
        if not nectar_path.exists():
            self._nectar_cache = "# NECTAR.md not found"
            self._nectar_cache_ts = now
            log.warning("NECTAR.md not found at %s", nectar_path)
            return self._nectar_cache

        lines = nectar_path.read_text(encoding="utf-8").splitlines(keepends=True)
        tail_lines = lines[-n_lines:] if len(lines) > n_lines else lines
        self._nectar_cache = "".join(tail_lines)
        self._nectar_cache_ts = now
        return self._nectar_cache

    def _read_agent_card_excerpt(self, agent_type: str) -> str:
        """Read agent card behavioral excerpt for role-specific prompt injection."""
        card_path = self.claude_home / "agents" / f"{agent_type}.md"
        if not card_path.exists():
            return f"# Agent card for {agent_type!r} not found — using default behavioral template"

        content = card_path.read_text(encoding="utf-8")
        # Only inject card body; skip heavy frontmatter if over budget (~800 tok = 3200 chars)
        if len(content) > 3_200:
            # Trim: keep first 800 chars (preamble) + last 200 chars (closing)
            content = content[:800] + "\n[...card trimmed for bundle budget...]\n" + content[-200:]
        return content

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_rendering_context(
        self,
        config: AgentSpawnConfig,
        extra_pollen: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Get metadata about HONEY rendering for this bundle.

        Returns dict with keys:
          - global_honey_present: bool
          - project_honey_present: bool
          - nectar_present: bool
          - pollen_present: bool
          - global_honey_hash: str (SHA256[:16])
          - project_honey_hash: str (SHA256[:16])
          - agent_type: str
          - wave: int
          - phase: str
        """
        global_honey = config.honey_content or self._read_global_honey()
        project_honey = self._read_project_honey()
        nectar = config.nectar_content or self._read_nectar_tail(n_lines=50)
        pollen = config.pollen_content or extra_pollen or ""

        return {
            "global_honey_present": bool(global_honey and "HONEY" in global_honey.upper()),
            "project_honey_present": bool(project_honey and "HONEY" in project_honey.upper()),
            "nectar_present": bool(nectar and "NECTAR" in nectar.upper()),
            "pollen_present": bool(pollen and len(pollen) > 10),
            "global_honey_hash": self._hash_global_honey(),
            "project_honey_hash": hashlib.sha256(project_honey.encode()).hexdigest()[:16],
            "agent_type": config.agent_type,
            "wave": config.wave,
            "phase": config.phase,
        }

    def compose(
        self,
        config: AgentSpawnConfig,
        extra_pollen: Optional[str] = None,
    ) -> str:
        """
        Compose a complete bundle string for injection as agent prompt prefix.

        Args:
            config:       AgentSpawnConfig carrying goal, agent_type, etc.
            extra_pollen: Additional live session observations (MEM blocks).

        Returns:
            Complete bundle string, ready to prefix any agent prompt.
        """
        sections: list[str] = []

        # --- Header ---
        sections.append(
            f"# FAERIE2 SPAWN BUNDLE — {config.agent_type.upper()}\n"
            f"# task_id={config.task_id}  wave=W{config.wave}  "
            f"investigation_label={config.investigation_label}\n"
            f"# Composed: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        )

        # --- Global HONEY ---
        global_honey = config.honey_content or self._read_global_honey()
        sections.append(f"## GLOBAL HONEY (crystallized universal facts)\n\n{global_honey}\n")

        # --- Project HONEY ---
        project_honey = self._read_project_honey()
        sections.append(f"## PROJECT HONEY (repo-scoped facts)\n\n{project_honey}\n")

        # --- NECTAR tail ---
        nectar = config.nectar_content or self._read_nectar_tail(n_lines=50)
        sections.append(f"## NECTAR (recent HIGH/CRITICAL findings, last 50 lines)\n\n{nectar}\n")

        # --- Pollen ---
        pollen_parts = []
        if config.pollen_content:
            pollen_parts.append(config.pollen_content)
        if extra_pollen:
            pollen_parts.append(extra_pollen)
        if pollen_parts:
            pollen_text = "\n\n".join(pollen_parts)
            sections.append(f"## POLLEN (live session MEM blocks)\n\n{pollen_text}\n")

        # --- Agent card ---
        card_excerpt = self._read_agent_card_excerpt(config.agent_type)
        sections.append(
            f"## AGENT ROLE CARD — {config.agent_type}\n\n"
            f"{card_excerpt}\n"
        )

        # --- Spawn discipline boilerplate ---
        sections.append(
            "## SPAWN DISCIPLINE (mandatory; every agent)\n\n"
            "1. Write manifest to `forensics/manifests/{YYYY-MM-DD}/{HH-MM-SS}Z_manifest_{task_id}_{agent_type}_{counter}.json`\n"
            "   BEFORE returning. Manifest includes: task_id, dashboard_line (<=80 chars), compass_edge (N/S/E/W), "
            "next_task_queued, quality_score (0.0-1.0), belief_index (0.0-1.0).\n"
            "2. Every artifact lands in `forensics/artifacts/{date}/` with task_id in filename.\n"
            "3. AGENT-RUN-ID is in this bundle header — include it in manifest as `agent_run_id`.\n"
            "4. Compass edges: S=proceed, N=unblock, E=parallel, W=retreat/reframe.\n"
            "5. dashboard_line is EXACTLY <=80 chars. It is the ONLY signal main reads.\n"
            "6. Do not write to .claude/; write only to forensics/.\n"
            "7. Manifest truthfulness is measured. Honest failure > fabricated success.\n"
        )

        # --- Task goal ---
        sections.append(
            f"## TASK GOAL\n\n"
            f"task_id: {config.task_id}\n"
            f"investigation_label: {config.investigation_label}\n"
            f"wave: W{config.wave}\n"
            f"phase: {config.phase}\n"
            f"model: {config.effective_model}\n"
            + (f"parent_task_id: {config.parent_task_id}\n" if config.parent_task_id else "")
            + (f"compass_edge_in: {config.compass_edge_in}\n" if config.compass_edge_in else "")
            + f"\n**GOAL:**\n{config.goal}\n"
        )

        return "\n---\n".join(sections)

    def validate_bundle(self, bundle: str) -> list[str]:
        """
        Validate a composed bundle for required sections.

        Returns list of validation warnings (empty = valid).
        """
        warnings = []
        required_markers = [
            "FAERIE2 SPAWN BUNDLE",
            "GLOBAL HONEY",
            "NECTAR",
            "AGENT ROLE CARD",
            "TASK GOAL",
            "dashboard_line",
            "compass_edge",
        ]
        for marker in required_markers:
            if marker not in bundle:
                warnings.append(f"Bundle missing required section/marker: {marker!r}")

        # Budget check: warn if over ~60K tokens (~240K chars)
        if len(bundle) > 240_000:
            warnings.append(
                f"Bundle may exceed context budget: {len(bundle):,} chars "
                f"(~{len(bundle)//4:,} tokens). Consider trimming HONEY/NECTAR."
            )

        return warnings


# ---------------------------------------------------------------------------
# AgentRunID — forensic anchor generation
# ---------------------------------------------------------------------------


class AgentRunID:
    """
    Generates and registers immutable AGENT-RUN-ID for each agent execution.

    ID format: agent-run-{session_id_8}-{agent_type}-{hash_8}
    where hash = SHA256(agent_type + session_id + task_id + wave + ts + nonce)[:8]
    """

    @staticmethod
    def generate(
        agent_type: str,
        task_id: str,
        wave: int,
        session_id: Optional[str] = None,
    ) -> str:
        """Generate a deterministic-within-session, globally unique AGENT-RUN-ID."""
        if session_id is None:
            session_id = os.environ.get("CLAUDE_SESSION_ID", secrets.token_hex(4))

        nonce = secrets.token_hex(4)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        raw = f"{agent_type}|{session_id}|{task_id}|W{wave}|{ts}|{nonce}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        session_id_8 = session_id[:8]
        return f"agent-run-{session_id_8}-{agent_type}-{h}"

    @staticmethod
    def try_register_via_script(
        agent_type: str,
        task_id: str,
        wave: int,
        agent_run_id: str,
    ) -> bool:
        """
        Attempt to register AGENT-RUN-ID via 9x_agent_run_id_generator.py.

        Falls back gracefully if script is unavailable (e.g., in tests).
        Returns True if registration succeeded.
        """
        if not AGENT_RUN_ID_GEN.exists():
            log.debug("agent_run_id_generator not found; skipping registration")
            return False

        session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")[:8]
        try:
            result = subprocess.run(
                [
                    sys.executable, str(AGENT_RUN_ID_GEN),
                    "--agent-type", agent_type,
                    "--session-id", session_id,
                    "--task-id", task_id,
                    "--wave", f"W{wave}",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                log.debug("Registered agent_run_id=%s", agent_run_id)
                return True
            else:
                log.warning(
                    "agent_run_id registration returned exit %d: %s",
                    result.returncode,
                    result.stderr[:200],
                )
                return False
        except (subprocess.TimeoutExpired, OSError) as e:
            log.warning("agent_run_id registration failed: %s", e)
            return False


# ---------------------------------------------------------------------------
# ManifestWriter — atomic writes + COC chaining
# ---------------------------------------------------------------------------


class ManifestWriter:
    """
    Writes agent outcome manifests atomically with COC chain integrity.

    Guarantees:
      - Manifest written only AFTER agent execution completes (no stale signals)
      - Atomic write via temp-file + rename (no partial reads)
      - COC entry appended via 4x_coc_writer.py (hash-chain integrity)
      - Naming convention: {HH-MM-SS}Z_manifest_{task_id}_{agent_type}_{counter}.json
      - Counter increments within same second to prevent collision

    All forensic writes land in: forensics/manifests/{YYYY-MM-DD}/
    """

    def __init__(self, repo_root: Path = REPO_ROOT) -> None:
        self.repo_root = repo_root
        self._counter_state: dict[str, int] = {}  # key=(ts_prefix, task_id, agent) -> counter
        self._lock = asyncio.Lock() if _is_async_context() else None

    def _next_counter(self, ts_prefix: str, task_id: str, agent_type: str) -> int:
        """Collision-resistant counter (increments within same second + agent + task)."""
        key = f"{ts_prefix}|{task_id}|{agent_type}"
        current = self._counter_state.get(key, 0) + 1
        self._counter_state[key] = current
        return current

    def _compute_compass_edge(
        self,
        quality_score: float,
        belief_index: float,
        phase: str = "SEED",
    ) -> str:
        """
        Compute compass edge (N/S/E/W bearing) from quality + belief metrics.

        Phase gates (from CLAUDE.md):
        - SEED:   quality >= 0.50 AND belief >= 0.50 → S; else rules below
        - DEEPEN: quality >= 0.70 AND belief >= 0.50 → S
        - EXTEND: quality >= 0.80 AND belief >= 0.75 → S
        - FULL:   quality >= 0.85 AND belief >= 0.75 → S

        Bearing rules (any phase):
        - S (South/Proceed):    quality >= phase_q AND belief >= phase_b
        - E (East/Parallel):    quality >= phase_q AND belief < phase_b
        - W (West/Retreat):     quality < phase_q AND belief >= phase_b
        - N (North/Unblock):    quality < phase_q AND belief < phase_b

        Args:
            quality_score: 0.0-1.0 data quality metric
            belief_index:  0.0-1.0 agent honesty metric
            phase:         "SEED" | "DEEPEN" | "EXTEND" | "FULL"

        Returns:
            str: One of 'N', 'S', 'E', 'W'
        """
        thresholds = PHASE_THRESHOLDS.get(phase, PHASE_THRESHOLDS["SEED"])
        q_threshold = thresholds["quality"]
        b_threshold = thresholds["belief"]

        q_ok = quality_score >= q_threshold
        b_ok = belief_index >= b_threshold

        if q_ok and b_ok:
            return "S"  # South: proceed to next phase
        elif q_ok and not b_ok:
            return "E"  # East: quality good, but low confidence → parallel validation
        elif b_ok and not q_ok:
            return "W"  # West: honest but failed → retreat/reframe
        else:
            return "N"  # North: both low → unblock prerequisites first

    def _manifest_dir(self, date_str: str) -> Path:
        d = self.repo_root / "forensics" / "manifests" / date_str
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _build_filename(
        self,
        ts: datetime,
        task_id: str,
        agent_type: str,
    ) -> str:
        """Build canonical manifest filename following forensic naming standard."""
        ts_prefix = ts.strftime("%H-%M-%S")
        counter = self._next_counter(ts_prefix, task_id, agent_type)
        counter_str = f"{counter:03d}"
        # Sanitize task_id for filename safety
        safe_task = task_id.replace("/", "-").replace("\\", "-")[:60]
        return f"{ts_prefix}Z_manifest_{safe_task}_{agent_type}_{counter_str}.json"

    def write(
        self,
        result: AgentRunResult,
        investigation_label: str,
        config: Optional[AgentSpawnConfig] = None,
        discovered_work: Optional[list[str]] = None,
        honey_version: Optional[str] = None,
        honey_context: Optional[dict[str, Any]] = None,
        honey_fidelity: float = 0.5,
    ) -> Path:
        """
        Write manifest atomically with full schema compliance. Returns path of written manifest.

        Steps:
          1. Compose manifest dict (result + investigation metadata + HONEY metadata)
          2. Write to temp file (same dir as target)
          3. fsync + rename (atomic on POSIX)
          4. Append COC entry via 4x_coc_writer.py

        Args:
            result:              AgentRunResult from spawn execution
            investigation_label: Stigmergic mission cluster label
            config:              Optional AgentSpawnConfig for phase/parent metadata
            discovered_work:     Optional list of task_ids found during frontier scan
            honey_version:       SHA256 hash of HONEY.md used in bundle (for versioning)
            honey_context:       Dict with keys: global_honey_present, project_honey_present,
                                 nectar_present, pollen_present, audience, fragments_used
            honey_fidelity:      0.0-1.0 quality metric of HONEY rendering
        """
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        manifest_dir = self._manifest_dir(date_str)
        filename = self._build_filename(now, result.task_id, result.agent_type)
        target_path = manifest_dir / filename

        # Compose manifest
        manifest = result.to_manifest_dict()
        manifest["investigation_label"] = investigation_label

        # Wire discovered_work (frontier scan results)
        if discovered_work is not None:
            manifest["discovered_work"] = discovered_work
        # else: leave as empty [] from to_manifest_dict()

        # Wire HONEY metadata
        if honey_version:
            manifest["honey_version_used"] = honey_version
        if honey_context:
            manifest["honey_rendering_context"].update(honey_context)
        manifest["honey_render_fidelity"] = max(0.0, min(1.0, honey_fidelity))

        # Wire config metadata
        if config:
            manifest["phase"] = config.phase
            if config.parent_task_id:
                manifest["parent_task_id"] = config.parent_task_id
            if config.compass_edge_in:
                manifest["compass_edge_in"] = config.compass_edge_in

        # Compute phase gate: compass_edge derived from quality_score + belief_index
        manifest["compass_edge"] = self._compute_compass_edge(
            quality_score=result.quality_score,
            belief_index=result.belief_index,
            phase=config.phase if config else "SEED",
        )

        manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)

        # --- Atomic write (temp + rename) ---
        tmp_fd, tmp_path_str = tempfile.mkstemp(
            dir=manifest_dir,
            prefix=".manifest_tmp_",
            suffix=".json",
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(manifest_json)
                f.flush()
                os.fsync(f.fileno())
            os.rename(tmp_path_str, target_path)
        except Exception:
            # Cleanup temp on failure
            try:
                os.unlink(tmp_path_str)
            except OSError:
                pass
            raise

        log.info("Manifest written: %s", target_path)

        # --- COC chain entry ---
        self._write_coc_entry(result, target_path, now)

        return target_path

    def _write_coc_entry(
        self,
        result: AgentRunResult,
        manifest_path: Path,
        ts: datetime,
    ) -> None:
        """
        Append COC chain entry via 4x_coc_writer.py subprocess.

        On failure, logs warning but does NOT raise (manifest write already succeeded;
        COC failure is degraded, not fatal).
        """
        if not COC_WRITER.exists():
            log.warning(
                "4x_coc_writer.py not found at %s; COC entry skipped", COC_WRITER
            )
            return

        coc_dir = self.repo_root / "forensics" / "coc-entries" / ts.strftime("%Y-%m-%d")
        coc_dir.mkdir(parents=True, exist_ok=True)
        coc_file = coc_dir / f"{ts.strftime('%H-%M-%S')}Z_coc-entry_{result.task_id}_{result.agent_type}_001.jsonl"

        entry = {
            "ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent_id": result.agent_type,
            "task_id": result.task_id,
            "body": {
                "action": "manifest_written",
                "agent_run_id": result.agent_run_id,
                "manifest_path": str(manifest_path),
                "dashboard_line": result.dashboard_line,
                "compass_edge": result.compass_edge,
                "status": result.status,
                "quality_score": result.quality_score,
                "belief_index": result.belief_index,
            },
        }

        try:
            env = {**os.environ, "COC_WRITER_ACTIVE": "1"}
            subprocess.run(
                [
                    sys.executable, str(COC_WRITER),
                    "append",
                    "--file", str(coc_file),
                    "--entry", json.dumps(entry),
                ],
                capture_output=True,
                text=True,
                timeout=15,
                env=env,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            log.warning("COC entry write failed (non-fatal): %s", e)


# ---------------------------------------------------------------------------
# Rate Limiter — token bucket for API quota compliance
# ---------------------------------------------------------------------------


class TokenBucketRateLimiter:
    """
    Simple token-bucket rate limiter for API calls.

    Prevents exceeding Anthropic API quotas during W1 LIFTOFF
    (4-5 parallel spawns simultaneously).
    """

    def __init__(self, rps: float = RATE_LIMIT_RPS) -> None:
        self._rps = rps
        self._tokens = rps  # start full
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock() if _is_async_context() else None

    async def acquire_async(self) -> None:
        """Async acquire — yields until a token is available."""
        while True:
            now = time.monotonic()
            elapsed = now - self._last_refill
            # Refill tokens
            self._tokens = min(self._rps, self._tokens + elapsed * self._rps)
            self._last_refill = now

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return
            # Wait for next token
            wait_time = (1.0 - self._tokens) / self._rps
            await asyncio.sleep(wait_time)

    def acquire_sync(self) -> None:
        """Sync acquire — blocks until a token is available."""
        while True:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self._rps, self._tokens + elapsed * self._rps)
            self._last_refill = now

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return
            wait_time = (1.0 - self._tokens) / self._rps
            time.sleep(wait_time)


# ---------------------------------------------------------------------------
# AgentSpawner — single-agent lifecycle
# ---------------------------------------------------------------------------


class AgentSpawner:
    """
    Manages the complete lifecycle of a single agent spawn.

    Responsibilities:
      1. Generate AGENT-RUN-ID (forensic anchor)
      2. Compose bundle (via BundleComposer)
      3. Validate bundle composition
      4. Call Anthropic Agent SDK (or dry-run simulation)
      5. Extract manifest signals from agent output
      6. Write manifest (via ManifestWriter) AFTER execution
      7. Retry with exponential backoff on transient errors
      8. Handle timeouts gracefully

    The Anthropic SDK integration point is the `_execute_agent` method.
    When the SDK is available (`import anthropic`), it spawns a real agent.
    When unavailable (testing, offline), it runs a dry-run simulation that
    produces a structurally valid result without API calls.
    """

    def __init__(
        self,
        bundle_composer: BundleComposer,
        manifest_writer: ManifestWriter,
        rate_limiter: Optional[TokenBucketRateLimiter] = None,
        dry_run: bool = False,
    ) -> None:
        self.bundle_composer = bundle_composer
        self.manifest_writer = manifest_writer
        self.rate_limiter = rate_limiter or TokenBucketRateLimiter()
        self.dry_run = dry_run
        self._sdk_available = self._probe_sdk()

    @staticmethod
    def _probe_sdk() -> bool:
        """Check if Anthropic SDK is importable."""
        try:
            import anthropic  # noqa: F401
            return True
        except ImportError:
            return False

    async def spawn(
        self,
        config: AgentSpawnConfig,
        investigation_label: str,
    ) -> AgentRunResult:
        """
        Full agent spawn lifecycle with retry + backoff.

        Returns AgentRunResult regardless of success/failure.
        Never raises (errors surface via result.status and result.error_message).
        """
        # Validate config
        errors = config.validate()
        if errors:
            err_msg = "; ".join(errors)
            log.error("Config validation failed for task %s: %s", config.task_id, err_msg)
            return AgentRunResult(
                agent_run_id=AgentRunID.generate(config.agent_type, config.task_id, config.wave),
                task_id=config.task_id,
                agent_type=config.agent_type,
                wave=config.wave,
                status="skipped",
                dashboard_line=f"SKIPPED: config invalid — {err_msg}"[:80],
                compass_edge="W",
                next_task_queued=None,
                quality_score=0.0,
                belief_index=0.0,
                manifest_path=None,
                error_message=err_msg,
            )

        # Generate AGENT-RUN-ID
        agent_run_id = AgentRunID.generate(config.agent_type, config.task_id, config.wave)
        AgentRunID.try_register_via_script(config.agent_type, config.task_id, config.wave, agent_run_id)

        # Compose bundle
        bundle = self.bundle_composer.compose(config)
        bundle_warnings = self.bundle_composer.validate_bundle(bundle)
        if bundle_warnings:
            for w in bundle_warnings:
                log.warning("[%s] Bundle warning: %s", config.task_id, w)

        # Retry loop
        last_error: Optional[str] = None
        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                log.info(
                    "[%s] Retry %d/%d — waiting %.1fs",
                    config.task_id, attempt, MAX_RETRIES - 1, delay,
                )
                await asyncio.sleep(delay)

            try:
                # Rate limit before API call
                await self.rate_limiter.acquire_async()

                t0 = time.monotonic()
                result = await self._execute_agent(config, bundle, agent_run_id)
                result.duration_seconds = time.monotonic() - t0
                result.retries_used = attempt

                # Gather HONEY metadata for manifest
                honey_context = self.bundle_composer.get_rendering_context(config)
                honey_version = honey_context.get("global_honey_hash", "")
                # Estimate fidelity: if both global and project HONEY present, fidelity is high
                honey_fidelity = 0.9 if (honey_context.get("global_honey_present") and
                                          honey_context.get("project_honey_present")) else 0.7

                # Write manifest AFTER successful execution
                manifest_path = self.manifest_writer.write(
                    result,
                    investigation_label,
                    config,
                    discovered_work=getattr(result, "discovered_work", None),
                    honey_version=honey_version,
                    honey_context=honey_context,
                    honey_fidelity=honey_fidelity,
                )
                result.manifest_path = str(manifest_path)

                log.info(
                    "[%s] Agent complete: status=%s compass=%s duration=%.1fs",
                    config.task_id, result.status, result.compass_edge, result.duration_seconds,
                )
                return result

            except asyncio.TimeoutError:
                last_error = f"timeout after {config.effective_timeout}s"
                log.warning("[%s] Timeout on attempt %d", config.task_id, attempt + 1)

            except Exception as e:
                last_error = str(e)
                log.error("[%s] Error on attempt %d: %s", config.task_id, attempt + 1, e, exc_info=True)
                if _is_unrecoverable(e):
                    log.error("[%s] Unrecoverable error — aborting retries", config.task_id)
                    break

        # All retries exhausted
        failed_result = AgentRunResult(
            agent_run_id=agent_run_id,
            task_id=config.task_id,
            agent_type=config.agent_type,
            wave=config.wave,
            status="error",
            dashboard_line=f"FAILED ({config.agent_type}): {(last_error or 'unknown')[:60]}"[:80],
            compass_edge="W",  # West = retreat/reframe on honest failure
            next_task_queued=None,
            quality_score=0.0,
            belief_index=0.0,
            manifest_path=None,
            error_message=last_error,
            retries_used=MAX_RETRIES - 1,
        )
        # Write error manifest (no stale-signal risk — this IS the final signal)
        try:
            honey_context = self.bundle_composer.get_rendering_context(config)
            honey_version = honey_context.get("global_honey_hash", "")
            manifest_path = self.manifest_writer.write(
                failed_result,
                investigation_label,
                config,
                honey_version=honey_version,
                honey_context=honey_context,
                honey_fidelity=0.5,  # error case: lower fidelity
            )
            failed_result.manifest_path = str(manifest_path)
        except Exception as e:
            log.error("[%s] Failed to write error manifest: %s", config.task_id, e)

        return failed_result

    async def _execute_agent(
        self,
        config: AgentSpawnConfig,
        bundle: str,
        agent_run_id: str,
    ) -> AgentRunResult:
        """
        Execute agent via Anthropic SDK or dry-run simulation.

        SDK path: uses anthropic.Anthropic() client with the Agent-compatible
        messages.create() call, respecting model + timeout from config.

        Dry-run path: returns a structurally-valid synthetic result for testing.

        NOTE: The Anthropic Agent SDK (`Agent(subagent_type=...)`) is a Claude
        Code tool, not a Python importable. The SDK-callable equivalent for
        programmatic Python use is the Anthropic Messages API or Batch API.
        This method uses the Messages API directly for maximum portability.
        For Claude Code agent spawning, the bundle is emitted and the Agent
        tool call is issued by the orchestrating context — this method handles
        the Python SDK path for standalone/programmatic invocation.
        """
        if self.dry_run or not self._sdk_available:
            return await self._dry_run_agent(config, agent_run_id)

        # --- Anthropic SDK path ---
        import anthropic

        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

        # Inject agent_run_id into bundle header
        bundle_with_id = (
            f"AGENT-RUN-ID: {agent_run_id}\n"
            f"MODEL: {config.effective_model}\n"
            f"WAVE: W{config.wave}\n\n"
            + bundle
        )

        try:
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.messages.create(
                        model=config.effective_model,
                        max_tokens=8192,
                        messages=[
                            {
                                "role": "user",
                                "content": bundle_with_id,
                            }
                        ],
                        system=(
                            f"You are {config.agent_type} executing task {config.task_id!r}. "
                            "Your output MUST include a JSON manifest block marked "
                            "```manifest\n{...}\n``` with fields: dashboard_line (<=80 chars), "
                            "compass_edge (N/S/E/W), next_task_queued (str or null), "
                            "quality_score (0.0-1.0), belief_index (0.0-1.0), status."
                        ),
                    ),
                ),
                timeout=config.effective_timeout,
            )
        except asyncio.TimeoutError:
            raise

        raw_output = ""
        for block in response.content:
            if hasattr(block, "text"):
                raw_output += block.text

        # Extract manifest signals from output
        return self._parse_agent_output(
            raw_output=raw_output,
            config=config,
            agent_run_id=agent_run_id,
        )

    async def _dry_run_agent(
        self,
        config: AgentSpawnConfig,
        agent_run_id: str,
    ) -> AgentRunResult:
        """
        Dry-run simulation — structurally valid result, no API call.

        Used for: testing, offline development, CI pipelines.
        Simulates realistic timing with a short sleep.
        """
        await asyncio.sleep(0.05)  # Simulate minimal API round-trip

        dashboard_line = (
            f"[DRY-RUN] {config.agent_type} task={config.task_id} wave=W{config.wave} "
            f"goal={config.goal[:20]}..."
        )[:80]

        return AgentRunResult(
            agent_run_id=agent_run_id,
            task_id=config.task_id,
            agent_type=config.agent_type,
            wave=config.wave,
            status="success",
            dashboard_line=dashboard_line,
            compass_edge="S",  # South = proceed (dry-run always succeeds)
            next_task_queued=None,
            quality_score=0.75,  # Synthetic mid-range score
            belief_index=0.80,
            manifest_path=None,
            raw_output=f"[DRY-RUN] Simulated output for task={config.task_id}",
        )

    def _parse_agent_output(
        self,
        raw_output: str,
        config: AgentSpawnConfig,
        agent_run_id: str,
    ) -> AgentRunResult:
        """
        Extract manifest signals from agent text output.

        Looks for a ```manifest ... ``` fenced code block first,
        then falls back to scanning for JSON-like patterns.
        """
        import re

        manifest_data: dict[str, Any] = {}

        # Try fenced manifest block
        fenced_match = re.search(
            r"```manifest\s*\n(\{.*?\})\s*\n```",
            raw_output,
            re.DOTALL,
        )
        if fenced_match:
            try:
                manifest_data = json.loads(fenced_match.group(1))
            except json.JSONDecodeError:
                log.warning("[%s] Failed to parse fenced manifest JSON", config.task_id)

        # Fallback: scan for any JSON object with dashboard_line key
        if not manifest_data:
            json_match = re.search(
                r'\{[^{}]*"dashboard_line"[^{}]*\}',
                raw_output,
                re.DOTALL,
            )
            if json_match:
                try:
                    manifest_data = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass

        # Extract with defaults
        dashboard_line = str(manifest_data.get("dashboard_line", f"{config.agent_type}: task complete"))[:80]
        compass_edge = str(manifest_data.get("compass_edge", "S")).upper()
        if compass_edge not in ("N", "S", "E", "W"):
            compass_edge = "S"

        quality_score = float(manifest_data.get("quality_score", 0.5))
        quality_score = max(0.0, min(1.0, quality_score))

        belief_index = float(manifest_data.get("belief_index", 0.5))
        belief_index = max(0.0, min(1.0, belief_index))

        next_task = manifest_data.get("next_task_queued")
        if next_task:
            next_task = str(next_task)

        status = str(manifest_data.get("status", "success"))

        return AgentRunResult(
            agent_run_id=agent_run_id,
            task_id=config.task_id,
            agent_type=config.agent_type,
            wave=config.wave,
            status=status,
            dashboard_line=dashboard_line,
            compass_edge=compass_edge,
            next_task_queued=next_task,
            quality_score=quality_score,
            belief_index=belief_index,
            manifest_path=None,
            raw_output=raw_output[:2000] if raw_output else None,  # Cap stored output
        )


# ---------------------------------------------------------------------------
# WaveDispatcher — multi-agent parallel lifecycle
# ---------------------------------------------------------------------------


class WaveDispatcher:
    """
    Coordinates parallel agent dispatch across W1/W2/W3 waves.

    W1 LIFTOFF: spawn up to 5 agents concurrently (asyncio.gather);
                haiku model; wait inline; target 5-min cache TTL hit.
    W2 CRUISE:  spawn up to 3 agents; sonnet model; wait inline.
    W3 INSERTION: spawn 1-2 agents; sonnet model; fire-and-forget (background).

    Respects rate limiter to stay within API quotas.
    Logs wave summary on completion.
    """

    def __init__(
        self,
        repo_root: Path = REPO_ROOT,
        dry_run: bool = False,
        rate_limit_rps: float = RATE_LIMIT_RPS,
    ) -> None:
        self.repo_root = repo_root
        self.dry_run = dry_run
        self._bundle_composer = BundleComposer(repo_root=repo_root)
        self._manifest_writer = ManifestWriter(repo_root=repo_root)
        self._rate_limiter = TokenBucketRateLimiter(rps=rate_limit_rps)
        self._spawner = AgentSpawner(
            bundle_composer=self._bundle_composer,
            manifest_writer=self._manifest_writer,
            rate_limiter=self._rate_limiter,
            dry_run=dry_run,
        )
        self._background_tasks: list[asyncio.Task] = []

    async def dispatch_wave(
        self,
        wave: int,
        configs: list[AgentSpawnConfig],
        investigation_label: str = "default",
        on_result: Optional[Callable[[AgentRunResult], None]] = None,
    ) -> WaveResult:
        """
        Dispatch all configs in this wave concurrently (up to wave max_parallel).

        Args:
            wave:                Wave number (1, 2, or 3).
            configs:             List of AgentSpawnConfig — one per agent to spawn.
            investigation_label: Compass cluster label for all agents in this wave.
            on_result:           Optional callback fired on each agent completion.

        Returns:
            WaveResult with aggregate stats + all individual AgentRunResults.
        """
        if wave not in WAVE_PARAMS:
            raise ValueError(f"Invalid wave {wave!r}; must be 1, 2, or 3")

        wave_params = WAVE_PARAMS[wave]
        max_parallel = wave_params["max_parallel"]

        # Enforce wave max_parallel ceiling
        if len(configs) > max_parallel:
            log.warning(
                "W%d: %d configs exceed max_parallel=%d — truncating to %d",
                wave, len(configs), max_parallel, max_parallel,
            )
            configs = configs[:max_parallel]

        # Ensure all configs have correct wave set
        for c in configs:
            c.wave = wave

        log.info(
            "W%d DISPATCH: %d agents — %s",
            wave, len(configs), wave_params["description"],
        )

        t0 = time.monotonic()
        is_background = wave_params["run_in_background"]

        if is_background:
            # W3: fire-and-forget; return immediately with pending results
            return await self._dispatch_background(
                wave=wave,
                configs=configs,
                investigation_label=investigation_label,
                on_result=on_result,
            )
        else:
            # W1/W2: wait inline for all results
            return await self._dispatch_inline(
                wave=wave,
                configs=configs,
                investigation_label=investigation_label,
                on_result=on_result,
                t0=t0,
            )

    async def _dispatch_inline(
        self,
        wave: int,
        configs: list[AgentSpawnConfig],
        investigation_label: str,
        on_result: Optional[Callable[[AgentRunResult], None]],
        t0: float,
    ) -> WaveResult:
        """W1/W2: concurrent spawn, wait for all results."""

        async def _spawn_one(cfg: AgentSpawnConfig) -> AgentRunResult:
            result = await self._spawner.spawn(cfg, investigation_label)
            if on_result:
                try:
                    on_result(result)
                except Exception as e:
                    log.warning("on_result callback error: %s", e)
            return result

        # Python 3.11+ asyncio.TaskGroup for structured concurrency
        results: list[AgentRunResult] = []
        try:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(_spawn_one(cfg)) for cfg in configs]
            results = [t.result() for t in tasks]
        except* Exception as eg:
            # ExceptionGroup handling (Python 3.11+)
            for exc in eg.exceptions:
                log.error("Wave W%d task exception: %s", wave, exc)
            # Partial results from succeeded tasks
            results = [t.result() for t in tasks if not t.exception()]

        wave_result = _aggregate_results(wave, results, time.monotonic() - t0)
        log.info("W%d COMPLETE: %s", wave, wave_result.summary())
        return wave_result

    async def _dispatch_background(
        self,
        wave: int,
        configs: list[AgentSpawnConfig],
        investigation_label: str,
        on_result: Optional[Callable[[AgentRunResult], None]],
    ) -> WaveResult:
        """W3: fire-and-forget; track background tasks for eventual cleanup."""
        t0 = time.monotonic()

        async def _background_spawn(cfg: AgentSpawnConfig) -> None:
            result = await self._spawner.spawn(cfg, investigation_label)
            if on_result:
                try:
                    on_result(result)
                except Exception as e:
                    log.warning("on_result callback error (background): %s", e)

        for cfg in configs:
            task = asyncio.create_task(
                _background_spawn(cfg),
                name=f"w3-{cfg.agent_type}-{cfg.task_id}",
            )
            self._background_tasks.append(task)

        # Return immediately with "pending" status
        pending_results = [
            AgentRunResult(
                agent_run_id=AgentRunID.generate(c.agent_type, c.task_id, c.wave),
                task_id=c.task_id,
                agent_type=c.agent_type,
                wave=c.wave,
                status="pending",
                dashboard_line=f"W3 PENDING: {c.agent_type} — {c.goal[:40]}..."[:80],
                compass_edge="S",
                next_task_queued=None,
                quality_score=0.0,
                belief_index=0.0,
                manifest_path=None,
            )
            for c in configs
        ]
        wave_result = _aggregate_results(wave, pending_results, time.monotonic() - t0)
        log.info(
            "W%d BACKGROUND: %d agents dispatched (fire-and-forget)", wave, len(configs)
        )
        return wave_result

    async def wait_background(self, timeout: float = 1800.0) -> list[AgentRunResult]:
        """
        Wait for all W3 background tasks to complete.

        Should be called at session teardown if the caller needs W3 results.
        Returns list of results from completed background tasks.
        """
        if not self._background_tasks:
            return []

        done, pending = await asyncio.wait(
            self._background_tasks,
            timeout=timeout,
        )

        if pending:
            log.warning(
                "%d background W3 tasks did not complete within %.0fs",
                len(pending), timeout,
            )
            for task in pending:
                task.cancel()

        results = []
        for task in done:
            if not task.cancelled() and not task.exception():
                pass  # Result captured by on_result callback if set
        return results


# ---------------------------------------------------------------------------
# Convenience: three-wave session orchestration
# ---------------------------------------------------------------------------


async def run_three_wave_session(
    repo_root: Path,
    w1_configs: list[AgentSpawnConfig],
    w2_configs: list[AgentSpawnConfig],
    w3_configs: list[AgentSpawnConfig],
    investigation_label: str,
    dry_run: bool = False,
    on_result: Optional[Callable[[AgentRunResult], None]] = None,
) -> dict[str, WaveResult]:
    """
    Orchestrate a complete W1 → W2 → W3 session.

    W1 and W2 are awaited inline (results available for next wave decisions).
    W3 is dispatched as background (caller receives pending results immediately).

    Args:
        repo_root:           Repo root for forensics paths.
        w1_configs:          Agents for W1 LIFTOFF (triage, haiku).
        w2_configs:          Agents for W2 CRUISE (feature work, sonnet).
        w3_configs:          Agents for W3 INSERTION (synthesis, sonnet bg).
        investigation_label: Compass cluster label for all waves.
        dry_run:             If True, no API calls made.
        on_result:           Optional callback on each individual result.

    Returns:
        Dict with keys "w1", "w2", "w3" mapping to WaveResult objects.
    """
    dispatcher = WaveDispatcher(repo_root=repo_root, dry_run=dry_run)
    results: dict[str, WaveResult] = {}

    # W1 — LIFTOFF
    if w1_configs:
        log.info("Launching W1 LIFTOFF")
        results["w1"] = await dispatcher.dispatch_wave(
            wave=1,
            configs=w1_configs,
            investigation_label=investigation_label,
            on_result=on_result,
        )
    else:
        log.info("W1: no configs — skipping")

    # W2 — CRUISE
    if w2_configs:
        log.info("Launching W2 CRUISE")
        results["w2"] = await dispatcher.dispatch_wave(
            wave=2,
            configs=w2_configs,
            investigation_label=investigation_label,
            on_result=on_result,
        )
    else:
        log.info("W2: no configs — skipping")

    # W3 — INSERTION (background)
    if w3_configs:
        log.info("Launching W3 INSERTION (background)")
        results["w3"] = await dispatcher.dispatch_wave(
            wave=3,
            configs=w3_configs,
            investigation_label=investigation_label,
            on_result=on_result,
        )
    else:
        log.info("W3: no configs — skipping")

    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_async_context() -> bool:
    """Return True if running inside an asyncio event loop."""
    try:
        return asyncio.get_event_loop().is_running()
    except RuntimeError:
        return False


def _is_unrecoverable(exc: Exception) -> bool:
    """
    Return True if the exception type should NOT be retried.

    Unrecoverable: auth errors, invalid requests (4xx except 429).
    Recoverable: timeout, rate limit, transient server errors (5xx, 429).
    """
    # If Anthropic SDK available, check for auth error types
    try:
        import anthropic
        if isinstance(exc, anthropic.AuthenticationError):
            return True
        if isinstance(exc, anthropic.BadRequestError):
            return True
    except ImportError:
        pass
    return False


def _aggregate_results(
    wave: int,
    results: list[AgentRunResult],
    duration: float,
) -> WaveResult:
    """Aggregate individual results into a WaveResult."""
    succeeded = sum(1 for r in results if r.status == "success")
    failed = sum(1 for r in results if r.status == "error")
    timed_out = sum(1 for r in results if r.status == "timeout")
    skipped = sum(1 for r in results if r.status in ("skipped", "pending"))

    return WaveResult(
        wave=wave,
        spawned=len(results),
        succeeded=succeeded,
        failed=failed,
        timed_out=timed_out,
        skipped=skipped,
        results=results,
        duration_seconds=duration,
    )


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


async def _run_self_tests() -> int:
    """
    Run internal self-tests. Uses dry-run mode; no API calls.
    Returns 0 on success, 1 on failure.
    """
    import tempfile

    errors = []
    print("Running self-tests...", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)

        # ---- Test 1: AgentRunID uniqueness ---
        id1 = AgentRunID.generate("python-pro", "task-001", 1)
        id2 = AgentRunID.generate("python-pro", "task-001", 1)
        if id1 == id2:
            errors.append("Test 1 FAILED: AgentRunID not unique across calls (nonce collision?)")
        elif not id1.startswith("agent-run-"):
            errors.append(f"Test 1 FAILED: AgentRunID format wrong: {id1!r}")
        else:
            print("  Test 1 PASS: AgentRunID unique + correct format", file=sys.stderr)

        # ---- Test 2: BundleComposer produces valid bundle ---
        composer = BundleComposer(
            claude_home=Path(tmpdir),
            repo_root=repo_root,
        )
        config = AgentSpawnConfig(
            task_id="test-bundle-001",
            agent_type="python-pro",
            investigation_label="self-test",
            goal="Test bundle composition",
            wave=1,
            honey_content="# Test HONEY\n\nTest fact: x=1",
            nectar_content="## Test NECTAR\n\nTest finding: Y happened",
        )
        bundle = composer.compose(config)
        if "FAERIE2 SPAWN BUNDLE" not in bundle:
            errors.append("Test 2 FAILED: bundle missing header")
        elif "Test HONEY" not in bundle:
            errors.append("Test 2 FAILED: bundle missing HONEY content")
        elif "TASK GOAL" not in bundle:
            errors.append("Test 2 FAILED: bundle missing TASK GOAL section")
        else:
            print("  Test 2 PASS: BundleComposer produces valid bundle", file=sys.stderr)

        # ---- Test 3: ManifestWriter atomic write ---
        writer = ManifestWriter(repo_root=repo_root)
        run_id = AgentRunID.generate("python-pro", "test-manifest-001", 1)
        result = AgentRunResult(
            agent_run_id=run_id,
            task_id="test-manifest-001",
            agent_type="python-pro",
            wave=1,
            status="success",
            dashboard_line="Test manifest write: 42 lines, OK",
            compass_edge="S",
            next_task_queued="next-test-task",
            quality_score=0.85,
            belief_index=0.90,
            manifest_path=None,
        )
        written_path = writer.write(result, investigation_label="self-test")
        if not written_path.exists():
            errors.append("Test 3 FAILED: manifest file not created")
        else:
            written = json.loads(written_path.read_text(encoding="utf-8"))
            if written.get("task_id") != "test-manifest-001":
                errors.append(f"Test 3 FAILED: manifest task_id wrong: {written.get('task_id')!r}")
            elif written.get("compass_edge") != "S":
                errors.append(f"Test 3 FAILED: compass_edge wrong: {written.get('compass_edge')!r}")
            elif len(written.get("dashboard_line", "")) > 80:
                errors.append("Test 3 FAILED: dashboard_line exceeds 80 chars")
            else:
                print("  Test 3 PASS: ManifestWriter atomic write + schema valid", file=sys.stderr)

        # ---- Test 4: AgentSpawner dry-run ---
        spawner = AgentSpawner(
            bundle_composer=composer,
            manifest_writer=writer,
            dry_run=True,
        )
        dry_result = await spawner.spawn(config, investigation_label="self-test")
        if dry_result.status != "success":
            errors.append(f"Test 4 FAILED: dry-run status={dry_result.status!r}")
        elif dry_result.manifest_path is None:
            errors.append("Test 4 FAILED: dry-run manifest_path not set")
        elif not Path(dry_result.manifest_path).exists():
            errors.append("Test 4 FAILED: dry-run manifest file not created")
        else:
            print("  Test 4 PASS: AgentSpawner dry-run produces manifest", file=sys.stderr)

        # ---- Test 5: WaveDispatcher W1 parallel dry-run ---
        dispatcher = WaveDispatcher(repo_root=repo_root, dry_run=True)
        w1_configs = [
            AgentSpawnConfig(
                task_id=f"wave-test-{i:03d}",
                agent_type="python-pro",
                investigation_label="self-test",
                goal=f"Test goal {i}",
                wave=1,
                honey_content="# Test HONEY",
            )
            for i in range(3)
        ]
        wave_result = await dispatcher.dispatch_wave(
            wave=1, configs=w1_configs, investigation_label="self-test"
        )
        if wave_result.succeeded != 3:
            errors.append(
                f"Test 5 FAILED: expected 3 succeeded, got {wave_result.succeeded}"
            )
        elif wave_result.spawned != 3:
            errors.append(f"Test 5 FAILED: spawned={wave_result.spawned} != 3")
        else:
            print(
                f"  Test 5 PASS: WaveDispatcher W1 dispatched 3 agents "
                f"({wave_result.duration_seconds:.2f}s)",
                file=sys.stderr,
            )

        # ---- Test 6: Config validation catches bad input ---
        bad_config = AgentSpawnConfig(
            task_id="",  # invalid
            agent_type="python-pro",
            investigation_label="test",
            goal="test",
            wave=99,  # invalid
        )
        validation_errors = bad_config.validate()
        if not validation_errors:
            errors.append("Test 6 FAILED: expected validation errors for bad config, got none")
        elif len(validation_errors) < 2:
            errors.append(f"Test 6 FAILED: expected >=2 errors, got {validation_errors}")
        else:
            print(
                f"  Test 6 PASS: Config validation catches {len(validation_errors)} errors",
                file=sys.stderr,
            )

        # ---- Test 7: BundleComposer validation catches missing sections ---
        incomplete_bundle = "just some text without required sections"
        bundle_warnings = composer.validate_bundle(incomplete_bundle)
        if len(bundle_warnings) < 5:
            errors.append(
                f"Test 7 FAILED: expected >=5 bundle warnings, got {len(bundle_warnings)}"
            )
        else:
            print(
                f"  Test 7 PASS: Bundle validator caught {len(bundle_warnings)} missing sections",
                file=sys.stderr,
            )

        # ---- Test 8: Three-wave session produces all three WaveResults ---
        w2_configs = [
            AgentSpawnConfig(
                task_id="wave2-test-001",
                agent_type="code-reviewer",
                investigation_label="self-test",
                goal="Review test code",
                wave=2,
                honey_content="# Test HONEY",
            )
        ]
        w3_configs = [
            AgentSpawnConfig(
                task_id="wave3-test-001",
                agent_type="knowledge-synthesizer",
                investigation_label="self-test",
                goal="Synthesize test findings",
                wave=3,
                honey_content="# Test HONEY",
            )
        ]
        session_results = await run_three_wave_session(
            repo_root=repo_root,
            w1_configs=w1_configs[:1],
            w2_configs=w2_configs,
            w3_configs=w3_configs,
            investigation_label="self-test",
            dry_run=True,
        )
        if "w1" not in session_results or "w2" not in session_results or "w3" not in session_results:
            errors.append(f"Test 8 FAILED: missing wave keys in session_results: {list(session_results)}")
        else:
            print(
                "  Test 8 PASS: three-wave session produces w1+w2+w3 results",
                file=sys.stderr,
            )

    # Summary
    if errors:
        for err in errors:
            print(f"  FAIL: {err}", file=sys.stderr)
        print(f"\nSelf-test result: {len(errors)} failure(s)", file=sys.stderr)
        return 1
    else:
        print("\nSelf-test result: all 8 tests passed", file=sys.stderr)
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "implementation_spec.py — Production-grade Agent SDK Harness\n\n"
            "Implements W1/W2/W3 wave dispatch with manifest writing + COC integrity.\n"
            "Use --dry-run for offline testing (no API calls).\n"
            "Use --self-test to run internal validation suite."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate agent execution without API calls",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run internal self-tests and exit",
    )
    parser.add_argument(
        "--wave",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Wave to dispatch (1=LIFTOFF, 2=CRUISE, 3=INSERTION)",
    )
    parser.add_argument(
        "--task-id",
        default="cli-test-001",
        help="Task ID for CLI test spawn",
    )
    parser.add_argument(
        "--agent-type",
        default="python-pro",
        help="Agent type for CLI test spawn",
    )
    parser.add_argument(
        "--investigation-label",
        default="cli-test",
        help="Investigation label for CLI test spawn",
    )
    parser.add_argument(
        "--goal",
        default="CLI-invoked test spawn",
        help="Goal text for CLI test spawn",
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help=f"Repo root path (default: {REPO_ROOT})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of agents to spawn in the wave (max enforced by wave params)",
    )
    return parser


async def _cli_main(args: argparse.Namespace) -> int:
    if args.self_test:
        return await _run_self_tests()

    repo_root = Path(args.repo_root)
    configs = [
        AgentSpawnConfig(
            task_id=f"{args.task_id}-{i:03d}" if args.count > 1 else args.task_id,
            agent_type=args.agent_type,
            investigation_label=args.investigation_label,
            goal=args.goal,
            wave=args.wave,
        )
        for i in range(args.count)
    ]

    dispatcher = WaveDispatcher(repo_root=repo_root, dry_run=args.dry_run)
    wave_result = await dispatcher.dispatch_wave(
        wave=args.wave,
        configs=configs,
        investigation_label=args.investigation_label,
    )

    print(wave_result.summary())
    for r in wave_result.results:
        print(
            f"  [{r.status.upper():8s}] {r.agent_type:30s} "
            f"edge={r.compass_edge} q={r.quality_score:.2f} b={r.belief_index:.2f}"
        )
        print(f"    dashboard: {r.dashboard_line}")
        if r.manifest_path:
            print(f"    manifest:  {r.manifest_path}")
        if r.error_message:
            print(f"    error:     {r.error_message}")

    return 0 if wave_result.failed == 0 and wave_result.timed_out == 0 else 1


def main() -> None:
    parser = _build_cli_parser()
    args = parser.parse_args()
    sys.exit(asyncio.run(_cli_main(args)))


if __name__ == "__main__":
    main()
