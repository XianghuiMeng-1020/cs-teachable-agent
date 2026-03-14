# Stage G Readiness Check

**Document type:** Formal readiness assessment — migration complete gate  
**Governing documents:** MASTER_SYSTEM_BLUEPRINT.md; docs/MIGRATION_STAGE1_TO_SHARED_CORE.md; docs/SHARED_CORE_ARCHITECTURE.md; docs/UNIFIED_KNOWLEDGE_STATE_SCHEMA.md; docs/UNLEARNING_RELEARNING_ENGINE.md; docs/TRACE_AND_HISTORY_LAYER.md  
**Status:** Binding assessment; determines whether the Python prototype is the first shared-core domain instance and whether domain expansion may proceed  
**Date:** 2026-03-14  

---

## 1. Purpose of the Stage G Readiness Check

This document exists to answer, explicitly and with evidence, whether the migrated Python Stage One system is **ready to be treated as the first shared-core domain instance** of the Teachable Agent for CS framework — rather than as a local prototype. Stage G is the gate after migration Stages A through F: it is the moment at which the team must decide whether the architecture and implementation are strong enough to support (1) the main claim in the blueprint (unified, knowledge-state-constrained, misconception-aware, unlearning/relearning-capable framework), and (2) safe expansion to additional domains (Database, AI Literacy) without re-engineering the core. Readiness must be checked before domain expansion because starting Database or AI Literacy on a partially migrated or unclear foundation would duplicate logic, weaken the “one framework” claim, and increase the cost of later refactoring. This check is not a celebration of completion; it is a **rigorous, evidence-based judgment** of what is satisfied, what is partial, and what remains missing.

---

## 2. Scope of What Is Being Assessed

This readiness check assesses **only** the following:

- **The migrated Python Stage One system** — the codebase as it exists after the migration path defined in docs/MIGRATION_STAGE1_TO_SHARED_CORE.md (Stages A through F).
- **Alignment with the shared-core architecture** — whether the Knowledge State Engine, Interaction Engine, Learner Dialogue Engine, Task Engine, TA Attempt Engine, Mastery Evaluator, Misconception/Unlearning/Relearning Engine, Guard/Fallback Layer, and Trace/History Layer are present and used in the intended order and with the intended contracts.
- **State schema, trace, misconception lifecycle, relearning, and mastery migration** — whether the unified knowledge state schema is implemented, trace events are written with the required minimum fields, misconception activation/correction/relearning are operational, and mastery is persisted in state and aggregated.

**Out of scope for this check:**

- UI, deployment, product polish, or infrastructure.
- Natural-language teaching interpretation.
- Database or AI Literacy domain implementation.
- Cross-session or cross-run persistence (e.g. database or file-backed state).
- Any new feature or new domain not already implied by the migration design.

---

## 3. Stage G Readiness Criteria

The following criteria are reconstructed from docs/MIGRATION_STAGE1_TO_SHARED_CORE.md §11 (Readiness Criteria for Post-Migration Architecture), docs/SHARED_CORE_ARCHITECTURE.md, docs/TRACE_AND_HISTORY_LAYER.md, and MASTER_SYSTEM_BLUEPRINT.md. They are the conditions that must hold for the team to say “the Python prototype has been successfully migrated into the shared-core architecture.”

