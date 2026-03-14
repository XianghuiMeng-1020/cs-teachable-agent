# Unlearning and Relearning Engine

**Document type:** Shared core design — misconception lifecycle and state transition logic  
**Governing document:** MASTER_SYSTEM_BLUEPRINT.md  
**Companion document:** docs/UNIFIED_KNOWLEDGE_STATE_SCHEMA.md (shared terminology, state language, evidence representation)  
**Alignment:** §2 Main Claim and Claim Stack (C2); §10 Negative Scope; §12 Unified Knowledge State Logic; §13 Misconception, Unlearning, and Relearning Logic; §16 Evaluation Logic; §19 Non-Negotiable Design Guardrails; §21 Evidence Map; §23 Blueprint Alignment Checks  
**Status:** Binding logic for all domains; misconception lifecycle is central to the project’s contribution

---

## 1. Why Unlearning and Relearning Are Central

The project’s strongest potential contribution is not “more domains” or “a bigger demo.” It is the **shared mechanism**: unified knowledge-state-constrained learner behavior, misconception-aware modeling, and explicit unlearning/relearning logic with cross-domain traceability. Most teachable-agent systems treat knowledge as monotonically increasing (teach more → know more). This system models knowledge as **non-monotonic**: the TA can learn incorrectly, exhibit specific errors, require correction, undergo unlearning, and relearn — and every step must be explicitly represented, behaviorally observable, and evaluable. The Unlearning/Relearning Engine is the component that implements this lifecycle. Without it, the TA’s errors are random or predetermined (as in the Stage One stub-based failure path), not educationally meaningful; with it, the TA’s errors are traceable to specific misconceptions, and the student’s corrective teaching has specific, measurable effects on state and mastery. This document defines the full logic so that all domains (Python, Database, AI Literacy) use the same engine and the same transition rules.

---

## 2. Core Concepts and Definitions

- **Misconception:** A documented incorrect understanding of one or more knowledge units. It has an id, affected units, example wrong/correct behavior, and remediation criteria (from the domain’s misconception catalog). In the engine, “misconception” refers to the *activation* of such a catalog entry in the TA’s state.

- **Activation:** The process by which a misconception enters the TA’s knowledge state for a given unit. After activation, the misconception is *active*: it appears in the unit’s `active_misconceptions` and must affect dialogue and task performance.

- **Correction:** The process by which the student (or system) provides teaching or feedback that directly addresses the misconception and is consistent with the correct understanding. Correction is *detected* by the engine (e.g. by matching teaching to remediation criteria or by explicit correction event) and triggers unlearning.

- **Unlearning:** The state transition from “holding the misconception” to “no longer holding it.” The misconception is removed from `active_misconceptions`; the unit’s status moves to a transitional state (e.g. `corrected` or `partially_learned_post_correction`), not immediately back to `learned`. Unlearning is represented in the schema via correction_evidence.

- **Relearning:** The process of re-establishing correct understanding after a misconception has been unlearned. It is driven by additional correct teaching and/or successful task performance. The unit’s status transitions from the post-correction state back to `learned` (or `partially_learned`) when sufficient relearning evidence exists. Relearning is represented in the schema via relearning_evidence and optionally updated status and mastery_history.

- **Mastery recalculation:** After correction and relearning, the Mastery Evaluator recomputes mastery for the affected unit(s). Test results obtained while the misconception was active may be weighted differently from results after relearning; the current mastery level should reflect current understanding while history is preserved for evaluation.

---

## 3. Misconception Lifecycle Overview

The full lifecycle is:

1. **Acquisition** — Wrong or ambiguous teaching (or pre-seeding) causes a misconception to be activated for one or more units.
2. **Persistence** — The misconception remains in `active_misconceptions` until correction is detected.
3. **Behavioral effect** — Dialogue and task attempts reflect the misconception (wrong code, wrong query, wrong explanation).
4. **Correction detection** — The system detects that the student has provided corrective teaching (or an explicit correction event).
5. **Unlearning** — The misconception is removed from active state; the unit moves to a post-correction transitional status; correction_evidence is written.
6. **Relearning** — Further correct teaching and/or successful tests accumulate; relearning_evidence is written; when sufficient, status returns to learned.
7. **Mastery recalculation** — Mastery for the unit is updated to reflect current evidence; history preserves the trajectory (e.g. failing → developing → proficient after relearning).

