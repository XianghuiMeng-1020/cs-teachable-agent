"""
Output guard for TA-generated code. Rejects out-of-scope constructs (def, class, import, etc.)
to prevent knowledge leakage and ensure Stage One scope.
"""

import re

# Forbidden patterns for introductory Python scope
_FORBIDDEN_PATTERNS = [
    re.compile(r"\bdef\s+\w+", re.IGNORECASE),
    re.compile(r"\bclass\s+\w+", re.IGNORECASE),
    re.compile(r"\bimport\s+", re.IGNORECASE),
    re.compile(r"\bopen\s*\(", re.IGNORECASE),
    re.compile(r"\btry\s*:", re.IGNORECASE),
    re.compile(r"\bexcept\b", re.IGNORECASE),
    re.compile(r"\bwith\s+\w+\s+as\b", re.IGNORECASE),
]


def output_guard(code: str) -> bool:
    """
    Return True if the code is allowed (no forbidden constructs).
    Rejects def, class, import, open(, try:, except, with...as.
    """
    if not code or not code.strip():
        return False
    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(code):
            return False
    return True
