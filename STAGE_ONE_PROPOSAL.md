# Stage One Proposal: Teachable Agent — Zero Knowledge, Mastery Test, and Interaction Design

**Document Type:** Focused first-step proposal (companion to PROPOSAL.md)  
**Date:** 2026-03-12  
**Context:** Please treat this as a follow-up clarification from the user: the teacher's immediate concern is the first executable step, not the full system.

This document does **not** replace the master proposal (PROPOSAL.md). It narrows scope to the teacher's stated immediate goals and defines what Stage One must deliver before building a larger system.

---

## 1. Stage One Goal

Stage One has three concrete goals:

1. **Define a teachable agent (TA) that starts with no programming knowledge** — so that the system has a clear, testable starting point.
2. **Design and specify a programming test** that can **examine the TA's mastery level in programming** — so that we can measure what the TA has learned.
3. **Determine the design for the interaction** through which the TA **learns Introductory Python from human student interaction** — including explanation, conversation, and generated programming problems — so that the first executable stage has a complete interaction model.

Stage One is **design and seed-resource only**. No application code, no frontend, no backend. The outcome is a set of specifications and seed assets that a later Cursor run can use to build the first executable prototype.

---

## 2. Direct Alignment with Teacher Goal

The teacher's wording is reflected directly:

| Teacher statement | Stage One response |
|---|---|
| "A teachable agent (TA) has no knowledge in programming" | Section 6 defines the TA's zero-knowledge state precisely. |
| "Let's find a programming test to examine the TA mastery level in programming" | Section 11 specifies the programming mastery test design. |
| "Teachable agents can learn programming (Intro to Python) from human student interaction" | Section 8 and 12 define how the TA learns from that interaction. |
| "Such as explanation, or generated programming problems" | Section 8–10 spell out explanation, conversation, and problem generation. |
| "Let's determine the design for the interaction" | Section 8 is the interaction design. |
| "Conversation could be part of it, but we should also prepare some problem generation" | Section 9 explains why conversation alone is not enough; Section 10 defines the role of generated problems. |

This document stays within this wording. It does not expand to full product, other domains, or implementation stack.

---

## 3. Why This Must Start with Zero Programming Knowledge

The TA must start with **no usable programming knowledge** for three reasons:

1. **Pedagogical validity.** The teachable-agent paradigm assumes the agent is the learner. If the TA already "knows" Python, the student is not teaching — they are chatting with a system that pretends to learn. Zero knowledge makes the student's teaching the sole source of the TA's competence.

2. **Testability.** We need a programming test to *examine* mastery. If the TA starts with knowledge, we cannot cleanly attribute test results to what the student taught. A zero-knowledge baseline means: any correct behavior on the test must have come from the interaction.

3. **Design constraint.** Defining "no knowledge" forces us to specify exactly what counts as a knowledge unit and what the initial state looks like. That specification is necessary for both the mastery test (what we are testing) and the interaction (what the student can teach).

Therefore, Stage One must **explicitly define** the TA's initial state: no knowledge units marked as learned, no prior code-writing ability, and behavior that reflects ignorance (e.g., "I don't know what a variable is") until the student teaches it.

---

## 4. Why Introductory Python is the Right First Scenario

Introductory Python is the right first scenario because:

- **Executable and testable.** We can run the TA's code and compare output to expected output. Mastery is measurable.
- **Bounded.** A small set of topics (variables, types, I/O, operators, conditionals, loops, lists) is enough to design a test and an interaction without covering all of CS.
- **Aligned with "Intro to Python."** The teacher specified Introductory Python; Stage One limits to the subset listed in Section 5 below.

Other domains (AI Literacy, Database, etc.) are **not** part of Stage One. They are later extensions.

---

## 5. Narrow Scope of Stage One

### 5.1 Python Topics Included (Only These)

Stage One **locks** the scope to these Introductory Python topics:

| Topic | Description | Example concepts |
|---|---|---|
| **Variables and assignment** | Storing values in names | `x = 5`, `name = "Alice"` |
| **Basic data types** | int, float, str, bool | Literals, type of values |
| **Input/output** | Reading and printing | `input()`, `print()` |
| **Operators** | Arithmetic, comparison, logical | `+`, `==`, `and`, `or` |
| **Conditionals** | Branching | `if`, `else`, `elif` |
| **Loops** | Repetition | `while`, `for` (with `range()` and over sequences) |
| **Lists** | Ordered sequences | Creating lists, indexing, `len()`, iterating |

