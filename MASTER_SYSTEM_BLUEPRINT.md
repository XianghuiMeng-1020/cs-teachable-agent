# MASTER SYSTEM BLUEPRINT

**Teachable Agent for Computer Science: Unified Knowledge-State-Constrained, Misconception-Aware Framework**

**Document type:** Governing blueprint — single source of strategic truth for the entire project  
**Date:** 2026-03-13  
**Revised:** 2026-03-13 (hardening pass: Main Claim and Claim Stack, Negative Scope, Evidence Map, stronger alignment/drift checks)  
**Status:** Active governing document  
**Scope:** Full project — all domains, all phases, all future Cursor runs  
**Authority:** All future implementation, evaluation, system extension, and paper positioning must remain consistent with this blueprint. Any deviation must be justified against the principles defined here.

---

## 1. Project Identity

This project is not a chatbot. It is not a tutoring system. It is not a coding assistant with a different persona. It is not a collection of domain-specific demos stitched together under a common name.

This project is the design, implementation, and evaluation of a **unified teachable-agent framework for computer science education** — a system in which a human student teaches an AI agent that begins with zero domain knowledge, and where the agent's behavior at every moment is governed by an explicit, structured, inspectable knowledge state. The framework must support multiple CS domains — beginning with Introductory Python programming and extending to Database fundamentals and AI Literacy — under a single shared architecture for knowledge representation, misconception modeling, unlearning and relearning logic, mastery evaluation, and state-constrained learner behavior.

The project should be understood as a unified research-and-system endeavor. "Teachable Agent for CS" is the external name, but the internal identity is more precise: it is the construction of a **knowledge-state-constrained, misconception-aware, unlearning/relearning-capable agent framework** that can operate across multiple computer science domains while maintaining a single coherent model of what the agent knows, what it misunderstands, what it has forgotten, and what it has relearned. The Stage One Python foundation that already exists is a validated starting point — a proof that the core loop (teach → state update → constrained problem attempt → grading → mastery report) is feasible and implementable. But the final system is far larger than that foundation. The final system must demonstrate that the framework's mechanisms generalize: that the same knowledge-state engine, the same misconception logic, the same unlearning and relearning architecture, and the same evaluation methodology can govern agent behavior in Python, in Database, and in AI Literacy — and that this shared governance is what produces both the system's educational value and its research contribution.

The reason this project is larger than the Stage One Python prototype is not that it covers more topics. It is that the prototype validated a mechanism (state-constrained agent behavior with testing) but did not yet demonstrate that the mechanism can generalize across structurally different domains, handle misconceptions as a first-class modeling concern, represent unlearning and relearning as explicit state transitions, or produce evaluation evidence linking teaching quality to knowledge-state change to mastery outcomes. Those are the pieces that elevate the project from a single-domain demo to a framework-level contribution.

---

## 2. Main Claim and Claim Stack

This section makes the project’s claim hierarchy explicit so that future work can be tested against it. The main claim and its supporting subclaims define what the project must prove; the evidence and component mappings define how it will be proven.

### 2.1 The Main Claim

**Main Claim (single-sentence):**  
We propose and operationalize a **unified, knowledge-state-constrained, misconception-aware, unlearning/relearning-capable teachable-agent framework** for computer science learning across multiple domains — where the agent’s behavior is structurally governed by an explicit knowledge state (not persona alone), misconceptions are first-class objects with activation, correction, unlearning, and relearning, and the same framework logic applies across structurally different domains (code execution, query evaluation, conceptual assessment).

### 2.2 Supporting Subclaims

The main claim rests on the following supporting subclaims. Each must be demonstrable; if any is weak or unsupported, the main claim is weakened.

| # | Supporting claim | System mechanism / component | Evidence needed | What weakens it |
|---|-------------------|------------------------------|-----------------|-----------------|
| **C1** | The agent’s behavior is **structurally constrained** by an explicit knowledge state (not only by prompts). | Knowledge State Engine; Guard/Fallback Layer; TA Attempt Engine; Learner Dialogue Engine | State governs selection, generation, and dialogue; guards reject out-of-scope output; fallback when LLM violates constraints | Constraint enforced only by prompts; no guards; no fallback; state bypassed in any path |
| **C2** | **Misconception lifecycle** (activation → behavior → correction → unlearning → relearning) is implemented and observable in the system. | Misconception / Unlearning / Relearning Engine; Knowledge State (misconception fields); TA Attempt Engine (misconception injection) | Traced cycles per domain; wrong behavior matches misconception; correction changes state; mastery reflects relearning | Misconceptions only in data model; no behavioral effect; no unlearning/relearning transitions; only stub failure |
| **C3** | The **same framework** (shared engines, same state model, same rubric, same evaluation chain) operates across Python, Database, and AI Literacy. | Domain Layer (content only); shared Knowledge State Engine; shared Misconception Engine; shared Mastery Evaluator; shared Interaction Engine | One codebase for engines; new domain = new content layer only; cross-domain mastery comparable | Domain-specific engines; different state formats; different mastery logic; adding a domain requires engine changes |
| **C4** | **Evaluation** traces the full chain: teaching action → state change → behavior change → mastery outcome. | History / Trace Layer; Evaluation Logic (Section 18); teaching-to-state-change and mastery evaluation | Logged teaching events, state diffs, task attempts, results; analyses that link teaching to state to outcome | Evaluation is “demo works”; no traces; no teaching→state→mastery analysis |

### 2.3 Component–Claim Mapping

- **Knowledge State Engine** supports C1, C2, C3.  
- **Guard / Fallback Layer** supports C1.  
- **Misconception / Unlearning / Relearning Engine** supports C2, C3.  
- **TA Attempt Engine, Learner Dialogue Engine** support C1, C2.  
- **Mastery Evaluator, Task/Problem Engine, Interaction Engine** support C1, C3, C4.  
- **History / Trace Layer** supports C4.  
- **Domain Layer** (content only, no engine logic) supports C3.

Future work that modifies these components must preserve the support for the claims above; if a change undermines a claim, it is off track unless the claim stack is explicitly revised in this blueprint. See Section 18 (Evaluation Logic) for the evaluation design that supports C4.

---

## 3. What We Have Already Completed

The Python Stage One foundation has been designed, implemented, documented, evaluated, and reflected upon. It is a real, runnable, reproducible system — not a sketch or a plan. The following is a concrete accounting of what exists.

### Completed

- **Zero-knowledge teachable agent.** The TA initializes with all 20 knowledge units set to `unknown`. It has no usable programming knowledge until a student teaches it. The `StateTracker` enforces this: it loads units from `knowledge-units-stage1.json` and begins every session from a blank state.

- **Structured knowledge state as single source of truth.** The TA's knowledge is represented as a structured per-unit state (unknown / partially_learned / learned) maintained by `state_tracker.py`. All downstream behavior — problem selection, code generation, conversation constraints — reads from this state. The state is not implicit in conversation history; it is an explicit, inspectable data structure.

- **Structured teaching events.** Teaching is delivered via structured events (`teaching_events.py`), each containing a topic, a list of knowledge units taught, and a note. The `apply_teaching_event()` function updates the state tracker deterministically. This mechanism validates that the system can receive teaching input and translate it into state changes.

- **Knowledge-state-constrained problem selection.** The `problem_selector.py` module selects problems from the curated bank (`sample-problems-stage1.json`, 16 problems) only when every required knowledge unit has been learned. `get_eligible_problem_ids()` returns the set of selectable problems; `get_ineligible_reasons()` explains why each non-selectable problem is excluded (listing missing units). This validates that the TA is never tested on concepts it has not been taught.

- **TA code attempt generation with dual paths.** The system supports two code-generation paths: a stub path (`ta_attempt.py`) that returns predefined correct or incorrect code per problem, and an optional LLM path (`ta_code_generation.py`) that calls an LLM to generate code constrained by the TA's learned units and active misconceptions. The LLM path includes an output guard that rejects code containing forbidden constructs (`def`, `class`, `import`, `open(`, `try:`, `except`, `with ... as`). If the guard rejects the LLM output or the LLM call fails, the system falls back to the stub path. This validates both the constrained-generation concept and the fallback-safety concept.

- **Automated grading and mastery evaluation.** The `mastery_evaluator.py` module executes the TA's code in a subprocess, compares stdout against expected test-case outputs, and produces pass/fail results. It computes per-unit and overall mastery levels (failing / developing / proficient) based on pass rates, following the rubric defined in `mastery-rubric-stage1.md`. This validates that the system can objectively measure what the TA has learned.

- **TA learner-style conversation response.** The `ta_conversation.py` module generates learner-persona responses to teaching events, either via a stub (short rule-based sentences reflecting learned units) or via an optional LLM call constrained by the TA's current knowledge state and Stage One scope. The conversation prompt template (`ta_learner_conversation_prompt.md`) instructs the model to behave as a novice who only knows what has been taught.

- **Three demonstration scenarios.** `demo_scenarios.py` implements three scenarios that together validate the core loop:
  - **Scenario A (constrained selection):** Only `print_function` is taught; no problem in the bank is eligible because every problem also requires other units. Demonstrates that the knowledge state controls selection.
  - **Scenario B (success path):** `variable_assignment` and `print_function` are taught; `prob_var_001` becomes eligible; the TA produces correct code (stub or LLM); the evaluator reports PASS and proficient mastery.
  - **Scenario C (failure path):** Same teaching as B, but `force_fail_problem_ids` forces the TA to produce incorrect stub code; the evaluator reports FAIL and failing mastery.

- **Streamlit teacher-facing demo.** `streamlit_app.py` exposes all three scenarios through a web interface, showing teaching events, TA responses, problem selection, TA code, grading results, and mastery reports. Runs locally with `streamlit run streamlit_app.py`.

- **Seed resources.** The project contains curated seed data:
  - `knowledge-units-stage1.json`: 20 knowledge units covering variables, types, I/O, operators, conditionals, loops, and lists, each with prerequisites, descriptions, and example code.
  - `sample-problems-stage1.json`: 16 programming problems with test cases, knowledge-unit tags, difficulty levels, and targeted misconceptions.
  - `misconceptions-stage1.json`: 6 misconceptions (assign_vs_equal, off_by_one_range, string_int_concat, indent_error, comparison_in_if, list_index_one_based) with affected units, example incorrect/correct code, and remediation hints.
  - `problem-schema-stage1.md`: Schema definition for the problem format.

- **LLM prompt templates.** Two prompt templates govern LLM behavior:
  - `ta_code_generation_prompt.md`: Constrains code generation to learned units, injects active misconceptions, forbids advanced constructs.
  - `ta_learner_conversation_prompt.md`: Constrains conversation to novice learner persona within Stage One scope and learned units.

