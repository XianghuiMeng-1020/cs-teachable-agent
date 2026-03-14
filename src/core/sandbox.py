"""Safe execution of TA-generated Python code (timeout, no network/files)."""

import subprocess
import tempfile
from pathlib import Path


def run_python_sandbox(
    code: str,
    stdin_str: str = "",
    timeout_seconds: float = 2.0,
) -> tuple[str, str, int]:
    """
    Execute Python code with given stdin. Returns (stdout, stderr, returncode).
    Uses subprocess with timeout; not a full sandbox (no network isolation).
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        path = Path(f.name)
    try:
        result = subprocess.run(
            ["python", str(path)],
            input=stdin_str,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=path.parent,
        )
        return (result.stdout or "", result.stderr or "", result.returncode)
    except subprocess.TimeoutExpired:
        return ("", "timeout", -1)
    finally:
        path.unlink(missing_ok=True)
