Below is a single authoritative Phase 3 document you can drop into your repo.
It includes agent instructions, explicit guardrails, file-level expectations, and completion criteria.

This is written so your IDE agent can execute Phase 3 without interpretation drift.


---

PHASE_3_CALIBRATION_VALIDATION_AGENT.md

Phase 3: Calibration, Assumption Control, and Historical Validation

(Ewing-Style System Completion Phase)


---

1. Phase Purpose (Read First)

Phase 3 converts ewing-engine from a simulation engine into a diagnostic calibration system.

This phase exists to answer one question:

> Where does the model systematically differ from reality, and why?



This phase must not attempt to improve predictions.
It must measure model behavior, expose fragility, and document failure modes.

This mirrors the original Ewing system philosophy:

simulations first

distributions over point estimates

edges discovered through miscalibration, not optimization



---

2. Absolute Constraints (Hard Rules)

The agent must NOT:

add machine learning models

fit parameters to outcomes

scrape sportsbook odds

introduce player-level data

add live data ingestion

optimize performance over clarity


Violating any constraint invalidates Phase 3.


---

3. Phase 3 Deliverables (Required)

By completion, the repository must include:

1. A centralized assumption registry


2. A sensitivity analysis engine


3. A scenario/stress testing framework


4. A historical replay engine


5. Outcome comparison metrics


6. Full test coverage for all new components


7. Updated documentation reflecting system behavior




---

4. Required Architectural Additions

4.1 Assumption Registry

Purpose:
Expose all modeling assumptions as explicit, adjustable parameters.

Implementation Requirements

Create a dedicated module (e.g. engine/assumptions.py)

Every assumption must:

have a name

have a default value

be documented


Defaults must reproduce Phase 2 results exactly

Assumptions must be injectable into simulations

Changing assumptions must preserve determinism under fixed seeds


Examples (Not Exhaustive)

possession_length_distribution

turnover_rate

shot_type_mix

free_throw_rate

offensive_rebound_rate

pace_modifier

home_court_advantage



---

4.2 Sensitivity Analysis Engine

Purpose:
Measure how simulation outputs respond to assumption changes.

Capabilities

One-at-a-time perturbation (±X%)

Multi-parameter perturbation

Comparison of full distributions, not just means


Outputs

Δ win probability

Δ expected margin

Δ variance

Δ skewness

Δ kurtosis


File Expectations

New module (e.g. engine/sensitivity.py)

Clean interfaces usable by API or scripts

Deterministic outputs



---

4.3 Scenario & Stress Testing Framework

Purpose:
Expose tail behavior and instability under extreme but plausible conditions.

Examples

High-pace environments

Turnover-heavy games

High-variance shooting nights

Fat-tail stress scenarios


Requirements

Scenarios must be named and reproducible

Scenarios must override assumptions via the registry

Outputs must include distribution comparisons



---

4.4 Historical Replay Engine

Purpose:
Replay past games using only pre-game information, then compare simulations to actual results.

Implementation Requirements

Create a historical interface (e.g. engine/historical.py)

Accept historical game inputs:

teams

date

known pre-game parameters


Run Monte Carlo simulations

Store:

actual final score

simulated distribution

actual outcome percentile


No post-game data leakage


This engine exists to measure calibration, not accuracy.


---

4.5 Outcome Comparison Metrics

Purpose:
Evaluate whether reality behaves as the model expects.

Required Metrics

Actual outcome percentile

Confidence interval coverage

Bias in spread

Bias in totals

Tail miss frequency


Metrics must focus on distribution correctness, not win/loss accuracy.


---

4.6 Model Disagreement Framework (Heuristic Only)

Purpose:
Expose structural uncertainty via competing models.

Requirements

Support multiple heuristic models simultaneously

No learning or parameter fitting

Output disagreement metrics


Disagreement is a diagnostic signal.


---

5. API Layer Expectations (Optional but Encouraged)

If API endpoints are added, they must:

remain deterministic

expose raw distributions

be auditable


Suggested endpoints:

/sensitivity/run

/scenario/run

/historical/replay

/calibration/report



---

6. Testing Requirements

The agent must add tests validating:

deterministic behavior

assumption injection correctness

sensitivity engine consistency

scenario reproducibility

historical replay integrity

metric correctness


Tests should fail on model instability, not just syntax errors.


---

7. Documentation Updates

The agent must update or add:

ASSUMPTIONS.md

CALIBRATION.md

HISTORICAL_REPLAY.md


Documentation must describe:

what the model assumes

where it breaks

what failure looks like



---

8. Completion Criteria

Phase 3 is complete only when:

all assumptions are explicit

historical outcomes can be replayed

calibration behavior is measurable

failure modes are documented

all tests pass


At this point, the system is ready for Phase 4 data ingestion.


---

9. Phase Boundary

Phase 4 will handle:

data acquisition (API or datasets)

ingestion pipelines

dataset normalization


Phase 5 will introduce:

machine learning

visualization

exploratory analysis


Phase 3 must not anticipate or include Phase 4 or Phase 5 behavior.


---

End of Phase 3 Agent Specification


---

This document gives you something rare: a system that knows how wrong it is.

That’s the exact moment where ML becomes useful instead of dangerous.