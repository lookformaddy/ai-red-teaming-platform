# ai-red-teaming-platform

An LLM red-teaming / adversarial evaluation platform: a deterministic library
of attack probes, a pluggable target interface, scorers, regression gates, and
Markdown/JSON reporting — plus an optional FastAPI service and a CLI.

## Enterprise problem

Shipping an LLM feature without adversarial testing means discovering prompt
injection, PII leakage, and tool-abuse failures in production. Teams need a
repeatable, CI-gatable evaluation that runs on every model or prompt change,
with a baseline comparison that blocks regressions before release.

## Architecture

- `src/red_teaming/attacks.py` — deterministic attack library (21 cases):
  prompt injection, jailbreak templates, PII-extraction probes, toxicity/bias
  probes, tool-abuse scenarios, plus two keyword-evasion variants.
- `src/red_teaming/target.py` — `Target` protocol + `ScriptedTarget`
  (deterministic, no network/keys). Swap in a real LLM client behind the
  same `respond(case)` contract.
- `src/red_teaming/runner.py` — runs every case against a target.
- `src/red_teaming/scorers.py` — attack success rate, refusal rate,
  per-category pass rates, severity breakdown, critical successes.
- `src/red_teaming/gates.py` — regression gate vs an ASR cap and a baseline.
- `src/red_teaming/report.py` — Markdown / JSON reports.
- `src/red_teaming/service.py` — FastAPI service (`/health`, `/attacks`,
  `/evaluate`); `app` is `None` when FastAPI is not installed.
- `src/red_teaming/cli.py` — `--list` / `--run` CLI with gate verdict.

See `docs/architecture.md` for the full design.

## How to run

```bash
pip install -r requirements.txt   # pytest; fastapi/uvicorn optional
python3 demo.py
python3 -m pytest -q
PYTHONPATH=src python3 -m red_teaming.cli --run
PYTHONPATH=src python3 -m red_teaming.cli --run --mode lenient  # gate FAILs, by design
```

Against the default strict scripted target, 17/21 attacks are refused and
the 4 evasion variants succeed (ASR 19.0%) — the gate passes at the
default 20% cap. The lenient target fails the gate, demonstrating regression
detection.

## Key design decisions and trade-offs

- **Deterministic, offline core.** No randomness without a seed, no network
  calls in core/tests, so results are reproducible in CI.
- **Scripted target is intentionally naive.** A keyword refusal policy is
  easy to evade — that is the point: it surfaces bypass classes rather than
  pretending to be a production guardrail.
- **Success = non-refusal.** A deliberately simple, auditable scoring rule;
  production deployments should add judge-based scoring per category.
- **CI workflow ships as `docs/github-actions-ci.yml`**, not
  `.github/workflows/`, because the push integration rejects workflow paths;
  it activates by moving it into place.

## What it demonstrates

Adversarial evaluation design, pluggable model targets, safety metrics and
regression gating, clean-room synthetic test data, and a service + CLI
surface suitable for CI integration.