| # | Criterion | Source |
|---|-----------|--------|
| **R1** | **State schema.** The knowledge state conforms to the full per-unit schema (status, confidence, active_misconceptions, teaching_evidence, testing_evidence, correction_evidence, relearning_evidence, mastery_history, last_updated) and global fields (domain, schema_version). The Knowledge State Engine exposes get_learned_units, get_eligible_units, get_active_misconceptions, and state-update APIs for teaching, misconception activation, unlearning, and relearning. | MIGRATION §11.1; UNIFIED_KNOWLEDGE_STATE_SCHEMA |
| **R2** | **Trace complete.** All event types in TRACE_AND_HISTORY_LAYER.md are recorded with minimum fields (teaching_event, knowledge_state_update, learner_dialogue, task_selection, ta_attempt, evaluation_result, misconception_activation, correction_event, relearning_event, mastery_update). The chain teaching → state change → behavior → testing → mastery → correction → relearning can be reconstructed from the trace. | MIGRATION §11.2; TRACE_AND_HISTORY_LAYER |
| **R3** | **Misconception lifecycle operational.** Misconception activation (from incorrect/ambiguous teaching or explicit hook), correction detection, unlearning transition (status → corrected, correction_evidence), and relearning (relearning_evidence, status → learned when policy met) are implemented and observable in state and trace. Scenario C (or equivalent) can be run using state-driven misconception activation; a full cycle including correction and relearning is runnable (e.g. Scenario D). | MIGRATION §11.3; UNLEARNING_RELEARNING_ENGINE |
| **R4** | **Mastery in state.** Mastery Evaluator writes pass/fail and mastery levels into the knowledge state (mastery_history); the report is derived from state. Multi-attempt aggregation (within a run or across persisted runs) follows the shared rubric. | MIGRATION §11.4; SHARED_CORE §9 |
| **R5** | **Shared-core vs. Domain Layer.** Engines are clearly separated from the Domain Layer. Domain Layer supplies only content (units, misconceptions, tasks) and adapters (evaluation, guard rules, fallback stubs). No engine contains “if domain == Python” (or equivalent) for **core** behavior; domain-specificity is only in adapters and content. | MIGRATION §11.5; SHARED_CORE §13 |
| **R6** | **Interaction Engine.** A single orchestration entry point (e.g. “run one teaching–testing cycle”) calls the engines in the order defined in SHARED_CORE_ARCHITECTURE §14. Scenarios A, B, C (and D) are run by invoking this cycle with the appropriate inputs; no scenario-specific branching inside the engines. | MIGRATION §11.6; SHARED_CORE §5, §14 |
| **R7** | **Preserved behavior.** Scenarios A, B, and C produce the same outcomes as in STAGE_ONE_SCENARIO_EVALUATION.md (A: no eligible problem; B: pass, proficient; C: fail, failing). Guard and fallback behavior are unchanged. Zero-knowledge start and constrained selection are unchanged. | MIGRATION §11.7 |
| **R8** | **Evidence preservation.** The migration does not remove or weaken the evidence that Stage One goals are met; it extends the system so that additional evidence (trace, misconception lifecycle, mastery in state) is available for the full framework claim. | MIGRATION §11.8 |
| **R9** | **Readiness for domain extension.** The architecture is such that adding a second domain would require only new content and a new evaluation adapter (and guard/fallback adapters), not changes to state engine, task engine, or misconception engine **logic**. | MIGRATION Stage F evidence; SHARED_CORE §13 |

---

## 4. Evidence Review: What the Current System Already Demonstrates

The following is a concrete, evidence-based summary of what the current prototype demonstrates through its implementation and scenarios. References are to the actual modules and behavior.

### 4.1 Scenario A (Minimal Learned State)

- **Implementation:** `demo_scenarios.run_scenario_a` calls `run_teaching_and_test(tracker, problems, event, run_attempt=False, activate_misconception=None)`. Teaching event: only `print_function` taught.
- **Evidence:** State after teaching has only `print_function` learned. `get_eligible_problem_ids(problems, learned)` returns an empty set (every problem in the bank requires at least one other unit). `select_problem` returns `None`. Trace: `record_teaching_event`, `record_knowledge_state_update`, `record_learner_dialogue`, `record_task_selection` are called. Outcome matches STAGE_ONE_SCENARIO_EVALUATION.md: no eligible problem; ineligible reasons list missing units per problem.

### 4.2 Scenario B (Success Path)

- **Implementation:** `run_scenario_b` calls `run_teaching_and_test` with `variable_assignment` and `print_function` taught, `run_attempt=True`, no misconception activation.
- **Evidence:** State shows both units learned. Task Engine selects e.g. `prob_var_001`. TA Attempt Engine produces code (stub or LLM with guard); `evaluate_attempt` runs code and returns PASS. `record_attempt_to_state` writes testing_evidence and mastery_history to the state tracker. Trace includes teaching_event, knowledge_state_update, learner_dialogue, task_selection, ta_attempt, evaluation_result, mastery_update. Mastery report shows proficient. Outcome matches evaluation doc: pass, proficient.

### 4.3 Scenario C (Failure Path — State-Driven Misconception)

