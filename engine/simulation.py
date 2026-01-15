# engine/simulation.py

import numpy as np
from .config import SimulationConfig
from .models import SimulationModel
from .game_log import GameLog
from data.teams import TEAM_DATA

def simulate_game(model: SimulationModel, home_team_id: str, away_team_id: str, config: SimulationConfig, log_game: bool = False):
    home_team = TEAM_DATA[home_team_id]
    away_team = TEAM_DATA[away_team_id]
    game_log = GameLog(enabled=log_game)

    # Apply home court advantage
    home_team_sim = {**home_team, "off_rating": home_team["off_rating"] + config.home_court_advantage}
    away_team_sim = {**away_team}

    # Determine game pace
    avg_pace = (home_team_sim["pace"] + away_team_sim["pace"]) / 2.0
    possession_count = int(np.random.normal(avg_pace, config.pace_std_dev))
    possession_count = max(config.min_pace, min(config.max_pace, possession_count))

    home_score = 0
    away_score = 0

    for i in range(possession_count):
        if i % 2 == 0:
            points, outcome = model.get_possession_outcome(home_team_sim, away_team_sim)
            home_score += points
            game_log.record("home", outcome, points)
        else:
            points, outcome = model.get_possession_outcome(away_team_sim, home_team_sim)
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
