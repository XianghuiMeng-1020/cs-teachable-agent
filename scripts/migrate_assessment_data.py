"""
Migrate assessment items from Assessment Studio outputs/ directory into the database.

Usage:
    python -m scripts.migrate_assessment_data [--outputs-dir PATH] [--db-url URL]

Scans outputs/query_*/task_*/ for *-parsons.json, *-dropdown.json, *-execution-trace.json,
reads corresponding *-eval/summary.json for AI pass rates, and inserts into assessment_items table.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, AssessmentItem

ITEM_TYPE_SUFFIXES = {
    "-parsons.json": "parsons",
    "-dropdown.json": "dropdown",
    "-execution-trace.json": "execution-trace",
}

DEFAULT_OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "AI-assisted-Assessment-studio-main" / "outputs"


def find_typed_items(outputs_dir: Path) -> list[dict]:
    """Scan outputs directory and collect all typed assessment items."""
    items = []

    for query_dir in sorted(outputs_dir.iterdir()):
        if not query_dir.is_dir() or not query_dir.name.startswith("query_"):
            continue
        query_id = query_dir.name

        for task_dir in sorted(query_dir.iterdir()):
            if not task_dir.is_dir() or not task_dir.name.startswith("task_"):
                continue
            task_id = task_dir.name

            for json_file in sorted(task_dir.iterdir()):
                if not json_file.is_file():
                    continue
                for suffix, item_type in ITEM_TYPE_SUFFIXES.items():
                    if json_file.name.endswith(suffix):
                        items.append({
                            "path": json_file,
                            "query_id": query_id,
                            "task_id": task_id,
                            "item_type": item_type,
                        })
                        break

    return items


def load_eval_summary(item_path: Path) -> dict | None:
    """Load the AI evaluation summary for an item if it exists."""
    base_name = item_path.stem
    eval_dir = item_path.parent / f"{base_name}-eval"
    summary_path = eval_dir / "summary.json"
    if summary_path.exists():
        with open(summary_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def parse_item(info: dict) -> dict | None:
    """Parse a single assessment item JSON file into a DB record dict."""
    try:
        with open(info["path"], encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  SKIP {info['path']}: {e}")
        return None

    eval_summary = load_eval_summary(info["path"])
    ai_pass_rate = None
    if eval_summary:
        ai_pass_rate = eval_summary.get("pass_rate")

    metadata = raw.get("metadata", {})
    validation = raw.get("validation", {})

    quality = metadata.get("quality_metrics", {})
    total_stu = _to_float(quality.get("total_num_stu"))
    passed_stu = _to_float(quality.get("num_passed_stu"))
    student_pass_rate = (passed_stu / total_stu * 100) if total_stu and passed_stu is not None else None

    interaction_content = raw.get("interaction_content", {})
    answer_key = _normalize_answer_key(
        info["item_type"],
        interaction_content,
        raw.get("answer_key", {}),
    )

    return {
        "item_id": raw.get("item_id", f"{info['task_id']}-{info['item_type']}"),
        "item_type": info["item_type"],
        "domain_id": "python",
        "source_query_id": info["query_id"],
        "source_task_id": info["task_id"],
        "title": raw.get("title", info["task_id"]),
        "prompt": raw.get("prompt", ""),
        "interaction_content": interaction_content,
        "answer_key": answer_key,
        "grading_rule": raw.get("grading_rule"),
        "metadata_theme": metadata.get("theme"),
        "metadata_concepts": metadata.get("concepts", []),
        "ai_pass_rate": ai_pass_rate,
        "difficulty": _compute_difficulty(ai_pass_rate, student_pass_rate),
        "validation_passed": validation.get("passed"),
    }


def _normalize_answer_key(item_type: str, interaction_content: dict, answer_key: dict) -> dict:
    """
    Ensure answer key fields are present and aligned with interaction_content.

    Studio exports sometimes place correct answers on blanks/checkpoints directly.
    Our grading pipeline expects answer_key.correct_answers consistently.
    """
    normalized = dict(answer_key or {})

    if item_type == "dropdown":
        blanks = interaction_content.get("blanks", []) or []
        inferred = {
            b.get("blank_id"): b.get("correct_answer")
            for b in blanks
            if b.get("blank_id") and b.get("correct_answer") is not None
        }
        existing = normalized.get("correct_answers", {}) or {}
        if inferred:
            merged = dict(inferred)
            merged.update(existing)
            normalized["correct_answers"] = merged
        elif "correct_answers" not in normalized:
            normalized["correct_answers"] = {}

    if item_type == "execution-trace":
        checkpoints = interaction_content.get("checkpoints", []) or []
        inferred = {
            cp.get("checkpoint_id"): cp.get("correct")
            for cp in checkpoints
            if cp.get("checkpoint_id") and cp.get("correct") is not None
        }
        existing = normalized.get("correct_answers", {}) or {}
        if inferred:
            merged = dict(inferred)
            merged.update(existing)
            normalized["correct_answers"] = merged
        elif "correct_answers" not in normalized:
            normalized["correct_answers"] = {}

    return normalized


def _to_float(val) -> float | None:
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _compute_difficulty(ai_pass_rate: float | None, student_pass_rate: float | None) -> float | None:
    if ai_pass_rate is not None:
        return round(1.0 - ai_pass_rate / 100.0, 3)
    if student_pass_rate is not None:
        return round(1.0 - student_pass_rate / 100.0, 3)
    return None


def migrate(outputs_dir: Path, db_url: str) -> None:
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Scanning: {outputs_dir}")
    found = find_typed_items(outputs_dir)
    print(f"Found {len(found)} typed assessment item files")

    inserted = 0
    skipped = 0
    errors = 0

    for info in found:
        record = parse_item(info)
        if not record:
            errors += 1
            continue

        existing = session.query(AssessmentItem).filter(
            AssessmentItem.item_id == record["item_id"]
        ).first()

        if existing:
            print(f"  EXISTS: {record['item_id']} (updating)")
            for key, val in record.items():
                setattr(existing, key, val)
            skipped += 1
        else:
            item = AssessmentItem(**record)
            session.add(item)
            inserted += 1
            print(f"  INSERT: {record['item_id']} ({record['item_type']}) - {record['title']}")

    session.commit()
    session.close()

    print(f"\nDone: {inserted} inserted, {skipped} updated, {errors} errors")


def main():
    parser = argparse.ArgumentParser(description="Migrate assessment items to database")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=DEFAULT_OUTPUTS_DIR,
        help="Path to Assessment Studio outputs/ directory",
    )
    parser.add_argument(
        "--db-url",
        default=os.environ.get("DATABASE_URL", "sqlite:///./data/app.db"),
        help="Database URL (default: from DATABASE_URL env var or sqlite:///./data/app.db)",
    )
    args = parser.parse_args()

    if not args.outputs_dir.exists():
        print(f"Error: outputs directory not found: {args.outputs_dir}")
        sys.exit(1)

    migrate(args.outputs_dir, args.db_url)


if __name__ == "__main__":
    main()
