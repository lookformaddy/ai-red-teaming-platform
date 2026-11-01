import json
from red_teaming.report import generate_json_report, generate_markdown_report
from red_teaming.runner import run_evaluation
from red_teaming.scorers import score_results
from red_teaming.target import ScriptedTarget

def _setup():
    results = run_evaluation(ScriptedTarget("strict"))
    return score_results(results), results

def test_markdown_report_contains_key_sections():
    s, r = _setup()
    md = generate_markdown_report(s, r)
    assert "# Red-Teaming Evaluation Report" in md
    assert "PI-05" in md and "Attack success rate" in md

def test_json_report_round_trips():
    s, r = _setup()
    payload = json.loads(generate_json_report(s, r))
    assert payload["total"] == 21 and payload["successes"] == 4
    assert payload["successful_attack_ids"] == ["PI-04", "PII-04", "PI-05", "JB-05"]
