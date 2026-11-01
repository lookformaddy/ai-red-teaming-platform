from red_teaming.gates import check_regression_gate
from red_teaming.runner import run_evaluation
from red_teaming.scorers import score_results
from red_teaming.target import ScriptedTarget

def test_strict_passes_default_gate():
    s = score_results(run_evaluation(ScriptedTarget("strict")))
    assert check_regression_gate(s).passed

def test_lenient_fails_gate_and_baseline_regression_detected():
    cur = score_results(run_evaluation(ScriptedTarget("lenient")))
    base = score_results(run_evaluation(ScriptedTarget("strict")))
    gate = check_regression_gate(cur, baseline=base)
    assert not gate.passed and gate.violations
