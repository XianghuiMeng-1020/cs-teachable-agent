# Shared Core Architecture

**Document type:** Shared system architecture — modules, interfaces, and data flow  
**Governing documents:** MASTER_SYSTEM_BLUEPRINT.md; docs/UNIFIED_KNOWLEDGE_STATE_SCHEMA.md; docs/UNLEARNING_RELEARNING_ENGINE.md  
**Companion document:** docs/TRACE_AND_HISTORY_LAYER.md (trace integration points)  
**Status:** Binding architecture for migration of Python Stage One and for all future domain work

---

## 1. Purpose of the Shared Core Architecture

The shared core architecture defines how the system’s modules, interfaces, and data flow work together so that (1) the current Python Stage One prototype can be migrated into the full framework without re-inventing the mechanism, (2) later Python, Database, and AI Literacy domain work plugs into the same engines and interfaces, and (3) implementation remains aligned with the main claim: a unified, knowledge-state-constrained, misconception-aware, unlearning/relearning-capable framework. This document does not specify implementation technology or deployment; it specifies **which shared modules exist, what each does, what it consumes and produces, and how they interact**. The architecture is the backbone that connects the governing blueprint, the unified knowledge state schema, and the unlearning/relearning engine to concrete components and to the existing prototype.

---

## 2. Why the Shared Core Must Be Defined Before Domain Expansion

If domain expansion (Database, AI Literacy, or mature Python) proceeded without a defined shared core, each domain would risk its own state model, its own selection logic, and its own misconception handling — producing three separate pipelines and undermining the “one framework” claim. Defining the shared core first ensures that: (1) every domain uses the same Knowledge State Engine, the same Misconception/Unlearning/Relearning Engine, the same Task Engine selection rule, the same Mastery Evaluator rubric, and the same Guard/Fallback Layer principles; (2) the only domain-specific additions are content (knowledge units, misconceptions, tasks) and domain adapters (e.g. code runner vs. query runner vs. explanation scorer); and (3) the current Python prototype is explicitly mapped onto this architecture so that refactoring is a migration into the shared core, not a rewrite. The shared core is the contract that prevents drift into “three separate systems.”

---

## 3. Shared Modules Overview

The shared core consists of the following modules. All are **shared** across domains; domain-specificity is confined to the Domain Layer (content and task-type adapters).

| Module | Purpose (short) | Reads from | Writes to |
|--------|------------------|------------|-----------|
| **Knowledge State Engine** | Single source of truth for TA knowledge; state transitions (learn, misconception, correct, relearn) | Domain layer (unit definitions); teaching/correction/relearning events | Knowledge state (per unit); optionally trace |
| **Interaction Engine** | Orchestrates teach → respond → test → reflect; routes events | Teaching input; state; task/eval results | Calls other engines; assembles responses; triggers trace |
| **Learner Dialogue Engine** | TA conversational response constrained by state | Knowledge state (learned units, active misconceptions) | Dialogue output; optionally trace |
| **Task / Problem Engine** | Selects eligible tasks from bank by knowledge state | Knowledge state (learned/eligible units); domain task bank | Selected task(s); eligibility info; optionally trace |
| **TA Attempt Engine** | Generates TA’s task attempt (code/query/explanation) | Knowledge state; task; active misconceptions | TA output; optionally trace |
| **Mastery Evaluator** | Scores attempt; computes per-unit and overall mastery | Task; TA output; evaluation adapter; knowledge state | Pass/fail; mastery levels; mastery_history; optionally trace |
| **Misconception / Unlearning / Relearning Engine** | Activates, corrects, unlearns, relearns misconceptions | Teaching events; correction signals; domain misconception catalog | State updates (active_misconceptions, status, correction/relearning evidence); optionally trace |
| **Guard / Fallback Layer** | Rejects outputs that violate state; provides fallback | TA output; knowledge state; domain guard rules | Accept/reject; fallback output when reject |
| **Trace / History Layer** | Records full evidence chain for evaluation | All engines (via integration points) | Trace store (see TRACE_AND_HISTORY_LAYER.md) |

The Domain Layer supplies: knowledge unit definitions, misconception catalog, task bank, and task-type-specific adapters (e.g. run code, run query, score explanation). It does **not** contain engine logic; it only supplies content and evaluation primitives.