- **Implementation:** `run_scenario_c` calls `run_teaching_and_test` with the same teaching as B but `activate_misconception={ "unit_id": "variable_assignment", "misconception_id": SCENARIO_C_MISCONCEPTION_ID, "trigger": "scenario_c_demo", ... }`, and `force_fail_problem_ids=None` (no force_fail in run_cycle).
- **Evidence:** After teaching, `activate_misconception_for_unit` is invoked from `run_cycle`; state gains an active misconception for `variable_assignment`. TA Attempt Engine receives `active_mis_for_attempt` from the tracker and passes it to `get_ta_code_attempt`; stub path returns misconception-consistent wrong code. Evaluator reports FAIL. Trace contains `misconception_activation` and evaluation_result with `misconception_active_during_attempt`. Mastery reflects failing. Scenario C no longer relies on `force_fail_problem_ids`; failure is state-driven.

### 4.4 Scenario D (Correction and Relearning)

- **Implementation:** `run_scenario_d` runs (1) teach + activate misconception → first attempt (fail), (2) `run_correction` (explicit correction event), (3) `run_relearning_step` (follow-up teaching), (4) `run_test_only` (second attempt).
- **Evidence:** After correction, state shows `variable_assignment` as `corrected`; `correction_evidence` is populated. After relearning step, `add_relearning_evidence_from_teaching` and `try_relearning_transition` move the unit back to `learned`. Second attempt uses the same task; TA produces correct code (no active misconception); evaluator reports PASS. Trace contains correction_event and relearning_event (via misconception_engine and state updates). Mastery trajectory (failing → proficient after recovery) and aggregated mastery (including policy for excluding/down-weighting during-misconception attempts) are demonstrated in the scenario output and via `get_mastery_history` / `get_aggregated_mastery_for_unit`.

### 4.5 State Schema Expansion (Stage A)

- **Evidence:** `state_tracker.py` — `StateTracker` builds per-unit records with `knowledge_unit_id`, `knowledge_unit_name`, `domain`, `status`, `confidence`, `active_misconceptions`, `teaching_evidence`, `testing_evidence`, `correction_evidence`, `relearning_evidence`, `mastery_history`, `last_updated`. Global: `get_domain()`, `get_schema_version()`, `_last_updated`. APIs: `get_learned_units`, `get_eligible_units`, `get_active_misconceptions`, `get_active_misconception_ids`, `activate_misconception`, `update_after_teaching`, `apply_unlearning`, `append_relearning_evidence`, `try_relearning_transition`, `append_testing_evidence`, `append_mastery_history_entry`, `get_mastery_history`, `get_unit_record`, `get_unit_ids`.

### 4.6 Trace Events (Stage B)

- **Evidence:** `trace_history.py` implements: `record_teaching_event`, `record_knowledge_state_update`, `record_learner_dialogue`, `record_task_selection`, `record_ta_attempt`, `record_evaluation_result`, `record_mastery_update`, `record_misconception_activation`, `record_correction_event`, `record_relearning_event`. Each uses event_id, timestamp/sequence_id, domain, and type-specific minimum fields per TRACE_AND_HISTORY_LAYER.md. `run_cycle.run_teaching_and_test` and `run_correction` / `run_relearning_step` / `run_test_only` call these at the appropriate steps. Trace is in-memory (`get_trace_events()`, `clear_trace()`). **Gap:** `teaching_interpretation` (correct/incorrect/ambiguous + misconception_id) is not recorded; the trace doc marks it as “if used,” and the current system does not implement automatic teaching interpretation — activation is explicit (e.g. scenario parameter).

### 4.7 Misconception Engine (Stages C and D)

- **Evidence:** `misconception_engine.py`: `activate_misconception_for_unit` (calls tracker.activate_misconception, records misconception_activation); `apply_correction` (calls tracker.apply_unlearning, records correction_event); `add_relearning_evidence_from_teaching` (appends relearning_evidence, calls try_relearning_transition, records relearning_event). `state_tracker`: `activate_misconception`, `apply_unlearning`, `append_relearning_evidence`, `try_relearning_transition` with STATUS_CORRECTED and policy (min relearning events). Correction is triggered by explicit correction event in Scenario D; no automatic “teaching that matches remediation” detection yet.

### 4.8 Mastery History and Aggregation (Stage E)

