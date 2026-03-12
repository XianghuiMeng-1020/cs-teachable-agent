# Stage One: Capability Audit

**Document type:** Teacher-facing evaluation — what the prototype implements vs stubs  
**Date:** 2026-03-12  
**Purpose:** Clearly describe what the Stage One prototype can do, what is rule-based, what is LLM-backed, what is optional, and what remains stubbed.

---

## 1. What the Stage One Prototype Currently Implements

The prototype demonstrates **one full Stage One loop**: student teaches → TA knowledge state updates → problem selection constrained by state → TA attempts problem (stub or optional LLM) → code is run and graded → mastery report is produced. All of this runs locally from a single script (`prototype/demo_stage1.py`) with no frontend, backend API, database, or deployment.

| Capability | Implemented | Notes |
|------------|-------------|--------|
| TA starts with zero knowledge | Yes | All knowledge units start as `unknown` in `state_tracker.py`. |
| Knowledge state as single source of truth | Yes | `StateTracker` holds per-unit status; selection and code generation read from it. |
| Structured teaching events | Yes | `teaching_events.py`: topic + `knowledge_units_taught` + note; applied to tracker. |
| Problem selection by learned units | Yes | Only problems whose `knowledge_units_tested` ⊆ learned units are eligible. |
| TA code attempt (constrained by state) | Yes | Stub path always; optional LLM path when `USE_LLM_CODE=1`. |
| Automated grading (run code, compare output) | Yes | `mastery_evaluator.py`: subprocess run, test cases, pass/fail. |
| Mastery report (per problem, per unit, overall) | Yes | Pass/fail → level (failing/proficient); report includes selected problem, required KUs, result. |
| TA learner-style response after teaching | Yes | Stub or optional LLM; constrained by learned units and Stage One scope. |
| Failure path (wrong code → FAIL) | Yes | Scenario C uses `force_fail_problem_ids` to produce wrong stub code; evaluator FAIL. |
| Selection transparency (why problems in/out) | Yes | `get_eligible_problem_ids`, `get_ineligible_reasons` show which problems need which units. |

---

## 2. What Is Rule-Based (No LLM)

- **Knowledge state:** Loaded from `seed/knowledge-units-stage1.json`; all units start `unknown`. Updates are deterministic: `apply_teaching_event` sets listed units to `learned`.
- **Problem selection:** Purely rule-based. A problem is eligible iff every ID in `knowledge_units_tested` is in the set of learned unit IDs. First eligible problem is selected.
- **Stub TA code:** `ta_attempt.py` holds fixed correct/wrong code per `problem_id`. Used when LLM is off, when `force_fail_problem_ids` is set, or when LLM/guard fails.
- **Mastery evaluation:** Run Python in subprocess, compare stdout to expected output per test case; all must match for pass. Mastery summary is computed from that single attempt (proficient if pass, failing if fail).
- **Stub TA conversation:** `ta_conversation.py` has a rule-based fallback that returns short learner-style sentences based on topic/learned units (e.g. “So I can put a value in a variable and then print it with print()?”).

---

## 3. What Is LLM-Backed (Optional)

- **TA learner response (conversation):** If `OPENAI_API_KEY` is set and the `openai` package is available, `get_ta_learner_response` can call the API (e.g. gpt-4o-mini) with a prompt filled from the teaching event and learned units. The prompt restricts the TA to Stage One concepts and learned units only. If the key is missing or the call fails, the **stub response** is used.
- **TA code generation:** If `USE_LLM_CODE=1` (or `true`) **and** `OPENAI_API_KEY` is set, Scenario B calls `ta_code_generation.get_ta_code_attempt(..., use_llm_code=True)`. The LLM generates code from the problem and learned units; the result is checked by an **output guard**. If the guard passes, that code is used; otherwise the **stub path** is used. Scenario C never uses the LLM for code (always stub) so the failure path stays deterministic.

---

## 4. What Is Optional

- **LLM for conversation:** Optional. Without `OPENAI_API_KEY`, the demo uses the rule-based learner response. The prototype runs fully without any API.
- **LLM for code:** Optional and gated by `USE_LLM_CODE=1`. Default is stub-only. When enabled, only Scenario B uses the LLM for the TA attempt; Scenario C always uses the stub for reproducible failure.

---

## 5. What Remains Stubbed or Simplified

- **Teaching input:** No natural-language understanding. Teaching is **structured only**: the scenario passes a teaching event with `topic_taught`, `knowledge_units_taught`, and `note`. There is no parsing of free-form student text into knowledge units.
- **TA code (default path):** The default code path is **stub only**: correct and wrong code are predefined per problem in `ta_attempt.py`. Not all problems in the bank have stubs; missing ones get a placeholder. The LLM path is an optional add-on.
- **TA conversation:** Without an API key, responses are short rule-based phrases. There is no multi-turn chat history or dialogue state.
- **Mastery history:** No persistence. Each scenario starts from a fresh state; there is no accumulation of multiple attempts across problems or sessions.
- **Misconception state:** The design supports optional `active_misconceptions` in prompts, but Scenario C forces failure via `force_fail_problem_ids` and stub wrong code rather than by toggling a misconception state that drives the LLM.
- **Problem bank:** Curated only (`sample-problems-stage1.json`). No automatic problem generation.

---

## 6. How Fallback Works

- **Conversation:** Try LLM if `OPENAI_API_KEY` is set; on missing key, exception, or empty response → use `_fallback_stub_response()`.
- **Code generation:** If `use_llm_code` is False, required KUs are missing, or `force_fail_problem_ids` contains the problem → use `ta_attempt.get_ta_attempt()` (stub). If `use_llm_code` is True: call LLM, then run **output guard** on the returned code; if guard fails or LLM fails → use stub.
- **Output guard:** Rejects code containing forbidden patterns: `def`, `class`, `import`, `open(`, `try:`, `except`, `with ... as`. Rejected code is not used; stub is used instead.

---

## 7. How Knowledge-State Constraints Are Enforced

- **Initial state:** All units from `knowledge-units-stage1.json` are set to `unknown`. Only teaching events update state to `partially_learned` or `learned`.
- **Problem selection:** `select_problem` and `get_eligible_problem_ids` require `knowledge_units_tested ⊆ learned_unit_ids`. No problem requiring an untaught unit can be selected.
- **TA code (stub):** `get_ta_attempt` in `ta_attempt.py` checks `required <= learned_unit_ids`. If any required KU is not learned, it returns a no-attempt placeholder (`# TA has not learned required units; no attempt.\nprint()`).
- **TA code (LLM path):** The code-generation prompt is filled with **only** the current `learned_unit_ids` and instructs the model to use only those concepts. The **output guard** then rejects out-of-scope constructs (functions, classes, etc.). If the model “leaks” such constructs, the guard fails and the stub is used.
- **TA conversation:** The conversation prompt is filled with `learned_unit_ids` (intersected with Stage One scope IDs). The stub response only mentions concepts present in the event or in learned units; it never references untaught Stage One units.

---

## 8. Summary Table

| Component | Implementation | Fallback |
|-----------|----------------|----------|
| Knowledge state | Rule-based | N/A |
| Teaching application | Rule-based | N/A |
| Problem selection | Rule-based | N/A |
| TA learner response | Optional LLM | Stub (rule-based) |
| TA code attempt | Stub always available; optional LLM | Stub if no LLM, guard fail, or force_fail |
| Grading / mastery | Rule-based (run code, compare) | N/A |

The prototype is **self-contained**: it runs with no env vars (stub-only) and optionally uses the LLM for conversation and/or code when keys and flags are set.
