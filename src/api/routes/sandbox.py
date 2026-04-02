"""Sandbox: run Python code (for Live Code Editor). Rate-limited and auth required."""

from fastapi import APIRouter, Request

from pydantic import BaseModel

from src.api.deps import CurrentUser, DbSession
from src.api.limiter import limiter
from src.core.evaluator import run_python_code

router = APIRouter(prefix="/api/sandbox", tags=["sandbox"])


class RunPythonRequest(BaseModel):
    code: str = ""
    stdin: str = ""


@router.post("/run-python")
@limiter.limit("30/minute")
def run_python(request: Request, body: RunPythonRequest, current_user: CurrentUser):
    """Run Python code with optional stdin. Returns stdout, stderr, returncode."""
    code = (body.code or "").strip()
    stdin_str = body.stdin or ""
    if not code:
        return {"stdout": "", "stderr": "No code provided", "returncode": -1}
    if len(code) > 20_000:
        return {"stdout": "", "stderr": "Code too long", "returncode": -1}
    stdout, stderr, returncode = run_python_code(code, stdin_str, timeout_seconds=5.0)
    return {"stdout": stdout, "stderr": stderr, "returncode": returncode}


@router.post("/run-problem-code")
def run_problem_code(
    body: RunPythonRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    """Run problem code and return output for preview. Limited to 5 second timeout."""
    code = (body.code or "").strip()
    if not code:
        return {"stdout": "", "stderr": "No code provided", "returncode": -1}
    if len(code) > 20_000:
        return {"stdout": "", "stderr": "Code too long", "returncode": -1}
    stdout, stderr, returncode = run_python_code(
        code, body.stdin or "", timeout_seconds=5.0,
    )
    return {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode,
    }
