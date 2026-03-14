# Trace and History Layer

**Document type:** Shared architecture — trace and history for the evidence chain  
**Governing documents:** MASTER_SYSTEM_BLUEPRINT.md; docs/UNIFIED_KNOWLEDGE_STATE_SCHEMA.md; docs/UNLEARNING_RELEARNING_ENGINE.md; docs/SHARED_CORE_ARCHITECTURE.md  
**Status:** Binding design for evaluation, interpretability, and paper evidence

---

## 1. Purpose of the Trace and History Layer

The Trace and History Layer records the full evidence chain required to support the project’s main claim: **teaching → state change → behavior → testing → mastery → correction → relearning**. Without a structured, shared trace, the system cannot demonstrate that (1) teaching actions produce the expected state changes, (2) the TA’s behavior is constrained by that state, (3) mastery reflects state and testing outcomes, and (4) misconception activation, correction, unlearning, and relearning are observable and evaluable. This layer is essential for evaluation (linking teaching to state to behavior to mastery), interpretability (why did the TA do X?), mastery history (trajectory over time), misconception lifecycle analysis, and future paper evidence. It does not replace the knowledge state as the source of truth for “what the TA knows”; it provides a **log of events** that can reconstruct how the state and behavior evolved so that claims can be validated.

---

## 2. Why Traceability Is Central to the Main Claim

The main claim is that the project delivers a **unified, knowledge-state-constrained, misconception-aware, unlearning/relearning-capable framework** with behavior and outcomes traceable across domains. Supporting that claim requires evidence that:

- Teaching events cause predictable state updates (unknown → learned, or activation of a misconception).
- The TA’s dialogue and task attempts are consistent with the current state (learned units, active misconceptions).
- Task selection is constrained by state (only eligible tasks are offered).
- Evaluation results (pass/fail, mastery levels) follow from attempts and state.
- Correction events trigger unlearning; relearning evidence triggers return to learned.

None of this can be proven with “the demo works” alone. It requires a **trace** that records, for each relevant event: what happened, when, which domain and units were affected, what the state was before and after, and how the event links to prior events (e.g. attempt_id, teaching_event_id). The Trace and History Layer defines which events are recorded and what minimum fields each must have so that analyses and evaluation scripts can reconstruct the chain and distinguish never learned, partially learned, learned wrongly, corrected, relearned, succeeded because of teaching, failed because of missing knowledge, and failed because of misconception.

---

## 3. Core Event Types to Record

The following event types must be recorded. Each is produced by one or more shared modules (see SHARED_CORE_ARCHITECTURE.md §12).

| Event type | Produced by | Why recorded |
|------------|-------------|--------------|
| **teaching_event** | Interaction Engine (or teaching pipeline) | Start of chain: what the student taught and when. |
| **teaching_interpretation** | Teaching interpreter / Interaction Engine | Whether teaching was correct, incorrect (with misconception_id), or ambiguous. Links teaching to misconception activation. |
| **knowledge_state_update** | Knowledge State Engine | State before and after each change (teaching, correction, relearning, mastery). Links events to state. |
| **learner_dialogue** | Learner Dialogue Engine | TA’s response after teaching; shows dialogue is state-constrained. |
| **task_selection** | Task / Problem Engine | Which task was selected (or none) and why (eligible set, ineligible reasons). |
| **ta_attempt** | TA Attempt Engine | TA’s output for a task; guard result; whether fallback used; which misconceptions applied. |
| **evaluation_result** | Mastery Evaluator | Pass/fail and mastery change for the attempt. |
| **misconception_activation** | Misconception / Unlearning / Relearning Engine | When and why a misconception was activated. |
| **correction_event** (unlearning) | Misconception Engine | When a misconception was corrected and state moved to corrected. |
| **relearning_event** | Misconception Engine (or Knowledge State Engine) | When relearning evidence was recorded and status returned to learned. |
| **mastery_update** | Mastery Evaluator / Knowledge State Engine | When mastery_level or mastery_history was updated (can be part of evaluation_result or separate). |

Together these allow reconstruction of the full cycle and of per-unit and per-session trajectories.

---

## 4. Teaching Event Records

**Event type:** `teaching_event`

**Purpose:** Record that a teaching event was received and what it contained. This is the root of the chain for “teaching → state change.”

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id for this teaching event (e.g. teaching_event_id). |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When the event occurred. |
| **domain** | String | Domain this teaching applies to. |
| **topic_taught** | String (optional) | Human-readable topic. |
| **knowledge_units_taught** | List of unit ids | Units the teaching claimed to target. |
| **note** | String (optional) | Free text or structured note. |
| **session_id** (optional) | String | Session or run identifier for grouping. |

**Optional:** Raw or summarized teaching content if needed for analysis. Interpretation (correct/incorrect/ambiguous) is recorded in teaching_interpretation.

