"""
TA code generation constrained by knowledge state. Optional LLM path; output guard; stub fallback.
"""

from src.llm.client import llm_completion
from src.llm.guard import output_guard

# Correct code per problem_id (stub when TA has all required KUs and no failure injection).
# All 50 stage1 problems covered so tests can pass without LLM.
TA_CORRECT_CODE_BY_PROBLEM: dict[str, str] = {
    "prob_var_001": "age = 20\nprint(age)",
    "prob_var_002": 'greeting = "Hello"\nprint(greeting)',
    "prob_var_003": "a = 7\nb = 3\nprint(a)",
    "prob_var_004": "score = 100\nprint(score)",
    "prob_io_001": "line = input()\nprint(line)",
    "prob_io_002": "x = input()\nprint(x)",
    "prob_io_003": "line = input()\nprint(line)\nprint(line)",
    "prob_arith_001": "print(10 + 20)",
    "prob_arith_002": "a = int(input())\nb = int(input())\nprint(a + b)",
    "prob_arith_003": "print(15 - 6)",
    "prob_arith_004": "print(4 * 5)",
    "prob_arith_005": "n = int(input())\nprint(n * 2)",
    "prob_cond_001": "n = int(input())\nprint(\"positive\" if n > 0 else \"not positive\")",
    "prob_cond_002": "n = int(input())\nprint(\"even\" if n % 2 == 0 else \"odd\")",
    "prob_cond_003": "n = int(input())\nprint(\"negative\" if n < 0 else \"non-negative\")",
    "prob_cond_004": "n = int(input())\nprint(\"zero\" if n == 0 else \"positive\" if n > 0 else \"negative\")",
    "prob_cond_005": "n = int(input())\nprint(\"answer\" if n == 42 else \"no\")",
    "prob_loop_001": "for i in range(5):\n    print(i)",
    "prob_loop_002": "for i in range(3):\n    print(i)",
    "prob_loop_003": "i = 1\nwhile i <= 5:\n    print(i)\n    i += 1",
    "prob_loop_004": "for i in range(4):\n    print(i)",
    "prob_loop_005": "for i in range(6):\n    print(i)",
    "prob_loop_006": "i = 0\nwhile i < 5:\n    print(i)\n    i += 1",
    "prob_loop_007": "for c in \"abc\":\n    print(c)",
    "prob_list_001": "nums = [1, 2, 3]\nprint(nums[0])",
    "prob_list_002": "nums = [10, 20, 30]\nprint(len(nums))",
    "prob_list_003": "lst = [\"a\", \"b\", \"c\"]\nfor x in lst:\n    print(x)",
    "prob_list_004": "lst = [5, 10, 15, 20]\nprint(lst[1])",
    "prob_list_005": "lst = [\"x\", \"y\", \"z\"]\nprint(lst[-1])",
    "prob_list_006": "lst = [1, 2, 3]\nfor x in lst:\n    print(x)",
    "prob_list_007": "lst = [2, 4, 6, 8]\nprint(len(lst))",
    "prob_list_008": "lst = [1, 2]\nlst.append(3)\nprint(lst)",
    "prob_apply_001": "n = int(input())\nprint(\"big\" if n >= 10 else \"small\")",
    "prob_apply_002": "a = int(input())\nb = int(input())\nprint(\"same\" if a == b else \"different\")",
    "prob_apply_003": "n = int(input())\nprint(\"even\" if n % 2 == 0 else \"odd\")",
    "prob_apply_004": "a = int(input())\nb = int(input())\nprint(a if a >= b else b)",
    "prob_apply_005": "n = int(input())\nfor i in range(n):\n    print(i)",
    "prob_apply_006": "a = int(input())\nb = int(input())\nc = int(input())\nprint(min(a, b, c))",
    "prob_apply_007": "n = int(input())\nprint(\"in range\" if n >= 1 and n <= 5 else \"out\")",
    "prob_apply_008": "n = int(input())\nfor i in range(1, n + 1):\n    print(i)",
    "prob_apply_009": "lst = [10, 20, 30, 40]\nprint(lst[0] + lst[-1])",
    "prob_apply_010": "n = int(input())\nprint(\"fizzbuzz\" if n % 15 == 0 else \"fizz\" if n % 3 == 0 else \"buzz\" if n % 5 == 0 else n)",
    "prob_str_001": "msg = \"Python\"\nprint(msg)",
    "prob_str_002": "print(\"Hello \" + \"World\")",
    "prob_log_001": "n = int(input())\nprint(\"digit\" if n > 0 and n < 10 else \"other\")",
}