The engine does not treat “misconception goes away” as a single step. Unlearning and relearning are distinct transitions so that the system can represent “corrected but not yet reinforced” and so that evaluation can trace the full cycle.

---

## 4. How Wrong Teaching Enters the System

Wrong teaching can enter in four ways:

1. **Incorrect student teaching.** The student explains a concept wrongly (e.g. “range(5) gives 1 through 5” or “= and == are the same”). The teaching interpretation layer (structured event or future NL interpretation) marks the teaching as contradicting the correct understanding of the relevant knowledge unit(s). The engine matches this to a catalog misconception (e.g. `off_by_one_range`) and **activates** that misconception for those units.

2. **Ambiguous student teaching.** The student’s explanation is incomplete or ambiguous in a way that matches a known misconception pattern (e.g. teaching loops without clarifying that range is exclusive of the upper bound). The engine may activate the misconception with lower confidence or with a trigger type `ambiguous_teaching`, so that correction and history can distinguish “explicitly wrong” from “ambiguous.”

3. **Pre-seeded misconceptions.** Some misconceptions may be seeded at session start (e.g. the TA “starts” with common beginner errors). The trigger is `pre_seeded`. This mirrors the educational case where the student must correct pre-existing beliefs.

4. **Misconception transfer.** A misconception activated for one unit may propagate to related units (e.g. `assign_vs_equal` affects both `variable_assignment` and `if_statement`). The engine applies transfer rules defined in the domain’s misconception catalog (e.g. “when M is activated for unit A, also activate for units B, C”). Trigger is `transfer_from_unit` with a reference to the source unit.

In all cases, the engine records in the knowledge state: which misconception_id was activated, when (timestamp or sequence_id), and the trigger type. This supports the evaluation requirement that we can trace “wrong teaching → misconception activation → wrong behavior.”

---

## 5. How Misconceptions Become Active

When the engine activates a misconception for a unit:

1. **Add to active_misconceptions.** The unit’s `active_misconceptions` list gains one entry: misconception_id, activated_at, trigger, trigger_reference (e.g. teaching_event_id). Optionally, flagged_for_correction is set to false.

2. **Update status.** The unit’s `status` is set to `misconception` if the misconception is considered to dominate (e.g. the unit was learned and is now overridden by the wrong belief). Policy may allow a unit to remain `learned` with an “overlay” of active misconceptions in some domains; the schema supports both. The engine must define a clear rule: for this project, when any misconception is active for a unit, the unit’s status is at least `misconception` (or an equivalent that drives behavior the same way), so that dialogue and task generation always see “this unit is misconception-affected.”

3. **Optional: reduce confidence.** Confidence for the unit may be reduced to reflect that the TA’s understanding is wrong.

4. **Persist.** The state is persisted (or written to the trace layer) so that subsequent dialogue and task attempts use the updated state.

Activation is idempotent for the same (unit, misconception_id) within a session: if the misconception is already active, the engine does not duplicate the entry but may update activated_at or trigger_reference if the same misconception is re-triggered by another teaching event.

---

## 6. How Misconceptions Affect Dialogue

The Learner Dialogue Engine receives the current knowledge state, including `active_misconceptions` per unit. When the TA is asked to respond in a context that involves a unit with an active misconception:

- The dialogue prompt (or equivalent) must include the misconception’s description and/or example incorrect belief so that the TA’s response **expresses** the misconception (e.g. “So range(5) gives me the numbers 1, 2, 3, 4, 5?”). The TA does not “pretend” to be wrong; the state says it holds this wrong belief, and the response must be consistent with that state.

- The same applies across domains: for Database, the TA might say “So I use = NULL to check for null?” when `null_equality` is active; for AI Literacy, “So the model really understands what the words mean?” when `ai_understands_meaning` is active.

The engine does not generate dialogue itself; it supplies the state (including active_misconceptions) to the Learner Dialogue Engine. The contract is: whenever a unit has non-empty active_misconceptions, the dialogue engine must use that information so that the TA’s conversational behavior is consistent with the misconception. This makes the misconception observable and gives the student a diagnostic signal.

---

## 7. How Misconceptions Affect Task Performance

The TA Attempt Engine receives the current state, including learned units and active_misconceptions. When the TA attempts a task that involves a unit with an active misconception:

- The engine (or the attempt generator) must produce output that **reflects** the misconception. For Python: wrong code consistent with the misconception (e.g. off-by-one in range). For Database: wrong query (e.g. `= NULL` instead of `IS NULL`). For AI Literacy: wrong explanation (e.g. “AI understands meaning”).