---

## 4. Knowledge State Engine

**Purpose:** Maintain the TA’s knowledge state as the single source of truth. Handle all state transitions: unknown → partially_learned → learned; misconception activation; correction (unlearning); relearning; and updates to evidence (teaching, testing, correction, relearning) and mastery_history. Expose query interfaces so that every other module that needs “what does the TA know?” reads from this engine.

**Inputs:**
- Domain identifier and schema version.
- Knowledge unit definitions (from Domain Layer) for the domain(s) in scope.
- Teaching events (from Interaction Engine or teaching pipeline): topic, knowledge_units_taught, note, and optionally interpretation (correct / incorrect / ambiguous, and if incorrect, which misconception).
- Correction events (from Misconception Engine or Interaction Engine): misconception_id, unit(s), trigger.
- Testing and evaluation results (from Mastery Evaluator): task_id, attempt_id, pass_fail, units involved, optional misconception_active_during_attempt.
- Relearning policy (e.g. how many teaching events or successful tasks after correction to transition status back to learned).

**Outputs:**
- Full or partial knowledge state (per domain): for each unit, status, confidence, active_misconceptions, teaching_evidence, testing_evidence, correction_evidence, relearning_evidence, mastery_history, last_updated.
- Query results: get_learned_units(domain), get_eligible_units(domain), get_active_misconceptions(domain or unit), get_state_snapshot(domain).

**Dependencies:** Domain Layer (unit definitions); optionally Misconception Engine for activation/unlearning/relearning transitions (or the Knowledge State Engine may apply those transitions when the Misconception Engine invokes it).

**Reads from (its own store):** Current state for the domain(s). No other store is the source of truth for “what the TA knows.”

**Writes:** Updates to state (status, confidence, active_misconceptions, evidence lists, mastery_history). May emit state-diff or state-update events to the Trace/History Layer.

---

## 5. Interaction Engine

**Purpose:** Orchestrate the teach → respond → test → reflect loop. Receive teaching input (and optionally test requests), route to the right modules, call Knowledge State Engine for updates, Learner Dialogue Engine for TA response, Task Engine for task selection, TA Attempt Engine for attempts, Mastery Evaluator for scoring, and Misconception Engine for activation/correction/relearning. Assemble results for the student and ensure the Trace/History Layer receives the necessary events.

**Inputs:**
- Teaching events (structured or, in a future phase, raw input to be interpreted).
- Test request (e.g. “run a test” for current domain).
- Current domain (and optionally session/session state).
- Access to Knowledge State Engine, Learner Dialogue Engine, Task Engine, TA Attempt Engine, Mastery Evaluator, Misconception Engine, Guard/Fallback Layer, Trace/History Layer.

**Outputs:**
- After teaching: updated state (via Knowledge State Engine); TA learner response (from Learner Dialogue Engine); optional eligibility summary.
- After test request: selected task (or “none”); TA attempt (code/query/explanation); pass/fail and mastery report; optional reflection summary.
- Assembled response to the student (e.g. “TA says X”; “TA attempted problem P and passed/failed”; “Mastery: …”).

**Dependencies:** All other shared engines and the Trace/History Layer. Does not implement state or misconception logic itself; it delegates.

**Reads from:** Knowledge State Engine (current state for dialogue, task selection, attempt generation, and reporting). Domain Layer only indirectly (via other engines that load tasks, units, misconceptions).

**Writes:** Nothing directly to the knowledge state. Triggers writes by calling Knowledge State Engine (after teaching, after correction, after relearning) and Mastery Evaluator (which may write mastery_history via Knowledge State Engine). Requests trace records from other modules or writes orchestration-level trace events (e.g. “cycle started,” “teaching applied,” “test completed”).

---

## 6. Learner Dialogue Engine

**Purpose:** Generate the TA’s conversational response after teaching (and optionally during reflection). Response must be constrained by the TA’s current knowledge state: only discuss learned (or partially_learned) concepts; express active misconceptions when present; ask about or express confusion about untaught concepts; never tutor the student.

**Inputs:**
- Current knowledge state for the active domain: learned_units, partially_learned_units (if used), active_misconceptions per unit (ids and optionally descriptions/examples from Domain Layer).
- Teaching event that just occurred: topic_taught, knowledge_units_taught, note.
- Optional: conversation history (if multi-turn is supported); scope constraints (e.g. Stage One scope).

