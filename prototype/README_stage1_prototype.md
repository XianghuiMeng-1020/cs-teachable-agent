# Stage One: First Executable Prototype (Hardened)

Minimal local prototype that demonstrates **one full Stage One loop** and, after the **hardening pass**, multiple teaching/testing scenarios plus a failure path. The knowledge state is the only source of truth; the TA never uses concepts outside the current learned state.

**Source of truth:** Stage One seed files in `../seed/` and docs in `../docs/`.

---

## What the hardening pass added

- **Multiple demo scenarios:** Three scenarios (A, B, C) run in one script: minimal learned state, success path, and failure path.
- **Explicit teaching input:** Structured teaching events (`topic_taught`, `knowledge_units_taught`, optional `note`) so the teaching step is clear and inspectable.
- **Stronger TA attempt control:** Success only when all required KUs are learned; failure can be state-driven via **misconception activation** (Stage C) or, as fallback, `force_fail_problem_ids`; TA never uses concepts outside state.
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

## Stage C: Misconception engine integration

- **State-driven misconception activation:** A unit can have one or more active misconceptions in `active_misconceptions`. The state tracker exposes `activate_misconception(unit_id, misconception_id, trigger, …)` and `get_active_misconception_ids(unit_ids)` so dialogue and attempt logic read from state.
- **Scenario C is misconception-driven:** After teaching (same as B), the demo activates a misconception for `variable_assignment` (e.g. `variable_print_off`). The TA attempt layer sees active misconceptions for the problem’s tested units and returns the corresponding wrong code (rule-based). No `force_fail_problem_ids` on the main path; it remains as a fallback.
- **Trace:** `misconception_activation` events are recorded (event_id, timestamp, domain, unit_id, misconception_id, trigger, trigger_reference, state_before, state_after).
- **Dialogue:** When the state has active misconceptions, the learner response can optionally reflect slight confusion (e.g. stub: “I might still mix up what to print sometimes”).

## Stage D: Unlearning / Relearning state transitions and evidence flow

- **Correction detection:** A structured correction event (`correction_events.make_correction_event`) identifies unit, misconception, trigger (e.g. `explicit_correction_event`), and optional teaching_event_id. The system records which unit is corrected and which misconception; state is updated accordingly.
- **Unlearning transition:** When correction is applied, the misconception is removed from `active_misconceptions`, status is set to `corrected` (not immediately back to `learned`), and one entry is written to `correction_evidence` (misconception_id, corrected_at, trigger, state_before, state_after). Trace: `correction_event` with event_id, timestamp, domain, unit_id, misconception_id, trigger, state_before, state_after.
- **Relearning evidence:** Post-correction teaching or a successful task can be recorded as relearning_evidence (type: `teaching` or `successful_task`). The state tracker exposes `append_relearning_evidence` and `try_relearning_transition` (policy: at least one correction + at least one relearning event → status returns to `learned`). Trace: `relearning_event` with event_id, unit_id, type, state_after, reference_id.
- **Relearning transition:** When the policy is satisfied, the unit moves from `corrected` to `learned`; confidence can be restored. Mastery report can show unit status (corrected vs learned) via optional `unit_status_for_display` in `build_mastery_report`.
- **Scenario D:** Full path: teach → activate misconception → first attempt (FAIL) → explicit correction (unlearning) → follow-up teaching (relearning evidence) → status → learned → second attempt (PASS). The demo shows failed due to misconception, corrected, state after relearning, and recovered.

## Stage E: Mastery aggregation and persistence within the run

- **Mastery results in state:** After each evaluated attempt, `record_attempt_to_state` writes to each affected unit: `testing_evidence` (existing) and a per-attempt `mastery_history` entry with attempt_id, problem_id, pass_fail, mastery_level, misconception_active_during_attempt, and period (before_misconception | during_misconception | after_correction). So mastery is no longer only a one-off summary; per-unit mastery history exists in state.
- **Multi-attempt aggregation:** `aggregate_mastery(history_entries, include_during_misconception=True)` and `get_aggregated_mastery_for_unit(tracker, unit_id, …)` return attempt_count, pass_count, pass_rate, and aggregated_level (failing / developing / proficient per rubric). Optionally `include_during_misconception=False` so “current” mastery can reflect only post-correction attempts.
- **Misconception-period attempts:** Attempts are tagged with period and misconception_active_during_attempt. Aggregation can include or exclude them; count_during_misconception and count_after_correction are reported so the system can distinguish before/during/after correction.
- **Scenario D mastery trajectory:** Scenario D output now includes a mastery trajectory for the corrected unit (e.g. variable_assignment): before first attempt, after failure, after correction, after relearning success, with aggregated levels and (optionally) aggregated excluding during-misconception attempts.

