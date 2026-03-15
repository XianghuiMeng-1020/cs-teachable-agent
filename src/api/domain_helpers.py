"""Shared domain adapter and state helpers for TA routes."""

from pathlib import Path

from fastapi import HTTPException

from src.core.knowledge_state import StateTracker
from src.db.models import TAInstance
from src.domains.python_domain import PythonDomainAdapter
from src.domains.database_domain import DatabaseDomainAdapter
from src.domains.ai_literacy_domain import AILiteracyDomainAdapter

_SEED_ROOT = Path(__file__).resolve().parent.parent.parent


def get_domain_adapter(domain_id: str):
    """Return the DomainAdapter for the given domain_id."""
    if domain_id == "python":
        return PythonDomainAdapter(seed_dir=_SEED_ROOT / "seed")
    if domain_id == "database":
        return DatabaseDomainAdapter()
    if domain_id == "ai_literacy":
        return AILiteracyDomainAdapter()
    raise HTTPException(status_code=400, detail=f"Unknown domain: {domain_id}")


def get_tracker_for_ta(ta: TAInstance) -> StateTracker:
    """Build a StateTracker from TA instance using the correct domain adapter."""
    adapter = get_domain_adapter(ta.domain_id)
    units = adapter.load_knowledge_units()
    tracker = StateTracker(unit_definitions=units, domain=ta.domain_id)
    if ta.knowledge_state and isinstance(ta.knowledge_state, dict):
        units = ta.knowledge_state.get("units", {})
        if not isinstance(units, dict):
            units = {}
        tracker.merge_persisted_state(
            units,
            reflection_store=ta.knowledge_state.get("reflection_store"),
        )
    return tracker


def save_tracker_to_ta(ta: TAInstance, tracker: StateTracker, db) -> None:
    """Persist tracker state to TA instance and commit."""
    ta.knowledge_state = tracker.get_full_state()
    db.add(ta)
    db.commit()
