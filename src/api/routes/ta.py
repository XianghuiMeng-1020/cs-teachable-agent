"""TA instance CRUD: list, create, get, delete."""

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import TACreate, TAResponse
from src.api.deps import DbSession, CurrentUser
from src.api.domain_helpers import get_domain_adapter
from src.db.models import User, TAInstance
from src.core.knowledge_state import StateTracker

router = APIRouter(prefix="/api/ta", tags=["ta"])


@router.get("", response_model=list[TAResponse])
def list_ta(current_user: CurrentUser, db: DbSession):
    instances = db.query(TAInstance).filter(TAInstance.user_id == current_user.id).all()
    return instances


@router.post("", response_model=TAResponse)
def create_ta(data: TACreate, current_user: CurrentUser, db: DbSession):
    adapter = get_domain_adapter(data.domain_id)
    units = adapter.load_knowledge_units()
    tracker = StateTracker(unit_definitions=units, domain=data.domain_id)
    state = tracker.get_full_state()
    ta = TAInstance(
        user_id=current_user.id,
        domain_id=data.domain_id,
        name=data.name,
        knowledge_state=state,
    )
    db.add(ta)
    db.commit()
    db.refresh(ta)
    return ta


@router.get("/{ta_id}", response_model=TAResponse)
def get_ta(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    return ta


@router.delete("/{ta_id}")
def delete_ta(ta_id: int, current_user: CurrentUser, db: DbSession):
    ta = db.query(TAInstance).filter(
        TAInstance.id == ta_id,
        TAInstance.user_id == current_user.id,
    ).first()
    if not ta:
        raise HTTPException(status_code=404, detail="TA not found")
    db.delete(ta)
    db.commit()
    return {"ok": True}
