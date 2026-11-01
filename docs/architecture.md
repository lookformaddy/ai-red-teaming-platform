# Architecture

```
attacks.py (21 deterministic cases)
      |
      v
runner.py -- Target protocol --> ScriptedTarget (or a real LLM client)
      |
      v
scorers.py --> EvaluationSummary (ASR, refusal rate, per-category, severity)
      |                |
      v                v
report.py        gates.py (ASR cap + baseline delta + critical-success rule)
      |
      v
service.py (FastAPI, optional) / cli.py / demo.py
```

## Data flow

1. `build_attack_library()` returns the fixed 21-case library, grouped by
   category (`prompt_injection`, `jailbreak`, `pii_extraction`,
   `toxicity_bias`, `tool_abuse`) and severity (`low`–`critical`).
2. The runner calls `target.respond(case)` once per case, in order.
3. Scorers aggregate; gates compare against a cap and an optional baseline.
4. Reports render the same summary as Markdown or JSON.

## Extension points

- New attack: add one `_c(...)` entry in `attacks.py` and a test asserting
  its expected outcome against the scripted target.
- New target: implement `respond(case) -> TargetResponse`; nothing else changes.
- New scorer metric: extend `EvaluationSummary` and `score_results`.
- Production hardening: rate-limit the service, add auth, replace the
  keyword policy with a guardrail model, and add a judge scorer per category.

## Safety notes

All prompts are synthetic and generic. PII probes use category names only
("social security number", "credit card number") — never real values.
No employer code, data, or internal designs are included.
