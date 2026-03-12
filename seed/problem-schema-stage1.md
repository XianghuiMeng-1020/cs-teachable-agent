# Stage One: Programming Problem Schema

This document defines the schema for Stage One programming problems. Problems are **curated** (selected from a fixed bank); full automatic problem generation is out of scope for Stage One.

---

## Scope

- All problems use **only** Stage One topics: variables and assignment, basic data types, input/output, operators, conditionals, loops, lists.
- No functions, classes, files, recursion, dictionaries, tuples, or external libraries.

---

## Schema Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **problem_id** | string | Yes | Unique identifier (e.g., `prob_var_001`). |
| **problem_statement** | string | Yes | Natural language description of what the program should do. |
| **input_spec** | string or null | Yes | Description of input (e.g., "One integer per line") or null if no input. |
| **test_cases** | array | Yes | List of `{ "input": string, "expected_output": string }`. Input is the raw stdin; expected_output is the exact stdout (including newlines). |
| **knowledge_units_tested** | array of strings | Yes | IDs from `knowledge-units-stage1.json` that this problem exercises. |
| **difficulty** | string | Yes | One of: `remember` (single concept, direct use), `apply` (combine 2–3 concepts). |
| **targeted_misconceptions** | array of strings | No | IDs from `misconceptions-stage1.json` that this problem can surface if the TA has them. |

---

## Field Details

### problem_id
- Unique within the problem bank.
- Convention: `prob_<topic_abbrev>_<number>`, e.g., `prob_var_001`, `prob_loop_003`.

### problem_statement
- Clear, self-contained instructions.
- Must be solvable using only Stage One constructs (no `def`, no `open()`, no dicts, etc.).

### input_spec
- Describe what the program reads (e.g., "One integer, then one string on the next line").
- Use `null` or empty string if the program produces output without reading input.

### test_cases
- At least one test case per problem.
- **input**: Exact string fed to stdin (e.g., `"5\n"` for the number 5 and newline).
- **expected_output**: Exact string the correct program must print to stdout (including trailing newline if required).
- Grading: run TA's code with each input, compare stdout to expected_output (exact or trimmed per implementation rule).

### knowledge_units_tested
- Subset of knowledge unit IDs from Stage One.
- Used to map test results to per-unit mastery and to select problems appropriate to the TA's current knowledge state.

### difficulty
- **remember**: Single concept, direct application (e.g., "Create a variable x with value 10 and print it").
- **apply**: Combine 2–3 concepts (e.g., "Read a number and print whether it is even or odd").

### targeted_misconceptions
- Optional. Lists misconception IDs that this problem is designed to expose (e.g., a problem requiring `==` in a condition targets `assign_vs_equal`).

---

## How This Schema Supports the Programming Mastery Test

1. **Test assembly**: The mastery test is built by **selecting** problems from the bank that match the TA's taught knowledge units. The schema's `knowledge_units_tested` enables filtering (e.g., only problems that use `for_loop_range` and `print_function`).

2. **Grading**: Each problem has executable `test_cases`. The system runs the TA's code with each input and compares stdout to `expected_output`. Pass/fail per test case, then per problem (e.g., all test cases must pass for the problem to pass).

3. **Mastery computation**: Results (which problems passed) are aggregated by `knowledge_units_tested` to compute per-knowledge-unit mastery and overall mastery, as defined in `docs/mastery-rubric-stage1.md`.

4. **No generator**: Problems are stored in a JSON file (e.g., `sample-problems-stage1.json`). Selection is by query over the bank; generation of new problems is deferred.

---

## Example Problem (Minimal)

```json
{
  "problem_id": "prob_var_001",
  "problem_statement": "Write a program that creates a variable named age, assigns it the value 20, and prints that value.",
  "input_spec": null,
  "test_cases": [
    { "input": "", "expected_output": "20\n" }
  ],
  "knowledge_units_tested": ["variable_assignment", "print_function"],
  "difficulty": "remember",
  "targeted_misconceptions": []
}
```