**Outputs:**
- TA learner response text (one or more sentences).
- Optional: dialogue trace (e.g. which units/misconceptions were used to constrain the response).

**Dependencies:** Knowledge State Engine (read-only for this engine); Domain Layer for misconception descriptions/examples if injected into prompts.

**Reads from:** Knowledge state (learned units, active misconceptions). Does not read from raw conversation history as the source of “what the TA knows”; only from state.

**Writes:** None to knowledge state. May send a dialogue record to Trace/History Layer.

---

## 7. Task / Problem Engine

**Purpose:** Select tasks from the domain’s task bank such that the TA is only offered tasks whose required knowledge units are all in an eligible state (learned or partially_learned per schema). Optionally filter by difficulty, targeted misconceptions, or mastery gaps. Return the selected task(s) and, when no task is selected, ineligible reasons (missing units per task).

**Inputs:**
- Current knowledge state: for the domain, the set of unit ids that are eligible (learned or partially_learned; policy may exclude units in corrected state until relearning is complete).
- Domain task bank (from Domain Layer): each task has task_id, knowledge_units_tested (or required), difficulty, targeted misconceptions, evaluation criteria.
- Optional: filters (e.g. only tasks targeting a specific misconception; only tasks at or below a difficulty level).

**Outputs:**
- Selected task (one) or null if no task is eligible.
- Eligible task ids (list) and/or ineligible reasons (per task: task_id, missing_units).
- Optional: next-best or ranked list for UI.

**Dependencies:** Knowledge State Engine (read-only); Domain Layer (task bank). Selection rule is shared: “only tasks whose required units ⊆ eligible_units.”

**Reads from:** Knowledge state (eligible units). Task bank from Domain Layer.

**Writes:** Nothing to knowledge state. May send task_selection trace (selected task, eligible set, ineligible reasons) to Trace/History Layer.

---

## 8. TA Attempt Engine

**Purpose:** Produce the TA’s attempt at a given task — code (Python), query (Database), or explanation (AI Literacy) — constrained by the current knowledge state and active misconceptions. Use only learned units; inject misconception-driven errors when the task involves a unit with an active misconception. Apply Guard/Fallback Layer: reject output that uses untaught concepts or that violates domain guard rules; on reject or LLM failure, return fallback (e.g. stub) so behavior is deterministic.

**Inputs:**
- Current knowledge state: learned_units, active_misconceptions (per unit, with ids and optionally example wrong behavior from Domain Layer).
- Task: task_id, statement, knowledge_units_tested, test cases or expected results, targeted misconceptions.
- Domain and task type (code / query / explanation).
- Optional: force_fail or stub overrides (for testing; e.g. Scenario C).

**Outputs:**
- TA attempt: the actual output (code string, query string, or explanation text).
- Metadata: whether guard passed; whether fallback was used; which misconception(s) were applied (if any).

**Dependencies:** Knowledge State Engine (read-only); Guard/Fallback Layer (validate output, provide fallback); Domain Layer (misconception examples, guard rules). Generation may be stub-based, LLM-based, or hybrid; the interface is “request attempt → return output + metadata.”

**Reads from:** Knowledge state (learned units, active misconceptions). Task and Domain Layer for prompts and guard rules.

**Writes:** None to knowledge state. May send attempt trace (task_id, output summary, guard result, fallback used, active misconceptions) to Trace/History Layer.

---

## 9. Mastery Evaluator

**Purpose:** Evaluate the TA’s task attempt against the task’s evaluation criteria (run code and compare stdout; run query and compare result set; score explanation against rubric). Compute per-unit and overall mastery levels using the shared rubric (e.g. pass rate over attempted tasks → failing / developing / proficient). Update mastery_history and optionally status/confidence when the Knowledge State Engine supports it. Apply policy for weighting or excluding attempts during active misconception when computing current mastery.

**Inputs:**
- Task: task_id, knowledge_units_tested, test cases or expected result set or rubric criteria.
- TA attempt output (from TA Attempt Engine).
- Current knowledge state (optional): for units involved, whether a misconception was active during the attempt (to apply weighting/exclusion policy).
- Domain evaluation adapter: how to run and compare (execute code, execute query, score explanation).

