# Stage One: Interaction Protocol

This document specifies how the student teaches the TA, how the TA responds, how curated problems are used, and how testing and results work. It stays aligned with the teacher's goal: **zero-knowledge TA**, **mastery test**, **interaction design** with **explanation**, **conversation**, and **programming problems**.

The **structured knowledge state** is the only source of truth. The TA must not use or mention any concept outside the current Stage One knowledge state.

**Stage One loop in one sentence:** You teach by explaining and talking; the TA replies as a learner; you then give it problems to try, and the test results show what it has learned. You can re-teach if the TA fails.

---

## For the student: getting started

- **What to do first:** Start by teaching one concept (e.g. variables and assignment, or variables and `print()`). Explain in your own words and optionally show a short code example. The TA will respond as a learner—restating, asking questions, or saying what it thinks it learned. You can then teach more or move to testing.
- **When to test the TA:** You can test the TA after teaching one topic or after several—whenever you want to see how much it has learned. Ask the system to give the TA a problem (or a short test) that matches what you have taught. There is no fixed moment; test when it feels right.
- **If the TA fails a problem:** Use the TA’s code and the expected output to decide what went wrong. Then re-explain the concept, clarify a misconception (e.g. the difference between `=` and `==`), or teach a related idea. After that, you can give the same or another problem to see if the TA does better.
- **Summary of the flow:** Teach → TA responds → give a problem → review the result → re-teach if needed. Repeat as you like.

---

## 1. How the Student Teaches

### 1.1 Modes of Teaching

- **Explanation:** The student explains a concept in natural language (e.g., "A variable is like a box; you write x = 5 to put 5 in the box.").
- **Code examples:** The student may show correct (or incorrect) code snippets as part of the explanation (e.g., "So you can do: age = 20").
- **Conversation:** The student may answer the TA's questions, clarify, or correct the TA's restatements.

The system does **not** prescribe curriculum order. The student chooses what to teach and when. Teaching is interpreted and mapped to **knowledge units** from Stage One only (variables, basic data types, input/output, operators, conditionals, loops, lists).

### 1.2 What Gets Updated

After each teaching exchange (or after a coherent block of explanation), the system updates the TA's **knowledge state**: the relevant knowledge units move from `unknown` to `partially_learned` or `learned` based on the content and correctness of the teaching. The exact rule (e.g., one explanation → partially_learned, two consistent explanations → learned) is an implementation detail; the protocol requires that state updates are driven only by student input and only within Stage One scope.

---

## 2. How the TA Responds (Learner Persona)

### 2.1 Role

The TA is a **learner**, not a tutor. It does not explain Python to the student. It does not give hints or correct the student's code. It only:

- Reacts to what the student said (e.g., restates in its own words).
- Asks clarifying questions ("Can the variable hold words too?").
- Expresses confusion when something is unclear or contradictory.
- Acknowledges what it thinks it learned ("So x = 5 puts 5 in the box?").

### 2.2 Constraint by Knowledge State

The TA's responses must be **consistent with its current knowledge state**:

- It must not claim to know concepts that are still `unknown`.
- It must not use or refer to concepts outside Stage One (no functions, no dictionaries, etc.).
- If asked to do something that requires an untaught concept, it should respond as a novice would (e.g., "I don't know how to do that yet" or "You haven't taught me about loops.").

### 2.3 No Tutoring

The TA never teaches the student. It never explains syntax, suggests solutions, or evaluates the student's code. Its only "output" to the student is: (1) conversational replies in the teaching flow, and (2) code and test results when taking a programming test.

---

## 3. Explanation and Conversation Flow

### 3.1 Typical Turn

1. **Student** sends a message (explanation and/or code).
2. **System** interprets the message and updates the knowledge state (which units are touched, and how).
3. **TA** generates a reply as a novice: restate, question, or express confusion. The reply is constrained by the current knowledge state (so the TA does not "leak" knowledge it hasn't been taught).
4. **Student** may continue explaining or switch topic.

### 3.2 Multi-Turn Teaching

Teaching can span multiple turns. The state accumulates: repeated or reinforced teaching of the same unit can move it from `partially_learned` to `learned`. Contradictory teaching may leave the unit in `partially_learned` or trigger a misconception (if the system models misconceptions).

---

## 4. How Curated Problems Are Introduced

### 4.1 Source of Problems

Problems come from the **curated problem bank** only (e.g., `sample-problems-stage1.json`). There is **no** automatic problem generator in Stage One. Problems are **selected** from the bank.

### 4.2 When Problems Are Used

- **After teaching:** The student (or the system, if designed) can offer a problem for the TA to try after the student has taught one or more topics. This supports "try what you learned."
- **For the mastery test:** The student or system can trigger a **test**: a set of problems selected to examine the TA's mastery (e.g., one or more problems per taught knowledge unit).

### 4.3 Selection Rule

Problems are selected so that they **only use knowledge units the TA has been taught** (or that are under examination). For example, if the TA has not learned loops, do not give it a loop problem (or give it and expect failure; the protocol prefers not to use concepts not yet taught, so the TA is not asked to use unknown concepts). Concretely: filter the bank by `knowledge_units_tested` and only offer problems whose units are all in the TA's "learned" or "partially_learned" set, or explicitly allow "challenge" problems for diagnostic purposes—for Stage One, the simple rule is: **only assign problems that match the TA's current knowledge state** so that the test is a fair examination of what was taught.

---

## 5. How Testing Happens

### 5.1 Test Flow

1. The student (or system) selects one or more problems from the bank (per selection rule above).
2. For each problem, the TA **produces code**. The TA's code must be generated under the constraint of the **current knowledge state** and any active **misconceptions**—i.e., the TA must not use concepts it hasn't learned, and it may exhibit errors consistent with its misconceptions.
3. The system **runs** the TA's code against each test case (stdin → compare stdout to expected_output).
4. The problem is **passed** if all test cases pass; otherwise **failed**.
5. Results are stored (e.g., problem_id, passed/failed, TA's code, expected vs actual output) for mastery computation and for display.

### 5.2 Mastery Examination

Mastery is computed from these results using the rubric in `docs/mastery-rubric-stage1.md`: per–knowledge-unit and overall pass rates, with thresholds (failing / developing / proficient).

---

## 6. How Results Are Shown to the Student

### 6.1 After Each Problem

The student should see:

- The problem statement.
- The TA's code.
- For each test case (or a summary): whether the output matched. Optionally, expected vs actual output for failed cases.
- Whether the problem **passed** or **failed** overall.

### 6.2 After a Test (Multiple Problems)

The student should see:

- A **mastery summary**: per knowledge unit (and overall), the level (failing / developing / proficient) or not_assessed.
- Optionally, which problems were passed or failed and the TA's code for each.

This supports reflection: "Why did the TA get this wrong? What should I teach next?"

---

## 7. Alignment with Teacher Goal

| Teacher goal | Protocol element |
|--------------|-------------------|
| TA has no knowledge in programming | Initial state: all units `unknown`; TA behavior reflects ignorance until taught. |
| Programming test to examine TA mastery | Problems from curated bank; run TA code; compare output; compute mastery per rubric. |
| TA learns from human student interaction | Student teaches via explanation and conversation; knowledge state updates from that input only. |
| Conversation + problems | Conversation for teaching; curated problems for testing and for practice during teaching. |
| Interaction design | This document defines the full flow: teach → state update → TA reply; problem selection → TA codes → grading → results to student. |

The TA never uses concepts outside the current Stage One knowledge state. The knowledge state is the only source of truth for what the TA "knows."
