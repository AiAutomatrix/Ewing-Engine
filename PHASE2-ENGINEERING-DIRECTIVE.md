Here’s a clean Markdown document you can drop straight into your repo and hand to your agent.
It’s written as an internal engineering directive, not a chatty explanation.


---

# Phase 2 Engineering Directive — Ewing-Engine

**Status:** Phase 1 complete  
**Audience:** Autonomous Engineering Agent  
**Goal:** Expand the engine from a functional prototype into an inspectable, configurable, and extensible simulation system while preserving determinism and API stability.

---

## 1. Current Assessment

The `ewing-engine` project is in a strong state.

- Core simulation logic is implemented and deterministic
- API boundaries are clean and stable
- Engine logic is properly separated from Flask
- Tests pass and enforce correctness
- Project structure supports future expansion

This phase is **not** about fixing bugs or changing behavior.  
It is about **deepening the architecture** so future intelligence upgrades (data-driven or ML-based) can be added safely and transparently.

---

## 2. Global Rules (Must Follow)

1. **Do not break existing tests**
2. **Preserve deterministic behavior** when `random_seed` is supplied
3. **Every new feature must live in its own file**
4. **All new logic must be unit-testable without Flask**
5. **Do not change the public API contract**
6. **Do not add ML or training logic in this phase**

---

## 3. Phase 2 Objectives

### Objective Summary
Add:
- Centralized configuration
- Simulation diagnostics & metrics
- Optional introspection via game logs
- A future-proof model interface
- Supporting tests and documentation

Without:
- Increasing API complexity
- Reducing performance by default
- Introducing speculative intelligence layers

---

## 4. Required Engineering Tasks

### 4.1 Add a Simulation Configuration Layer

**Create file:**

engine/config.py

**Purpose:**
Centralize all simulation constants and tunable parameters.

**Requirements:**
- Use a `SimulationConfig` dataclass
- Include (at minimum):
  - Possessions per game assumptions
  - Pace modifiers
  - Score variance controls
  - Home-court advantage factor
  - Default Monte Carlo run count
- Provide safe defaults
- Allow overrides internally (not via API yet)

---

### 4.2 Add Metrics & Diagnostics Module

**Create file:**

engine/metrics.py

**Purpose:**
Analyze simulation behavior, not just final outcomes.

**Must compute:**
- Average possessions per game
- Score variance per team
- Win margin distribution
- Optional skew/kurtosis when score distributions are enabled

**Design Notes:**
- Accept raw simulation outputs
- Return structured, serializable metrics objects
- No Flask imports
- Deterministic given deterministic inputs

---

### 4.3 Add Optional Game Log Abstraction

**Create file:**

engine/game_log.py

**Purpose:**
Enable possession-by-possession inspection for debugging and research.

**Requirements:**
- Represent a single simulated game as a sequence of possessions
- Each possession records:
  - Team
  - Outcome type
  - Points scored
- Must be disabled by default for performance
- Controlled internally by a debug flag
- Must not affect default API responses

---

### 4.4 Refine the Model Interface

**Update (do not break):**

engine/models.py

**Add:**
- An abstract base class or protocol for simulation models
- Explicit method contracts (e.g. `simulate_possession(team_state)`)

**Goal:**
Make it obvious how alternative models (heuristic, statistical, ML-based) can be swapped in without modifying simulation flow.

---

### 4.5 Add Unit Tests for New Modules

**Create files:**

tests/test_config.py tests/test_metrics.py

**Tests must:**
- Validate deterministic output
- Confirm default config values load correctly
- Avoid Flask and API usage
- Be fast and isolated

---

### 4.6 Add Engine Architecture Documentation

**Create file:**

ENGINE_ARCHITECTURE.md

**Must explain:**
- Data flow: API → Engine → Model → Metrics
- Responsibility of each engine submodule
- How to safely add a new model
- Why determinism is enforced and where randomness is controlled

This is an internal engineering document, not marketing copy.

---

## 5. Explicit Non-Goals (Do Not Do)

- Do not introduce machine learning models
- Do not connect to live data sources
- Do not expand the API surface
- Do not optimize prematurely
- Do not add visualization or UI logic

---

## 6. Success Criteria

Phase 2 is complete when:
- All new files exist and are populated
- All tests (old and new) pass
- The engine exposes configuration, metrics, and introspection hooks
- The architecture clearly supports future intelligence upgrades

---

**End of Phase 2 Directive**


---

This document is strong enough to:

Guide an autonomous agent

Prevent architectural drift

Lock in your design philosophy

Scale without rewriting foundations


Once your agent completes this phase, the next natural step will be model realism vs calibration, not “more code for the sake of code.”