# Researcher Guide — CS Teachable Agent

This guide describes how to use the system for research: trace data, analytics export, and experimental configuration.

## Trace and history

- **Trace events** are stored per teaching session in the `trace_events` table. Each event has `session_id`, `event_type`, and `payload` (JSON).
- **GET /api/ta/{ta_id}/trace** returns all trace events for that TA (across its sessions), ordered by time. Use this to reconstruct the full teaching–testing cycle.
- **GET /api/ta/{ta_id}/history** returns a paginated list of teaching and test events (teach, test_pass, test_fail) with titles and timestamps.
- **GET /api/ta/{ta_id}/messages** returns the conversation history (student input and TA response) for that TA.

## Analytics export (teacher)

- **Analytics** (GET /api/teacher/analytics) includes: student count, average mastery, knowledge coverage per KU, mastery trend (last 7 days), misconception counts, per-student-per-unit status, and recent activity.
- The **Export data (JSON)** button on the Analytics page downloads a JSON file containing all of the above plus a timestamp. Use it for offline analysis or replication.

## BKT and knowledge state

- **GET /api/ta/{ta_id}/bkt** returns the current BKT state: decayed `p_know` per knowledge unit. Use this for learning curve or knowledge-over-time analysis.
- Knowledge state is updated after each teaching event (with prerequisite checks) and after each test attempt (BKT update). State is persisted in `ta_instances.knowledge_state` (JSON).

## Problem selection strategy

The task engine supports configurable strategies: `coverage`, `difficulty`, `spaced`, `misconception`, `round_robin`. The default is `coverage`. To change strategy for experiments, configure the backend call to `select_problem(..., strategy="...")` in the testing/orchestration layer.

## Domains

- **Python**: code execution, test-case comparison, AST guard.
- **Database**: SQL execution against a seed schema, result-set comparison, partial correctness.
- **AI Literacy**: concept questions, LLM rubric evaluation.

Each domain has its own seed data under `seed/python`, `seed/database`, `seed/ai_literacy` (or legacy paths). TA creation allows choosing the domain (Python / Database / AI Literacy).

## Running tests

```bash
# Backend unit and integration tests
pytest tests/ -v

# BKT and knowledge state tests
pytest tests/test_knowledge_state.py -v
```

## Citation and paper alignment

The system is designed to support:

1. **Cross-domain TA framework** (Python + Database + AI Literacy, shared core).
2. **Misconception lifecycle** (activation, propagation, auto-detection, correction, relearning).
3. **Learning analytics** (BKT, adaptive problem selection, trace, teacher dashboard).

For detailed architecture and migration notes, see `SHARED_CORE_ARCHITECTURE.md` and `TRACE_AND_HISTORY_LAYER.md`.
