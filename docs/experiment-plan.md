# Phase G: Formal Experiment Plan (Paper 3)

This document outlines the process for running the controlled study (Paper 3: *Evaluating Learning-by-Teaching with Teachable Agents*). It is not implementation; it is a checklist for researchers.

## Prerequisites

- System stable and deployed (Phases A–D complete).
- Python domain (and optionally Database / AI Literacy) ready for the target curriculum.

## Steps

1. **IRB / Ethics approval**  
   Submit study protocol (informed consent, data handling, minimal risk) to your institution’s IRB. Obtain approval before recruiting.

2. **Recruit participants**  
   Target: 40–60 CS introductory students. Define inclusion/exclusion (e.g. no prior Python, same course). Plan compensation if applicable.

3. **Design**  
   - **Experimental group**: Use the CS Teachable Agent (teach TA, run tests, see mastery).  
   - **Control A**: Traditional practice (e.g. same problems on a non-TA platform).  
   - **Control B** (optional): LLM chat learning without knowledge-state constraint.  
   - Random assignment; pre-test and post-test (concept + application).

4. **Run study**  
   - Same duration and topic scope across conditions.  
   - Collect: pre/post scores, trace data (teaching events, attempts, mastery), questionnaires (SUS, self-efficacy, perceived learning).

5. **Analysis**  
   - Learning gain (post − pre) by condition (ANOVA or mixed model).  
   - Trace-derived metrics: teaching coverage, misconception correction rate, mastery growth.  
   - Qualitative: themes from open-ended feedback.

6. **Write-up**  
   Paper 3: method, results, discussion, limitations. Target venues: Computers & Education, AIED, LAK.

## Notes

- Trace schema and export format are defined in the core (Trace layer). Ensure export (e.g. JSON/CSV) is available for analysis.
- Mastery and misconception lifecycle events are already recorded; align analysis variables with these.
