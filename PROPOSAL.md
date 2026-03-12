# Teachable Agent for Computer Science: Project Proposal and Executive Build Plan

**Project Title:** Teachable Agent for CS — Phase 1: Introductory Python Programming  
**Date:** 2026-03-12  
**Status:** Proposal (Pre-Implementation)  
**Repository State:** Empty — Zero to One  

---

## 1. Project Goal

Build a **Teachable Agent (TA) system** in which a human student teaches an AI agent how to program, rather than the AI teaching the student. The agent begins with **zero programming knowledge** and must learn exclusively through interaction with the student. The student's learning occurs as a byproduct of the teaching process — a well-established phenomenon known as "learning by teaching" (Biswas et al., 2005; Chase et al., 2009).

The first implementation targets **Introductory Python programming** as a controlled, well-scoped domain. The system is a **research prototype**, not a consumer product. Its purpose is to validate the core interaction loop: student teaches → agent learns → agent is tested → results reflect both the agent's state and the student's teaching effectiveness.

---

## 2. Alignment with Teacher Goal

The teacher's stated goal is to design a Teachable Agent for CS. This proposal is aligned as follows:

| Teacher Requirement | Proposal Response |
|---|---|
| TA starts with no knowledge | Section 7 defines the agent's initial blank state precisely |
| Programming test to examine TA mastery | Section 10 designs a multi-level mastery test |
| TA learns from human student interaction | Section 9 specifies the interaction flow |
| Conversation + generated problems | Section 8 explains why both are necessary |
| Broader CS domains (AI Literacy, DB, etc.) | Section 5 explicitly defers these to later phases |
| First step = Introductory Python | Section 3 justifies this choice |
| Build from zero | Sections 17–21 lay out concrete deliverables and build order |

This proposal does **not** deviate from, extend, or reinterpret the teacher's requirements. Every design decision traces back to a stated requirement.

---

## 3. Why Introductory Python is the First-Step Domain

Introductory Python is the correct first-step domain for the following concrete reasons:

1. **Bounded knowledge space.** Introductory Python has a well-defined, finite set of concepts (variables, types, conditionals, loops, functions, basic data structures). This makes it feasible to enumerate knowledge units, define mastery levels, and build a problem bank — all of which are prerequisites for a testable TA.

2. **Executable correctness criterion.** Python programs can be run and tested. Unlike natural-language domains, a TA's "understanding" of Python can be verified by having it write code that is executed against test cases. This provides an objective, automatable mastery signal.

3. **Rich misconception literature.** Decades of CS education research have cataloged common beginner misconceptions in Python/programming (e.g., confusing `=` with `==`, off-by-one errors, mutable default arguments). These can be directly encoded into the TA's initial misconception model.

4. **Low barrier to problem generation.** Python programming problems at the introductory level are straightforward to generate and validate automatically. This supports the requirement for generated programming problems.

5. **Broad curricular consensus.** Most introductory Python courses cover the same core topics in a similar order. This means the knowledge unit structure will generalize across educational contexts.

6. **Foundation for extension.** The system architecture built for Introductory Python (knowledge state tracking, problem generation, mastery testing, interaction protocol) can be reused when extending to AI Literacy, Databases, or other CS domains. Python is the simplest case to validate the architecture.

Choosing a broader domain (e.g., "all of CS" or "Python + databases") for Phase 1 would make the knowledge space intractable, the mastery test design ambiguous, and the prototype unshippable within a reasonable timeline.

---

## 4. First-Stage Scope

Phase 1 is a **small, controlled prototype** with the following boundaries:

**In scope:**
- A single TA agent that starts with no Python knowledge
- A text-based interaction interface (conversation + code input)
- A fixed set of ~30–50 introductory Python knowledge units
- A problem bank of ~50–100 auto-gradable Python problems
- A mastery test that evaluates the TA on a subset of knowledge units
- A knowledge state model that tracks what the TA "knows" and "misunderstands"
- A teaching interaction protocol (how the student teaches, how the TA responds)
- Basic misconception simulation (the TA can hold and display common beginner errors)
- A mastery report showing the TA's test results to the student

**Scale:**
- 1 student interacting with 1 TA instance at a time
- No concurrent users, no authentication, no cloud deployment
- No persistent user accounts; session-based only

---

## 5. Out-of-Scope Items for Phase 1

The following are **explicitly excluded** from Phase 1. They may be addressed in later phases.

| Item | Reason for Exclusion |
|---|---|
| AI Literacy domain | Requires separate knowledge unit design; deferred |
| Database domain | Requires separate knowledge unit design; deferred |
| Other CS domains (TBA) | Not yet defined |
| Multi-student support | Adds authentication, state isolation, and scaling complexity |
| Persistent user accounts | Not needed for prototype validation |
| Cloud deployment | Local-only prototype is sufficient |
| Voice or multimodal interaction | Text-based interaction is sufficient for validation |
| TA personality or emotional modeling | Out of scope for core learning mechanics |
| Curriculum sequencing by the system | The student decides what to teach and in what order |
| Adaptive difficulty for the student | The TA is the learner, not the student |
| Mobile or responsive UI | Desktop-only prototype |
| Plagiarism detection | Not relevant to the TA interaction model |
| Integration with LMS (Moodle, Canvas, etc.) | Deferred to productization phase |
| Fine-tuning or training custom ML models | Use prompted LLM (e.g., GPT-4 / Claude) with structured state |

