"""FastAPI application entry point."""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from src.db.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from src.api.routes import auth, ta, teaching, testing, state, teacher_dashboard, sandbox, gamification, experiment, collaboration, ai_experiments, reports, adaptive_test, spaced_repetition, learning_analytics, advanced_features, assessment, admin_config
from src.api.limiter import limiter

_frontend_url = os.getenv("FRONTEND_URL", "*")
_workers_url = os.getenv("WORKERS_URL", "")

def _allowed_origin(request_origin: str | None) -> str:
    if _frontend_url == "*":
        return "*"
    allowed = [o.strip() for o in _frontend_url.split(",") if o.strip()]
    if _workers_url:
        allowed.extend(o.strip() for o in _workers_url.split(",") if o.strip())
    allowed += ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]
    if request_origin and request_origin in allowed:
        return request_origin
    return allowed[0] if allowed else "*"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "86400",
}

app = FastAPI(
    title="ARTS-CS API",
    description="AI Resistant Teaching System for Computer Science: teach, test, state, trace, misconception lifecycle.",
    version="2.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class CORSEverythingMiddleware(BaseHTTPMiddleware):
    """Ensure every single response has CORS headers, including preflight."""

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return Response(
                status_code=200,
                headers=CORS_HEADERS,
            )
        response = await call_next(request)
        for k, v in CORS_HEADERS.items():
            response.headers[k] = v
        return response


app.add_middleware(CORSEverythingMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Log unhandled exceptions and return 500 with a safe message. Skip HTTPException."""
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."},
        headers=CORS_HEADERS,
    )

@app.on_event("startup")
def startup():
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Database init failed: %s", e)
    _seed_demo_accounts()
    sk = os.getenv("SECRET_KEY", "")
    if os.getenv("ENVIRONMENT") == "production" and (not sk or sk == "dev-secret-change-in-production"):
        logger.error("SECRET_KEY not configured properly for production")
    logger.info("Startup complete. PORT=%s, ENV=%s", os.getenv("PORT"), os.getenv("ENVIRONMENT"))


def _seed_demo_accounts():
    """Create demo_student and demo_teacher if they don't exist yet."""
    try:
        from src.db.database import SessionLocal
        from src.db.models import User
        from src.api.deps import get_password_hash

        db = SessionLocal()
        try:
            for uname, role in [("demo_student", "student"), ("demo_teacher", "teacher")]:
                if not db.query(User).filter(User.username == uname).first():
                    db.add(User(username=uname, password_hash=get_password_hash("demo123"), role=role))
                    logger.info("Seeded demo account: %s", uname)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        logger.warning("Demo account seeding skipped: %s", e)


app.include_router(auth.router)
app.include_router(ta.router)
app.include_router(teaching.router)
app.include_router(testing.router)
app.include_router(state.router)
app.include_router(teacher_dashboard.router)
app.include_router(sandbox.router)
app.include_router(gamification.router)
app.include_router(experiment.router)
app.include_router(collaboration.router)
app.include_router(ai_experiments.router)
app.include_router(reports.router)
app.include_router(adaptive_test.router)
app.include_router(spaced_repetition.router)
app.include_router(learning_analytics.router)
app.include_router(advanced_features.router)
app.include_router(assessment.router)
app.include_router(admin_config.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "2.0.0", "cors": "CORSEverythingMiddleware"}


@app.get("/api/config")
def get_config():
    """Return public configuration (non-sensitive)."""
    providers = []
    if os.getenv("DEEPSEEK_API_KEY"):
        providers.append("deepseek")
    if os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    if os.getenv("QWEN_API_KEY"):
        providers.append("qwen")
    return {
        "llm_configured": len(providers) > 0,
        "llm_providers": providers,
        "llm_primary": providers[0] if providers else None,
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
