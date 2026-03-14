# Diagnose Misconception from Failed Attempt

You are an expert in diagnosing learner errors. The TA (teachable agent) just produced a **wrong** solution to a problem. Your job is to infer which **known misconception** best explains the error.

## Problem statement
{{PROBLEM_STATEMENT}}

## Knowledge units tested by this problem
{{UNITS_TESTED}}

## TA's wrong code or answer
{{TA_CODE_OR_ANSWER}}

## Known misconceptions (id and short description)
{{MISCONCEPTIONS}}

## Task
Output a single JSON object with key **candidates**: a list of up to 3 items. Each item has:
- **misconception_id**: one of the known misconception IDs from the list above
- **affected_unit_id**: one knowledge unit ID from UNITS_TESTED that this misconception affects
- **confidence**: number 0–1 (how likely this misconception explains the error)

Example:
{"candidates": [{"misconception_id": "off_by_one_range", "affected_unit_id": "for_loop_range", "confidence": 0.85}, {"misconception_id": "assign_vs_equal", "affected_unit_id": "if_statement", "confidence": 0.4}]}

Output only the JSON, no other text.
