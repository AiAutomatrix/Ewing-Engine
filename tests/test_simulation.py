# tests/test_simulation.py

import random
import numpy as np
from engine.simulation import Simulation
from engine.models import HeuristicModel, Team
from engine.config import default_config
from engine.assumptions import AssumptionRegistry
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

def test_pace_impact_on_scores():
    """Tests that a higher pace modifier leads to higher scores."""
    random.seed(42)
    np.random.seed(42)
    
    teams_df = team_clean[0]
    teams = TeamAdapter(teams_df).to_engine_objects()
    simulation = Simulation(players=[], teams=teams, games=[], boxscores=[])
    league_avg_off_rating = np.mean([team.off_rating for team in teams])
    model = HeuristicModel(league_avg_off_rating=league_avg_off_rating)

    # Run simulation with default pace
    assumptions_default = AssumptionRegistry()
    config_default = default_config
    config_default.assumptions = assumptions_default
    results_default = [simulation.simulate_game(model, "GSW", "LAL", config=config_default) for _ in range(100)]
    avg_total_points_default = np.mean([r["total_points"] for r in results_default])

    # Run simulation with higher pace
    assumptions_high_pace = AssumptionRegistry()
    assumptions_high_pace.pace_modifier.value = 1.2
    config_high_pace = default_config
    config_high_pace.assumptions = assumptions_high_pace
    results_high_pace = [simulation.simulate_game(model, "GSW", "LAL", config=config_high_pace) for _ in range(100)]
    avg_total_points_high_pace = np.mean([r["total_points"] for r in results_high_pace])

    assert avg_total_points_high_pace > avg_total_points_default
