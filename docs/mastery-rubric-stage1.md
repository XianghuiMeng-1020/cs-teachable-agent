# Stage One: Mastery Rubric

This document defines how the programming test results map to the TA's mastery level. The **structured knowledge state** is the only source of truth for what the TA "knows"; test results are used to **examine** and **report** mastery.

---

## Inputs

- **Per problem:** The TA's code is run against each test case. A problem **passes** if the TA's output matches the expected output for every test case (exact or normalized per implementation).
- **Per knowledge unit:** Each problem has `knowledge_units_tested`. A passed (or failed) problem counts toward mastery for each of those units.

---

## Per–Knowledge-Unit Mastery

For each knowledge unit (e.g., `for_loop_range`):

1. Collect all problems that list this unit in `knowledge_units_tested` and that the TA has **attempted** (i.e., the TA was given the problem and produced code).
2. Compute: **passed_count** = number of those problems the TA passed; **attempted_count** = number attempted.
3. If **attempted_count** is 0, the unit is **not_assessed**.
4. Otherwise compute **pass_rate** = passed_count / attempted_count (a number between 0 and 1).

**Levels (per unit):**

| Level | Condition |
|-------|-----------|
| **failing** | pass_rate < 0.5 |
| **developing** | 0.5 ≤ pass_rate < 0.8 |
| **proficient** | pass_rate ≥ 0.8 |

No "mastered" tier in Stage One; keep thresholds simple. Optionally, if a unit has both `remember` and `apply` problems, proficient could require passing at least one of each—but for Stage One, a single pass_rate threshold is enough.

---

## Overall Mastery

1. Collect all problems the TA has attempted (any unit).
2. **overall_pass_rate** = (number of problems passed) / (number of problems attempted).
3. If no problems attempted, overall mastery is **not_assessed**.

**Levels (overall):**

| Level | Condition |
|-------|-----------|
| **failing** | overall_pass_rate < 0.5 |
| **developing** | 0.5 ≤ overall_pass_rate < 0.8 |
| **proficient** | overall_pass_rate ≥ 0.8 |

---

## How Misconceptions Affect Reporting (Optional)

- If the TA has an active misconception (recorded in knowledge state), the system may **label** that unit as having a misconception when showing results to the student.
- Mastery level is still computed from pass/fail. The misconception is explanatory (e.g., "TA is developing on conditionals but has assign_vs_equal"), not a separate threshold.
- Stage One keeps this lightweight: report pass rates and levels; optionally surface which misconceptions are active for context.

---

## Summary

- **Per unit:** pass_rate over attempted problems that test that unit → failing / developing / proficient.
- **Overall:** pass_rate over all attempted problems → failing / developing / proficient.
- **Not assessed:** no problems attempted for that unit (or at all).
- **Single source of truth:** The knowledge state holds what was taught; the test **examines** mastery. Results update the **report** to the student; the implementation may also update state (e.g., "last test result") but the canonical "what the TA is allowed to know" remains the structured knowledge state.
