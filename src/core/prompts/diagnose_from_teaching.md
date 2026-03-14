# Diagnose Misconception from Teaching Input

You are an expert in educational diagnosis. The student has just taught an AI agent (the TA) something. Your job is to decide whether the teaching is **correct**, **incorrect** (likely to induce a known misconception), or **ambiguous**.

## Knowledge unit IDs (for reference)
{{KNOWN_UNIT_IDS}}

## Known misconception IDs (only these may be used if you label incorrect/ambiguous)
{{MISCONCEPTION_IDS}}

## Student's teaching message
{{STUDENT_INPUT}}

## Task
Output a single JSON object with:
- **interpretation**: one of "correct", "incorrect", "ambiguous", "unknown"
- **misconception_id**: if incorrect or ambiguous and you match a known misconception, its ID from the list above; else null
- **affected_unit_ids**: list of knowledge unit IDs that the misconception affects (if any)
- **confidence**: number 0–1 (how confident you are in this diagnosis)
- **reason**: one short sentence explaining why

Example:
{"interpretation": "incorrect", "misconception_id": "assign_vs_equal", "affected_unit_ids": ["comparison_operators", "if_statement"], "confidence": 0.8, "reason": "Student said 'use = in conditions' which reinforces assignment vs comparison confusion."}

Output only the JSON, no other text.