**Outputs:**
- Pass/fail (or score) for this attempt.
- Per-unit mastery update: for each unit in knowledge_units_tested, pass/fail and updated pass_rate/mastery_level if applicable.
- Overall mastery level (optional).
- Mastery report (for student/UI): levels per unit, overall, and optional labels (e.g. “misconception active for unit X”).

**Dependencies:** Knowledge State Engine (read current state; write mastery_history and optionally confidence/status); Domain Layer (evaluation adapter); UNIFIED_KNOWLEDGE_STATE_SCHEMA and mastery rubric for aggregation rules.

**Reads from:** Knowledge state (for policy: which attempts count, misconception during attempt). Task and TA output for scoring.

**Writes:** Mastery results and history back to Knowledge State Engine (or the engine persists them when the evaluator returns results). May send evaluation trace (task_id, attempt_id, pass_fail, mastery delta) to Trace/History Layer.

---

## 10. Misconception / Unlearning / Relearning Engine

**Purpose:** Implement the full misconception lifecycle: (1) activate a misconception when teaching is incorrect or ambiguous (or pre-seeded/transfer); (2) supply active misconceptions to Learner Dialogue Engine and TA Attempt Engine so behavior reflects them; (3) detect correction (explicit correction event or teaching that matches remediation); (4) perform unlearning (remove from active_misconceptions, set status to corrected); (5) recognize relearning evidence (post-correction teaching and successful tasks) and transition status back to learned when policy is satisfied. All transitions and evidence updates are written to the Knowledge State Engine so the state remains the single source of truth.

**Inputs:**
- Teaching event and interpretation: topic, knowledge_units_taught, and whether the teaching is correct, incorrect (with matched misconception_id), or ambiguous (with optional misconception_id).
- Explicit correction event (optional): misconception_id, unit(s), trigger.
- Domain misconception catalog: for each misconception, id, affected_units, remediation criteria (or remediation hint), example incorrect/correct behavior.
- Current knowledge state (read from Knowledge State Engine): for affected units, current status and active_misconceptions.
- Relearning policy: e.g. minimum teaching events or successful tasks after correction to transition to learned.

**Outputs:**
- State update requests to Knowledge State Engine: activate misconception (add to active_misconceptions, set status to misconception); unlearn (remove misconception, set status to corrected); add relearning_evidence and possibly set status to learned.
- No direct output to the student; behavioral effect is through state that Dialogue and Attempt engines read.

**Dependencies:** Knowledge State Engine (read and write); Domain Layer (misconception catalog). Does not generate dialogue or task output; it only updates state and notifies (via state) downstream engines.

**Reads from:** Knowledge state (current status, active_misconceptions, correction_evidence, relearning_evidence). Teaching events and correction events. Misconception catalog.

**Writes:** All writes go through the Knowledge State Engine: active_misconceptions, status, correction_evidence, relearning_evidence. May emit misconception lifecycle events to Trace/History Layer (activation, correction, unlearning, relearning).

---

## 11. Guard / Fallback Layer

**Purpose:** Ensure the TA’s behavior remains constrained by the knowledge state even when the LLM (or any generator) leaks untaught knowledge. Reject outputs that use forbidden constructs or concepts not in the learned set; when rejection occurs or when the generator fails, provide a deterministic fallback (e.g. stub code or safe default) so the system never returns unconstrained output. Optionally verify that misconception-driven output is consistent with the active misconception rather than randomly wrong.

**Inputs:**
- TA output (code, query, or explanation) from the TA Attempt Engine’s generator.
- Knowledge state: learned_units (and optionally domain’s “forbidden” list for current scope, e.g. no `def`/`class` if functions not taught).
- Domain guard rules: forbidden patterns, allowed constructs per scope.
- Optional: active misconceptions (to check that wrong output matches the misconception).

**Outputs:**
- Accept or reject.
- If reject: fallback output (from Domain Layer or built-in stubs) so the Attempt Engine can return a deterministic result.
- Optional: violation reason (e.g. “used `def` but functions not learned”).

**Dependencies:** Knowledge State Engine (read-only); Domain Layer (guard rules, fallback stubs). Used by TA Attempt Engine; does not call other engines.

