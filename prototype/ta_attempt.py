"""
Stage One: Generate TA code attempt constrained by current knowledge state.
- Success only when all required knowledge units are learned.
- Failure can occur when required units are missing OR when a misconception is active.
- The TA never uses concepts outside the current learned state.
Rule-based/stub implementation; no LLM.
"""

# Correct code per problem_id (used when TA has all required KUs and no failure injection).
TA_CORRECT_CODE_BY_PROBLEM: dict[str, str] = {
    "prob_var_001": "age = 20\nprint(age)",
    "prob_var_002": 'greeting = "Hello"\nprint(greeting)',
    "prob_io_001": "line = input()\nprint(line)",
    "prob_io_002": "x = input()\nprint(x)",
    "prob_arith_001": "print(10 + 20)",
    "prob_loop_001": "for i in range(5):\n    print(i)",
    "prob_loop_002": "for i in range(3):\n    print(i)",
    "prob_list_001": "nums = [1, 2, 3]\nprint(nums[0])",
    "prob_list_002": "nums = [10, 20, 30]\nprint(len(nums))",
}

# Wrong code per problem_id for failure-path demo (e.g. misconception: wrong output).
# Used when force_fail_problem_ids contains this problem_id.
TA_WRONG_CODE_BY_PROBLEM: dict[str, str] = {
    "prob_var_001": "age = 20\nprint(age + 1)",  # prints 21 instead of 20
    "prob_var_002": 'greeting = "Hello"\nprint("Hi")',  # wrong string
    "prob_arith_001": "print(10 + 10)",  # 20 instead of 30
}


def get_ta_attempt(
    problem: dict,
    learned_unit_ids: set[str],
    force_fail_problem_ids: set[str] | None = None,
    active_misconception_ids: list[str] | None = None,
) -> str:
    """
    Return TA's code attempt for the given problem.
    - If any required KU is not in learned_unit_ids, return a no-attempt placeholder.
    - If active_misconception_ids is non-empty (state-driven misconception for a tested unit)
      and we have wrong code for this problem, return that wrong code (Stage C path).
    - If force_fail_problem_ids contains this problem_id, return wrong code (fallback).
    - Otherwise return correct stub code when available.
    """
    pid = problem.get("problem_id", "")
    required = set(problem.get("knowledge_units_tested", []))
    force_fail = force_fail_problem_ids or set()
    mis = active_misconception_ids or []

    if not required <= learned_unit_ids:
        return "# TA has not learned required units; no attempt.\nprint()"

    # State-driven misconception: any active misconception on tested units → wrong code if we have it
    if mis and pid in TA_WRONG_CODE_BY_PROBLEM:
        return TA_WRONG_CODE_BY_PROBLEM[pid]

    if pid in force_fail and pid in TA_WRONG_CODE_BY_PROBLEM:
        return TA_WRONG_CODE_BY_PROBLEM[pid]

    return TA_CORRECT_CODE_BY_PROBLEM.get(pid, "# No stub for this problem\nprint()")
