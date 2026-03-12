"""
Stage One Teachable Agent — Teacher-facing Streamlit demo.
Wraps the current prototype; demonstrates zero-knowledge TA, constrained selection,
success/failure paths, and mastery reporting. Stub-only by default; optional LLM when enabled.
"""

import os
import sys
from pathlib import Path

# Ensure repo root and prototype are on path when run from repo root (local or Streamlit Cloud)
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "prototype") not in sys.path:
    sys.path.insert(0, str(ROOT / "prototype"))

import streamlit as st

KU_PATH = ROOT / "seed" / "knowledge-units-stage1.json"
PROBLEMS_PATH = ROOT / "seed" / "sample-problems-stage1.json"


def _ensure_seed():
    if not KU_PATH.exists() or not PROBLEMS_PATH.exists():
        st.error("Seed files not found. Ensure `seed/knowledge-units-stage1.json` and `seed/sample-problems-stage1.json` exist.")
        return False
    return True


def run_scenario_a():
    from demo_scenarios import run_scenario_a as _run_a
    return _run_a(KU_PATH, PROBLEMS_PATH)


def run_scenario_b():
    from demo_scenarios import run_scenario_b as _run_b
    return _run_b(KU_PATH, PROBLEMS_PATH)


def run_scenario_c():
    from demo_scenarios import run_scenario_c as _run_c
    return _run_c(KU_PATH, PROBLEMS_PATH)