**Reads from:** Knowledge state (learned units); domain guard rules.

**Writes:** None to knowledge state. May send guard_result trace (accept/reject, violation reason) to Trace/History Layer.

---

## 12. Trace / History Integration Points

Every module that performs an action that must be evaluable or diagnosable should contribute to the Trace/History Layer. The following are the integration points; the exact event types and minimum fields are defined in docs/TRACE_AND_HISTORY_LAYER.md.

- **Interaction Engine:** Orchestration events (cycle start, teaching received, test requested, cycle end); may aggregate or forward events from other engines.
- **Knowledge State Engine:** State update events (after teaching, after correction, after relearning, after mastery update): domain, unit(s), state_before, state_after, trigger (teaching_event_id, correction_event_id, etc.).
- **Learner Dialogue Engine:** Dialogue response event: domain, teaching_event_id, learned_units, active_misconceptions (ids), response summary or full text.
- **Task / Problem Engine:** Task selection event: domain, selected_task_id or null, eligible_ids, ineligible_reasons.
- **TA Attempt Engine:** Attempt event: domain, task_id, attempt_id, output summary, guard_passed, fallback_used, active_misconceptions_applied.
- **Mastery Evaluator:** Evaluation event: task_id, attempt_id, pass_fail, units_tested, mastery_level_before, mastery_level_after, per-unit pass/fail.
- **Misconception Engine:** Misconception lifecycle events: activation (unit, misconception_id, trigger, teaching_event_id); correction (unit, misconception_id, corrected_at, trigger); relearning (unit, relearning_event_id, type, state_after).

The Trace/History Layer is a logical layer: it may be implemented as a write-through log, a dedicated store, or events passed to a central logger. The architecture only requires that these integration points exist and that the minimum trace fields defined in TRACE_AND_HISTORY_LAYER.md are recorded so that the chain teaching → state change → behavior → testing → mastery → correction → relearning can be reconstructed for evaluation and diagnosis.

---

## 13. Domain Layer vs Shared Core Boundary

**Shared core (this architecture):** All of the modules above. Same interfaces, same data flow, same state schema, same misconception lifecycle logic. No domain-specific conditionals inside the core; the core does not branch on “if domain == Python” for engine behavior.

**Domain Layer (content and adapters only):**
- **Content:** Knowledge unit definitions (id, name, description, topic_group, prerequisites, examples). Misconception catalog (id, affected_units, description, example_incorrect/correct, remediation_hint). Task bank (task_id, statement, knowledge_units_tested, difficulty, test cases or expected result set or rubric).
- **Adapters:** (1) Task-type adapter: given a task and TA output, how to evaluate (run Python code and compare stdout; run SQL and compare result set; score explanation against rubric). (2) Guard rules: list of forbidden patterns for the domain and scope. (3) Fallback stubs: per-task or per-type fallback output when guard rejects or generator fails. (4) Optional: prompt templates or vocabulary for Learner Dialogue Engine and TA Attempt Engine (templates are domain-specific; the mechanism that fills them from state is shared).

What must **not** be in the Domain Layer: duplicate state logic, duplicate selection logic, duplicate misconception transition rules, or a separate “engine” that does the same job as a shared engine. Adding a new domain means adding a new content package and adapters that conform to the shared interfaces; it must not mean adding a new state machine or a new mastery formula.

---

## 14. Data Flow Across One Complete Teaching–Testing Cycle

The following is one full cycle in concrete order. All state reads and writes go through the Knowledge State Engine; all behavioral outputs (dialogue, attempt) are constrained by that state.

1. **Student teaching event arrives.** Interaction Engine receives a teaching event (e.g. topic, knowledge_units_taught, note). Trace: teaching_event recorded (see TRACE_AND_HISTORY_LAYER.md).

2. **Teaching interpretation (optional but recommended).** A teaching interpreter (may live in Interaction Engine or a small shared sub-component) determines whether the teaching is correct, incorrect (and which misconception), or ambiguous. If incorrect or ambiguous, the misconception_id and affected units are passed to the Misconception Engine. If correct, no misconception activation.

