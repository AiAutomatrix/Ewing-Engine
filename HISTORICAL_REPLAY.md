# Historical Replay

This document describes the historical replay feature of the `ewing-engine`, a key deliverable of Phase 3.

## HistoricalGame

The `engine.historical.HistoricalGame` class provides the ability to replay a historical game through the simulation. This is a critical tool for measuring the model's accuracy against real-world outcomes.

The `replay` method takes the home and away teams and the final score of a real game. It then runs a simulation with those teams and calculates the percentile of the actual outcome within the simulated distribution of outcomes.

### Key Metrics

The historical replay feature calculates the following key metrics:

- **Margin Percentile**: The percentile of the actual point margin within the simulated distribution of margins. A value of 0.5 indicates that the actual margin was the median of the simulated outcomes.
- **Total Points Percentile**: The percentile of the actual total points scored within the simulated distribution of total points. A value of 0.5 indicates that the actual total points was the median of the simulated outcomes.

By analyzing these percentiles, we can get a sense of how well the model's predictions align with reality.

### Failure Modes

The historical replay feature can fail in a few ways:

- **Data Quality**: The accuracy of the historical replay is dependent on the quality of the historical data. If the data is inaccurate, the replay will be as well.
- **Model Bias**: If the model is systematically biased, the historical replay will reflect that bias. For example, if the model consistently overestimates the number of points scored, the `total_points_percentile` will be consistently low.
