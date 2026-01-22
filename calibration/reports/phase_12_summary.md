
# Phase 12 Calibration Summary

This document summarizes the key findings from the simulation calibration efforts conducted in Phase 12.

## 1. HeuristicModel Calibration Limits

The `HeuristicModel` has undergone extensive calibration. While parameters like `global_score_multiplier` have been effective in controlling `average_total_points`, other metrics have proven difficult to influence.

## 2. Empirical Variance Ceiling

The most significant finding is the confirmation of an empirical variance ceiling in the `HeuristicModel`. The model, due to its deterministic `scale_factor` logic in the `get_possession_outcome` method, cannot produce a `margin_of_victory_stddev` that meets the target value of `12.5`.

Our most recent test, using extreme parameters, yielded a `margin_of_victory_stddev` of `5.9739`, confirming that the model's core logic is the limiting factor.

## 3. Confirmed Non-Effect of Pace Variance

We have confirmed that manipulating the `pace_standard_deviation` parameter does not have a significant impact on the `margin_of_victory_stddev`. Increasing this parameter from `10.0` to `25.0` had a negligible effect, proving that the number of possessions is not the bottleneck for score variance.

## 4. Full Calibration Schema Restored

The `engine/calibration.py` file has been updated to include the full set of calibration parameters, including those related to home and away team scalars. This ensures that the model is fully configurable for future experiments.

## Next Steps: A Design Decision

As you stated, we are no longer debugging; we are designing. We have two clear paths forward:

1.  **API + Production Hardening:** Accept the limitations of the `HeuristicModel`, and focus on building a robust API and production-ready infrastructure around the existing simulation engine.
2.  **Model Family Expansion:** Proceed with the development of the `StochasticModel`, which uses a Poisson distribution to introduce more realistic variance into the simulation.

Please advise on which path you would like to pursue for Phase 13.