---

## 5. Teaching Interpretation Records

**Event type:** `teaching_interpretation`

**Purpose:** Record how the teaching was interpreted (correct, incorrect, ambiguous) and, if incorrect or ambiguous, which misconception was matched. Links teaching to misconception activation.

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id for this interpretation record. |
| **teaching_event_id** | String | Links to the teaching event. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When interpretation was done. |
| **domain** | String | Domain. |
| **interpretation** | Enum: correct | incorrect | ambiguous | Result of interpretation. |
| **misconception_id** | String (optional) | If incorrect or ambiguous, which catalog misconception was matched. |
| **affected_unit_ids** | List of strings (optional) | Units for which the misconception was (or may be) activated. |

---

## 6. Knowledge State Update Records

**Event type:** `knowledge_state_update`

**Purpose:** Record a change to the knowledge state so that “state before” and “state after” are traceable. Supports “teaching → state change” and “correction → unlearning,” “relearning → learned.”

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id for this state update. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When the update was applied. |
| **domain** | String | Domain. |
| **trigger** | String or enum | What caused the update: e.g. teaching_event_id, correction_event_id, evaluation_result, relearning_event_id. |
| **unit_ids** | List of strings | Which units were updated. |
| **state_before** | Snapshot or per-unit (status, active_misconceptions) | State of affected units before update. Can be full snapshot or diff. |
| **state_after** | Snapshot or per-unit | State of affected units after update. |
| **evidence_source** | String (optional) | E.g. teaching_event_id, attempt_id. |

Implementations may log a full state snapshot periodically and log diffs (unit_id, field, old_value, new_value) for each update to reduce size while keeping reconstructability.

---

## 7. Learner Dialogue Records

**Event type:** `learner_dialogue`

**Purpose:** Record the TA’s conversational response after teaching. Allows verification that dialogue was produced in the same cycle as the teaching event and that the response can be linked to the state (learned units, active misconceptions) that constrained it.

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id for this dialogue record. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When the response was produced. |
| **domain** | String | Domain. |
| **teaching_event_id** | String | The teaching event this response is to. |
| **learned_unit_ids** | List of strings | Units the TA was allowed to use (from state). |
| **active_misconception_ids** | List of strings (optional) | Misconceptions that were active and should be reflected in response. |
| **response_text** or **response_summary** | String | TA’s response (full or summary for storage). |

---

## 8. Task Selection Records

**Event type:** `task_selection`

**Purpose:** Record which task was selected (or that none was eligible) and why. Supports “state constrains selection” and diagnosis when no task is available.

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When selection occurred. |
| **domain** | String | Domain. |
| **eligible_unit_ids** | List of strings | Units that were learned/eligible at selection time. |
| **selected_task_id** | String or null | The task chosen, or null if none. |
| **eligible_task_ids** | List of strings (optional) | All task ids that were eligible. |
| **ineligible_reasons** | List of { task_id, missing_units } (optional) | For some or all ineligible tasks, why they were not selected. |

---

## 9. TA Attempt Records

**Event type:** `ta_attempt`

**Purpose:** Record the TA’s attempt at a task: output, whether guard passed, whether fallback was used, which misconceptions were applied. Supports “behavior reflects state” and “wrong behavior reflects misconception.”

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** or **attempt_id** | String (unique) | Unique id for this attempt. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When the attempt was produced. |
| **domain** | String | Domain. |
| **task_id** | String | Task attempted. |
| **learned_unit_ids** | List of strings | Units the TA was allowed to use. |
| **active_misconception_ids** | List of strings (optional) | Misconceptions applied to this attempt. |
| **output_summary** or **output_ref** | String | TA output (full or reference to stored artifact). |
| **guard_passed** | Boolean | Whether the Guard/Fallback Layer accepted the output. |
| **fallback_used** | Boolean | Whether fallback output was returned instead of generator output. |

---

## 10. Evaluation Records

**Event type:** `evaluation_result`

**Purpose:** Record the result of evaluating the TA’s attempt (pass/fail, mastery change). Supports “state → behavior → outcome” and mastery trajectory.

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When evaluation was done. |
| **domain** | String | Domain. |
| **task_id** | String | Task that was attempted. |
| **attempt_id** | String | Links to ta_attempt. |
| **pass_fail** | Boolean | Whether the attempt passed the task’s criteria. |
| **unit_ids_tested** | List of strings | Units this task tested. |
| **mastery_level_before** | Per-unit or overall (optional) | Mastery level(s) before this attempt. |
| **mastery_level_after** | Per-unit or overall (optional) | Mastery level(s) after this attempt. |
| **misconception_active_during_attempt** | String or null (optional) | If a misconception was active and may explain failure. |

---

## 11. Misconception Activation / Correction / Relearning Records

