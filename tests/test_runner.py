from red_teaming.attacks import build_attack_library
from red_teaming.runner import run_evaluation
from red_teaming.target import ScriptedTarget

def test_strict_target_refuses_most_but_sneaky_variants_succeed():
    results = run_evaluation(ScriptedTarget(mode="strict"))
    assert len(results) == 21
    succeeded = {r.case.id for r in results if r.attack_succeeded}
    assert succeeded == {"PI-04", "PII-04", "PI-05", "JB-05"}  # evasion variants by design

def test_lenient_target_lets_more_through():
    strict = sum(r.attack_succeeded for r in run_evaluation(ScriptedTarget("strict")))
    lenient = sum(r.attack_succeeded for r in run_evaluation(ScriptedTarget("lenient")))
    assert lenient > strict

def test_unknown_mode_rejected():
    import pytest
    with pytest.raises(ValueError):
        ScriptedTarget(mode="chaos")
