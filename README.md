# CS Teachable Agent

Research prototype: a **Teachable Agent (TA)** that starts with no programming knowledge and learns Introductory Python from a human student. The student teaches; the TA is tested with programming problems; mastery is reported.

## Recommended: Full stack (FastAPI + React)

**Main way to run** the app with production-grade UI (student/teacher dashboards, teach & test flow, transcripts, analytics).

1. **Backend** (API):
   ```bash
   uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
   ```
   API docs: http://127.0.0.1:8000/docs

2. **Frontend** (React + Vite):
   ```bash
   cd frontend && npm install && npm run dev
   ```
   App: http://localhost:3000 (Vite proxies `/api` to the backend).

3. **Optional — LLM**: Copy `.env.example` to `.env` and set `OPENAI_API_KEY` or `DEEPSEEK_API_KEY` for teaching interpretation, TA dialogue, and code generation. Without keys, the system uses keyword heuristics and stub code (tests still run).

4. **First use**: Open the app → Sign up (or Sign in) → Create a TA (or use the default) → Teach and Test from the sidebar.

- **Docker**: `docker-compose up backend` runs the API only; run the frontend locally as above.
- **Demo script**: [docs/demo-script.md](docs/demo-script.md)

## Teacher-facing demo (Streamlit, optional)

From the repo root:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (e.g. http://localhost:8501). The demo runs **fully in stub mode** without any API keys. Optional LLM for conversation and for Scenario B code is available if `OPENAI_API_KEY` is set. Use this for a quick teacher-only demo; for full student/teacher and transcripts, use the FastAPI + React stack above.

## Deployment and shareable links

### 推荐方案（免费托管）
**[DEPLOY_CF_RAILWAY.md](DEPLOY_CF_RAILWAY.md)** — Cloudflare Pages (前端) + Railway (后端)
- 前端：全球 CDN，自动 HTTPS
- 后端：Python/FastAPI 原生支持
- 成本：免费额度内完全够用

### 其他方案
See **[DEPLOY.md](DEPLOY.md)** for:
- **Streamlit Community Cloud** — one-time steps for a shareable teacher-demo link.
- **Self-hosted** — nginx 反向代理部署方案。

## Repo structure

- **frontend/** — React + TypeScript + Vite app (student/teacher UI, transcripts, analytics)
- **src/api/** — FastAPI backend (auth, TA CRUD, teach/test, state, teacher endpoints)
- **PROPOSAL.md**, **STAGE_ONE_PROPOSAL.md** — Project and Stage One scope
- **streamlit_app.py** — Teacher-facing Streamlit demo (optional)
- **prototype/** — Stage One logic (state, selection, TA code, grading, scenarios)
- **seed/** — Knowledge units, sample problems (Stage One scope)
- **docs/** — Interaction protocol, mastery rubric, evaluation pack

## Stage One scope

Introductory Python only: variables, types, I/O, operators, conditionals, loops, lists. No functions, classes, files, recursion, dictionaries, or external libraries as learning content.
