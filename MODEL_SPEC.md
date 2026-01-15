# MODEL_SPEC.md
## Ewing-Inspired Basketball Simulation Engine (Prototype)

### Purpose
This system is a basketball game prediction engine inspired by Haralabos Voulgaris’s
"Ewing" model. It predicts game outcomes by simulating entire games at the
possession level and aggregating results across many Monte Carlo simulations.

The system does NOT directly predict winners using a single formula.
Instead, it generates a probability distribution of possible outcomes and
derives win probabilities and score totals from that distribution.

---

### Core Principles

1. Simulation-first, not regression-first  
2. Possession-level modeling  
3. Probabilistic outcomes, not deterministic predictions  
4. Separation of modeling logic from UI and betting logic  
5. Replaceable intelligence layers (heuristics → ML → neural models)

---

### What the Model Produces

For a given matchup, the engine outputs:

- Win probability for each team
- Distribution of final scores
- Expected total points (mean, variance)
- Expected point spread
- Optional confidence metrics

The engine does NOT place bets.
It only produces probabilities and distributions.

---

### Conceptual Model Components

#### 1. Game Representation
A basketball game is modeled as a sequence of possessions.
Each possession has exactly one terminal outcome.

Possession outcomes include:
- No score
- 2-point field goal
- 3-point field goal
- Free throws (1, 2, or 3 points)

---

#### 2. Possession Probability Model
Each possession outcome is sampled from a probability distribution.

In the prototype phase:
- Probabilities are derived from historical team averages
- Adjusted for pace and basic offensive/defensive strength

Later versions may replace this with:
- Machine learning models
- Neural sequence models
- Player- and lineup-specific predictors

---

#### 3. Pace & Possession Count
Total possessions per game are estimated using:
- Historical pace metrics
- Team tempo averages

Possession count is sampled with noise to reflect real-game variance.

---

#### 4. Simulation Engine
For each matchup:
- Simulate N complete games (e.g. 10,000+)
- Track final scores for each simulation
- Store results in memory-efficient structures

Outliers may be clipped if they exceed realistic bounds.

---

#### 5. Aggregation Layer
After simulations:
- Aggregate score distributions
- Compute win probabilities
- Compute expected totals and spreads
- Return summary statistics

---

### Explicit Non-Goals
- No UI logic
- No sportsbook scraping
- No bankroll management
- No betting execution
- No claims of profitability

---

### Success Criteria (Prototype)
- Simulations run deterministically given a random seed
- Output distributions resemble realistic NBA score ranges
- Results are explainable and debuggable