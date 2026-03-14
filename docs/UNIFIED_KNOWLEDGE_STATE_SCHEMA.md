# Unified Knowledge State Schema

**Document type:** Shared core design — single schema governing all domains  
**Governing document:** MASTER_SYSTEM_BLUEPRINT.md  
**Alignment:** §2 Main Claim and Claim Stack; §10 Negative Scope; §11 Unified Knowledge State Logic; §12 Misconception, Unlearning, and Relearning Logic; §16 Evaluation Logic; §19 Non-Negotiable Design Guardrails; §21 Evidence Map; §23 Blueprint Alignment Checks  
**Status:** Binding schema for all later domain work (Python, Database, AI Literacy)

---

## 1. Purpose of the Unified Knowledge State Schema

The unified knowledge state schema is the single data model that represents what the Teachable Agent (TA) knows, misunderstands, has been taught, has failed on, has corrected, and has relearned — across all domains. It is not a convenience layer or an optional annotation. It is the **structural core** that makes the system a teachable agent rather than a chatbot: every component that needs to know “what does the TA know?” must query this schema. The schema exists so that learner dialogue, task eligibility, TA attempt generation, mastery evaluation, misconception effects, and relearning tracking all share one source of truth. Without a unified schema, the project’s main claim — a single framework operating across Python, Database, and AI Literacy with comparable mastery and traceable state — cannot be sustained.

---

## 2. Why a Shared Schema Is Necessary

The project’s contribution is not “we support three domains.” It is that **one framework** (one state model, one misconception lifecycle, one evaluation chain) operates across structurally different domains. If each domain used a different state format, cross-domain mastery comparison would require ad-hoc translation; task selection, attempt generation, and mastery computation would each need domain-specific branches; and the evaluation chain (teaching → state change → behavior → mastery) could not be traced in a single, comparable way. A shared schema ensures that:

- **Dialogue control** uses the same notion of “learned” and “misconception-affected” in every domain.
- **Task eligibility** is determined by the same rule: only tasks whose required knowledge units are in an eligible state (learned or partially_learned, with domain-agnostic semantics).
- **TA attempt generation** receives the same state shape (learned units, active misconceptions, correction/relearning history) regardless of whether the output is code, a query, or an explanation.
- **Mastery evaluation** consumes the same evidence structures (teaching, testing, correction, relearning) so that “proficient in Python loops” and “proficient in SQL joins” are computed by the same rubric logic.
- **Misconception effects** are represented uniformly so that the misconception/unlearning/relearning engine can operate without domain-specific conditionals in the core.

The Python Stage One prototype already uses a minimal state (unit_id → status: unknown | partially_learned | learned). The unified schema extends that foundation with the fields required for misconception lifecycle, evidence tracing, and cross-domain comparability — without abandoning the proven status model.

---

## 3. Core Design Principles

1. **Single source of truth.** No component may determine the TA’s behavior by querying the LLM’s inherent knowledge, raw conversation history, or any store other than the knowledge state. The schema is the only authority for “what the TA knows.”

2. **Domain-agnostic structure, domain-specific content.** The schema defines the same fields and value types for every domain. Domain-specific variation is confined to the *content* of those fields (e.g., which knowledge_unit_ids exist, which misconception_ids exist), not to the presence or meaning of the fields themselves.

3. **Evidence-carrying.** The schema does not only record current status; it carries sufficient evidence (teaching events, test attempts, corrections, relearning events) to support the evaluation chain: teaching action → state change → behavior change → mastery outcome. Implementation can store evidence in the same structure or in linked stores keyed by the schema’s identifiers; the logical model is that the schema defines what evidence exists and how it is referenced.

4. **Misconception as first-class.** Misconceptions are not tags or metadata; they are represented in the schema with activation time, trigger, and linkage to correction and relearning. The schema must support the full lifecycle: activation → behavior → correction → unlearning → relearning.

5. **Inspectable and traceable.** Every field that affects eligibility, generation, or mastery must be explicitly present so that evaluation and debugging can trace why the TA behaved as it did. No implicit or hidden state.

