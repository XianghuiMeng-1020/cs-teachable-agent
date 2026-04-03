"""Startup wrapper - if full app fails, falls back to minimal health-only server."""
import sys
import os
import traceback
import uvicorn

port = int(os.environ.get("PORT", "10000"))

print("=== Attempting full app import ===", flush=True)
try:
    from src.api.main import app
    print("=== Full app import OK, starting ===", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
except Exception:
    traceback.print_exc()
    print("=== Full app FAILED, starting diagnostic fallback ===", flush=True)

    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    fallback = FastAPI()
    error_info = traceback.format_exc()

    @fallback.get("/api/health")
    def health():
        return {"status": "degraded", "error": "full app failed to import", "details": error_info[:500]}

    @fallback.get("/api/debug")
    def debug():
        return PlainTextResponse(error_info)

    uvicorn.run(fallback, host="0.0.0.0", port=port)
