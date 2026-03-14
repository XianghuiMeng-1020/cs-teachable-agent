"""
Select problems from the bank that fit the TA's current knowledge state.
Only problems whose knowledge_units_tested are all learned/partially_learned are eligible.
"""

import json
from pathlib import Path


def load_problems(path: Path) -> list[dict]:
    """Load problems from JSON (e.g. sample-problems-stage1.json or domain seed)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("problems", [])


def select_problem(problems: list[dict], learned_unit_ids: set[str]) -> dict | None:
    """Select one problem that the TA is allowed to attempt."""
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if required and required <= learned_unit_ids:
            return p
    return None


def get_eligible_problem_ids(problems: list[dict], learned_unit_ids: set[str]) -> list[str]:
    """Return list of problem_ids that the TA is allowed to attempt."""
    out = []
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if required and required <= learned_unit_ids:
            out.append(p.get("problem_id", ""))
    return out


def get_ineligible_reasons(problems: list[dict], learned_unit_ids: set[str]) -> list[dict]:
    """Return for each ineligible problem: problem_id, required units, missing units."""
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