---

## 6. Core System Idea

The system implements a **role-reversed pedagogical loop**:

```
┌─────────────────────────────────────────────────────┐
│                  TEACHING LOOP                       │
│                                                      │
│   Student ──teaches──▶ TA (agent)                   │
│      │                    │                          │
│      │                    ▼                          │
│      │              TA updates its                   │
│      │              knowledge state                  │
│      │                    │                          │
│      │                    ▼                          │
│      │              TA is tested                     │
│      │              (programming problems)           │
│      │                    │                          │
│      │                    ▼                          │
│      │◀──sees results─── Mastery Report             │
│      │                                               │
│      ▼                                               │
│   Student reflects:                                  │
│   "Why did the TA get this wrong?"                  │
│   "Did I explain this clearly enough?"              │
│   "What should I teach next?"                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

The student's learning happens through **reflection on the TA's failures and successes**. If the TA fails a test, the student must diagnose whether the failure is due to:
- A concept the student never taught
- A concept the student taught poorly
- A misconception the student failed to correct

This reflective loop is the core pedagogical mechanism.

---

## 7. Definition of the Teachable Agent

### 7.1 What the TA Is

The TA is a **simulated novice learner** with the following properties:

- **Initial state:** The TA begins with **zero usable programming knowledge**. It does not know what a variable is, what a loop does, or how to write any Python code. Its initial knowledge state is an empty (or near-empty) map.

- **Learning mechanism:** The TA updates its internal knowledge state based on what the student tells it. If the student explains that "a variable stores a value," the TA's knowledge state for `variable_assignment` moves from `unknown` toward `partially_learned` or `learned`. The mapping from student input to state update is mediated by an LLM that interprets the teaching and maps it to knowledge units.

- **Misconception capacity:** The TA can acquire misconceptions, either by default (pre-seeded common errors) or through ambiguous/incorrect student teaching. For example, if the student says "a list and a tuple are the same thing," the TA may acquire the misconception `list_tuple_equivalence`.

- **Forgetting (simplified):** In Phase 1, forgetting is modeled simply. Knowledge units that have not been reinforced decay toward `partially_learned` over a session. This is a simplified decay, not a full spaced-repetition model.

- **Test-taking behavior:** When given a programming problem, the TA attempts to solve it using only its current knowledge state. If it has not learned loops, it cannot write loop-based solutions. If it holds a misconception about `==` vs `=`, it may produce code that uses `=` in a conditional.

### 7.2 What the TA Is NOT

- The TA is **not a tutor**. It does not teach the student. It does not provide hints, corrections, or explanations of Python to the student. Its role is purely that of a learner.
- The TA is **not a coding assistant**. It does not help the student write code. It writes code only when taking a mastery test, and the code it writes reflects its (possibly flawed) understanding.
- The TA is **not an LLM chatbot with full Python knowledge**. The underlying LLM is prompted/constrained to behave as if it only knows what has been taught. The knowledge state model governs the TA's capabilities.

### 7.3 TA Behavioral Persona

The TA should behave like an eager but naive student:
- Asks clarifying questions ("What do you mean by 'iterate'?")
- Restates what it thinks it learned ("So a `for` loop repeats code for each item in a list?")
- Expresses confusion when taught contradictory information
- Attempts problems with visible reasoning ("I think I need a loop here because you said loops repeat things...")
- Makes mistakes that are consistent with its knowledge state

---

## 8. Interaction Design Principles

### 8.1 Why Conversation Alone Is Not Enough

Conversation (natural language dialogue between student and TA) is a necessary component but is **insufficient** on its own for the following reasons:

1. **No objective mastery signal.** If the student and TA only converse, there is no way to objectively measure whether the TA has "learned" anything. The TA could parrot back correct-sounding explanations without being able to apply them. Conversation provides the illusion of understanding without verification.

2. **No executable artifact.** Programming is a skill that produces executable artifacts (code). A learner who can describe a loop but cannot write one has not learned to program. The TA must demonstrate its knowledge by writing code that runs and passes tests.

3. **No structured feedback loop.** Without tests and problems, the student has no concrete signal to guide their teaching. They cannot see *what specifically* the TA misunderstands. Conversation alone produces vague feedback ("I think I understand") rather than precise feedback ("The TA used `=` instead of `==` in line 3").

4. **Reduced reflective depth.** The pedagogical value of the teachable agent paradigm comes from the student reflecting on *concrete failures*. A TA that only converses never fails concretely. A TA that writes buggy code fails in a way the student can analyze.

### 8.2 Why Problem Generation and Programming Tests Must Be Included

1. **Mastery verification.** Problems and tests are the only mechanism to verify that the TA's knowledge state is accurate. If the TA claims to know loops, a loop-based problem tests that claim.

2. **Misconception surfacing.** Well-designed problems can expose specific misconceptions. A problem that requires `==` in a conditional will surface the `=` vs `==` misconception if the TA holds it.

3. **Student diagnostic tool.** When the TA fails a problem, the student sees the TA's (incorrect) code and must diagnose the error. This diagnosis is itself a deep learning activity for the student.

4. **Progress tracking.** A bank of graded problems provides a quantitative measure of TA progress over time, which is essential for both the student's motivation and the researcher's evaluation.

### 8.3 The Two Interaction Channels

The system therefore uses **two complementary interaction channels**:

| Channel | Purpose | Example |
|---|---|---|
| **Teaching conversation** | Student explains concepts to the TA; TA asks questions, restates understanding, expresses confusion | "A `for` loop lets you go through each item in a list one by one." |
| **Problem-based testing** | TA attempts auto-graded programming problems; results are shown to the student | TA writes `for i in range(5): print(i)` for a "print numbers 0–4" problem |

Both channels are mandatory. The conversation channel drives knowledge acquisition. The problem channel drives knowledge verification and student reflection.

---

## 9. Proposed Teaching Interaction Flow

The following is the primary interaction loop for Phase 1:

### Step 1: Student Chooses What to Teach
The student selects a topic (or teaches freely). The system does not prescribe a curriculum order. The student may say: *"Today I'm going to teach you about variables."*

### Step 2: Student Teaches via Conversation
The student explains the concept using natural language, code examples, or both. The TA responds as a novice learner: asks questions, restates, expresses confusion.

```
Student: "A variable is like a box that holds a value. You create one by writing
          something like x = 5."
