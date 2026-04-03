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


class AssessmentItem(Base):
    __tablename__ = "assessment_items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String(128), unique=True, index=True, nullable=False)
    item_type = Column(String(32), nullable=False, index=True)  # parsons | dropdown | execution-trace
    domain_id = Column(String(50), nullable=False, default="python")
    source_query_id = Column(String(64), nullable=True)
    source_task_id = Column(String(64), nullable=True)
    title = Column(String(512), nullable=False)
    prompt = Column(Text, nullable=False)
    interaction_content = Column(JSON, nullable=False)
    answer_key = Column(JSON, nullable=False)
    grading_rule = Column(Text, nullable=True)
    metadata_theme = Column(String(128), nullable=True)
    metadata_concepts = Column(JSON, nullable=True)
    ai_pass_rate = Column(Float, nullable=True)
    difficulty = Column(Float, nullable=True)
    validation_passed = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    attempts = relationship("AssessmentAttempt", back_populates="item")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ta_instance_id = Column(Integer, ForeignKey("ta_instances.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("assessment_items.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("teaching_sessions.id"), nullable=True)
    attempt_number = Column(Integer, nullable=False, default=1)
    submission = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    score = Column(Float, nullable=True)
    expected_count = Column(Integer, nullable=True)
    selected_count = Column(Integer, nullable=True)
    correct_count = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    hints_used = Column(Integer, nullable=False, default=0)
    feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="assessment_attempts")
    item = relationship("AssessmentItem", back_populates="attempts")
    ta_instance = relationship("TAInstance", backref="assessment_attempts")
    session = relationship("TeachingSession", backref="assessment_attempts")


class AdminConfig(Base):
    """Key-value store for admin-controlled security and UI settings."""
    __tablename__ = "admin_config"

    id = Column(Integer, primary_key=True)
    key = Column(String(64), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GamificationProfile(Base):
    __tablename__ = "gamification_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    xp = Column(Integer, nullable=False, default=0)
    level = Column(Integer, nullable=False, default=1)
    streak_days = Column(Integer, nullable=False, default=0)
    badges = Column(JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="gamification_profile")


class CollaborationRoom(Base):
    __tablename__ = "collaboration_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    domain_id = Column(String(64), nullable=False, index=True)
    is_private = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    participants = relationship("CollaborationParticipant", back_populates="room")
    messages = relationship("CollaborationMessage", back_populates="room")


class CollaborationParticipant(Base):
    __tablename__ = "collaboration_participants"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("collaboration_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ta_id = Column(Integer, ForeignKey("ta_instances.id"), nullable=True)
    contribution_score = Column(Integer, nullable=False, default=0)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("CollaborationRoom", back_populates="participants")
    user = relationship("User")
    ta = relationship("TAInstance")


class CollaborationMessage(Base):
    __tablename__ = "collaboration_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("collaboration_rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(2000), nullable=False)
    message_type = Column(String(32), nullable=False, default="chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("CollaborationRoom", back_populates="messages")
    user = relationship("User")


class StudentFlag(Base):
    """Records of abnormal student behaviour detected automatically or flagged manually."""
    __tablename__ = "student_flags"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flag_type = Column(String(64), nullable=False, index=True)
    severity = Column(String(16), nullable=False, default="warning")
    detail = Column(JSON, nullable=True)
    session_id = Column(String(128), nullable=True)
    item_id = Column(Integer, nullable=True)
    resolved = Column(Boolean, nullable=False, default=False)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], backref="flags")
    resolver = relationship("User", foreign_keys=[resolved_by])
