"""
Stage One: Demo runner for all scenarios (hardening pass).
  Scenario A: Minimal learned state – only print_function; verify selection is constrained.
  Scenario B: Success path – teach variable_assignment + print_function → problem → PASS.
  Scenario C: Failure path – same teaching, TA produces wrong code → FAIL.

Run from repository root:  python prototype/demo_stage1.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = REPO_ROOT / "seed"


def main() -> None:
    ku_path = SEED_DIR / "knowledge-units-stage1.json"
    problems_path = SEED_DIR / "sample-problems-stage1.json"

    if not ku_path.exists() or not problems_path.exists():
        print("Missing seed files. Run from repo root and ensure seed/ exists.", file=sys.stderr)
        sys.exit(1)

    from demo_scenarios import (
        run_scenario_a,
        run_scenario_b,
        run_scenario_c,
        print_scenario_a_output,
        print_scenario_b_output,
        print_scenario_c_output,
    )

    print("=" * 60)
    print("Stage One Prototype – Multiple scenarios (hardening pass)")
    print("=" * 60)

    # ---------- Scenario A ----------
    print("\n" + "=" * 60)
    print("Scenario A: Minimal learned state (print_function only)")
    print("Goal: Only problems requiring learned units can be selected;")
    print("      problems requiring untaught concepts are not selected.")
    print("=" * 60)
    data_a = run_scenario_a(ku_path, problems_path)
    print_scenario_a_output(data_a)

    # ---------- Scenario B ----------
    print("\n" + "=" * 60)
    print("Scenario B: Success path (variable_assignment + print_function)")
    print("Goal: Teach two units → select matching problem → TA succeeds → mastery PASS.")
    print("=" * 60)
    data_b = run_scenario_b(ku_path, problems_path)
    print_scenario_b_output(data_b)
    if not data_b["pass_fail"]:
        print("  WARNING: Scenario B expected PASS.", file=sys.stderr)

    # ---------- Scenario C ----------
    print("\n" + "=" * 60)
    print("Scenario C: Failure path (simulated misconception)")
    print("Goal: Same teaching as B, but TA produces wrong code → evaluator FAIL → mastery reflects failure.")
    print("=" * 60)
    data_c = run_scenario_c(ku_path, problems_path)
    print_scenario_c_output(data_c)
    if data_c["pass_fail"]:
        print("  WARNING: Scenario C expected FAIL.", file=sys.stderr)

    print("\n" + "=" * 60)
    print("End of demo: A (selection constraint), B (success), C (failure) completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