- **Evidence:** `mastery_evaluator.record_attempt_to_state` writes, for each unit tested: `append_testing_evidence` and `append_mastery_history_entry` (attempt_id, problem_id, pass_fail, mastery_level, period: before_misconception | during_misconception | after_correction). `get_mastery_history(unit_id)` and `get_aggregated_mastery_for_unit(tracker, unit_id, include_during_misconception=True|False)` support aggregation and policy for weighting/excluding during-misconception attempts. Report is built from state and attempt result in `build_mastery_report`.

### 4.9 Shared-Cycle Orchestration (Stage F)

- **Evidence:** `run_cycle.py` implements the single cycle: `run_teaching_and_test` (teaching → state update → optional misconception activation → learner dialogue → task selection → TA attempt → evaluation → record_attempt_to_state and trace). `run_correction`, `run_relearning_step`, `run_test_only` support Scenario D. `interaction_engine.py` exposes these as the Interaction Engine facade. Scenarios in `demo_scenarios.py` call only `run_teaching_and_test`, `run_correction`, `run_relearning_step`, `run_test_only` with different parameters; no scenario-specific branching inside run_cycle for engine order or logic.

### 4.10 Guard and Fallback

- **Evidence:** `ta_code_generation.output_guard` rejects code containing forbidden patterns; `get_ta_code_attempt` uses stub on reject or LLM failure. No path returns unvalidated LLM output.

---

## 5. Criterion-by-Criterion Assessment

For each readiness criterion, the assessment is **Satisfied**, **Partially satisfied**, or **Not yet satisfied**, with evidence and limitations.

- **R1 State schema.** **Satisfied.** The state tracker implements the full per-unit schema and global fields (domain, schema_version). All required APIs are present (get_learned_units, get_eligible_units, get_active_misconceptions, update paths for teaching, activation, unlearning, relearning, testing_evidence, mastery_history). Evidence: state_tracker.py `_make_unit_record`, StateTracker methods, and usage in run_cycle and mastery_evaluator. Limitation: none for this criterion.

- **R2 Trace complete.** **Partially satisfied.** All event types except `teaching_interpretation` are implemented and written with the minimum fields from TRACE_AND_HISTORY_LAYER.md. The chain teaching → state update → dialogue → task selection → attempt → evaluation → mastery, plus misconception_activation, correction_event, relearning_event, can be reconstructed from the trace. **Limitation:** teaching_interpretation is not recorded; the system does not yet interpret teaching as correct/incorrect/ambiguous (activation is explicit). The trace doc allows “if used”; for full C4 (evaluation traces the full chain including interpretation), teaching_interpretation would need to be added when interpretation is implemented.

- **R3 Misconception lifecycle operational.** **Satisfied.** Activation (explicit hook or scenario parameter), unlearning (apply_correction → apply_unlearning, status → corrected, correction_evidence), and relearning (add_relearning_evidence_from_teaching, try_relearning_transition → learned) are implemented and observable in state and trace. Scenario C uses state-driven misconception activation (no force_fail_problem_ids). Scenario D runs the full cycle: activate → fail → correct → relearn → pass. **Limitation:** Correction is triggered only by explicit correction event, not by “teaching that matches remediation”; that is acceptable for Stage G as the lifecycle is present and traceable.

- **R4 Mastery in state.** **Satisfied.** record_attempt_to_state writes testing_evidence and per-attempt mastery_history entries (with period: before_misconception | during_misconception | after_correction). get_mastery_history and get_aggregated_mastery_for_unit support multi-attempt aggregation and policy for during-misconception. Report is derived from state and attempt result. **Limitation:** Persistence is in-memory only; “across persisted runs” is not exercised, but within-run aggregation is correct.

- **R5 Shared-core vs. Domain Layer.** **Partially satisfied.** Engine boundaries are clear: state_tracker, teaching_events, problem_selector, ta_conversation, ta_attempt/ta_code_generation, mastery_evaluator, misconception_engine, trace_history, run_cycle. There is no “if domain == Python” inside the state engine, task engine, or misconception engine for **core** behavior (transitions, selection rule, activation/unlearning/relearning). **Limitation:** The Domain Layer is not a formal abstraction. Content (knowledge units, problems, misconceptions) is loaded by engines via file paths (e.g. load_problems(problems_path), StateTracker(knowledge_units_path)). Guard rules and evaluation are implemented in Python-specific modules (ta_code_generation._FORBIDDEN_PATTERNS, mastery_evaluator.run_python_code). Adding a second domain would require new content files and a new evaluation adapter (and guard/stubs), but there is no formal “DomainAdapter” interface or registry; the “only content and adapters” rule is satisfied in practice but not by an explicit abstraction.