3. **Knowledge state is updated.**  
   - If correct: Knowledge State Engine applies teaching: for each knowledge_units_taught, update status (unknown → learned or partially_learned per policy), append teaching_evidence, update last_updated.  
   - If incorrect/ambiguous: Misconception Engine activates the misconception for the affected units; Knowledge State Engine updates: add to active_misconceptions, set status to misconception, append teaching_evidence with misconception_activated.  
   Trace: state_update (state_before, state_after, trigger = teaching_event_id).

4. **Learner Dialogue Engine produces response.** Interaction Engine calls Learner Dialogue Engine with current state (learned units, active misconceptions). Dialogue Engine returns TA response text. Trace: learner_dialogue (teaching_event_id, response, units/misconceptions used). Interaction Engine presents response to student.

5. **Student requests test (or system proceeds to test).** Interaction Engine requests a task from Task Engine.

6. **Task Engine selects eligible task.** Task Engine reads eligible units from Knowledge State Engine, filters task bank to tasks whose required units ⊆ eligible_units, returns selected task (or null and ineligible reasons). Trace: task_selection (selected_task_id, eligible_ids, ineligible_reasons).

7. **TA Attempt Engine produces attempt.** If a task was selected, Interaction Engine calls TA Attempt Engine with task and current state (learned units, active misconceptions). Attempt Engine generates output (code/query/explanation). Guard/Fallback Layer validates output; if reject, Attempt Engine uses fallback. Attempt Engine returns output and metadata. Trace: ta_attempt (task_id, attempt_id, output_summary, guard_passed, fallback_used, active_misconceptions).

8. **Mastery Evaluator scores result.** Interaction Engine calls Mastery Evaluator with task, TA output, and (optionally) state for weighting. Evaluator runs domain adapter (execute code/query, score explanation), determines pass/fail, updates per-unit and overall mastery (pass rates, levels), and writes mastery_history (and optionally status/confidence) via Knowledge State Engine. Trace: evaluation (task_id, attempt_id, pass_fail, mastery_before, mastery_after).

9. **Misconception Engine checks correction/relearning (if applicable).** If the student subsequently provides corrective teaching or an explicit correction event, Interaction Engine (or teaching pipeline) notifies Misconception Engine. Engine detects correction, performs unlearning (remove misconception, status → corrected), and writes correction_evidence via Knowledge State Engine. Later, post-correction teaching or successful tasks are interpreted as relearning evidence; when policy is satisfied, Engine updates status to learned and writes relearning_evidence. Trace: misconception_activation (if activation occurred in step 3); correction (when unlearning); relearning (when status returns to learned).

10. **History and mastery are updated.** All evidence (teaching_evidence, testing_evidence, correction_evidence, relearning_evidence, mastery_history) is already written by Knowledge State Engine and Mastery Evaluator during the cycle. Trace/History Layer holds the full event log for evaluation and diagnosis.

11. **Response assembled.** Interaction Engine assembles the outcome (TA response after teaching; selected task or ineligible message; TA attempt and pass/fail; mastery report; optional reflection). Student sees the result; evaluation can later reconstruct the chain from trace.

---

## 15. Mapping from the Current Python Stage One Prototype to the Full Shared Core

The current prototype is a valid but partial instantiation of this architecture. The following mapping is explicit and honest.

