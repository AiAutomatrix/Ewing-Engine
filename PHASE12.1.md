Excellent. Then we proceed like engineers, not gamblers.

Below is a Phase 12.1 implementation plan written the way a serious agent should receive it: concrete, ordered, test-driven, and impossible to “hand-wave” past. This phase is deliberately unglamorous. That’s how you know it’s the right next step.


---

🔵 Phase 12.1 — Calibration Sanity Layer

Objective:
Prove the simulator can be systematically pulled toward reality by adjusting assumptions, without breaking determinism or stochastic validity.

This is not ML yet. This is measurement + control.


---

Core Principle (Do Not Violate)

> The simulation engine is a forward model.
Calibration modifies inputs, never internal mechanics.



If the simulator changes, Phase 11 is invalidated. We do not do that.


---

12.1.1 — Define Calibration Parameters (Minimal Set)

Create a new structure, conceptually:

CalibrationParams

global_score_multiplier (float, default = 1.0)

home_offense_scalar (float, default = 1.0)

home_defense_scalar (float, default = 1.0)

away_offense_scalar (float, default = 1.0)

away_defense_scalar (float, default = 1.0)


Rules:

Scalars multiply existing ratings

No per-player parameters yet

No team-specific params yet


This keeps the surface area tiny and debuggable.


---

12.1.2 — Injection Point (Critical Design Step)

Add one and only one place where calibration touches the engine.

Required behavior:

CalibrationParams are applied:

immediately before simulation

via SimulationConfig or a wrapper


They must NOT:

mutate stored data

alter historical stats

leak between simulations



Test requirement:
Two runs with same seed + same calibration → identical output.


---

12.1.3 — Calibration Dataset Selection

Pick a fixed historical slice:

Example: first 200 regular season games

Exclude playoffs

Freeze this dataset permanently for Phase 12.1


This dataset is:

calibration data only

never used for validation later


Document the game IDs.


---

12.1.4 — Baseline Error Measurement (Before Calibration)

Write a test:

tests/test_calibration_baseline_error.py

For each game:

1. Run N simulations (N = 200–500)


2. Record:

predicted mean home score

predicted mean away score

win probability



3. Compare to actual outcome



Compute:

MAE (home score)

MAE (away score)

Brier score (win probability)


Persist results to stdout or a CSV.

This is your “before” snapshot.


---

12.1.5 — Calibration Search (No ML)

Implement a brute-honest optimizer:

Options allowed:

Grid search

Coordinate descent

Random search (with fixed seed)


Forbidden:

Backprop

Gradient descent

Neural nets

Anything opaque


Target:

Minimize weighted sum of:

score MAE

Brier score



Keep iteration count small and observable.


---

12.1.6 — Post-Calibration Evaluation

Re-run the same test with best parameters.

Assertions:

MAE decreases vs baseline

Brier score improves

Std dev remains > 0

Determinism still holds


If MAE improves but variance collapses → FAIL
If win rate converges to 0% or 100% → FAIL


---

12.1.7 — Phase 12.1 Exit Criteria

Phase 12.1 passes only if all are true:

Calibration parameters reduce error

Simulation remains stochastic

Determinism invariant still holds

No engine internals were modified

Calibration logic is isolated and removable


When this passes, the simulator becomes a predictive instrument, not just a generator.


---

What This Enables Next (Phase 12.2+)

Once this works:

Predictions are now anchored

Confidence intervals mean something

ML can safely model residuals, not chaos

Monte Carlo outputs become tradable, bettable, evaluatable



---

One Final Framing (Important)

You are no longer “building a sports sim.”

You are building:

> a controlled stochastic belief engine



That’s why Phase 12.1 matters more than any neural net.

When you finish implementing this:

Show me the baseline error output

Show me calibrated error output

Show me the exact parameters found


Then we move to Phase 12.2: Prediction Output Contract, and the engine starts speaking in probabilities instead of vibes.