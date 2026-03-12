"""
Stage One: Select one problem from the curated bank that fits the TA's current knowledge state.
Only problems whose knowledge_units_tested are all learned/partially_learned are eligible.
"""

import json
from pathlib import Path


def load_problems(path: Path) -> list[dict]:
    """Load problems from sample-problems-stage1.json."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("problems", [])


def select_problem(problems: list[dict], learned_unit_ids: set[str]) -> dict | None:
    """
    Select one problem that the TA is allowed to attempt:
    every knowledge_unit in knowledge_units_tested must be in learned_unit_ids.
    Returns first matching problem, or None if none match.
    """
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if required and required <= learned_unit_ids:
            return p
    return None


def get_eligible_problem_ids(problems: list[dict], learned_unit_ids: set[str]) -> list[str]:
    """Return list of problem_ids that the TA is allowed to attempt (all required KUs learned)."""
    out = []
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if required and required <= learned_unit_ids:
            out.append(p.get("problem_id", ""))
    return out


def get_ineligible_reasons(problems: list[dict], learned_unit_ids: set[str]) -> list[dict]:
    """
    Return for each problem that is NOT eligible: problem_id, required units, missing units.
    Makes it clear why a problem was not selected (untaught concepts).
    """
    reasons = []
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if not required:
            continue
        missing = required - learned_unit_ids
        if missing:
            reasons.append({
                "problem_id": p.get("problem_id", ""),
                "required_units": sorted(required),
                "missing_units": sorted(missing),
            })
    return reasons