## Stage F: Shared-core refactor (single-cycle orchestration and engine boundaries)

- **Single shared-cycle path:** All scenarios now go through one orchestration layer (`run_cycle.py`). The cycle order is: teaching event → state update → (optional misconception activation) → learner dialogue → task selection → (optional) TA attempt → evaluation → mastery/state updates → trace at each step. This matches SHARED_CORE_ARCHITECTURE §14.
- **Interaction Engine:** `interaction_engine.py` is a thin facade that re-exports `run_teaching_and_test`, `run_correction`, `run_relearning_step`, and `run_test_only`. The actual logic lives in `run_cycle`.
- **Engine boundaries:** Responsibilities are clearly separated: **state** (state_tracker), **teaching/events** (teaching_events, apply via run_cycle), **misconception lifecycle** (misconception_engine, correction_events), **dialogue** (ta_conversation), **task selection** (problem_selector), **attempt** (ta_code_generation, ta_attempt), **evaluation/mastery** (mastery_evaluator), **trace** (trace_history). The cycle calls these in order; it does not implement state or misconception logic itself.
- **Scenario coupling reduced:** Scenarios only configure inputs (teaching event, optional `activate_misconception`, run_attempt, use_llm_code) and call `run_teaching_and_test` (and for D: `run_correction`, `run_relearning_step`, `run_test_only`). They no longer manually wire components or call trace/state/attempt in sequence.
- **Python as content:** Domain content (knowledge units, problems, misconception ids) remains in seed data and scenario config; the shared cycle is domain-agnostic and takes tracker + problems + event + options.

---

## Files