# ----- Page config and session state -----
st.set_page_config(
    page_title="Stage One: Teachable Agent Demo",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "last_scenario" not in st.session_state:
    st.session_state.last_scenario = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "use_llm_code" not in st.session_state:
    st.session_state.use_llm_code = False

# Sync env with UI toggle (prototype reads USE_LLM_CODE)
if st.session_state.use_llm_code:
    os.environ["USE_LLM_CODE"] = "1"
else:
    os.environ.pop("USE_LLM_CODE", None)

# ----- 1. Overview / Landing -----
st.title("📘 Stage One: Teachable Agent for Introductory Python")
st.markdown("---")

st.header("What this is")
st.markdown("""
This is a **teacher-facing demo** of the **Stage One** prototype for a **Teachable Agent (TA)** in Computer Science.
The TA starts with **no programming knowledge** and learns only what a human student teaches it.
The student's learning happens by **teaching** the agent and reflecting when the agent fails a programming test.
""")

st.subheader("What the teacher asked for")
st.markdown("""
1. **A TA with zero programming knowledge** — so we have a clear, testable starting point.  
2. **A programming test** that **examines the TA's mastery level** — so we can measure what the TA has learned.  
3. **An interaction design** — explanation, conversation, and **curated programming problems** — so the TA learns Introductory Python from the student.
""")

st.subheader("What this demo shows")
st.markdown("""
- **Zero-knowledge TA:** All knowledge units start as *unknown*; only teaching events update state.  
- **Structured teaching:** We simulate teaching with a fixed topic and knowledge units (no free-text parser yet).  
- **Learner-style TA response:** After each teaching event, the TA replies like a novice (stub or optional LLM).  
- **Constrained problem selection:** Only problems whose required concepts are all learned can be selected.  
- **TA code attempt:** The TA writes code (stub or optional LLM) and the system runs it and grades it.  
- **Mastery report:** Pass/fail and a short mastery summary are shown so you can see what the TA “knows” and how it performed.
""")

st.markdown("---")

# ----- 2. Stage One capability summary -----
st.header("Stage One capability summary")
with st.expander("Show current capabilities", expanded=False):
    st.markdown("""
    | Capability | Status |
    |------------|--------|
    | Zero-knowledge TA | ✅ All units start *unknown*; only teaching updates state. |
    | Teaching event | ✅ Structured: topic + knowledge units + note. |
    | Learner response | ✅ One short reply per event (stub or optional LLM). |
    | Constrained problem selection | ✅ Only problems with all required KUs learned are eligible. |
    | TA code attempt | ✅ Stub always; optional LLM for Scenario B when enabled. |
    | Pass/fail evaluation | ✅ Code run against test cases; exact output match. |
    | Mastery report | ✅ Per-problem and overall level (e.g. proficient / failing). |
    | Optional LLM (conversation) | ✅ If `OPENAI_API_KEY` is set, TA reply can come from LLM. |
    | Optional LLM (code) | ✅ If enabled below, Scenario B can use LLM-generated code (with guard fallback). |
    | Fallback behavior | ✅ If API or guard fails, stub is used; demo always runs. |
    """)

st.markdown("---")

# ----- 3. Optional LLM toggle -----
st.header("Optional LLM code (Scenario B only)")
st.caption("Scenario C always uses stub code so the failure path stays reproducible.")
use_llm = st.checkbox(
    "Use optional LLM code generation for Scenario B (requires OPENAI_API_KEY)",
    value=st.session_state.use_llm_code,
    help="When enabled, Scenario B will try to generate TA code via LLM; if unavailable or rejected by guard, stub is used.",
)
st.session_state.use_llm_code = use_llm
if use_llm:
    os.environ["USE_LLM_CODE"] = "1"
else:
    os.environ.pop("USE_LLM_CODE", None)

st.markdown("---")

# ----- 4. Scenario runner -----
st.header("Run a scenario")
if not _ensure_seed():
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    run_a = st.button("▶ Run Scenario A — Minimal learned state", use_container_width=True)
with col2:
    run_b = st.button("▶ Run Scenario B — Success path", use_container_width=True)
with col3:
    run_c = st.button("▶ Run Scenario C — Failure path", use_container_width=True)

# Run selected scenario
result = None
scenario_id = None
if run_a:
    with st.spinner("Running Scenario A..."):
        result = run_scenario_a()
        scenario_id = "A"
if run_b:
    with st.spinner("Running Scenario B..."):
        result = run_scenario_b()
        scenario_id = "B"
if run_c:
    with st.spinner("Running Scenario C..."):
        result = run_scenario_c()
        scenario_id = "C"

if result is not None:
    st.session_state.last_result = result
    st.session_state.last_scenario = scenario_id

st.markdown("---")

# ----- 5. Scenario output panel -----
st.header("Scenario output")
if st.session_state.last_result is None:
    st.info("Run one of the scenarios above (A, B, or C) to see output here.")
else:
    data = st.session_state.last_result
    sid = data.get("scenario_id", "?")

    st.subheader(f"Scenario {sid}: {data.get('name', '')}")

    # What was taught
    event = data.get("teaching_event", {})
    st.markdown("**What was taught**")
    st.json(event)

    # Learned units
    learned = data.get("learned_units", [])
    st.markdown("**Current learned knowledge units**")
    st.code(", ".join(learned) if learned else "(none)", language=None)

    # TA learner response
    st.markdown("**TA learner-style response**")
    st.write(data.get("ta_learner_response", "—"))

    # Selected problem or no eligible
    sel = data.get("selected_problem")
    if sel:
        st.markdown("**Selected problem**")
        st.write(f"**ID:** {sel.get('problem_id', '')}")
        st.write(sel.get("problem_statement", ""))
    else:
        st.markdown("**Selected problem**")
        st.write("None (no eligible problem — required units not all learned).")
        elig = data.get("eligible_problem_ids", [])
        inel = data.get("ineligible_reasons", [])
        st.caption(f"Eligible IDs: {elig or '(none)'}.")
        if inel:
            for r in inel:
                st.caption(f"  • {r.get('problem_id', '')}: missing {r.get('missing_units', [])}")

    # Stub vs LLM path (infer for B)
    if sid == "B":
        path_used = "LLM (if enabled and available)" if st.session_state.use_llm_code else "Stub"
        st.markdown("**Code path used**")
        st.caption(path_used + " — Scenario C always uses stub.")

    # TA code
    ta_code = data.get("ta_code", "")
    if ta_code:
        st.markdown("**TA code**")
        st.code(ta_code, language="python")

    # Evaluation result
    pf = data.get("pass_fail")
    if pf is not None:
        st.markdown("**Evaluation result**")
        if pf is True:
            st.success("PASS")
        elif pf is False:
            st.error("FAIL")
        else:
            st.caption(str(pf))
        res = data.get("attempt_result", {})
        if res and res.get("details"):
            for i, d in enumerate(res["details"], 1):
                st.caption(f"Test {i}: {'pass' if d.get('passed') else 'fail'}")
    elif sid == "A":
        st.caption("No attempt run in Scenario A (focus on selection only).")

    # Mastery summary
    report = data.get("mastery_report", {})
    if report:
        st.markdown("**Mastery summary**")
        st.write(f"Pass/Fail: {report.get('pass_fail', 'N/A')}")
        st.write(report.get("overall_summary", ""))
        st.caption(report.get("per_problem_interpretation", ""))

    # Brief explanation
    st.markdown("**What this scenario demonstrates**")
    if sid == "A":
        st.info("Knowledge state controls selection: with only *print_function* learned, no problem in the bank has all required units learned, so no problem is selected. Ineligible reasons show which units each problem needs.")
    elif sid == "B":
        st.success("Success path: teach variable_assignment + print_function → select a matching problem → TA produces correct code → test passes → mastery reported as proficient.")
    elif sid == "C":
        st.warning("Failure path: same teaching as B, but TA code is forced wrong (simulated misconception) → test fails → mastery reflects failing. The student can see the TA's wrong code and reflect on what to re-teach.")

st.markdown("---")

# ----- 6. Current limitations -----
st.header("Current limitations")
with st.expander("Show limitations", expanded=True):
    st.markdown("""
    - **Stage One only** — Introductory Python scope (variables, types, I/O, operators, conditionals, loops, lists). No functions, classes, files, recursion, dictionaries, or external libraries as learning content.
    - **Research prototype** — Not a production product. Single run, no user accounts.
    - **Some components stubbed or partial:** Teaching is structured only (no natural-language teaching parser). TA code is stub by default; LLM code is optional and only in Scenario B.
    - **No persistence** — Each scenario starts from a fresh state; no history across runs.
    - **No natural-language teaching yet** — We use fixed teaching events (topic + list of knowledge units), not free-form student text.
    """)

st.markdown("---")

# ----- 7. Next-step recommendations -----
st.header("Recommended next steps")
st.markdown("""
1. **Persistence + aggregated mastery** — Save knowledge state and attempt history; compute mastery over multiple problems per unit (failing / developing / proficient) per the rubric.  
2. **Minimal teacher UI** — Keep this Streamlit demo and add small improvements (e.g. choose which problem to try, see multiple attempts).  
3. **Controlled natural-language teaching** — Pilot: accept free-form student text, map it to knowledge units via LLM, then apply updates so the TA “learns” from natural explanation.
""")

st.markdown("---")
st.caption("Stage One Teachable Agent — Demo for professor review. Stub mode works without API keys; optional LLM when OPENAI_API_KEY and toggle are set.")
