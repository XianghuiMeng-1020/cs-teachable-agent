"""Minimal health test to verify Render can start uvicorn."""
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "test", "mode": "minimal"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"Starting minimal server on port {port}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
