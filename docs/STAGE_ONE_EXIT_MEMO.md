# Stage One: Exit Memo

**Document type:** Concise closure memo for teacher review  
**Date:** 2026-03-12  
**Purpose:** State why Stage One can be considered complete, what evidence supports this, what boundaries remain, and 2–3 recommended next-step options for Stage Two.

---

## Why Stage One Can Be Considered Complete

Stage One (first executable prototype) had three goals (STAGE_ONE_PROPOSAL.md):

1. **Define a TA that starts with no programming knowledge.**  
2. **Design and specify a programming test that examines the TA’s mastery level in programming.**  
3. **Determine the design for the interaction** (explanation, conversation, and generated/curated programming problems) through which the TA learns Introductory Python from the student.

The current prototype **implements** these in a minimal, runnable form:

- The TA starts with all knowledge units `unknown`; only teaching events update state. So the TA has no usable programming knowledge until the student “teaches” (via structured events).
- A **programming test** is implemented: problems are selected from a curated bank by knowledge state; the TA produces code (stub or optional LLM); the code is executed and compared to test cases; pass/fail and a mastery level (e.g. proficient / failing) are reported.
- The **interaction design** is in place: structured teaching → TA learner response (stub or LLM) → problem selection by state → TA attempt → grading → mastery report. Conversation and problems are both present; the loop is closed.

The prototype runs locally with a single command, with or without an LLM. It does not add new scope (no frontend, backend API, database, deployment, or other CS domains). Within these boundaries, Stage One is **functionally complete** for the stated first-step goal.

---

## What Evidence Supports This

- **Capability audit** (STAGE_ONE_CAPABILITY_AUDIT.md): Documents what is implemented (state, selection, grading, report, conversation, code paths), what is rule-based vs optional LLM, and how knowledge-state constraints and fallbacks work. No undocumented behavior is claimed.
- **Scenario evaluation** (STAGE_ONE_SCENARIO_EVALUATION.md): Three scenarios are specified and run:
  - **A:** Only `print_function` learned → no problem eligible → selection constrained by state.
  - **B:** `variable_assignment` + `print_function` taught → problem selected → TA code (stub or LLM) → PASS → proficient.
  - **C:** Same teaching, forced wrong code → FAIL → failing.
- **Reproducibility guide** (STAGE_ONE_REPRODUCIBILITY_GUIDE.md): Instructions to run in stub mode and with optional LLM, env vars, expected outputs, and how to interpret them. The demo is reproducible.
- **Existing docs:** PROPOSAL.md and STAGE_ONE_PROPOSAL.md define scope and goals; STAGE_ONE_REFLECTION.md and prototype README describe seed resources and hardening. The evaluation pack aligns with these and does not expand scope.

Together, this provides **traceable evidence** that the zero-knowledge TA, the programming test for mastery, and the interaction design (explanation + conversation + problems) are implemented and demonstrable.

---

## What Boundaries Still Remain

- **Scope:** Introductory Python only (variables, types, I/O, operators, conditionals, loops, lists). No functions, classes, files, recursion, dictionaries, or other domains (e.g. AI literacy, databases).
- **Teaching:** Structured events only (topic + list of knowledge units + note). No natural-language understanding of free-form student text.
- **TA code:** Default is stub (fixed correct/wrong code per problem). LLM code is optional and used only in Scenario B when enabled; Scenario C is stub-only for deterministic failure.
- **Persistence:** No session or history persistence. Each scenario (and each run) starts from a fresh state.
- **Deployment:** Local script only. No frontend, backend API, database, Docker, or cloud. Single user, single TA, single run.

These boundaries are **intentional** for Stage One and are documented in the capability audit and proposal. They do not invalidate completion; they define what “Stage One complete” means.

---

## Recommended Next-Step Options for Stage Two

**Option 1 — Persist state and broaden the test (recommended first step)**  
Keep the same scope and interaction design. Add: (a) persistence of knowledge state and attempt history across “sessions” or multiple problems per run, and (b) use of the mastery rubric across multiple problems per unit (e.g. pass rate over several problems) so that per-unit and overall levels (failing / developing / proficient) are computed as in the rubric. This strengthens the “examine mastery” goal without adding new domains or UI.

**Option 2 — Add a minimal teacher-facing UI**  
Expose the same loop (teach → response → select problem → attempt → report) through a simple UI (e.g. Streamlit or a single-page app): form or buttons for teaching events, display of TA response and selected problem, run attempt and show code + result + mastery report. No new backend or database required for a first cut; can still use file-based or in-memory state. This makes the prototype directly usable by the teacher for a live demo or small pilot.

**Option 3 — Teach from natural language (pilot)**  
Keep the current flow but add a **pilot** path: accept free-form student text (e.g. one message per turn), call an LLM to map that text to knowledge unit updates, then apply those updates to the state and continue as now. This validates “learning from human student interaction” in a more natural form before committing to a full NL teaching pipeline. Stub/structured path remains the default for reproducibility.

---

## Summary

Stage One is **complete** for the stated first-step goal: zero-knowledge TA, programming test that examines mastery, and interaction design with explanation, conversation, and curated problems. The evidence is documented in the capability audit, scenario evaluation, and reproducibility guide. Boundaries (scope, stubs, no persistence, no deployment) are explicit. The single most recommended next step is **Option 1**: persist state and aggregate mastery over multiple problems per unit so the test more fully “examines” the TA’s mastery as in the rubric, then consider Option 2 (minimal UI) or Option 3 (NL teaching pilot) as follow-ons.