---

## 4. Required Global Fields

The **global** (system- or session-level) view of the knowledge state includes:

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **domain** | Enum or identifier: e.g. `python`, `database`, `ai_literacy` | Scopes all knowledge units and evidence to one domain. Enables cross-domain aggregation (e.g. “mastery summary across domains”) while keeping per-domain state separate. |
| **schema_version** | String (e.g. `"1.0"`) | Allows future schema evolution without breaking existing traces or stored state. |
| **last_updated** | Timestamp (or logical sequence id) | Indicates when the state was last modified. Used for ordering events, cache invalidation, and trace ordering. |

These global fields apply to the state as a whole (e.g. one “state document” per domain, or one document with a top-level `domains` map keyed by domain). They ensure that later architecture can support multi-domain sessions and cross-domain dashboards without redefining the schema.

---

## 5. Required Per-Knowledge-Unit Fields

For **each knowledge unit** (e.g. `variable_assignment`, `select_statement`, `supervised_learning`), the schema must include the following. All are required in the sense that the shared engines assume they exist; implementations may use defaults (e.g. empty list, zero confidence) where appropriate.

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **knowledge_unit_id** | String, unique within domain | Stable identifier for the unit. Comes from the domain’s knowledge-unit definitions. |
| **knowledge_unit_name** | String | Human-readable name. Used in dialogue, reports, and debugging. |
| **status** | Enum: see below | Primary indicator of “what the TA knows” for this unit. Drives eligibility and generation. |
| **confidence** | Numeric in [0.0, 1.0] | System’s estimate of how solidly the unit is learned. Rises with consistent correct teaching and successful tests; falls with contradictory teaching, failures, or active misconceptions. Used for tie-breaking, reporting, and optionally for partial eligibility. |
| **active_misconceptions** | List of misconception records (see §6) | Misconceptions currently affecting this unit. Drives TA behavior (dialogue and task attempts). Empty when none are active. |
| **teaching_evidence** | List of teaching evidence records (see §7) | All teaching events that targeted this unit. Supports “when and how was the TA taught?” for evaluation. |
| **testing_evidence** | List of testing/task evidence records (see §8) | All task attempts that involved this unit. Supports mastery computation and “what did the TA do?” for evaluation. |
| **correction_evidence** | List of correction evidence records (see §9) | Corrections of misconceptions that affected this unit. Supports unlearning and relearning logic. |
| **relearning_evidence** | List of relearning evidence records (see §9) | Post-correction teaching and testing that re-established correct understanding. Distinguishes first-time learning from relearning. |
| **mastery_history** | List of mastery history entries (see §10) | Time-series of mastery levels for this unit. Supports “improving / stable / regressing” and evaluation. |
| **last_updated** | Timestamp or sequence id | When this unit’s state was last changed. Used for ordering and traces. |

**Status values (required enum):**

- **unknown** — The TA has never been taught this unit (or has been reset). No teaching evidence, or only evidence that was later invalidated.
- **partially_learned** — The TA has received some teaching but not enough for confident “learned” (e.g. one brief teaching event, or contradictory signals). The TA may use this unit under constrained conditions; domain and rubric can define whether partially_learned units are eligible for tasks.
- **learned** — The TA has been taught and has demonstrated understanding (via conversation and/or tests). This is the normal “can use this concept” state.
- **misconception** — The TA has acquired an incorrect understanding; at least one misconception is active and dominates. Behavior should reflect the misconception(s).
- **corrected** (or **partially_learned_post_correction**) — The TA previously held a misconception that was corrected; it has not yet accumulated enough relearning evidence to return to **learned**. Transitional state between unlearning and relearning.
- **unstable** (optional but recommended) — Reserved for states where the unit has received conflicting teaching or repeated failures after correction; confidence is low and status may be in flux. Can be used to require extra reinforcement before counting as learned.

