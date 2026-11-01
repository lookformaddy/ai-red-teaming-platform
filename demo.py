"""Demo: run the full library against the strict scripted target and print the report."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve() / "src" if False else Path(__file__).parent / "src"))
from red_teaming import (ScriptedTarget, build_attack_library, check_regression_gate,
                         generate_markdown_report, run_evaluation, score_results)

def main() -> None:
    cases = build_attack_library()
    print(f"Attack library: {len(cases)} cases across "
          f"{len({c.category for c in cases})} categories")
    results = run_evaluation(ScriptedTarget(mode="strict"), cases)
    summary = score_results(results)
    print(generate_markdown_report(summary, results), end="")
    gate = check_regression_gate(summary)
    print(f"Regression gate: {'PASS' if gate.passed else 'FAIL'}")

if __name__ == "__main__":
    main()