| File | Purpose |
|------|--------|
| `state_tracker.py` | Loads KUs; full per-unit schema (evidence, `active_misconceptions`, `correction_evidence`, `relearning_evidence`, `mastery_history`). Stage D: `apply_unlearning`, `append_relearning_evidence`, `try_relearning_transition`, `STATUS_CORRECTED`. Stage E: `append_mastery_history_entry` (per-attempt: attempt_id, problem_id, pass_fail, mastery_level, period), `get_mastery_history`. State is the only source of truth. |
| `problem_selector.py` | Loads problems; `select_problem()` picks one whose required KUs are all learned; `get_eligible_problem_ids()` and `get_ineligible_reasons()` show what can/cannot be selected and why. |
| `teaching_events.py` | Structured teaching events: `make_teaching_event(topic, knowledge_units_taught, note)` and `apply_teaching_event(tracker, event)`. |
| `ta_conversation.py` | **Conversation only:** Generates a short TA learner-style response after a teaching event. Uses LLM when `OPENAI_API_KEY` is set; otherwise stub. Constrained by learned units and Stage One scope. |
| `prompts/ta_learner_conversation_prompt.md` | Prompt template for the TA learner response. |
| `ta_code_generation.py` | **Code generation:** Optional LLM path for TA code attempt. Uses `ta_attempt.get_ta_attempt` as fallback. Enforces knowledge-state and output guard; supports `USE_LLM_CODE` for Scenario B. |
| `prompts/ta_code_generation_prompt.md` | Prompt template for TA code: problem, learned units only, forbidden constructs, optional misconceptions. |
| `ta_attempt.py` | **Stub code path:** Correct/wrong code per problem_id. When `active_misconception_ids` is set (from state), returns wrong code for that problem if available (Stage C). `force_fail_problem_ids` kept as fallback. |
| `mastery_evaluator.py` | Runs TA code, pass/fail; `build_mastery_report`, `format_mastery_report_line`. Stage E: `record_attempt_to_state` (writes testing_evidence + mastery_history per unit), `aggregate_mastery`, `get_aggregated_mastery_for_unit` (attempt_count, pass_rate, aggregated_level; optional exclude during-misconception). |
| `run_cycle.py` | **Shared-cycle orchestration (Stage F):** `run_teaching_and_test(tracker, problems, teaching_event, …)` runs one full cycle (teach → state → dialogue → task selection → optional attempt → evaluation → trace). Also `run_correction`, `run_relearning_step`, `run_test_only` for Scenario D. Single entry point; no scenario-specific branching inside. |
| `interaction_engine.py` | Thin facade over run_cycle; re-exports cycle functions per SHARED_CORE_ARCHITECTURE (Interaction Engine). |
| `demo_scenarios.py` | Runs A, B, C, D by calling run_cycle with scenario-specific inputs; builds return dicts and mastery_trajectory for D. No manual engine wiring. |
| `trace_history.py` | Trace/history layer: teaching_event, knowledge_state_update, learner_dialogue, task_selection, ta_attempt, evaluation_result, mastery_update, misconception_activation, correction_event, relearning_event (Stage D). |
| `misconception_engine.py` | Stage C: `activate_misconception_for_unit`. Stage D: `apply_correction`, `add_relearning_evidence_from_teaching`, `add_relearning_evidence_from_successful_task`; unlearning and relearning transitions + trace. |
| `correction_events.py` | Stage D: `make_correction_event(unit_id, misconception_id, trigger, …)` for structured correction input. |
| `demo_stage1.py` | Runs scenarios A, B, C, and D in sequence. |
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
| **C: Failure path** | Same teaching as B, but TA has an **active misconception** → wrong code → evaluator FAIL. | Same teaching as B. A misconception is **activated** for `variable_assignment` (state-driven). Problem `prob_var_001` selected; TA produces wrong code (e.g. prints 21 instead of 20) from state. Evaluator FAIL; mastery report shows failing. |
| **D: Correction and relearning** | Full misconception lifecycle: fail → correct → relearn → recovery. | Same as C up to first attempt (FAIL). Then explicit correction (unlearning); follow-up teaching (relearning); second attempt PASS. Report shows unit status and recovered. Stage E: mastery trajectory (before first attempt, after failure, after correction, after relearning success) and aggregated mastery (all attempts vs excluding during-misconception). |

---

## What remains intentionally simplified (stubbed)

- **Teaching:** Structured events only (topic + unit IDs + note). No natural-language understanding of free-form student text.
- **TA code generation:** Stub path remains the default; LLM code path is **optional** via `USE_LLM_CODE=1`. When the LLM is used, the output guard is minimal (forbidden patterns); no full AST or semantic check. Scenario C failure is **state-driven**: an active misconception is activated for a unit and the stub returns the corresponding wrong code; deterministic and traceable.
- **TA conversation:** Optional LLM when `OPENAI_API_KEY` is set; otherwise stub. Single reply per teaching event; no multi-turn chat.
- **Mastery history:** Persisted in state within the run (Stage E): per-attempt entries in mastery_history; aggregation across attempts; no cross-restart persistence.
- **Problem bank:** Curated only; no automatic problem generation.

The prototype remains **intentionally minimal**: local, no frontend/API/database/deployment/Docker/cloud, Stage One scope only.

---

## Running with or without an LLM

- **Default (no env vars):** Conversation and code generation both use stubs. The demo runs with no external services.
- **Conversation only:** Set `OPENAI_API_KEY` and install `openai`. The TA learner response may come from the LLM; code attempts still use the stub unless `USE_LLM_CODE` is set.
- **Code generation only:** Set `OPENAI_API_KEY` and `USE_LLM_CODE=1` (or `true`). Scenario B will use the LLM to generate the TA code attempt; if the API fails or the output guard rejects the code, the stub is used automatically. Scenario C always uses the stub.
- **Both:** Set `OPENAI_API_KEY` and `USE_LLM_CODE=1` to use the LLM for both conversation and (in B) code.

---

## Next step after Stage F

1. **Stage G:** Readiness gate for domain expansion (verify migration complete; no new code).
2. **Later:** Domain adapter extraction (guard rules, stubs, evaluation adapter as Python “content” only); add Database / AI Literacy as new content + adapters.
