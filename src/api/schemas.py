"""Pydantic request/response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ----- Auth -----
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# ----- TA -----
class TACreate(BaseModel):
    domain_id: str = "python"
    name: str | None = None


class TAResponse(BaseModel):
    id: int
    user_id: int
    domain_id: str
    name: str | None
    knowledge_state: dict
    created_at: datetime | None = None

    class Config:
        from_attributes = True


# ----- Teaching -----
class TeachRequest(BaseModel):
    student_input: str = Field(..., description="Student's teaching message (natural language or structured)")


class TeachResponse(BaseModel):
    teaching_event_id: str
    interpreted_units: list[str]
    topic_taught: str
    quality_score: float
    state_update: dict
    ta_response: str


class CorrectRequest(BaseModel):
    unit_id: str
    misconception_id: str
    explanation: str = ""


# ----- Testing -----
class TestRequest(BaseModel):
    problem_id: str | None = None  # If None, system selects one


class TestResponse(BaseModel):
    problem_id: str
    problem_statement: str
    ta_code: str
    passed: bool
    details: list[dict]
    mastery_report: dict
    reflection_prompt: str | None = None


class ComprehensiveTestResultItem(BaseModel):
    problem_id: str
    passed: bool
    problem_statement: str


class ComprehensiveTestResponse(BaseModel):
    total_run: int
    total_passed: int
    results: list[ComprehensiveTestResultItem]
    overall_summary: str


# ----- State -----
class StateResponse(BaseModel):
    domain: str
    units: dict[str, Any]
    learned_unit_ids: list[str]
    active_misconception_ids: list[str]
    knowledge_unit_definitions: list[dict] | None = None  # id, name, prerequisites for graph


class MasteryResponse(BaseModel):
    selected_problem_id: str | None
    required_kus: list[str]
    learned_kus_at_attempt: list[str]
    pass_fail: str | None
    overall_summary: str
    per_problem_interpretation: str | None = None
    ta_code_preview: str | None = None
    mastery_percent: int | None = None
    pass_rate: float | None = None
    test_count: int | None = None


class MisconceptionDetail(BaseModel):
    id: str
    description: str
    affected_units: list[str]
    remediation_hint: str
    status: str  # active | correcting | resolved
    activated_at: str | None = None
    severity_score: float | None = None
    trigger_count: int | None = None


class MisconceptionsResponse(BaseModel):
    active_misconception_ids: list[str]
    misconceptions: list[MisconceptionDetail]


class TraceEventResponse(BaseModel):
    id: int
    event_type: str
    payload: dict | None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    id: str
    type: str  # teach | test_pass | test_fail | misconception_activated | correction | relearning
    title: str
    description: str
    timestamp: str
    metadata: dict[str, Any] | None = None


class HistoryResponse(BaseModel):
    items: list[HistoryItem]
    total: int
    page: int
    per_page: int


# ----- Teacher Transcripts -----
class TranscriptSessionSummary(BaseModel):
    session_id: int
    student: dict  # { id, username }
    ta_id: int
    domain_id: str
    message_count: int
    kus_covered: list[str]
    started_at: str
    ended_at: str | None = None


class TranscriptListResponse(BaseModel):
    items: list[TranscriptSessionSummary]
    total: int
    page: int
    per_page: int


class TranscriptMessageSchema(BaseModel):
    seq: int
    type: str  # teach | test
    speaker: str  # student | ta | system
    content: str
    interpreted_units: list[str] | None
    quality_score: float | None
    timestamp: str


class TranscriptDetailResponse(BaseModel):
    session_id: int
    student: dict
    ta: dict
    started_at: str
    messages: list[TranscriptMessageSchema]


# ----- Teacher -----
class StudentSummary(BaseModel):
    user_id: int
    username: str
    ta_count: int
    domain_ids: list[str]


class StudentTADetail(BaseModel):
    id: int
    domain_id: str
    learned_count: int
    total_kus: int
    mastery_percent: int
    active_misconceptions: list[str]
    test_count: int
    pass_rate: float
    last_active: str | None
    units: dict[str, dict] | None = None  # unit_id -> { status, ... } for KnowledgeGraph


class StudentDetailResponse(BaseModel):
    user: dict  # id, username, role, created_at
    ta_instances: list[StudentTADetail]


class AnalyticsResponse(BaseModel):
    student_count: int
    avg_mastery: float | None = None
    active_misconception_counts: dict[str, int]
    knowledge_coverage: list[dict]
    mastery_trend: list[dict] | None = None  # [{ "date": "YYYY-MM-DD", "avg_mastery": 0.0-1.0 }]
    recent_activity: list[dict] | None = None  # [{ "student": str, "action": str, "result": str | None, "timestamp": str }]
    student_unit_status: list[dict] | None = None  # [{ "user_id": int, "unit_id": str, "status": str }] for heatmap
    sessions_today: int = 0  # Number of teaching sessions today