TA:      "So x is the box, and 5 is what's inside it? Can I put words in the box too?"
Student: "Yes! You can write name = 'Alice' to put a string in a variable."
TA:      "Got it. So x = 5 makes a number variable, and name = 'Alice' makes a
          string variable. Is that right?"
```

### Step 3: TA Updates Knowledge State
After the teaching exchange, the system updates the TA's internal knowledge state. The knowledge unit `variable_assignment` moves from `unknown` to `partially_learned` or `learned`, depending on the depth and correctness of the teaching.

### Step 4: Student Requests a Test (or System Suggests One)
The student can ask the system to test the TA on what it has learned. The system generates or selects a problem appropriate to the TA's current knowledge state.

```
System: "Here's a problem for your TA to try:
         Write a program that creates a variable called `age`, sets it to 20,
         and prints it."
```

### Step 5: TA Attempts the Problem
The TA writes code based on its current knowledge state. If it has learned variables and `print()`, it may produce correct code. If it has a misconception, it may produce incorrect code.

```
TA's attempt:
    age = 20
    print(age)
    # Result: PASS ✓
```

Or, if the TA has a misconception:

```
TA's attempt:
    age = "20"
    print(age)
    # Result: PARTIAL — output is correct but type is wrong
```

### Step 6: Student Reviews Results and Reflects
The student sees the TA's code and the test results. If the TA failed, the student must figure out why and re-teach the concept.

### Step 7: Loop
The student continues teaching, testing, and correcting. The TA's knowledge state evolves over the session.

---

## 10. Programming Mastery Test Design

### 10.1 Test Purpose

The mastery test measures **what the TA can do**, not what it says it knows. The test consists of programming problems that the TA must solve by writing executable Python code.

### 10.2 Test Structure

Each test problem has the following components:

| Component | Description |
|---|---|
| **Problem ID** | Unique identifier (e.g., `prob_var_001`) |
| **Knowledge units tested** | List of knowledge units the problem requires (e.g., `[variable_assignment, print_function]`) |
| **Problem statement** | Natural language description of what the program should do |
| **Input specification** | What input the program receives (if any) |
| **Expected output** | What the correct program should output |
| **Test cases** | 3–5 input/output pairs for automated grading |
| **Difficulty tier** | `remember`, `apply`, or `transfer` (see below) |
| **Common misconceptions targeted** | Which misconceptions this problem is designed to surface |

### 10.3 Difficulty Tiers

Problems are classified into three tiers based on Bloom's taxonomy (simplified):

1. **Remember:** Direct application of a single concept. *"Create a variable `x` with value 10 and print it."*
2. **Apply:** Combine 2–3 concepts to solve a straightforward problem. *"Write a program that reads a number and prints whether it is even or odd."*
3. **Transfer:** Apply learned concepts to a novel situation not directly covered in teaching. *"Write a program that counts how many vowels are in a user-provided string."*

### 10.4 Mastery Levels

The TA's mastery on each knowledge unit is determined by test performance:

| Level | Criterion |
|---|---|
| **Not assessed** | No problems attempted for this knowledge unit |
| **Failing** | <50% of relevant problems passed |
| **Developing** | 50–79% of relevant problems passed |
| **Proficient** | 80–100% of relevant problems passed, `remember` + `apply` tiers |
| **Mastered** | 80–100% passed across all tiers including `transfer` |

### 10.5 Test Administration

- The student can request a test at any time for any knowledge unit or group of units.
- The system can also suggest a "comprehensive test" covering all units the TA has been taught.
- Tests are auto-graded by executing the TA's code against test cases in a sandboxed environment.
- The TA's code, the expected output, and the actual output are all shown to the student.

---

## 11. Knowledge State Design

### 11.1 Knowledge Unit Structure

The TA's knowledge is represented as a structured state over a predefined set of **knowledge units** (KUs). Each KU represents a single learnable concept in Introductory Python.

Proposed knowledge units for Phase 1 (~35 units, organized by topic):

**Fundamentals (8 units):**
- `print_function` — Using `print()` to display output
- `comments` — Writing comments with `#`
- `variable_assignment` — Assigning values to variables
- `data_types_int_float` — Integer and float types
- `data_types_string` — String type and string literals
- `data_types_bool` — Boolean type (`True`, `False`)
- `type_conversion` — Using `int()`, `str()`, `float()`
- `user_input` — Using `input()` to read user input

