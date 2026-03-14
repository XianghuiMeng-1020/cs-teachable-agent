"""
Output guard for TA-generated code. Rejects out-of-scope constructs (def, class, import, etc.)
and optionally enforces knowledge-state: only constructs corresponding to learned KUs allowed (AST-level).
"""

import ast
import re
from typing import Set

# Forbidden patterns for introductory Python scope (regex fallback)
_FORBIDDEN_PATTERNS = [
    re.compile(r"\bdef\s+\w+", re.IGNORECASE),
    re.compile(r"\bclass\s+\w+", re.IGNORECASE),
    re.compile(r"\bimport\s+", re.IGNORECASE),
    re.compile(r"\bopen\s*\(", re.IGNORECASE),
    re.compile(r"\btry\s*:", re.IGNORECASE),
    re.compile(r"\bexcept\b", re.IGNORECASE),
    re.compile(r"\bwith\s+\w+\s+as\b", re.IGNORECASE),
]

# Map AST node usage to required knowledge unit IDs (Stage One scope)
_AST_NODE_TO_KU: dict[type, list[str]] = {
    ast.For: ["for_loop_range", "for_loop_iterable"],
    ast.While: ["while_loop"],
    ast.If: ["if_statement", "if_else", "if_elif_else"],
    ast.Compare: ["comparison_operators"],
    ast.BoolOp: ["logical_operators"],
    ast.UnaryOp: ["arithmetic_operators"],
    ast.BinOp: ["arithmetic_operators", "string_concatenation"],
    ast.Subscript: ["list_indexing"],
    ast.Call: ["print_function", "user_input", "list_basics"],
    ast.List: ["list_creation"],
    ast.Assign: ["variable_assignment"],
    ast.Constant: ["data_types_int_float", "data_types_string", "data_types_bool"],
}


def _collect_required_kus_from_ast(tree: ast.AST) -> Set[str]:
    """Walk AST and collect required KU ids for used constructs."""
    required: Set[str] = set()

    def visit(node: ast.AST) -> None:
        for kus in _AST_NODE_TO_KU.get(type(node), []):
            required.add(kus)
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return required


def ast_guard(code: str, allowed_ku_ids: Set[str]) -> bool:
    """
    Return True if code only uses constructs that map to KUs in allowed_ku_ids.
    Uses ast.parse; on parse error returns False.
    """
    if not code or not code.strip():
        return False
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    required = _collect_required_kus_from_ast(tree)
    if not required:
        return True
    return required <= allowed_ku_ids


def output_guard(code: str, allowed_ku_ids: Set[str] | None = None) -> bool:
    """
    Return True if the code is allowed: no forbidden constructs (regex), and if
    allowed_ku_ids is provided, only AST-allowed constructs (knowledge-state guard).
    """
    if not code or not code.strip():
        return False
    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(code):
            return False
    if allowed_ku_ids is not None:
        return ast_guard(code, allowed_ku_ids)
    return True
