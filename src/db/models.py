"""SQLAlchemy ORM models for User, TAInstance, sessions, events, trace."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="student")  # student | teacher
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ta_instances = relationship("TAInstance", back_populates="user")


class TAInstance(Base):
    __tablename__ = "ta_instances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    domain_id = Column(String(50), nullable=False, default="python")
    name = Column(String(255), nullable=True)  # optional display name
    knowledge_state = Column(JSON, nullable=False, default=dict)  # full state snapshot
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="ta_instances")
    teaching_sessions = relationship("TeachingSession", back_populates="ta_instance")


class TeachingSession(Base):
    __tablename__ = "teaching_sessions"

    id = Column(Integer, primary_key=True, index=True)
    ta_instance_id = Column(Integer, ForeignKey("ta_instances.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    ta_instance = relationship("TAInstance", back_populates="teaching_sessions")
    teaching_events = relationship("TeachingEvent", back_populates="session")
    test_attempts = relationship("TestAttempt", back_populates="session")
    trace_events = relationship("TraceEvent", back_populates="session")


class TeachingEvent(Base):
    __tablename__ = "teaching_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("teaching_sessions.id"), nullable=False)
    teaching_event_id = Column(String(64), unique=True, index=True, nullable=False)
    student_input = Column(Text, nullable=True)
    topic_taught = Column(String(255), nullable=True)
    interpreted_units = Column(JSON, nullable=True)  # list of KU ids
    quality_score = Column(Float, nullable=True)
    ta_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TeachingSession", back_populates="teaching_events")


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("teaching_sessions.id"), nullable=False)
    problem_id = Column(String(64), nullable=False)
    ta_code = Column(Text, nullable=True)
    passed = Column(Boolean, nullable=False)
    execution_output = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    misconceptions_active = Column(JSON, nullable=True)  # list of misconception ids
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TeachingSession", back_populates="test_attempts")


class TraceEvent(Base):
    __tablename__ = "trace_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("teaching_sessions.id"), nullable=True)
    event_type = Column(String(64), nullable=False, index=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TeachingSession", back_populates="trace_events")