The schema does not prescribe a single “correct” enum set for all time; it requires that the **semantics** above are representable. Implementations may collapse or extend (e.g. merge `corrected` with `partially_learned` with a flag, or add `relearned`) as long as eligibility and generation logic can distinguish “can use correctly,” “using with misconception,” and “post-correction, not yet relearned.”

---

## 6. Misconception Representation in the Schema

For each **active** misconception on a knowledge unit, the schema holds a **misconception record** (or reference plus activation metadata). This is distinct from the domain’s misconception *catalog* (which defines what misconceptions exist and their remediation hints). The state holds *activation* and *lifecycle* data.

Per active misconception, the schema must represent:

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **misconception_id** | String (matches catalog id) | Which misconception (e.g. `off_by_one_range`, `null_equality`, `ai_understands_meaning`). |
| **activated_at** | Timestamp or sequence id | When this misconception was activated. |
| **trigger** | Enum or string: e.g. `incorrect_teaching`, `ambiguous_teaching`, `pre_seeded`, `transfer_from_unit` | How the misconception entered the state. Supports evaluation (“wrong teaching led to wrong behavior”). |
| **trigger_reference** | Optional id (e.g. teaching_event_id) | Links to the teaching event or seed that caused activation. |
| **flagged_for_correction** | Boolean | Whether the student (or system) has indicated that correction is in progress or requested. Can drive dialogue or UI. |

When a misconception is **unlearned**, it is removed from `active_misconceptions` and its lifecycle is recorded in **correction_evidence** and **relearning_evidence** (see §9). The schema does not keep “inactive” misconceptions in the active list; history is in evidence.

---

## 7. Teaching Evidence Representation

Each teaching event that targets a knowledge unit must be recorded so that the evaluation chain can trace “teaching action → state change.”

Per teaching evidence entry:

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **teaching_event_id** | String (unique per event) | Links to the global teaching event. |
| **timestamp** (or **sequence_id**) | Timestamp or monotonic id | When the teaching occurred. |
| **topic_taught** | String (optional) | Human-readable topic from the event. |
| **knowledge_units_taught** | List of unit ids | Units that this event claimed to teach (may include this unit). |
| **state_before** | Status (or snapshot id) | Status of this unit before this event. |
| **state_after** | Status | Status of this unit after this event. |
| **misconception_activated** | Optional misconception_id | If this teaching activated a misconception on this unit, which one. |
| **note** | Optional string | Free text or structured note from the event. |

This supports: “Show all teaching that affected unit X,” “Did wrong teaching precede misconception Y?,” and “When did the TA transition from unknown to learned for X?”

---

## 8. Testing and Task Evidence Representation

Each task attempt that involves a knowledge unit must be recorded so that mastery can be computed and the evaluation chain can trace “state → behavior → outcome.”

Per testing evidence entry (per knowledge unit; one attempt may generate one entry per unit involved):

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **task_id** (or **problem_id**) | String | Identifies the task. |
| **attempt_id** | String (unique per attempt) | Identifies the attempt for linking to TA output and grader result. |
| **timestamp** (or **sequence_id**) | Timestamp or monotonic id | When the attempt occurred. |
| **pass_fail** | Boolean or enum (pass / fail) | Whether the TA’s output met the task’s evaluation criteria. |
| **mastery_level_at_attempt** | Optional enum (e.g. failing, developing, proficient) | Mastery level computed for this unit at or after this attempt (for history). |
| **ta_output_summary** | Optional string or reference | Short summary or reference to the TA’s output (e.g. code snippet, query, or explanation id). Supports “what did the TA do?” in evaluation. |
| **misconception_active_during_attempt** | Optional misconception_id | If a misconception was active and may have caused the failure. |

This supports: pass-rate aggregation per unit, “trajectory of mastery over time,” and “failed attempts that coincided with misconception M.”

---

## 9. Correction, Unlearning, and Relearning Evidence Representation