**Operators (5 units):**
- `arithmetic_operators` — `+`, `-`, `*`, `/`, `//`, `%`, `**`
- `comparison_operators` — `==`, `!=`, `<`, `>`, `<=`, `>=`
- `logical_operators` — `and`, `or`, `not`
- `string_concatenation` — Using `+` to join strings
- `assignment_operators` — `+=`, `-=`, etc.

**Control Flow (6 units):**
- `if_statement` — Basic `if` conditional
- `if_else` — `if`/`else` branching
- `if_elif_else` — Multi-branch conditionals
- `while_loop` — `while` loop with condition
- `for_loop_range` — `for` loop with `range()`
- `for_loop_iterable` — `for` loop over strings, lists

**Functions (5 units):**
- `function_definition` — Defining functions with `def`
- `function_parameters` — Parameters and arguments
- `return_statement` — Returning values from functions
- `function_calls` — Calling functions
- `scope_basics` — Local vs. global variables (simplified)

**Data Structures (7 units):**
- `list_creation` — Creating lists
- `list_indexing` — Accessing list elements by index
- `list_methods` — `append()`, `pop()`, `len()`
- `list_iteration` — Looping through lists
- `tuple_basics` — Tuples and immutability
- `dictionary_creation` — Creating dictionaries
- `dictionary_access` — Accessing and modifying dictionary values

**Miscellaneous (4 units):**
- `string_methods` — `.upper()`, `.lower()`, `.strip()`, `.split()`
- `string_formatting` — f-strings or `.format()`
- `error_types` — `SyntaxError`, `TypeError`, `NameError` (recognition only)
- `basic_debugging` — Reading error messages, identifying common bugs

### 11.2 Knowledge State Per Unit

Each knowledge unit has a state:

```
{
  "unit_id": "for_loop_range",
  "status": "partially_learned",    // unknown | partially_learned | learned | misconception
  "confidence": 0.6,                // 0.0 to 1.0
  "misconceptions": ["off_by_one_range"],  // active misconceptions
  "last_taught": "2026-03-12T10:30:00",
  "teach_count": 2,                 // how many times student has taught this
  "test_results": [                 // history of test performance
    {"problem_id": "prob_for_001", "passed": true},
    {"problem_id": "prob_for_002", "passed": false}
  ]
}
```

### 11.3 Misconception Catalog

Phase 1 should include a curated catalog of ~20–30 common introductory Python misconceptions. Examples:

| ID | Misconception | Affected KUs | Example Behavior |
|---|---|---|---|
| `assign_vs_equal` | Confuses `=` (assignment) with `==` (comparison) | `variable_assignment`, `comparison_operators` | Writes `if x = 5:` instead of `if x == 5:` |
| `off_by_one_range` | Thinks `range(5)` produces 1–5 | `for_loop_range` | Writes `range(5)` expecting output `1 2 3 4 5` |
| `string_int_concat` | Tries to concatenate string and int with `+` | `string_concatenation`, `type_conversion` | Writes `"Age: " + 20` without `str()` |
| `mutable_default` | Does not understand list mutability | `list_methods` | Surprised when appending to a list changes it "everywhere" |
| `print_vs_return` | Confuses `print()` with `return` | `print_function`, `return_statement` | Uses `print()` in a function and expects the caller to get the value |
| `indent_error` | Incorrect indentation after `:` | `if_statement`, `for_loop_range` | Writes code without indentation after `if:` |
| `loop_variable_scope` | Thinks loop variable disappears after loop | `for_loop_range`, `scope_basics` | Doesn't use `i` after the loop, thinking it's gone |

The full catalog should be developed as a seed resource before implementation.

---

## 12. Required Seed Resources

Before any application code is written, the following seed resources must be created:

### 12.1 Knowledge Unit Definitions
A structured file (JSON or YAML) defining all ~35 knowledge units with:
- ID, name, description
- Prerequisites (which KUs must be learned before this one)
- Related misconceptions
- Example correct code
- Example incorrect code (reflecting misconceptions)

