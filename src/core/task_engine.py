"""
Select problems from the bank that fit the TA's current knowledge state.
Supports multiple strategies: coverage, difficulty (ZPD), spaced repetition, misconception diagnosis.
"""

import json
import time
from pathlib import Path
from typing import Any

STRATEGY_COVERAGE = "coverage"
STRATEGY_DIFFICULTY = "difficulty"
STRATEGY_SPACED = "spaced"
STRATEGY_MISCONCEPTION = "misconception"
STRATEGY_UNCERTAINTY = "uncertainty"
STRATEGY_ROUND_ROBIN = "round_robin"
DEFAULT_STRATEGY = STRATEGY_UNCERTAINTY


def load_problems(path: Path) -> list[dict]:
    """Load problems from JSON (e.g. sample-problems-stage1.json or domain seed)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("problems", [])


def get_eligible_problems(
    problems: list[dict], learned_unit_ids: set[str]
) -> list[dict]:
    """Return problems whose required KUs are all in learned."""
    out = []
    for p in problems:
        required = set(p.get("knowledge_units_tested", []))
        if required and required <= learned_unit_ids:
            out.append(p)
    return out


def get_eligible_problem_ids(problems: list[dict], learned_unit_ids: set[str]) -> list[str]:
    """Return list of problem_ids that the TA is allowed to attempt."""
    return [p.get("problem_id", "") for p in get_eligible_problems(problems, learned_unit_ids)]


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


def _score_coverage(problem: dict, p_know: dict[str, float]) -> float:
    """Lower avg p_know of required KUs => higher priority (need more practice)."""
    required = problem.get("knowledge_units_tested", [])
    if not required:
        return 1.0
    avg = sum(p_know.get(uid, 0.0) for uid in required) / len(required)
    return 1.0 - avg


def _score_difficulty(problem: dict, p_know: dict[str, float], zpd_min: float = 0.4, zpd_max: float = 0.85) -> float:
    """Prefer problems in ZPD: avg p_know in [zpd_min, zpd_max]. Distance from 0.6 ideal."""
    required = problem.get("knowledge_units_tested", [])
    if not required:
        return 0.0
    avg = sum(p_know.get(uid, 0.0) for uid in required) / len(required)
    if zpd_min <= avg <= zpd_max:
        ideal = 0.6
        return 1.0 - abs(avg - ideal)
    return 0.0


def _score_spaced(problem: dict, last_practiced: dict[str, float]) -> float:
    """Larger time since last practice => higher priority."""
    required = problem.get("knowledge_units_tested", [])
    if not required:
        return 0.0
    now = time.time()
    min_last = min(last_practiced.get(uid, 0.0) for uid in required)
    return min(1.0, (now - min_last) / 86400.0)


def _score_misconception(problem: dict, active_misconception_ids: list[str]) -> float:
    """Prefer problems that target an active misconception."""
    targeted = set(problem.get("targeted_misconceptions", []) or [])
    if not active_misconception_ids or not targeted:
        return 0.0
    overlap = len(set(active_misconception_ids) & targeted)
    return float(overlap)


def _score_uncertainty(problem: dict, p_know: dict[str, float]) -> float:
    """Uncertainty-based: prefer problem whose required KUs have p_know closest to 0.5 (max uncertainty)."""
    required = problem.get("knowledge_units_tested", [])
    if not required:
        return 0.0
    # Score = 1 - min distance from 0.5 (higher = more uncertain = better to test)
    distances = [abs(p_know.get(uid, 0.5) - 0.5) for uid in required]
    min_dist = min(distances)
    return 1.0 - min_dist


def select_problem(
    problems: list[dict],
    learned_unit_ids: set[str],
    tracker: Any = None,
    strategy: str = DEFAULT_STRATEGY,
) -> dict | None:
    """
    Select one problem. If tracker is provided and strategy is not round_robin,
    use adaptive strategy; otherwise use first eligible (legacy).
    """
    eligible = get_eligible_problems(problems, learned_unit_ids)
    if not eligible:
        return None
    if tracker is None or strategy == STRATEGY_ROUND_ROBIN:
        return eligible[0]
    p_know = {}
    last_practiced = {}
    if hasattr(tracker, "get_bkt_state"):
        p_know = tracker.get_bkt_state()
    if hasattr(tracker, "_state"):
        for uid, rec in tracker._state.items():
            ts = rec.get("last_practiced_at")
            if ts:
                try:
                    last_practiced[uid] = float(ts)
                except (TypeError, ValueError):
                    last_practiced[uid] = 0.0
    active_mis = []
    if hasattr(tracker, "get_active_misconception_ids"):
        active_mis = tracker.get_active_misconception_ids(learned_unit_ids) or []

    # Misconception-targeted: prefer problems that exercise active misconceptions
    if strategy == STRATEGY_MISCONCEPTION and active_mis:
        scored = [(p, _score_misconception(p, active_mis)) for p in eligible]
        scored = [(p, s) for p, s in scored if s > 0]
        if scored:
            scored.sort(key=lambda x: -x[1])
            return scored[0][0]
    # Uncertainty-based: prefer problem where p_know is closest to 0.5 (most informative)
    if strategy == STRATEGY_UNCERTAINTY and p_know:
        scored = [(p, _score_uncertainty(p, p_know)) for p in eligible]
        scored.sort(key=lambda x: -x[1])
        if scored and scored[0][1] > 0:
            return scored[0][0]
    if strategy == STRATEGY_SPACED and last_practiced:
        scored = [(p, _score_spaced(p, last_practiced)) for p in eligible]
        scored.sort(key=lambda x: -x[1])
        if scored and scored[0][1] > 0:
            return scored[0][0]
    if strategy == STRATEGY_DIFFICULTY:
        scored = [(p, _score_difficulty(p, p_know)) for p in eligible]
        scored = [(p, s) for p, s in scored if s > 0]
        if scored:
            scored.sort(key=lambda x: -x[1])
            return scored[0][0]
    scored = [(p, _score_coverage(p, p_know)) for p in eligible]
    scored.sort(key=lambda x: -x[1])
    return scored[0][0] if scored else eligible[0]