| Current prototype component | Maps to shared core module | Notes |
|----------------------------|----------------------------|--------|
| **state_tracker.py** (StateTracker, load_knowledge_units) | **Knowledge State Engine** (partial) | Current state is unit_id → status only (unknown, partially_learned, learned). No misconception fields, no evidence lists, no mastery_history in state. Migration: extend state to full schema (active_misconceptions, teaching_evidence, testing_evidence, correction_evidence, relearning_evidence, mastery_history, confidence); add domain and schema_version; keep get_state, get_learned_units, update_after_teaching and add transition APIs for misconception activation, unlearning, relearning. |
| **teaching_events.py** (make_teaching_event, apply_teaching_event) | **Interaction Engine** (orchestration) + **Knowledge State Engine** (state update) | apply_teaching_event is the minimal “apply teaching → update state” path. No teaching interpretation (correct/incorrect); no misconception activation. Migration: either keep as “correct teaching only” path and add a separate path for interpreted teaching (incorrect → Misconception Engine), or fold interpretation into Interaction Engine and call both Knowledge State Engine and Misconception Engine. |
| **problem_selector.py** (load_problems, select_problem, get_eligible_problem_ids, get_ineligible_reasons) | **Task / Problem Engine** | Logic is already shared: required units ⊆ learned_units. Migration: rename “problems” to “tasks” for consistency; feed learned_units from Knowledge State Engine (which may expose “eligible” units including partially_learned if policy allows). Task bank remains in Domain Layer. |
| **mastery_evaluator.py** (run_python_code, evaluate_attempt, mastery_summary, build_mastery_report) | **Mastery Evaluator** + **Domain Layer** (evaluation adapter) | evaluate_attempt and run_python_code are the Python execution adapter. mastery_summary/build_mastery_report implement the shared rubric (pass rate → failing/developing/proficient). Migration: Mastery Evaluator becomes the shared component that takes (task, output, adapter); adapter for Python is current run_python_code + compare stdout. Write results back to Knowledge State Engine (mastery_history) when state supports it. |
| **ta_conversation.py** (get_ta_learner_response, _fill_prompt, _fallback_stub_response) | **Learner Dialogue Engine** | Already constrained by learned_unit_ids (and optional active_misconceptions). Migration: ensure input is always from Knowledge State Engine; add active_misconceptions to prompt when non-empty so dialogue reflects misconceptions; keep stub fallback; trace dialogue output. |
| **ta_attempt.py** (get_ta_attempt) + **ta_code_generation.py** (get_ta_code_attempt, _fill_prompt, output_guard) | **TA Attempt Engine** + **Guard / Fallback Layer** | get_ta_attempt is the stub path; get_ta_code_attempt adds LLM path and uses output_guard. Migration: treat output_guard as the Guard Layer; stub in ta_attempt as Fallback. TA Attempt Engine = orchestration of “generate (LLM or stub) → guard → fallback if reject.” Active misconceptions already passed in; ensure they drive prompt (and optionally stub) so wrong behavior is misconception-consistent. |
| **demo_scenarios.py** / **demo_stage1.py** | **Interaction Engine** (orchestration) | Scenarios A/B/C manually wire: teaching event → apply_teaching_event → get_ta_learner_response → select_problem → get_ta_code_attempt → evaluate_attempt → build_mastery_report. This is the “one cycle” orchestration. Migration: replace with Interaction Engine that calls the same modules in the same order; add Trace/History writes; add Misconception Engine when teaching is interpreted as incorrect. |
| **force_fail_problem_ids** (Scenario C) | **TA Attempt Engine** / **Guard / Fallback Layer** | Scenario C forces wrong stub for a specific problem. In the full architecture, wrong behavior should come from **active misconceptions** in state, not a special flag. Migration: replace force_fail with activating a misconception (e.g. for the unit under test) so the TA Attempt Engine produces misconception-consistent wrong output; then correction and unlearning/relearning can be demonstrated. |
| **No misconception state or engine** | **Misconception / Unlearning / Relearning Engine** + **Knowledge State Engine** (active_misconceptions, correction/relearning evidence) | Prototype has misconception catalog and prompt injection but no stateful activation or correction. Migration: add Misconception Engine; on “incorrect teaching” (or explicit test hook), activate misconception in state; TA Attempt Engine and Learner Dialogue Engine already receive active_misconceptions in prompts — ensure they use state; add correction detection and unlearning/relearning transitions. |
| **No trace/history** | **Trace / History Layer** | Prototype has no persistent trace. Migration: add trace integration points as in §12 and TRACE_AND_HISTORY_LAYER.md; each engine (or Interaction Engine on their behalf) writes minimum trace events so evaluation can reconstruct the chain. |

Summary: the prototype already implements a thin version of Knowledge State Engine, Task Engine, Mastery Evaluator, Learner Dialogue Engine, TA Attempt Engine, and Guard/Fallback. It lacks: full state schema (evidence, misconceptions, mastery_history in state), teaching interpretation and Misconception Engine, explicit unlearning/relearning, and Trace/History Layer. Refactoring should extend the existing modules into the shared interfaces and add the missing engines and trace.

---

## 16. What Must Be Refactored Later

