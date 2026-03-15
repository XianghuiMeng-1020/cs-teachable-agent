"""
A/B experiment framework: assign users to conditions (e.g. with/without Teaching Helper).
"""

from __future__ import annotations

import hashlib

CONDITION_CONTROL = "control"
CONDITION_TREATMENT_HELPER = "treatment_teaching_helper"
CONDITION_TREATMENT_MODE_SHIFT = "treatment_mode_shift"
CONDITIONS = [CONDITION_CONTROL, CONDITION_TREATMENT_HELPER, CONDITION_TREATMENT_MODE_SHIFT]


def get_condition_for_user(user_id: int, seed: str = "cs-ta-exp") -> str:
    """Deterministically assign user to a condition based on user_id and seed."""
    h = hashlib.sha256(f"{seed}:{user_id}".encode()).hexdigest()
    idx = int(h[:8], 16) % len(CONDITIONS)
    return CONDITIONS[idx]


def has_teaching_helper(condition: str) -> bool:
    return condition == CONDITION_TREATMENT_HELPER


def has_mode_shift(condition: str) -> bool:
    return condition == CONDITION_TREATMENT_MODE_SHIFT