- The misconception catalog provides example_incorrect_code / example_incorrect_behavior; the TA Attempt Engine uses this (and the active misconception id) to constrain generation (e.g. via prompt injection or stub when a specific misconception is active). The guard layer may check that the output is consistent with the misconception (and with learned units) rather than randomly wrong.

- If the TA fails the task, the failure is **attributed** to the misconception in testing_evidence (e.g. misconception_active_during_attempt = misconception_id). This supports “wrong behavior matches misconception” in evaluation and mastery recalculation (e.g. down-weight or exclude attempts during active misconception when computing current mastery).

The engine ensures that active_misconceptions are passed to the TA Attempt Engine and that results are recorded with a link to the misconception when applicable. The engine does not generate task output; it maintains state and feeds it to the attempt layer.

---

## 8. What Counts as Correction

Correction is the event that triggers unlearning. The engine treats the following as correction:

1. **Explicit correction event.** The student (or teacher UI) sends a structured “correct misconception M for unit U” event. The engine then runs the unlearning transition for M on U.

2. **Corrective teaching that matches remediation.** The student provides teaching that (a) targets the same unit(s) as the active misconception and (b) matches the misconception’s remediation criteria (e.g. correct explanation of range(n) as 0..n-1). Teaching interpretation may be rule-based (e.g. structured event with a “correction_for” misconception_id) or, in a future phase, LLM-based analysis that detects “this teaching contradicts the misconception and matches correct understanding.” When the engine receives a teaching event that is tagged as corrective for misconception M (or that is inferred to be corrective), it runs the unlearning transition for M on the affected unit(s).

3. **Reinforcement rule (optional).** Some designs may require that the student not only teach correctly once but also that the TA acknowledge or that a subsequent task be passed before unlearning is confirmed. The engine can define a “correction = teaching that matches remediation + optional acknowledgment or successful task.” For traceability, the minimal requirement is that at least one corrective teaching event (or explicit correction event) is recorded; additional reinforcement can be part of relearning.

The engine must not treat “any new teaching on the unit” as correction; the teaching must be explicitly or inferentially corrective for the specific active misconception. Otherwise, the system could unlearn without the student having addressed the error.

---

## 9. What Counts as Unlearning

Unlearning is the **state transition** that occurs when correction is detected. It is not “the misconception disappears from the UI”; it is a formal transition in the knowledge state.

**Unlearning transition (per unit, per misconception):**

1. **Remove from active_misconceptions.** The entry for this misconception_id is removed from the unit’s `active_misconceptions` list.

2. **Set status to a post-correction state.** The unit’s status is set to `corrected` or `partially_learned_post_correction` (terminology aligned with UNIFIED_KNOWLEDGE_STATE_SCHEMA.md). The unit does **not** immediately return to `learned`. This reflects the educational reality that being told the correct answer once does not immediately produce robust understanding; relearning requires further evidence.

3. **Write correction_evidence.** One entry is appended to the unit’s correction_evidence: misconception_id, corrected_at, trigger (e.g. student_reteaching), teaching_event_id or correction_event_id, state_before (e.g. misconception), state_after (e.g. corrected).

4. **Optional: adjust confidence.** Confidence may remain low or be set to a value that reflects “recently corrected, not yet reinforced.”

5. **Persist and trace.** The new state is persisted; the trace layer logs the unlearning event (unit, misconception_id, timestamp, trigger).

**Design choice — immediate vs. partial restoration:** This document specifies that correction **does not** immediately restore `learned` status. The unit moves to a transitional state and requires relearning to return to `learned`. This avoids overclaiming “the TA is fixed” after one corrective sentence and supports the evaluation need to distinguish “never learned,” “learned wrongly then corrected,” and “relearned after correction.”

---

## 10. What Counts as Relearning

Relearning is the process of re-establishing correct understanding after unlearning. It is driven by **evidence** that the TA now holds the correct understanding.

**Relearning evidence (either or both):**

1. **Correct teaching on the unit after correction.** Teaching events that target the unit after the correction event, and that are consistent with correct understanding (not marked as incorrect or ambiguous), add one relearning_evidence entry (type: teaching). After N such events (N ≥ 1, policy-defined), the unit may transition from `corrected` to `partially_learned` or `learned`.

