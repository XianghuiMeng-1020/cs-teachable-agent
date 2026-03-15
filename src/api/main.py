"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import init_db
from src.api.routes import auth, ta, teaching, testing, state, teacher_dashboard

app = FastAPI(
    title="CS Teachable Agent API",
    description="Backend for the Teachable Agent: teach, test, state, trace.",
    version="0.1.0",
)

# CORS 配置：生产环境使用特定域名，开发环境允许本地
import os

allowed_origins = [
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
    allowed_origins.append(frontend_url)

workers_url = os.getenv("WORKERS_URL")
if workers_url:
    allowed_origins.append(workers_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
