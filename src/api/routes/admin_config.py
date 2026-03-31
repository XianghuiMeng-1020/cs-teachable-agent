"""Admin configuration and student flag endpoints."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from src.api.deps import CurrentUser, CurrentUserOptional, get_db
from src.db.models import AdminConfig, StudentFlag, User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])

# ── Default security settings ────────────────────────────────────────

DEFAULTS: dict[str, Any] = {
    "anti_capture_enabled": True,
    "anti_capture_hz": 40,
    "focus_loss_threshold": 5,
    "min_solve_time_ms": 15000,
    "typing_anomaly_enabled": True,
    "watermark_enabled": True,
    "devtools_detection_enabled": True,
    "print_block_enabled": True,
    "ocr_noise_enabled": True,
}


def _get_config_map(db: Session) -> dict[str, Any]:
    rows = db.query(AdminConfig).all()
    merged = dict(DEFAULTS)
    for row in rows:
        merged[row.key] = row.value
    return merged


# ── Schemas ──────────────────────────────────────────────────────────

class ConfigResponse(BaseModel):
    settings: dict[str, Any]


class ConfigUpdateRequest(BaseModel):
    settings: dict[str, Any]


class FlagCreate(BaseModel):
    user_id: int
    flag_type: str
    severity: str = "warning"
    detail: dict | None = None
    session_id: str | None = None
    item_id: int | None = None


class FlagOut(BaseModel):
    id: int
    user_id: int
    username: str | None = None
    flag_type: str
    severity: str
    detail: dict | None
    session_id: str | None
    item_id: int | None
    resolved: bool
    resolved_by: int | None
    resolved_at: str | None
    created_at: str | None


class FlagSummaryItem(BaseModel):
    user_id: int
    username: str
    total_flags: int
    unresolved: int
    critical: int
    warning: int
    info: int
    latest_flag_at: str | None


# ── Config endpoints ─────────────────────────────────────────────────

@router.get("/config", response_model=ConfigResponse)
def get_admin_config(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(CurrentUserOptional),
):
    """Public: students need Hz and feature flags to render overlays."""
    return ConfigResponse(settings=_get_config_map(db))


@router.put("/config", response_model=ConfigResponse)
def update_admin_config(
    body: ConfigUpdateRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    for key, value in body.settings.items():
        row = db.query(AdminConfig).filter(AdminConfig.key == key).first()
        if row:
            row.value = value
            row.updated_by = current_user.id
        else:
            db.add(AdminConfig(key=key, value=value, updated_by=current_user.id))
    db.commit()
    return ConfigResponse(settings=_get_config_map(db))


# ── Flag endpoints ───────────────────────────────────────────────────

@router.get("/flags")
def list_flags(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    user_id: int | None = Query(None),
    flag_type: str | None = Query(None),
    severity: str | None = Query(None),
    resolved: bool | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    q = db.query(StudentFlag, User.username).join(User, StudentFlag.user_id == User.id)
    if user_id is not None:
        q = q.filter(StudentFlag.user_id == user_id)
    if flag_type:
        q = q.filter(StudentFlag.flag_type == flag_type)
    if severity:
        q = q.filter(StudentFlag.severity == severity)
    if resolved is not None:
        q = q.filter(StudentFlag.resolved == resolved)

    total = q.count()
    rows = q.order_by(StudentFlag.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "flags": [
            FlagOut(
                id=f.id, user_id=f.user_id, username=uname,
                flag_type=f.flag_type, severity=f.severity,
                detail=f.detail, session_id=f.session_id, item_id=f.item_id,
                resolved=f.resolved, resolved_by=f.resolved_by,
                resolved_at=str(f.resolved_at) if f.resolved_at else None,
                created_at=str(f.created_at) if f.created_at else None,
            ).dict()
            for f, uname in rows
        ],
        "total": total,
    }


@router.post("/flags")
def create_flag(
    body: FlagCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    flag = StudentFlag(
        user_id=body.user_id,
        flag_type=body.flag_type,
        severity=body.severity,
        detail=body.detail,
        session_id=body.session_id,
        item_id=body.item_id,
    )
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return {"id": flag.id, "ok": True}


@router.patch("/flags/{flag_id}")
def resolve_flag(
    flag_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    flag = db.query(StudentFlag).filter(StudentFlag.id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")

    flag.resolved = True
    flag.resolved_by = current_user.id
    flag.resolved_at = datetime.now(timezone.utc)
    db.commit()
    return {"ok": True}


@router.get("/flags/summary")
def flag_summary(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")

    from sqlalchemy import case

    rows = (
        db.query(
            StudentFlag.user_id,
            User.username,
            sa_func.count(StudentFlag.id).label("total"),
            sa_func.sum(case((StudentFlag.resolved == False, 1), else_=0)).label("unresolved"),
            sa_func.sum(case((StudentFlag.severity == "critical", 1), else_=0)).label("critical"),
            sa_func.sum(case((StudentFlag.severity == "warning", 1), else_=0)).label("warning"),
            sa_func.sum(case((StudentFlag.severity == "info", 1), else_=0)).label("info"),
            sa_func.max(StudentFlag.created_at).label("latest"),
        )
        .join(User, StudentFlag.user_id == User.id)
        .group_by(StudentFlag.user_id, User.username)
        .order_by(sa_func.sum(case((StudentFlag.resolved == False, 1), else_=0)).desc())
        .all()
    )

    return {
        "students": [
            FlagSummaryItem(
                user_id=r.user_id, username=r.username,
                total_flags=r.total, unresolved=r.unresolved or 0,
                critical=r.critical or 0, warning=r.warning or 0, info=r.info or 0,
                latest_flag_at=str(r.latest) if r.latest else None,
            ).dict()
            for r in rows
        ]
    }
