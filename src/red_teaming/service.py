"""FastAPI service module. Optional import: ``app`` is None when FastAPI
is not installed, and the service tests skip in that case."""
from __future__ import annotations
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    _HAS_FASTAPI = True
except ImportError:  # pragma: no cover - environment without FastAPI
    FastAPI = None  # type: ignore
    BaseModel = object  # type: ignore
    _HAS_FASTAPI = False

if _HAS_FASTAPI:
    from .attacks import build_attack_library
    from .runner import run_evaluation
    from .scorers import score_results
    from .target import ScriptedTarget

    app = FastAPI(title="Red-Teaming Platform")

    class EvaluateRequest(BaseModel):
        mode: str = "strict"

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/attacks")
    def list_attacks() -> list[dict]:
        return [{"id": c.id, "category": c.category.value, "severity": c.severity.value,
                 "technique": c.technique} for c in build_attack_library()]

    @app.post("/evaluate")
    def evaluate(req: EvaluateRequest) -> dict:
        results = run_evaluation(ScriptedTarget(mode=req.mode))
        summary = score_results(results)
        return {"total": summary.total, "successes": summary.successes,
                "attack_success_rate": summary.attack_success_rate,
                "critical_successes": summary.critical_successes}
else:
    app = None