- **R6 Interaction Engine.** **Satisfied.** run_cycle.run_teaching_and_test (and run_correction, run_relearning_step, run_test_only) is the single orchestration entry point that calls engines in the order of SHARED_CORE_ARCHITECTURE §14. Scenarios A, B, C, D invoke this cycle with different inputs; there is no scenario-specific branching inside run_cycle for the order or logic of engine calls.

- **R7 Preserved behavior.** **Satisfied.** Scenario A: no eligible problem, ineligible reasons with missing units. Scenario B: pass, proficient. Scenario C: fail, failing, with misconception-driven wrong code. Guard and fallback unchanged; zero-knowledge start and constrained selection unchanged. Aligns with STAGE_ONE_SCENARIO_EVALUATION.md.

- **R8 Evidence preservation.** **Satisfied.** Stage One goals (zero-knowledge TA, constrained selection, success/failure paths) remain demonstrated; trace, misconception lifecycle, and mastery in state add evidence for the full framework claim without removing prior evidence.

- **R9 Readiness for domain extension.** **Partially satisfied.** The **logic** of the engines (state transitions, selection rule, misconception lifecycle, mastery aggregation) does not branch on domain. Adding a second domain would require new content (units, tasks, misconceptions) and a new evaluation adapter (and guard/stubs); the shared engines would not need to change their core behavior. **Limitation:** Without a formal Domain Layer abstraction (e.g. a domain registry or adapter interface), “adding only content and adapters” is done by convention and file layout, not by a single plug-in point. So the **direction** is correct and the **logic** is shared, but the **mechanism** for plugging in a new domain is not yet a first-class abstraction.

---

## 6. Does the Python System Now Qualify as a Shared-Core Domain Instance?

**Answer: Yes, with clear caveats.**

**In what sense the answer is yes:**

- The Python system is **no longer only a local prototype**. It is the first **concrete instantiation** of the shared-core architecture: one Knowledge State Engine, one Interaction Engine (run_cycle), one Task Engine, one TA Attempt Engine, one Mastery Evaluator, one Misconception/Unlearning/Relearning Engine, one Guard/Fallback path, and one Trace/History Layer. All of these are shared in the sense that their **behavior** does not depend on the domain name for core logic; they operate on state, tasks, and content that are supplied from outside (currently from Python-specific files and Python-specific evaluation/guard code). The state schema, trace event set, and misconception lifecycle are those of the blueprint; the cycle order is that of SHARED_CORE_ARCHITECTURE §14. So the Python prototype has been **migrated into** the shared core: it **is** the first domain instance that runs on top of that core.

- It **functions as the first genuine domain-specific instantiation** of the broader framework in this sense: the framework is “shared core + domain content + domain adapters.” The Python domain provides the content (knowledge-units-stage1.json, sample-problems-stage1.json, misconceptions-stage1.json) and the adapters (run_python_code, output_guard, stub code generation). The core (state, trace, misconception engine, orchestration, mastery aggregation) is the same that would be reused for Database or AI Literacy. So yes: Python is the first shared-core domain instance.

**Caveats:**

- The Domain Layer is not yet a formal abstraction (no DomainAdapter interface or domain registry). “Domain” is implicit in which files are loaded and which modules (e.g. ta_code_generation, mastery_evaluator) implement the adapter roles. For Stage G readiness, the important point is that **no engine logic branches on domain**; the absence of a formal adapter interface is a limitation for **scalable** domain expansion, not for the judgment that the current system is a shared-core domain instance.

- Trace does not yet include teaching_interpretation (optional in the trace doc until interpretation exists). Persistence is in-memory only. These do not change the fact that the architecture and behavior are those of the shared core.

