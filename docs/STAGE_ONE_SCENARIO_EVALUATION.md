# Stage One: Scenario Evaluation

**Document type:** Teacher-facing evaluation — demo scenarios and what they demonstrate  
**Date:** 2026-03-12  
**Purpose:** Summarize the three demo scenarios (A, B, C), their setup, behavior, and outcomes, and link them to the teacher’s first-step goal.

---

## Overview of the Three Scenarios

The Stage One prototype runs three scenarios in sequence via `python prototype/demo_stage1.py`:

| Scenario | Goal | Expected outcome |
|----------|------|------------------|
| **A** | Minimal learned state | Only problems requiring learned units can be selected; with only `print_function` learned, eligible set is empty; ineligible problems listed with missing units. |
| **B** | Success path | Teach `variable_assignment` + `print_function` → select matching problem → TA succeeds → mastery PASS (proficient). |
| **C** | Failure path | Same teaching as B; TA produces wrong code (simulated misconception) → evaluator FAIL → mastery reflects failure (failing). |

---

## Scenario A: Minimal Learned State

### Setup

- **Teaching event:** One event only.
  - `topic_taught`: "Print output"
  - `knowledge_units_taught`: `["print_function"]`
  - `note`: "Student teaches only how to use print()."
- **State after teaching:** Only `print_function` is learned. All other units remain `unknown`.

### Learned Knowledge Units

- `print_function` (only).

### Selected or Non-Selected Problem Behavior

- **Eligible problems:** None. In the curated bank, every problem that uses `print_function` also requires at least one other unit (e.g. `variable_assignment`, `user_input`). So the set of problems whose `knowledge_units_tested` ⊆ {`print_function`} is empty.
- **Selected problem:** `None`.
- **Ineligible reasons:** The demo prints the first 5 ineligible problems with `problem_id` and `missing_units` (e.g. `prob_var_001` missing `variable_assignment`), showing why each is not selectable.

### TA Response Behavior

- After the teaching event, `get_ta_learner_response` is called. With stub: a short learner-style line such as “I think print() is how I show something on the screen.” With LLM: a 1–2 sentence reply constrained by learned units and Stage One scope.

### Code Attempt Path

- No problem is selected, so **no code attempt** is run in Scenario A. The scenario focuses on **selection constraint** only.

### Evaluation Outcome

- No test is executed. The outcome is **demonstration that knowledge state controls selection**: only when all required KUs are learned can a problem be selected; with only `print_function`, no problem in the bank is eligible.

### What This Scenario Demonstrates

- The TA starts from a minimal learned state (one unit).
- Problem selection is **strictly constrained** by the knowledge state: if any required KU is not learned, the problem is ineligible and is not selected.
- The prototype makes this visible via “eligible problem IDs” (empty) and “ineligible reasons” (missing units per problem), supporting the teacher goal that the **programming test examines the TA’s mastery** only over what has been taught.

---

## Scenario B: Success Path

### Setup

- **Teaching event:** One event.
  - `topic_taught`: "Variables and print"
  - `knowledge_units_taught`: `["variable_assignment", "print_function"]`
  - `note`: "Student teaches variables and print()."
- **State after teaching:** `variable_assignment` and `print_function` are learned.

### Learned Knowledge Units

- `variable_assignment`, `print_function`.

### Selected or Non-Selected Problem Behavior

- **Eligible problems:** Include any problem whose `knowledge_units_tested` ⊆ {`variable_assignment`, `print_function`}. The first such problem in the bank is typically `prob_var_001` (“creates a variable named age, assigns it 20, and prints that value”), which requires exactly those two units.
- **Selected problem:** `prob_var_001` (or first eligible in load order).

### TA Response Behavior

- Same as in A: one learner-style response after the teaching event (stub or LLM), consistent with learned units.

### Code Attempt Path