- **Comprehensive documentation and evaluation pack:**
  - `PROPOSAL.md`: Full project proposal with goals, interaction design, knowledge state design, mastery test design, risks, build order.
  - `STAGE_ONE_PROPOSAL.md`: Focused Stage One proposal.
  - `STAGE_ONE_EXIT_MEMO.md`: Closure memo establishing that Stage One goals are met.
  - `STAGE_ONE_CAPABILITY_AUDIT.md`: Detailed audit of what is implemented vs. stubbed, what is rule-based vs. LLM-backed, how fallbacks work, and how knowledge-state constraints are enforced.
  - `STAGE_ONE_SCENARIO_EVALUATION.md`: Evaluation of the three demo scenarios with setup, behavior, outcomes, and alignment to teacher goals.
  - `STAGE_ONE_REFLECTION.md`: Fit-for-purpose review of the 6 seed resources with identified gaps and recommended revisions.
  - `STAGE_ONE_REPRODUCIBILITY_GUIDE.md`: Instructions for reproducing both stub-mode and LLM-mode runs.

### Partially Completed

- **Misconception-driven behavior.** The seed data defines 6 misconceptions and the prompt templates include misconception injection, but the current prototype does not yet implement a misconception state that actively drives TA code generation or conversation. Scenario C simulates failure via `force_fail_problem_ids` and predetermined wrong code rather than through a misconception state that causes the LLM to produce error-consistent code. The architectural placeholder exists (misconception fields in knowledge state, misconception parameters in prompts), but the active misconception → behavioral effect pipeline is not yet operational.

- **Mastery aggregation across multiple problems.** The rubric defines pass-rate-based mastery across multiple attempts per unit, but the current prototype evaluates mastery from a single problem attempt per scenario. Multi-problem aggregation logic exists in the rubric but has not been exercised in the demo.

- **Session persistence.** No state or attempt history persists between runs. Each scenario starts from a fresh zero-knowledge state.

### Not Yet Started

- **Natural-language teaching interpretation.** Teaching is currently delivered via structured events (topic + knowledge_units + note). No system exists to parse free-form student text and extract knowledge-unit updates from it.

- **Unlearning and relearning logic.** There is no mechanism for the TA to unlearn a misconception, revert from a learned state, or transition through explicit relearning after correction. The state can move from unknown to learned but cannot yet move backward or through a correction cycle.

- **Cross-domain architecture.** The current system is Python-only. No shared domain layer, no domain-agnostic knowledge-state engine, and no cross-domain mastery logic exist.

- **Database domain.** Not designed, not seeded, not implemented.

- **AI Literacy domain.** Not designed, not seeded, not implemented.

- **Multi-turn dialogue state management.** The current system treats each teaching event independently. There is no conversation history, no multi-turn context, and no dialogue state that tracks what has been discussed across turns.

- **Knowledge decay or forgetting model.** The proposal mentions simplified forgetting, but no decay mechanism has been implemented.

- **Full evaluation methodology.** No systematic evaluation comparing teaching-to-state-change, no cross-domain evaluation, no comparative analysis with alternative approaches.

---

## 4. Final System Goal

The mature final system is a unified teachable-agent platform for computer science education that supports at minimum three domains — **Python Programming**, **Database**, and **AI Literacy** — with a shared architectural core and the capacity to extend to additional domains in the future. The system is not three separate teachable agents that happen to share a UI. It is one framework instantiated across three domains, with a single knowledge-state engine, a single misconception-and-relearning architecture, a single evaluation methodology, and domain-specific content layers that plug into the shared core.

### What the mature system must include

**Domain coverage:**
- **Python Programming:** Extending the current Stage One foundation to cover the full introductory Python curriculum (adding functions, dictionaries, tuples, file I/O, basic OOP concepts, error handling) and incorporating mature misconception-driven behavior, unlearning/relearning cycles, and multi-problem mastery aggregation.
- **Database:** Covering relational database fundamentals — tables, schemas, primary/foreign keys, SQL queries (SELECT, INSERT, UPDATE, DELETE), joins, grouping, filtering, normalization concepts — with TA behavior that demonstrates SQL misconceptions (e.g., confusing WHERE with HAVING, misunderstanding NULL, incorrect JOIN logic) and can be tested through query-based problems with result-set comparison.
- **AI Literacy:** Covering foundational concepts of artificial intelligence — what AI is and is not, supervised vs. unsupervised learning, training data and bias, classification vs. regression, overfitting, ethical considerations, limitations of AI systems — with TA behavior that demonstrates conceptual misconceptions (e.g., "AI understands meaning," "more data always helps," "AI is objective") and can be tested through scenario-based and explanation-based assessments rather than code execution.
- **Future domains (TBA):** The architecture must be extensible so that adding a new CS domain requires only a new domain content layer (knowledge units, misconceptions, problems, task types) plugged into the existing shared core, without modifying the core engines.

**What makes it one unified system:**
- A single `KnowledgeStateEngine` that represents, updates, and queries the TA's knowledge across all domains using the same data structure, the same state-transition logic, and the same misconception model.
- A single `MisconceptionEngine` that handles misconception activation, propagation to behavior, correction detection, unlearning, and relearning — regardless of whether the misconception is about Python indentation, SQL NULL semantics, or AI bias.
- A single `MasteryEvaluator` that computes mastery from domain-specific test results using a shared rubric framework, so that "proficient in Python loops" and "proficient in SQL joins" and "proficient in AI bias concepts" are all computed by the same logic and are directly comparable.
- A single `InteractionEngine` that manages the teach → respond → test → reflect loop across all domains, adapting task types (code execution for Python, query result comparison for Database, explanation evaluation for AI Literacy) while keeping the loop structure constant.

**What the mature user experience would be:**
A student opens the system and selects a domain (or the system presents available domains). They begin teaching the TA about that domain's concepts. The TA responds as a novice — asking questions, restating, expressing confusion — and its responses are constrained by what it has been taught in that domain. The student can request a test at any time; the system selects appropriate tasks from the domain's problem bank, the TA attempts them using only its current knowledge state, and results are shown with mastery levels. If the TA fails due to a misconception, the student sees the TA's work, diagnoses the error, and re-teaches. The system explicitly tracks whether the TA has unlearned the misconception and whether relearning has occurred. The student can switch domains, and the system maintains separate-but-comparable knowledge states for each domain. A cross-domain mastery dashboard shows how the TA is progressing in all domains.

**What the system must be capable of before final professor review:**
1. Demonstrate the full teach → state update → constrained behavior → test → mastery report loop in all three domains.
2. Demonstrate at least two misconception → wrong behavior → correction → unlearning → relearning cycles per domain.
3. Produce a mastery report that compares the TA's state across domains using the same evaluation framework.
4. Provide traceable evidence that the TA's behavior in every domain is governed by its knowledge state — never by the LLM's inherent knowledge — with guard mechanisms and fallback paths documented and testable.
5. Include an evaluation methodology that links teaching actions to state changes to mastery outcomes, not just "the demo works."

---

## 5. Why the Current Python Foundation Matters

### Why Python was the correct first domain

Python was chosen first for reasons that remain valid and that strengthen the broader project:

1. **Bounded, enumerable knowledge space.** Introductory Python has a well-defined set of concepts that can be listed, structured into knowledge units, and tagged with prerequisites. This made it possible to build a concrete knowledge-state model rather than a vague one.

2. **Executable correctness criterion.** Python programs can be run against test cases, producing objective pass/fail signals. This gave the project an automated, unambiguous mastery measurement from the start — something that would have been far harder in a purely conceptual domain like AI Literacy.

3. **Rich misconception literature.** Decades of CS education research document exactly what beginners get wrong in Python. This allowed the misconception catalog to be grounded in established findings rather than speculation.

4. **Foundation for extension.** The architecture built for Python — state tracker, teaching events, problem selector, code attempt generator, mastery evaluator, guard/fallback layer — was designed with domain-agnostic interfaces. The refactoring cost to generalize it to other domains is manageable precisely because it was built around the right abstractions from the start.

### What the current prototype has already validated

The Python Stage One prototype is not a toy. It validates the following claims with working, reproducible code:

- **Zero-knowledge initialization works.** The TA genuinely starts knowing nothing and can only act on what has been taught. This is demonstrated in Scenario A, where the TA cannot even attempt a problem because it has only been taught one unit.

- **Knowledge-state-constrained selection works.** The problem selector enforces a strict policy: only problems whose required units are all learned can be selected. This is not aspirational; it is implemented and tested.

- **Knowledge-state-constrained code generation works.** Both the stub path and the optional LLM path generate code that is constrained by the TA's learned units. The output guard rejects code that uses constructs the TA should not know. Fallback to stubs ensures deterministic behavior when the LLM fails or violates constraints.

- **Automated mastery evaluation works.** The evaluator runs code, compares outputs, and produces pass/fail verdicts and mastery levels. The rubric is defined, implemented, and demonstrated.

- **The full teach → test → report loop is closed.** A student can teach, the TA's state updates, a problem is selected, the TA attempts it, the result is graded, and a mastery report is produced. This loop — the core pedagogical mechanism — is operational.

### Why it anchors the credibility of the broader system

The Python prototype proves that the project's core ideas are implementable, not just theoretically interesting. When the project claims that a knowledge-state-constrained teachable agent can operate in Database or AI Literacy, it can point to the Python prototype as evidence that the mechanism works in at least one domain. Without this prototype, the broader system would be a set of claims without a working proof-of-concept.

### Why later domains should build from it

Later domains should extend from the Python foundation — not rebuild from scratch — because the Python prototype already embodies the correct architectural patterns: explicit state, deterministic selection logic, constrained generation with guard and fallback, automated evaluation, and a clean separation between domain content (knowledge units, problems, misconceptions) and domain-agnostic engines (state tracker, evaluator, interaction flow). The generalization task is to abstract these patterns into a shared core and then instantiate them for each new domain, not to re-invent them.

---

## 6. Core Research Gap

The gap this project addresses is not simply "few people have built teachable agents for CS." Many researchers have explored learning-by-teaching systems since Biswas, Leelawong, Schwartz, and others established the paradigm in the 2000s. The gap is deeper and more specific than a count of prior systems.

### Lack of unified teachable-agent architecture across CS domains

Existing teachable-agent systems in CS education are almost universally single-domain. Betty's Brain (Biswas et al.) operates in science domains. SimStudent (Matsuda et al.) works in algebra. Various programming tutors exist, but they are tutors, not teachable agents. When systems do cross domains, they are typically rebuilt from scratch for each domain, with no shared representation of what the agent knows, no shared mechanism for how it learns, and no shared framework for evaluating whether it has learned correctly. There is no established architecture that says: "Here is how you build a teachable agent for any CS domain, using a shared knowledge-state engine, shared misconception logic, and shared evaluation methodology." This gap means that every new domain requires re-engineering the agent from the ground up, and that cross-domain comparisons of teaching effectiveness are architecturally impossible.

### Lack of explicit knowledge-state-constrained learner behavior

Most LLM-based educational agents rely on the LLM's inherent knowledge, modulated by persona prompts. A "novice learner" persona tells the LLM to act confused, but the LLM still knows Python, SQL, and everything else in its training data. The constraint is social (persona) rather than structural (state). This means the agent's behavior is not genuinely governed by what it has been taught — it is governed by how well the prompt suppresses the LLM's actual knowledge. The result is leaky agents that sometimes "know" things they were never taught, breaking the pedagogical contract. The gap is the absence of systems where the agent's behavior is structurally constrained by an explicit knowledge state — where the agent literally cannot generate code using loops if loops have not been taught, enforced by guards and fallback logic rather than by prompt engineering alone.

