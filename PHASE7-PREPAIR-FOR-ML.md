Perfect, Phase 6 is solid. You now have a fully integrated engine that can run end-to-end historical simulations using the normalized NBA data. Everything is wired up, adapter layers are working, and your integration tests confirm the engine is ready to operate on real data.

Here’s a Phase 7 prep doc for your agent to get ready for ML modeling and visualization. It will guide the next stage: implementing replay logic, generating features, and preparing datasets for predictive modeling.


---

# Phase 7 — Machine Learning & Visualization Prep

## Objective
Phase 7 focuses on transforming the engine's historical simulation outputs into **structured datasets** suitable for machine learning, analytics, and visualization. This phase will:
- Build out the `run_historical_replay` method in the `Simulation` class.
- Aggregate player, team, and game statistics from historical data.
- Prepare feature sets and labels for predictive modeling.
- Generate visualizations to explore trends and validate simulation outputs.

---

## Step 1 — Historical Replay Logic

Enhance `Simulation.run_historical_replay()` to:

1. Iterate over historical games in chronological order.
2. Populate each game with corresponding `Player` and `Team` objects from adapters.
3. Track simulation state (score, player stats, substitutions, possessions).
4. Record output metrics per game:
   - `win_probability` for home and away teams
   - `expected_margin`
   - Player performance deviations
5. Store results in a structured DataFrame:
```python
columns = [
    'game_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score',
    'win_probability_home', 'win_probability_away', 'expected_margin',
    'player_stats_snapshot', 'team_stats_snapshot'
]


---

Step 2 — Feature Engineering for ML

Prepare the data for predictive modeling:

Player-level features:

Minutes, points, rebounds, assists, steals, blocks, turnovers

Shooting percentages: FG%, 3P%, FT%

Plus-minus per game


Team-level features:

Cumulative stats: wins, losses, points scored/conceded

Efficiency metrics: offensive/defensive rating, turnovers, rebounds


Game-level features:

Home/away indicator

Matchup history (head-to-head results)

Recent form (last N games)


Target variable:

Game outcome (win / loss) or point differential




---

Step 3 — Dataset Output

Write a method in Simulation to export replay data as CSV or parquet files for ML:


simulation_results.to_csv('logs/historical_simulation.csv', index=False)

Keep a separate dataset for engine validation, containing all raw metrics for debugging.



---

Step 4 — Visualization Pipeline

Create basic visualizations for exploration:

Time-series plots of team performance across the season.

Player performance heatmaps (points, rebounds, assists).

Distribution of predicted vs actual outcomes.

Correlation matrices to analyze feature importance.


Tools:

matplotlib, seaborn for static visualizations.

Optional: plotly or dash for interactive dashboards.



---

Step 5 — Test Suite

Add tests in tests/test_simulation_replay.py:

def test_replay_output_structure():
    sim = Simulation(players, teams, games)
    results = sim.run_historical_replay()
    assert 'game_id' in results.columns
    assert 'win_probability_home' in results.columns
    assert len(results) > 0


---

Step 6 — Phase 7 Completion Criteria

[ ] run_historical_replay method fully implemented.

[ ] Structured dataset generated for all historical games.

[ ] Player, team, and game features correctly computed.

[ ] ML-ready dataset exported to CSV/parquet.

[ ] Basic visualizations generated for exploratory analysis.

[ ] Tests confirm output structure and completeness.



---

Step 7 — Next Steps

Once Phase 7 is complete:

1. Use the ML-ready dataset to build predictive models (Phase 8):

Win probability prediction

Player impact estimation

Margin forecasting



2. Integrate visualizations with the engine dashboard.


3. Iterate on feature engineering based on ML insights.



---

This doc sets up your agent to:

- Expand the historical replay simulation logic.
- Aggregate and engineer features from Phase 6 outputs.
- Prepare ML-ready datasets.
- Generate visualizations for analysis and validation.

The system is now fully ready to transition from historical replay into predictive modeling.  

I can also draft a **helper script your agent can run to automatically produce the ML-ready dataset from all replayed games**, which will save a lot of repetitive work. Do you want me to do that next?