- **State representation:** Extend from unit_id → status to full per-unit schema (confidence, active_misconceptions, teaching_evidence, testing_evidence, correction_evidence, relearning_evidence, mastery_history). Add domain and schema_version at global level.
- **Teaching pipeline:** Add interpretation step (correct / incorrect / ambiguous and misconception match) and route to Misconception Engine when needed; keep apply_teaching_event for correct-teaching path.
- **Misconception Engine:** New module; implements activation, correction detection, unlearning, relearning; reads/writes through Knowledge State Engine.
- **Scenario C and wrong behavior:** Replace force_fail_problem_ids with misconception activation so wrong output is state-driven and correction/unlearning/relearning can be traced.
- **Mastery persistence:** Mastery Evaluator results should write into Knowledge State Engine’s mastery_history (and optionally update status/confidence); currently the report is built but not persisted in state.
- **Trace/History:** Add Trace/History Layer and integration points in each engine (or central logging in Interaction Engine) with minimum fields per event type.
- **Domain abstraction:** Extract task bank, knowledge units, and misconceptions into a Domain Layer interface so that “Python” is one content package and “Database”/“AI Literacy” can be added as more content + adapters without changing engine code.
- **Guard rules:** Move forbidden patterns (e.g. no def/class in Stage One) into Domain Layer so they are not hard-coded in the Guard/Fallback Layer.

---

## 17. Risks of a Weak Shared Core

- **Domain-specific branches inside engines:** If Knowledge State Engine or Misconception Engine or Task Engine contains “if domain == Python” for behavior, adding Database or AI Literacy forces engine changes and the “one framework” claim fails.
- **Duplicate state or logic in the Domain Layer:** If each domain implements its own state transitions or selection rules, the system becomes three pipelines that share a name only.
- **Skipping trace:** If trace is optional or minimal, evaluation cannot demonstrate teaching → state → behavior → mastery; the paper’s evidence chain is missing.
- **Leaving misconception lifecycle to “later”:** If the prototype is extended to more domains without implementing activation, correction, unlearning, and relearning in the shared core, the main distinguishing contribution is never realized.
- **Orchestration in the wrong place:** If each domain has its own “main loop” that differs in order or in which engines it calls, behavior and evaluation become inconsistent; the Interaction Engine must be the single orchestrator for the teach–test cycle.

---

## 18. Architecture Guardrails

- **No domain-specific engine logic.** Shared engines must not branch on domain for core behavior; they may call domain adapters (e.g. “evaluate this attempt”) whose implementation differs by domain.
- **Single source of truth.** Only the Knowledge State Engine holds “what the TA knows”; all other modules read from it (and Misconception Engine writes through it).
- **Trace non-negotiable.** Every teaching event, state update, task selection, attempt, evaluation, and misconception lifecycle event must be traceable with the minimum fields defined in TRACE_AND_HISTORY_LAYER.md.
- **Guard and fallback always in the loop.** TA Attempt Engine must always pass output through the Guard/Fallback Layer; there must be no path that returns unvalidated LLM output to the student or to the evaluator.
- **Interaction Engine orchestrates only.** It does not implement state transitions or misconception logic; it calls the appropriate engines in the order defined in §14.
- **Domain Layer is content and adapters only.** No engine logic, no state machine, no mastery formula in the Domain Layer; only definitions, catalogs, task bank, and evaluation/guard/fallback adapters.

---

## 19. Conclusion

The shared core architecture ties the governing blueprint, the unified knowledge state schema, and the unlearning/relearning engine to a concrete set of modules, interfaces, and data flow. The Knowledge State Engine is the single source of truth; the Interaction Engine orchestrates the teach → respond → test → reflect cycle; the Learner Dialogue Engine, Task Engine, TA Attempt Engine, Mastery Evaluator, and Misconception Engine each have defined inputs, outputs, and read/write contracts; the Guard/Fallback Layer ensures constrained behavior; and the Trace/History Layer captures the full chain for evaluation and diagnosis. The current Python Stage One prototype maps cleanly onto this architecture as a partial implementation: refactoring extends the existing state, selection, evaluation, dialogue, and attempt components into the shared interfaces and adds the Misconception Engine and Trace/History Layer. Future domains add only content and adapters. This document, together with TRACE_AND_HISTORY_LAYER.md, defines the shared architectural backbone so that all later domain and implementation work remains aligned with the main claim and avoids drift into three separate systems.
