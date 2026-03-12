# Stage One: First Executable Prototype (Hardened)

Minimal local prototype that demonstrates **one full Stage One loop** and, after the **hardening pass**, multiple teaching/testing scenarios plus a failure path. The knowledge state is the only source of truth; the TA never uses concepts outside the current learned state.

**Source of truth:** Stage One seed files in `../seed/` and docs in `../docs/`.

---

## What the hardening pass added

- **Multiple demo scenarios:** Three scenarios (A, B, C) run in one script: minimal learned state, success path, and failure path.
- **Explicit teaching input:** Structured teaching events (`topic_taught`, `knowledge_units_taught`, optional `note`) so the teaching step is clear and inspectable.
- **Stronger TA attempt control:** Success only when all required KUs are learned; failure can be simulated via `force_fail_problem_ids` (misconception); TA never uses concepts outside state.
- **Richer mastery reporting:** Each scenario report includes selected problem, required KUs, learned KUs at attempt time, pass/fail, per-problem interpretation, and overall summary.
- **Selection transparency:** Scenario A shows eligible vs ineligible problems and *why* (missing units), so it is clear that knowledge state controls which problems can be selected.

## What the conversation-only LLM pass added

- **Controlled conversation layer:** After each teaching event, the TA can produce a short **learner-style response** (restate, ask a question, express confusion). This is **conversation only**; TA code generation for problems remains rule-based stubs.
- **Knowledge-state control:** The reply is constrained to the current learned units and Stage One scope; the TA does not teach, give hints, or mention concepts it has not learned.
- **Optional LLM + fallback:** If `OPENAI_API_KEY` is set and the `openai` package is installed, the module uses a small prompt to request a 1–2 sentence learner reply. Otherwise a **stub fallback** returns a short rule-based response so the demo runs without any API.
- **Prompt template:** `prompts/ta_learner_conversation_prompt.md` defines the learner persona and constraints so the architecture is ready for controlled LLM use.

## What the code-generation LLM pass added

- **Parallel code path:** A separate, controlled **LLM-backed code-generation** path exists alongside the existing stub path. The stub path in `ta_attempt.py` is **never removed**; it is used as fallback whenever the LLM path is off, required KUs are missing, a forced-fail is requested, or the LLM/guard fails.
- **Controlled code generation:** `ta_code_generation.get_ta_code_attempt()` takes the problem, learned units, optional misconceptions, and `use_llm_code`. It only calls the LLM when `use_llm_code` is True; generated code is checked by an **output guard** that rejects forbidden constructs (e.g. `def`, `class`, `import`, `open(`, `try:`, `except`). If the guard fails or the LLM is unavailable, the stub path is used.
- **Scenario B optional LLM:** When the env var `USE_LLM_CODE=1` (or `true`) is set, Scenario B uses the LLM code path for the TA attempt; otherwise it uses the stub. Scenario C always uses the stub so the failure path stays deterministic.
- **Misconception-aware:** The code-generation prompt accepts optional active misconceptions so the model can produce plausible beginner-style errors when desired (used in the prompt; fallback behavior still uses stub wrong code for Scenario C).

---

## Files