2. **Successful task performance on the unit after correction.** A task attempt that (a) involves this unit, (b) occurs after the correction timestamp, and (c) passes (pass_fail = true) adds one relearning_evidence entry (type: successful_task). After M successful tasks (M ≥ 1, policy-defined), the unit may transition to `learned`.

**Relearning transition (when sufficient evidence exists):**

1. **Update status.** The unit’s status is set from `corrected` (or `partially_learned_post_correction`) to `learned` (or, if policy uses it, first to `partially_learned` and then to `learned` after more evidence).

2. **Append relearning_evidence.** Each qualifying teaching or successful task already appended an entry; no extra write is needed at transition except possibly a “relearning_complete” marker or the status change itself.

3. **Optional: restore or increase confidence.** Confidence may be increased to reflect reinforced understanding.

4. **Mastery recalculation.** The Mastery Evaluator recomputes mastery for this unit (see §12).

**Design choice — fresh evidence required:** Relearning **requires** post-correction evidence. The engine does not treat “correction happened” as sufficient for learned; at least one (and typically more) teaching or successful task after correction must be recorded. This keeps “relearned” distinguishable from “corrected but not yet reinforced” and supports the claim that the system models fragile post-correction state.

---

## 11. State Transition Logic

The following summarizes the state machine in a structured form. All transitions are applied by the shared engine; domains only supply content (misconception catalogs, teaching events, task results).

**Initial state (per unit):**  
`status = unknown`, `active_misconceptions = []`, no teaching/testing/correction/relearning evidence (or default empty).

**Teaching event (correct):**  
If teaching targets unit U and is consistent with correct understanding:  
- `status` (U): unknown → partially_learned or learned (policy: e.g. one event → learned, or multi-event threshold).  
- Append to teaching_evidence (U).  
- No change to active_misconceptions.

**Teaching event (incorrect or ambiguous):**  
If teaching targets unit U and matches misconception M (incorrect or ambiguous):  
- Activate M for U: append to active_misconceptions (U); set status (U) = misconception.  
- Append to teaching_evidence (U) with misconception_activated = M.  
- Optional: transfer M to related units per catalog.

**Failed test evidence (with active misconception):**  
- Append to testing_evidence (U) with pass_fail = false and misconception_active_during_attempt = M.  
- Mastery history may show failing; current mastery computation may down-weight or exclude this attempt when recalculating after correction.

**Correction evidence (unlearning):**  
When correction is detected for misconception M on unit U:  
- Remove M from active_misconceptions (U).  
- Set status (U) = corrected (or partially_learned_post_correction).  
- Append to correction_evidence (U): M, corrected_at, trigger, state_before = misconception, state_after = corrected.

**Relearning evidence:**  
When a correct teaching event or successful task on U occurs after correction:  
- Append to relearning_evidence (U).  
- When relearning policy is satisfied (e.g. at least one teaching and one successful task, or N events):  
  - Set status (U) = learned.  
  - Trigger mastery recalculation for U.

**Updated mastery state:**  
After any testing_evidence or relearning update, the Mastery Evaluator recomputes mastery for the unit and appends to mastery_history. Current mastery level reflects the rubric applied to the relevant evidence (with policy for weighting post-correction vs. during-misconception attempts).

---

## 12. Mastery Recalculation Logic

After correction and during/after relearning, mastery for the affected unit(s) must be recomputed.

**Principles:**

1. **Current mastery reflects current understanding.** The reported mastery level (e.g. failing / developing / proficient) should be based primarily on evidence that reflects the TA’s *current* state. Test attempts that occurred while the misconception was active may be:  
   - Excluded from the current pass-rate numerator and denominator, or  
   - Weighted lower than post-correction attempts, or  
   - Kept in the denominator but with a clear policy (e.g. “mastery = pass rate over all attempts” but with a label “includes X attempts during misconception”).  
   The schema and rubric document should define one policy so that mastery is comparable across domains.

2. **History is preserved.** mastery_history retains the full trajectory (e.g. failing when misconception was active, then developing, then proficient after relearning). This supports evaluation and the student view (“the TA was failing, then you corrected, then after two tasks it became proficient”).

3. **Relearning may require extra evidence.** The blueprint states that a unit that has been through a misconception → correction → relearning cycle may require additional test evidence before being marked proficient. The Mastery Evaluator can implement this by: requiring a minimum number of post-correction successful attempts before the unit’s mastery level can rise to proficient, or by using a stricter threshold for “relearned” units. The engine does not dictate the exact threshold but requires that the recalculation uses the same rubric and evidence structure as in UNIFIED_KNOWLEDGE_STATE_SCHEMA.md.

