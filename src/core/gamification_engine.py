"""Gamification: points, level, achievements from teaching and test data."""

from __future__ import annotations

POINTS_PER_TEACH = 1
POINTS_PER_TEST_PASS = 5
POINTS_PER_TEST_ATTEMPT = 2
POINTS_PER_LEVEL = 50

ACHIEVEMENTS = [
    {"id": "first_teach", "name": "First lesson", "description": "Teach your TA once", "required": 1, "type": "teach"},
    {"id": "teach_5", "name": "Getting started", "description": "Teach 5 times", "required": 5, "type": "teach"},
    {"id": "teach_10", "name": "Dedicated teacher", "description": "Teach 10 times", "required": 10, "type": "teach"},
    {"id": "first_pass", "name": "First pass", "description": "Pass a test", "required": 1, "type": "test_pass"},
    {"id": "pass_5", "name": "On a roll", "description": "Pass 5 tests", "required": 5, "type": "test_pass"},
    {"id": "early_bird", "name": "Early bird", "description": "Reach level 2", "required": 2, "type": "level"},
]


def compute_points(teach_count: int, test_attempt_count: int, test_pass_count: int) -> int:
    return (
        teach_count * POINTS_PER_TEACH
        + test_pass_count * POINTS_PER_TEST_PASS
        + (test_attempt_count - test_pass_count) * POINTS_PER_TEST_ATTEMPT
    )


def level_from_points(points: int) -> int:
    return max(1, 1 + points // POINTS_PER_LEVEL)


def all_achievements_with_status(
    teach_count: int, test_pass_count: int, level: int
) -> list[dict]:
    result = []
    for a in ACHIEVEMENTS:
        unlocked = False
        if a["type"] == "teach":
            unlocked = teach_count >= a["required"]
        elif a["type"] == "test_pass":
            unlocked = test_pass_count >= a["required"]
        elif a["type"] == "level":
            unlocked = level >= a["required"]
        result.append({
            "id": a["id"],
            "name": a["name"],
            "description": a["description"],
            "unlocked": unlocked,
        })
    return result