**Event type:** `misconception_activation`

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When activated. |
| **domain** | String | Domain. |
| **unit_id** | String | Unit(s) affected (can repeat for multiple units). |
| **misconception_id** | String | Catalog misconception id. |
| **trigger** | Enum or string | incorrect_teaching | ambiguous_teaching | pre_seeded | transfer_from_unit. |
| **teaching_event_id** or **trigger_reference** | String (optional) | Link to teaching event or other trigger. |

**Event type:** `correction_event` (unlearning)

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When correction was applied. |
| **domain** | String | Domain. |
| **unit_id** | String | Unit corrected. |
| **misconception_id** | String | Misconception that was unlearned. |
| **trigger** | String or enum | e.g. student_reteaching, explicit_correction_event. |
| **teaching_event_id** (optional) | String | If correction came from teaching. |
| **state_before** | Status | e.g. misconception. |
| **state_after** | Status | e.g. corrected. |

**Event type:** `relearning_event`

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** or **relearning_event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When relearning was recorded. |
| **domain** | String | Domain. |
| **unit_id** | String | Unit that was relearned. |
| **type** | Enum | teaching | successful_task. |
| **state_after** | Status | e.g. learned. |
| **reference_id** (optional) | String | teaching_event_id or attempt_id. |

---

## 12. Mastery Update Records

**Event type:** `mastery_update`

**Purpose:** Record when mastery_level or mastery_history was updated for a unit (or overall). Can be embedded in evaluation_result or emitted separately when the Knowledge State Engine or Mastery Evaluator updates mastery_history.

**Minimum trace fields:**

| Field | Type | Purpose |
|-------|------|--------|
| **event_id** | String (unique) | Unique id. |
| **timestamp** or **sequence_id** | Timestamp or monotonic id | When mastery was updated. |
| **domain** | String | Domain. |
| **unit_id** (optional) | String | Unit; omit for overall mastery. |
| **mastery_level** | Enum | not_assessed | failing | developing | proficient (optional: mastered). |
| **pass_rate** (optional) | Numeric | Pass rate at this update. |
| **attempt_count** (optional) | Integer | Number of attempts in the computation. |
| **trigger** (optional) | String | attempt_id or evaluation_result id. |

---

## 13. Cross-Domain Traceability

Traces from different domains must be comparable and combinable for cross-domain evaluation and dashboards.

- **Domain field:** Every event type must include `domain` so that filters and analyses can restrict to one domain or compare across domains.
- **Shared event schema:** The same event types and minimum fields are used in every domain. Domain-specific extensions (e.g. extra fields for Python code snippets) are optional and must not replace the minimum fields.
- **Session and run identity:** Optional `session_id` or `run_id` allows grouping events from one student session or one demo run across domains. Cross-domain mastery comparison then uses the same session/run and same rubric semantics (from the shared Mastery Evaluator).
- **Ordering:** `timestamp` or `sequence_id` must allow ordering events within a domain and within a session so that “teaching before attempt” and “correction before relearning” are unambiguous.

---

## 14. How Trace Supports Evaluation

The trace layer enables evaluation to demonstrate the following.

- **Teaching → state change:** For each teaching event, there is a teaching_event and a knowledge_state_update with the same trigger; state_before and state_after show the transition (e.g. unknown → learned, or learned → misconception). Teaching_interpretation links incorrect teaching to misconception_activation.

- **State → behavior:** For each task attempt, ta_attempt shows learned_unit_ids and active_misconception_ids; evaluation_result shows pass_fail. Analysis can verify that when a misconception was active, the attempt failed (or produced misconception-consistent wrong output) and that when the unit was learned and no misconception active, the attempt could pass.

- **State → selection:** task_selection shows eligible_unit_ids and selected_task_id (or null). Evaluation can verify that only tasks whose required units are in the eligible set were selected and that when units were missing, no task (or only eligible tasks) were offered.

- **Mastery trajectory:** evaluation_result and mastery_update (or mastery_history in state) give a time-series of mastery levels per unit. Evaluation can show “mastery improved after teaching” and “mastery dropped when misconception was active, then improved after correction and relearning.”

- **Full chain:** By joining teaching_event → teaching_interpretation → knowledge_state_update → learner_dialogue → task_selection → ta_attempt → evaluation_result → (optional) misconception_activation → correction_event → relearning_event → mastery_update, evaluation can produce evidence that the system behaves as claimed: teaching drives state, state drives behavior and selection, behavior is evaluated, and misconception lifecycle is recorded.

- **Distinguishing cases (see §15):** Trace allows the evaluator to distinguish never learned, partially learned, learned wrongly, corrected, relearned, succeeded because of teaching, failed because of missing knowledge, and failed because of misconception by querying the sequence of state updates, attempt metadata, and evaluation results.