| File | Purpose |
|------|--------|
| `state_tracker.py` | Loads KUs from `knowledge-units-stage1.json`; initializes all units to `unknown`; exposes `update_after_teaching(unit_ids)` and `get_learned_units()`. State is the only source of truth. |
| `problem_selector.py` | Loads problems; `select_problem()` picks one whose required KUs are all learned; `get_eligible_problem_ids()` and `get_ineligible_reasons()` show what can/cannot be selected and why. |
| `teaching_events.py` | Structured teaching events: `make_teaching_event(topic, knowledge_units_taught, note)` and `apply_teaching_event(tracker, event)`. |
| `ta_conversation.py` | **Conversation only:** Generates a short TA learner-style response after a teaching event. Uses LLM when `OPENAI_API_KEY` is set; otherwise stub. Constrained by learned units and Stage One scope. |
| `prompts/ta_learner_conversation_prompt.md` | Prompt template for the TA learner response. |
| `ta_code_generation.py` | **Code generation:** Optional LLM path for TA code attempt. Uses `ta_attempt.get_ta_attempt` as fallback. Enforces knowledge-state and output guard; supports `USE_LLM_CODE` for Scenario B. |
| `prompts/ta_code_generation_prompt.md` | Prompt template for TA code: problem, learned units only, forbidden constructs, optional misconceptions. |
| `ta_attempt.py` | **Stub code path (unchanged):** Correct/wrong code per problem_id; `force_fail_problem_ids` for failure demo. Used whenever LLM code path is not used or falls back. |
| `mastery_evaluator.py` | Runs TA code, compares to test cases, pass/fail. `build_mastery_report()` and `format_mastery_report_line()`. |
| `demo_scenarios.py` | Runs A, B, C; uses `get_ta_learner_response()` and `get_ta_code_attempt()` (with optional `USE_LLM_CODE` for B). |
| `demo_stage1.py` | Runs all three scenarios in sequence. |
| `README_stage1_prototype.md` | This file. |

---

## How to run the demo

From the **repository root** (the folder that contains `prototype/` and `seed/`):

```bash
python prototype/demo_stage1.py
```

Or from inside `prototype/`:

```bash
cd prototype
python demo_stage1.py
```

---

## Scenarios now covered

| Scenario | Goal | What happens |
|----------|------|--------------|
| **A: Minimal learned state** | Verify that only problems requiring learned units can be selected; confirm problems requiring untaught concepts are not selected. | Teach only `print_function`. Eligible problem list is empty (no problem in the bank uses only print_function). Ineligible problems are listed with missing units. No problem is selected. |
| **B: Success path** | Teach → select matching problem → TA succeeds → mastery PASS. | Teach `variable_assignment` + `print_function`. Problem `prob_var_001` is selected. TA produces correct code; evaluator PASS; mastery report shows proficient. |
| **C: Failure path** | Same teaching as B, but TA produces wrong code → evaluator FAIL → mastery reflects failure. | Same teaching as B. Problem `prob_var_001` selected; TA code is forced to a wrong version (e.g. prints 21 instead of 20). Evaluator FAIL; mastery report shows failing. |

---

## What remains intentionally simplified (stubbed)

- **Teaching:** Structured events only (topic + unit IDs + note). No natural-language understanding of free-form student text.
- **TA code generation:** Stub path remains the default; LLM code path is **optional** via `USE_LLM_CODE=1`. When the LLM is used, the output guard is minimal (forbidden patterns); no full AST or semantic check. Misconception for Scenario C is still simulated by stub wrong code so the failure path is deterministic.
- **TA conversation:** Optional LLM when `OPENAI_API_KEY` is set; otherwise stub. Single reply per teaching event; no multi-turn chat.
- **Mastery history:** No persistence; each scenario starts from a fresh state.
- **Problem bank:** Curated only; no automatic problem generation.

The prototype remains **intentionally minimal**: local, no frontend/API/database/deployment/Docker/cloud, Stage One scope only.

---

## Running with or without an LLM

- **Default (no env vars):** Conversation and code generation both use stubs. The demo runs with no external services.
- **Conversation only:** Set `OPENAI_API_KEY` and install `openai`. The TA learner response may come from the LLM; code attempts still use the stub unless `USE_LLM_CODE` is set.
- **Code generation only:** Set `OPENAI_API_KEY` and `USE_LLM_CODE=1` (or `true`). Scenario B will use the LLM to generate the TA code attempt; if the API fails or the output guard rejects the code, the stub is used automatically. Scenario C always uses the stub.
- **Both:** Set `OPENAI_API_KEY` and `USE_LLM_CODE=1` to use the LLM for both conversation and (in B) code.

---

## Next step after the code-generation pass

1. **Optional:** Run with `USE_LLM_CODE=1` and inspect that generated code passes the guard and stays within Stage One; if the model sometimes emits forbidden constructs, the guard will fall back to stub.
2. **Later:** Persist attempt history and aggregate mastery across multiple problems per unit (per rubric); keep scope at Stage One.