### 12.2 Misconception Catalog
A structured file defining all ~20–30 misconceptions with:
- ID, description
- Affected knowledge units
- Example manifestation in code
- How to correct (what the student should teach)

### 12.3 Problem Bank
A structured file containing ~50–100 programming problems with:
- Problem statement
- Knowledge units tested
- Difficulty tier
- Test cases (input/output pairs)
- Targeted misconceptions

### 12.4 Mastery Rubric
A document defining:
- How mastery levels are computed from test results
- Thresholds for each level
- How misconceptions affect mastery

### 12.5 Interaction Protocol
A document specifying:
- How the TA responds to different types of teaching input
- How knowledge state updates are triggered
- How the TA behaves during tests
- How the TA expresses its current understanding

### 12.6 LLM Prompt Templates
Draft prompt templates for:
- TA conversation behavior (novice learner persona)
- Knowledge extraction from student teaching
- Code generation constrained by knowledge state
- Misconception-consistent code generation

---

## 13. Functional Requirements

### FR-1: Teaching Conversation
The system shall provide a text-based interface where the student can teach the TA using natural language and code examples.

### FR-2: TA Responses
The TA shall respond to teaching input as a novice learner: asking questions, restating understanding, expressing confusion, and acknowledging what it has learned.

### FR-3: Knowledge State Tracking
The system shall maintain an internal knowledge state for the TA, updating it based on teaching interactions.

### FR-4: Problem Generation / Selection
The system shall generate or select programming problems from the problem bank based on the TA's current knowledge state.

### FR-5: TA Code Generation
When given a problem, the TA shall generate Python code that reflects its current knowledge state, including any active misconceptions.

### FR-6: Automated Grading
The system shall execute the TA's code against test cases and report pass/fail results.

### FR-7: Mastery Reporting
The system shall display the TA's mastery level for each knowledge unit, based on test performance.

### FR-8: Misconception Display
When the TA fails a test, the system shall display the TA's code so the student can diagnose the error.

### FR-9: Session State
The system shall maintain the TA's knowledge state within a session. State persists for the duration of one session.

### FR-10: Test Request
The student shall be able to request a test for the TA at any time, specifying which topics to test or requesting a comprehensive test.

---

## 14. Educational Requirements

### ER-1: Learning by Teaching
The system design shall support the "learning by teaching" paradigm. The student must be the active teacher; the TA must be the passive learner.

### ER-2: No Tutoring by the TA
The TA shall not provide explanations, hints, or instruction to the student. It shall only express its own (possibly incorrect) understanding.

### ER-3: Visible Reasoning
When the TA attempts a problem, it shall show its reasoning process ("I think I need a loop here because...") so the student can diagnose errors in the TA's thinking.

### ER-4: Misconception Fidelity
The TA's mistakes shall reflect realistic beginner misconceptions, not random errors. The misconceptions shall be drawn from the curated misconception catalog.

### ER-5: Reflective Prompting
After a test, the system should prompt the student to reflect: "Why do you think the TA got this wrong?" or "What would you teach differently?"

### ER-6: No Curriculum Prescription
The system shall not prescribe what the student teaches or in what order. The student has full autonomy over the teaching sequence.

---

## 15. Engineering Requirements

### ENGR-1: Technology Stack (Recommended)
- **Backend:** Python (FastAPI or Flask)
- **Frontend:** Web-based (React or simple HTML/JS); or Streamlit for rapid prototyping
- **LLM Integration:** OpenAI API (GPT-4) or Anthropic API (Claude) via structured prompting
- **Code Execution Sandbox:** Docker-based or subprocess with timeout and resource limits
- **Data Storage:** File-based (JSON) for Phase 1; no database required
- **Version Control:** Git

### ENGR-2: LLM Usage Architecture
The LLM is used as a **prompted simulation engine**, not as the TA itself. The architecture is:

```
Student Input
     │
     ▼
┌─────────────────┐
│ Teaching         │
│ Interpreter      │──▶ LLM extracts knowledge from student's teaching
│ (LLM call #1)   │    and maps it to knowledge units
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Knowledge State  │
│ Manager          │──▶ Updates the structured knowledge state
│ (deterministic)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TA Response      │
│ Generator        │──▶ LLM generates novice-learner response
│ (LLM call #2)   │    constrained by current knowledge state
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Code Generator   │
│ (for tests)      │──▶ LLM generates code constrained by knowledge state
│ (LLM call #3)   │    (only knows what it's been taught, makes expected errors)
└─────────────────┘
```

This architecture ensures that the TA's behavior is **governed by the knowledge state**, not by the LLM's inherent capabilities. The LLM is a tool for natural language generation, not the source of truth for what the TA knows.

### ENGR-3: Sandboxed Code Execution
The TA's generated code must be executed in a sandboxed environment with:
- Timeout (e.g., 5 seconds per execution)
- Memory limit (e.g., 128 MB)
- No network access
- No file system access beyond stdin/stdout

