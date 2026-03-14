"""Database domain: execute SQL and compare result sets (SQLite, result set comparison, partial correctness)."""

import sqlite3
from pathlib import Path
from typing import Any


def _normalize_row(row: tuple) -> tuple:
    """Normalize for comparison (e.g. float tolerance)."""
    out = []
    for v in row:
        if isinstance(v, float):
            out.append(round(v, 10))
        else:
            out.append(v)
    return tuple(out)


def _rows_to_set(rows: list[tuple]) -> set[tuple]:
    return {_normalize_row(r) for r in rows}


def _run_schema(conn: sqlite3.Connection, schema_path: Path) -> None:
    sql_text = schema_path.read_text(encoding="utf-8")
    conn.executescript(sql_text)


def _execute_sql(conn: sqlite3.Connection, sql: str) -> tuple[list[tuple], str]:
    """Execute single SELECT (or DML); return (rows, error_msg). For SELECT return fetched rows."""
    sql = (sql or "").strip()
    if not sql:
        return [], "No SQL provided."
    try:
        cur = conn.execute(sql)
        if cur.description:
            return list(cur.fetchall()), ""
        conn.commit()
        return [], ""
    except sqlite3.Error as e:
        return [], str(e)


def _compare_result_sets(
    got_rows: list[tuple],
    expected_rows: list[list[Any]],
    order_matters: bool = False,
) -> tuple[bool, float, str]:
    """
    Compare got vs expected. expected_rows are from JSON (list of lists).
    Returns (passed, partial_score, message).
    """
    expected_tuples = [tuple(r) for r in expected_rows]
    got_norm = [_normalize_row(r) for r in got_rows]
    exp_set = _rows_to_set(expected_tuples)
    got_set = _rows_to_set(got_rows)

    if order_matters:
        if len(got_norm) != len(expected_tuples):
            return False, 0.0, f"Row count mismatch: got {len(got_norm)}, expected {len(expected_tuples)}"
        for i, (g, e) in enumerate(zip(got_norm, expected_tuples)):
            if _normalize_row(g) != _normalize_row(tuple(e)):
                return False, 0.0, f"Row {i+1} mismatch"
        return True, 1.0, "Exact match (order)."

    if got_set == exp_set:
        return True, 1.0, "Exact match."
    if not exp_set:
        return len(got_set) == 0, 1.0 if len(got_set) == 0 else 0.0, "No rows expected."
    intersection = len(got_set & exp_set)
    union = len(got_set | exp_set)
    partial = intersection / len(exp_set) if exp_set else 1.0
    passed = got_set == exp_set
    return passed, partial, f"Partial: {intersection}/{len(exp_set)} rows correct."


def evaluate_sql_attempt(
    problem: dict,
    sql: str,
    schema_path: Path | None = None,
    *,
    order_matters: bool = False,
) -> dict:
    """
    Execute SQL against a test DB (schema from schema_path), compare to problem expected_rows.
    Returns {passed: bool, details: [...], score: float, stdout, stderr}.
    """
    if not sql or not sql.strip():
        return {"passed": False, "details": [], "stdout": "", "stderr": "No SQL provided.", "score": 0.0}
    expected_rows = problem.get("expected_rows", [])
    schema_path = schema_path or Path(__file__).resolve().parent.parent.parent.parent / "seed" / "database" / "schema.sql"

    try:
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        try:
            if schema_path.exists():
                _run_schema(conn, schema_path)
            got_rows, err = _execute_sql(conn, sql)
            if err:
                return {
                    "passed": False,
                    "details": [{"error": err}],
                    "stdout": "",
                    "stderr": err,
                    "score": 0.0,
                }
            passed, score, msg = _compare_result_sets(got_rows, expected_rows, order_matters=order_matters)
            return {
                "passed": passed,
                "details": [{"message": msg, "rows_returned": len(got_rows)}],
                "stdout": str(got_rows)[:500],
                "stderr": "",
                "score": round(score, 2),
            }
        finally:
            conn.close()
    except Exception as e:
        return {
            "passed": False,
            "details": [{"error": str(e)}],
            "stdout": "",
            "stderr": str(e),
            "score": 0.0,
        }
