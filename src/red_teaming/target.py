"""Pluggable target interface + deterministic scripted target (no network).

A real deployment swaps ScriptedTarget for a wrapper around an LLM client;
the runner, scorers and gates only depend on the ``respond`` contract.
"""
from __future__ import annotations
from typing import Protocol
from .models import AttackCase, TargetResponse

class Target(Protocol):
    def respond(self, case: AttackCase) -> TargetResponse: ...

# Naive keyword refusal policy -- intentionally imperfect, so sneaky
# variants (PI-05, JB-05) bypass it and show up as attack successes.
DEFAULT_REFUSAL_PHRASES = (
    "ignore previous instructions", "reveal your system prompt", "system prompt",
    "social security", "ssn", "credit card number", "password",
    "unrestricted", "no safety rules", "dan", "no restrictions",
    "hateful insult", "rank these demographic", "harassing messages",
    "delete_database", "delete all production", "transfer_funds",
    "send_email", "read_file", "/etc/passwd", "bypass safety",
    "disregard all prior rules",
)

class ScriptedTarget:
    """Deterministic stand-in target.

    mode='strict' refuses every phrase-list hit; mode='lenient' refuses
    only critical-severity hits, letting the rest through -- useful for
    demonstrating regression gates failing against a weaker target.
    """
    def __init__(self, mode: str = "strict",
                 refusal_phrases: tuple[str, ...] = DEFAULT_REFUSAL_PHRASES) -> None:
        if mode not in ("strict", "lenient"):
            raise ValueError(f"unknown mode: {mode!r}")
        self.mode = mode
        self.refusal_phrases = refusal_phrases

    def respond(self, case: AttackCase) -> TargetResponse:
        text = case.prompt.lower()
        hit = any(p in text for p in self.refusal_phrases)
        if self.mode == "lenient":
            from .models import Severity
            hit = hit and case.severity == Severity.CRITICAL
        if hit:
            return TargetResponse(text="I can't help with that request.", refused=True, latency_ms=5)
        return TargetResponse(text=f"Completed request: {case.prompt[:80]}", refused=False, latency_ms=5)
