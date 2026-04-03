"""Startup wrapper with diagnostics for Render deployment."""
import sys
import os
import traceback

os.environ.setdefault("PYTHONPATH", "/app")

print("=== ENV CHECK ===", flush=True)
for k in ["PORT", "ENVIRONMENT", "SECRET_KEY", "DATABASE_URL", "PYTHONPATH", "DEEPSEEK_API_KEY", "OPENAI_API_KEY"]:
    v = os.environ.get(k, "")
    print(f"  {k} = {'SET (' + str(len(v)) + ' chars)' if v else 'NOT SET'}", flush=True)

print("=== IMPORT CHECK ===", flush=True)
try:
    import fastapi; print(f"  fastapi {fastapi.__version__}", flush=True)
    import uvicorn; print(f"  uvicorn OK", flush=True)
    import sqlalchemy; print(f"  sqlalchemy {sqlalchemy.__version__}", flush=True)
    import openai; print(f"  openai {openai.__version__}", flush=True)
    import slowapi; print(f"  slowapi OK", flush=True)
    from jose import jwt; print(f"  python-jose OK", flush=True)
    import httpx; print(f"  httpx OK", flush=True)
except Exception:
    traceback.print_exc()
    print("=== IMPORT FAILED ===", flush=True)
    sys.exit(1)

print("=== APP IMPORT ===", flush=True)
try:
    from src.api.main import app
    print("=== APP IMPORT OK ===", flush=True)
except Exception:
    traceback.print_exc()
    print("=== APP IMPORT FAILED ===", flush=True)
    sys.exit(1)

port = int(os.environ.get("PORT", "10000"))
print(f"=== STARTING UVICORN on :{port} ===", flush=True)
uvicorn.run(app, host="0.0.0.0", port=port)