### Lack of misconception-aware system design

Misconceptions in existing educational systems are typically treated as error patterns to be detected and remediated — something the tutor notices and corrects. In a teachable-agent context, misconceptions must be something the agent *has* and *exhibits* — the agent must produce wrong code or wrong explanations that are consistent with specific, documented misconceptions, so that the student can diagnose the error and correct it through re-teaching. This requires misconceptions to be first-class objects in the system's data model, with explicit representations, activation conditions, behavioral effects, and correction criteria. Very few systems model misconceptions this way; none do so across multiple CS domains within a unified framework.

### Lack of explicit unlearning and relearning logic

When a teachable agent holds a misconception and the student corrects it, what happens in the system? In most existing work, the answer is vague: the state is updated, the misconception goes away. But educationally, unlearning is not the same as never having learned. Unlearning requires the system to represent that the agent once held a wrong belief, that the wrong belief was corrected, and that the agent's new understanding is a relearning — potentially fragile, requiring reinforcement, and distinct from learning something for the first time. No existing teachable-agent framework models this distinction. The gap is the absence of explicit state transitions for misconception → correction → unlearning → relearning, with those transitions represented in the knowledge state and reflected in the agent's behavior and mastery evaluation.

### Lack of cross-domain mastery modeling

If a teachable agent operates in both Python and Database, how do you compare its mastery across domains? What does it mean for the TA to be "proficient in Python loops" and "developing in SQL joins"? Are these comparable statements? Can the student see a unified mastery dashboard? Existing work does not address this because existing work does not operate across domains. The gap is the absence of a mastery framework that is domain-agnostic in its computation logic but domain-specific in its content, allowing meaningful cross-domain comparison.

### Lack of integrated teaching-state-testing evaluation logic

Most teachable-agent evaluations measure either the agent's final performance (did it learn?) or the student's learning gains (did the student learn by teaching?). Few evaluations trace the full causal chain: student teaches concept X → agent's state for X changes from unknown to learned → agent is tested on X → agent's performance reflects the state change → the mastery report correctly captures the outcome. This chain — from teaching action to state change to behavioral consequence to evaluation — is what makes the system credible as a research contribution. The gap is the absence of evaluation designs that trace this chain explicitly and use it to validate that the system's mechanisms work as claimed.

### Lack of a shared framework making Python, Database, and AI Literacy comparable

These three domains differ in fundamental ways: Python produces executable code, Database produces SQL queries evaluated against result sets, and AI Literacy involves conceptual understanding evaluated through explanations and scenario analysis. A shared framework must accommodate these differences while maintaining a common structure for knowledge representation, misconception modeling, and mastery evaluation. No existing work demonstrates such a framework. The gap is not just "nobody has done Python + Database + AI Literacy"; it is that nobody has shown that a single teachable-agent architecture can handle domains with fundamentally different task types and evaluation methods while preserving a unified knowledge model.

---

## 7. Strongest Potentially Groundbreaking Contribution

The deepest reason this project could matter — the reason it could support a top-tier publication rather than just a system demo — is that it would be the first demonstration that **explicit knowledge-state-constrained agent behavior, combined with first-class misconception modeling and unlearning/relearning logic, can generalize across structurally different CS domains within a unified framework**.

This is not a claim about feature count. It is a claim about mechanism.

The specific mechanism is: a teachable agent whose behavior is at every moment structurally governed by an explicit knowledge state (not just a persona prompt), where that knowledge state includes not just "what the agent knows" but also "what it misunderstands" (misconceptions), "what it used to misunderstand and has been corrected on" (unlearning), and "what it has re-established after correction" (relearning) — and where this mechanism is shown to work not just in one domain but across Python, Database, and AI Literacy, with a single shared engine and domain-specific content layers.

### What makes it more than another teachable agent

Most teachable agents in the literature are proof-of-concept implementations in a single domain. They demonstrate that learning-by-teaching works (students learn when they teach an agent) but do not address the question of how to build a reusable framework. This project goes further: it claims that the framework itself — the knowledge-state engine, the misconception model, the unlearning/relearning logic, the evaluation chain — is the contribution, and the domains are instantiations that validate the framework's generality.

### What mechanism makes it paper-worthy

The paper-worthy mechanism is the **knowledge-state-constrained behavior pipeline**: the chain from explicit knowledge state → constrained agent action (code generation, query generation, explanation generation) → automated evaluation → mastery determination, with misconception modeling and unlearning/relearning as first-class components of the state. If this pipeline is shown to work in three structurally different domains, with traceable evidence that the state governs behavior and that misconceptions produce the predicted errors and corrections produce the predicted improvements, then the contribution is not "we built a bigger demo" but "we demonstrated a generalizable mechanism for state-constrained agent-based learning."

### What would make it weak

- If the final system is just three separate teachable agents with no shared mechanism.
- If the misconception logic is bolted on rather than central to the architecture.
- If unlearning/relearning is mentioned in the paper but not implemented or evaluated.
- If the evaluation only shows "the demo works" without tracing the teaching → state → behavior → mastery chain.
- If the knowledge-state constraint is enforced only by prompts and not by structural guards.
- If cross-domain comparison is not demonstrated (each domain evaluated in isolation).

### What would make it strong

- A single shared knowledge-state engine operating across three domains with domain-specific content layers.
- Explicit misconception state transitions (activation, behavioral effect, correction detection, unlearning, relearning) demonstrated with traceable evidence in every domain.
- Evaluation that traces the full chain: teaching action → state change → behavior change → mastery outcome.
- A clear demonstration that the framework, not just the domain content, is the reusable contribution.
- Evidence that the system's behavior is genuinely constrained by state, not leaked from the LLM — with guard mechanisms, fallback logic, and violation-detection documented and tested.

---

## 8. Why This Is Not Just Another Teachable Agent

Several lines of existing work might superficially resemble this project. It is essential to articulate why this project must not be conflated with them.

**Betty's Brain and its descendants** (Biswas et al., 2005–2020) established the teachable-agent paradigm in science education. Students teach a virtual agent by constructing concept maps; the agent reasons over the maps and can be quizzed. Betty's Brain is a landmark contribution, but it operates in a single domain (usually river ecosystems or thermoregulation), uses concept maps as its knowledge representation, does not model misconceptions as first-class objects, does not handle unlearning/relearning, and does not incorporate LLM-based behavior constrained by state.

**SimStudent** (Matsuda et al., 2013–2020) learns procedural skills from student demonstrations, primarily in algebra. It acquires production rules by induction and can generalize to new problems. SimStudent is a different paradigm: it learns from examples rather than from explanatory teaching, it operates in a single domain, and its internal representation (production rules) is domain-specific and not designed for cross-domain generalization.

**LLM-based "learning companions"** — various recent systems use LLMs to simulate study partners, tutors, or Socratic questioners. These are not teachable agents in the Biswas sense: the LLM already knows the domain, and the "learning" is simulated through persona prompts rather than through explicit state changes. The student is not genuinely teaching the agent; the agent is pretending to learn while actually knowing everything. This project differs fundamentally because the TA's knowledge state is an explicit data structure that governs behavior through structural constraints, not just through persona simulation.

**Multi-domain tutoring systems** (e.g., Carnegie Learning, ALEKS) cover multiple subjects, but they are tutors — they teach the student, not the other way around. Their architecture may share components across domains, but the pedagogical direction is reversed. This project's contribution is in the learning-by-teaching direction, where the student is the teacher and the agent is the constrained learner.

The distinction this project must maintain is: **the agent's behavior is structurally governed by an explicit knowledge state that changes only through student teaching, with misconceptions as first-class objects that produce predictable behavioral effects, and with unlearning/relearning as explicit state transitions — all within a framework that generalizes across multiple CS domains**. No existing system combines all of these properties.

---

## 9. Why Multi-Domain Alone Is Not Enough

If this project's contribution were "we built a teachable agent for Python, and then we built one for Database, and then we built one for AI Literacy," the contribution would be incremental. Three demos are not a framework. Each individual domain demo faces the objection: "this is just Betty's Brain for [domain X]" — a known paradigm applied to a new domain.

The real contribution must be the **shared mechanism**, not the domain count.

Adding Python + Database + AI Literacy is valuable only if it serves as evidence for a deeper claim: that the framework's core mechanisms (knowledge-state-constrained behavior, misconception modeling, unlearning/relearning logic, mastery evaluation) are genuinely domain-agnostic and can handle domains with fundamentally different task types (code execution, query evaluation, conceptual assessment) under a single architecture.

If each domain is implemented as a separate codebase with its own state model, its own misconception logic, and its own evaluation, then the project has not demonstrated a framework — it has demonstrated three independent systems that happen to appear in the same repository. That would be a weak contribution.

To avoid this, the project must enforce the following principle: **every domain must instantiate the same shared core engines, and the only domain-specific components must be content layers** (knowledge unit definitions, misconception catalogs, problem banks, task-type adapters). If this principle holds, then the multi-domain evidence supports the framework claim. If it does not hold, then the project has drifted into being a collection of demos — exactly what this blueprint warns against.

The way to detect this drift is straightforward: if adding a fourth domain would require modifying the shared engines (not just adding a new content layer), then the shared engines are not truly shared, and the framework claim is weakened.

---

## 10. Negative Scope: What This Project Is Not

The following framings are **explicitly rejected**. Treating the project in these terms weakens the contribution and must be avoided. Future work, documentation, and paper positioning must not collapse into these descriptions.

### 10.1 Rejected Framings

| Rejected framing | Why it is wrong |
|------------------|------------------|
| **A generic tutoring chatbot** | The TA does not tutor the student. The student teaches the TA. The agent’s behavior is constrained by an explicit knowledge state, not by a generic “helpful assistant” persona. |
| **A multi-domain educational product** | The contribution is not “we support Python, Database, and AI Literacy.” It is the unified framework (state engine, misconception lifecycle, evaluation chain) that generalizes across domains. Domain count is evidence for the framework, not the contribution. |
| **A larger demo** | The project is not “Stage One plus more domains and more problems.” It is the operationalization of a framework with state-constrained behavior, misconception/unlearning/relearning logic, and traceable evaluation. A “bigger demo” without these mechanisms is off track. |
| **A UI-first or deployment-first project** | Mechanism clarity and research contribution come first. UI polish, hosting, and deployment serve demonstration and evaluation; they do not define success. Prioritizing UI or deployment over the knowledge-state mechanism and misconception lifecycle is drift. |
| **A domain-count contribution** | Claiming “we built a teachable agent for three domains” is weak. The claim is “we built one framework that operates across three domains with shared engines and comparable mastery.” |
| **A simple prompt-based “pretend learner”** | The TA is not an LLM asked to “act like you don’t know Python.” Behavior must be structurally constrained by the knowledge state (guards, fallbacks, state-driven selection and generation). Without explicit state logic and enforcement, the system is not this project. |

