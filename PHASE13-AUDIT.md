You don’t need to apologize. What you’re feeling is a totally rational response to cognitive overload plus a misbehaving agent. You paused, recalibrated, and regained control — that’s competence, not failure.

Below is a clean, strict instruction block you can give to a new or reset agent. This is written to prevent destructive behavior, force observability, and produce a single artifact you can review calmly with me afterward.


---

Agent Directive: Test Audit & Report Generation (Phase 11 Finalization)

Role

You are operating in AUDIT MODE.
Your job is to observe, run, and report — not to refactor, delete, infer, or “fix” anything.

You are not allowed to modify application code, engine code, tests, data, or configuration files.


---

Global Rules (Non-Negotiable)

❌ Do NOT delete or edit any files

❌ Do NOT create or modify data

❌ Do NOT refactor tests

❌ Do NOT assume schemas, intent, or architecture

❌ Do NOT create new scripts

❌ Do NOT “fix” failing tests

✅ Only run existing tests

✅ Only capture output

✅ Only summarize observed results


If an error occurs, record it exactly. Do not attempt recovery.


---

Step 1: Environment Confirmation

1. Activate the existing virtual environment:

source .venv/bin/activate


2. Verify test tooling is available:

pytest --version


3. If pytest is unavailable, STOP and record the error.




---

Step 2: Enumerate Test Suite

1. List all test files:

ls tests/


2. Record the list verbatim into the report.




---

Step 3: Run Tests Individually

For each test file in the tests/ directory:

1. Run the test in isolation:

pytest tests/<test_file>.py -v


2. Capture:

Test name(s)

PASS / FAIL status

Full stdout/stderr

Tracebacks (if any)



3. Do not rerun failing tests.


4. Do not change flags, seeds, or configuration.




---

Step 4: Generate Markdown Report

Create a single file:

test_audit_phase11.md

Required Structure:

# Phase 11 – Test Audit Report

## Environment
- Python version:
- Pytest version:
- Virtualenv active: Yes/No

## Test Inventory
- test_*.py
- ...

## Test Results

### ✅ Passed Tests
- test_x.py::test_name
- ...

### ❌ Failed Tests

#### test_y.py::test_name
**Error Type:**  
**Traceback:**  
```text
(full traceback here)

Observed Behavior:
(What happened, no interpretation)


---

Summary

Total tests run:

Passed:

Failed:

Deterministic failures observed: Yes/No

Engine import failures: Yes/No

API startup blockers: Yes/No


Notes

(No opinions. No fixes. No guesses.)

---

### **Step 5: Stop**
Once the Markdown report is complete:
- Do not proceed further
- Do not suggest fixes
- Do not enter Phase 12
- Do not touch the engine or API

Your task ends when `test_audit_phase11.md` is written.

---

## **What Happens Next (for you, not the agent)**

Once you show me that `.md` file:
- I will **diagnose the failures structurally**
- We will decide what is *actually broken* vs *miswired*
- Then we will write **Phase 12 as a clean, forward-only document**
- No more thrashing, no more guessing

You’re not behind. You’re doing the right thing now: forcing observability before action.  
That’s how real engines get built.