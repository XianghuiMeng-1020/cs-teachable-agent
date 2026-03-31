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
    title="CS Teachable Agent API",
    description="Backend for the Teachable Agent: teach, test, state, trace.",
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
    init_db()
    if os.getenv("ENVIRONMENT") == "production":
        sk = os.getenv("SECRET_KEY", "")
        if not sk or sk == "dev-secret-change-in-production":
            raise RuntimeError("SECRET_KEY must be set in production (and must not be the default dev value)")


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
    return {
        "llm_configured": bool(os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")),
        "llm_provider": "openai" if os.getenv("OPENAI_API_KEY") else ("deepseek" if os.getenv("DEEPSEEK_API_KEY") else None),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
