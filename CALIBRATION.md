# Calibration

This document describes the calibration capabilities of the `ewing-engine`, a key deliverable of Phase 3.

## Sensitivity Analysis

The `engine.sensitivity.SensitivityAnalysis` class provides the tools to measure the impact of changes in the model's assumptions. This is a critical part of understanding the model's behavior and identifying the most important assumptions to calibrate.

The `run_one_at_a_time` method allows for a systematic analysis of a single assumption. It works by perturbing the assumption by a series of given percentages, running a simulation with each perturbed value, and measuring the change in the model's outputs.

### Key Metrics

The sensitivity analysis engine measures the delta in the following key metrics:

- **Win Probability**: The change in the home team's win probability.
- **Expected Margin**: The change in the expected point margin between the home and away teams.

By analyzing these deltas, we can understand how sensitive the model's predictions are to changes in each assumption.

### Failure Modes

The calibration process can fail in a few ways:

- **Overfitting**: It is possible to over-calibrate the model to a specific set of historical data, resulting in a model that performs well on that data but poorly on new data.
- **Interactions**: The `run_one_at_a_time` method only analyzes the impact of changing one assumption at a time. It does not account for the interactions between assumptions, which can be significant.