### 10.2 Strong Framing to Reinforce

All communication about the project should reinforce:

- **Unified framework** — One architecture, one state model, one misconception lifecycle, one evaluation methodology; domains are content layers.
- **State-constrained learner behavior** — The agent can only use what the state records as learned; guards and fallbacks enforce this.
- **Misconception lifecycle** — Activation, behavioral effect, correction, unlearning, relearning are first-class, implemented, and evaluable.
- **Unlearning / relearning** — Explicit state transitions, not “misconception goes away”; history and mastery reflect correction and relearning.
- **Cross-domain mastery logic** — Same rubric, same thresholds, comparable mastery across domains; cross-domain dashboard is a consequence of the shared framework.

If a task, doc, or paper draft describes the project in a rejected framing or omits the strong framing above, treat it as misaligned and correct it before proceeding.

---

## 11. Full-System Architecture

The mature system architecture must be organized around a set of engines and layers, each with a clear purpose, clear ownership (shared vs. domain-specific), and clear interfaces. The following defines the major modules.

### 11.1 Domain Layer

**What it does:** Provides all domain-specific content — knowledge unit definitions, prerequisite graphs, misconception catalogs, problem/task banks, task-type adapters, and domain-specific evaluation logic.

**Why it exists:** To encapsulate everything that varies between Python, Database, and AI Literacy into a pluggable content layer, so that the rest of the system is domain-agnostic.

**Shared or domain-specific:** Domain-specific. Each domain provides its own content package. The domain layer's interface (what a "knowledge unit" looks like, what a "problem" looks like, what a "misconception" looks like) is defined by the shared core, but the content is domain-specific.

### 11.2 Knowledge State Engine

**What it does:** Maintains the TA's knowledge state as an explicit, structured, inspectable data object. Handles all state transitions: unknown → partially_learned → learned, misconception activation, misconception correction, unlearning, relearning. Provides query interfaces for downstream consumers (what does the TA know? what misconceptions are active? what has been unlearned and relearned?).

**Why it exists:** This is the single source of truth for the TA's knowledge. Without it, the TA's behavior would be governed by the LLM's inherent knowledge rather than by what the student has taught. This engine is the structural constraint that makes the system a teachable agent rather than a chatbot with a persona.

**Shared or domain-specific:** Shared. The engine operates over domain-provided knowledge units but does not contain domain-specific logic. The same engine manages Python state, Database state, and AI Literacy state.

### 11.3 Interaction Engine

**What it does:** Manages the overall teach → respond → test → reflect loop. Receives teaching input from the student, routes it to the appropriate processing modules, orchestrates TA responses, handles test requests, and assembles results for presentation. Manages conversation flow and session state.

**Why it exists:** To provide a consistent user experience across domains and to ensure that the pedagogical loop is correctly structured regardless of which domain is active.

**Shared or domain-specific:** Shared, with domain-specific hooks for task presentation and evaluation. The loop structure (teach → update state → respond → select task → TA attempts → evaluate → report) is the same in every domain. The task types differ (run code vs. run query vs. evaluate explanation), so the engine delegates to domain-specific task adapters.

### 11.4 Learner Dialogue Engine

**What it does:** Generates the TA's conversational responses during teaching interactions. Produces novice-learner-persona text that is constrained by the TA's current knowledge state: the TA can only discuss concepts it has been taught, asks questions about unfamiliar ideas, restates its understanding, and expresses confusion when taught contradictory information.

**Why it exists:** The conversational response is how the student perceives the TA's learning. If the TA responds as if it already knows everything, the learning-by-teaching mechanism breaks down. The dialogue engine ensures that the TA's conversational behavior is consistent with its knowledge state.

**Shared or domain-specific:** Shared engine with domain-specific prompt templates. The mechanism for constraining responses by knowledge state is the same; the vocabulary, examples, and domain context vary.

### 11.5 Task/Problem Engine

**What it does:** Selects or generates tasks/problems from the domain's task bank based on the TA's current knowledge state. Applies selection rules: only tasks whose required knowledge units are all at the appropriate state (learned, partially_learned) are eligible. Can filter by difficulty, by targeted misconceptions, and by mastery gaps.

**Why it exists:** To ensure that the TA is only tested on what it has been taught, and that tests are targeted to reveal specific mastery levels or misconceptions.

**Shared or domain-specific:** Shared selection logic, domain-specific task banks and task-type adapters. The rule "only select tasks whose required units are learned" is domain-agnostic. The tasks themselves (Python code problems, SQL query problems, AI concept questions) are domain-specific.

### 11.6 TA Attempt Engine

**What it does:** Generates the TA's attempt at a given task, constrained by its current knowledge state and active misconceptions. For Python, this means generating Python code. For Database, this means generating SQL queries. For AI Literacy, this means generating explanations or scenario analyses. Includes guard logic to reject outputs that use concepts the TA has not been taught, and fallback logic to provide deterministic stub outputs when the LLM fails or violates constraints.

**Why it exists:** This is where the TA's "understanding" becomes visible and testable. The attempt must be consistent with the knowledge state; otherwise the system is not a teachable agent.

**Shared or domain-specific:** Shared guard/fallback architecture, domain-specific generation logic. The principle "constrain output by knowledge state" is shared. The output format and validation rules differ by domain.

### 11.7 Mastery Evaluator

**What it does:** Evaluates the TA's task attempts against expected outcomes. For Python, runs code and compares stdout. For Database, runs queries and compares result sets. For AI Literacy, evaluates explanations against rubric criteria (potentially with LLM-assisted evaluation). Computes per-unit and overall mastery levels using a shared rubric framework.

**Why it exists:** To provide objective mastery measurement that drives the reflective loop. Without automated evaluation, the student has no concrete signal to guide their teaching.

**Shared or domain-specific:** Shared rubric framework (pass rates, mastery levels, aggregation logic), domain-specific evaluation adapters (code execution, query execution, explanation scoring).

### 11.8 Misconception / Unlearning / Relearning Engine