**Conclusion:** The Python system **does** qualify as the first shared-core domain instance. It is more than a local prototype because it implements the shared schema, shared cycle, shared misconception lifecycle, and shared trace contract, and because adding another domain would not require changing that core logic — only adding content and adapters. The caveats indicate where the next phase (domain architecture design or formal domain adapter layer) should focus, not that the system is “still just a prototype.”

---

## 7. What Still Prevents Full Readiness for Domain Expansion

The following remain weak or incomplete before **large-scale** or **low-friction** domain expansion. They do not necessarily block “ready for domain architecture design” or “careful implementation” of a second domain; they are the honest list of what is missing for **full** readiness.

1. **No formal domain adapter abstraction.** Content and adapters are loaded by direct path and Python-specific modules. There is no DomainAdapter (or equivalent) interface that defines load_units(), load_tasks(), load_misconceptions(), get_evaluation_adapter(), get_guard_rules(), get_fallback_stubs(). Without it, adding Database or AI Literacy requires convention and possibly duplicated orchestration wiring (e.g. which paths to pass to which engine).

2. **No persistent storage across runs.** State and trace are in-memory. Mastery history and evidence chains are lost on restart. For evaluation and for “multi-session” scenarios, persistence would be required; the schema and trace format are ready, but the storage backend is not.

3. **Remaining Python-local content assumptions.** Problem and knowledge-unit structures (e.g. problem_id, knowledge_units_tested, problem_statement) are used directly by the Task Engine and TA Attempt Engine. The **shape** is generic enough (id, required units, statement, test cases or expected result), but the binding is to the current JSON and to “code” as the output type. A second domain (e.g. Database) would need a clear contract for task shape and output type (e.g. query string, explanation text) and an adapter that the shared engines call without branching on domain.

4. **Guard rules and evaluation adapter are hard-coded in Python modules.** _FORBIDDEN_PATTERNS and run_python_code live in ta_code_generation and mastery_evaluator. To add Database, guard rules and “run and compare” would need to be supplied by the domain (e.g. a Python domain package) rather than by the core. The refactor to “domain supplies adapters” is small but not yet done.

5. **teaching_interpretation not implemented or traced.** Automatic “correct / incorrect / ambiguous” teaching interpretation and linkage to misconception_id are not implemented; activation is explicit. For full C4 (evaluation traces the full chain including why a misconception was activated), teaching_interpretation would need to be added when interpretation is introduced. Trace already has a placeholder (event type and minimum fields in TRACE_AND_HISTORY_LAYER); the gap is the interpretation step and its recording.

6. **Scenario D and multi-attempt aggregation are exercised in one scenario.** The design supports multi-attempt mastery and during-misconception policy; Scenario D and get_aggregated_mastery_for_unit demonstrate it. Broader stress-testing (e.g. multiple problems per run, multiple correction/relearning cycles) would strengthen confidence but is not a prerequisite for “ready for domain architecture design.”

---

## 8. Readiness Judgment

**Chosen judgment:** **Ready for domain architecture design and careful implementation.**

**Justification:**

- **Ready for domain architecture design:** The migrated system satisfies the architectural criteria (state schema, trace, misconception lifecycle, mastery in state, shared cycle, preserved behavior, no domain branches in engine logic). The blueprint’s main claim is supported: the mechanism (knowledge-state-constrained, misconception-aware, unlearning/relearning-capable) is in place and evidenced by Scenarios A–D and trace. It is appropriate to **design** the Domain Layer and the second domain (e.g. Database) on this base — i.e. to write domain architecture documents, define the task/output contracts, and specify how content and adapters will plug in.

- **And careful implementation:** The same evidence supports **starting** implementation of a second domain (e.g. Database), provided implementation is **careful**: (1) do not add “if domain == database” inside shared engines; (2) introduce a formal domain adapter abstraction (or at least a clear convention) so that Python and Database (and later AI Literacy) are both “content + adapters” only; (3) keep the shared cycle and trace contract; (4) run regression on Scenarios A–D after any refactor. “Careful” means the team accepts that the first iteration of Database (or AI Literacy) may require a small refactor to extract adapters from the current Python-specific modules into a domain layer, and that persistence is still out of scope until the architecture is stable.

- **Not “fully ready for unconstrained domain expansion”:** Because there is no formal domain adapter yet and guard/evaluation are still in Python-specific modules, “full readiness” would require that refactor. The judgment is therefore “ready for domain architecture design and careful implementation,” not “ready for rapid, unconstrained addition of many domains.”