4. **Traceability.** Each mastery_history entry should be attributable to a point in time and to the evidence set used (e.g. “after attempt_id X” or “after relearning_event_id Y”). This allows evaluation to show “mastery after correction” and “mastery trajectory.”

---

## 13. Traceability and History Requirements

The engine and the schema together must support full traceability:

- **Every activation** is recorded (misconception_id, unit, activated_at, trigger, trigger_reference).  
- **Every correction** is recorded in correction_evidence (misconception_id, corrected_at, trigger, state_before, state_after).  
- **Every relearning step** is recorded in relearning_evidence (event id, type, state_after).  
- **Mastery history** preserves the time-series of levels so that “never learned” vs “learned wrongly then corrected” vs “relearned” can be distinguished in evaluation and in the student view.

The trace layer (see MASTER_SYSTEM_BLUEPRINT) must log: teaching events, state diffs (before/after), task attempts, results, misconception activations, corrections, and mastery updates. The engine writes state and evidence; the trace layer may subscribe to these writes or be called explicitly so that no transition is unlogged. This is non-negotiable for the evaluation claim (teaching → state → behavior → mastery).

---

## 14. Shared Engine vs Domain-Specific Misconceptions

The **engine** (transition rules, when to activate/unlearn/relearn, how to update status and evidence) is **shared**. It is the same code (or the same specification) for Python, Database, and AI Literacy.

The **misconceptions** (ids, descriptions, affected units, examples, remediation criteria) are **domain-specific**. They live in each domain’s misconception catalog. The engine does not hard-code “off_by_one_range” or “null_equality”; it receives misconception_id and unit_id and applies the same activation, correction detection, unlearning, and relearning logic. Domain-specific behavior is confined to: (a) which misconceptions exist and for which units, (b) how teaching is interpreted (e.g. which catalog misconception a teaching event matches), and (c) how task output is generated to reflect the misconception (code vs query vs explanation). The engine only needs to know “misconception M was activated for unit U,” “correction for M on U was detected,” “relearning evidence was added for U” — and it performs the same state transitions in every domain.

---

## 15. Example Lifecycle: Python

1. **Initial:** Unit `for_loop_range` is unknown.  
2. **Wrong teaching:** Student says “range(5) gives you 1, 2, 3, 4, 5.” Teaching is interpreted as incorrect for `for_loop_range` and matches catalog misconception `off_by_one_range`. Engine activates `off_by_one_range` for `for_loop_range`; status = misconception; active_misconceptions = [off_by_one_range].  
3. **Task attempt:** TA is given a problem “print 0 to 4.” TA produces code that prints 1–5 (reflecting misconception). Test fails. Testing_evidence records pass_fail = false, misconception_active_during_attempt = off_by_one_range. Mastery (if computed) = failing.  
4. **Correction:** Student teaches “range(n) gives 0 through n-1.” Engine detects corrective teaching for `off_by_one_range`. Unlearning: remove off_by_one_range from active_misconceptions; status = corrected; append correction_evidence.  
5. **Relearning:** Student gives another correct explanation or TA passes a range-related task. Relearning_evidence appended. After policy (e.g. one successful task), status = learned. Mastery recalculated (e.g. proficient if the post-correction attempt passed).  
6. **History:** Evaluation can show: “Unit for_loop_range: learned → misconception (off_by_one_range) → corrected → relearned → learned; mastery: failing → proficient.”

---

## 16. Example Lifecycle: Database

1. **Initial:** Unit `null_handling` is unknown.  
2. **Wrong teaching:** Student says “you check for NULL with = NULL.” Teaching matches misconception `null_equality`. Engine activates `null_equality` for `null_handling`; status = misconception.  
3. **Task attempt:** TA writes `WHERE col = NULL`. Query returns wrong results. Testing_evidence: pass_fail = false, misconception_active_during_attempt = null_equality.  
4. **Correction:** Student teaches “use IS NULL and IS NOT NULL.” Engine detects correction for `null_equality`. Unlearning: status = corrected; correction_evidence appended.  
5. **Relearning:** TA passes a task that requires correct NULL handling. Relearning_evidence (type: successful_task). Status → learned. Mastery recalculated.  
6. **Same engine, different content:** The transition logic is identical to Python; only the misconception id, unit id, and task type (query vs code) differ.

