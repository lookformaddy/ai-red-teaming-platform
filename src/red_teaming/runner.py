"""Evaluation runner: deterministic, sequential, no concurrency surprises."""
from __future__ import annotations
from .models import AttackCase, EvaluationResult
from .target import Target

def run_evaluation(target: Target, cases: list[AttackCase] | None = None) -> list[EvaluationResult]:
    from .attacks import build_attack_library
    cases = build_attack_library() if cases is None else cases
    return [EvaluationResult(case=c, response=target.respond(c)) for c in cases]
