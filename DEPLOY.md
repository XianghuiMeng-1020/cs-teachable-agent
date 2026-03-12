# Deploy Stage One Streamlit Demo (Streamlit Community Cloud)

One-time setup to get a **shareable live link** for professor review.

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

## Redeploying

Push changes to the same branch; Streamlit Community Cloud will redeploy automatically (or use “Reboot” in the app menu).
