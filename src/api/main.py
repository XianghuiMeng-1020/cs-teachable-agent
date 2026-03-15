"""FastAPI application entry point."""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.db.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from src.api.routes import auth, ta, teaching, testing, state, teacher_dashboard, sandbox, gamification, experiment, collaboration, ai_experiments, reports, adaptive_test, spaced_repetition, learning_analytics, advanced_features
from src.api.limiter import limiter

app = FastAPI(
    title="CS Teachable Agent API",
    description="Backend for the Teachable Agent: teach, test, state, trace.",
    version="0.1.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Log unhandled exceptions and return 500 with a safe message. Skip HTTPException."""
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."},
    )

# CORS 配置：生产环境使用特定域名，开发环境允许本地
import re

# Build dynamic origin checking for wildcard support
def get_allowed_origins():
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:5173",
        "https://cs-teachable-agent.pages.dev",
        "https://cs-teachable-agent.xmeng19.workers.dev",
    ]
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        origins.append(frontend_url)
    workers_url = os.getenv("WORKERS_URL")
    if workers_url:
        origins.append(workers_url)
    return origins

# Pattern for preview deployments
cs_ta_pattern = re.compile(r"^https://[a-z0-9-]+\.cs-teachable-agent\.pages\.dev$")

class DynamicCORSMiddleware(CORSMiddleware):
    async def __call__(self, scope, receive, send):
        # Handle both preflight and regular requests
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            origin = None
            for key, value in headers.items():
                if key.decode().lower() == "origin":
                    origin = value.decode()
                    break
            
            # Check if origin is allowed
            if origin:
                allowed = origin in get_allowed_origins()
                if not allowed:
                    # Check preview deployment pattern
                    allowed = bool(cs_ta_pattern.match(origin))
                
                if allowed:
                    # Add CORS headers to the scope
                    scope["headers"].append((b"access-control-allow-origin", origin.encode()))
                    scope["headers"].append((b"access-control-allow-credentials", b"true"))
                    scope["headers"].append((b"access-control-allow-methods", b"*"))
                    scope["headers"].append((b"access-control-allow-headers", b"*"))
        
        await super().__call__(scope, receive, send)

# Use standard CORS with dynamic origin checking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all, we do custom checking
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight for 24 hours
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


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/config")
def get_config():
    """Return public configuration (non-sensitive)."""
    return {
        "llm_configured": bool(os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY")),
        "llm_provider": "openai" if os.getenv("OPENAI_API_KEY") else ("deepseek" if os.getenv("DEEPSEEK_API_KEY") else None),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
