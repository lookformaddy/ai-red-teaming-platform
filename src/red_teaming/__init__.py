"""LLM red-teaming / adversarial evaluation platform (clean-room, synthetic data only)."""
from .models import AttackCase, AttackCategory, EvaluationResult, Severity, TargetResponse
from .attacks import build_attack_library
from .target import ScriptedTarget
from .runner import run_evaluation
from .scorers import score_results
from .gates import check_regression_gate
from .report import generate_json_report, generate_markdown_report

__all__ = ["AttackCase","AttackCategory","EvaluationResult","Severity","TargetResponse",
 "build_attack_library","ScriptedTarget","run_evaluation","score_results",
 "check_regression_gate","generate_json_report","generate_markdown_report"]
__version__ = "1.0.0"