### ENGR-4: Stateless LLM, Stateful Knowledge Model
The LLM is called statelessly (each call includes the relevant knowledge state in the prompt). The knowledge state is the single source of truth and is stored as a structured JSON object.

### ENGR-5: Prototype Fidelity
Phase 1 is a **functional prototype**, not a production system. The following engineering shortcuts are acceptable:
- No authentication
- No database (file-based persistence)
- No CI/CD
- Minimal error handling
- No accessibility compliance
- No internationalization

---

## 16. Constraints

### C-1: LLM Dependency
The system depends on an external LLM API (OpenAI or Anthropic). This introduces cost, latency, and rate-limit constraints. Phase 1 must include API key management and basic cost monitoring.

### C-2: Code Execution Safety
Executing AI-generated code is inherently risky. The sandbox must prevent harmful code from affecting the host system.

### C-3: Knowledge State Fidelity
The LLM must be reliably constrained to behave according to the knowledge state. If the LLM "leaks" knowledge the TA hasn't been taught, the educational validity of the system is compromised. Prompt engineering and output validation are critical.

### C-4: No Curriculum Design
Phase 1 does not prescribe a curriculum. The knowledge units are defined, but the order of teaching is left to the student. This means the system must handle any teaching order gracefully.

### C-5: Research Prototype, Not Product
The system must be evaluated as a research prototype. Success criteria are defined in Section 19, not by user satisfaction metrics.

### C-6: Single Domain
Phase 1 is strictly limited to Introductory Python. The architecture should be extensible to other domains, but no other domain is implemented.

---

## 17. Deliverables for Stage 1

Stage 1 is **design and seed resources** (before implementation):

| # | Deliverable | Format | Description |
|---|---|---|---|
| D1.1 | This proposal document | Markdown | The current document |
| D1.2 | Knowledge unit definitions | JSON/YAML | All ~35 knowledge units with metadata |
| D1.3 | Misconception catalog | JSON/YAML | All ~20–30 misconceptions with metadata |
| D1.4 | Problem bank | JSON/YAML | ~50–100 problems with test cases |
| D1.5 | Mastery rubric | Markdown | Mastery level definitions and computation rules |
| D1.6 | Interaction protocol | Markdown | How the TA responds in each situation |
| D1.7 | LLM prompt templates | Text/Markdown | Draft prompts for all LLM call types |
| D1.8 | Architecture diagram | Markdown/Diagram | System component diagram |
| D1.9 | Low-fidelity UI wireframe | Markdown/Image | Basic wireframe of the interaction interface |

**Stage 1 is complete when all D1.x deliverables are reviewed and approved.**

---

## 18. Deliverables for Stage 2

Stage 2 is **implementation of the first functional prototype**:

| # | Deliverable | Format | Description |
|---|---|---|---|
| D2.1 | Backend API | Python (FastAPI) | Teaching endpoint, test endpoint, state endpoint |
| D2.2 | Knowledge state engine | Python module | State initialization, update logic, misconception activation |
| D2.3 | LLM integration layer | Python module | Prompt construction, API calls, response parsing |
| D2.4 | Code execution sandbox | Python/Docker | Sandboxed execution of TA-generated code |
| D2.5 | Problem selection engine | Python module | Select/generate problems based on knowledge state |
| D2.6 | Frontend (prototype) | Streamlit or React | Teaching conversation UI, test UI, mastery dashboard |
| D2.7 | Integration test suite | Python (pytest) | End-to-end tests of the teaching → testing loop |
| D2.8 | Demo script | Markdown | Step-by-step script for demonstrating the prototype |

**Stage 2 is complete when the prototype can run the full teaching → testing → reflection loop for at least 5 knowledge units with a live human student.**

---

## 19. Proceed Criteria

### Proceed from Stage 1 to Stage 2 when:
1. All Stage 1 deliverables (D1.1–D1.9) are created and reviewed.
2. The knowledge unit list is validated against at least 2 introductory Python syllabi.
3. The problem bank contains at least 50 problems with working test cases.
4. The LLM prompt templates have been manually tested with at least 5 simulated teaching scenarios.
5. The interaction protocol has been reviewed for pedagogical soundness.

### A successful Phase 1 prototype (end of Stage 2) is defined as:
1. A human student can teach the TA at least 5 knowledge units via conversation.
2. The TA's knowledge state updates reflect what was taught.
3. The TA can attempt programming problems and produce code consistent with its knowledge state.
4. The TA's code is automatically graded against test cases.
5. The student can see the TA's test results and diagnose errors.
6. The TA demonstrates at least 2 distinct misconceptions that are resolvable through re-teaching.
7. The full loop (teach → test → reflect → re-teach) is functional end-to-end.

---

## 20. Recommended Repository Structure

