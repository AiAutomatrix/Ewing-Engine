# engine/simulation.py

import numpy as np
from .config import SimulationConfig, default_config
from .models import SimulationModel, HeuristicModel
from .game_log import GameLog
from .metrics import analyze_results
from data.teams import TEAM_DATA, LEAGUE_AVG_OFF_RATING

def run_simulation_with_config(home_team_id: str = "GSW", away_team_id: str = "LAL", num_simulations: int = None, config: SimulationConfig = None, assumptions = None, return_distributions: bool = False):
    """Runs a Monte Carlo simulation with a given configuration."""
    if config is None:
        config = default_config
    
    if assumptions is not None:
        config.assumptions = assumptions
    
    if num_simulations is None:
        num_simulations = config.default_num_simulations

    model = HeuristicModel(league_avg_off_rating=LEAGUE_AVG_OFF_RATING)
    results = [simulate_game(model, home_team_id, away_team_id, config) for _ in range(num_simulations)]
    return analyze_results(results, return_distributions=return_distributions)

def simulate_game(model: SimulationModel, home_team_id: str, away_team_id: str, config: SimulationConfig, log_game: bool = False):
    home_team = TEAM_DATA[home_team_id]
    away_team = TEAM_DATA[away_team_id]
    game_log = GameLog(enabled=log_game)

    # Apply home court advantage from assumptions
    home_court_advantage = config.assumptions.home_court_advantage.value
    home_team_sim = {**home_team, "off_rating": home_team["off_rating"] + home_court_advantage}
    away_team_sim = {**away_team}

    # Determine game pace
    avg_pace = (home_team_sim["pace"] + away_team_sim["pace"]) / 2.0
    pace_modifier = config.assumptions.pace_modifier.value
    final_pace = avg_pace * pace_modifier

    possession_count = int(np.random.normal(final_pace, config.pace_std_dev))
    possession_count = max(config.min_pace, min(config.max_pace, possession_count))

    home_score = 0
    away_score = 0

    for i in range(possession_count):
        if i % 2 == 0:
            points, outcome = model.get_possession_outcome(home_team_sim, away_team_sim, config.assumptions)
            home_score += points
            game_log.record("home", outcome, points)
        else:
            points, outcome = model.get_possession_outcome(away_team_sim, home_team_sim, config.assumptions)
            away_score += points
            game_log.record("away", outcome, points)

    result = {
        "home_score": home_score,
        "away_score": away_score,
        "total_points": home_score + away_score,
        "winner": "home" if home_score > away_score else "away" if away_score > home_score else "draw"
    }

    if log_game:
        result["log"] = game_log.to_dict()
    
    return result