No other Python topics are in scope for Stage One.

### 5.2 Python Topics Explicitly Excluded in Stage One

The following are **out of scope** for Stage One. They may be added in later stages:

- **Functions** (def, parameters, return)
- **Classes and OOP**
- **Files** (reading/writing files)
- **Recursion**
- **Dictionaries**
- **Tuples** (beyond what is minimally needed for `for` over sequences, if any)
- **External libraries** (e.g., `math`, `random`)

If a concept is not in the table in 5.1, it is excluded unless explicitly mentioned as a later extension.

### 5.3 Non-Software Scope Limits

Stage One also does **not** include:

- Frontend or backend implementation
- Multi-user support, authentication, or cloud deployment
- Full product stack or production architecture
- Any domain other than Introductory Python (no AI Literacy, Database, etc.)

---

## 6. What the TA Should Be in Stage One

The TA in Stage One is:

- **A learner with zero initial programming knowledge.** It does not know variables, types, I/O, operators, conditionals, loops, or lists until the student teaches them.

- **A simulated novice.** It behaves like a beginner: can ask clarifying questions, restate what it thinks it learned, and express confusion. Its responses are constrained by a **knowledge state** (Section 12) that records what has been taught.

- **Capable of being tested.** When given a programming problem (from the mastery test or problem bank), it produces Python code that reflects **only** what it has been taught and any designated misconceptions. It does not use concepts it has not learned.

- **Updated by interaction.** When the student explains or teaches, the system updates the TA's knowledge state. That state drives both the TA's conversational behavior and its code generation.

- **A single agent per session.** One TA, one student, one session. No persistence or user accounts required for Stage One design.

---

## 7. What the TA Should Not Be

The TA in Stage One is **not**:

- **A tutor.** It does not teach the student. It does not explain Python, give hints, or correct the student's code.
- **A coding assistant.** It does not help the student write code. It writes code only when taking a programming test, and that code reflects its (possibly wrong) understanding.
- **An omniscient chatbot.** It must not behave as if it already knows Python. The design must ensure that the TA's behavior is governed by the knowledge state (and, if used, by prompts that inject that state), not by the full knowledge of an underlying model.
- **Multi-domain.** It only "learns" Introductory Python as scoped in Section 5. It does not learn AI Literacy, databases, or other CS topics in Stage One.

---

## 8. Interaction Design for Stage One

The interaction is how the TA learns Introductory Python from the human student. It has two main channels.

### 8.1 Channel 1: Explanation and Conversation

- **Explanation:** The student explains concepts in natural language and/or with code examples (e.g., "A variable is like a box; you write `x = 5` to put 5 in the box.").
- **Conversation:** The TA responds as a novice — e.g., asking "Can the box hold words too?", restating ("So `x` is the name of the box?"), or expressing confusion. The TA does not explain Python to the student.

The design must specify:
- How the student's explanation is interpreted (e.g., mapped to knowledge units).
- How the TA's reply is generated so it stays consistent with the current knowledge state.
- That the TA never teaches; it only learns and responds as a learner.

### 8.2 Channel 2: Generated Programming Problems

