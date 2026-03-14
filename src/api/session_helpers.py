"""Helpers for teaching session and event persistence."""

from datetime import datetime, timezone, timedelta

from src.db.models import TeachingSession, TeachingEvent, TestAttempt


def get_or_create_teaching_session(db, ta_instance_id: int):
    """Get or create a teaching session for this TA for today (UTC)."""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today_start + timedelta(days=1)

    session = (
        db.query(TeachingSession)
        .filter(
            TeachingSession.ta_instance_id == ta_instance_id,
            TeachingSession.started_at >= today_start,
            TeachingSession.started_at < tomorrow,
        )
        .order_by(TeachingSession.started_at.desc())
        .first()
    )
    if session:
        return session
    session = TeachingSession(ta_instance_id=ta_instance_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session
