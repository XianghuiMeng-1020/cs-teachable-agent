"""Startup wrapper that catches import/startup errors and prints them clearly."""
import sys
import os
import traceback

os.environ.setdefault("PYTHONPATH", "/app")

try:
    print("=== STARTUP: importing app ===", flush=True)
    from src.api.main import app
    print("=== STARTUP: import OK ===", flush=True)
except Exception:
    traceback.print_exc()
    print("=== STARTUP FAILED: import error ===", flush=True)
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "10000"))
    print(f"=== STARTUP: launching uvicorn on port {port} ===", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
