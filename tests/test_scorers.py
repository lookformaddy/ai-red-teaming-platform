from red_teaming.runner import run_evaluation
from red_teaming.scorers import score_results
from red_teaming.target import ScriptedTarget

def test_scores_for_strict_target():
    s = score_results(run_evaluation(ScriptedTarget("strict")))
    assert s.total == 21 and s.successes == 4
    assert abs(s.attack_success_rate - 4/21) < 1e-9 and abs(s.refusal_rate - 17/21) < 1e-9
    assert s.critical_successes == 0
    assert s.by_category is not None

def test_empty_results_score_safely():
    s = score_results([])
    assert s.total == 0 and s.attack_success_rate == 0.0 and s.refusal_rate == 1.0