---

## 15. How Trace Supports Diagnosis of Weak Teaching vs Active Misconception

Trace supports diagnosis (for the student, teacher, or researcher) in these ways.

- **Never learned:** Unit has no teaching_event (or only events that did not target it); state remains unknown; task_selection shows the unit in missing_units for some tasks. No misconception_activation for this unit.

- **Partially learned:** Unit has teaching_evidence but status is partially_learned; optional low confidence. Task may or may not be selected depending on policy; if attempted, pass_fail may be mixed. No active misconception.

- **Learned wrongly:** misconception_activation exists for the unit; state is misconception; active_misconception_ids appear in learner_dialogue and ta_attempt. evaluation_result shows pass_fail = false and optionally misconception_active_during_attempt. So: “TA failed because it holds a specific misconception,” not because it never learned.

- **Corrected:** correction_event exists for the unit and misconception_id; state_after = corrected. So: “TA no longer holds that misconception but has not yet been reinforced.”

- **Relearned:** relearning_event(s) exist after correction_event; state_after = learned. So: “TA was wrong, was corrected, and then relearned correctly.”

- **Succeeded because of teaching:** teaching_event(s) for the unit with interpretation = correct; knowledge_state_update shows state_after = learned; a subsequent ta_attempt for a task that tests the unit has pass_fail = true and no misconception active. So: “Teaching led to learned state and to successful performance.”

- **Failed because of missing knowledge:** task_selection shows the unit in missing_units for the task (task not selected), or the task was selected but the unit was not in learned_unit_ids at attempt time; no misconception_activation. So: “TA failed or could not attempt because it had not been taught.”

- **Failed because of misconception:** misconception_activation for the unit; ta_attempt has that misconception in active_misconception_ids; evaluation_result pass_fail = false and misconception_active_during_attempt = that misconception. So: “TA failed because of a specific wrong belief, not because of no teaching.”

These distinctions are only possible if the trace records teaching events, interpretation, state updates, task selection, attempt metadata (learned units, active misconceptions), evaluation results, and misconception lifecycle events with the minimum fields above.

---

## 16. Risks of Weak Trace Design

- **Missing event types:** If teaching_interpretation or misconception_activation or correction_event are not recorded, the chain “wrong teaching → misconception → wrong behavior → correction → relearning” cannot be reconstructed; the misconception lifecycle claim is not evaluable.

- **Missing links:** If attempt_id is not stored in evaluation_result (or task_id/attempt_id not in mastery_update), joins between attempt, evaluation, and mastery are broken. Every event that references another (e.g. teaching_event_id, attempt_id) must store the reference.

- **No state before/after:** If knowledge_state_update does not record state_before and state_after, evaluation cannot show “teaching caused this state change” or “correction caused unlearning.”

- **Domain-specific trace formats:** If each domain logs different fields or different event names, cross-domain analysis and shared evaluation scripts become impossible. Minimum fields must be shared.

- **Trace as an afterthought:** If trace is added late or only for “important” events, historical runs and demos will lack the data needed for the paper. Trace integration points must be part of the architecture from the start (see SHARED_CORE_ARCHITECTURE.md §12).

---

## 17. Trace Design Guardrails

- **Every event type in §3 must be recordable.** No engine may skip its integration point; at least the minimum fields for its events must be written (or delegated to a central logger that receives the same payload).

- **Minimum fields are mandatory.** Implementations may add optional fields (e.g. full output text, full state snapshot) but must not omit the minimum fields listed in §§4–12. Evaluation and diagnosis depend on them.

- **Same schema across domains.** The event type names and minimum field sets are shared. Domain-specific extensions are optional and additive.

- **Trace does not replace state.** The knowledge state remains the source of truth for “what the TA knows.” Trace is a log of what happened; it is used for evaluation and diagnosis, not for driving the next step of the cycle (which is driven by the current state).

- **Ordering and identity.** Every event must have a unique event_id (or equivalent) and a timestamp or sequence_id so that ordering and deduplication are possible. References (teaching_event_id, attempt_id, task_id) must be stable and consistent across events.

---

## 18. Conclusion

The Trace and History Layer defines which events are recorded (teaching, interpretation, state update, dialogue, task selection, attempt, evaluation, misconception activation, correction, relearning, mastery update), the minimum fields for each, and how trace supports evaluation and diagnosis. With this layer, the project can demonstrate the full chain teaching → state change → behavior → testing → mastery → correction → relearning and can distinguish never learned, partially learned, learned wrongly, corrected, relearned, succeeded because of teaching, failed because of missing knowledge, and failed because of misconception. Together with the Shared Core Architecture, the unified knowledge state schema, and the unlearning/relearning engine, the trace design ensures that the main claim is not only implemented but **evidenced** for papers and for future improvement.