**Correction evidence** records the moment when a misconception was corrected (unlearned).

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **misconception_id** | String | Which misconception was corrected. |
| **corrected_at** | Timestamp or sequence id | When the correction was recorded. |
| **trigger** | Enum or string: e.g. `student_ret teaching`, `explicit_correction_event` | What triggered the correction. |
| **teaching_event_id** (or similar) | Optional string | Link to the teaching event that delivered the correction. |
| **state_before** | Status | Unit status before correction (e.g. misconception). |
| **state_after** | Status | Unit status after correction (e.g. corrected or partially_learned_post_correction). |

**Relearning evidence** records post-correction teaching and/or successful testing that re-establishes correct understanding.

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **relearning_event_id** | String | Identifies the relearning event (teaching or test). |
| **timestamp** (or **sequence_id**) | Timestamp or monotonic id | When the event occurred. |
| **type** | Enum: e.g. `teaching`, `successful_task` | Whether relearning came from teaching or from a passed task. |
| **state_after** | Status | Unit status after this relearning step (e.g. back to learned). |

Together, correction and relearning evidence support: “The TA held misconception M, was corrected at time T1, and reached learned again at T2 after two teaching events and one passed task.” This is required for the misconception lifecycle to be observable and evaluable.

---

## 10. Mastery History Representation

**Mastery history** is a time-series of mastery levels for the unit, computed from testing evidence (and optionally from rubric rules that consider correction/relearning).

Per mastery history entry:

| Field | Type / semantics | Purpose |
|-------|-------------------|--------|
| **timestamp** (or **sequence_id**) | Timestamp or monotonic id | When this mastery level was computed or recorded. |
| **mastery_level** | Enum: e.g. not_assessed, failing, developing, proficient (and optionally mastered) | The level at that time. |
| **pass_rate** (optional) | Numeric in [0.0, 1.0] | Pass rate over attempted tasks for this unit at that time. |
| **attempt_count** (optional) | Integer | Number of attempts included in the computation. |

The shared rubric (see MASTER_SYSTEM_BLUEPRINT and mastery-rubric-stage1.md) defines how pass_rate maps to mastery_level. The schema only requires that the history can store the outcome of that computation over time so that “improving / stable / regressing” and “mastery after correction” are visible.

---

## 11. Domain Layer vs Shared Layer

- **Shared layer (schema):** The *structure* of the state — which fields exist, what they mean, how they relate to dialogue, task eligibility, TA generation, and mastery — is defined once and is the same for Python, Database, and AI Literacy. All shared engines (Knowledge State Engine, Misconception/Unlearning/Relearning Engine, Mastery Evaluator, Task Engine, TA Attempt Engine, Learner Dialogue Engine) consume and produce data that conforms to this schema.

- **Domain layer (content):** The *content* is domain-specific: the set of `knowledge_unit_id`s, their names, descriptions, prerequisites, and topic groups; the set of `misconception_id`s and their affected units, examples, and remediation hints; the task bank and evaluation criteria. The schema does not define “what is variable_assignment” or “what is off_by_one_range”; the domain’s knowledge-unit and misconception catalogs do. The schema defines that each unit has `status`, `active_misconceptions`, `teaching_evidence`, etc., and that the engines use those fields uniformly.

Implementations may store the schema in one document per domain, in a single document with a `domains` map, or in normalized tables keyed by (domain, knowledge_unit_id); the logical model is that the same field set exists per unit in every domain.

---

## 12. Example Schema Instance: Python

For the Python domain, after one teaching event (“Variables and print”) and one successful task:

- **domain:** `python`
- **schema_version:** `"1.0"`
- **last_updated:** &lt;timestamp&gt;

Per unit (illustrative for `variable_assignment` and `print_function`):

- **knowledge_unit_id:** `variable_assignment`
- **knowledge_unit_name:** `Variables and Assignment`
- **status:** `learned`
- **confidence:** e.g. `0.85`
- **active_misconceptions:** `[]`
- **teaching_evidence:** one entry (event “Variables and print”, state_before unknown, state_after learned)
- **testing_evidence:** one entry (e.g. task `prob_var_001`, pass, proficiency at attempt)
- **correction_evidence:** `[]`
- **relearning_evidence:** `[]`
- **mastery_history:** one entry (proficient, pass_rate 1.0, attempt_count 1)
- **last_updated:** &lt;timestamp&gt;

