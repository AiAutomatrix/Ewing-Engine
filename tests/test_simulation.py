# tests/test_simulation.py

import random
import numpy as np
from engine.simulation import simulate_game
from engine.models import HeuristicModel
from engine.config import default_config
from data.teams import LEAGUE_AVG_OFF_RATING

def test_simulate_game_deterministic():
    """Tests that the simulation is deterministic with a fixed random seed."""
    random.seed(42)
    np.random.seed(42)
    model = HeuristicModel(league_avg_off_rating=LEAGUE_AVG_OFF_RATING)
    result1 = simulate_game(model, "GSW", "LAL", config=default_config)

    random.seed(42)
    np.random.seed(42)
    result2 = simulate_game(model, "GSW", "LAL", config=default_config)

    assert result1["home_score"] == result2["home_score"]
    assert result1["away_score"] == result2["away_score"]

def test_simulate_game_log():
    """Tests that the game log is correctly generated when requested."""
    random.seed(42)
    np.random.seed(42)
    model = HeuristicModel(league_avg_off_rating=LEAGUE_AVG_OFF_RATING)
    result = simulate_game(model, "GSW", "LAL", config=default_config, log_game=True)

    assert "log" in result
    assert isinstance(result["log"], list)
    assert len(result["log"]) > 0
    assert "team" in result["log"][0]
    assert "outcome" in result["log"][0]
    assert "points" in result["log"][0]