**What it does:** Manages the lifecycle of misconceptions: activation (when does the TA acquire a misconception?), behavioral effect (how does the misconception change the TA's code, queries, or explanations?), detection (how is a misconception identified from test results or conversation?), correction (what must the student do to correct it?), unlearning (removing the misconception from active state), and relearning (re-establishing correct understanding after correction). Maintains a misconception history for each knowledge unit.

**Why it exists:** This is one of the most important engines in the system. Without it, the TA's errors are random or predetermined, not educationally meaningful. With it, the TA's errors are traceable to specific misconceptions, and the student's corrective teaching has specific, measurable effects.

**Shared or domain-specific:** Shared engine with domain-specific misconception catalogs. The lifecycle logic (activate → affect behavior → detect → correct → unlearn → relearn) is the same in every domain. The specific misconceptions (off-by-one in Python, NULL confusion in SQL, "AI understands meaning" in AI Literacy) are domain-specific.

### 11.9 History / Trace Layer

**What it does:** Records the full history of teaching events, state transitions, task attempts, evaluation results, misconception activations, corrections, and relearning events. Provides trace data that can be used for evaluation, debugging, and research analysis.

**Why it exists:** To support the evaluation methodology. Without traceable history, it is impossible to demonstrate the teaching → state change → behavior → mastery chain that validates the system's claims. The trace layer also supports session persistence and multi-session learning.

**Shared or domain-specific:** Shared. The trace format is the same regardless of domain.

### 11.10 Guard / Fallback Layer

**What it does:** Provides safety mechanisms that ensure the TA's behavior remains constrained by its knowledge state even when the LLM attempts to leak knowledge. Includes output guards (rejecting code/queries/explanations that use untaught concepts), input validation (ensuring teaching events map to valid knowledge units), and fallback paths (providing deterministic stub behavior when LLM outputs are rejected).

**Why it exists:** LLMs inherently know more than the TA is supposed to know. Without guards, the TA would occasionally produce correct answers using knowledge it was never taught, destroying the educational validity of the system. The guard layer is what makes the knowledge-state constraint structural rather than merely aspirational.

**Shared or domain-specific:** Shared architecture, domain-specific guard rules. The principle "reject outputs that violate knowledge-state constraints" is shared. The specific forbidden patterns (Python: no `def`/`class` if functions not taught; SQL: no subqueries if subqueries not taught) are domain-specific.

---

## 12. Unified Knowledge State Logic

The knowledge state is the single most important data structure in the entire system. It is not a secondary feature or a metadata annotation. It is the structural core that makes the system a teachable agent rather than a chatbot.

### What the unified knowledge state must represent

For every knowledge unit across every domain, the state must include:

**Domain.** Which domain this unit belongs to (Python, Database, AI Literacy). This allows cross-domain queries and comparison.

**Knowledge unit identifier and metadata.** The unit ID, human-readable name, description, topic group, and prerequisites. These come from the domain layer.

**Learning status.** One of: `unknown` (the TA has never been taught this), `partially_learned` (the TA has received some teaching but not enough for confidence), `learned` (the TA has been taught this concept and has demonstrated understanding through conversation or testing), `misconception` (the TA has acquired an incorrect understanding of this concept).

**Misconception details.** If the unit's status is `misconception` or if misconceptions are active alongside a learned status: which specific misconception IDs are active, when they were activated, what triggered them (incorrect teaching, ambiguous teaching, initial seeding), and whether they have been flagged for correction.

**Confidence.** A numerical value (0.0 to 1.0) representing the system's estimate of how solidly the TA has learned this unit. Confidence increases with consistent correct teaching, reinforcement, and successful test performance. Confidence decreases when teaching is contradictory, when test results are poor, or when misconceptions are active.

**Evidence of teaching.** A record of all teaching events that targeted this unit: timestamps, teaching content summaries, and the state transition each event caused. This supports the evaluation chain: we can trace exactly when and how the TA was taught each concept.

**Evidence of testing.** A record of all task attempts that involved this unit: problem IDs, pass/fail results, the TA's output, and the mastery level computed at each point. This supports mastery tracking over time.

**Evidence of correction.** If the TA held a misconception that was later corrected, the correction event is recorded: what misconception was corrected, when, what teaching triggered the correction, and what the state transitioned to.

**Evidence of relearning.** After a misconception is corrected and the TA transitions through unlearning, subsequent teaching and testing on the same unit constitutes relearning. The state must distinguish first-time learning from relearning, because relearning may be more fragile and may require additional reinforcement.

**Mastery history.** A time-series of mastery levels for this unit, computed from accumulated test results. This allows the student and the system to see whether mastery is improving, stable, or regressing.

### Why this must remain the single source of truth

Every component of the system that needs to know "what does the TA know?" must query this state. The LLM is not the source of truth. The conversation history is not the source of truth. The state is the source of truth. This principle must be enforced architecturally: the dialogue engine receives the state as input and must constrain its output accordingly; the task engine queries the state to determine eligible tasks; the attempt engine receives the state and must generate output consistent with it; the evaluator updates the state based on results.

If any component of the system bypasses the state — if the LLM generates a response based on its own knowledge rather than the state, and no guard catches it — then the system's educational validity is compromised. The student would be teaching an agent that does not actually learn from their teaching, which destroys the pedagogical mechanism.

The unified nature of the state is also essential for cross-domain comparison. If Python, Database, and AI Literacy each had their own state format, cross-domain mastery dashboards and evaluation analyses would require ad-hoc translation. By using a single state format, the system can compute cross-domain statistics (e.g., "the TA is proficient in 80% of Python units and 40% of Database units") without domain-specific adapters.

---

## 13. Misconception, Unlearning, and Relearning Logic

This section describes the most distinctive and research-significant mechanism in the entire system. Misconception handling is not a secondary feature, not a "nice-to-have," not something to add after the core is working. It is a core architectural component that must be designed, implemented, and evaluated with the same rigor as the knowledge state engine itself.

### How wrong teaching can happen

The TA can acquire misconceptions through several pathways:

1. **Incorrect student teaching.** The student explains a concept wrongly (e.g., "range(5) gives you 1 through 5" or "= and == are the same thing"). The system detects that the teaching content contradicts the correct understanding of the relevant knowledge unit and activates the corresponding misconception.

2. **Ambiguous student teaching.** The student's explanation is incomplete or ambiguous in a way that leaves room for misinterpretation (e.g., teaching loops without explaining that range is exclusive of the upper bound). The system may activate a misconception with lower confidence, reflecting the ambiguity.

3. **Pre-seeded misconceptions.** Some misconceptions may be seeded as defaults — the system starts with the TA holding common beginner errors that the student must actively correct. This mirrors the educational reality that novices often come with pre-existing misconceptions from informal learning.

4. **Misconception transfer.** In some cases, a misconception in one concept may propagate to related concepts (e.g., a misconception about `=` vs. `==` affects both variable assignment understanding and conditional logic). The misconception engine must track these dependencies.

### How misconceptions become active

When a misconception is activated, it is recorded in the knowledge state for the affected unit(s):
- The misconception ID is added to the unit's active misconception list.
- The activation timestamp and trigger (which teaching event or which default seeding) are recorded.
- The unit's learning status may change (e.g., from `learned` to `misconception`, or the unit may remain `learned` with an active misconception overlay, depending on severity).

### How misconceptions affect dialogue and task performance

Active misconceptions must have observable behavioral effects — otherwise they are invisible metadata that serve no educational purpose.

**In dialogue:** When the TA discusses a concept for which it holds a misconception, it should express the misconception in its conversational response. For example, if the TA holds `off_by_one_range`, it might say: "So range(5) gives me the numbers 1, 2, 3, 4, 5?" This gives the student a diagnostic signal.

**In task attempts:** When the TA attempts a problem that involves a misconceived concept, it should produce output that reflects the misconception. For example, if the TA holds `off_by_one_range` and is asked to print numbers 0 through 4, it might produce `for i in range(5): print(i + 1)`, printing 1 through 5 instead. The error is not random — it is consistent with the specific misconception the TA holds.

**In the prompt pipeline:** The misconception engine injects active misconceptions into the LLM prompt, instructing the model to produce output that reflects those specific errors. The guard layer must verify that the output is consistent with the misconception (not just randomly wrong) — though this verification may be approximate in early stages.

### How correction works

Correction occurs when the student re-teaches the concept in a way that directly addresses the misconception. The system must detect that the new teaching contradicts the active misconception and is consistent with the correct understanding. This detection may involve:
- Matching the teaching content against the misconception's remediation criteria (defined in the misconception catalog).
- Using LLM-based analysis of the student's teaching to determine whether it addresses the specific misconception.
- Requiring explicit reinforcement (the student must teach the concept correctly at least once after the misconception was active, and the TA must acknowledge the correction in conversation).

### How unlearning is represented

Unlearning is the transition from holding a misconception to no longer holding it. In the knowledge state, this is represented as:
- The misconception is moved from `active` to `unlearned` status.
- The unlearning timestamp and trigger (which teaching event prompted the correction) are recorded.
- The unit's learning status transitions: from `misconception` to a transitional state (e.g., `corrected` or `partially_learned_post_correction`), not directly back to `learned`. This transitional state reflects the educational reality that simply being told the correct answer does not immediately produce robust understanding.

### How relearning is represented

Relearning is the process of re-establishing correct understanding after a misconception has been unlearned. In the knowledge state:
- Additional teaching events on the corrected concept accumulate evidence of relearning.
- Successful test performance on problems involving the previously misconceived concept provides evidence that the relearning is effective.
- The unit's status transitions from the post-correction transitional state back to `learned` (or `partially_learned`) based on the evidence.
- The relearning history is preserved: the state records that this unit was first learned (possibly incorrectly), held a misconception, was corrected, and was relearned. This history is available for evaluation and for display to the student.

### How mastery is recalculated

After an unlearning/relearning cycle, the mastery evaluator must reconsider the unit's mastery level:
- Test results obtained while the misconception was active may be weighted differently from results obtained after relearning.
- The mastery level should reflect current understanding, not historical performance — but the history is preserved for research analysis.
- A unit that has been through a misconception → correction → relearning cycle may require additional test evidence before being marked `proficient`, reflecting the fragility of relearned knowledge.

### Why this is one of the strongest distinguishing features

The misconception/unlearning/relearning mechanism is the feature that most clearly separates this project from simpler teachable-agent implementations. Most systems treat the TA's knowledge as monotonically increasing: teach more → know more. This system models knowledge as non-monotonic: the TA can learn incorrectly, exhibit specific errors, require correction, undergo unlearning, and relearn — and every step of this process is explicitly represented, behaviorally observable, and evaluable. This is not only more educationally realistic; it also provides far richer research data (how do students diagnose and correct misconceptions?) and far stronger evaluation evidence (can we trace the misconception → correction → relearning chain?).

---

## 14. Domain Design Principles

Before defining individual domains, the following shared design principles must govern every domain in the system. These principles ensure that domains are comparable, that the shared core engines work correctly, and that adding a new domain is a content-authoring task rather than a systems-engineering task.

### Knowledge-unit design

Every domain must define its knowledge as a set of discrete, enumerable **knowledge units**. Each unit must have:
- A unique ID within the domain.
- A human-readable name and description.
- A topic group (for organizing related units).
- A list of prerequisite units (within the same domain).
- Example correct understanding.
- Example incorrect understanding (linked to misconceptions).

Knowledge units must be granular enough that each can be independently taught, tested, and misconceived, but not so granular that the unit count becomes unmanageable. A target range of 20–50 units per domain is appropriate for the first version.

### Task design

Every domain must provide a **task bank** of assessable items. Each task must:
- List the knowledge units it requires.
- Specify a difficulty level.
- List targeted misconceptions (which misconceptions the task is designed to reveal).
- Include evaluation criteria (test cases for code, expected result sets for queries, rubric criteria for explanations).

Tasks must be automatically or semi-automatically evaluable. Fully subjective tasks that require human grading are not acceptable for the core evaluation loop, though they may supplement it.

### Mastery examination

Every domain must support mastery computation using the shared rubric framework. The rubric uses pass rates over attempted tasks per knowledge unit, with shared thresholds (failing / developing / proficient). Domains may define additional mastery tiers (e.g., `mastered` for transfer-level performance) as long as the base tiers are present and comparable across domains.

### Misconception representation

Every domain must provide a **misconception catalog** with the same structure: misconception ID, description, affected knowledge units, example incorrect and correct behavior, remediation criteria. The misconception engine operates over this catalog domain-agnostically.

### Learner-style interaction

In every domain, the TA must respond as a novice learner: restating, asking questions, expressing confusion, and never tutoring the student. The persona is consistent; only the domain vocabulary changes.

### Where domains may differ

Domains may differ in:
- **Task type.** Python uses code execution; Database uses query execution against a schema; AI Literacy uses explanation/scenario evaluation.
- **Evaluation method.** Exact stdout comparison vs. result-set comparison vs. rubric-based scoring.
- **Prerequisite structure.** Python has a relatively linear prerequisite chain; Database may have a more tree-like structure; AI Literacy may have fewer hard prerequisites.
- **Misconception character.** Python misconceptions are procedural (wrong syntax, wrong semantics). Database misconceptions may be both syntactic (wrong SQL) and conceptual (wrong mental model of joins). AI Literacy misconceptions are primarily conceptual.

### Where domains must remain comparable

Domains must remain comparable in:
- **Knowledge state structure.** Same fields, same status values, same confidence model.
- **Mastery computation.** Same rubric, same thresholds, same aggregation logic.
- **Misconception lifecycle.** Same activation → behavior → correction → unlearning → relearning pipeline.
- **Interaction loop.** Same teach → respond → test → reflect structure.
- **Evaluation methodology.** Same teaching → state change → behavior → mastery chain analysis.

---

## 15. Domain Plan: Python Programming

### What has already been done

The Stage One prototype covers Introductory Python with 20 knowledge units (variables, types, I/O, operators, conditionals, loops, lists), 16 sample problems, 6 misconceptions, a functioning state tracker, problem selector, code attempt generator (stub + optional LLM), mastery evaluator, and three demonstration scenarios. The interaction protocol, mastery rubric, prompt templates, and evaluation pack are documented.

### What remains to be extended

The Python domain must mature from a Stage One prototype to a full domain within the unified framework. This involves:

1. **Expanding knowledge units.** Add units for functions (`function_definition`, `function_parameters`, `return_statement`, `function_calls`, `scope_basics`), dictionaries (`dictionary_creation`, `dictionary_access`), tuples (`tuple_basics`), string methods (`string_methods`, `string_formatting`), error handling (`error_types`, `basic_debugging`), and potentially file I/O and basic OOP. Target: 35–50 units total.

2. **Expanding the problem bank.** Add problems for the new units, targeting at least 2 problems per unit per difficulty tier. Target: 80–150 problems.

3. **Expanding the misconception catalog.** Add misconceptions for the new units: `print_vs_return`, `mutable_default`, `loop_variable_scope`, `global_vs_local`, `list_aliasing`, `integer_division`, etc. Target: 15–30 misconceptions.

4. **Activating misconception-driven behavior.** Move from `force_fail_problem_ids` to actual misconception-driven code generation: the TA's code should reflect its active misconceptions through the prompt injection → constrained generation → guard pipeline.

5. **Implementing unlearning/relearning.** When the student corrects a misconception, the state should transition through the unlearning → relearning cycle as defined in Section 13.

6. **Multi-problem mastery aggregation.** Exercise the rubric's multi-problem aggregation: mastery levels computed from pass rates over multiple problems per unit, not just single-attempt pass/fail.

7. **Natural-language teaching (pilot).** Accept free-form student text, use LLM to extract knowledge-unit updates, apply them to the state. Begin with a constrained pilot (e.g., teaching one concept per message) before supporting free-form multi-concept teaching.

### Later-stage Python topics

Topics for later addition include: recursion, list comprehensions, lambda functions, exception handling (`try`/`except`), modules and imports, basic classes and objects, file reading and writing. These should be added only after the core framework is stable and the other domains are operational.

### Mature Python mastery logic

In the mature Python domain, mastery should incorporate difficulty tiers: `proficient` requires passing remember and apply problems; `mastered` requires also passing transfer-level problems. Misconception history should be visible in the mastery report: "The TA was proficient in loops but had corrected misconception off_by_one_range."

### Important misconceptions

The Python domain has well-documented misconceptions from CS education research: assignment vs. comparison confusion, off-by-one errors in ranges, string-integer concatenation errors, indentation errors, print vs. return confusion, mutable default argument bugs, scope confusion, integer division surprises, list aliasing misconceptions, and operator precedence errors. These should be drawn from the literature (e.g., work by Kaczmarczyk, Pea, Sorva) and mapped to knowledge units.

### How Python supports the full framework argument

Python is the domain where the framework is most mature and best tested. It serves as the reference implementation: if the misconception/unlearning/relearning pipeline works in Python, we have concrete evidence that it can work in other domains. Python's executable nature provides the strongest automated evaluation signal (run code, compare output), making it the cleanest domain for demonstrating the teaching → state → behavior → mastery chain.

---

## 16. Domain Plan: Database

### Domain learning scope

The Database domain covers relational database fundamentals as typically taught in an introductory database course. The focus is on conceptual understanding of relational structure and practical SQL query writing.

### Candidate knowledge units

- **Relational model:** `table_concept`, `row_and_column`, `primary_key`, `foreign_key`, `schema_definition`, `data_types_sql`
- **Basic SQL:** `select_statement`, `where_clause`, `insert_statement`, `update_statement`, `delete_statement`, `order_by`, `limit`
- **Filtering and conditions:** `comparison_operators_sql`, `logical_operators_sql` (AND, OR, NOT), `like_operator`, `in_operator`, `between_operator`, `null_handling` (IS NULL, IS NOT NULL)
- **Aggregation:** `count_function`, `sum_avg_functions`, `group_by`, `having_clause`
- **Joins:** `inner_join`, `left_join`, `join_conditions`, `self_join`
- **Normalization concepts:** `functional_dependency`, `first_normal_form`, `second_normal_form`, `third_normal_form`

Target: 25–35 units.

### Candidate misconceptions

- `where_vs_having`: Using WHERE instead of HAVING for aggregate conditions, or vice versa.
- `null_equality`: Comparing with `= NULL` instead of `IS NULL`.
- `join_cartesian_product`: Omitting the join condition, producing a Cartesian product.
- `group_by_missing_column`: Selecting a non-aggregated column without including it in GROUP BY.
- `update_without_where`: Issuing UPDATE without a WHERE clause, affecting all rows.
- `delete_without_where`: Issuing DELETE without a WHERE clause, deleting all rows.
- `like_wildcard_confusion`: Confusing `%` (any characters) with `_` (single character).
- `foreign_key_direction`: Misunderstanding which table holds the foreign key in a one-to-many relationship.
- `inner_vs_left_join`: Not understanding that INNER JOIN excludes non-matching rows.
- `normalization_overkill`: Over-normalizing to the point of impracticality, or confusing normalization forms.

Target: 10–20 misconceptions.

### Interaction modes

Teaching a TA about databases involves:
- **Conceptual explanation:** "A primary key uniquely identifies each row in a table."
- **Schema demonstration:** "Imagine a table called `students` with columns `id`, `name`, `grade`."
- **Query explanation:** "To get all students with grade above 80, you write: `SELECT * FROM students WHERE grade > 80`."
- **Relationship teaching:** "The `enrollments` table has a `student_id` column that references the `students` table."

The TA responds as a novice: "So a primary key is like a name tag for each row? Can two rows have the same primary key?"

### Task types

Database tasks differ fundamentally from Python tasks:
- **Query-writing tasks:** "Write a SELECT statement to find all students with grade above 80." The TA produces a SQL query; the system executes it against a predefined schema with sample data and compares the result set to the expected result set.
- **Schema-interpretation tasks:** "Given this schema, explain what the foreign key `student_id` in the `enrollments` table means." The TA produces an explanation evaluated against rubric criteria.
- **Error-identification tasks:** "This query is wrong: `SELECT * FROM students WHERE grade = NULL`. What is the error?" The TA must identify the misconception.

### Mastery meaning

Mastery in Database means the TA can write correct SQL queries, interpret schemas, understand join logic, and apply normalization concepts — as demonstrated through tasks, not conversation. "Proficient in SQL joins" means the TA passes 80%+ of join-related query tasks with correct result sets.

### Why Database stresses the framework differently from Python

Database stresses the framework because:
1. **Evaluation is result-set comparison, not stdout comparison.** Row order may not matter; column types may differ; NULL handling introduces complexity. The mastery evaluator must be extended with a result-set comparator.
2. **Misconceptions are both syntactic and conceptual.** `null_equality` is syntactic (wrong SQL); `foreign_key_direction` is conceptual (wrong mental model). The misconception engine must handle both types.
3. **Task setup requires schema and data.** Each task needs a database schema and sample data, adding a content dimension that Python tasks do not have.
4. **Some tasks are not executable.** Schema-interpretation and normalization tasks may require explanation-based evaluation (rubric or LLM-assisted), which is a different evaluation modality.

These differences are precisely what make Database valuable for validating the framework: if the same knowledge-state engine, misconception lifecycle, and mastery rubric can handle both Python code and SQL queries, the framework's generality is credibly demonstrated.

---

## 17. Domain Plan: AI Literacy

### Domain learning scope

AI Literacy covers foundational concepts of artificial intelligence, aimed at students who may not be computer science majors but need to understand AI as informed citizens and future professionals. This is a conceptual domain with no code execution, which stress-tests the framework's ability to handle non-executable task types.

### Candidate knowledge units

- **Foundations:** `what_is_ai`, `narrow_vs_general_ai`, `ai_vs_automation`, `brief_history_of_ai`
- **Machine learning basics:** `supervised_learning`, `unsupervised_learning`, `training_data`, `features_and_labels`, `model_concept`, `prediction_vs_classification`, `regression_basics`
- **Data and bias:** `data_quality`, `bias_in_data`, `bias_in_models`, `fairness_concepts`, `representative_data`
- **Model behavior:** `overfitting`, `underfitting`, `generalization`, `accuracy_vs_precision_recall`, `confidence_scores`
- **AI applications:** `natural_language_processing_basics`, `computer_vision_basics`, `recommendation_systems_basics`
- **Ethics and society:** `ai_ethics_overview`, `transparency_and_explainability`, `human_in_the_loop`, `ai_limitations`, `societal_impact_of_ai`

Target: 25–35 units.

### Candidate misconceptions

- `ai_understands_meaning`: Believing that AI models like LLMs understand language the way humans do.
- `more_data_always_better`: Believing that adding more data always improves model performance, regardless of data quality or relevance.
- `ai_is_objective`: Believing that AI decisions are inherently unbiased because they are made by machines.
- `ai_learns_like_humans`: Believing that machine learning works like human learning (experience, intuition, understanding).
- `accuracy_is_sufficient`: Believing that high accuracy means the model is good, ignoring class imbalance, precision/recall trade-offs.
- `ai_can_do_anything`: Believing that current AI systems are general-purpose intelligences with broad capabilities.
- `training_equals_programming`: Believing that training a model is the same as writing a program with explicit rules.
- `correlation_implies_causation_ai`: Believing that if a model finds a pattern, the pattern is causal.
- `black_box_means_useless`: Believing that if a model is not fully explainable, it should not be used.
- `ai_replaces_all_human_judgment`: Believing that AI should replace rather than augment human decision-making.

Target: 10–20 misconceptions.

### Interaction modes

Teaching a TA about AI Literacy involves:
- **Conceptual explanation:** "Supervised learning is when you train a model on labeled examples — data where the correct answer is already known."
- **Analogy and example:** "Think of it like studying with flashcards: you see the question and the answer, and you learn to match them."
- **Misconception correction:** "No, AI doesn't understand language like we do. It finds patterns in text data, but it doesn't have meaning or comprehension."
- **Scenario discussion:** "If a hiring AI is trained on historical data where most managers were male, the AI might learn that male candidates are better — even though that's bias, not truth."

The TA responds as a novice: "So supervised learning is like a teacher giving you the answers to study? Does unsupervised learning mean there's no teacher at all?"

### Task types

AI Literacy tasks differ from both Python and Database tasks because they assess conceptual understanding rather than executable output:
- **Explanation tasks:** "Explain what overfitting is in your own words." The TA produces an explanation evaluated against rubric criteria (must mention: model performs well on training data, poorly on new data; relates to memorization vs. generalization).
- **Scenario analysis tasks:** "A bank uses an AI to approve loans. The AI was trained on 10 years of loan data. What potential bias issues should the bank consider?" The TA produces an analysis evaluated for mention of historical bias, demographic representation, and outcome fairness.
- **Concept distinction tasks:** "What is the difference between supervised and unsupervised learning?" Evaluated for correct identification of key differences (labeled vs. unlabeled data, prediction vs. clustering, etc.).
- **True/false with justification:** "True or false: AI models are objective because they use math. Explain your reasoning." Evaluated for correctly identifying the statement as false and explaining why (data bias, design choices, etc.).

### Mastery meaning

Mastery in AI Literacy means the TA can correctly explain AI concepts, identify misconceptions, analyze scenarios for bias and ethical issues, and distinguish between related concepts — as demonstrated through explanation and scenario tasks, evaluated against rubric criteria. "Proficient in bias concepts" means the TA passes 80%+ of bias-related tasks with explanations that meet the rubric criteria.

### Why AI Literacy is a serious domain within the unified framework rather than just general discussion

AI Literacy might appear to be "just conversation" rather than a real domain with testable knowledge. This appearance is wrong, and the project must resist it.

AI Literacy has:
- **Discrete, enumerable knowledge units** (supervised learning, overfitting, data bias, etc.) that are either known or unknown.
- **Specific, documented misconceptions** (AI is objective, more data is always better, AI understands meaning) that produce predictable wrong answers in scenario tasks.
- **Assessable tasks** with rubric-based evaluation criteria that can distinguish correct from incorrect understanding.
- **A prerequisite structure** (understanding training data before understanding overfitting; understanding bias in data before understanding bias in models).

What makes AI Literacy particularly valuable for the framework is that it forces the framework to handle a domain where evaluation is not automated stdout comparison. If the shared mastery evaluator can compute mastery for AI Literacy using rubric-based scoring with the same rubric framework that computes mastery for Python using code execution, then the framework's generality extends beyond executable domains — a significantly stronger claim.

---

## 18. Evaluation Logic for the Full System

Evaluation is not an afterthought. It is the mechanism that transforms the project from a system demo into a research contribution. Without rigorous evaluation, the project cannot support the claims it needs to make.

### TA-level evaluation

At the most basic level, evaluation must verify that the TA behaves as intended:
- **Does the TA start with zero knowledge?** Verified by attempting tasks before any teaching and confirming that the TA cannot produce correct output.
- **Does the TA's behavior reflect its knowledge state?** Verified by teaching specific concepts and confirming that the TA's task attempts use only those concepts.
- **Does the TA's behavior reflect its misconceptions?** Verified by activating misconceptions and confirming that the TA produces error-consistent output.
- **Does the guard layer prevent knowledge leakage?** Verified by testing edge cases where the LLM might leak untaught knowledge and confirming that guards catch violations.

### Teaching-to-state-change evaluation

This evaluates whether teaching actions produce the expected state changes:
- Teaching concept X should move unit X from `unknown` to `partially_learned` or `learned`.
- Teaching concept X incorrectly should activate the corresponding misconception.
- Corrective teaching should trigger unlearning of the misconception.
- Reinforcing correct teaching after correction should produce relearning.

This is traced through the history/trace layer: for each teaching event, the state before and after must be recorded and compared.

### Mastery evaluation

This evaluates whether the mastery computation correctly reflects the TA's state:
- A TA that has been correctly taught concept X and passes all X-related tasks should be rated `proficient` on X.
- A TA that holds a misconception on X and fails X-related tasks should be rated `failing` on X.
- A TA that has undergone correction and relearning on X should show a mastery trajectory: failing → developing → proficient.

### Domain-level evaluation

For each domain, evaluation must demonstrate:
- The full teach → state update → constrained behavior → test → mastery report loop works.
- At least two misconception → correction → unlearning → relearning cycles are demonstrated.
- Mastery levels computed from the shared rubric are meaningful within the domain.
- The domain's task evaluation method (code execution, query execution, explanation scoring) produces reliable results.

### System-level evaluation

Across the entire system, evaluation must demonstrate:
- The shared knowledge-state engine operates correctly in all domains without domain-specific modifications.
- The shared misconception lifecycle (activation → behavior → correction → unlearning → relearning) operates correctly in all domains.
- Cross-domain mastery comparison is meaningful: a mastery report showing "proficient in Python, developing in Database, failing in AI Literacy" reflects genuine differences in the TA's state, not artifacts of domain-specific evaluation quirks.
- Adding a new domain required only a content layer, not engine modifications.

### What evidence would support the main claim

The main claim is: "We present a unified framework for knowledge-state-constrained, misconception-aware teachable agents in CS education." The strongest evidence for this claim would be:

1. **Three-domain demonstration** with all three domains operating under the same shared engines.
2. **Traced misconception cycles** in each domain, showing that the same misconception lifecycle logic handles Python code errors, SQL query errors, and AI concept misunderstandings.
3. **Cross-domain mastery dashboard** showing comparable mastery levels computed by the same rubric.
4. **Knowledge-state constraint verification** showing that guards and fallbacks prevent LLM knowledge leakage in all domains.
5. **Teaching → state → behavior → mastery chain** traced end-to-end in each domain with logged evidence.

### What evidence would still be weak

- Showing only that the demo runs without tracing the internal state transitions.
- Evaluating domains in isolation without cross-domain comparison.
- Claiming misconception handling works without demonstrating the full unlearning/relearning cycle.
- Using only stub outputs without demonstrating that LLM-generated outputs are properly constrained.
- Showing mastery computation without demonstrating that it changes correctly in response to teaching and testing.

---

## 19. What Makes This Top-Tier Worthy — If Successful

This section must be honest about what the project must achieve to support a top-tier conference submission, and what could prevent it from reaching that level.

### Why this could support a top-tier conference paper

A top-tier venue (e.g., CHI, AIED, L@S, LAK, or a major AI-in-education venue) publishes work that makes a clear, novel, well-evaluated contribution to knowledge. This project could support such a paper if it successfully demonstrates:

1. **A novel architectural contribution:** The first unified framework for teachable agents across multiple CS domains with explicit knowledge-state constraints, misconception modeling, and unlearning/relearning logic. This is novel because no prior work has combined all of these in a single framework, and the cross-domain generalization adds a dimension that no prior single-domain work addresses.

2. **A convincing evaluation:** Not just "the system works" but traceable evidence that the knowledge-state mechanism governs behavior, that misconceptions produce the predicted errors, that corrections produce the predicted improvements, and that the framework generalizes across structurally different domains. This evidence must go beyond screenshots and include logged traces, quantitative mastery data, and systematic comparisons.

3. **An operationalized theoretical framework:** The paper would contribute not just a system but a way of thinking about teachable agents: what must a teachable agent's state include? How should misconceptions be represented? What does unlearning look like in an agent's knowledge model? These questions have been discussed informally in the learning-by-teaching literature but have not been operationalized into a reusable framework.

### What must be true for that to happen

- The framework must be genuinely shared across domains, not three separate systems in a trench coat.
- The misconception/unlearning/relearning mechanism must be implemented and evaluated, not just proposed.
- The evaluation must trace the teaching → state → behavior → mastery chain with logged evidence.
- At least two domains must be beyond the prototype stage, with functioning misconception cycles and mastery computation.
- The paper must clearly articulate what is novel beyond "we built a bigger system."

### Which part carries the real intellectual weight

The real intellectual weight is in the **knowledge-state-constrained behavior mechanism** and the **misconception/unlearning/relearning lifecycle**. These are the parts that are architecturally novel and educationally significant. The domain count (three) is evidence for the mechanism's generality, not the contribution itself.

### What would keep it from reaching top-tier level

- If the evaluation is only demo-level ("here is a screenshot of the system working").
- If the misconception mechanism is shallow (misconceptions exist in the data model but do not meaningfully affect behavior).
- If the cross-domain claim is undermined by domain-specific hacks in the shared engines.
- If the paper cannot articulate a clear contribution beyond "more domains" or "bigger system."
- If unlearning/relearning is described but not demonstrated with evidence.

---

## 20. Current Gaps Between Now and the Final System

### What the current Python Stage One prototype already proves

- Zero-knowledge TA initialization works.
- Knowledge-state-constrained problem selection works.
- Constrained code generation (with guards and fallback) works.
- Automated mastery evaluation works.
- The teach → state → test → report loop is closed and reproducible.
- Stub + optional LLM dual-path architecture works.
- The concept of a teachable agent for Python is feasible.

### What still remains missing

**Framework-level gaps:**
- No shared domain-agnostic core. The current code is Python-specific; it has not been refactored into a shared engine + domain layer architecture.
- No unified knowledge-state engine. The `StateTracker` works for Python but is not designed for multi-domain operation.
- No misconception lifecycle engine. Misconceptions exist in the data model but do not actively drive behavior through the unlearning/relearning pipeline.
- No cross-domain mastery comparison infrastructure.

**Domain-level gaps:**
- Python is Stage One only (20 units, 16 problems, 6 misconceptions). It needs expansion to full introductory scope and activation of misconception-driven behavior.
- Database domain is entirely unbuilt: no knowledge units, no problems, no misconceptions, no task evaluation (query execution and result-set comparison).
- AI Literacy domain is entirely unbuilt: no knowledge units, no problems, no misconceptions, no task evaluation (explanation scoring).

**Mechanism-level gaps:**
- No unlearning/relearning logic. The state can move from `unknown` to `learned` but cannot undergo misconception → correction → unlearning → relearning transitions.
- No natural-language teaching interpretation. Teaching is via structured events, not free-form student text.
- No multi-turn dialogue management. Each teaching event is independent; no conversation history is maintained.
- No knowledge decay/forgetting model.

**Evaluation-level gaps:**
- No systematic evaluation methodology beyond the three demo scenarios.
- No trace infrastructure for logging teaching → state → behavior → mastery chains.
- No cross-domain evaluation design.

**Infrastructure-level gaps:**
- No session persistence. State resets every run.
- No multi-user support.
- No deployment infrastructure (acceptable for research prototype, but needed for any user study).

### Major research risks

1. **LLM constraint leakage.** LLMs may resist being constrained to only "know" what the state says. If guards are insufficient, the TA's behavior will not reflect its knowledge state, invalidating the core mechanism.

2. **Misconception fidelity.** Getting the LLM to produce output that is consistently wrong in the *right* way (reflecting a specific misconception rather than random errors) is difficult. If misconception-driven behavior is unreliable, the unlearning/relearning claim is weakened.

3. **Explanation evaluation reliability.** For AI Literacy (and some Database tasks), evaluation requires assessing the quality of natural-language explanations. LLM-based evaluation may be unreliable; rubric-based evaluation requires carefully designed rubrics and validation.

4. **Framework generality vs. domain specificity.** The shared engines must be general enough to work across domains but specific enough to handle each domain's unique requirements (code execution, query execution, explanation evaluation). Finding the right abstraction level is a genuine design challenge.

5. **Scope management.** The project is large. There is a risk of spending too much time on one domain (Python) and not enough on the others, or of building extensive infrastructure that never gets evaluated.

---

## 21. Evidence Map

This section maps each major claim (Section 2) to the evidence that exists today versus what is still missing. Use it to answer: *What has already been proven? What has only been designed? What still needs to be demonstrated?*

### 21.1 Main Claim and Subclaims: Evidence Status

| Claim | Evidence already available (Python Stage One) | Evidence partially available | Evidence still missing (full system) |
|-------|-----------------------------------------------|-----------------------------|--------------------------------------|
| **Main claim** (unified, state-constrained, misconception-aware, unlearning/relearning-capable framework across domains) | Single-domain loop works; state constrains selection and code path; guard/fallback exist | — | Multi-domain under one engine; misconception lifecycle operational; unlearning/relearning implemented and traced; cross-domain evaluation |
| **C1** (behavior structurally constrained by state) | State drives problem selection; stub and LLM code path use learned units; output guard rejects forbidden constructs; fallback to stub on guard/LLM failure | LLM path optional; constraint partly prompt-based | Same constraint in Database and AI Literacy; guard/fallback verified for all domains; no state bypass in any path |
| **C2** (misconception lifecycle implemented and observable) | Misconception catalog and prompt injection exist; Scenario C shows failure path via forced wrong code | Failure path is stub-driven, not misconception-state-driven | Misconception activation from teaching; misconception → wrong behavior; correction → unlearning → relearning with state transitions; traced cycles per domain |
| **C3** (same framework across Python, Database, AI Literacy) | Python-only codebase; domain-agnostic interfaces in design (proposal, blueprint) | — | Single codebase with shared engines; Database and AI Literacy as content layers only; adding a domain does not require engine changes |
| **C4** (evaluation traces teaching → state → behavior → mastery) | Three scenarios show loop; capability audit and scenario evaluation docs | No automated trace; no logged state diffs | Trace layer logging all events; analyses linking teaching to state change to mastery; cross-domain evaluation design |

### 21.2 Summary: What Is Proven vs. Missing

- **Already proven (Python Stage One):** Zero-knowledge start; state-constrained selection; state-constrained code generation with guard and fallback; automated mastery evaluation; closed teach → state → test → report loop; reproducible scenarios A/B/C.
- **Designed but not yet implemented:** Shared multi-domain engines; misconception activation and behavioral effect; unlearning/relearning state transitions; trace layer; cross-domain mastery comparison.
- **Still missing for full claim:** Second and third domains (Database, AI Literacy) as content layers only; full misconception lifecycle in at least one domain; end-to-end traced evaluation (teaching → state → behavior → mastery); evidence that adding a new domain requires no engine changes.

Future work should use this map to prioritize: evidence that is “still missing” is what moves the main claim from partial to full support.

---

## 22. Non-Negotiable Design Guardrails

The following rules govern all future work on this project. They are not suggestions. They are constraints that must be enforced in every Cursor run, every code review, and every design decision.

**G1. Do not reduce the contribution to domain count.** The contribution is the framework mechanism (knowledge-state-constrained behavior, misconception modeling, unlearning/relearning logic), not the number of domains. Never describe the project as "a teachable agent for Python, Database, and AI Literacy." Always describe it as "a unified framework for knowledge-state-constrained teachable agents, demonstrated across three CS domains."

**G2. Keep the knowledge state as the single source of truth.** No component of the system may determine the TA's behavior by querying the LLM's inherent knowledge, the conversation history, or any source other than the explicit knowledge state. If a component needs to know what the TA knows, it must query the knowledge-state engine.

**G3. Keep misconception / unlearning / relearning central.** Misconception handling is not a "Phase 3" feature to be added after the core is done. It is part of the core. Do not release a "complete" domain without functioning misconception-driven behavior and at least a prototype of the unlearning/relearning cycle.

**G4. Keep evaluation tied to mastery, not just interaction.** Do not evaluate the system by showing that the TA "has a nice conversation." Evaluate it by showing that teaching actions produce state changes, state changes produce behavioral differences, and behavioral differences are reflected in mastery outcomes.

**G5. Do not let the system become a generic chatbot.** If the TA can answer arbitrary questions, express opinions about non-domain topics, or produce output that is not constrained by its knowledge state, the system has failed. Every TA output must be governed by the state.

**G6. Do not prioritize UI/deployment over mechanism clarity.** A beautiful interface with a broken knowledge-state mechanism is worthless for the research contribution. Build and validate the mechanism first; polish the interface later.

**G7. Do not build domain-specific engines where shared engines should exist.** Before writing domain-specific code, ask: "Should this logic be in the shared core?" If the answer is yes, generalize the existing engine rather than adding a parallel implementation. If adding a fourth domain would require modifying the shared engines, the shared engines are not correctly designed.

**G8. Do not skip the trace layer.** Every teaching event, state transition, task attempt, evaluation result, misconception activation, and correction must be logged. Without traces, the evaluation claims cannot be supported.

**G9. Do not pretend the system works by using only stubs.** Stubs are acceptable for initial development and deterministic testing, but the final system must demonstrate that LLM-generated outputs are properly constrained. A system that only works with stubs has not validated the LLM-constraint mechanism.

**G10. Do not expand scope before the core is solid.** Do not add advanced Python topics, additional database concepts, or new domains before the shared core engines (knowledge state, misconception lifecycle, mastery evaluation, guard/fallback) are implemented, tested, and working in at least two domains.

---

## 23. Blueprint Alignment Checks

This section defines how to determine whether future work is aligned with this blueprint. It is intended to be referenced at the start and end of every Cursor run, every design review, and every evaluation planning session. Use it as an **active review tool**: before and after a task, run through the criteria below to judge alignment and detect drift.

### 23.1 Future Work Judgment Criteria

Classify any planned or completed work using these four categories:

| Judgment | Meaning | Example |
|----------|--------|--------|
| **Strongly on track** | Work directly advances the main claim or a supporting subclaim (C1–C4); preserves or strengthens the framework, state constraint, or misconception lifecycle; adds evidence that appears in the Evidence Map (Section 21) as “still missing.” | Implementing the misconception engine so that active misconceptions drive TA code; refactoring to a shared Knowledge State Engine used by Python and Database. |
| **Acceptable but secondary** | Work is useful for demonstration, reproducibility, or usability but does not by itself support the main claim. It must not replace or delay work that fills “evidence still missing,” and it must not violate guardrails (Section 22). | Improving Streamlit UI for scenario selection; adding a reproducibility script; writing a deployment guide. |
| **Drifting** | Work emphasizes surface outcomes (more domains, more problems, nicer UI) without advancing the shared mechanism, state constraint, or misconception lifecycle; or it describes the project in a rejected framing (Section 10); or it omits the strong framing (unified framework, state-constrained behavior, misconception lifecycle, unlearning/relearning, cross-domain mastery). | Adding a second domain with a separate state model and separate mastery logic; prioritizing “three domains working” over “one framework operating in three domains.” |
| **Off track** | Work contradicts the main claim or guardrails: e.g., state is bypassed; misconception lifecycle is removed or demoted to “future work”; shared engines are duplicated per domain; evaluation is only “demo works” with no trace of teaching → state → mastery. | Making the TA a tutor; dropping guards/fallbacks; implementing Database with domain-specific engine code instead of a content layer. |

When in doubt, ask: *Does this work add or preserve evidence for the main claim and subclaims (Section 2), or does it only add features that could support a weaker framing?* If the latter, treat it as drifting unless reframed.

### 23.2 What later work must preserve

1. **The knowledge-state-constrained behavior mechanism as the core contribution.** If later work re-frames the contribution as "multi-domain coverage" or "nice UI" or "LLM-powered tutoring," the project has drifted.

2. **Misconception / unlearning / relearning as a central, implemented, evaluated feature.** If later work deprioritizes this to a "future work" section in the paper, the strongest distinguishing feature has been abandoned.

3. **The shared-engine architecture.** If later work builds domain-specific engines that duplicate shared logic, the framework claim is weakened.

4. **The teaching → state → behavior → mastery evaluation chain.** If later work evaluates the system by showing conversation logs rather than traced state transitions and mastery outcomes, the evaluation is insufficient.

5. **The zero-knowledge starting point.** If later work allows the TA to start with pre-loaded knowledge (except for deliberately seeded misconceptions), the "teachable agent" identity is compromised.

### 23.3 What later work must not simplify away

- The explicit knowledge state structure (do not replace it with implicit LLM memory).
- The guard/fallback layer (do not assume the LLM will always respect constraints).
- The misconception catalog and lifecycle (do not reduce misconceptions to random errors).
- The mastery evaluation rubric (do not reduce evaluation to "thumbs up/down").
- The trace/history layer (do not rely on unlogged system behavior for evaluation claims).

### 23.4 How to detect drift into a weak "bigger demo" framing

The project has drifted if:
- A progress update describes new features (more domains, more problems, better UI) without mentioning whether the knowledge-state mechanism, misconception lifecycle, or evaluation chain has advanced.
- A demo shows the TA producing correct output without demonstrating that the output is constrained by state (i.e., without showing what happens when the TA has not been taught the relevant concept).
- Cross-domain comparison is absent from evaluation plans.
- Misconception → correction → unlearning → relearning is not demonstrated in any domain.
- The paper draft frames the contribution as "we built a system for three CS domains" rather than "we demonstrate that a unified knowledge-state mechanism generalizes across three structurally different CS domains."

### 23.5 How to detect when later work no longer supports the main claim

The main claim is: "A unified, knowledge-state-constrained, misconception-aware teachable-agent framework can generalize across multiple CS domains with structurally different task types and evaluation methods."

This claim is no longer supported if:
- The shared engines contain domain-specific conditionals (e.g., `if domain == "python": ...`) rather than domain-agnostic logic with pluggable content layers.
- Misconception handling works in one domain but not others.
- Mastery computation uses different logic in different domains.
- The knowledge state format differs between domains.
- Adding a new domain requires modifying core engine code.

### 23.6 How future Cursor runs should use this blueprint to stay aligned

At the start of every Cursor run that involves implementation, design, or evaluation planning:

1. **Read this blueprint** (or the relevant sections) before beginning work.
2. **Check the non-negotiable guardrails** (Section 22) against the planned work. If the planned work would violate a guardrail, stop and reconsider.
3. **Verify that the planned work advances the core contribution** (knowledge-state mechanism, misconception lifecycle, cross-domain framework), not just surface features (more problems, prettier UI, deployment infrastructure).
4. **After completing work, verify alignment:** Does the completed work maintain the knowledge state as single source of truth? Does it support the shared-engine architecture? Does it include trace logging? Does it advance misconception / unlearning / relearning?
5. **If alignment is questionable, flag it.** Add a note in the commit or documentation explaining the concern and how it should be resolved.

6. **Use the Evidence Map (Section 21) to prioritize.** Work that fills “evidence still missing” for the main claim or C1–C4 is strongly on track; work that only adds “acceptable but secondary” value should not delay that evidence-building.

7. **Classify the task using the Future Work Judgment Criteria (23.1).** If the classification is “drifting” or “off track,” revise the task or explicitly flag and justify the exception before proceeding.

---

## 24. Blueprint Conclusion

This project is now a validated research prototype in its first domain, with a clear path toward a framework-level contribution. The Python Stage One foundation is real: it demonstrates that a zero-knowledge teachable agent with knowledge-state-constrained behavior, automated mastery evaluation, and guard/fallback mechanisms is implementable and reproducible. That foundation is not the final system, but it is not a toy either — it is the proof that the core mechanism works.

The broader system must become a unified framework that operates the same mechanism across Python, Database, and AI Literacy, with misconception modeling and unlearning/relearning as central architectural components, not afterthoughts. The framework's value is not in its domain count but in the generality of its mechanism: the knowledge-state engine, the misconception lifecycle, the constrained behavior pipeline, and the evaluation chain that traces teaching to state change to mastery outcome.

What the team should focus on next, in priority order:

1. **Architect the shared core.** Refactor the Python-specific prototype into a domain-agnostic core with a Python content layer. Define the interfaces for the knowledge-state engine, misconception engine, mastery evaluator, task engine, and guard layer so that Database and AI Literacy content layers can plug in.

2. **Implement the misconception / unlearning / relearning lifecycle.** This is the highest-value mechanism in the project. Build it in the Python domain first, then verify that it works through the shared engine without domain-specific code.

3. **Build the second domain (Database).** This is the critical test of the framework claim. If the shared engines work for Database with only a content layer addition, the framework is credible. If they require extensive modification, the architecture needs revision before proceeding further.

4. **Build the trace layer.** Without traces, the evaluation claims cannot be supported. Build logging for teaching events, state transitions, misconception activations, corrections, and mastery computations from the start — not as a retroactive addition.

5. **Design the evaluation methodology.** Before writing the paper, design the evaluation plan: what evidence is needed, how it will be collected, what claims it supports, and what it cannot support. Do not begin evaluation planning after the system is built; design it alongside.

This blueprint is the governing document for all of this work. It is not a wish list or a brainstorming note. It is a constraint source. Future work that contradicts this blueprint must explicitly justify the contradiction. Future work that advances this blueprint must explicitly trace its contribution back to the principles defined here. The project succeeds if the final system, evaluated against this blueprint, demonstrates a unified, knowledge-state-constrained, misconception-aware teachable-agent framework that generalizes across structurally different CS domains — and fails if it produces only a larger demo without the underlying mechanism.

---

*End of Master System Blueprint*
