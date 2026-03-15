"""
Learning gain measurement: pre-test / post-test and normalized gain.
"""

from __future__ import annotations

def normalized_gain(pre_score: float, post_score: float, max_score: float = 1.0) -> float:
    """Normalized gain (Hake): (post - pre) / (max - pre). Returns 0 if pre >= max."""
    if max_score <= 0 or pre_score >= max_score:
        return 0.0
    return (post_score - pre_score) / (max_score - pre_score)


def learning_gain_summary(
    pre_scores: dict[str, float],
    post_scores: dict[str, float],
    *,
    max_score: float = 1.0,
) -> dict:
    """Per-unit and aggregate learning gain. pre_scores/post_scores: unit_id -> score."""
    unit_ids = set(pre_scores.keys()) | set(post_scores.keys())
    gains = {}
    for uid in unit_ids:
        pre = pre_scores.get(uid, 0.0)
        post = post_scores.get(uid, 0.0)
        gains[uid] = normalized_gain(pre, post, max_score)
    n = len(gains)
    avg_gain = sum(gains.values()) / n if n else 0.0
    return {
        "per_unit_gain": gains,
        "average_normalized_gain": round(avg_gain, 4),
        "units_count": n,
    }
