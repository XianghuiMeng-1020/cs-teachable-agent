"""AI Literacy domain: LLM rubric-based evaluation and partial correctness scoring."""

import re
from src.llm.client import llm_completion

PASS_THRESHOLD = 0.6


def _heuristic_score(problem: dict, answer: str) -> float:
    """Fallback when LLM unavailable: simple keyword overlap with rubric."""
    rubric = (problem.get("rubric") or "").lower()
    answer_lower = (answer or "").lower()
    if not rubric or not answer_lower:
        return 0.0
    words = set(re.findall(r"\w+", rubric))
    answer_words = set(re.findall(r"\w+", answer_lower))
    overlap = len(words & answer_words) / len(words) if words else 0.0
    return min(1.0, overlap * 1.5)


def evaluate_concept_attempt(problem: dict, code_or_answer: str) -> dict:
    """
    Evaluate open-ended concept answer using problem rubric. LLM scores 0-1; fallback heuristic.
    Returns {passed: bool, details: [...], score: float, stdout, stderr}.
    """
    answer = (code_or_answer or "").strip()
    if not answer:
        return {"passed": False, "details": [], "stdout": "", "stderr": "No answer.", "score": 0.0}

    rubric = problem.get("rubric", "")
    statement = problem.get("problem_statement", "")
    prompt = f"""You are grading a short-answer question.

Question: {statement}
Rubric (what a good answer should include): {rubric}

Student answer: {answer}

Reply with exactly two lines:
Line 1: A number between 0 and 1 (score, e.g. 0.7).
Line 2: One short sentence explaining why (optional).

Example:
0.8
The answer correctly mentions key points from the rubric."""

    out = llm_completion(prompt, max_tokens=150, temperature=0.1)
    score = 0.0
    reason = ""

    if out:
        lines = [l.strip() for l in (out or "").strip().split("\n") if l.strip()]
        for line in lines:
            try:
                s = float(line.strip().split()[0].replace(",", "."))
                if 0 <= s <= 1:
                    score = s
                    break
            except (ValueError, IndexError):
                continue
        if len(lines) > 1:
            reason = lines[1][:200]

    if score == 0.0 and not out:
        score = _heuristic_score(problem, answer)
        reason = "Scored by heuristic (LLM unavailable)."

    passed = score >= PASS_THRESHOLD
    return {
        "passed": passed,
        "details": [{"score": score, "reason": reason or "Rubric-based evaluation."}],
        "stdout": answer[:500],
        "stderr": "",
        "score": round(score, 2),
    }