- **Problems** are programming tasks (e.g., "Write a program that asks for a number and prints whether it is even or odd.").
- They can be **selected** from a fixed problem bank or **generated** (e.g., from templates) so that they align with the TA's current knowledge state.
- The TA **attempts** the problem by writing code. The system **grades** the code (e.g., by running it against given inputs and comparing output).
- Results (pass/fail, and the TA's code) are shown so the student can see the TA's mastery and reflect on what to teach next.

The design must specify:
- How problems are selected or generated for the TA's current state.
- How the TA's code is produced (constrained by knowledge state).
- How grading is done (e.g., test cases, expected output).
- How results are summarized for the student (mastery signal).

### 8.3 How the Two Channels Work Together

- **Conversation/explanation** → TA's knowledge state is updated.
- **Problems** → TA is tested on that state; results show mastery.
- **Student** uses test results to decide what to explain next or what to re-explain.

So the interaction design for Stage One is: **explanation + conversation** for teaching, and **generated/selected programming problems** for testing and mastery examination. Both are required.

---

## 9. Why Conversation Alone Is Not Enough

Conversation (and explanation) alone is **not** enough to examine the TA's mastery in programming, for these reasons:

1. **No proof of application.** The TA might repeat correct-sounding explanations without being able to write correct code. Programming mastery requires producing runnable, correct code, not only talking about it.

2. **No objective mastery signal.** Without a programming test, we cannot measure mastery. Conversation gives no clear, comparable measure across topics or over time.

3. **No concrete failure mode.** When the TA fails a problem, the student sees *what* went wrong (e.g., wrong operator, wrong loop bound). That supports reflection and re-teaching. Conversation alone does not provide that.

4. **Teacher's requirement.** The teacher asked for a "programming test to examine the TA mastery level" and to "prepare some problem generation." So tests and problems are required, not optional.

Therefore, Stage One design must include **both** conversation/explanation **and** programming problems (and a test built from them).

---

## 10. Role of Generated Programming Problems

Generated (or selected) programming problems serve two roles in Stage One:

1. **Mastery examination.** A **programming test** is built from problems. The TA solves them by writing code; the system runs the code and scores it. The test result is the TA's mastery level (per topic or overall).

2. **Interaction and learning support.** Problems can be used **during** teaching, not only at the end: the student can give the TA a problem to try after explaining a topic. So problem generation (or selection) supports both testing and the teaching loop.

Design requirements for problems:

- Each problem is tied to one or more **knowledge units** (from the narrow set in Section 5).
- Each problem has a clear **task** (what the program should do), **input/output specification**, and **test cases** (inputs and expected outputs) for automatic grading.
- Problems can be **selected** from a fixed bank and/or **generated** (e.g., from templates) so that they match the TA's current knowledge (e.g., no problems requiring loops if the TA has not learned loops).

Stage One must specify the **format** of problems (so a problem bank and/or generator can be built later) and how they feed into the mastery test (Section 11).

**Stage One seed resources:** For Stage One seed resources, a curated schema plus sample problems is sufficient. Full automatic problem generation is optional and can be deferred. The next implementation step should not prioritize building a problem generator engine; selecting from a fixed problem bank is enough for the first executable prototype.

---

## 11. Proposed Programming Mastery Test

The programming test is the way we **examine the TA's mastery level in programming**. It is not a human exam; it is an automated assessment of the TA's code.

### 11.1 What the Test Is

- A set of **programming problems** drawn from the problem bank (or generated), restricted to Stage One topics: variables, basic types, I/O, operators, conditionals, loops, lists.
- For each problem, the TA **produces Python code**. The system **runs** the code on predefined inputs and **compares** output to expected output.
- **Mastery** is derived from which problems the TA passes (and optionally from difficulty or knowledge-unit tags).

### 11.2 Test Structure (Per Problem)

Each item in the test should have:

- **Problem ID**
- **Problem statement** (what the program should do)
- **Input specification** (if any)
- **Expected output** (or multiple test cases: input → expected output)
- **Knowledge units tested** (subset of the Stage One list)
- **Difficulty** (e.g., remember / apply), so mastery can be reported by level

### 11.3 How Mastery Is Examined

- **Per knowledge unit:** e.g., percentage of problems passed that tag that unit, or count of problems passed vs. attempted for that unit.
- **Overall:** e.g., percentage of all problems passed, or a simple level (e.g., failing / developing / proficient) based on thresholds.

The exact thresholds (e.g., what counts as "proficient") should be defined in a **mastery rubric** (Section 13). The important point is: the test is **objective** (run code, compare output) and **scoped** to the Stage One knowledge units.

### 11.4 When the Test Is Used

- The student (or system) can trigger a test **after** some teaching, to see the TA's current mastery.
- The same test design can support both "spot checks" (a few problems) and a "full mastery test" (more problems across units). Stage One design should specify both use cases at a conceptual level.

---

## 12. Proposed Knowledge State for Stage One

The TA's **knowledge state** is the internal representation of what the TA "knows" and "does not know." It drives the TA's behavior and is updated by the interaction.

### 12.1 Purpose

- **Initial state:** All Stage One knowledge units are "unknown" (zero knowledge).
- **After teaching:** Units that the student has explained are updated (e.g., to "partially_learned" or "learned").
- **For testing:** When the TA is given a problem, it may only use concepts in units that are at least partially learned; otherwise it should not produce correct code for those concepts (or should express that it doesn't know).
- **For conversation:** The TA's replies should be consistent with this state (e.g., it doesn't claim to know loops if the loop unit is still "unknown").

### 12.2 Knowledge Units for Stage One

Only the topics in Section 5 are represented. Suggested units (to be fully enumerated in seed resources):

- **Variables and assignment:** e.g., `variable_assignment`
- **Basic data types:** e.g., `data_types_int_float`, `data_types_string`, `data_types_bool`
- **Input/output:** e.g., `print_function`, `user_input`
- **Operators:** e.g., `arithmetic_operators`, `comparison_operators`, `logical_operators`
- **Conditionals:** e.g., `if_statement`, `if_else`, `if_elif_else`
- **Loops:** e.g., `while_loop`, `for_loop_range`, `for_loop_iterable` (for lists/sequences)
- **Lists:** e.g., `list_creation`, `list_indexing`, `list_iteration`, `list_basics` (e.g., `len()`)

The exact list and IDs should be fixed in the **Required Seed Resources** (Section 13). Optional: a small set of **misconceptions** (e.g., `=` vs `==`, off-by-one in `range`) so the TA can exhibit plausible errors when tested.

### 12.3 State Per Unit

For each knowledge unit, the state can include at least:

- **Status:** e.g., `unknown` | `partially_learned` | `learned` (and optionally `misconception`)
- **Optional:** confidence, last_taught time, or teach count — if useful for the first executable version.

The mastery test (Section 11) uses **test results** (which problems were passed) to compute mastery; the knowledge state is the **input** to the TA's behavior (what it "knows" when it talks and when it codes).

**Single source of truth for the executable prototype:** In the later executable prototype, the TA must not use any concept outside the current Stage One knowledge state. The structured knowledge state is the only source of truth for what the TA "knows." Any component that drives the TA's conversation or code generation must read from this state and must not allow the TA to exhibit knowledge of concepts that are not yet learned (or to use constructs from out-of-scope topics such as functions or dictionaries).

---

## 13. Required Seed Resources for Stage One

Before building any application, Stage One should produce these **seed resources** (design artifacts and data):

### 13.1 Knowledge Unit Definitions

- A structured file (e.g., JSON or YAML) listing every Stage One knowledge unit.
- For each unit: id, name, short description, topic group (e.g., variables, loops, lists), optional prerequisites, example correct code snippet, optional example incorrect code (for misconceptions).

### 13.2 Problem Bank (or Problem Schema + Sample Problems)

- A set of programming problems that:
  - Use only Stage One topics.
  - Include problem statement, input/output spec, and test cases (input → expected output).
  - Are tagged with knowledge units and difficulty (e.g., remember/apply).
- Either: a **problem bank file** with a defined schema, or a **schema document** plus a small number of example problems so that a full bank can be created later.

### 13.3 Mastery Rubric

- A short document that defines:
  - How test results (pass/fail per problem) map to mastery **per knowledge unit** and **overall**.
  - Thresholds (e.g., what is "proficient" vs "developing" vs "failing").
  - Optionally, how misconceptions affect the reported mastery.

### 13.4 Interaction Protocol

- A document that describes:
  - How the student teaches (explanation, conversation).
  - How the TA responds (learner persona, no tutoring).
  - How knowledge state is updated after teaching.
  - How problems are selected or generated for the TA.
  - How the TA generates code when given a problem (constrained by knowledge state).
  - How results are presented to the student (e.g., pass/fail, TA's code, mastery summary).

### 13.5 Optional: Misconception List

- A short list of common misconceptions for Stage One topics (e.g., assignment vs comparison, range bounds), with id, description, and affected knowledge units. This supports the TA making plausible errors and the student diagnosing them.

---

## 14. Deliverables for Stage One

Stage One is **complete** when the following deliverables exist (no code required):

| # | Deliverable | Description |
|---|---|---|
| D1 | Stage One Proposal | This document (STAGE_ONE_PROPOSAL.md). |
| D2 | Knowledge unit definitions | Structured list of all Stage One KUs (variables, types, I/O, operators, conditionals, loops, lists) with metadata. |
| D3 | Problem bank schema + sample problems | Schema for a problem (statement, I/O, test cases, tags), plus at least 10–15 sample problems covering all Stage One topics. |
| D4 | Mastery rubric | How test results map to mastery level (per unit and overall); thresholds. |
| D5 | Interaction protocol | Written specification of teaching flow, TA behavior, problem use, and mastery reporting. |
| D6 | Optional: misconception list | List of misconceptions for Stage One topics, with IDs and linked knowledge units. |

These are the assets that the **next** Cursor run (or implementation stage) will use to create the first executable prototype. No frontend/backend implementation is part of Stage One.

---

## 15. Constraints and Non-Goals

### Constraints

- **Python scope:** Only variables, basic data types, I/O, operators, conditionals, loops, lists. No functions, classes, files, recursion, dictionaries, tuples, or external libraries in scope.
- **Single TA, single student, single session.** No multi-user, no auth, no persistence across sessions for Stage One design.
- **Design and seed resources only.** No application code, no deployment, no production architecture.

### Non-Goals for Stage One

- No AI Literacy, Database, or other CS domains.
- No full product stack, frontend/backend implementation plan, or production infrastructure.
- No multi-user, cloud deployment, or authentication.
- No expansion of Python beyond the seven topic areas above.
- No code writing in this stage — only proposals and seed resource definitions.

---

## 16. Proceed Criteria for Moving Beyond Stage One

Proceed from Stage One to implementation (e.g., first executable prototype) when:

1. **All Stage One deliverables (D1–D6)** are complete and reviewed.
2. **Knowledge units** are fixed and cover only the seven Stage One topics; each has a clear id and description.
3. **Problem bank schema and sample problems** exist; sample problems have test cases and are tagged with knowledge units and difficulty.
4. **Mastery rubric** clearly defines how the programming test is used to examine the TA's mastery level (per unit and overall).
5. **Interaction protocol** clearly describes explanation, conversation, problem use, and how the TA's knowledge state is updated and used.

After that, the next step can be to build the first executable version: e.g., a minimal run where the TA starts with zero knowledge, the student "teaches" via a simple interface, and the TA is tested with problems from the bank and receives a mastery report. That implementation is **not** part of Stage One; it is the immediate follow-on.

---

## 17. Recommended Next Cursor Step After Approval

After this Stage One Proposal is approved:

1. **Keep PROPOSAL.md** as the overall master plan. Do not replace or rewrite it.
2. **Create the Stage One seed resources** in the repository:
   - **Knowledge unit definitions file** — All units for variables, basic types, I/O, operators, conditionals, loops, lists; one structured file (e.g., `seed/knowledge-units-stage1.json` or similar).
   - **Problem bank schema** — Document or JSON schema describing: problem_id, statement, input_spec, expected_output or test_cases, knowledge_units_tested, difficulty.
   - **Sample problems** — At least 10–15 problems that fit the schema and cover the seven topics; include test cases for each.
   - **Mastery rubric** — Short document (e.g., `docs/mastery-rubric-stage1.md`) defining how test results map to mastery levels.
   - **Interaction protocol** — Document (e.g., `docs/interaction-protocol-stage1.md`) describing the teaching flow, TA behavior, and use of problems.
   - **Optional: misconception list** — Small list of misconceptions for Stage One topics (e.g., `seed/misconceptions-stage1.json` or a section in the interaction protocol).
3. **Do not yet** write application code, frontend, backend, or deployment. The next step after seed resources is to use these assets to implement the first executable prototype (as in the master proposal, Stage 2).

4. **When implementing the prototype later:** Use a **curated problem bank** (schema + sample problems); do not build a full automatic problem generator. Treat the **structured knowledge state as the only source of truth** — the TA must not use concepts outside that state.

This keeps the teacher's immediate first-step goal — zero-knowledge TA, programming test for mastery, interaction design with conversation and problem generation — as the single focus of Stage One.

---

*End of Stage One Proposal*

---

**说明（给 Cursor）：**  
本文档是用户对教师目标的补充说明：教师当前关心的是「第一步可执行成果」，而不是完整系统。请将本 Stage One 提案视为与主提案（PROPOSAL.md）配套的聚焦文档，在实施时优先完成本文档中列出的种子资源与设计产物，再进入主提案中的 Stage 2 实现阶段。