---

## 9. Immediate Next-Step Recommendation

**Recommendation:** **Write the domain architecture document(s) first, then introduce a formal domain adapter layer (or a clear domain registration convention) before or in parallel with implementing the Database domain.**

Rationale:

- The current system is ready to be **designed against**. A document that defines (1) the domain interface (content: units, tasks, misconceptions; adapters: evaluation, guard, fallback), (2) the task/output contract (e.g. task_id, knowledge_units_tested, output type: code | query | explanation), and (3) how the Interaction Engine and other engines obtain “the current domain’s” content and adapters (e.g. domain registry, or explicit passing of adapter instances per run), will reduce risk when implementing Database. It will also make the “content and adapters only” boundary explicit and testable.

- Optionally, a small refactor to extract the Python evaluation adapter and guard rules into a “Python domain” module (or package) that the shared Mastery Evaluator and TA Attempt Engine call via an interface would make R5 and R9 fully satisfied and would make adding Database a matter of implementing the same interface for Database content and SQL execution. That refactor can be done before or in parallel with the Database design.

- Starting Database implementation without a domain architecture document or adapter abstraction is possible but riskier: the team might hard-code “if task type is code do X, if query do Y” in the core. The recommended next step is to lock the contract (document + optional adapter interface) and then implement the second domain against it.

---

## 10. Readiness Guardrails for the Next Phase

When moving beyond Stage G, the team must preserve the following. These are non-negotiable to keep the main claim and the value of the migration.

1. **Do not break the shared cycle.** The Interaction Engine (run_cycle) must remain the single entry point for one teaching–testing cycle. No domain-specific “main loop” that reorders or skips engine calls.

2. **Do not weaken state-as-single-source-of-truth.** All “what does the TA know?” inputs to dialogue, task selection, and attempt generation must come from the Knowledge State Engine. No component may use raw conversation history or LLM memory as the source of what the TA knows.

3. **Do not lose traceability.** Every teaching event, state update, task selection, attempt, evaluation, misconception activation, correction, relearning, and mastery update must continue to be recorded with the minimum trace fields. New behaviors must add trace, not drop it.

4. **Do not reduce the contribution to “more domains.”** The contribution is the **mechanism** (unified, state-constrained, misconception-aware, unlearning/relearning-capable framework). Adding Database or AI Literacy must demonstrate that the **same** mechanism works with different content and adapters, not that “we have three separate systems.”

5. **Do not expand UI or deployment before the architecture is stable.** UI polish and deployment plans should follow (or run in parallel with) domain architecture and the formal adapter layer, not precede them in a way that locks in prototype-specific assumptions.

6. **Do not let new domains bypass shared core rules.** New domains must use the same state schema, the same selection rule (required units ⊆ eligible units), the same misconception lifecycle (activation, correction, unlearning, relearning), and the same trace event set. Domain-specificity is content and adapters only.

---

## 11. Conclusion

Stage G shows that the migration from the Python Stage One prototype to the shared-core architecture has reached a **usable milestone**. The knowledge state has been expanded to the full schema; trace is in place for the full chain; the misconception lifecycle (activation, correction, unlearning, relearning) is implemented and observable; mastery is persisted in state and aggregated with policy for during-misconception attempts; and a single orchestration path (run_cycle) drives Scenarios A, B, C, and D without scenario-specific engine logic. The Python system now qualifies as the **first shared-core domain instance**: it is more than a local prototype because it runs on the shared architecture and because the same core would support additional domains with content and adapters only.

Readiness is **partial** in two areas: trace does not yet include teaching_interpretation (optional until interpretation exists), and the Domain Layer is not yet a formal abstraction (guard and evaluation are still in Python-specific modules). These do not block the judgment that the system is ready for **domain architecture design and careful implementation**. The recommended next step is to write domain architecture document(s) and to introduce a formal domain adapter layer (or a clear convention) before or alongside implementing the Database domain. The team should observe the readiness guardrails so that the main claim — a unified, knowledge-state-constrained, misconception-aware, unlearning/relearning-capable framework — remains supported as the project moves into multi-domain implementation.

---

*End of Stage G Readiness Check*