---

## 17. Example Lifecycle: AI Literacy

1. **Initial:** Unit `what_is_ai` or a concept related to “AI understanding” is learned or partially learned.  
2. **Misconception activation:** Student says “the model understands what the words mean.” Teaching matches misconception `ai_understands_meaning`. Engine activates it for the relevant unit(s); status = misconception.  
3. **Task attempt:** TA is asked “Does the model understand meaning?” TA explains in line with the misconception. Explanation is evaluated (rubric) as incorrect. Testing_evidence: pass_fail = false, misconception_active_during_attempt = ai_understands_meaning.  
4. **Correction:** Student says “No, it doesn’t understand meaning; it finds patterns in text data.” Engine detects correction. Unlearning: status = corrected; correction_evidence appended.  
5. **Relearning:** TA is taught again correctly and/or passes an explanation task that requires correct understanding. Relearning_evidence appended; status → learned. Mastery recalculated.  
6. **Same engine:** Again, only the content (conceptual misconception, explanation tasks) is domain-specific; activation, unlearning, relearning, and mastery recalculation use the shared engine.

---

## 18. Risks of Weak Misconception Modeling

- **Misconception only in data:** If misconceptions exist in the catalog and schema but do not drive dialogue and task output, the TA’s errors are not traceable to specific misconceptions; the unlearning/relearning cycle is not observable; the main claim (misconception lifecycle implemented and observable) fails.

- **Correction immediately restores “learned”:** If the engine sets status back to learned as soon as correction is detected, the system overclaims. The distinction between “corrected” and “relearned” is lost; evaluation cannot show that relearning requires reinforcement; the design is no longer aligned with the blueprint.

- **No history:** If correction and relearning are not recorded in correction_evidence and relearning_evidence, evaluation cannot trace “learned wrongly then corrected” vs “never learned,” and the research value of the mechanism is reduced.

- **Domain-specific branches in the engine:** If the unlearning/relearning logic differs per domain (e.g. different transition rules for Python vs Database), the “same framework” claim is weakened and maintenance and evaluation become harder.

- **Random or stub-only errors:** If the TA’s wrong behavior is not consistently tied to active misconceptions (e.g. only stubbed wrong code), the link “misconception M → wrong behavior → correction → unlearning → relearning” cannot be demonstrated; C2 (misconception lifecycle implemented and observable) is not met.

---

## 19. Engine Design Guardrails

- **Do not make unlearning/relearning optional or “Phase 3.”** They are part of the core. No domain is considered complete without at least a prototype of the full cycle (activation → behavior → correction → unlearning → relearning) and traceable evidence.

- **Do not collapse correction and relearning into one step.** The schema and engine must represent: (1) misconception active, (2) correction detected → unlearning (status = corrected), (3) relearning evidence accumulated → status = learned. This supports both evaluation and the “fragile post-correction” narrative.

- **Do not allow domain-specific transition rules in the shared engine.** Activation, unlearning, and relearning transitions are the same for every domain. Domain-specificity is in the catalog (which misconceptions, which units) and in teaching/task interpretation, not in the state machine.

- **Do not leave correction detection underspecified.** The engine must define what counts as correction (explicit event vs. teaching that matches remediation) and how the system detects it (structured event field, or inference from teaching content). If detection is vague, unlearning cannot be triggered reliably and the lifecycle is broken.

- **Preserve full history.** Mastery history and evidence (teaching, testing, correction, relearning) must be preserved so that “never learned” vs “learned wrongly then corrected” vs “relearned” is distinguishable and so that evaluation can link teaching → state → behavior → mastery.

---

## 20. Conclusion

The Unlearning/Relearning Engine implements the misconception lifecycle that is central to the project’s contribution: the TA can learn incorrectly, exhibit specific errors, be corrected, unlearn the misconception, and relearn — with every step represented in the unified knowledge state and observable in behavior and mastery. The engine is shared across Python, Database, and AI Literacy; only the misconception content and the form of teaching/tasks are domain-specific. Together with the Unified Knowledge State Schema, this document defines the shared conceptual backbone for misconception-aware, state-constrained teachable agents. Later domain work must plug into this engine and schema; it must not implement a separate or weaker misconception logic. The contribution is the mechanism — the shared architecture and lifecycle — not the number of domains; these two documents lock down that mechanism so that all future domain architecture and implementation can depend on it.