For a unit that has been through a misconception cycle (e.g. `for_loop_range` with `off_by_one_range` corrected):

- **status:** e.g. `corrected` or `partially_learned_post_correction` (before further relearning) or `learned` (after relearning)
- **active_misconceptions:** `[]` (misconception moved to correction_evidence)
- **correction_evidence:** one entry (misconception_id `off_by_one_range`, state_before misconception, state_after corrected)
- **relearning_evidence:** one or more entries (teaching and/or successful task)

---

## 13. Example Schema Instance: Database

For the Database domain, the same field set applies. Content differs:

- **domain:** `database`
- **knowledge_unit_id:** e.g. `select_statement`, `where_clause`, `null_handling`
- **knowledge_unit_name:** e.g. `SELECT Statement`, `WHERE Clause`, `NULL Handling`
- **status,** **confidence,** **active_misconceptions,** **teaching_evidence,** **testing_evidence,** **correction_evidence,** **relearning_evidence,** **mastery_history,** **last_updated** — all present with the same semantics. Testing evidence references task_ids from the Database task bank; pass_fail is determined by query result-set comparison or rubric, not by stdout.

Example with active misconception:

- **knowledge_unit_id:** `null_handling`
- **status:** `misconception`
- **active_misconceptions:** one record (misconception_id `null_equality`, activated_at, trigger incorrect_teaching)

---

## 14. Example Schema Instance: AI Literacy

For the AI Literacy domain:

- **domain:** `ai_literacy`
- **knowledge_unit_id:** e.g. `supervised_learning`, `bias_in_data`, `ai_understands_meaning` (if a unit)
- Same field set: **status,** **confidence,** **active_misconceptions,** **teaching_evidence,** **testing_evidence,** **correction_evidence,** **relearning_evidence,** **mastery_history,** **last_updated**. Testing evidence records pass_fail from explanation/scenario tasks evaluated by rubric (or LLM-assisted evaluation). TA output is explanations or scenario analyses, not code or SQL.

---

## 15. How the Schema Governs System Behavior

The schema is not passive storage. It **governs** behavior in the following ways.

- **Learner dialogue control:** The Learner Dialogue Engine receives the current state (per domain): learned units, partially_learned units, active misconceptions. It must constrain responses to concepts the TA “knows” (learned or partially_learned) and may express misconceptions when the unit is misconception-affected. The schema defines what “learned” and “misconception-affected” mean so that the same logic applies in every domain.

- **Task / problem selection:** The Task Engine selects tasks whose required knowledge units are all in an **eligible** state (learned or partially_learned, and not blocked by policy). Eligibility is a function of `status` (and optionally `confidence` and `active_misconceptions`). The schema’s `status` and unit set are the only inputs; no domain-specific branch is needed in the selection rule.

- **TA code / query / response generation:** The TA Attempt Engine receives learned units and active misconceptions from the state. It generates code (Python), queries (Database), or explanations (AI Literacy) using only learned units and injecting misconception-driven errors where active. The schema’s `active_misconceptions` and `status` drive what is passed into prompts and guards; the same shape is used in all domains.

- **Mastery computation:** The Mastery Evaluator aggregates `testing_evidence` (pass_fail, attempt counts) per unit and optionally applies rubric rules (e.g. weight recent attempts, or down-weight attempts during active misconception). It writes back `mastery_history` and may update `status` or `confidence`. The schema defines where evidence lives so that the same aggregation logic runs on the same structure in every domain.

- **Misconception-triggered errors:** When `active_misconceptions` is non-empty for a unit, the misconception engine (and TA Attempt Engine) use it to produce wrong-but-consistent output. The schema ensures that “which misconception” and “for which unit” are explicit, so that correction and unlearning can target the right misconception.

