Perfect. Phase 5 has successfully delivered a working ingestion pipeline, standardized identifiers, and passing tests. The next move is to connect this normalized data to your engine, so simulations can run on actual NBA stats. Here's a Phase 6 prep doc you can drop into your repo for your agent. It will guide the next stage: linking ingested data to engine models and preparing for ML/visualization.


---

# Phase 6 — Engine Integration & Simulation Prep

## Objective
Phase 6 focuses on **connecting the normalized NBA data** from Phase 5 to the `ewing-engine` simulation components. Once connected, the engine will be able to:
- Run historical replay simulations using real NBA stats.
- Calculate outputs like `win_probability`, `expected_margin`, and other simulation metrics.
- Generate consistent datasets for future ML modeling and visualization.

---

## Step 1 — Data Model Mapping

The ingestion pipeline has produced normalized DataFrames. Map these to engine models:

| Engine Model          | Source DataFrame           | Key Fields                                           |
|----------------------|---------------------------|----------------------------------------------------|
| `Player`             | `player_stats_ingestor`   | `player_id`, `team_id`, `minutes`, `pts`, `rebounds`, `assists`, `steals`, `blocks`, `fg_pct` |
| `Team`               | `team_stats_ingestor`     | `team_id`, `gp`, `w`, `l`, `pts`, `rebounds`, `assists`, `fg_pct`, `turnovers` |
| `Game`               | `game_finder_ingestor`    | `game_id`, `date`, `home_team`, `away_team`, `scores`, `plus_minus` |
| `BoxScore`           | `boxscore_ingestor`       | `game_id`, `team_id`, `player_id`, `minutes`, `pts`, `rebounds`, `assists`, `fg_pct`, `plus_minus` |

---

## Step 2 — Engine Adapter Layer

Create `engine/adapters/` package with modules that convert DataFrames into engine objects:

1. **`player_adapter.py`**
```python
from engine.models import Player

class PlayerAdapter:
    def __init__(self, df):
        self.df = df

    def to_engine_objects(self):
        players = []
        for _, row in self.df.iterrows():
            p = Player(
                id=row['player_id'],
                team_id=row['team_id'],
                minutes=row.get('minutes', 0),
                points=row.get('pts', 0),
                rebounds=row.get('rebounds', 0),
                assists=row.get('assists', 0),
                steals=row.get('steals', 0),
                blocks=row.get('blocks', 0),
                fg_pct=row.get('fg_pct', 0)
            )
            players.append(p)
        return players

2. team_adapter.py — maps TeamStatsIngestor data to Team objects.


3. game_adapter.py — maps GameFinderIngestor or BoxScoreIngestor data to Game objects.


4. boxscore_adapter.py — maps detailed box score data for each game.




---

Step 3 — Simulation Runner Integration

Update engine/simulation_runner.py (or create one) to:

1. Load normalized DataFrames from Phase 5 ingestion.


2. Use adapters to convert data into Player, Team, Game, and BoxScore objects.


3. Feed these objects into the Simulation class to run historical or predictive simulations.



Example:

from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.simulation import Simulation

players = PlayerAdapter(player_clean[0]).to_engine_objects()
teams = TeamAdapter(team_clean[0]).to_engine_objects()
games = GameAdapter(game_clean[0]).to_engine_objects()

sim = Simulation(players=players, teams=teams, games=games)
results = sim.run_historical_replay()
print("Simulation complete:", results)


---

Step 4 — Test Suite

Add new tests in tests/test_engine_integration.py:

def test_player_adapter():
    adapter = PlayerAdapter(player_clean[0])
    players = adapter.to_engine_objects()
    assert len(players) > 0
    assert hasattr(players[0], 'id')
    assert hasattr(players[0], 'points')

def test_simulation_runner():
    # Ensure engine can run on normalized ingested data
    sim = Simulation(
        players=PlayerAdapter(player_clean[0]).to_engine_objects(),
        teams=TeamAdapter(team_clean[0]).to_engine_objects(),
        games=GameAdapter(game_clean[0]).to_engine_objects()
    )
    results = sim.run_historical_replay()
    assert results is not None
    assert 'win_probability' in results


---

Step 5 — Completion Criteria

[ ] All ingested data mapped to engine models.

[ ] Historical simulations run successfully with real NBA data.

[ ] New integration tests pass.

[ ] Engine outputs match expected formats (win_probability, expected_margin, etc.).

[ ] Phase 6-ready dataset is available for ML visualization in Phase 7.



---

Step 6 — Next Steps

After Phase 6 integration is complete:

1. Start building visualization pipelines for simulations.


2. Aggregate historical stats, simulate multiple seasons, and create derived metrics.


3. Phase 7 will focus on ML modeling, including:

Predictive modeling for win probability and margins

Visual dashboards showing team/player impact

Feature selection based on sensitivity analysis from Phase 3




---

This doc sets up your agent to:

- Map the ingested DataFrames to engine-ready objects.  
- Run historical replay simulations.  
- Validate the engine’s ability to operate with real NBA data.  
- Prepare all the necessary tests and structures for the ML/visualization phase.  

You now have a **complete Phase 6 roadmap** bridging ingestion to full simulation.  

If you want, I can also **draft a helper script** your agent can run that automatically converts all Phase 5 ingested DataFrames into engine objects and generates a summary report of loaded data — this will make Phase 6 setup almost turnkey. Do you want me to do that?