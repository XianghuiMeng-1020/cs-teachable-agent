# Deployment

This document covers (1) Streamlit Community Cloud for the teacher demo and (2) production-style deployment of the full React + FastAPI stack.

> 🚀 **推荐部署方案**: [DEPLOY_CF_RAILWAY.md](DEPLOY_CF_RAILWAY.md) — Cloudflare Pages (前端) + Railway (后端)，免费且易于维护。

---

## 1. Streamlit Community Cloud (teacher demo)

One-time setup to get a **shareable live link** for the teacher-facing Streamlit demo.

## Prerequisites

- The repo is on **GitHub** (public or private). If it is not, push it first:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```
- A **GitHub account** (for signing in to Streamlit Community Cloud).

## Single minimal action to deploy

1. Open **[share.streamlit.io](https://share.streamlit.io)** in your browser.
2. Click **"Sign in with GitHub"** and authorize if prompted.
3. Click **"New app"**.
4. Fill in:
   - **Repository:** `YOUR_USERNAME/YOUR_REPO` (e.g. `jane/cs-teachable-agent`)
   - **Branch:** `main` (or your default branch)
   - **Main file path:** `streamlit_app.py`
5. Click **"Deploy!"**.

After a few minutes, your app will be live at:

**`https://YOUR_APP_NAME.streamlit.app`**

(Streamlit will show the exact URL in the app dashboard; you can rename the app there if you like.)

## No API key required for stub mode

The demo runs **fully in stub mode** without any environment variables. The professor can use all three scenarios (A, B, C) without setting `OPENAI_API_KEY`. Optional LLM code for Scenario B is available only if you add `OPENAI_API_KEY` in the app’s **Secrets** in the Streamlit Cloud dashboard (Settings → Secrets).

## Redeploying (Streamlit)

Push changes to the same branch; Streamlit Community Cloud will redeploy automatically (or use “Reboot” in the app menu).

---

## 2. Production: React frontend + FastAPI backend

For **SkillSight-style** or **tutor-dialogue-style** hosting (full student/teacher UI, transcripts, analytics), deploy the React app and API together.

**Option A — Same host, reverse proxy:** Build the frontend (`cd frontend && npm ci && npm run build`). Serve `frontend/dist` for `/` (e.g. nginx with `try_files $uri $uri/ /index.html`) and proxy `/api` to the FastAPI backend. Run the backend with `uvicorn src.api.main:app --host 0.0.0.0 --port 8000`.

**Option B — Vite preview:** Run the backend on port 8000 and `npm run preview` in `frontend`; use a reverse proxy so `/api` forwards to the backend.

Set `OPENAI_API_KEY` or `DEEPSEEK_API_KEY` for LLM; use PostgreSQL and `DATABASE_URL` for production database.