# Wrong code for failure-path demo (misconception). Must be runnable but fail test cases.
# assign_vs_equal: simulate wrong logic (e.g. always one branch). off_by_one_range: print 1..n instead of 0..n-1.
TA_WRONG_CODE_BY_PROBLEM: dict[str, str] = {
    "prob_var_001": "age = 20\nprint(age + 1)",
    "prob_var_002": 'greeting = "Hello"\nprint("Hi")',
    "prob_arith_001": "print(10 + 10)",
    "prob_cond_001": "n = int(input())\nprint(\"not positive\")",
    "prob_cond_002": "n = int(input())\nprint(\"odd\")",
    "prob_apply_001": "n = int(input())\nprint(\"small\")",
    "prob_apply_002": "a = int(input())\nb = int(input())\nprint(\"different\")",
    "prob_loop_001": "for i in range(5):\n    print(i + 1)",
    "prob_loop_002": "for i in range(3):\n    print(i + 1)",
    "prob_apply_005": "n = int(input())\nfor i in range(n):\n    print(i + 1)",
    "prob_apply_008": "n = int(input())\nfor i in range(n):\n    print(i + 1)",
}


def _extract_code(raw: str) -> str:
    """Strip markdown code fence if present."""
    text = (raw or "").strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def _get_stub_attempt(
    problem: dict,
    learned_unit_ids: set[str],
    force_fail_problem_ids: set[str],
    active_misconception_ids: list[str] | None,
) -> str:
    """Return stub code (correct or wrong) for the problem."""
    pid = problem.get("problem_id", "")
    required = set(problem.get("knowledge_units_tested", []))
    mis = active_misconception_ids or []

    if not required <= learned_unit_ids:
        return "# TA has not learned required units; no attempt.\nprint()"
    if mis and pid in TA_WRONG_CODE_BY_PROBLEM:
        return TA_WRONG_CODE_BY_PROBLEM[pid]
    if pid in force_fail_problem_ids and pid in TA_WRONG_CODE_BY_PROBLEM:
        return TA_WRONG_CODE_BY_PROBLEM[pid]
    return TA_CORRECT_CODE_BY_PROBLEM.get(pid, "# No stub for this problem\nprint()")


def get_ta_code_attempt(
    problem: dict,
    learned_unit_ids: set[str],
    active_misconceptions: list[str] | None = None,
    force_fail_problem_ids: set[str] | None = None,
    *,
    filled_prompt: str | None = None,
    use_llm_code: bool | None = None,
) -> str:
    """
    Return TA code attempt. If filled_prompt and use_llm_code, try LLM then guard; else stub.
    """
    required = set(problem.get("knowledge_units_tested", []))
    force_fail = force_fail_problem_ids or set()
    pid = problem.get("problem_id", "")
    active_mis_list = list(active_misconceptions) if active_misconceptions else None

    if not required <= learned_unit_ids:
        return _get_stub_attempt(
            problem, learned_unit_ids, force_fail, active_mis_list
        )
    if pid in force_fail:
        return _get_stub_attempt(
            problem, learned_unit_ids, force_fail, active_mis_list
        )
    if use_llm_code is not True or not filled_prompt:
        return _get_stub_attempt(
            problem, learned_unit_ids, force_fail, active_mis_list
        )

    raw = llm_completion(filled_prompt, max_tokens=256, temperature=0.3)
    code = _extract_code(raw) if raw else ""
    if code and output_guard(code):
        return code
    return _get_stub_attempt(
        problem, learned_unit_ids, force_fail, active_mis_list
    )
