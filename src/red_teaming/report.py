"""Markdown + JSON report generation (pure functions, deterministic output)."""
from __future__ import annotations
import json
from .models import EvaluationResult, EvaluationSummary

def _category_lines(summary: EvaluationSummary) -> list[str]:
    lines = []
    for cat in sorted(summary.by_category, key=lambda c: c.value):
        cs = summary.by_category[cat]
        lines.append(f"- {cat.value}: {cs.total - cs.successes}/{cs.total} passed "
                     f"({cs.pass_rate:.0%} pass rate, {cs.successes} succeeded)")
    return lines

def generate_markdown_report(summary: EvaluationSummary,
                             results: list[EvaluationResult]) -> str:
    lines = ["# Red-Teaming Evaluation Report", "",
             f"- Total attacks: {summary.total}",
             f"- Attack success rate: {summary.attack_success_rate:.2%}",
             f"- Refusal rate: {summary.refusal_rate:.2%}",
             f"- Critical successes: {summary.critical_successes}", "",
             "## Per-category pass rates", *_category_lines(summary), "",
             "## Severity breakdown (successful attacks)"]
    for sev in sorted(summary.by_severity, key=lambda s: s.value):
        lines.append(f"- {sev.value}: {summary.by_severity[sev]}")
    lines += ["", "## Successful attacks"]
    for r in results:
        if r.attack_succeeded:
            lines.append(f"- {r.case.id} [{r.case.category.value}/{r.case.severity.value}] "
                         f"{r.case.technique}")
    return chr(10).join(lines) + chr(10)

def generate_json_report(summary: EvaluationSummary,
                         results: list[EvaluationResult]) -> str:
    payload = {
        "total": summary.total, "successes": summary.successes,
        "attack_success_rate": summary.attack_success_rate,
        "refusal_rate": summary.refusal_rate,
        "critical_successes": summary.critical_successes,
        "by_category": {c.value: {"total": cs.total, "successes": cs.successes,
                                   "pass_rate": cs.pass_rate}
                        for c, cs in summary.by_category.items()},
        "by_severity": {s.value: n for s, n in summary.by_severity.items()},
        "successful_attack_ids": [r.case.id for r in results if r.attack_succeeded],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + chr(10)
