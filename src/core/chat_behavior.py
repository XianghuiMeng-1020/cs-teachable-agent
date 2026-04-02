"""
Chat behavior analysis for detecting AI-generated paste patterns.

Analyzes typing cadence, response timing, and linguistic patterns
to flag potentially AI-assisted responses.
"""

import re
import statistics
from typing import Any


# Patterns commonly seen in GPT output
_GPT_MARKERS = [
    r"(?i)\blet me explain\b",
    r"(?i)\bhere'?s (?:what|how|why)\b",
    r"(?i)\bin summary\b",
    r"(?i)\bspecifically,?\b",
    r"(?i)\bfurthermore\b",
    r"(?i)\bmoreover\b",
    r"(?i)\bit'?s worth noting\b",
    r"(?i)\bI'?d be happy to\b",
    r"(?i)\bI hope this helps\b",
    r"(?i)\bas an AI\b",
    r"(?i)\bgreat question\b",
    r"(?i)\bfirstly.*secondly.*thirdly\b",
]

_GPT_PATTERNS_COMPILED = [re.compile(p) for p in _GPT_MARKERS]


def compute_gpt_pattern_score(text: str) -> float:
    """
    Score 0.0-1.0 indicating likelihood of AI-generated text.
    Higher = more likely AI-generated.
    """
    if not text or len(text) < 20:
        return 0.0

    score = 0.0
    hits = 0

    for pat in _GPT_PATTERNS_COMPILED:
        if pat.search(text):
            hits += 1

    score += min(0.4, hits * 0.1)

    words = text.split()
    if len(words) > 5:
        avg_word_len = sum(len(w) for w in words) / len(words)
        if avg_word_len > 6.5:
            score += 0.1

    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) >= 3:
        lens = [len(s.split()) for s in sentences]
        if len(lens) >= 2:
            cv = statistics.stdev(lens) / max(statistics.mean(lens), 1)
            if cv < 0.3:
                score += 0.15

    bullet_count = text.count("\n- ") + text.count("\n* ") + text.count("\n1.")
    if bullet_count >= 3:
        score += 0.15

    if re.search(r'```\w+\n', text):
        score += 0.2

    return min(1.0, score)


def analyze_response_timing(
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze timing patterns in a conversation to detect anomalies.
    Each message should have 'timestamp' (ISO string) and 'role'.
    Returns analysis with flags.
    """
    from datetime import datetime

    student_gaps: list[float] = []
    ta_response_gaps: list[float] = []

    for i in range(1, len(messages)):
        prev = messages[i - 1]
        curr = messages[i]
        try:
            t_prev = datetime.fromisoformat(prev["timestamp"].replace("Z", "+00:00"))
            t_curr = datetime.fromisoformat(curr["timestamp"].replace("Z", "+00:00"))
            gap_ms = (t_curr - t_prev).total_seconds() * 1000
        except (KeyError, ValueError, TypeError):
            continue

        if curr.get("role") == "student" and prev.get("role") == "ta":
            student_gaps.append(gap_ms)
        elif curr.get("role") == "ta" and prev.get("role") == "student":
            ta_response_gaps.append(gap_ms)

    flags = []

    if student_gaps:
        ultra_fast = [g for g in student_gaps if g < 5000]
        if len(ultra_fast) >= 3:
            flags.append({
                "type": "rapid_student_responses",
                "count": len(ultra_fast),
                "avg_ms": statistics.mean(ultra_fast),
            })

    if student_gaps and len(student_gaps) >= 3:
        std = statistics.stdev(student_gaps) if len(student_gaps) > 1 else 0
        mean = statistics.mean(student_gaps)
        if std < 1000 and mean < 10000:
            flags.append({
                "type": "robotic_timing",
                "mean_ms": mean,
                "std_ms": std,
            })

    return {
        "student_response_gaps": student_gaps,
        "avg_student_gap_ms": statistics.mean(student_gaps) if student_gaps else None,
        "flags": flags,
    }


def analyze_message_for_cheating(
    text: str,
    elapsed_ms: float | None = None,
    char_count: int | None = None,
) -> dict[str, Any]:
    """
    Analyze a single student message for cheating indicators.
    Returns a dict with 'suspicious' bool and 'reasons' list.
    """
    reasons = []
    gpt_score = compute_gpt_pattern_score(text)

    if gpt_score >= 0.5:
        reasons.append(f"High GPT-pattern score: {gpt_score:.2f}")

    if elapsed_ms is not None and char_count is not None:
        if char_count > 100 and elapsed_ms < 5000:
            cps = char_count / (elapsed_ms / 1000)
            if cps > 30:
                reasons.append(f"Typing speed {cps:.0f} chars/sec exceeds human max")

    if text.count("\n") > 10 and len(text) > 300:
        reasons.append("Unusually structured multi-line response")

    return {
        "suspicious": len(reasons) > 0,
        "gpt_pattern_score": gpt_score,
        "reasons": reasons,
    }
