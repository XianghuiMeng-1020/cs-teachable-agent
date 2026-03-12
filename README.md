# Teachable Agent for CS — Stage One

Research prototype: a **Teachable Agent (TA)** that starts with no programming knowledge and learns Introductory Python from a human student. The student teaches; the TA is tested with programming problems; mastery is reported.

## Run the teacher-facing demo (Streamlit)

From the repo root:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (e.g. http://localhost:8501). The demo runs **fully in stub mode** without any API keys. Optional LLM for conversation and for Scenario B code is available if `OPENAI_API_KEY` is set.

## Get a shareable live link

See **[DEPLOY.md](DEPLOY.md)** for the one-time steps to deploy on Streamlit Community Cloud and get a link for professor review.

## Repo structure

- **PROPOSAL.md**, **STAGE_ONE_PROPOSAL.md** — Project and Stage One scope
- **streamlit_app.py** — Teacher-facing Streamlit demo (this stage’s UI)
- **prototype/** — Stage One logic (state, selection, TA code, grading, scenarios)
- **seed/** — Knowledge units, sample problems (Stage One scope)
- **docs/** — Interaction protocol, mastery rubric, evaluation pack

## Stage One scope

Introductory Python only: variables, types, I/O, operators, conditionals, loops, lists. No functions, classes, files, recursion, dictionaries, or external libraries as learning content.
