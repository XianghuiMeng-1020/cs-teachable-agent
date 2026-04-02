"""
Dynamic problem variant generation.
Randomizes variable names and numeric values in code problems
to make each student's version unique, preventing answer sharing.
"""

import hashlib
import random
import re

# Pools for random variable names
_VAR_POOLS = [
    ["x", "y", "z", "w", "v"],
    ["alpha", "beta", "gamma", "delta", "epsilon"],
    ["val", "num", "count", "total", "result"],
    ["a", "b", "c", "d", "e"],
    ["item", "elem", "data", "value", "temp"],
]

_NAME_POOLS = [
    ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    ["Max", "Luna", "Oscar", "Ivy", "Leo"],
]


def _seed_for_student(problem_id: str, user_id: int) -> int:
    """Deterministic seed so same student always sees same variant."""
    h = hashlib.md5(f"{problem_id}:{user_id}".encode()).hexdigest()
    return int(h[:8], 16)


def generate_variant(problem: dict, user_id: int) -> dict:
    """
    Generate a student-specific variant of a problem.
    Replaces numeric literals and simple variable names with randomized alternatives.
    Returns a new dict (original is not modified).
    """
    if user_id <= 0:
        return problem

    problem_id = problem.get("problem_id", "")
    rng = random.Random(_seed_for_student(problem_id, user_id))

    variant = dict(problem)
    variant["_variant_seed"] = _seed_for_student(problem_id, user_id)

    code = variant.get("code", "")
    correct_code = variant.get("correct_code", "")

    if not code:
        return variant

    # Generate number replacements (small ints only to keep problems meaningful)
    number_map = {}
    for match in re.finditer(r"\b(\d{1,3})\b", code):
        orig = int(match.group(1))
        if orig in (0, 1) or orig in number_map:
            continue
        # Replace with a nearby value (±50% but at least ±1)
        low = max(2, int(orig * 0.5))
        high = max(orig + 2, int(orig * 1.5))
        new_val = rng.randint(low, high)
        if new_val == orig:
            new_val = orig + rng.choice([-1, 1])
        number_map[orig] = max(2, new_val)

    # Apply number replacements to code and correct_code
    def replace_numbers(text: str) -> str:
        def _repl(m):
            n = int(m.group(0))
            return str(number_map.get(n, n))

        return re.sub(r"\b(\d{1,3})\b", _repl, text)

    if number_map:
        variant["code"] = replace_numbers(code)
        if correct_code:
            variant["correct_code"] = replace_numbers(correct_code)
        # Update expected_output if it's a prediction problem
        if variant.get("expected_output") and variant.get("problem_type") == "output-prediction":
            # Re-running code would be ideal, but for safety just mark as needs-recompute
            variant["_output_needs_recompute"] = True

    # Randomize string names in code (e.g., "Alice" -> "Bob")
    name_pool = rng.choice(_NAME_POOLS)
    rng.shuffle(name_pool)
    name_idx = 0
    for orig_pool in _NAME_POOLS:
        for name in orig_pool:
            if name in code and name_idx < len(name_pool):
                replacement = name_pool[name_idx]
                variant["code"] = variant["code"].replace(f'"{name}"', f'"{replacement}"')
                variant["code"] = variant["code"].replace(f"'{name}'", f"'{replacement}'")
                if variant.get("correct_code"):
                    variant["correct_code"] = variant["correct_code"].replace(
                        f'"{name}"', f'"{replacement}"'
                    )
                    variant["correct_code"] = variant["correct_code"].replace(
                        f"'{name}'", f"'{replacement}'"
                    )
                name_idx += 1

    return variant


def generate_variants_for_problems(
    problems: list[dict],
    user_id: int,
) -> list[dict]:
    """Generate variants for all problems in a list."""
    return [generate_variant(p, user_id) for p in problems]