- **Fallback and guard behavior:** Guards verify that TA output does not use untaught concepts and, where applicable, that misconception-driven output is consistent with the active misconception. The schema’s learned set and active_misconceptions are the inputs to those checks; no separate “shadow” state is allowed.

If any component bypasses the schema (e.g. uses raw conversation or LLM memory to decide what the TA “knows”), the system’s educational validity and the main claim are compromised. The schema is the contract that keeps the contribution (unified, state-constrained, misconception-aware framework) intact.

---

## 16. What Must Never Be Left Outside the Schema

The following must be represented *inside* the unified knowledge state (or in stores keyed by schema identifiers); they must not exist only in conversation history, logs, or undocumented caches:

- Current **status** and **confidence** for every knowledge unit.
- **Active misconceptions** (id, activation time, trigger) for every unit that has them.
- **Teaching evidence** sufficient to trace which teaching events changed which units and to what status.
- **Testing evidence** sufficient to compute pass rates and mastery history per unit.
- **Correction evidence** and **relearning evidence** sufficient to trace unlearning and relearning and to support “never learned” vs “learned wrongly then corrected.”
- **Mastery history** sufficient to show trajectory over time and to support evaluation (e.g. “mastery after correction”).

Anything that affects “what the TA can do” or “what the TA did” must be derivable from the schema (or its referenced evidence). Otherwise, evaluation cannot trace teaching → state → behavior → mastery, and the framework claim is weakened.

---

## 17. Risks of a Weak or Incomplete Schema

- **Fragmented state:** If dialogue, tasks, and mastery use different notions of “learned” or store evidence in incompatible forms, cross-domain comparison and shared engines become impossible; the project drifts toward “three separate systems.”

- **Misconception as afterthought:** If misconceptions are only in a catalog and not in the state (with activation and correction/relearning evidence), the misconception lifecycle cannot be implemented or evaluated; the main claim’s distinguishing feature is lost.

- **No correction/relearning trace:** If the schema does not distinguish first-time learning from post-correction relearning, the system cannot support “relearning may be fragile” or “mastery recalculation after correction,” and evaluation cannot distinguish “never learned” from “learned wrongly then corrected.”

- **Implicit or hidden state:** If eligibility or generation depend on state that is not in the schema (e.g. “last three messages”), the system is no longer a single-source-of-truth teachable agent; guards and evaluation cannot be trusted.

---

## 18. Schema Design Guardrails

- **Do not add domain-only fields to the shared schema.** Domain-specific data (e.g. “preferred SQL dialect”) belongs in the domain layer or in optional, domain-keyed extensions that do not affect shared engine logic.

- **Do not remove or weaken evidence fields.** Teaching, testing, correction, and relearning evidence are required for the evaluation chain and for the misconception lifecycle. Shortcuts (e.g. “we only store last status”) undermine traceability.

- **Do not make “learned” mean something different per domain.** The semantics of status (unknown, partially_learned, learned, misconception, corrected, etc.) must be shared so that eligibility and generation rules do not branch on domain.

- **Keep the schema implementation-ready.** Prose and field definitions should be precise enough that a later implementation (Python, database, or API) can be built without reinterpreting intent. Avoid vague “could include” without specifying how it affects behavior.

---

## 19. Conclusion

The unified knowledge state schema is the shared backbone for all domain work. It defines what a “knowledge state” is in this project: a per-domain, per-unit structure with status, confidence, active misconceptions, and full evidence for teaching, testing, correction, and relearning, plus mastery history. By keeping this schema single and explicit, the system ensures that learner dialogue, task eligibility, TA attempt generation, mastery evaluation, and misconception effects are all driven by one source of truth, and that the same logic applies across Python, Database, and AI Literacy. Later domain architectures (Python mature, Database, AI Literacy) must plug into this schema; they must not introduce a second, competing state model. This document, together with the Unlearning/Relearning Engine design, forms the shared conceptual core that makes the Teachable Agent for CS framework’s contribution — the mechanism, not the domain count — concrete and implementable.
