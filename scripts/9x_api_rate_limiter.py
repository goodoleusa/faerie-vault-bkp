#!/usr/bin/env python3
"""
9x_api_rate_limiter.py — Token-Aware Rate Limiter

TIER: 9x_
PURPOSE: Prevents API rate limit hammering with sensible defaults
LOAD: light

Usage:
  from 9x_api_rate_limiter import RateLimiter, TokenBucket
  
  # Simple rate limiting
  limiter = RateLimiter(max_calls=10, period=60)  # 10 calls per minute
  if limiter.allow():
      do_api_call()
  else:
      wait_and_retry()
"""

import os
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from functools import wraps

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Default limits - adjust based on your API tier
DEFAULT_LIMITS = {
    "openai": {"calls": 50, "period": 60},      # 50/min for GPT-4
    "anthropic": {"calls": 50, "period": 60},     # 50/min for Claude
    "github": {"calls": 60, "period": 60},     # 60/min
    "tavily": {"calls": 15, "period": 60},      # 15/min free tier
    "default": {"calls": 10, "period": 60},     # 10/min fallback
}

# Per-provider tokens (from env)
API_TOKENS = {
    "openai": os.environ.get("OPENAI_API_KEY"),
    "anthropic": os.environ.get("ANTHROPIC_API_KEY"),
    "github": os.environ.get("GITHUB_TOKEN"),
    "tavily": os.environ.get("TAVILY_TOKEN"),
}

# ---------------------------------------------------------------------------
# Token Bucket Algorithm
# ---------------------------------------------------------------------------

@dataclass
class TokenBucket:
    """Token bucket rate limiter - allows burst, enforces average."""
    
    capacity: int = 10           # Max tokens (burst)
    refill_rate: float = 1.0     # Tokens per second
    tokens: float = field(default=None)
    last_refill: float = field(default=None)
    lock: threading.Lock = field(default=None)
    
    def __post_init__(self):
        self.tokens = float(self.capacity)
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """Add tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
    
    def allow(self, cost: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        with self.lock:
            self._refill()
            if self.tokens >= cost:
                self.tokens -= cost
                return True
            return False
    
    def wait_time(self, cost: int = 1) -> float:
        """Seconds to wait until request would succeed."""
        with self.lock:
            self._refill()
            if self.tokens >= cost:
                return 0.0
            return (cost - self.tokens) / self.refill_rate


# ---------------------------------------------------------------------------
# Simple Rate Limiter Class
# ---------------------------------------------------------------------------

class RateLimiter:
    """Simple rolling-window rate limiter."""
    
    def __init__(self, max_calls: int = 10, period: float = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls: list[float] = []
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        """Check if call is allowed under limit."""
        now = time.time()
        
        with self.lock:
            # Remove old calls outside window
            self.calls = [t for t in self.calls if now - t < self.period]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            
            return False
    
    def wait_time(self) -> float:
        """Seconds to wait until next call allowed."""
        now = time.time()
        
        with self.lock:
            if len(self.calls) < self.max_calls:
                return 0.0
            
            # Time until oldest call exits window
            oldest = min(self.calls)
            return max(0.0, self.period - (now - oldest))
    
    def wait_until_allowed(self, max_wait: float = 60.0) -> bool:
        """Block until allowed or timeout."""
        start = time.time()
        
        while time.time() - start < max_wait:
            if self.allow():
                return True
            
            wait = self.wait_time()
            if wait > 0:
                time.sleep(min(wait, max_wait - (time.time() - start)))
        
        return False


# ---------------------------------------------------------------------------
# Provider-Specific Limiter Registry
# ---------------------------------------------------------------------------

class LimiterRegistry:
    """Manages rate limiters for multiple providers."""
    
    _instance: Optional['LimiterRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._limiters = {}
        return cls._instance
    
    def get_or_create(self, provider: str) -> RateLimiter:
        """Get or create limiter for provider."""
        if provider not in self._limiters:
            config = DEFAULT_LIMITS.get(provider, DEFAULT_LIMITS["default"])
            self._limiters[provider] = RateLimiter(
                max_calls=config["calls"],
                period=config["period"]
            )
        return self._limiters[provider]
    
    def allow(self, provider: str) -> bool:
        """Check if call allowed for provider."""
        return self.get_or_create(provider).allow()
    
    def wait_time(self, provider: str) -> float:
        """Get wait time for provider."""
        return self.get_or_create(provider).wait_time()


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------

def rate_limited(provider: str = "default", max_calls: int = None, period: float = None):
    """Decorator to rate-limit a function.
    
    Usage:
        @rate_limited("github")
        def github_api_call():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter = LimiterRegistry().get_or_create(provider)
            
            if max_calls and period:
                limiter = RateLimiter(max_calls=max_calls, period=period)
            
            if limiter.allow():
                return func(*args, **kwargs)
            
            wait = limiter.wait_time()
            print(f"[rate-limit] Waiting {wait:.1f}s for {provider}...")
            time.sleep(wait)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# CLI for Testing
# ---------------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="API Rate Limiter")
    parser.add_argument("--provider", default="default", help="Provider name")
    parser.add_argument("--calls", type=int, default=10, help="Max calls per period")
    parser.add_argument("--period", type=float, default=60, help="Period in seconds")
    parser.add_argument("--test", action="store_true", help="Run test")
    parser.add_argument("--watch", action="store_true", help="Watch mode")
    
    args = parser.parse_args()
    
    if args.test:
        # Test mode - show limits
        print("Provider Rate Limits:")
        for prov, cfg in DEFAULT_LIMITS.items():
            print(f"  {prov}: {cfg['calls']}/ {cfg['period']}s")
        return
    
    limiter = RateLimiter(max_calls=args.calls, period=args.period)
    
    if args.watch:
        # Continuous test
        print(f"Testing {args.calls} calls per {args.period}s...")
        for i in range(args.calls + 5):
            if limiter.allow():
                print(f"✓ Call {i+1} allowed")
            else:
                wait = limiter.wait_time()
                print(f"✗ Call {i+1} blocked (wait {wait:.1f}s)")
                time.sleep(wait)
                print(f"✓ After wait: call {i+1} allowed")
        return
    
    # Simple check
    if limiter.allow():
        print(f"✓ Call allowed ({args.calls}/{args.period}s limit)")
    else:
        wait = limiter.wait_time()
        print(f"✗ Blocked (wait {wait:.1f}s)")


if __name__ == "__main__":
    main()