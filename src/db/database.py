"""Database connection and session management."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.db.models import Base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./data/app.db",
)

if DATABASE_URL.startswith("sqlite"):
    raw = DATABASE_URL.split("///", 1)[-1] if "///" in DATABASE_URL else ""
    if raw:
        Path(raw).parent.mkdir(parents=True, exist_ok=True)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
