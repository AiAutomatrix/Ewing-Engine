# Assumptions

This document outlines the core assumptions that drive the `ewing-engine` simulation model. Making these assumptions explicit is a core requirement of Phase 3, as it allows for systematic calibration and sensitivity analysis.

## Assumption Registry

The `engine.assumptions.AssumptionRegistry` dataclass is the central location for all model assumptions. Each assumption is an instance of the `Assumption` class, containing a `name`, `value`, and `description`.

### Key Assumptions

- **Possession Length Distribution**: The probability distribution of the time it takes for a team to complete a single possession. This is a critical factor in determining the total number of possessions in a game.

- **Turnover Rate**: The base probability that a possession will end in a turnover. This can be adjusted to model teams with different levels of ball security.

- **Shot Selection Distribution**: The distribution of shot types (e.g., 2-pointers, 3-pointers) that a team takes. This is a key driver of offensive efficiency.

- **Free Throw Rate**: The probability that a foul will result in free throws.

### Failure Modes

The model's accuracy is highly dependent on the quality of these assumptions. If the assumptions do not accurately reflect the real world, the model's predictions will be inaccurate. For example:

- If the `turnover_rate` is too low, the model will overestimate offensive efficiency.
- If the `possession_length_distribution` is skewed too far towards longer possessions, the model will underestimate the total number of possessions in a game, leading to lower scores.