- **Stub path (default):** `get_ta_code_attempt(..., use_llm_code=False)` → `ta_attempt.get_ta_attempt()` returns the stub correct code for `prob_var_001`: e.g. `age = 20` and `print(age)`.
- **LLM path (optional):** If `USE_LLM_CODE=1` and `OPENAI_API_KEY` is set, Scenario B calls `get_ta_code_attempt(..., use_llm_code=True)`. The LLM generates code from the problem and learned units; if the **output guard** accepts it (no forbidden constructs), that code is used; otherwise the stub is used. No `force_fail_problem_ids`; no forced misconception.

### Evaluation Outcome

- TA code is run against the problem’s test cases (e.g. empty stdin, expected output `"20\n"`). Stub code produces the correct output → **PASS**.
- Mastery summary: one problem attempted, passed → per-unit and overall **proficient** (pass rate ≥ 0.8 in the single-attempt rubric).

### What This Scenario Demonstrates

- **Teach → select matching problem → TA succeeds → mastery PASS.** The full success path of the Stage One loop.
- The TA’s code is **constrained by knowledge state**: only learned units are used (stub or LLM). The programming test **examines** the TA’s mastery and the result is reported (proficient).
- With `USE_LLM_CODE=1`, the prototype can show that the **optional** LLM code path can also satisfy the same constraint and pass the test when the guard accepts the generated code.

---

## Scenario C: Failure Path

### Setup

- **Teaching event:** Same as B.
  - `topic_taught`: "Variables and print"
  - `knowledge_units_taught`: `["variable_assignment", "print_function"]`
- **State after teaching:** Same as B: `variable_assignment`, `print_function` learned.

### Learned Knowledge Units

- `variable_assignment`, `print_function`.

### Selected or Non-Selected Problem Behavior

- Same as B: `prob_var_001` is selected (same eligible set).

### TA Response Behavior

- Same pattern: one learner response after teaching (stub or LLM). The note in the event mentions a misconception for context, but the **code path** is forced to fail via `force_fail_problem_ids`, not via a misconception-driven LLM.

### Code Attempt Path

- **Stub only (deterministic):** `get_ta_code_attempt(..., force_fail_problem_ids={"prob_var_001"}, use_llm_code=False)`. The code path **always** uses the stub: for `prob_var_001` the “wrong” stub is returned (e.g. `age = 20` and `print(age + 1)` → output `21` instead of `20`). LLM is **not** used so the failure is reproducible.

### Evaluation Outcome

- TA code is run against the same test cases. Output is wrong → **FAIL**.
- Mastery summary: one problem attempted, failed → per-unit and overall **failing** (pass rate < 0.5 in the single-attempt rubric).

### What This Scenario Demonstrates

- **Same teaching as B, but TA produces wrong code → evaluator FAIL → mastery reflects failure.** The student (or teacher) can see the TA’s incorrect code and the test result, supporting reflection and re-teaching.
- The failure path is **intentionally stubbed** so it does not depend on LLM non-determinism; the demo always shows a clear fail and a failing mastery level when the TA’s code is wrong.

---

## Link to the Teacher’s First-Step Goal

The teacher’s immediate goals (from STAGE_ONE_PROPOSAL.md) are:

1. **Define a TA that starts with no programming knowledge** — Scenario A and B both start from a state where only the units just “taught” are learned; the rest are unknown. Scenario A makes the minimal state explicit (only `print_function`).
2. **Design a programming test to examine the TA’s mastery** — Scenarios B and C use one problem from the bank; the TA’s code is run and compared to expected output. Pass/fail and mastery level (proficient vs failing) are reported. Scenario A shows that the test is only applied to problems that match what the TA has learned.
3. **Determine the design for the interaction** (explanation, conversation, programming problems) — The prototype uses structured teaching events (explanation), a single TA learner response per event (conversation), and curated problems with selection by knowledge state (programming problems). The three scenarios together show: selection constrained by state (A), success path (B), and failure path (C).

Together, A, B, and C provide **evidence** that the first-step goal is met: zero-knowledge TA, mastery examined via a programming test, and an interaction design that combines teaching, response, problem selection, attempt, and mastery reporting in one reproducible loop.