```
cs-teachable-agent/
├── PROPOSAL.md                    # This document
├── README.md                      # Project overview and setup instructions
├── .env.example                   # API key template
├── .gitignore
│
├── docs/
│   ├── architecture.md            # System architecture description
│   ├── interaction-protocol.md    # TA behavior specification
│   ├── mastery-rubric.md          # Mastery level definitions
│   └── wireframes/                # UI wireframes
│       └── main-interface.md
│
├── seed/
│   ├── knowledge-units.json       # Knowledge unit definitions
│   ├── misconceptions.json        # Misconception catalog
│   ├── problem-bank.json          # Programming problems with test cases
│   └── prompt-templates/
│       ├── ta-conversation.md     # Prompt for TA conversation behavior
│       ├── knowledge-extractor.md # Prompt for extracting knowledge from teaching
│       ├── code-generator.md      # Prompt for TA code generation
│       └── test-evaluator.md      # Prompt for evaluating TA's code rationale
│
├── src/
│   ├── backend/
│   │   ├── main.py                # FastAPI application entry point
│   │   ├── knowledge_state.py     # Knowledge state management
│   │   ├── llm_client.py          # LLM API integration
│   │   ├── teaching_engine.py     # Teaching interaction processing
│   │   ├── test_engine.py         # Problem selection and code grading
│   │   ├── sandbox.py             # Code execution sandbox
│   │   └── models.py              # Data models
│   │
│   └── frontend/
│       └── app.py                 # Streamlit prototype (or React app)
│
├── tests/
│   ├── test_knowledge_state.py
│   ├── test_teaching_engine.py
│   ├── test_sandbox.py
│   └── test_integration.py
│
└── scripts/
    ├── validate_problem_bank.py   # Validate all test cases in problem bank
    └── demo.py                    # Demo script for prototype walkthrough
```

---

## 21. Recommended Build Order

The build should proceed in this exact order:

### Phase A: Seed Resources (Stage 1)
1. **A1.** Write `knowledge-units.json` — Define all ~35 knowledge units with prerequisites and metadata
2. **A2.** Write `misconceptions.json` — Define all ~20–30 misconceptions linked to knowledge units
3. **A3.** Write `problem-bank.json` — Create ~50–100 problems with test cases, tagged by knowledge unit and difficulty tier
4. **A4.** Write `mastery-rubric.md` — Define mastery levels and computation rules
5. **A5.** Write `interaction-protocol.md` — Specify TA behavior in all interaction scenarios
6. **A6.** Write prompt templates — Draft and manually test all LLM prompts
7. **A7.** Write `architecture.md` — Finalize the system architecture
8. **A8.** Write UI wireframes — Low-fidelity wireframe of the interface

### Phase B: Core Backend (Stage 2)
9. **B1.** Implement `models.py` — Data models for knowledge units, misconceptions, problems, knowledge state
10. **B2.** Implement `knowledge_state.py` — Initialize, update, and query the TA's knowledge state
11. **B3.** Implement `llm_client.py` — LLM API integration with prompt template loading
12. **B4.** Implement `sandbox.py` — Sandboxed code execution with timeout and resource limits
13. **B5.** Implement `teaching_engine.py` — Process student teaching input, update knowledge state
14. **B6.** Implement `test_engine.py` — Select problems, generate TA code, grade results

### Phase C: API and Frontend (Stage 2)
15. **C1.** Implement `main.py` — FastAPI endpoints for teaching, testing, and state inspection
16. **C2.** Implement frontend — Streamlit or React interface with conversation panel, test panel, and mastery dashboard
17. **C3.** Write integration tests — End-to-end tests of the full loop
18. **C4.** Write demo script — Step-by-step demo for stakeholder review

---

## 22. Risks and Mitigation

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | LLM leaks knowledge the TA hasn't been taught | High | High | Strict prompt engineering; output validation against knowledge state; fallback rejection of responses that reference untaught concepts |
| R2 | LLM-generated code doesn't reflect misconceptions accurately | Medium | High | Explicit misconception injection in prompts; post-generation validation; human review of generated code samples |
| R3 | Sandbox escape during code execution | Low | Critical | Use Docker-based sandbox; restrict system calls; enforce strict timeouts; no network access |
| R4 | Student teaches in a way the system can't parse | Medium | Medium | Graceful degradation; TA asks for clarification; system logs unprocessable inputs for later analysis |
| R5 | Knowledge state update is too coarse or too fine | Medium | Medium | Iterative tuning; start with coarse updates and refine based on testing |
| R6 | Problem bank is too small to cover all knowledge units | Low | Medium | Ensure at least 2 problems per knowledge unit per difficulty tier during seed resource creation |
| R7 | LLM API costs exceed budget | Medium | Medium | Implement token counting; cache common prompts; use cheaper models for simple tasks |
| R8 | The TA persona is not convincing as a novice learner | Medium | High | Extensive prompt engineering; user testing with actual students; iterative persona refinement |
| R9 | Students may try to "cheat" by teaching the TA everything at once | Low | Low | The system allows this — it's a valid teaching strategy; the TA's imperfect retention handles it naturally |
| R10 | Scope creep into other CS domains during Phase 1 | Medium | High | This proposal explicitly excludes other domains; enforce through code review and task scoping |

---

## 23. Final Recommendation

**Begin with seed resources, not code.**

