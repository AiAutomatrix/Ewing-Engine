Alright. Deep breath. Phase 11 did its job. Now we move like engineers, not firefighters.

Below is a clean, implementation-ready PHASE 12 document you can drop directly into your repo (e.g. PHASE_12_CALIBRATION.md). It is written explicitly for an autonomous agent to follow without breaking existing behavior.


---

PHASE 12 — Calibration & Reality Alignment Layer

Phase Objective (Read This First)

Phase 12 introduces calibration, not prediction upgrades.

The goal is not to make the simulator “right.” The goal is to make it less wrong in measurable ways while preserving stochastic behavior.

At the end of Phase 12, the Ewing Engine must be able to:

Compare simulated distributions to historical outcomes

Measure divergence quantitatively

Adjust simulation parameters incrementally

Preserve randomness and variance at all times


If variance collapses, Phase 12 has failed.


---

Non-Negotiable Constraints

These rules override all other instructions.

1. DO NOT change the simulation engine’s core logic

No rewriting score generation

No removing randomness

No deterministic shortcuts



2. DO NOT modify API contracts

/simulate response shape must remain compatible

New fields may be additive only



3. Calibration must be external

Calibration wraps the simulator

The simulator remains ignorant of calibration



4. One change at a time

No multi-parameter tuning in a single step

Each calibration variable must be independently measurable





---

Architectural Principle

> Simulation produces reality candidates.
Calibration judges how close they are.



This means:

The simulator generates outcomes

The calibration layer evaluates outcomes

Feedback flows into parameters, not logic



---

New Components to Introduce

1. Calibration Module (NEW)

Create a new module, suggested path:

engine/calibration/
├── __init__.py
├── calibrator.py
├── metrics.py
├── targets.py

Do not place calibration code inside:

simulation.py

simulation_runner.py

API routes



---

2. Calibration Targets

Define what “realistic” means.

Examples (do not hard-code values yet):

Average total points per game

Margin distribution shape

Home win rate

Score variance ranges


Store targets in a data-only structure, not logic.

Example concept:

CalibrationTarget(
    name="average_total_points",
    historical_value=XXX,
    tolerance=YYY
)

No optimization yet. Just definition.


---

3. Metrics Layer (NEW)

Implement functions that compare:

Simulated distributions

Historical distributions


Metrics must include:

Mean error

Variance ratio

Distribution distance (simple, e.g. bucketed delta)


Avoid complex math (KL-divergence can come later).


---

Calibration Workflow (Step-by-Step)

Step 1 — Baseline Snapshot

Run the simulator without calibration:

Fixed matchups

Fixed number of simulations

Record outputs


Save results to disk:

calibration/baselines/

These baselines are sacred. Never overwrite.


---

Step 2 — Single-Parameter Calibration

Introduce one adjustable parameter at a time, for example:

Global scoring multiplier

Pace scalar

Noise scale


Rules:

Parameter must be injected, not hard-coded

Defaults must preserve current behavior



---

Step 3 — Measure Before Adjusting

For each parameter:

1. Run simulation


2. Compute metrics vs targets


3. Record divergence



No adjustment yet. Observation only.


---

Step 4 — Incremental Adjustment

Apply small bounded changes:

Linear nudges

No jumps

No loops that auto-converge


Every adjustment must:

Be logged

Be reversible

Show before/after metrics



---

Step 5 — Stability Check

After calibration:

Run multiple seeds

Ensure variance still exists

Confirm distributions did not collapse


If outputs become too tight, rollback.


---

Required Outputs (Artifacts)

Phase 12 must produce:

calibration/
├── reports/
│   ├── baseline.md
│   ├── calibration_step_1.md
│   ├── calibration_step_2.md
│   └── summary.md

Each report must include:

Parameter values

Metrics before

Metrics after

Observed side effects



---

API Impact (Minimal & Safe)

Optional additions to /simulate response:

calibration_version

calibration_params_used


Do not:

Change existing fields

Remove randomness

Add calibration logic to API routes



---

Success Criteria

Phase 12 is complete when:

Calibration exists as a separate layer

Metrics can quantify realism gaps

At least one parameter can be tuned safely

Simulator still behaves stochastically

No existing tests or endpoints break



---

Explicit Anti-Goals (Do NOT Do These)

Do not optimize for betting accuracy yet

Do not fit historical games perfectly

Do not remove randomness to “improve” results

Do not introduce ML models in this phase


Those belong later.


---

Mental Model for the Agent

Think like this:

> “I am adjusting the climate, not controlling the weather.”



The simulator remains wild. Calibration just nudges the ecosystem.


---

Phase Boundary

Phase 12 ends when calibration exists and is measurable.
Phase 13 begins only after this layer is stable.


---

END OF PHASE 12 DOCUMENT

When you’re ready after this, Phase 13 becomes genuinely interesting: validation, scoring, and confronting the model with reality without flinching.