The most common failure mode for educational technology prototypes is building the application before defining the educational content. If the knowledge units are poorly defined, the misconceptions unrealistic, or the problems untested, no amount of engineering will produce a valid prototype.

The recommended path is:

1. **Approve this proposal** as the governing document for Phase 1.
2. **Create all seed resources** (knowledge units, misconceptions, problem bank, prompts) and validate them against educational standards.
3. **Only then begin implementation**, starting with the backend core (knowledge state engine, LLM integration, sandbox) and progressing to the frontend.
4. **Validate the prototype** against the success criteria in Section 19.
5. **Only after Phase 1 validation**, consider extending to other CS domains.

This approach minimizes wasted engineering effort and ensures that the prototype is educationally sound from the start.

---

## 24. Implementation Handoff Notes for Cursor

This section specifies exactly what the next Cursor implementation run should do after this proposal is approved.

### Immediate Next Actions (Stage 1 — Seed Resources)

**Action 1: Initialize repository structure**
Create the directory structure defined in Section 20. Create empty placeholder files where needed. Create `.gitignore` (Python template), `.env.example` (with `OPENAI_API_KEY=` or `ANTHROPIC_API_KEY=`), and a basic `README.md` linking to this proposal.

**Action 2: Create `seed/knowledge-units.json`**
Populate with all ~35 knowledge units defined in Section 11.1. Each unit must include:
- `id` (string, snake_case)
- `name` (string, human-readable)
- `description` (string, 1–2 sentences)
- `topic_group` (string, one of: fundamentals, operators, control_flow, functions, data_structures, miscellaneous)
- `prerequisites` (array of unit IDs)
- `related_misconceptions` (array of misconception IDs)
- `example_correct_code` (string, short Python snippet)
- `example_incorrect_code` (string, showing a common error)

**Action 3: Create `seed/misconceptions.json`**
Populate with ~20–30 misconceptions as outlined in Section 11.3. Each misconception must include:
- `id` (string, snake_case)
- `description` (string, 1–2 sentences)
- `affected_knowledge_units` (array of unit IDs)
- `example_incorrect_code` (string)
- `example_correct_code` (string)
- `remediation_hint` (string, what the student should teach to fix this)

**Action 4: Create `seed/problem-bank.json`**
Populate with at least 50 problems. Start with at least 2 problems per knowledge unit for the `remember` tier, then add `apply` and `transfer` tier problems. Each problem must include:
- `id` (string)
- `knowledge_units_tested` (array of unit IDs)
- `difficulty_tier` (string: `remember` | `apply` | `transfer`)
- `problem_statement` (string)
- `input_spec` (string or null)
- `expected_output_description` (string)
- `test_cases` (array of `{input: string, expected_output: string}`)
- `targeted_misconceptions` (array of misconception IDs)

**Action 5: Create `docs/mastery-rubric.md`**
Write the mastery rubric as defined in Section 10.4, including:
- Mastery level definitions
- Computation rules (how to aggregate test results)
- How misconceptions affect mastery scores

**Action 6: Create `docs/interaction-protocol.md`**
Write the interaction protocol as defined in Section 9, including:
- TA response patterns for different teaching inputs
- Knowledge state update triggers
- TA behavior during tests
- TA behavior when confused
- TA behavior when taught contradictory information

**Action 7: Create `seed/prompt-templates/`**
Create the four prompt template files:
- `ta-conversation.md`: System prompt for the TA in conversation mode. Must include the novice learner persona, instructions to never tutor the student, and the current knowledge state injection format.
- `knowledge-extractor.md`: System prompt for extracting taught knowledge from student messages. Must output structured updates to knowledge units.
- `code-generator.md`: System prompt for generating Python code constrained by knowledge state. Must include instructions for incorporating active misconceptions.
- `test-evaluator.md`: System prompt for the TA to explain its reasoning when solving a problem.

**Action 8: Create `docs/architecture.md`**
Write the architecture description based on Section 15.2, including the LLM call architecture diagram and data flow.

### What NOT to Do in the Next Cursor Run
- Do NOT write any Python source code in `src/`
- Do NOT create a `requirements.txt` or install any packages
- Do NOT set up a frontend
- Do NOT integrate with any LLM API
- Do NOT write any test code in `tests/`
- Do NOT create any Docker files

### Validation Before Proceeding to Stage 2
Before any implementation begins, the following must be true:
1. `seed/knowledge-units.json` contains ≥35 knowledge units with all required fields
2. `seed/misconceptions.json` contains ≥20 misconceptions with all required fields
3. `seed/problem-bank.json` contains ≥50 problems with working test case specifications
4. All four prompt templates exist and contain substantive draft prompts
5. `docs/mastery-rubric.md` and `docs/interaction-protocol.md` are complete
6. This proposal (`PROPOSAL.md`) is in the repository root

### After Stage 1 Validation
Once all seed resources are validated, the next Cursor run should begin Stage 2 implementation following the build order in Section 21, Phase B, starting with `models.py` and `knowledge_state.py`.

---

*End of Proposal*
